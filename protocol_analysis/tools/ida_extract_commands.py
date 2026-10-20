# -*- coding: utf-8 -*-
"""
IDA 静态提取器（阶段一：命令全集枚举）
======================================
用途：不依赖任何历史结论，从客户端 exe 静态提取全部 C<->S 协议命令的
      {opcode, 方向, 协议类, 命令名, 代码位置}。

原理（本脚本只做机械提取，不做任何语义猜测）：
  1. 客户端把协议层函数名以字符串形式内联在代码里：
       ")->_proto_<cls>_client::recv_<name>( "
       ")<-_proto_<cls>_client::send_<name>( "
  2. 每个字符串的引用点落在某个函数里：
       - 该函数内出现 >=2 个协议名  ->  recv 分发器（switch(opcode) 实现）
       - 该函数内只有 1 个 send_ 名 ->  C->S 组包函数
  3. S->C 的 opcode：反解分发器的 switch 实现，得到 opcode -> case 块地址；
     case 块归属 = 「不大于名字符串引用点的最大 case 起始地址」。
     switch 的三种形态都要处理（MSVC 常见）：
       a) cmp reg,K ; jg/jz/...            —— 二分比较树
       b) sub reg,BASE ; cmp reg,MAXIDX ; ja def ; movzx reg,byte_TBL[reg]
          ; jmp dword_JPT[reg*4]           —— 二级跳转表（字节表 + 目标表）
  4. C->S 的 opcode：组包函数里 `mov word ptr [buf+0], IMM` 立即数即 opcode；
     报文总长 = `push IMM` + `call <从 [r+78h] 取出的分配器>` 的 IMM。

运行：IDA MCP 的 py_exec_file（静态，不附加调试器、不下断点）
产出：protocol_analysis/_meta/commands_raw.json
"""

import json
import os
import re
import struct
import time

import ida_bytes
import idaapi
import idautils
import idc

ROOT = r'F:\9ymsgo\9you\protocol_analysis'
OUT = os.path.join(ROOT, '_meta', 'commands_raw.json')

# 不改变标志位的指令：允许出现在 cmp 与 jcc 之间
NS = frozenset({
    'mov', 'movzx', 'movsx', 'lea', 'push', 'pop', 'nop', 'xchg',
    'movsd', 'movss', 'movdqu', 'movaps', 'movups', 'prefetchnta',
})
JCC = frozenset({
    'jg', 'ja', 'jge', 'jae', 'jl', 'jb', 'jle', 'jbe',
    'jz', 'je', 'jnz', 'jne',
})

NAME_RE = re.compile(r'_proto_([a-z0-9_]+)::(recv|send)_([A-Za-z0-9_]+)\s*\(')


def dec(ea):
    return idautils.DecodeInstruction(ea)


def mnem(ins):
    return str(ins.get_canon_mnem())


def is_reg(op):
    return op.type == idaapi.o_reg


def is_imm(op):
    return op.type == idaapi.o_imm


def func_of(ea):
    f = idaapi.get_func(ea)
    return f.start_ea if f else None


def func_end(ea):
    return idc.get_func_attr(ea, idc.FUNCATTR_END)


# ----------------------------------------------------------------------------
# 1) 收集协议名字符串
# ----------------------------------------------------------------------------
def collect_names():
    out = []
    for s in idautils.Strings():
        t = str(s)
        m = NAME_RE.search(t)
        if not m:
            continue
        out.append({
            'str_ea': int(s.ea),
            'raw': t,
            'proto': m.group(1),      # auth_client / battle_client / lounge_client
            'direction': m.group(2),  # recv / send
            'name': m.group(3),
        })
    out.sort(key=lambda d: d['str_ea'])
    return out


# ----------------------------------------------------------------------------
# 2) 名字 -> 所在函数；函数 -> 名字集合
# ----------------------------------------------------------------------------
def attach_funcs(names):
    by_func = {}
    for n in names:
        f = None
        for x in idautils.XrefsTo(n['str_ea']):
            g = func_of(x.frm)
            if g is not None:
                f = g
                break
        n['fn'] = f
        if f is not None:
            by_func.setdefault(f, []).append(n)
    return by_func


