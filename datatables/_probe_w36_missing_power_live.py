# -*- coding: utf-8 -*-
"""这 2 把缺 POWER 的武器，是否真的在**现役玩家数据**里？只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
T = [10840101, 10840501]
S = ["10840101", "10840501"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    print("== game.unlockw (item_id bigint) ==")
    cur.execute("select item_id, count(*), count(distinct pilot_id) from game.unlockw"
                " where item_id = any(%s) group by 1 order by 1", (T,))
    r = cur.fetchall()
    print("   命中 %d 种：%s" % (len(r), r))

    print("== game.ms_rokaku.eqweapon_itemid (ARRAY) ==")
    cur.execute("select eqweapon_itemid from game.ms_rokaku")
    hit = {}
    for (arr,) in cur.fetchall():
        for v in (arr or []):
            if v in T:
                hit[v] = hit.get(v, 0) + 1
    print("   命中：%s" % hit)

    print("== game.ms_rokaku.eqshield_itemid / eqspecial_itemid ==")
    for col in ("eqshield_itemid", "eqspecial_itemid"):
        cur.execute('select count(*) from game.ms_rokaku where "%s" = any(%%s)' % col, (T,))
        print("   %s: %d" % (col, cur.fetchone()[0]))

    print("== sidecar 武器分配明细 里有没有 ==")
    cur.execute("select count(*) from game.unlockw")
    print("   （sidecar 是文件，另查）unlockw 总行 %d" % cur.fetchone()[0])
    for t in ("unlockw",):
        cur.execute('select count(distinct item_id) from game."%s"' % t)
        print("   distinct item_id %d" % cur.fetchone()[0])
        cur.execute('select min(item_id), max(item_id) from game."%s"' % t)
        print("   范围 %s" % (cur.fetchone(),))

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    # #36 里这 2 把的现存族与值
    for k in S:
        cur.execute('select btrim(attr_name), btrim(attr_value), btrim(attr_value_2)'
                    ' from cfg."WEAPON_BATTLE_DETAIL" where btrim(weapon_id_key)=%s'
                    ' order by 1', (k,))
        print("   #36 %s → %s" % (k, cur.fetchall()))
    # #37 这 2 把的关键列
    cur.execute('select btrim(weapon_setting_id), btrim(weapon_category),'
                ' btrim(damage_attribute), btrim(equip_slot_type), btrim(ammo_type_id),'
                ' btrim(magazine_size), btrim(model_id_lo)'
                ' from cfg."WEAPON_SETTING" where btrim(weapon_setting_id) = any(%s)', (S,))
    for r in cur.fetchall():
        print("   #37 %s" % (r,))
