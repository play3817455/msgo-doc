# -*- coding: utf-8 -*-
"""IDA 侧：导出待 hook 函数的 start/end/retn 弹出字节数/调用的其它函数 -> datatables/_out_ida_funcs.json"""
import json
import os

import ida_funcs
import idautils
import idc

HERE = r"f:\9ymsgo\9you\datatables"
NAMES = os.path.join(HERE, "_out_hook_names.json")
OUT = os.path.join(HERE, "_out_ida_funcs.json")

names = json.load(open(NAMES, encoding="utf-8"))["names"]
res = {}
missing = []
for name in names:
    ea = idc.get_name_ea_simple(name)
    f = ida_funcs.get_func(ea) if ea != idc.BADADDR else None
    if not f:
        missing.append(name)
        continue
    # 函数最后一条指令 = retn
    last = idc.prev_head(f.end_ea)
    retn_pop = None
    if last != idc.BADADDR:
        if idc.get_operand_type(last, 0) != idc.o_void and idc.print_insn_mnem(last) in ("retn", "ret"):
            retn_pop = idc.get_operand_value(last, 0)
        elif idc.print_insn_mnem(last) in ("retn", "ret"):
            retn_pop = 0
    calls = {}
    for insn_ea in idautils.Heads(f.start_ea, f.end_ea):
        if idc.print_insn_mnem(insn_ea) == "call":
            t = idc.print_operand(insn_ea, 0)
            calls[t] = calls.get(t, 0) + 1
    res[name] = {
        "start": f.start_ea,
        "end": f.end_ea,
        "retn_pop": retn_pop or 0,
        "last_insn": idc.print_insn_mnem(last) if last != idc.BADADDR else None,
        "calls": calls,
    }
json.dump({"funcs": res, "missing": missing}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"funcs={len(res)} missing={missing}")
