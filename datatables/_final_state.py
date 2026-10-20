# -*- coding: utf-8 -*-
"""收尾体检：三张 cfg 表在收敛后的真实状态。"""
import collections
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

conn = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo")
cur = conn.cursor()
print("=== cfg 三表收敛后 ===")
for tag, tbl, col in (("#36", '"WEAPON_BATTLE_DETAIL"', "weapon_id_key"),
                      ("#37", '"WEAPON_SETTING"', "weapon_setting_id"),
                      ("#78", '"ITEM"', "item_id")):
    cur.execute('select count(*), count(distinct btrim(%s)) from cfg.%s' % (col, tbl))
    rows, keys = cur.fetchone()
    print("  %s %-24s 行 %7d  唯一键 %5d" % (tag, tbl, rows, keys))

print()
print("=== #36 键位数分布（应只剩 9 位 + 近战/现役引用）===")
cur.execute('select btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
by = collections.Counter(len(k) for (k,) in cur.fetchall())
print("  ", dict(sorted(by.items())))

print()
print("=== #78 里那 6 把（图标号族）仍在？名字应保留 ===")
for a in ("02600151", "02012401", "02240601", "12520101", "02210351", "02600101"):
    cur.execute('select btrim(name), btrim(item_type) from cfg."ITEM" where btrim(item_id)=%s', (a,))
    print("   %-9s %s" % (a, cur.fetchone()))

print()
print("=== POWER 原值带（9 位族）===")
cur.execute('''select btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' ''')
v = sorted(float(x) for (x,) in cur.fetchall())
print("   n=%d min=%.0f 中位=%.0f max=%.0f；>10000 的 %d 条"
      % (len(v), v[0], v[len(v) // 2], v[-1], sum(1 for x in v if x > 10000)))
conn.close()
