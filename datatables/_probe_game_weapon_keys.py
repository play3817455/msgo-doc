# -*- coding: utf-8 -*-
"""决定性问题：`game.*` 运行时表里这些短号是**哪种记法**（7 位 vs 前导 0 的 8 位）？
以及 `#37` / `#36` 与它们能否连上。只读。
"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
KEYS = ["1040101", "1010401", "2040101", "2840101", "8010101", "81040101",
        "12010101", "12840101"]
# 域文件里的前导 0 形态
PAD = ["01040101", "01010401", "02040101", "02840101", "08010101", "81040101",
        "12010101", "12840101"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("select table_name from information_schema.tables"
                " where table_schema='game' order by 1")
    tabs = [r[0] for r in cur.fetchall()]
    print("game 表 %d 张：%s" % (len(tabs), tabs))
    print()

    for t in tabs:
        cur.execute("select column_name from information_schema.columns"
                    " where table_schema='game' and table_name=%s order by ordinal_position", (t,))
        cols = [r[0] for r in cur.fetchall()]
        # 找文本列
        tcols = []
        for cc in cols:
            cur.execute("select data_type from information_schema.columns"
                        " where table_schema='game' and table_name=%s and column_name=%s", (t, cc))
            if cur.fetchone()[0] in ("text", "character varying", "character"):
                tcols.append(cc)
        if not tcols:
            continue
        for cc in tcols:
            for label, arr in (("7位", KEYS), ("带0 8位", PAD)):
                cur.execute('select count(*) from game."%s" where "%s" = any(%%s)' % (t, cc),
                            (arr,))
                n = cur.fetchone()[0]
                if n:
                    cur.execute('select distinct "%s" from game."%s" where "%s" = any(%%s)'
                                ' limit 8' % (cc, t, cc), (arr,))
                    got = sorted(r[0] for r in cur.fetchall())
                    print("  命中 game.%-22s.%-22s [%s] × %d  %s" % (t, cc, label, n, got))
