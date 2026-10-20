# -*- coding: utf-8 -*-
"""对「疑似真丢」的旧行，在新 CSV 同页里找最相似的候选名（按字符重合度）。"""
import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def load(p):
    with open(os.path.join(HERE, p), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def norm(s):
    s = s or ''
    s = re.sub(r'\[\[(?:文件|File):[^\]]*\]\]', '', s)
    s = re.sub(r'<[^>]*>', '', s)
    s = re.sub(r'(?:红锁距离|诱导距离|锁定距离)[:：]?\d+', '', s)
    s = re.sub(r'[\s\u00a0\u3000]+', '', s)
    return s


old, new = load('wiki_ms_weapons.csv.bak_pre_rowspan'), load('wiki_ms_weapons.csv')
newmap = set((r['#页面'], norm(r['武器名'])) for r in new)
lost = [r for r in old if (r['#页面'], norm(r['武器名'])) not in newmap]
JUNK = re.compile(r"^\(共振\)$|^時間$|^2倍/4倍$|^TYPE-B$|^\|$|^[\d.,\s()/\-]+$")
for r in lost:
    if JUNK.match(r['武器名'] or ''):
        continue
    tgt = norm(r['武器名'])
    print('=' * 70)
    print('旧 %-44r 归一化=%r' % (r['武器名'], tgt))
    cand = [x['武器名'] for x in new if x['#页面'] == r['#页面']]
    cand.sort(key=lambda c: -len(set(norm(c)) & set(tgt)))
    for c in cand[:5]:
        same = len(set(norm(c)) & set(tgt))
        print('   新候选(重合%d) %r  [%s]' % (same, c, norm(c)))
