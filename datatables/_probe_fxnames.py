# -*- coding: utf-8 -*-
"""A 组取证 ①：库侧占位值（= 武器号）在客户端资源里**能不能被解析**。

三条独立查法：
 1. FX 注册表 `settings/fx.csv` 里有没有「纯数字」的名字，且是否等于某个武器号；
 2. 全资产树里有没有以武器号命名的文件/目录（8/9 位）；
 3. `item/` 目录的分层形状（看武器号的哪一段才是资源键）。

只报告，不写。
"""
import csv
import io
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, "机动战士敢达Online", "GundamOnline")
UD = os.path.join(G, "unpackdat")
SRV = os.path.join(ROOT, "server", "datafiles", "lounge")

# 占位值样本（库侧 #37 写的武器号）—— 从 manifest 真实在发的 #37 里取更硬
PLACEHOLDER = ["10101", "01010401", "211101101", "214801312", "223005102"]

print("=== ① fx.csv 的「名字」列是不是纯数字 ===")
fxc = os.path.join(UD, "settings", "fx.csv")
rows = list(csv.reader(open(fxc, encoding="utf-8", errors="replace")))
print("  行数 %d，头 2 行: %s" % (len(rows), rows[:2]))
num_names = []
allnames = []
for r in rows:
    for c in r:
        c = c.strip()
        if c.startswith("#") or not c:
            continue
        allnames.append(c)
        if c.isdigit():
            num_names.append(c)
print("  非注释字段 %d 个，其中**纯数字** %d 个：%s" % (len(allnames), len(num_names), num_names[:20]))
print("  含 '/' 或 '.vra' 的（= 资源路径名）示例:",
      [n for n in allnames if "/" in n or n.endswith(".vra")][:6])
hit = [p for p in PLACEHOLDER if p in set(allnames)]
print("  占位值在 fx.csv 里的命中: %s" % (hit or "0 命中"))
numset = set(num_names)
print("  占位值命中「纯数字字段」的: %s" % ([p for p in PLACEHOLDER if p in numset] or "0 命中"))

print()
print("=== ② 资产树里有没有以武器号命名的文件/目录 ===")
found = {p: [] for p in PLACEHOLDER}
pat = re.compile(r"^(" + "|".join(PLACEHOLDER) + r")$")
n_dir = n_file = 0
for dirpath, dirnames, filenames in os.walk(UD):
    for nm in dirnames + filenames:
        m = pat.match(nm)
        if m and len(found[m.group(1)]) < 4:
            found[m.group(1)].append(os.path.relpath(os.path.join(dirpath, nm), UD))
        if nm.isdigit():
            (n_dir := n_dir) if False else None
print("  命中:", {k: (v or "无") for k, v in found.items()})

print()
print("=== ③ item/ 资源目录分层（看武器号哪一段才是资源键）===")
it = os.path.join(UD, "item")
for lvl1 in sorted(os.listdir(it))[:4]:
    p1 = os.path.join(it, lvl1)
    if not os.path.isdir(p1):
        continue
    l2 = sorted(os.listdir(p1))[:8]
    print("  item/%s -> %s ..." % (lvl1, l2))
lens = Counter()
for lvl1 in os.listdir(it):
    p1 = os.path.join(it, lvl1)
    if os.path.isdir(p1):
        for lvl2 in os.listdir(p1):
            lens[len(lvl2)] += 1
print("  第二层目录名长度分布:", dict(lens))

print()
print("=== ④ 种子 CSV 里 #37 的占位列（对账面）确实是空的 ===")
t37 = os.path.join(SRV, "item", "weapon_settings.csv")
for r in list(csv.reader(open(t37, encoding="utf-8", errors="replace")))[1:4]:
    if len(r) > 2 and r[0].strip().isdigit():
        print("  id=%-10s len=%d  第74列=%r 第87列=%r 第100列=%r"
              % (r[0], len(r), r[74] if len(r) > 74 else None,
                 r[87] if len(r) > 87 else None, r[100] if len(r) > 100 else None))
