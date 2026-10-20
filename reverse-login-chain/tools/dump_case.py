# -*- coding: utf-8 -*-
"""按 case 入口地址反汇编整个 case 体（IDA 静态）。

读 `reverse-login-chain/tools/_case_addrs.txt`（每行一个十六进制 entry，可用 `# 注释`）。
case 终点 = 分发函数里"下一个 case 起点"（`push <gate>; mov ecx,esi; call sub_B41120`）。

运行：IDA MCP 的 py_exec_file
"""
import os
import idc
import ida_ua
import ida_funcs

ROOT = r"F:\9ymsgo\9you"
ADDRS = os.path.join(ROOT, "reverse-login-chain", "tools", "_case_addrs.txt")
GATE_FN = 0xB41120
MAXINS = 260


def line(ea):
    return idc.generate_disasm_line(ea, 0) or ""


def case_starts(f):
    """扫一遍函数，找出所有"case 起点"（= gate 调用的 push 地址）。"""
    s, en = f.start_ea, f.end_ea
    out = []
    prev = []
    cur = s
    while cur < en:
        insn = ida_ua.insn_t()
        ln = ida_ua.decode_insn(insn, cur)
        if ln == 0:
            cur += 1
            continue
        mnem = idc.print_insn_mnem(cur)
        if mnem == "call" and idc.get_operand_value(cur, 0) == GATE_FN:
            if len(prev) >= 2 and prev[-1][1] == "mov" and prev[-2][1] == "push":
                out.append(prev[-2][0])
        prev.append((cur, mnem))
        if len(prev) > 3:
            prev.pop(0)
        cur += ln
    out.sort()
    return out


with open(ADDRS, encoding="utf-8") as fh:
    raw = [l.split("#")[0].strip() for l in fh]
targets = [int(x, 16) for x in raw if x]

for t in targets:
    f = ida_funcs.get_func(t)
    if not f:
        print("!! 0x%X 无函数" % t)
        continue
    starts = case_starts(f)
    nxt = None
    for st in starts:
        if st > t:
            nxt = st
            break
    end = nxt if nxt else t + 0x400
    print("\n===== case 0x%X .. 0x%X (size %d) =====" % (t, end, end - t))
    cur = t
    n = 0
    while cur < end and n < MAXINS:
        insn = ida_ua.insn_t()
        ln = ida_ua.decode_insn(insn, cur)
        if ln == 0:
            break
        print("%08X  %s" % (cur, line(cur)))
        cur += ln
        n += 1
