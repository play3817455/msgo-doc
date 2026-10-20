# -*- coding: utf-8 -*-
"""#37 / #36 / ITEM 里 10840101 / 10840501 的现状。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
KEYS = ["10840101", "10840501", "0840101", "0840501"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select column_name from information_schema.columns"
        " where table_schema='cfg' and table_name='WEAPON_SETTING' order by ordinal_position"
    )
    cols = [r[0] for r in cur.fetchall()]
    print("#37 列数 %d" % len(cols))
    print("    ", cols)
    print()
    cur.execute('select count(*) from cfg."WEAPON_SETTING"')
    print("#37 总行数 %s" % cur.fetchone()[0])
    for k in KEYS:
        cur.execute(
            "select _row_id, btrim(weapon_setting_id), btrim(weapon_category),"
            " btrim(equip_slot_type), btrim(model_id_lo), btrim(effect_name_list)"
            ' from cfg."WEAPON_SETTING" where btrim(weapon_setting_id)=%s',
            (k,),
        )
        for r in cur.fetchall():
            print("  #37 %s" % (r,))
    print()
    for k in KEYS:
        cur.execute(
            'select btrim(attr_name), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"'
            " where btrim(weapon_id_key)=%s order by attr_name",
            (k,),
        )
        rows = cur.fetchall()
        print("  #36 %-9s -> %d 行 %s" % (k, len(rows), [a for a, _ in rows]))
    print()
    for k in sorted(set(KEYS)):
        cur.execute(
            'select btrim(item_id), btrim(name), btrim(item_type) from cfg."ITEM" where btrim(item_id)=%s',
            (k,),
        )
        for r in cur.fetchall():
            print("  ITEM %s" % (r,))
