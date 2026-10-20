# -*- coding: utf-8 -*-
"""#36 覆盖缺口定位：哪些 #37 武器缺哪个属性族（尤其 POWER）。只读。"""
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
FAM = ["POWER", "RANGE", "HIGH_LOCKON", "STABILITY", "RAPIDDELAY",
       "COOLTIME", "RELOAD", "LOCKON_CAM", "RECOIL", "SWITCHTIME", "SHIELD"]

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING" order by 1')
    w = [r[0] for r in cur.fetchall()]
    have = {f: set() for f in FAM}
    cur.execute('select btrim(attr_name), btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
    for a, k in cur.fetchall():
        if a in have:
            have[a].add(k)

    print("#37 武器 %d" % len(w))
    print()
    print("%-14s %6s %6s  %s" % ("属性族", "覆盖", "缺", "缺的武器（最多 12）"))
    for f in FAM:
        miss = [x for x in w if x not in have[f]]
        print("%-14s %6d %6d  %s" % (f, len(have[f] & set(w)), len(miss),
                                     miss[:12] if len(miss) <= 12 else miss[:12] + ["…"]))

    print()
    print("=== 全族都缺的武器（= 完全取不到数值）===")
    full = [x for x in w if all(x not in have[f] for f in FAM)]
    print("   %d 把：%s" % (len(full), full[:40]))
    print()
    print("=== 缺 POWER 的武器 ===")
    print("   %s" % [x for x in w if x not in have["POWER"]])
    print()
    print("=== 只缺 POWER 之外某几族的（有 POWER，但缺 3 族及以上）===")
    core = ["POWER", "RANGE", "STABILITY", "RELOAD", "LOCKON_CAM"]
    cnt = {}
    for x in w:
        m = [f for f in core if x not in have[f]]
        if len(m) >= 3:
            cnt.setdefault(tuple(m), []).append(x)
    for k, v in sorted(cnt.items(), key=lambda t: -len(t[1])):
        print("   缺 %-40s × %d  样本 %s" % (",".join(k), len(v), v[:4]))
