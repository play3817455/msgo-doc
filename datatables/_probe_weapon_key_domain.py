# -*- coding: utf-8 -*-
"""键域体检：`datatables/names/可达武器号域.csv`（生成器口径哨读它）vs 真库 #37 / #36。
只读。
"""
import csv
import io
import os

import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOM = os.path.join(HERE, "names", "可达武器号域.csv")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

with io.open(DOM, encoding="utf-8-sig", newline="") as fh:
    rows = [r for r in csv.reader(fh) if r and not r[0].lstrip().startswith("#")]

print("域文件 %s" % os.path.relpath(DOM, ROOT))
print("  表头: %s" % (rows[0] if rows else None))
print("  数据行 %d" % (len(rows) - 1))

hdr = rows[0]
data = rows[1:]
# 找出"号"与"来源/类别"列
keycol = next((i for i, h in enumerate(hdr)
               if any(k in h for k in ("号", "ID", "id", "key"))), 0)
srccol = next((i for i, h in enumerate(hdr)
               if any(k in h for k in ("来源", "类别", "src", "kind", "reason"))), None)
domain = {r[keycol].strip() for r in data if r and r[keycol].strip()}
print("  去重号 %d" % len(domain))
if srccol is not None:
    cnt = {}
    for r in data:
        cnt[r[srccol].strip()] = cnt.get(r[srccol].strip(), 0) + 1
    print("  来源分布: %s" % cnt.items())

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
    w37 = {r[0] for r in cur.fetchall()}
    cur.execute('select distinct btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
    w36 = {r[0] for r in cur.fetchall()}

print()
print("#37 键 %d ／ #36 键 %d ／ 域 %d" % (len(w37), len(w36), len(domain)))
print()
print("① #37 越域（在库不在域）: %d" % len(w37 - domain))
for k in sorted(w37 - domain):
    print("     %-12s len=%d" % (k, len(k)))
print()
print("② 域里有、#37 没有: %d" % len(domain - w37))
for k in sorted(domain - w37)[:40]:
    print("     %s" % k)
print()
print("③ #36 越域: %d" % len(w36 - domain))
for k in sorted(w36 - domain):
    print("     %-12s len=%d" % (k, len(k)))
print()
print("④ #36 与 #37 键差集: #36 独有 %d ／ #37 独有 %d"
      % (len(w36 - w37), len(w37 - w36)))
for k in sorted(w36 ^ w37)[:30]:
    print("     %-12s in#36=%s in#37=%s" % (k, k in w36, k in w37))
