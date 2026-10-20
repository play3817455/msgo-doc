# -*- coding: utf-8 -*-
"""_audit_legacy_power.py —— 遗留号家族（非 9 位）的 #36 到底是"另一套真数据"还是"旧管线残渣"。

判据：
 ① 遗留号的 POWER 分布 —— 真武器的 POWER 原值应在 [20, 3400]（面板 200–34000）；
    若遗留号整片落在个位数，就是同一场事故的另一半，不是另一套口径。
 ② 遗留号的名字在 9 位空间里有没有同名（有 = 重复条目，真实身份已由 9 位一条覆盖）。
"""
import csv
import io
import os
import statistics
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")

cur = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo").cursor()

cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' and btrim(weapon_id_key) ~ '^[0-9]+$' ''')
rows = cur.fetchall()
new = [abs(float(v)) for k, v in rows if len(k) >= 9 and v.strip()]
old = [(k, v) for k, v in rows if len(k) < 9 and v.strip()]
oldv = [abs(float(v)) for _, v in old]

print("#36 POWER 行：9 位(新) %d 条；非 9 位(遗留) %d 条" % (len(new), len(old)))
if new:
    print("   9 位：min=%g 中位=%g max=%g；<10 的 %d 条"
          % (min(new), statistics.median(new), max(new), sum(1 for x in new if x < 10)))
if oldv:
    print("   遗留：min=%g 中位=%g max=%g；<10 的 %d 条（%.0f%%）"
          % (min(oldv), statistics.median(oldv), max(oldv),
             sum(1 for x in oldv if x < 10), 100.0 * sum(1 for x in oldv if x < 10) / len(oldv)))
    print("   遗留 POWER 取值分布：%s" % dict(Counter(int(x) for x in oldv).most_common(12)))

# 名字重名：遗留武器的名字在 9 位空间里有没有
cur.execute('''select btrim(item_id), btrim(name) from cfg."ITEM"
                where btrim(item_id) ~ '^[0-9]+$' and btrim(item_type)='WEAPON' ''')
nm = {}
for k, n in cur.fetchall():
    nm.setdefault(n, []).append(k)
nine_names = {n for n, ks in nm.items() if any(len(k) >= 9 for k in ks)}
leg_names = {n for n, ks in nm.items() if any(len(k) < 9 for k in ks)}
both = leg_names & nine_names
print()
print("#78 WEAPON 名 %d 个：9 位有 %d、遗留有 %d、**两边同名** %d"
      % (len(nm), len(nine_names), len(leg_names), len(both)))
print("   两边同名例：%s" % list(both)[:8])

# 6 把报警武器：名字在 9 位空间是否已有归属
print()
for raw in ("2600151", "2012401", "2240601", "12520101", "2210351", "2600101"):
    key = "%08d" % int(raw)
    cur.execute('select btrim(name) from cfg."ITEM" where btrim(item_id)=%s', (key,))
    r = cur.fetchone()
    n = r[0] if r else "(无名)"
    ks = [k for k in nm.get(n, []) if len(k) >= 9]
    print("   %-9s 名=%-28s 9 位同名键=%s" % (raw, n, ks or "（无）"))
