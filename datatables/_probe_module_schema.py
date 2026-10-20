# -*- coding: utf-8 -*-
"""cfg."MSMA_MODULE" 列结构 + 与种子逐行一致性。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select ordinal_position, column_name, data_type from information_schema.columns "
        "where table_schema='cfg' and table_name='MSMA_MODULE' order by ordinal_position")
    cols = cur.fetchall()
    for p, n, t in cols:
        print("  %2d %-20s %s" % (p, n, t))
    cur.execute('select count(*) from cfg."MSMA_MODULE"')
    print("rows:", cur.fetchone()[0])
    cur.execute('select * from cfg."MSMA_MODULE" order by 1 limit 3')
    for r in cur.fetchall():
        print("  sample:", r)
