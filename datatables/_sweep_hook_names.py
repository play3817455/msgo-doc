# -*- coding: utf-8 -*-
"""收集需要 hook 的函数名单（reader ∪ enum_converter ∪ 助手）-> datatables/_out_hook_names.json"""
import glob
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
OUT = os.path.join(HERE, "_out_hook_names.json")

HELPERS = ["sub_BBB370", "sub_BBB470", "sub_BBB4F0", "sub_456D90", "sub_CC5E75", "sub_CC529D",
           "sub_CC6876", "sub_CC74E9", "sub_4029E0", "sub_402AD0", "sub_BBB250"]

names = set(HELPERS)
converters = {}
for p in sorted(glob.glob(os.path.join(TABLES, "*.json"))):
    d = json.load(open(p, encoding="utf-8"))
    r = d.get("asm_reader")
    if r and r.startswith("sub_"):
        names.add(r)
    for c in d["columns"]:
        cv = c.get("enum_converter")
        if cv and cv.startswith("sub_"):
            names.add(cv)
            converters.setdefault(cv, []).append(f"{d['id']}.{c.get('name')}")

with open(OUT, "w", encoding="utf-8") as fh:
    json.dump({"names": sorted(names), "converters": converters}, fh, ensure_ascii=False, indent=1)
print(f"hook names={len(names)} converters={len(converters)}")
for k, v in sorted(converters.items()):
    print(f"  {k}: {', '.join(v)}")
