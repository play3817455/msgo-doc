# -*- coding: utf-8 -*-
"""把 WEAPON_SETTING / MISSION_COOP / QUEST reader 的 Hex-Rays 伪码落到磁盘。

用途：为「被 schema 误标 gap、但客户端真读」的列定名（列号 → 落点偏移 + 类型/转换函数）。
输出：datatables/_out_ida_readers_pseudo.txt
"""
import ida_hexrays
import idc

READERS = [
    ("WEAPON_SETTING", "sub_597F50"),
    ("WEAPON_SETTING_wrapper", "sub_5976F0"),
    ("MISSION_COOP", "sub_59DC00"),
    ("QUEST", "sub_58DCA0"),
]
OUT = r"f:\9ymsgo\9you\datatables\_out_ida_readers_pseudo.txt"

ida_hexrays.init_hexrays_plugin()
buf = []
for label, name in READERS:
    ea = idc.get_name_ea_simple(name)
    buf.append("=" * 110)
    buf.append(f"### {label}  {name}  ea={ea:#x}")
    buf.append("=" * 110)
    if ea == idc.BADADDR:
        buf.append("  NOT FOUND")
        continue
    try:
        cf = ida_hexrays.decompile(ea)
    except Exception as exc:  # noqa: BLE001
        buf.append(f"  decompile failed: {exc}")
        continue
    if cf is None:
        buf.append("  decompile returned None")
        continue
    buf.append(str(cf))
    buf.append("")

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(buf) + "\n")
print(f"wrote {OUT} ({len(buf)} lines)")