# ----------------------------------------------------------------------------
# 3) switch 反解：opcode -> case 块起始地址
# ----------------------------------------------------------------------------
def collect_jccs(p, limit=5):
    """从 p 起收集连续的条件跳转（跳过不改变标志位的指令）。"""
    jccs = []
    guard = 0
    while len(jccs) < limit and guard < 24:
        guard += 1
        i2 = dec(p)
        if i2 is None:
            break
        m2 = mnem(i2)
        if m2 in JCC:
            jccs.append((m2, i2.ops[0].addr))
            p += i2.size
            continue
        if m2 in NS:
            p += i2.size
            continue
        break
    return jccs, p


def _narrow(cur, m2, kv):
    """按条件跳转语义收窄 [c0,c1]；返回 (taken_range, new_cur) 。"""
    c0, c1 = cur
    if m2 in ('jg', 'ja'):
        return (max(c0, kv + 1), c1), (c0, min(c1, kv))
    if m2 in ('jge', 'jae'):
        return (max(c0, kv), c1), (c0, min(c1, kv - 1))
    if m2 in ('jl', 'jb'):
        return (c0, min(c1, kv - 1)), (max(c0, kv), c1)
    if m2 in ('jle', 'jbe'):
        return (c0, min(c1, kv)), (max(c0, kv + 1), c1)
    if m2 in ('jz', 'je'):
        return (kv, kv), None
    return None, (kv, kv)  # jnz / jne


def _taken(m2, v, k):
    """给定具体值 v，判断条件跳转是否成立。"""
    if m2 in ('jg', 'ja'):
        return v > k
    if m2 in ('jge', 'jae'):
        return v >= k
    if m2 in ('jl', 'jb'):
        return v < k
    if m2 in ('jle', 'jbe'):
        return v <= k
    if m2 in ('jz', 'je'):
        return v == k
    return v != k  # jnz / jne


def collect_defjumps(start_ea, end_ea):
    """收集该函数内所有 switch 跳转表的默认分支地址（= 无效 opcode 的落点）。"""
    out = set()
    for h in idautils.Heads(start_ea, end_ea):
        ins = dec(h)
        if ins is None or mnem(ins) != 'jmp':
            continue
        o = ins.ops[0]
        if o.type in (idaapi.o_displ, idaapi.o_mem, idaapi.o_phrase):
            si = idaapi.get_switch_info(h)
            if si and si.defjump:
                out.add(si.defjump)
    return out


