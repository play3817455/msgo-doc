# -*- coding: utf-8 -*-
"""看 batch8 定案的列：CHARA_PARAM csv83/85/86/89、MSMA_RENTAL 对应列、ACTION_MODULE_INFO / SCORE_CONFIG_CATEGORY / ITEM_PART"""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

for t, idxs in (
    ("CHARA_PARAM", (83, 85, 86, 89, 47, 48)),
    ("MSMA_RENTAL", (83, 85, 86, 89, 47, 48)),
    ("ACTION_MODULE_INFO", (0,)),
    ("SCORE_CONFIG_CATEGORY", (0,)),
    ("ITEM_PART", (42, 43, 49)),
):
    d = json.load(open(f"db_design/schema/cfg/tables/{t}.json", encoding="utf-8"))
    print(f"===== {t}")
    for c in sorted(d["columns"], key=lambda x: x["csv_index"]):
        if c["csv_index"] in idxs:
            brief = {k: v for k, v in c.items() if k in
                     ("csv_index", "name", "db_column", "type", "memory_offset", "status", "emu_exempt")}
            print("  ", json.dumps(brief, ensure_ascii=False))
            print("     meaning:", (c.get("meaning") or "")[:200])
