# -*- coding: utf-8 -*-
"""_probe_w36_keys.py —— #36 的键与属性清单（只读）"""
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute('SELECT count(DISTINCT btrim(weapon_id_key)) FROM cfg."WEAPON_BATTLE_DETAIL"')
    print("去重 weapon_id_key：%d" % cur.fetchone()[0])
    cur.execute("""SELECT btrim(attr_name), count(*) FROM cfg."WEAPON_BATTLE_DETAIL"
                    GROUP BY 1 ORDER BY 2 DESC""")
    print("属性清单：")
    for a, n in cur.fetchall():
        print("  %-14s %d 行" % (a, n))
    cur.execute("""SELECT length(btrim(weapon_id_key)) l, count(DISTINCT btrim(weapon_id_key))
                     FROM cfg."WEAPON_BATTLE_DETAIL" GROUP BY 1 ORDER BY 1""")
    print("weapon_id_key 号形：")
    for l, n in cur.fetchall():
        print("  %d 位：%d 个" % (l, n))
    cur.execute('SELECT btrim(weapon_setting_id) FROM cfg."WEAPON_SETTING"')
    s37 = {r[0] for r in cur.fetchall()}
    cur.execute('SELECT DISTINCT btrim(weapon_id_key) FROM cfg."WEAPON_BATTLE_DETAIL"')
    s36 = {r[0] for r in cur.fetchall()}
    print("#36 键 ⊂ #37 键：%d / %d；#36 有·#37 无：%d" % (len(s36 & s37), len(s36), len(s36 - s37)))
    print("#37 有·#36 无：%d → %s" % (len(s37 - s36), sorted(s37 - s36)[:8]))
