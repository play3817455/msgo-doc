# -*- coding: utf-8 -*-
"""在 wiki 抓取产物里找 `GNビームダガー` / `GNビームサーベル(投擲)` 的真实威力。只读。"""
import csv
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(HERE, "wiki", "wiki_ms_weapons.csv")
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")

PAT = re.compile(r"GN.*(ダガー|サーベル|ビームダガー)")

print("== wiki_ms_weapons.csv ==")
with io.open(WIKI, encoding="utf-8", errors="replace", newline="") as fh:
    rows = [r for r in csv.reader(fh) if r and any(x.strip() for x in r)]
hdr = rows[0]
print("   表头 %s" % hdr[:14])
n = 0
for r in rows:
    if len(r) < 7 or r[0].lstrip("\ufeff").startswith("#"):
        continue
    if PAT.search(r[3] if len(r) > 3 else ""):
        n += 1
        print("   %-28s | %-30s | 重量%-6s 威力%-14s 射程%-8s 集弹%-8s 连射%-8s 装填%-8s 锁定%-6s"
              % (r[0][:28], r[3][:30], r[4], r[8] if len(r) > 8 else "",
                 r[11] if len(r) > 11 else "", r[9] if len(r) > 9 else "",
                 r[10] if len(r) > 10 else "", r[12] if len(r) > 12 else "",
                 r[16] if len(r) > 16 else ""))
print("   命中 %d 行" % n)

print()
print("== sidecar 武器分配明细.csv 里的 GN 系 ==")
with io.open(SIDE, encoding="utf-8", errors="replace", newline="") as fh:
    s = [r for r in csv.reader(fh) if r and any(x.strip() for x in r)]
for r in s:
    if len(r) > 11 and PAT.search(r[5]):
        print("   %s | %s | %s | 重量%s 威力%s 集弹%s 连射%s 射程%s" % (r[1], r[2], r[5][:26],
                                                                      r[6], r[10], r[11],
                                                                      r[12] if len(r) > 12 else "",
                                                                      r[13] if len(r) > 13 else ""))
