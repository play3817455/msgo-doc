# -*- coding: utf-8 -*-
"""看 MSMA_WEAPONSET schema 前几列 + 库里实际列"""
import io
import json
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

d = json.load(open("db_design/schema/cfg/tables/MSMA_WEAPONSET.json", encoding="utf-8"))
for c in sorted(d["columns"], key=lambda x: x["csv_index"])[:6]:
    print(json.dumps(c, ensure_ascii=False))
print("--- db cols now ---")
with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as cn:
    cur = cn.cursor()
    cur.execute(
        "select column_name from information_schema.columns "
        "where table_schema='cfg' and table_name='MSMA_WEAPONSET' order by ordinal_position"
    )
    cols = [r[0] for r in cur.fetchall()]
print(len(cols), cols)
