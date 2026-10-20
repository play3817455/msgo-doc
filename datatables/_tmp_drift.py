# -*- coding: utf-8 -*-
"""WEAPON_BATTLE_DETAIL：按属性名统计值列个数（attr_value / attr_value_2 非空）。"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute("""
      SELECT attr_name,
             count(*) AS rows,
             count(*) FILTER (WHERE COALESCE(attr_value,'')  <> '') AS v1,
             count(*) FILTER (WHERE COALESCE(attr_value_2,'')<> '') AS v2
      FROM cfg."WEAPON_BATTLE_DETAIL"
      GROUP BY attr_name ORDER BY attr_name""")
    print("%-14s %6s %6s %6s" % ("attr_name", "rows", "v1", "v2"))
    for a, n, v1, v2 in cur.fetchall():
        print("%-14s %6d %6d %6d" % (a, n, v1, v2))

    print()
    cur.execute("""SELECT count(*) FROM cfg."WEAPON_BATTLE_DETAIL"
                   WHERE COALESCE(attr_value_2,'') <> ''""")
    print("v2 非空总行数 =", cur.fetchone()[0])
    cur.execute("""SELECT DISTINCT attr_name FROM cfg."WEAPON_BATTLE_DETAIL"
                   WHERE COALESCE(attr_value_2,'') <> ''""")
    print("有 v2 的属性 =", [r[0] for r in cur.fetchall()])
