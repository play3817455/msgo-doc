# -*- coding: utf-8 -*-
"""meta.cfg_table_def / cfg_manifest 里是否也存了列元数据（要跟着重导）。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in ("cfg_table_def", "cfg_manifest"):
        cur.execute("select column_name, data_type from information_schema.columns"
                    " where table_schema='meta' and table_name=%s order by ordinal_position", (t,))
        print("== meta.%s" % t)
        for a, b in cur.fetchall():
            print("     %-24s %s" % (a, b))
        cur.execute('select count(*) from meta."%s"' % t)
        print("   行 %d" % cur.fetchone()[0])
    print()
    cur.execute("select * from meta.cfg_table_def where table_name='WEAPON_SETTING'")
    rows = cur.fetchall()
    print("WEAPON_SETTING 在 cfg_table_def 的行数 %d" % len(rows))
    for r in rows[:3]:
        print("   ", r)
    print()
    cur.execute("select * from meta.cfg_manifest where file like '%%weapon_setting%%'")
    for r in cur.fetchall():
        print("   ", r)
