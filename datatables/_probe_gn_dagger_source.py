# -*- coding: utf-8 -*-
"""为「缺 POWER 的 2 把武器」找真值来源。只读。"""
import csv
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TARGETS = ["10840101", "10840501"]
NAMES = ["GNビームダガー", "GNビームサーベル(投擲)", "ビームダガー", "ビームサーベル"]

cands = ["names/武器分配明细.csv", "names/可达武器号域.csv",
         "wiki/wiki_ms_weapons.csv", "names/武器分配明细.csv"]
for c in cands:
    p = os.path.join(HERE, c)
    if not os.path.exists(p):
        print("(缺) %s" % c)
        continue
    print("== %s  %d bytes" % (c, os.path.getsize(p)))
    with io.open(p, encoding="utf-8", errors="replace", newline="") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        continue
    print("   表头: %s" % rows[0][:12])
    for i, r in enumerate(rows[:3], 1):
        print("   样本%d: %s" % (i, r[:12]))
    hit = [r for r in rows if any(t in r for t in TARGETS)]
    print("   ID 命中 %d" % len(hit))
    for r in hit[:6]:
        print("      %s" % r[:12])
    nh = [r for r in rows if any(n in "|".join(r) for n in NAMES)]
    print("   名字命中 %d" % len(nh))
    for r in nh[:8]:
        print("      %s" % r[:12])
    print()
