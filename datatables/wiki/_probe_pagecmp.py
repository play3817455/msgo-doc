# -*- coding: utf-8 -*-
"""打印某页新旧两版 CSV 的武器行（名字 + 关键列），用于人工核对改名/丢行。"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))


def load(p):
    with open(os.path.join(HERE, p), encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


pages = sys.argv[1:]
for pg in pages:
    print('=' * 78)
    print('页面', pg)
    for tag, fn in (('OLD', 'wiki_ms_weapons.csv.bak_pre_rowspan'), ('NEW', 'wiki_ms_weapons.csv')):
        rows = [r for r in load(fn) if r['#页面'].startswith(pg)]
        print(' %s (%d 行)' % (tag, len(rows)))
        for r in rows:
            print('    %-46r 威力=%-10s 射程=%-10s 装填=%-10s 锁定=%-8s 红锁=%-6s 重量=%-6s' % (
                r['武器名'], r['威力'], r['射程距离'], r['装填时间'], r['锁定'], r['红锁距离'], r['重量']))
