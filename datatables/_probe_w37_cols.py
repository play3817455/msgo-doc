# -*- coding: utf-8 -*-
"""_probe_w37_cols.py —— #37 物理列全表 + 非空统计，定位 buildup 键列（只读）

DB 的列名规则：已定名的列用真名，未定名的列用 `colN`（N = CSV 列号）。
实测 #1：physical[1]=weapon_group_id=CSV0, physical[2]=col1, physical[3]=weapon_item_id=CSV2
⇒ CSV 列号 = 物理下标 - 1。
本脚本按"CSV 列号"打印每一列的取值分布，避免再错位。
"""
import collections
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""SELECT ordinal_position, column_name, data_type
                     FROM information_schema.columns
                    WHERE table_schema='cfg' AND table_name='WEAPON_SETTING'
                    ORDER BY ordinal_position""")
    cols = cur.fetchall()

print("#37 WEAPON_SETTING 物理列 %d 个" % len(cols))
print()
print("%-4s %-4s %-8s %-22s %s" % ("phys", "CSV", "类型", "列名", "取值分布（最多 6 种）"))
for pos, name, dt in cols:
    csv_idx = pos - 2
    q = ('SELECT btrim("' + name + '"::text) FROM cfg."WEAPON_SETTING"')
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        cur.execute(q)
        vals = [r[0] for r in cur.fetchall()]
    c = collections.Counter(vals)
    top = ", ".join("%r×%d" % (k, v) for k, v in c.most_common(6))
    print("%-4d %-4s %-8s %-22s %s" % (pos, csv_idx, dt, name, top))
