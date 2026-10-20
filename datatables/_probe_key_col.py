# -*- coding: utf-8 -*-
"""看 reader_list 里这几张表登记的信息（declared/non_gap/其他）"""
import io, json, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, "_out_reader_list.json"), encoding="utf-8"))
for tn in ("ACTION_MODULE_INFO", "SCORE_CONFIG_CATEGORY", "ITEM_PART"):
    print(tn, json.dumps(r.get(tn), ensure_ascii=False)[:600], "\n")

# schema col0 for the two tables
ROOT = os.path.dirname(HERE)
for tn in ("ACTION_MODULE_INFO", "SCORE_CONFIG_CATEGORY"):
    t = json.load(open(os.path.join(ROOT, "db_design", "schema", "cfg", "tables", tn + ".json"), encoding="utf-8"))
    print("==", tn, {k: v for k, v in t.items() if k != "columns"})
    for i, c in enumerate(t["columns"][:4]):
        print("   ", json.dumps(c, ensure_ascii=False)[:300])