def concrete_ok(v, ptr, delta, start_ea, end_ea, defjs, step_limit=400):
    """用具体值 v 从 ptr 顺着比较链/跳转表走一遍，判断这条路径是否真的落到一个 case 体。

    - 走到 default/error（switch 的默认分支）或 ret/函数外 ⇒ False（这是伪 case）
    - 走到不属于比较链的指令（即 case 体）或表里直达的 case 块 ⇒ True
    """
    seen = set()
    treg = None
    last_bound = None
    steps = 0
    while steps < step_limit:
        steps += 1
        if ptr in defjs:
            return False
        if ptr < start_ea or ptr >= end_ea:
            return False
        if ptr in seen:
            return True  # 出现回边，按已到达 case 体处理
        seen.add(ptr)
        ins = dec(ptr)
        if ins is None:
            return False
        mn = mnem(ins)
        if mn == 'cmp' and is_reg(ins.ops[0]) and is_imm(ins.ops[1]):
            treg = ins.ops[0].reg
            k = (ins.ops[1].value + delta) & 0xFFFFFFFF
            last_bound = ins.ops[1].value
            jccs, p = collect_jccs(ptr + ins.size)
            hit = False
            for m2, tgt in jccs:
                if _taken(m2, v, k):
                    ptr = tgt
                    hit = True
                    break
            if hit:
                continue
            ptr = p
            continue
        if mn in ('sub', 'add') and is_reg(ins.ops[0]) and is_imm(ins.ops[1]) \
                and (treg is None or ins.ops[0].reg == treg):
            imm = ins.ops[1].value
            delta = (delta + imm) & 0xFFFFFFFF if mn == 'sub' else (delta - imm) & 0xFFFFFFFF
            treg = ins.ops[0].reg
            # sub/add 自身即“与 0 比较”，紧随的条件跳转按 v == delta 判定
            k = delta
            jccs, p = collect_jccs(ptr + ins.size)
            hit = False
            for m2, tgt in jccs:
                if _taken(m2, v, k):
                    ptr = tgt
                    hit = True
                    break
            if hit:
                continue
            ptr = p
            continue
        if mn == 'mov' and is_reg(ins.ops[0]) and is_reg(ins.ops[1]) \
                and treg is not None and ins.ops[1].reg == treg:
            treg = ins.ops[0].reg
            ptr += ins.size
            continue
        if mn == 'jmp':
            o = ins.ops[0]
            if o.type in (idaapi.o_displ, idaapi.o_mem, idaapi.o_phrase):
                si = idaapi.get_switch_info(ptr)
                if si is None:
                    return True
                idx = (v - delta) & 0xFFFFFFFF
                if last_bound is not None and idx > last_bound:
                    ptr = si.defjump
                    continue
                tbl = None
                pv = idc.prev_head(ptr)
                for _ in range(6):
                    if pv < start_ea:
                        break
                    iv = dec(pv)
                    if iv is not None and mnem(iv) in ('movzx', 'movsx'):
                        tbl = idc.get_operand_value(pv, 1)
                        break
                    pv = idc.prev_head(pv)
                if not tbl:
                    return True
                idx2 = ida_bytes.get_wide_byte(tbl + idx)
                tgt = ida_bytes.get_wide_dword((si.jumps or idc.get_operand_value(ptr, 0)) + idx2 * 4)
                if tgt == si.defjump or tgt in defjs:
                    ptr = si.defjump
                    continue
                return start_ea <= tgt < end_ea
            ptr = o.addr
            continue
        if mn in ('retn', 'ret'):
            return False
        if mn in NS:
            ptr += ins.size
            continue
        return True  # 不属于比较链 ⇒ 已到达 case 体
    return False


