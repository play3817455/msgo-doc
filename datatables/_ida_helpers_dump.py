# -*- coding: utf-8 -*-
"""导出 CSV 取值助手族的 Hex-Rays 伪码（判定「单列→u64」还是「双列→u64」等语义）。

输出：datatables/_out_ida_helpers_pseudo.txt
"""
import ida_hexrays
import idc

FUNCS = [
    ("sub_BBB370", "atoi → int"),
    ("sub_BBB3F0", "? → 64bit (edx:eax)"),
    ("sub_BBB470", "atof → float"),
    ("sub_BBB4F0", "raw wstring"),
    ("sub_BBB920", "? (used for wstring + parse)"),
    ("sub_456D90", "thiscall: 取字段指针"),
    ("sub_483020", "parent lookup?"),
    ("sub_42CD60", "unused"),
    ("sub_596100", "? (after sub_596B70)"),
    ("sub_56F550", "wstring → enum"),
    ("sub_5968A0", "wstring → int (range str)"),
    ("sub_596990", "wstring → int"),
    ("sub_596A80", "wstring → int"),
    ("sub_596B70", "wstring → enum fire_mode"),
    ("sub_596510", "wstring → enum"),
    ("sub_5965F0", "wstring → enum"),
    ("sub_5964A0", "wstring → enum"),
    ("sub_596C60", "wstring → int"),
    ("sub_596D50", "wstring → int"),
    ("sub_596E40", "wstring → int"),
]
OUT = r"f:\9ymsgo\9you\datatables\_out_ida_helpers_pseudo.txt"

ida_hexrays.init_hexrays_plugin()
buf = []
for name, note in FUNCS:
    ea = idc.get_name_ea_simple(name)
    buf.append("=" * 100)
    buf.append(f"### {name}  ({note})  ea={ea:#x}")
    buf.append("=" * 100)
    if ea == idc.BADADDR:
        buf.append("  NOT FOUND")
        buf.append("")
        continue
    try:
        cf = ida_hexrays.decompile(ea)
    except Exception as exc:  # noqa: BLE001
        buf.append(f"  decompile failed: {exc}")
        buf.append("")
        continue
    buf.append(str(cf) if cf else "  decompile returned None")
    buf.append("")

with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(buf) + "\n")
print(f"wrote {OUT} ({len(buf)} lines)")
