# -*- coding: utf-8 -*-
"""非 9 位号形（7/8 位）的 20 行 #37 到底是什么：名字 / ITEM / 被 #1 引用 / 属性覆盖。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('''select btrim(weapon_setting_id), btrim(weapon_category),
                          btrim(damage_attribute), btrim(equip_slot_type),
                          btrim(model_id_lo), btrim(parent_setting_id)
                     from cfg."WEAPON_SETTING"
                    where length(btrim(weapon_setting_id)) <> 9
                    order by 1''')
    odd = cur.fetchall()
    print("非 9 位号形 %d 行" % len(odd))
    print("%-10s %-16s %-14s %-10s %-12s %s" %
          ("ID", "类别", "攻击类型", "槽位", "model_lo", "父行"))
    for r in odd:
        print("%-10s %-16s %-14s %-10s %-12s %s" % r)

    ids = [r[0] for r in odd]
    print()
    # ITEM 命中（#65，按 9 位补零形态也试）
    for t, col in (("ITEM", "item_id"), ("MSMA_WEAPONSET", "weapon_item_id")):
        cur.execute('select count(*) from cfg."%s" where btrim("%s") = any(%%s)' % (t, col), (ids,))
        n1 = cur.fetchone()[0]
        padded = [i.zfill(9) for i in ids]
        cur.execute('select count(*) from cfg."%s" where btrim("%s") = any(%%s)' % (t, col), (padded,))
        n2 = cur.fetchone()[0]
        print("%-16s 原形命中 %2d ／ 补零 9 位命中 %2d ／ %d" % (t, n1, n2, len(ids)))

    # #36 属性覆盖
    cur.execute('select btrim(attr_name), btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
    have = {}
    for a, k in cur.fetchall():
        have.setdefault(k, set()).add(a)
    print()
    print("%-10s %-12s %s" % ("ID", "#36 族数", "族"))
    for i in ids:
        s = have.get(i, set())
        print("%-10s %-12d %s" % (i, len(s), sorted(s)))

    # ITEM 里的名字（若命中）
    cur.execute('select btrim(item_id), btrim(name) from cfg."ITEM" where btrim(item_id) = any(%s)',
                (ids + [x.zfill(9) for x in ids],))
    m = cur.fetchall()
    if m:
        print()
        print("ITEM 名字：")
        for a, b in m:
            print("   %-10s %s" % (a, b))
