# -*- coding: utf-8 -*-
"""校验 meta.cfg_table_def 里 WEAPON_SETTING csv23..32 的 meaning 是否已刷新。只读。"""
import json
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
WANT = {23, 24, 25, 26, 27, 28, 29, 30, 31, 32}

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select column_defs, updated_at from meta.cfg_table_def where table_name='WEAPON_SETTING'"
    )
    defs, updated = cur.fetchone()
    if isinstance(defs, str):
        defs = json.loads(defs)
    print("updated_at =", updated, " 列数 =", len(defs))
    for d in defs:
        if d.get("csv_index") in WANT:
            print("  csv%-3s %-18s %s" % (d.get("csv_index"), d.get("name"), (d.get("meaning") or "")[:110]))
