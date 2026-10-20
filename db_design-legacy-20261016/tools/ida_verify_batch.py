# -*- coding: utf-8 -*-
"""ida_verify_batch.py —— 在 IDA 内批量取「六项复核」的**原始证据切片**（只读，不改 IDA 任何东西）。

运行方式：IDA MCP 的 `py_exec_file`，参数为本文件的绝对路径
          `f:\\9ymsgo\\9you\\db_design\\tools\\ida_verify_batch.py`

输入：`db_design/schema/commands/_meta/_verify_job.json`（由 `tools/verify_commands_ida.py plan` 写）
    {
      "out_dir": ".../schema/commands/_verify/_raw",
      "insn_cap": 1500,          # 单命令块内指令上限（超出记 truncated）
      "callee_insn_cap": 400,    # 单个被调函数体上限
      "targets": [ {id, direction, proto, opcode, block:[lo,hi], handler_va}, ... ]
    }

输出：`<out_dir>/<id>.json`（每命令一份，含块内逐条指令 + 引用字符串 + 一级被调函数体）

设计口径
--------
* **只 dump 事实，不做判断**：容量/守卫/闭合点/去向槽的判定全部由本地
  `tools/verify_commands_ida.py ingest` 完成，便于在不动 IDA 的前提下迭代规则。
* 指令文本**已剥离行尾 ASCII 注释**（`push 4Ch ; char` ⇒ `push 4Ch`）——这是
  `protocol_analysis/_meta/长期记忆.md` 第 ⑲ 坑；数值另经 `get_operand_value` 结构化取出。
* 被调函数体只深度取 **1 层**，且仅限协议 IO 家族地址段（见 FAMILY）；
  更深的复合读取器链由 `schema/composites/` 负责，不在此重复。
"""

import json
import os
import time

import ida_bytes
import ida_funcs
import idaapi
import idautils
import idc

JOBD = r'F:\9ymsgo\9you\db_design\schema\commands\_meta\_verify_job.json'

# 协议 IO 家族地址段（被调函数体只在这两段里取）：
#   0xB02xxx~0xB06xxx = 读写原语 / 复合读取器 / 写入器 / 守卫 / 提交
#   0xB4xxxx          = lounge 侧的读取器、写入器、结构体打印器
FAMILY = ((0xB02000, 0xB0C100), (0xB40000, 0xB50000))


def dec(ea):
    return idautils.DecodeInstruction(ea)


def mnem_of(ins):
    return str(ins.get_canon_mnem())


def _disasm_text(ea):
    """反汇编文本，**剥离行尾注释**（第 ⑲ 坑）。"""
    line = ''
    try:
        import ida_lines
        line = ida_lines.tag_remove(ida_lines.generate_disasm_line(ea, 0))
    except Exception:
        try:
            import ida_lines
            line = ida_lines.tag_remove(idc.generate_disasm_line(ea, 0))
        except Exception:
            try:
                line = idc.GetDisasm(ea) or ''
            except Exception:
                line = ''
    if not line:
        return ''
    # 剥离 `; xxx` 注释（IDA 对可打印立即数会写 `push 4Ch ; char`）
    for sep in (';',):
        i = line.find(sep)
        if i >= 0:
            line = line[:i]
    return line.strip()


_STR_CACHE = {}


def resolve_string(ea):
    """把一个立即数当地址试读字符串字面量；读不到返回 None。"""
    if ea is None or ea < 0x400000 or ea > 0x20000000:
        return None
    if ea in _STR_CACHE:
        hit = _STR_CACHE[ea]
        return hit if hit != '' else None
    out = None
    try:
        if ida_bytes.is_loaded(ea):
            raw = ida_bytes.get_strlit_contents(ea, -1, 0)
            if raw:
                try:
                    txt = raw.decode('utf-8')
                except Exception:
                    txt = raw.decode('latin-1', 'replace')
                if txt and all(31 < ord(ch) or ch in '\t' for ch in txt):
                    out = txt
    except Exception:
        out = None
    _STR_CACHE[ea] = out if out is not None else ''
    return out


