# -*- coding: utf-8 -*-
"""临时取证：#37 内容分歧行带上武器名/类别，判「维基类别」与「名称正则」谁对。只报告，不写。"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SIDE = os.path.join(HERE, "names", "武器分配明细.csv")
T78 = os.path.join(ROOT, "server", "datafiles", "lounge", "item", "item.csv")
FOCUS = {"214802001", "214802101", "214802102", "210005101", "210101103", "212301107"}

names = {}
for r in csv.reader(open(T78, encoding="utf-8", errors="replace")):
    if len(r) > 2 and r[0].strip().isdigit():
        names[r[0].strip()] = r[2].strip()

side = {}
for r in csv.reader(open(SIDE, encoding="utf-8-sig", errors="replace")):
    if len(r) > 3 and r[1].strip().isdigit() and not r[0].startswith("#"):
        side[r[1].strip()] = {"slot": r[2].strip(), "cat": r[3].strip(), "name": r[5].strip(),
                              "mode": r[8].strip(), "page": r[4].strip()}

for k in sorted(FOCUS):
    print("== %s  ITEM名=%r" % (k, names.get(k, "")))
    s = side.get(k)
    if s:
        print("   sidecar: 槽=%s 类别=%s 名=%r 模式=%s" % (s["slot"], s["cat"], s["name"], s["mode"]))
    else:
        print("   sidecar: （无行 —— 8 位族）")
