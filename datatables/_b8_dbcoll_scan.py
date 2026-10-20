# -*- coding: utf-8 -*-
"""检查所有 schema 中 db_column 与 name 不一致的列（决定物理列名的权威字段）"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCHEMA_DIR = os.path.join("db_design", "schema", "cfg", "tables")
n_db = 0
for fn in sorted(os.listdir(SCHEMA_DIR)):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(SCHEMA_DIR, fn), encoding="utf-8"))
    rows = []
    for c in sorted(d.get("columns", []), key=lambda x: x.get("csv_index", 0)):
        dc = c.get("db_column")
        nm = c.get("name")
        if dc and nm and dc != nm:
            rows.append((c.get("csv_index"), nm, dc))
            n_db += 1
    if rows:
        print(f"== {d.get('id') or fn[:-5]} ({len(rows)} 处 db_column != name)")
        for i, nm, dc in rows:
            print(f"   [{i}] name={nm} db_column={dc}")
print(f"合计 {n_db} 处")
