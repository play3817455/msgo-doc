# -*- coding: utf-8 -*-
"""快照/比对三张 CSV：`gen_weapon_tables_wiki.py --apply` 前后是否有非预期改动。"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DF = os.path.join(ROOT, 'server', 'datafiles', 'lounge')
FILES = [os.path.join(DF, 'item', 'item.csv'),
         os.path.join(DF, 'item', 'weapon_battle_detail.csv'),
         os.path.join(DF, 'item', 'weapon_settings.csv')]
SNAP = os.path.join(HERE, '_snap_gen.txt')

if sys.argv[1:2] == ['save'] or not os.path.exists(SNAP):
    with open(SNAP, 'w', encoding='utf-8', newline='\n') as f:
        for p in FILES:
            b = open(p, 'rb').read()
            f.write('%s\t%d\t%s\n' % (os.path.basename(p), len(b), hashlib.md5(b).hexdigest()))
    print('快照已存 %s' % os.path.relpath(SNAP, ROOT))
    if sys.argv[1:2] == ['save']:
        raise SystemExit(0)

old = {}
for line in open(SNAP, encoding='utf-8'):
    n, ln, h = line.rstrip('\n').split('\t')
    old[n] = (int(ln), h)
for p in FILES:
    b = open(p, 'rb').read()
    n = os.path.basename(p)
    ln, h = old.get(n, (0, '?'))
    print('%-28s %s  bytes %d->%d' % (n, 'SAME' if h == hashlib.md5(b).hexdigest() else 'DIFF', ln, len(b)))
