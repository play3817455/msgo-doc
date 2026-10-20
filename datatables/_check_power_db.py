# -*- coding: utf-8 -*-
"""_check_power_db.py —— 对账：指定武器在库里的 POWER(客户端原值) vs CSV 值 vs 面板/伤害。"""
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T36 = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "weapon_battle_detail.csv")
IDS = [int(x) for x in (sys.argv[1:] or [
    "210002102", "214403301", "214407001", "214804201", "212002102", "214405101"])]

want = {}
for r in csv.reader(open(T36, encoding="utf-8", errors="replace")):
    if len(r) > 2 and r[0].strip() == "POWER" and r[1].strip().isdigit() and int(r[1]) in IDS:
        want[int(r[1])] = r[2].strip()

cur = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo").cursor()
cur.execute('''select btrim(weapon_id_key), btrim(attr_value)
                 from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' and btrim(weapon_id_key) = any(%s)''',
            ([str(i) for i in IDS],))
db = {int(k): v for k, v in cur.fetchall()}


def panel(raw):
    return int(abs(float(raw)) * 10 + 0.4)


def dmg(raw):
    return -(-panel(raw) // 10)


print("%-12s %-10s %-10s %-8s %-6s" % ("武器ID", "库POWER原值", "CSV POWER", "面板", "每发伤害"))
for i in IDS:
    d, w = db.get(i), want.get(i)
    if d is None or w is None:
        print("%-12d %-10s %-10s" % (i, d or "(缺)", w or "(缺)"))
        continue
    print("%-12d %-10s %-10s %-8d %-6d" % (i, d, w, panel(w), dmg(w)))
