# -*- coding: utf-8 -*-
"""GNビームダガー / GNビームサーベル(投擲) 的数据来源取证。只读。

1) units.json 里哪台机体引用 icon_id 10840101 / 10840501，行的原始字段长啥样
2) wiki_ms_weapons.csv 里有没有 GN 系名字
3) 侧车 武器分配明细.csv 里有没有这两个 ID
"""
import csv
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGETS = {"10840101", "10840501"}

units_path = None
for c in (
    os.path.join(ROOT, "gow_wiki", "data", "units.json"),
    os.path.join(HERE, "..", "gow_wiki", "data", "units.json"),
):
    if os.path.exists(c):
        units_path = os.path.abspath(c)
        break
print("units.json =", units_path)
units = json.load(open(units_path, encoding="utf-8"))

for u in units:
    if not isinstance(u, dict):
        continue
    for g in u.get("weapons") or []:
        for r in g.get("rows") or []:
            iid = str(r.get("icon_id") or "").strip()
            if iid in TARGETS or iid.lstrip("0") in {t.lstrip("0") for t in TARGETS}:
                print("== 机体 %s dev_id=%s" % (u.get("name"), u.get("dev_id")))
                print("   行: %s" % json.dumps(r, ensure_ascii=False))
                print("   同页全部武器行 icon_id: %s" % [
                    str(x.get("icon_id")) for gg in (u.get("weapons") or []) for x in (gg.get("rows") or [])])
                print()

print("== wiki_ms_weapons.csv 里含 'GN' 的行 ==")
W = os.path.join(HERE, "wiki", "wiki_ms_weapons.csv")
with io.open(W, encoding="utf-8", errors="replace", newline="") as fh:
    rows = list(csv.reader(fh))
n = 0
for r in rows:
    if len(r) > 3 and "GN" in r[3]:
        n += 1
        if n <= 15:
            print("   %-24s | %-26s | 威力%-14s 射程%-8s" % (r[0][:24], r[3][:26],
                                                             r[8] if len(r) > 8 else "",
                                                             r[11] if len(r) > 11 else ""))
print("   命中 %d 行" % n)

print()
print("== 侧车 武器分配明细.csv 里 10840101 / 10840501 ==")
S = os.path.join(HERE, "names", "武器分配明细.csv")
with io.open(S, encoding="utf-8", errors="replace", newline="") as fh:
    srows = list(csv.reader(fh))
hdr = srows[0]
print("   表头 %s" % hdr)
for r in srows:
    if len(r) > 5 and r[1].strip() in TARGETS:
        print("   %s" % r[:14])
