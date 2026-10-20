# -*- coding: utf-8 -*-
"""WEAPON_SETTING 参数块（15 个被误标 gap 的列）落点结构解析函数。

sub_5976F0: (dst, tbl, col) -> 取列 → sub_BBB920 建 wstring →（非空时）sub_56F550 加 FX 处理
sub_5978A0: (dst, src, flag) -> 把 src 串解析成 84 字节参数块（+0 为 wstring 头）
sub_597D00: (dst, src, flag, mode) -> 同族，mode=1 时为「派生复制」
sub_597AF0: (dst, src) -> 派生（后坐力/装填/…的键区复制）
输出：datatables/_out_ida_ws_blocks.txt
"""
import ida_hexrays
import idc

FUNCS = [
    ("sub_5978A0", "参数块解析（84B 结构）"),
    ("sub_597D00", "参数块解析/派生复制"),
    ("sub_597AF0", "派生复制"),
    ("sub_56F550", "wstring + FX 后缀"),
    ("sub_402310", "wstring assign (narrow?)"),
    ("sub_4029E0", "wstring assign"),
]
OUT = r"f:\9ymsgo\9you\datatables\_out_ida_ws_blocks.txt"

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
