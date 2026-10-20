# -*- coding: utf-8 -*-
"""scan_item_ids.py —— 从资源文件名里挖出「物品/武器 ID 全集」。

依据：客户端图标按 ID 命名 ——
  · interface/icon/item/d/d<数字>.dds        = 物品（武器/道具）图标
  · interface/icon/item/develop_d/d<数字>.dds = 机体开发图标（0+打包值）
  · interface/icon/battle/b/b<数字>.dds      = 战斗图标（机体号）
  · unpackdat/item/<类别>/…                  = 武器/道具资源本体（按类别分目录）

用于：补 #37 WEAPON_SETTING（武器主表）的主键池 —— 不必手工编 ID。
"""
import collections
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROOT, 'unpackdat')

KNOWN = {'1040101': 'ビームサーベル(wrestle)', '2040201': 'ヒートサーベル',
         '2040301': 'ヒートロッド', '81040101': 'ビームサーベル(別ID)',
         '213203402': 'エクシア GNブレイド', '220300001': 'ヴァイエイト ビームキャノン',
         '214801312': 'ギラ・ドーガ(袖付き)武器', '214604001': 'F91'}


def digits(name):
    m = re.match(r'^[a-z]?(\d+)\.', name, re.I)
    return m.group(1) if m else None


for sub in ('icon/item/d', 'icon/item/develop_d', 'icon/battle/b'):
    p = os.path.join(UD, 'interface', sub)
    if not os.path.isdir(p):
        print('(缺) %s' % sub)
        continue
    ids = [digits(f) for f in os.listdir(p) if f.lower().endswith('.dds')]
    ids = [x for x in ids if x]
    bylen = collections.Counter(len(x) for x in ids)
    print('=== %-20s %5d 个图标  位数分布 %s' % (sub, len(ids), dict(sorted(bylen.items()))))
    for ln in sorted(bylen):
        ex = sorted(x for x in ids if len(x) == ln)[:4]
        print('       %2d 位 %5d 个  例 %s' % (ln, bylen[ln], ex))
    hit = [k for k in KNOWN if k in set(ids) or ('0' + k) in set(ids)]
    print('       已知武器ID命中: %s' % [(k, KNOWN[k]) for k in hit])

print()
print('=== unpackdat/item/<类别>/ 里的资源命名（每类采样）===')
base = os.path.join(UD, 'item')
for d in sorted(os.listdir(base)):
    dd = os.path.join(base, d)
    if not os.path.isdir(dd):
        continue
    n = sum(len(f) for _, _, f in os.walk(dd))
    ex = []
    for dp, dn, fn in os.walk(dd):
        for f in sorted(fn)[:2]:
            ex.append(os.path.relpath(os.path.join(dp, f), dd).replace('\\', '/'))
        if len(ex) >= 2:
            break
    print('   item/%-4s %5d 文件   例 %s' % (d, n, ex))
