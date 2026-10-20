# -*- coding: utf-8 -*-
"""线性反汇编 WEAPON_SETTING/MISSION_COOP/QUEST 的 reader（含调用目标名与立即数）。

输出：datatables/_out_ida_reader_asm.txt
（本地再用脚本把「取列调用点 → 紧随的落点存储」配对，得到 col → 偏移/类型 全表）
"""
import ida_funcs
import idautils
import idc

TARGETS = [("WEAPON_SETTING", 0x597F50), ("MISSION_COOP", 0x59DC00), ("QUEST", 0x58DCA0)]
OUT = r"f:\9ymsgo\9you\datatables\_out_ida_reader_asm.txt"

buf = []
for label, va in TARGETS:
    f = ida_funcs.get_func(va)
    buf.append("=" * 100)
    if not f:
        buf.append(f"### {label} sub_{va:X} NOT FOUND")
        continue
    buf.append(f"### {label} sub_{va:X}  start={f.start_ea:#x} end={f.end_ea:#x}")
    buf.append("=" * 100)
    for ea in idautils.Heads(f.start_ea, f.end_ea):
        mnem = idc.print_insn_mnem(ea)
        ops = []
        for i in range(4):
            if idc.get_operand_type(ea, i) == idc.o_void:
                break
            ops.append(idc.print_operand(ea, i))
        extra = ""
        if mnem == "call":
            tgt = idc.get_operand_value(ea, 0)
            nm = idc.get_func_name(tgt) or ""
            extra = f"   ; -> {nm}"
        buf.append(f"  {ea:#010x}  {mnem:8s} {', '.join(ops)}{extra}")
    buf.append("")

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(buf) + "\n")
print(f"wrote {OUT} ({len(buf)} lines)")