def resolve_case_map(start_ea, end_ea, node_limit=2000000):
    """返回 (opcode->case地址, 统计, 跳转表报告, 被剔除的伪 case)。"""
    res = {}
    tables = []
    drops = []
    defjs = collect_defjumps(start_ea, end_ea)
    stack = [(start_ea, 0, 0xFFFF, 0, None)]
    seen = set()
    nodes = 0
    while stack:
        a, lo, hi, delta, treg = stack.pop()
        key = (a, lo, hi, delta, treg)
        if key in seen:
            continue
        seen.add(key)
        nodes += 1
        if nodes > node_limit:
            break
        ptr = a
        clo, chi = lo, hi
        last_kv = None
        last_bound = None
        guard = 0
        while guard < 200000:
            guard += 1
            if clo > chi:
                break
            if clo == chi:
                # 区间收窄到单点 ≠ 一定是 case：链尾可能产出伪 case。
                # 用具体值顺链走一遍验证，只有真的落到 case 体才记录。
                if concrete_ok(clo, ptr, delta, start_ea, end_ea, defjs):
                    res[clo] = ptr
                else:
                    drops.append({'opcode': clo, 'ptr': hex(ptr)})
                break
            if ptr >= end_ea:
                break
            ins = dec(ptr)
            if ins is None:
                break
            mn = mnem(ins)
            kv = None
            if mn == 'cmp' and is_reg(ins.ops[0]) and is_imm(ins.ops[1]):
                treg = ins.ops[0].reg
                kv = (ins.ops[1].value + delta) & 0xFFFFFFFF
                last_bound = ins.ops[1].value
            elif mn in ('sub', 'add') and is_reg(ins.ops[0]) and is_imm(ins.ops[1]):
                if treg is not None and ins.ops[0].reg == treg:
                    imm = ins.ops[1].value
                    delta = (delta + imm) & 0xFFFFFFFF if mn == 'sub' else (delta - imm) & 0xFFFFFFFF
                    kv = delta  # 与 0 比较：v == delta
                    last_bound = 0
            elif mn == 'mov' and is_reg(ins.ops[0]) and is_reg(ins.ops[1]):
                if treg is not None and ins.ops[1].reg == treg:
                    treg = ins.ops[0].reg
            elif mn == 'jmp':
                o = ins.ops[0]
                if o.type in (idaapi.o_displ, idaapi.o_mem, idaapi.o_phrase):
                    si = idaapi.get_switch_info(ptr)
                    jpt = idc.get_operand_value(ptr, 0)
                    if si:
                        jpt = si.jumps or jpt
                    # 反向找字节表
                    tbl = None
                    pv = idc.prev_head(ptr)
                    for _ in range(6):
                        if pv < a or pv < start_ea:
                            break
                        iv = dec(pv)
                        if iv is not None and mnem(iv) in ('movzx', 'movsx'):
                            tbl = idc.get_operand_value(pv, 1)
                            break
                        pv = idc.prev_head(pv)
                    real = 0
                    if tbl and jpt and last_bound is not None:
                        defj = si.defjump if si else 0
                        for i in range(0, (last_bound & 0xFFFFFFFF) + 1):
                            idx = ida_bytes.get_wide_byte(tbl + i)
                            tgt = ida_bytes.get_wide_dword(jpt + idx * 4)
                            if tgt == 0 or tgt == defj:
                                continue
                            if not (start_ea <= tgt < end_ea):
                                continue
                            op = (delta + i) & 0xFFFFFFFF
                            if op <= 0xFFFF:
                                res.setdefault(op, tgt)
                                real += 1
                    tables.append({
                        'jmp': hex(ptr), 'byte_tbl': hex(tbl) if tbl else None,
                        'jpt': hex(jpt) if jpt else None,
                        'base': hex(delta), 'maxidx': last_bound,
                        'real_cases': real,
                    })
                break
            if kv is not None:
                jccs, p = collect_jccs(ptr + ins.size)
                cur = (clo, chi)
                dead = False
                for m2, tgt in jccs:
                    taken, newcur = _narrow(cur, m2, kv)
                    if taken is not None and cur[0] <= cur[1]:
                        t0 = max(cur[0], taken[0])
                        t1 = min(cur[1], taken[1])
                        if t0 <= t1:
                            stack.append((tgt, t0, t1, delta, treg))
                    if newcur is None:
                        if m2 in ('jz', 'je'):
                            c0, c1 = cur
                            if c0 <= kv - 1:
                                stack.append((p, c0, min(c1, kv - 1), delta, treg))
                            if kv + 1 <= c1:
                                stack.append((p, kv + 1, c1, delta, treg))
                        dead = True
                        break
                    cur = (max(cur[0], newcur[0]), min(cur[1], newcur[1]))
                    if cur[0] > cur[1]:
                        dead = True
                        break
                if dead:
                    break
                clo, chi = cur
                ptr = p
                continue
            nxt = idc.next_head(ptr, end_ea)
            if nxt <= ptr:
                break
            ptr = nxt
    return res, nodes, tables, drops


def build_recv_entries(by_func):
    cmds = []
    report = []
    for f, items in sorted(by_func.items()):
        if len(items) < 2:
            continue
        dirs = set(i['direction'] for i in items)
        if dirs != {'recv'}:
            report.append({'fn': hex(f), 'note': 'multi-name but mixed dir', 'n': len(items)})
            continue
        proto = items[0]['proto']
        fend = func_end(f)
        t0 = time.time()
        cmap, nodes, tables, drops = resolve_case_map(f, fend)
        secs = round(time.time() - t0, 2)
        starts = sorted(cmap.values())
        report.append({
            'fn': hex(f), 'proto': proto, 'names': len(items),
            'cases_resolved': len(cmap), 'nodes': nodes, 'secs': secs,
            'tables': tables, 'dropped_fake_cases': drops,
        })
        for it in items:
            xref = None
            for x in idautils.XrefsTo(it['str_ea']):
                if func_of(x.frm) == f:
                    xref = x.frm
                    break
            if xref is None:
                continue
            owner = None
            for st in starts:
                if st <= xref:
                    owner = st
                else:
                    break
            opcode = None
            for k, v in cmap.items():
                if v == owner:
                    opcode = k
                    break
            nxt = fend
            for st in starts:
                if st > owner:
                    nxt = st
                    break
            cmds.append({
                'direction': 'SC',
                'opcode': opcode,
                'opcode_hex': ('0x%04X' % opcode) if opcode is not None else None,
                'proto': proto,
                'name': it['name'],
                'handler_fn': hex(f),
                'handler_name': idc.get_func_name(f),
                'case_start': hex(owner) if owner is not None else None,
                'case_end': hex(nxt) if owner is not None else None,
                'namestr_ea': hex(it['str_ea']),
                'namestr_xref': hex(xref),
                'expr': it['raw'],
            })
    return cmds, report


