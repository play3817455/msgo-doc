# -*- coding: utf-8 -*-
"""_probe_legacy.py —— 看某几个 id 在三表中的现状与 CSV 里的对应行（判断是遗留垃圾还是真武器）。"""
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")
IDS = [int(x) for x in (sys.argv[1:] or [
    "2600151", "2012401", "2240601", "12520101", "2210351", "2600101"])]

cur = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo").cursor()
cur.execute('''select btrim(item_id), btrim(name), btrim(item_type)
                 from cfg."ITEM" where btrim(item_id) = any(%s)''', ([str(i) for i in IDS],))
names = {int(a): (b, c) for a, b, c in cur.fetchall()}

for i in IDS:
    n, t = names.get(i, ("(无 #78 行)", "-"))
    print("== %d  #78: %s [%s]" % (i, n, t))
    cur.execute('''select btrim(attr_name), btrim(attr_value), btrim(coalesce(attr_value_2,''))
                     from cfg."WEAPON_BATTLE_DETAIL" where btrim(weapon_id_key)=%s
                    order by btrim(attr_name)''', (str(i),))
    rows = cur.fetchall()
    if not rows:
        print("   #36: (无)")
    for a, v, v2 in rows:
        print("   #36 %-14s %-14s %s" % (a, v, v2))
    cur.execute('''select magazine_size, equip_slot_type, weapon_category
                     from cfg."WEAPON_SETTING" where btrim(weapon_setting_id)=%s''', (str(i),))
    s = cur.fetchone()
    print("   #37 弹匣=%s 槽=%s 类=%s" % (tuple(s) if s else ("(无)", "-", "-")))

# CSV 里这些 id 的行
csvids = set()
for fn in ("weapon_battle_detail.csv", "weapon_settings.csv", "item.csv"):
    p = os.path.join(DF, fn)
    n = 0
    for r in csv.reader(open(p, encoding="utf-8", errors="replace")):
        if r and r[0].lstrip("\ufeff").strip().isdigit() and int(r[0].lstrip("\ufeff")) in IDS:
            n += 1
    print("CSV %-28s 命中这些 id 的行数=%d" % (fn, n))
