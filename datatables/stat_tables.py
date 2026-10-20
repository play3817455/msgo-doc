# -*- coding: utf-8 -*-
"""stat_tables.py —— 统计服务端下发的每张表里**真实数据行**有多少（注释行不算）。
目的：看清原版运营到底填了多少数据（用户判断：原版不会给自己找麻烦）。
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'server', 'datafiles')

rows = []
for dp, dn, fn in os.walk(D):
    for f in sorted(fn):
        if not f.lower().endswith('.csv'):
            continue
        p = os.path.join(dp, f)
        t = open(p, encoding='utf-8', errors='replace').read().splitlines()
        data = [l for l in t if l.strip() and not l.lstrip().startswith('#')]
        com = [l for l in t if l.lstrip().startswith('#')]
        keys = set()
        for l in data:
            k = l.split(',')[0].strip()
            if k:
                keys.add(k)
        rows.append((os.path.relpath(p, D).replace('\\', '/'), len(data), len(com), len(keys),
                     os.path.getsize(p)))
rows.sort(key=lambda r: -r[1])
print('%-46s %6s %6s %6s %9s' % ('表', '数据行', '注释行', '唯一键', '字节'))
print('-' * 82)
allz = 0
for r in rows:
    tag = '  ← 空表!' if r[1] == 0 else ''
    print('%-46s %6d %6d %6d %9d%s' % (r[0], r[1], r[2], r[3], r[4], tag))
    if r[1] == 0:
        allz += 1
print('-' * 82)
print('共 %d 张表；其中 **完全没有数据行** 的 %d 张，有数据的 %d 张'
      % (len(rows), allz, len(rows) - allz))
print('有数据的表：')
for r in rows:
    if r[1]:
        print('   %-44s %5d 行' % (r[0], r[1]))
