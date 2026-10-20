# -*- coding: utf-8 -*-
"""把指定 reader 的完整反汇编（含 push/call 注解）落到磁盘，供人读 -> datatables/_out_ida_asm.txt"""
import io
import collections
import sys

import ida_funcs
import idautils
import idc

FUNCS = [
    "sub_570880",  # BUILDUP_WEAPON 21 列 / 追踪到 4 次助手调用
    "sub_577DE0",  # MSMA_FORMATION 17 列 / 1 次
    "sub_580360",  # MSMA_OVERWRITE_PARAMS 23 列 / 0 次
    "sub_5A29B0",  # MODULE_BONUS 6 列 / 4 次 / 1 循环
]
OUT = r"f:\9ymsgo\9you\datatables\_out_ida_asm.txt"

buf = []


def emit(s=""):
    buf.append(s)


for name in FUNCS:
    ea = idc.get_name_ea_simple(name)
    f = ida_funcs.get_func(ea) if ea != idc.BADADDR else None
    emit("=" * 100)
    emit(f"### {name}  start={hex(ea)}")
    if not f:
        emit("  NOT FOUND")
        continue
    calls = collections.Counter()
    for insn_ea in idautils.Heads(f.start_ea, f.end_ea):
        mnem = idc.print_insn_mnem(insn_ea)
        if mnem == "call":
            tgt = idc.print_operand(insn_ea, 0)
            calls[tgt] += 1
    emit(f"  调用统计: {dict(calls)}")
    emit("-" * 100)
    for insn_ea in idautils.Heads(f.start_ea, f.end_ea):
        mnem = idc.print_insn_mnem(insn_ea)
        ops = []
        for i in range(4):
            t = idc.get_operand_type(insn_ea, i)
            if t == idc.o_void:
                break
            ops.append(f"{idc.print_operand(insn_ea, i)}")
        ann = ""
        if mnem == "push":
            ann = "   <-- push"
        elif mnem == "call":
            ann = "   <== CALL"
        emit(f"  {insn_ea:#010x}  {mnem:8s} {', '.join(ops):40s}{ann}")
    emit()

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(buf) + "\n")
print(f"wrote {OUT} ({len(buf)} lines)")
