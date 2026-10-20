# -*- coding: utf-8 -*-
"""game.unlockw / ms_rokaku / buildup_info 的列与短号记法。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in ("unlockw", "ms_rokaku", "buildup_info", "equip_set", "ms_set"):
        cur.execute("select column_name, data_type from information_schema.columns"
                    " where table_schema='game' and table_name=%s order by ordinal_position", (t,))
        cols = cur.fetchall()
        cur.execute('select count(*) from game."%s"' % t)
        n = cur.fetchone()[0]
        print("== game.%s  行 %d" % (t, n))
        for a, b in cols:
            print("     %-28s %s" % (a, b))
        # 打印前几行
        cur.execute('select * from game."%s" limit 4' % t)
        for r in cur.fetchall():
            print("     › %r" % (r,))
        print()
