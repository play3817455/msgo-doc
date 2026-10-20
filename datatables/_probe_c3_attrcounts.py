# -*- coding: utf-8 -*-
"""全表 attr 计数比对：CSV ↔ 库（找出两族之外的差，判断是否本次修复引入）。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

rows = F.rd(sys.argv[1] if len(sys.argv) > 1 else F.T36)
body = [r for r in rows if not r[0].lstrip("\ufeff").startswith("#")]
csv_c = collections.Counter(r[0].strip() for r in body)

with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(attr_name), count(*) from cfg."WEAPON_BATTLE_DETAIL" group by 1')
    db_c = dict(cur.fetchall())

al = sorted(set(csv_c) | set(db_c))
print("%-14s %6s %6s %6s" % ("attr", "CSV", "DB", "diff"))
for a in al:
    c, d = csv_c.get(a, 0), db_c.get(a, 0)
    if c != d:
        print("%-14s %6d %6d %+6d" % (a, c, d, d - c))
print("CSV 合计 %d / DB 合计 %d" % (len(body), sum(db_c.values())))
