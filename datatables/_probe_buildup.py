# -*- coding: utf-8 -*-
"""_probe_buildup.py —— cfg."BUILDUP_WEAPON" 第 1 行 slot_*_enabled='10' 的来路。"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "server", "datafiles", "lounge", "develop", "buildup_weapon.csv")

with psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo") as conn:
    cur = conn.cursor()
    cur.execute("select column_name from information_schema.columns where table_schema='cfg'"
                " and table_name='BUILDUP_WEAPON' order by ordinal_position")
    cols = [r[0] for r in cur.fetchall()]
    print("库列 %d：%s" % (len(cols), cols))
    print()
    cur.execute('select * from cfg."BUILDUP_WEAPON" order by _row_id')
    rows = cur.fetchall()
    print("行数 %d" % len(rows))
    for i, r in enumerate(rows, 1):
        nz = {c: v for c, v in zip(cols, r) if v not in (None, "")}
        print()
        print("--- 第 %d 行 ---" % i)
        print("   %s" % nz)
    print()
    print("=== 每列去重取值 ===")
    for c in cols:
        if c == "_row_id":
            continue
        cur.execute('select distinct btrim("%s"::text) from cfg."BUILDUP_WEAPON" order by 1' % c)
        vals = [r[0] for r in cur.fetchall()]
        print("   %-24s %s" % (c, vals[:12]))

print()
print("=== 种子 CSV ===")
print(CSV, os.path.exists(CSV))
if os.path.exists(CSV):
    with open(CSV, encoding="utf-8-sig") as fh:
        for i, l in enumerate(fh):
            print("   %s" % l.rstrip()[:160])
            if i > 6:
                break
