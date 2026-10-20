# -*- coding: utf-8 -*-
"""这 6 把（及低威力族）的武器名，在 wiki sidecar 里能不能按名字找到真威力。"""
import csv
import collections
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIDE = os.path.join(ROOT, "datatables", "names", "武器分配明细.csv")
rows = [r for r in csv.reader(open(SIDE, encoding="utf-8", errors="replace")
                              .read().replace("\r\n", "\n").split("\n"))
        if r and any(x.strip() for x in r)]
H = rows[0]
print("sidecar 表头:", H[:12])
body = rows[1:]
# 找「武器名」列号：表头里有 '武器名'
NAME_C, POW_C = None, None
for i, h in enumerate(H):
    h = h.lstrip("\ufeff").strip()
    if h == "武器名":
        NAME_C = i
    if h == "威力":
        POW_C = i
print("武器名列 =", NAME_C, " 威力列 =", POW_C)

byname = collections.defaultdict(list)
for r in body:
    if len(r) <= max(NAME_C, POW_C):
        continue
    byname[r[NAME_C].strip()].append((r[1].strip(), r[POW_C].strip()))

TARGETS = ["腹部メガ粒子砲", "ビーム・ライフル", "MNG-110ビーム・ライフル",
           "3連装シールド・ミサイルランチャー", "ビーム・ショット・ライフル",
           "専用ビーム・ライフル", "100mmマシンガン", "3点式90mmジム・マシンガン"]
for t in TARGETS:
    hit = byname.get(t, [])
    pows = sorted({p for _, p in hit if p})
    print("  %-26s sidecar 命中 %3d 行；威力取值 %s" % (t, len(hit), pows[:8]))
print()
print("sidecar 武器名总数 %d；含『ビーム・ショット』的名字 %s"
      % (len(byname), [n for n in byname if "ビーム・ショット" in n][:8]))
print()
print("=== 名字模糊匹配：以『ビーム・ライフル』结尾的名字 ===")
fz = [n for n in byname if n.endswith("ビーム・ライフル")]
print("  共 %d 个，例 %s" % (len(fz), fz[:10]))