# ----------------------------------------------------------------------------
# 4) C->S 组包函数：opcode / 报文总长
# ----------------------------------------------------------------------------
def scan_send_fn(by_func):
    cmds = []
    for f, items in sorted(by_func.items()):
        if len(items) != 1:
            continue
        it = items[0]
        if it['direction'] != 'send':
            continue
        opcode = None
        opcode_va = None
        total_len = None
        len_va = None
        fend = func_end(f)
        heads = list(idautils.Heads(f, fend))
        for i, h in enumerate(heads):
            ins = dec(h)
            if ins is None:
                continue
            mn = mnem(ins)
            if mn == 'mov' and is_imm(ins.ops[1]) and opcode is None:
                # 目标写法多变：mov word ptr [reg+disp], IMM / mov word ptr [reg], IMM
                if (ins.ops[0].type not in (idaapi.o_reg, idaapi.o_imm, idaapi.o_near)
                        and 'word ptr' in idc.print_operand(h, 0)):
                    opcode = ins.ops[1].value & 0xFFFF
                    opcode_va = h
            if mn == 'call' and is_reg(ins.ops[0]) and i >= 2:
                prev = dec(heads[i - 1])
                if prev is not None and mnem(prev) == 'push' and is_imm(prev.ops[0]):
                    reg = ins.ops[0].reg
                    ok = False
                    for j in range(max(0, i - 8), i):
                        pj = dec(heads[j])
                        if pj is None:
                            continue
                        if (mnem(pj) == 'mov' and is_reg(pj.ops[0])
                                and pj.ops[0].reg == reg
                                and pj.ops[1].type in (idaapi.o_displ, idaapi.o_mem)
                                and '78h' in idc.print_operand(heads[j], 1)):
                            ok = True
                            break
                    if ok and total_len is None:
                        total_len = prev.ops[0].value
                        len_va = heads[i - 1]
        cmds.append({
            'direction': 'CS',
            'opcode': opcode,
            'opcode_hex': ('0x%04X' % opcode) if opcode is not None else None,
            'proto': it['proto'],
            'name': it['name'],
            'send_fn': hex(f),
            'send_fn_name': idc.get_func_name(f),
            'fn_start': hex(f),
            'fn_end': hex(fend),
            'namestr_ea': hex(it['str_ea']),
            'opcode_insn': hex(opcode_va) if opcode_va else None,
            'declared_total_len': total_len,
            'declared_total_len_hex': ('0x%X' % total_len) if total_len is not None else None,
            'len_insn': hex(len_va) if len_va else None,
            'expr': it['raw'],
        })
    return cmds


# ----------------------------------------------------------------------------
# 4b) 不经分发器的 recv 处理函数（由分发器默认分支调用）
#     形态：movzx r, word ptr [buf]  →  紧接着 cmp <16 位寄存器>, IMM
#     例：0xB0C210 处理 _proto_battle::recv_entity_msma_fix，cmp ax, 20F5h
# ----------------------------------------------------------------------------
REG16 = ('ax', 'cx', 'dx', 'bx', 'si', 'di', 'bp', 'sp')


