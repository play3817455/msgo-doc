# -*- coding: utf-8 -*-
"""meta.cfg_manifest 的列名 + n1 五表的行数对账。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select column_name, data_type from information_schema.columns "
        "where table_schema='meta' and table_name='cfg_manifest' order by ordinal_position"
    )
    print("meta.cfg_manifest 列:")
    for n, t in cur.fetchall():
        print("   %-24s %s" % (n, t))
    print()

    cur.execute(
        "select file, row_count, octet_length(raw_csv) "
        "from meta.cfg_manifest "
        "where file ~* '(msma|chara)' order by file"
    )
    print("%-40s %8s %10s" % ("file", "row_count", "raw_csv_bytes"))
    for r in cur.fetchall():
        print("%-40s %8s %10s" % r)
