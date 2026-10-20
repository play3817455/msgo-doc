# -*- coding: utf-8 -*-
"""探测大厅报文体"读取器助手"的字节消费量（IDA 静态）。

背景：客户端每个 S->C case 用一组小助手函数从线体游标里取值。
判明每个助手消费多少字节，就能"数"出报文体长。
本脚本逐个反汇编候选助手，打印前若干条指令供判定。

运行：IDA MCP 的 py_exec_file
"""
import idaapi
import idc
import ida_ua
import ida_funcs
import ida_bytes

CANDIDATES = [
    0xB41470, 0xB413B0, 0xB41A10, 0xB41850, 0xB416C0, 0xB415A0,
    0xB02DD0, 0xB02DF0, 0xB06230, 0xB06200, 0xB434B0, 0xB43BE0,
    0xB43B00, 0xB02BA0, 0xB05E30, 0xB06060,
]


def dump(ea, n=24):
    out = []
    cur = ea
    f = ida_funcs.get_func(ea)
    end = f.end_ea if f else ea + 0x200
    for _ in range(n):
        if cur >= end:
            break
        insn = ida_ua.insn_t()
        ln = ida_ua.decode_insn(insn, cur)
        if ln == 0:
            break
        out.append("%08X  %s" % (cur, idc.generate_disasm_line(cur, 0)))
        cur += ln
    return out


print("=== 读取器助手字节消费探测 ===")
for a in CANDIDATES:
    name = idc.get_func_name(a)
    f = ida_funcs.get_func(a)
    print("\n--- 0x%X  %s  func=%s size=%s" % (
        a, idc.get_name(a) or "?", name,
        (f.end_ea - f.start_ea) if f else "none"))
    for l in dump(a, 20):
        print("   " + l)
