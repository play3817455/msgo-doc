# -*- coding: utf-8 -*-
"""前缀 10 的 3 把武器全貌 + 同名家族参考（含 POWER 的那把）。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def norm(k):
    s = str(k).strip()
    return s.zfill(8) if s.isdigit() and len(s) < 8 else s


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select btrim(weapon_setting_id), btrim(weapon_category), btrim(equip_slot_type) '
                'from cfg."WEAPON_SETTING"')
    ws = {norm(k): (cat, slot) for k, cat, slot in cur.fetchall()}
    fams = sorted(k for k in ws if k.startswith("10"))
    print("前缀 10 全部 %d 把：%s" % (len(fams), fams))
    for k in fams:
        cur.execute('select btrim(name), btrim(item_type) from cfg."ITEM" where btrim(item_id)=%s', (k,))
        nm = cur.fetchall()
        cur.execute('select btrim(attr_name), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"'
                    ' where btrim(weapon_id_key)=%s order by attr_name', (k,))
        rows = cur.fetchall()
        print("  %s %-14s %-10s item=%s" % (k, ws[k][0], ws[k][1], nm))
        for a, v in rows:
            print("        %-14s %s" % (a, v))
    print()
    print("== 全库中名字含 'ダガー' / '投擲' 的 ITEM ==")
    cur.execute("select btrim(item_id), btrim(name) from cfg.\"ITEM\" "
                "where name like '%ダガー%' or name like '%投擲%' or name like '%サーベル%' order by item_id")
    for r in cur.fetchall():
        print("   %s  %s" % r)
