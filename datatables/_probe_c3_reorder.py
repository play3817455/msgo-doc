# -*- coding: utf-8 -*-
"""证明生成器只改了行序、没改内容：当前 #36 vs 生成前快照（有序多重集比对）。"""
import collections
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fix_rapid_delay_units as F  # noqa: E402

A = F.T36
B = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'item',
                 'weapon_battle_detail.csv.bak_rapid20261005_004941')


def parts(p):
    rows = F.rd(p)
    head = [','.join(r) for r in rows if r[0].lstrip('\ufeff').startswith('#')]
    body = collections.Counter(','.join(r).rstrip(',') for r in rows
                               if not r[0].lstrip('\ufeff').startswith('#'))
    return head, body


ha, ba = parts(A)
hb, bb = parts(B)
print('表头相同 %s（%d 行）' % (ha == hb, len(ha)))
print('正文行数 当前 %d / 快照 %d' % (sum(ba.values()), sum(bb.values())))
only_a = ba - bb
only_b = bb - ba
print('当前独有 %d 行 %s' % (sum(only_a.values()), list(only_a.items())[:6]))
print('快照独有 %d 行 %s' % (sum(only_b.values()), list(only_b.items())[:6]))
print()
fam = [(k, c) for k, c in list(only_a.items()) + list(only_b.items())
       if k.startswith(('RAPIDDELAY,', 'COOLTIME,'))]
print('两族差异行 %d %s' % (len(fam), fam[:10]))
print('→ 内容集完全一致' if not only_a and not only_b else '→ 内容集有差异（见上）')
