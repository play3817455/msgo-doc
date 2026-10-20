# -*- coding: utf-8 -*-
"""空表体检 + DOWNLOAD 表行数总览。只读。"""
import json
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCHEMA_DIR = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")

specs = {}
for fn in sorted(os.listdir(SCHEMA_DIR)):
    if fn.endswith(".json"):
        s = json.load(open(os.path.join(SCHEMA_DIR, fn), encoding="utf-8"))
        specs[s["id"]] = s

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("""select table_name from information_schema.tables where table_schema='cfg'""")
    tables = sorted(r[0] for r in cur.fetchall())
    empties = []
    for t in tables:
        cur.execute('select count(*) from cfg."%s"' % t)
        n = cur.fetchone()[0]
        sp = specs.get(t, {})
        disp = str(sp.get("disposition", "?"))
        if n == 0:
            empties.append((t, disp, sp.get("table_id"), sp.get("csv_path")))
        print("%-28s %-9s tid=%-4s rows=%-6d %s" % (t, disp, sp.get("table_id"), n, sp.get("csv_path")))
    print()
    print("== 空表 %d ==" % len(empties))
    for t, d, tid, p in empties:
        print("  %s  disp=%s tid=%s csv=%s" % (t, d, tid, p))
