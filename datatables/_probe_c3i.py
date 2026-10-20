# -*- coding: utf-8 -*-
"""C3 取证 ⑦：sidecar col12（连射速度）在 916 条「空」行里到底长什么样。"""
import os, sys, csv, io, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
S = [r for r in csv.reader(open(SIDE, encoding='utf-8', errors='replace')) if r and any(x.strip() for x in r)]
body = [r for r in S[1:] if len(r) > 12 and r[1].strip().isdigit()]
c = collections.Counter(r[12].strip() for r in body)
print("sidecar col12 原样取值分布（全 %d 行）:" % len(body))
for k, n in c.most_common(30):
    print("   %-14r %4d" % (k, n))
print()
print("非数字/空 的行数:", sum(n for k, n in c.items() if not k[:1].isdigit()))
print()
# 对照：wiki 原始表里「连射速度」列的取值分布
W = [r for r in csv.reader(open(os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv'),
                                encoding='utf-8-sig', errors='replace')) if r and any(x.strip() for x in r)]
c2 = collections.Counter((r[10].strip() if len(r) > 10 else '<短行>') for r in W[1:])
print("wiki_ms_weapons col10「连射速度」取值分布（全 %d 行）:" % (len(W) - 1))
for k, n in c2.most_common(20):
    print("   %-14r %4d" % (k, n))
