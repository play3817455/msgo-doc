# -*- coding: utf-8 -*-
"""C4：把 cache 里所有「武器表」的表头原字面收集出来（设计同义词表用）。"""
import collections
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wiki'))
import parse_cache as PC  # noqa: E402


CACHE = PC.CACHE
tbl = collections.Counter()
pages = collections.defaultdict(set)
hdr_of = collections.defaultdict(set)

for f in sorted(os.listdir(CACHE)):
    if not f.endswith('.txt'):
        continue
    text = open(os.path.join(CACHE, f), encoding='utf-8').read()
    for headers, _ in PC.tables(text):
        if not headers:
            continue
        h = [x.strip() for x in headers]
        hit = [x for x in h if re.search(r'威力|恢复力|回復力|锁定|集弹|集弾', x)]
        if not hit:
            continue
        key = tuple(h)
        tbl[key] += 1
        pages[key].add(f)
        for x in h:
            hdr_of[x].add(f)

print('武器样表（表头含 威力/恢复力/锁定/集弹）不同表头组合 %d 个' % len(tbl))
print()
print('=== 全部出现的表头字面（次数=出现在几张表里）===')
for x, s in sorted(hdr_of.items(), key=lambda kv: -len(kv[1])):
    print('   %-24s 出现于 %4d 张表' % (x, len(s)))

print()
print('=== 表头组合 TOP 15 ===')
for k, n in tbl.most_common(15):
    print('   %3d × %s' % (n, list(k)))