def scan_orphan_recv(by_func):
    cmds = []
    for f, items in sorted(by_func.items()):
        if len(items) != 1 or items[0]['direction'] != 'recv':
            continue
        it = items[0]
        fend = func_end(f)
        opcode = None
        opcode_va = None
        heads = list(idautils.Heads(f, fend))
        pend = None
        for i, h in enumerate(heads):
            ins = dec(h)
            if ins is None:
                continue
            mn = mnem(ins)
            if (mn in ('movzx', 'movsx') and is_reg(ins.ops[0])
                    and 'word ptr' in idc.print_operand(h, 1)):
                pend = (i, ins.ops[0].reg)
                continue
            if (pend is not None and i - pend[0] <= 10 and mn == 'cmp'
                    and is_imm(ins.ops[1]) and is_reg(ins.ops[0])):
                o0 = idc.print_operand(h, 0)
                if o0 in REG16 or ins.ops[0].reg == pend[1]:
                    v = ins.ops[1].value
                    if 0x100 <= v <= 0xFFFF:
                        opcode = v
                        opcode_va = h
                        break
        caller = None
        caller_fn = None
        for x in idautils.XrefsTo(f):
            g = func_of(x.frm)
            if g is not None:
                caller = x.frm
                caller_fn = g
                break
        name_xref = None
        for x in idautils.XrefsTo(it['str_ea']):
            if func_of(x.frm) == f:
                name_xref = x.frm
                break
        cmds.append({
            'direction': 'SC',
            'opcode': opcode,
            'opcode_hex': ('0x%04X' % opcode) if opcode is not None else None,
            'proto': it['proto'],
            'name': it['name'],
            'handler_fn': hex(f),
            'handler_name': idc.get_func_name(f),
            'case_start': hex(f),
            'case_end': hex(fend),
            'namestr_ea': hex(it['str_ea']),
            'namestr_xref': hex(name_xref) if name_xref else None,
            'opcode_insn': hex(opcode_va) if opcode_va else None,
            'dispatch': 'orphan-handler（不经分发器 switch：由分发器默认分支调用）',
            'caller_fn': hex(caller_fn) if caller_fn else None,
            'caller_site': hex(caller) if caller else None,
            'expr': it['raw'],
        })
    return cmds


def main():
    t0 = time.time()
    names = collect_names()
    by_func = attach_funcs(names)
    print('[1] proto 名字符串 %d 条，落在 %d 个函数' % (len(names), len(by_func)))

    recv_cmds, report = build_recv_entries(by_func)
    print('[2] recv 分发器 %d 个' % len(report))
    for r in report:
        print('    ', {k: v for k, v in r.items() if k not in ('tables', 'dropped_fake_cases')})
        for tb in r.get('tables', []):
            print('       table', tb)
        for dp in r.get('dropped_fake_cases', []):
            print('       dropped(fake) opcode=%s ptr=%s' % (hex(dp['opcode']), dp['ptr']))
    print('[3] S->C 命令 %d 条' % len(recv_cmds))

    send_cmds = scan_send_fn(by_func)
    print('[4] C->S 命令 %d 条' % len(send_cmds))

    orphan_cmds = scan_orphan_recv(by_func)
    print('[5] 不经分发器的 recv（由默认分支调用）%d 条' % len(orphan_cmds))
    for o in orphan_cmds:
        print('    ', {'fn': o['handler_fn'], 'opcode': o['opcode_hex'], 'name': o['name'],
                       'caller': o['caller_fn'], 'call': o['caller_site'],
                       'opcode_insn': o['opcode_insn']})
    recv_cmds = recv_cmds + orphan_cmds

    n_no_op = len([c for c in recv_cmds if c['opcode'] is None])
    print('[6] S->C 命令 %d 条，未解出 opcode: %d 条' % (len(recv_cmds), n_no_op))

    data = {
        'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'idb': idc.get_idb_path(),
        'input': idc.get_input_file_path(),
        'imagebase': hex(idaapi.get_imagebase()),
        'counts': {
            'sc': len(recv_cmds),
            'cs': len(send_cmds),
            'total': len(recv_cmds) + len(send_cmds),
            'sc_without_opcode': n_no_op,
            'sc_orphan_handler': len(orphan_cmds),
        },
        'dispatchers': report,
        'orphan_recv': orphan_cmds,
        'commands': recv_cmds + send_cmds,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=1)
    print('[OK] 写出 %s  用时 %.1fs' % (OUT, time.time() - t0))


main()
