# -*- coding: utf-8 -*-
"""#4 CHARA_PARAM 逐字段对账（种子 vs 库），定位 mf 尾部多出来的那个值（只读）。"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

d = json.load(io.open(os.path.join(SCHEMA, "CHARA_PARAM.json"), encoding="utf-8"))
by_idx = {c["csv_index"]: c["name"] for c in d["columns"]}
print("schema csv_index 域 %d..%d（%d 列）" % (min(by_idx), max(by_idx), len(by_idx)))

seed = {}
with open(os.path.join(LOUNGE, "msma", "msma_settings.csv"), "rb") as f:
    raw = f.read().decode("utf-8", "replace")
for ln in raw.replace("\r\n", "\n").split("\n"):
    if not ln.strip() or ln.lstrip().startswith("#"):
        continue
    fs = ln.split(",")
    seed[fs[0].strip()] = fs

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select column_name from information_schema.columns "
        "where table_schema='cfg' and table_name='CHARA_PARAM' order by ordinal_position")
    dbcols = [r[0] for r in cur.fetchall() if r[0] != "_row_id"]
    print("库数据列 %d 个（最后 5 个: %s）" % (len(dbcols), dbcols[-5:]))
    for k in ("1100001", "1100011", "1100032", "1105021"):
        cur.execute(
            'select * from cfg."CHARA_PARAM" where msma_id=%s', (k,))
        row = cur.fetchone()
        desc = [x[0] for x in cur.description]
        db = {n: ("" if v is None else str(v)) for n, v in zip(desc, row) if n != "_row_id"}
        fs = seed.get(k, [])
        print("=" * 78)
        print("## %s  种子字段数=%d ／ 库数据列=%d" % (k, len(fs), len(dbcols)))
        print("   种子尾部 12 字段:", fs[-12:])
        print("   库  尾部 12 列:", [(n, db[n]) for n in dbcols[-12:]])
        print("   -- 非空字段逐列（按库的物理列序，用 schema csv_index 对齐种子）--")
        for i, n in enumerate(dbcols):
            sv = fs[i].strip() if i < len(fs) else "<越界>"
            dv = db[n].strip()
            if sv or dv:
                flag = "" if sv == dv else "   <<< 种子=%r 库=%r" % (sv, dv)
                print("     col%-3d %-34s 种子=%-14r 库=%r%s" % (i, n, sv, dv, flag))
