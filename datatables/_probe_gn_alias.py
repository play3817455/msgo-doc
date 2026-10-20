# -*- coding: utf-8 -*-
"""`10840101` / `10840501` 是不是某个 9 位武器号的历史别名？只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    print("== #37 里含 '840' 的键 ==")
    cur.execute('select btrim(weapon_setting_id), btrim(weapon_category),'
                ' btrim(damage_attribute), btrim(model_id_lo) from cfg."WEAPON_SETTING"'
                " where btrim(weapon_setting_id) like '%840%' order by 1")
    for r in cur.fetchall():
        print("   %s" % (r,))

    print()
    print("== #37 里含 '840501' / '840101' 的键 ==")
    for pat in ("%840501%", "%840101%", "210840%", "%0840101%", "%0840501%"):
        cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"'
                    " where btrim(weapon_setting_id) like %s order by 1", (pat,))
        print("   %-12s → %s" % (pat, [r[0] for r in cur.fetchall()]))

    print()
    print("== game.unlockw 里这 2 行的上下文 ==")
    cur.execute("select item_id, pilot_id, uniqid_ms, world_id, buildup_cnt, db_index"
                " from game.unlockw where item_id in (10840101, 10840501)")
    for r in cur.fetchall():
        print("   %s" % (r,))

    print()
    print("== 同 pilot 的其它武器（看这批数据的号形）==")
    cur.execute("select pilot_id, uniqid_ms from game.unlockw where item_id in (10840101,10840501)")
    pil = cur.fetchall()
    print("   pilot/ms: %s" % pil)
    for p, ms in pil:
        cur.execute("select item_id from game.unlockw where pilot_id=%s order by item_id", (p,))
        print("   pilot=%s → %s" % (p, [r[0] for r in cur.fetchall()]))

    print()
    print("== 这些 weapon 键在 ITEM 的名字 ==")
    cur.execute("select btrim(item_id), btrim(name) from cfg.\"ITEM\""
                " where btrim(item_id) in ('10840101','10840501','210840101','210840501')")
    for r in cur.fetchall():
        print("   %s" % (r,))
