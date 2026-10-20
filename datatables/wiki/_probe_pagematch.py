# -*- coding: utf-8 -*-
"""一次性排查：CSV 页面名 vs cache 文件名，以及对不上的页面名 repr。"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'cache')
rows = list(csv.DictReader(open(os.path.join(HERE, 'wiki_ms_weapons.csv'),
                                encoding='utf-8-sig', newline='')))
cache_names = set(os.listdir(CACHE))


def cache_file(t):
    return re.sub(r'[\\/:*?"<>|]', '_', t) + '.txt'


print('=== 1) CSV 页面名 与 cache 文件名对不上的（去重） ===')
miss = sorted(set(r['#页面'] for r in rows if cache_file(r['#页面']) not in cache_names))
for p in miss:
    print('  CSV   %r len=%d' % (p, len(p)))
    cand = [n for n in cache_names if n[:6] == p[:6]]
    for n in cand:
        print('     近义 cache %r len=%d' % (n, len(n)))
    if not cand:
        print('     （无近义文件名）')

print()
print('=== 2) 值不可追溯行涉及的页面（去重计数） ===')
from collections import Counter
import _probe_verify_values as V
CHECK = V.CHECK


def lines_of(title):
    return V.page_lines(title)


bad = Counter()
for r in rows:
    pg = r['#页面']
    nm = r['武器名']
    if not nm:
        continue
    lines = lines_of(pg)
    hits = [i for i, l in enumerate(lines) if nm in l]
    if not hits:
        continue
    for c in CHECK:
        v = V.norm_num(r.get(c, ''))
        if not v:
            continue
        blob = '\n'.join(lines[max(0, hits[0] - 25):hits[-1] + 26])
        blob = blob.replace(',', '').replace('，', '').replace(' ', '')
        if v not in blob:
            bad[pg] += 1
            break
for p, c in bad.most_common():
    print('  %-50s %d' % (p, c))
