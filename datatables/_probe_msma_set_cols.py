# -*- coding: utf-8 -*-
"""看现役 msma_weapon_set.csv 的表头与「短号」出现在哪一列。"""
import csv
import collections
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "server", "datafiles", "lounge", "msma", "msma_weapon_set.csv")
rows = [r for r in csv.reader(open(P, encoding="utf-8", errors="replace")
                              .read().replace("\r\n", "\n").split("\n"))
        if r and any(x.strip() for x in r)]
print("总行 %d" % len(rows))
for i, r in enumerate(rows[:6]):
    print("  [%d] %s" % (i, ",".join(r[:10])))
body = [r for r in rows if not r[0].lstrip("\ufeff").startswith("#")]
print("数据行 %d；列数分布 %s" % (len(body), dict(sorted(collections.Counter(
    len(r) for r in body).items()))))

# 每列的 id 位数分布
for c in range(min(10, max(len(r) for r in body))):
    L = collections.Counter(len(r[c].strip()) for r in body
                            if len(r) > c and r[c].strip().isdigit())
    if L:
        print("  col%d 位数分布 %s  样例 %s" % (
            c, dict(sorted(L.items())),
            [r[c].strip() for r in body[:3] if len(r) > c]))

short = {"04010101", "04840401", "02840151", "04842501", "10020101", "01010401",
         "02200101", "04840201", "02841701", "04200101", "04200151", "08010101",
         "02840101", "03010101", "10840501", "10840101", "04840601", "02711603"}
print()
for c in range(len(body[0])):
    hit = [(i, r[c].strip()) for i, r in enumerate(body) if len(r) > c and r[c].strip() in short]
    if hit:
        print("col%d 含短号 %d 处：%s" % (c, len(hit), sorted({v for _, v in hit})))
