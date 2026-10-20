# -*- coding: utf-8 -*-
"""临时探针 4：weapons_combat_calc.csv 的 威力→伤害 是否为 ceil(pw/10)（层二口径预检）。"""
import csv, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, '_probe_b7_fixture4.txt')


def iv(s):
    v = re.findall(r'-?\d+', (s or '').replace(',', ''))
    return int(v[0]) if v else None


n = bad = 0
samples = []
pws = []
for r in csv.DictReader(io.open(os.path.join(ROOT, 'gow_wiki/data/weapons_combat_calc.csv'),
                                 encoding='utf-8-sig')):
    p, d = iv(r.get('威力')), iv(r.get('伤害'))
    if p is None or d is None:
        continue
    n += 1
    pws.append(p)
    if -(-p // 10) != d:
        bad += 1
        if len(samples) < 10:
            samples.append((r.get('名称'), p, d))

o = io.open(OUT, 'w', encoding='utf-8')
o.write('rows=%d  ceil 不符=%d\n' % (n, bad))
for s in samples:
    o.write('  %r pw=%s dmg=%s\n' % s)
o.write('威力 非 10 倍数 行数=%d\n' % sum(1 for p in pws if p % 10))
o.write('威力 空/0 行数=%d\n' % sum(1 for p in pws if p == 0))
o.close()
print('ok')
