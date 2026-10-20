# -*- coding: utf-8 -*-
"""把 CSV 取值助手函数族的反汇编落到磁盘 -> datatables/_out_ida_helpers.txt"""
import collections

import ida_funcs
import idautils
import idc

FUNCS = [
    "sub_BBB370",  # atoi-ish?
    "sub_BBB470",  # float-ish (fmul after)
    "sub_BBB4F0",  # raw string
    "sub_BBBB70",  # 多参：off_110B128, 2, sub_5800D0, 0, 3
    "sub_456D90",  # thiscall: (dst, idx) 返回字段指针
]
OUT = r"f:\9ymsgo\9you\datatables\_out_ida_helpers.txt"

buf = []


def emit(s=""):
    buf.append(s)


for name in FUNCS:
    ea = idc.get_name_ea_simple(name)
    f = ida_funcs.get_func(ea) if ea != idc.BADADDR else None
    emit("=" * 100)
    if not f:
        emit(f"### {name}  NOT FOUND")
        continue
    calls = collections.Counter()
    for insn_ea in idautils.Heads(f.start_ea, f.end_ea):
        if idc.print_insn_mnem(insn_ea) == "call":
            calls[idc.print_operand(insn_ea, 0)] += 1
    emit(f"### {name}  start={hex(f.start_ea)} end={hex(f.end_ea)}  调用: {dict(calls)}")
    emit("-" * 100)
    for insn_ea in idautils.Heads(f.start_ea, f.end_ea):
        mnem = idc.print_insn_mnem(insn_ea)
        ops = []
        for i in range(4):
            if idc.get_operand_type(insn_ea, i) == idc.o_void:
                break
            ops.append(idc.print_operand(insn_ea, i))
        ann = "   <== CALL" if mnem == "call" else ""
        emit(f"  {insn_ea:#010x}  {mnem:8s} {', '.join(ops)}{ann}")
    emit()

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(buf) + "\n")
print(f"wrote {OUT} ({len(buf)} lines)")
