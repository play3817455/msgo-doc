# -*- coding: utf-8 -*-
"""机体表（wiki_ms_stats.csv）新旧逐格比对：谁变了、是丢值还是补值。"""
import csv
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def load(p):
    with open(os.path.join(HERE, p), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


old, new = load('wiki_ms_stats.csv.bak_pre_rowspan'), load('wiki_ms_stats.csv')
K = '#页面'
old = [r for r in old if r.get(K)]
new = [r for r in new if r.get(K)]
print('机体行 old/new:', len(old), len(new))
po = set(r[K] for r in old)
pn = set(r[K] for r in new)
print('页面 丢/增:', len(po - pn), len(pn - po))
cols = [c for c in old[0].keys() if c not in (K, '数据格式')]
mo = {r[K]: r for r in old}
mn = {r[K]: r for r in new}
lost, got, diff_pages = Counter(), Counter(), []
for p in sorted(po & pn):
    d = []
    for c in cols:
        a, b = (mo[p].get(c) or '').strip(), (mn[p].get(c) or '').strip()
        if a != b:
            d.append((c, a, b))
            (lost if (a and not b) else got)[c] += 1
    if d:
        diff_pages.append((p, d))
print('有差异的页面 %d 个' % len(diff_pages))
print('★ 丢值（旧有值→新空）的列：', dict(lost))
print('  补/改值的列：', dict(got))
for p, d in diff_pages[:15]:
    print('  %-40s %s' % (p[:40], d[:6]))
