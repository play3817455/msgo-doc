# -*- coding: utf-8 -*-
"""键域对账（完整）：域文件的号 vs #37/#36，含**归一化（去前导 0）后**的比较。
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


def norm(s):
    return s.lstrip("0") or "0"


with io.open(DOM, encoding="utf-8-sig", newline="") as fh:
    lines = [l.rstrip("\r\n") for l in fh]
head = [l for l in lines if l.lstrip().startswith("#")]
data = [l for l in lines if l and not l.lstrip().startswith("#")]
print("=== 域文件 ===")
print("  注释头 %d 行：" % len(head))
for l in head[:6]:
    print("     %s" % l)
recs = [l.split(",") for l in data]
keys = [(r[0].strip(), (r[1].strip() if len(r) > 1 else "")) for r in recs]
domain = {k for k, _ in keys}
print("  数据行 %d ／ 去重号 %d" % (len(keys), len(domain)))
kinds = {}
for _, s in keys:
    kinds[s] = kinds.get(s, 0) + 1
print("  来源分布：%s" % kinds)
print("  号长分布：%s" % {L: sum(1 for k in domain if len(k) == L) for L in (7, 8, 9)})

with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select btrim(weapon_setting_id) from cfg."WEAPON_SETTING"')
    w37 = {r[0] for r in cur.fetchall()}
    cur.execute('select distinct btrim(weapon_id_key) from cfg."WEAPON_BATTLE_DETAIL"')
    w36 = {r[0] for r in cur.fetchall()}

print()
print("=== 原始形态 ===")
print("  #37 %d ／ #36 %d ／ 域 %d" % (len(w37), len(w36), len(domain)))
print("  #37 越域        : %d  %s" % (len(w37 - domain), sorted(w37 - domain)))
print("  域有 #37 没有   : %d" % len(domain - w37))
for k, s in sorted(keys):
    if k not in w37:
        print("       %-10s len=%d  来源=%s" % (k, len(k), s))

print()
print("=== 归一化（去前导 0）后 ===")
n37 = {norm(k) for k in w37}
ndom = {norm(k) for k in domain}
print("  #37 %d ／ 域 %d" % (len(n37), len(ndom)))
print("  #37 仍越域      : %d  %s" % (len(n37 - ndom), sorted(n37 - ndom)))
print("  域有 #37 没有   : %d  %s" % (len(ndom - n37), sorted(ndom - n37)[:40]))

print()
print("=== 域里那些 8 位带前导 0 的号：真身是什么 ===")
lead0 = sorted(k for k in domain if len(k) == 8 and k.startswith("0"))
print("  %d 个：%s" % (len(lead0), lead0))
for k in lead0:
    src = next((s for kk, s in keys if kk == k), "")
    in37 = k in w37
    n = norm(k)
    print("     %-10s → 去 0 后 %-9s 在#37=%s  来源=%s"
          % (k, n, in37, src))
