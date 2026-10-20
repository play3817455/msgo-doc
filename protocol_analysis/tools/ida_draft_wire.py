# -*- coding: utf-8 -*-
"""
ida_draft_wire.py —— 逐条命令「机械提取」线格式草案（阶段二批量化）
====================================================================
对全部 915 条命令，从 exe 里机械提取字段序列（偏移 / 宽度 / 类型 / 证据 VA），
产出**草案**，供人工按规范补齐「含义 / 用途」后转 DONE。

严格边界（规范 §6）：
  * 只做机械提取，**不猜含义**；草案里 含义/用途 一律写 `待定`；
  * 类型一律来自汇编（读取器宽度 / 内联 movzx 的 size 关键字 / 寄存器宽度）；
  * 状态写 `DRAFT`（机器草案，未过质量门 G3/G5），绝不冒充 DONE。

IO 原语（由函数体形态自动识别：无 call + 唯一的 `add <mem>, IMM(1|2|4|8)`）：
  读：0xB02DD0=4 / 0xB02DF0=2 / 0xB06230=1   （带边界检查，cursor={cur@0,end@4}）
      0xB41470=4 / 0xB413B0=2 / 0xB05E30=1   （无边界检查，__thiscall，retn 4）
      0xB05E40=2 / 0xB05EA0=1 / 0xB41850=4   （定长数组读取器，循环 N 次）
  写：0xB02D80=4 / 0xB02DA0=2 / 0xB061C0=1
      0xB02B40 = 变长串：内容 edi 字节 + 1 字节 NUL（edi = sub_C85E30(src, N)）

运行：IDA MCP 的 py_exec_file
产出：_meta/wire_draft.json
      commands/<cmd>/draft-wire.md      （字段表 + 汇编证据序列）
      commands/<cmd>/draft-fields.csv   （机器可读草案字段表）
      commands/<cmd>/README.md          （仅把 状态：TODO 改成 状态：DRAFT）
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTOR = os.path.join(HERE, 'ida_extract_commands.py')
_src = open(EXTRACTOR, encoding='utf-8').read().replace('\nmain()\n', '\n')
_ns = {}
exec(compile(_src, EXTRACTOR, 'exec'), _ns)

import idaapi  # noqa: E402
import idautils  # noqa: E402
import idc  # noqa: E402

ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, '_meta', 'commands_raw.json')
OUT = os.path.join(ROOT, '_meta', 'wire_draft.json')
CMDS = os.path.join(ROOT, 'commands')

dec = _ns['dec']
mnem = _ns['mnem']
is_reg = _ns['is_reg']
is_imm = _ns['is_imm']
func_end = _ns['func_end']

MEMK = (idaapi.o_displ, idaapi.o_mem, idaapi.o_phrase)
ALLOWLIST = frozenset({0xABB2F0, 0xCA0CE0})  # 缓冲包装 / 游标复位（非字段 IO）
REG_W = {'al': 1, 'cl': 1, 'dl': 1, 'bl': 1, 'ah': 1, 'bh': 1, 'ch': 1, 'dh': 1,
         'ax': 2, 'cx': 2, 'dx': 2, 'bx': 2, 'si': 2, 'di': 2, 'bp': 2, 'sp': 2,
         'eax': 4, 'ecx': 4, 'edx': 4, 'ebx': 4, 'esi': 4, 'edi': 4, 'ebp': 4, 'esp': 4}


# ---------------------------------------------------------------------------
# IO 原语识别
# ---------------------------------------------------------------------------
_io_cache = {}


def io_width(fn):
    """识别 IO 原语。

    返回 (kind, 宽度, 是否数组)：
      kind = 'bounded'  ｜ 带边界检查（cmp + jcc）⇒ **真实字段读/写**，宽度取游标步进
             'reserve'  ｜ 无边界检查、仅推进游标 ⇒ 只做「解码缓冲预留」，**不是字段**
             'blob'     ｜ 内部 call memcpy(sub_CC56B0) ⇒ 变长串/字节块
    非 IO 原语返回 None。
    """
    if fn in _io_cache:
        return _io_cache[fn]
    res = None
    g = idaapi.get_func(fn)
    if g is not None and 0 < (g.end_ea - g.start_ea) <= 96:
        widths = []
        has_call = False
        has_cmp = False
        has_memcpy = False
        for h in idautils.Heads(g.start_ea, g.end_ea):
            ins = dec(h)
            if ins is None:
                continue
            mn = mnem(ins)
            if mn == 'call':
                has_call = True
                if ins.ops[0].addr == 0xCC56B0:
                    has_memcpy = True
            if mn == 'cmp':
                has_cmp = True
            if (mn == 'add' and ins.ops[0].type in MEMK
                    and is_imm(ins.ops[1]) and ins.ops[1].value in (1, 2, 4, 8)):
                widths.append(ins.ops[1].value)
        if has_memcpy:
            res = ('blob', None, False)
        elif not has_call and len(widths) == 1:
            res = ('bounded' if has_cmp else 'reserve',
                   widths[0], (g.end_ea - g.start_ea) >= 40)
    _io_cache[fn] = res
    return res


def type_name(w):
    return {1: 'u8', 2: 'u16', 4: 'u32', 8: 'u64'}.get(w, 'u%d' % (w * 8))


def operand_width_of_reg(txt):
    return REG_W.get(txt.strip().lower())


# esp / ebp -- any operand based on these is a stack slot, never a wire field.
STACK_REGS = (4, 5)


def wire_mem_operand(ptr, ins, index, off):
    """Does `ins.ops[index]` access the wire buffer inline at the running offset?

    `o_phrase` is displacement-free addressing (`[eax]`) and is taken as before.
    `o_displ` carries a displacement (`[eax+4]`, `[esp+48h+var_30]`, `[edi+7DDCh]`)
    and is accepted only when that displacement **is** the running wire offset --
    i.e. the operand addresses the frame absolutely. That single test is what keeps
    locals and object members out, and it is why dropping every `o_displ` (the
    previous behaviour) lost the high half of every 64-bit id: `mov [eax], esi` was
    recorded and `mov [eax+4], esi` was not, so `off` never advanced and every later
    field was reported 4 bytes low. Confirmed against the client's own frame size --
    `CS-0x0519` pushes 0xA for a body the draft called 4 and the analysis called 8.
    See `emulab/audit_raw.py` for the row-level audit this serves.
    """
    op = ins.ops[index]
    if op.type == idaapi.o_phrase:
        return True
    if op.type != idaapi.o_displ:
        return False
    return off is not None and op.reg not in STACK_REGS and op.addr == off


# ---------------------------------------------------------------------------
# SC：从 case 块里提读取序列
# ---------------------------------------------------------------------------
def find_alloc(heads, i0, end):
    """定位 `push CAP; call <reg>`（reg 来自 [obj+78h]）→ 返回 (下标, CAP)。"""
    for i in range(i0, len(heads)):
        ins = dec(heads[i])
        if ins is None or mnem(ins) != 'call' or not is_reg(ins.ops[0]):
            continue
        if i == 0:
            continue
        prev = dec(heads[i - 1])
        if prev is None or mnem(prev) != 'push' or not is_imm(prev.ops[0]):
            continue
        reg = ins.ops[0].reg
        for j in range(max(0, i - 8), i):
            pj = dec(heads[j])
            if (pj is not None and mnem(pj) == 'mov' and is_reg(pj.ops[0])
                    and pj.ops[0].reg == reg and pj.ops[1].type in MEMK
                    and '78h' in idc.print_operand(heads[j], 1)):
                return i + 1, prev.ops[0].value
    return None, None


def _success_next(ptr, hi, limit=8):
    """IO 调用之后：找 `test al, al` + 条件跳转，返回「成功(al!=0)分支」的地址。

    生成代码里失败会跳走：
        test al, al ; jz  <错误>   ⇒ 成功 = 顺序（落空）
        test al, al ; jnz <成功>   ⇒ 成功 = 跳转目标
    找不到就返回顺序位置，避免死循环。
    """
    p = ptr
    for _ in range(limit):
        if p is None or p >= hi:
            return None
        ins = dec(p)
        if ins is None:
            return None
        mn = mnem(ins)
        if mn == 'test' and is_reg(ins.ops[0]) and is_reg(ins.ops[1]):
            n = idc.next_head(p, hi)
            for _ in range(4):
                if n is None or n >= hi:
                    break
                i2 = dec(n)
                if i2 is None:
                    break
                m2 = mnem(i2)
                if m2 in ('jz', 'je'):
                    return idc.next_head(n, hi)
                if m2 in ('jnz', 'jne'):
                    return i2.ops[0].addr
                if m2 in ('mov', 'lea', 'pop', 'add'):
                    n = idc.next_head(n, hi)
                    continue
                break
            return idc.next_head(p, hi)
        if mn in ('call', 'retn', 'ret', 'jmp'):
            return None
        p = idc.next_head(p, hi)
    return None


def branch_target(ins):
    """条件跳转的目标地址（`jmp` 返回 None——它是块结束，扫描本来就停）。

    线性扫描没有 CFG：`jz/jnz/...` 只是被顺次跳过，于是 `if`/`switch` 两条臂的字段
    会被**串在一起**，草案就比定稿长出一截。这种偏离不是人工写错，是扫描器的已知盲区，
    所以要把「跨过条件跳转」这件事记下来，交 `emulab/audit_raw.py` 单独归类。
    """
    mn = mnem(ins)
    if mn == 'jmp' or not mn.startswith('j'):
        return None
    if ins.ops and ins.ops[0].type in (idaapi.o_near, idaapi.o_far):
        return ins.ops[0].addr
    return None


def extract_sc(c):
    f = int(c['handler_fn'], 16)
    lo = int(c.get('case_start') or c['handler_fn'], 16)
    hi = int(c.get('case_end') or hex(func_end(f)), 16)
    heads = list(idautils.Heads(lo, hi))
    start, cap = find_alloc(heads, 0, hi)
    if start is None or start >= len(heads):
        return {'fields': [], 'note': '未找到解码缓冲分配点（无法定位字段窗口）',
                'seq': [], 'stop': None, 'cap': None}
    ptr = heads[start]
    fields, ev = [], []
    off = 0
    stopped = None
    branchy = []
    steps = 0
    while ptr is not None and lo <= ptr < hi and steps < 4000:
        steps += 1
        ins = dec(ptr)
        if ins is None:
            break
        mn = mnem(ins)
        nxt = idc.next_head(ptr, hi)
        bt = branch_target(ins)
        if bt is not None and lo <= bt < hi:
            branchy.append(hex(ptr))
        if mn == 'call':
            tgt = ins.ops[0].addr
            if tgt in ALLOWLIST:
                ptr = nxt
                continue
            k = io_width(tgt)
            if k is None:
                stopped = (ptr, 'call %s（非 IO）' % idc.get_func_name(tgt))
                break
            kind, w, arr = k
            nm = idc.get_func_name(tgt)
            if kind == 'reserve':
                # 只推进「解码缓冲」游标，真正的取值由随后的 bounded 读取器完成
                ev.append((ptr, 'call %s → 解码缓冲预留 %s（非字段）' % (nm, type_name(w))))
                ptr = nxt
                continue
            if kind == 'blob':
                fields.append({'off': off, 'len': None, 'type': 'bytes',
                               'array': False, 'ev': hex(ptr)})
                off = None
                ev.append((ptr, 'call %s → 变长串/字节块（NUL 结尾）' % nm))
            else:
                fields.append({'off': off, 'len': w, 'type': type_name(w),
                               'array': arr, 'ev': hex(ptr)})
                if off is not None:
                    off += w
                ev.append((ptr, 'call %s → 读 %s%s' % (nm, type_name(w), '（数组）' if arr else '')))
            sn = _success_next(nxt, hi)
            ptr = sn if (sn is not None and lo <= sn < hi) else nxt
            continue
        if mn in ('movzx', 'movsx') and is_reg(ins.ops[0]) and wire_mem_operand(ptr, ins, 1, off):
            txt = idc.print_operand(ptr, 1)
            w = 1 if 'byte ptr' in txt else (2 if 'word ptr' in txt else (4 if 'dword ptr' in txt else None))
            if w:
                signed = mn == 'movsx'
                fields.append({'off': off, 'len': w, 'type': ('i%d' if signed else 'u%d') % (w * 8),
                               'array': False, 'ev': hex(ptr)})
                if off is not None:
                    off += w
                ev.append((ptr, '%s %s → 内联读 %s' % (mn, txt, ('i%d' if signed else 'u%d') % (w * 8))))
            ptr = nxt
            continue
        if mn == 'mov' and is_reg(ins.ops[0]) and wire_mem_operand(ptr, ins, 1, off):
            if operand_width_of_reg(idc.print_operand(ptr, 1)) == 4:
                fields.append({'off': off, 'len': 4, 'type': 'u32', 'array': False, 'ev': hex(ptr)})
                if off is not None:
                    off += 4
                ev.append((ptr, 'mov %s → 内联读 u32' % idc.print_operand(ptr, 1)))
            ptr = nxt
            continue
        if mn in ('retn', 'ret', 'jmp'):
            stopped = (ptr, mn)
            break
        ptr = nxt
    return {'fields': fields, 'cap': cap, 'branchy': branchy,
            'stop': stopped, 'seq': [(hex(a), s) for a, s in ev]}


# ---------------------------------------------------------------------------
# CS：从组包函数里提写入序列
# ---------------------------------------------------------------------------
def extract_cs(c):
    f = int(c['fn_start'], 16)
    hi = int(c['fn_end'], 16)
    heads = list(idautils.Heads(f, hi))
    start, cap = find_alloc(heads, 0, hi)
    if start is None or start >= len(heads):
        return {'fields': [], 'note': '未找到缓冲分配点（无法定位字段窗口）',
                'seq': [], 'stop': None, 'cap': None, 'branchy': []}
    ptr = heads[start]
    fields, ev = [], []
    off = 0
    stopped = None
    branchy = []
    steps = 0
    while ptr is not None and f <= ptr < hi and steps < 4000:
        steps += 1
        ins = dec(ptr)
        if ins is None:
            break
        mn = mnem(ins)
        nxt = idc.next_head(ptr, hi)
        bt = branch_target(ins)
        if bt is not None and f <= bt < hi:
            branchy.append(hex(ptr))
        if mn == 'call':
            tgt = ins.ops[0].addr
            if tgt in ALLOWLIST:
                ptr = nxt
                continue
            k = io_width(tgt)
            nm = idc.get_func_name(tgt)
            if k is None:
                if tgt == 0xB02FF0:
                    stopped = (ptr, 'call sub_B02FF0（提交/发送）')
                else:
                    stopped = (ptr, 'call %s（非 IO）' % nm)
                break
            kind, w, arr = k
            if kind == 'reserve':
                ev.append((ptr, 'call %s → 缓冲预留 %s（非字段）' % (nm, type_name(w))))
                ptr = nxt
                continue
            if kind == 'blob':
                prev = dec(idc.prev_head(ptr, f)) if ptr > f else None
                n = prev.ops[0].value if (prev is not None and mnem(prev) == 'push'
                                          and is_imm(prev.ops[0])) else None
                fields.append({'off': off, 'len': None, 'type': 'bytes',
                               'array': False, 'ev': hex(ptr), 'max': n})
                off = None
                ev.append((ptr, 'call %s → 变长串（≤%s 字节 + 1 字节 NUL）'
                           % (nm, n if n is not None else '?')))
            else:
                fields.append({'off': off, 'len': w, 'type': type_name(w),
                               'array': arr, 'ev': hex(ptr)})
                if off is not None:
                    off += w
                ev.append((ptr, 'call %s → 写 %s%s' % (nm, type_name(w), '（数组）' if arr else '')))
            sn = _success_next(nxt, hi)
            ptr = sn if (sn is not None and f <= sn < hi) else nxt
            continue
        if mn == 'mov' and ins.ops[0].type in MEMK and is_reg(ins.ops[1]):
            if wire_mem_operand(ptr, ins, 0, off):
                t = idc.print_operand(ptr, 0)
                if 'word ptr' in t:
                    w = 2
                else:
                    w = operand_width_of_reg(idc.print_operand(ptr, 1))
                if w in (1, 2, 4):
                    fields.append({'off': off, 'len': w, 'type': type_name(w),
                                   'array': False, 'ev': hex(ptr)})
                    if off is not None:
                        off += w
                    ev.append((ptr, 'mov %s → 内联写 %s' % (t, type_name(w))))
            ptr = nxt
            continue
        if mn in ('retn', 'ret', 'jmp'):
            stopped = (ptr, mn)
            break
        ptr = nxt
    return {'fields': fields, 'cap': cap, 'stop': stopped, 'branchy': branchy,
            'seq': [(hex(a), s) for a, s in ev]}


# ---------------------------------------------------------------------------
# 产物写出
# ---------------------------------------------------------------------------
STATUS_RE = re.compile(r'(> 状态：`)(?:TODO|DRAFT)(`)')

# 草案文件默认只服务 TODO/DRAFT 命令的迭代，DONE 的命令不重写（人工结论已定稿）。
# 但 2026-09 修掉了下面的 o_displ 盲区之后，需要把**全部**命令的草案重建一遍，
# 才能让草案成为一份与定稿对得上的对照面（`emulab/audit_raw.py` 就是拿它对账的）。
# 遂置 True 重跑一次；**README 的状态位仍不碰**（那是人工结论，不是生成物）。
FORCE_REWRITE = True


def write_draft(c, d):
    folder = os.path.join(CMDS, c['_folder'])
    if not os.path.isdir(folder):
        return False
    p0 = os.path.join(folder, 'README.md')
    marked = True
    if os.path.exists(p0):
        with open(p0, encoding='utf-8') as fp:
            head = fp.read(2000)
        marked = ('> 状态：`TODO`' in head or '> 状态：`DRAFT`' in head)
    if not marked and not FORCE_REWRITE:
        return False
    rows = []
    for i, fld in enumerate(d['fields'], 1):
        off = '?' if fld['off'] is None else fld['off']
        ln = '?' if not fld['len'] else fld['len']
        rows.append('%d,%s,%s,%s,%s,待定,待定,-,%s,类型确证/含义待定'
                    % (i, off, ln, fld['type'] + ('[]' if fld.get('array') else ''),
                       'f_%s' % (off if off != '?' else i), fld['ev']))
    head = '序号,偏移,长度,线类型,字段名,含义,用途,取值或枚举,证据VA,置信度\n'
    with open(os.path.join(folder, 'draft-fields.csv'), 'w', encoding='utf-8', newline='') as fp:
        fp.write(head + ('\n'.join(rows) + '\n' if rows else ''))

    # 自校验：S→C 容量 == 负载长；C→S 容量 == 负载长 + 2（opcode）
    fixed = bool(d['fields']) and all(f['len'] and not f.get('array') for f in d['fields'])
    total = sum(f['len'] for f in d['fields']) if fixed else None
    cap = d.get('cap')
    if fixed and cap:
        d['sum'] = total
        if c['direction'] == 'SC':
            # S→C：容量 == 负载长 是强证据；容量更宽只是「未证伪」（列表/上限型命令）
            if total == cap:
                d['self_check'] = 'PASS'
            elif total < cap:
                d['self_check'] = 'PASS(容量更宽/未证伪)'
            else:
                d['self_check'] = 'FAIL(超容量)'
        else:
            # C→S：组包缓冲容量只是「预留上限」，只要求 容量 >= 负载 + 2(opcode)
            d['self_check'] = 'PASS(容量≥线长)' if cap >= total + 2 else 'FAIL(超容量)'
    else:
        d['self_check'] = 'N/A'

    lines = ['# 机器草案：线格式 —— %s' % c['_folder'], '',
             '> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。',
             '> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。',
             '> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。', '',
             '## 命令', '',
             '| 项 | 值 |', '|---|---|',
             '| opcode | `%s` |' % (c['opcode_hex'] or '?'),
             '| 方向 | %s |' % c['direction'],
             '| 协议类 | `%s` |' % c['proto'],
             '| 命令名 | `%s` |' % c['name'],
             '| 代码位置 | `%s`..`%s` |' % (c.get('case_start') or c.get('fn_start'),
                                            c.get('case_end') or c.get('fn_end')),
             '| 声明容量 | `%s` |' % (('0x%X' % d['cap']) if d.get('cap') else '-'),
             '| 字段总长 | %s |' % (('**%d** 字节' % d['sum']) if d.get('sum') is not None
                                    else '含变长/数组字段，无法直接求和'),
             '| **自校验** | **%s**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）'
             % d['self_check'], '']
    if d.get('branchy'):
        lines += ['| **分支** | ⚠ 扫描跨过 %d 处条件跳转（%s）——线性扫描会把另一条臂的字段'
                  '也串进来，**本草案的尾部字段不可信**，以定稿为准 |'
                  % (len(d['branchy']), ', '.join('`%s`' % a for a in d['branchy'][:6])), '']
    if d.get('note'):
        lines += ['> **注**：%s' % d['note'], '']
    lines += ['## 草案字段表（机器提取）', '',
              '| # | 偏移 | 长度 | 线类型 | 证据VA |', '|---|---|---|---|---|']
    for i, fld in enumerate(d['fields'], 1):
        lines.append('| %d | %s | %s | %s | `%s` |'
                     % (i, '?' if fld['off'] is None else fld['off'],
                        fld['len'] or '?',
                        fld['type'] + ('[]' if fld.get('array') else ''),
                        fld['ev']))
    if not d['fields']:
        lines.append('| — | — | — | — | （未提取到字段） |')
    lines += ['', '## 汇编证据序列（按线序）', '', '```asm']
    for a, s in d['seq']:
        lines.append('; %s  %s' % (a, s))
    if not d['seq']:
        lines.append('; （无）')
    if d.get('stop'):
        lines.append('; —— 扫描停止于 %s：%s' % (hex(d['stop'][0]), d['stop'][1]))
    lines += ['```', '']
    with open(os.path.join(folder, 'draft-wire.md'), 'w', encoding='utf-8', newline='') as fp:
        fp.write('\n'.join(lines))

    p = os.path.join(folder, 'README.md')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as fp:
            txt = fp.read()
        new = STATUS_RE.sub(r'\1DRAFT\2', txt, count=1)
        if new != txt:
            with open(p, 'w', encoding='utf-8', newline='') as fp:
                fp.write(new)
    return True


def main():
    data = json.load(open(RAW, encoding='utf-8'))
    cmds = data['commands']
    out = []
    n_ok = 0
    n_field = 0
    n_empty = 0
    for c in cmds:
        c['_folder'] = '%s-%s-%s-%s' % (c['direction'], c.get('opcode_hex') or '0x----',
                                        (c.get('proto') or '?').replace('_client', ''), c['name'])
        d = extract_cs(c) if c['direction'] == 'CS' else extract_sc(c)
        d['folder'] = c['_folder']
        d['opcode_hex'] = c['opcode_hex']
        d['name'] = c['name']
        out.append(d)
        if write_draft(c, d):
            n_ok += 1
        if d['fields']:
            n_field += 1
            for f in d['fields']:
                if f.get('len') is None:
                    n_empty += 1
        else:
            n_empty += 1
    with open(OUT, 'w', encoding='utf-8') as fp:
        json.dump({'generated_at': __import__('time').strftime('%Y-%m-%d %H:%M:%S'),
                   'count': len(out), 'drafts': out}, fp, ensure_ascii=False, indent=1)
    print('[OK] 草案 %d 条；有字段 %d 条；无字段/变长 %d 处' % (n_ok, n_field, n_empty))
    for tag in ('SC', 'CS'):
        grp = [x for x in out if x['folder'].startswith(tag + '-')]
        pa = [x for x in grp if (x.get('self_check') or '').startswith('PASS')]
        fa = [x for x in grp if x.get('self_check') == 'FAIL']
        na = [x for x in grp if x.get('self_check') == 'N/A']
        print('[%s] 共 %d：自校验 PASS %d / FAIL %d / N/A(含变长或数组) %d'
              % (tag, len(grp), len(pa), len(fa), len(na)))
    print('[OK] 写出 %s' % OUT)


main()