def dump_insn(ea, strings):
    """一条指令 → [ea, mnem, text, ops, str_idx]。ops = [[type, value, text], ...]。"""
    ins = dec(ea)
    text = _disasm_text(ea)
    if ins is None:
        return [ea, '', text, [], -1]
    ops = []
    str_idx = -1
    try:
        n = len(ins.ops)
    except Exception:
        try:
            n = ins.ops.size()
        except Exception:
            n = 6
    for k in range(n):
        op = ins.ops[k]
        try:
            op_text = idc.print_operand(ea, k) or ''
        except Exception:
            op_text = ''
        try:
            val = idc.get_operand_value(ea, k)
        except Exception:
            val = 0
        ops.append([int(op.type), int(val), op_text])
        if str_idx < 0 and op.type in (idaapi.o_imm, idaapi.o_mem):
            s = resolve_string(val)
            if s:
                if s not in strings:
                    strings.append(s)
                str_idx = strings.index(s)
    return [ea, mnem_of(ins), text, ops, str_idx]


def in_family(ea):
    for lo, hi in FAMILY:
        if lo <= ea < hi:
            return True
    return False


def dump_block(lo, hi, strings, cap):
    out = []
    ea = lo
    truncated = False
    while ea != idc.BADADDR and ea < hi:
        if len(out) >= cap:
            truncated = True
            break
        out.append(dump_insn(ea, strings))
        nxt = idc.next_head(ea, hi)
        if nxt == idc.BADADDR or nxt <= ea:
            break
        ea = nxt
    return out, truncated


def callee_targets(insns):
    seen = []
    for rec in insns:
        if rec[1] != 'call':
            continue
        for t, v, x in rec[3]:
            if t == idaapi.o_near and in_family(v) and v not in seen:
                seen.append(v)
    return seen


def collect_callees(insns, strings, cap, cache):
    target_vas = callee_targets(insns)
    out = {}
    # 只取 1 层：对块内 call 目标逐个取函数体；函数体内部再出现的 call 不再展开
    for tgt in target_vas:
        key = str(tgt)
        if key in cache:
            out[key] = cache[key]
            continue
        g = ida_funcs.get_func(tgt)
        if g is None:
            continue
        body, trunc = dump_block(g.start_ea, g.end_ea, strings, cap)
        rec = {
            'name': (ida_funcs.get_func_name(g.start_ea) or ''),
            'start': g.start_ea,
            'end': g.end_ea,
            'insns': body,
            'truncated': trunc,
        }
        cache[key] = rec
        out[key] = rec
    return out


def resolve_range(t):
    """命令的扫描区间：块范围优先；C→S 无块（block=null）时退化为「处理函数整函数」。"""
    blk = t.get('block')
    if blk and len(blk) == 2 and blk[0]:
        return int(str(blk[0]), 16), int(str(blk[1]), 16), 'block'
    hv = t.get('handler_va')
    if hv:
        g = ida_funcs.get_func(int(str(hv), 16))
        if g is not None:
            return g.start_ea, g.end_ea, 'handler_func'
    raise ValueError('无块范围且无可用处理函数：%r' % (t,))


def main():
    with open(JOBD, encoding='utf-8') as fp:
        job = json.load(fp)
    out_dir = job['out_dir']
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    insn_cap = int(job.get('insn_cap') or 1500)
    callee_cap = int(job.get('callee_insn_cap') or 400)
    cache = {}
    ok = 0
    bad = []
    for t in job['targets']:
        cid = t['id']
        try:
            lo, hi, how = resolve_range(t)
            strings = []
            insns, trunc = dump_block(lo, hi, strings, insn_cap)
            callees = collect_callees(insns, strings, callee_cap, cache)
            doc = {
                'id': cid,
                'direction': t.get('direction'),
                'proto': t.get('proto'),
                'opcode': t.get('opcode'),
                'handler_va': t.get('handler_va'),
                'block': [hex(lo), hex(hi)],
                'range_from': how,
                'insn_cap': insn_cap,
                'callee_insn_cap': callee_cap,
                'block_truncated': trunc,
                'insns': insns,
                'strings': strings,
                'callees': callees,
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            }
            with open(os.path.join(out_dir, cid + '.json'), 'w', encoding='utf-8') as fp:
                json.dump(doc, fp, ensure_ascii=False)
            ok += 1
        except Exception as exc:  # 单条失败不影响整批
            bad.append('%s: %r' % (cid, exc))
    print('[OK] 原始切片写出 %d 份 → %s' % (ok, out_dir))
    if bad:
        print('[WARN] 失败 %d 条：' % len(bad))
        for b in bad[:20]:
            print('  - %s' % b)


main()
