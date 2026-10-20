# -*- coding: utf-8 -*-
"""_probe_lost44.py —— 44 台"将失去武器组"的机体到底什么状态？
① 桥表里的裁定档（OK / SUSPECT / UNRESOLVED）
② 它们现在引用的 8 位武器，是不是真的没有 #37 行（= 已经是断引用）
只报告，不写。
"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BRIDGE = os.path.join(HERE, "names", "机体-wiki武器页桥.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

LOST = """1100062 1101031 1101311 1101312 1102041 1104011 1104052 1108011 1109011 1119151
1124072 1124092 1126012 1132042 1132162 1132202 1133021 1134012 1145022 1146072
1156102 1163022 1171062 1201021 1207012 1210011 1213012 1221011 1222011 1223011
1235011 1261011 1262011 1267012 1401011 1403012 1410011 1411011 1412011 1421011
1422012 1430012 1432012 1507012""".split()

with open(BRIDGE, encoding="utf-8-sig") as fh:
    rows = [r for r in csv.reader(fh) if r and not r[0].lstrip("\ufeff").startswith("#")]
head = rows[0]
print("桥表首行（无表头，是数据）：%s" % rows[0])
print("桥表列数 %d ／ 数据行 %d" % (len(head), len(rows)))
print()

# 实测：col0=練度ID，col8=裁定档（OK / SUSPECT / UNRESOLVED）
verdict = {r[0].strip(): (r[8].strip() if len(r) > 8 else "") for r in rows}

import collections
cnt = collections.Counter(verdict.get(g, "(桥表无此行)") for g in LOST)
print("=== 44 台在桥表里的裁定档 ===")
for k, v in cnt.most_common():
    print("   %-16s %d" % (k, v))
print()

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
    d37 = {r[0] for r in cur.fetchall()}
    cur.execute('select btrim(weapon_group_id), btrim(weapon_item_id) from cfg."MSMA_WEAPONSET"')
    gw = collections.defaultdict(list)
    for g, i in cur.fetchall():
        gw[g].append(i)

tot, dang = 0, 0
for g in LOST:
    ids = gw.get(g, [])
    tot += len(ids)
    dang += sum(1 for i in ids if i not in d37)
print("=== 这 44 台现有武器行 ===")
print("   行数 %d ／ 其中 #37 无行（断引用）%d" % (tot, dang))
print("   ⇒ 断引用率 %.0f%%" % (100.0 * dang / max(1, tot)))
for g in LOST[:6]:
    ids = gw.get(g, [])
    print("   %s: %s  → 断 %d/%d" % (g, ids, sum(1 for i in ids if i not in d37), len(ids)))
