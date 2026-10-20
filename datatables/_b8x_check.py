# -*- coding: utf-8 -*-
"""batch8.x 验收：manifest 集合 / MSMA_OVERWRITE_PARAMS 新宽度 / 列注释快照"""
import glob
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

specs = {}
for p in glob.glob("db_design/schema/cfg/tables/*.json"):
    d = json.load(open(p, encoding="utf-8"))
    specs[d["id"]] = d

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select file from meta.cfg_manifest order by file")
    mf = [r[0] for r in cur.fetchall()]
    print("manifest", len(mf), "schema", len(specs))
    print("manifest 有 / schema 无:", [t for t in mf if t not in specs])
    print("schema 有 / manifest 无:", [t for t in specs if t not in mf])
    print("skipDB 表:", [t for t in specs if specs[t].get("skip_db")])

    cur.execute(
        "select column_name from information_schema.columns where table_schema='cfg' "
        "and table_name='MSMA_OVERWRITE_PARAMS' order by ordinal_position")
    cols = [r[0] for r in cur.fetchall()]
    print("OVERWRITE 物理列", len(cols))
    print("  首四:", cols[:4])
    print("  末四:", cols[-4:])

    cur.execute("select row_count, octet_length(raw_csv) from meta.cfg_manifest where file='MSMA_OVERWRITE_PARAMS'")
    print("manifest:", cur.fetchone())
    cur.execute("select jsonb_array_length(column_defs) from meta.cfg_table_def where table_name='MSMA_OVERWRITE_PARAMS'")
    print("cfg_table_def.column_defs 列数:", cur.fetchone()[0])
    cur.execute("select count(*) from cfg.\"MSMA_OVERWRITE_PARAMS\"")
    print("cfg 行数:", cur.fetchone()[0])
