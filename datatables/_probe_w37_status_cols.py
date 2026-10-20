# -*- coding: utf-8 -*-
"""#37 里 10840101 / 10840501 的 状态/威力 相关列，与同族参照对比。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")


def norm(k):
    s = str(k).strip()
    return s.zfill(8) if s.isdigit() and len(s) < 8 else s


COLS = ["weapon_power", "col37", "damage_type", "damage_attribute", "weapon_attribute",
        "status_duration_sec", "status_radius_m", "status_effect", "status_effect_power",
        "ui_stat_display_id", "display_mode", "col130", "special_effect_secondary",
        "damage_field_burst_cap", "melee_shield_subtype", "melee_shield_subtype_alt",
        "weapon_category", "equip_slot_type", "ammo_count", "ammo_reserve", "bullet_id",
        "projectile_setting_id", "grenade_arc_peak", "grenade_homing_strength",
        "projectile_launch_speed", "tag_list", "max_lock_count"]

KEYS = ["10840101", "10840501", "04840601", "04840201", "04840401", "04010101",
        "10020101", "01010401", "04101103", "10011301", "04960101", "10240101"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select weapon_setting_id, %s from cfg."WEAPON_SETTING"' % ", ".join(
        '"%s"' % x for x in COLS))
    rows = {norm(r[0]): r[1:] for r in cur.fetchall()}

for k in KEYS:
    r = rows.get(k)
    if not r:
        print("%s  #37 无此行" % k)
        continue
    print("== %s" % k)
    for name, v in zip(COLS, r):
        v = (v or "").strip()
        if v:
            print("     %-26s %s" % (name, v))
    print()
