# -*- coding: utf-8 -*-
"""20 个近战/短号武器的 #36 全族对照（看 18 有 POWER 的是什么来路）。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
SHORT = ["1010401", "2200101", "2711603", "2840101", "2840151", "2841701", "3010101",
         "4010101", "4200101", "4200151", "4840201", "4840401", "4840601", "4842501",
         "8010101", "10020101", "10840101", "10840501", "12010101", "12840101",
         "13200151", "13200251"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select btrim(weapon_setting_id), btrim(weapon_category), btrim(damage_attribute)'
                ' from cfg."WEAPON_SETTING" where btrim(weapon_setting_id) = any(%s)', (SHORT,))
    cat = {r[0]: (r[1], r[2]) for r in cur.fetchall()}
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value)'
                ' from cfg."WEAPON_BATTLE_DETAIL" where btrim(weapon_id_key) = any(%s)', (SHORT,))
    fam = {}
    for k, a, v in cur.fetchall():
        fam.setdefault(k, {})[a] = v

    order = ["POWER", "RANGE", "HIGH_LOCKON", "STABILITY", "RAPIDDELAY",
             "COOLTIME", "RELOAD", "LOCKON_CAM"]
    print("%-10s %-14s %-13s %s" % ("key", "类别", "攻击类型", " ".join("%-11s" % o for o in order)))
    for k in SHORT:
        cc, da = cat.get(k, ("?", "?"))
        row = fam.get(k, {})
        print("%-10s %-14s %-13s %s" % (k, cc, da,
              " ".join("%-11s" % (row.get(o, "—") or "∅") for o in order)))
