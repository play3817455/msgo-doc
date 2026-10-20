# -*- coding: utf-8 -*-
"""临时探针：B7 fixture 的联表可行性（列出后用 vitals 决定 join 口径）。"""
import collections, csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, '_probe_b7_fixture.txt')

# 表 36：POWER
pw = {}
for l in io.open(os.path.join(ROOT, 'server/datafiles/lounge/item/weapon_battle_detail.csv'),
                 encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n'):
    f = l.rstrip(',').split(',')
    if len(f) >= 3 and f[0] == 'POWER' and f[2].strip():
        pw[f[1].strip()] = f[2].strip()

# 表 65：名字
nm = {}
for l in io.open(os.path.join(ROOT, 'server/datafiles/lounge/item/item.csv'),
                 encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n'):
    if not l.strip() or l.startswith('#'):
        continue
    f = l.rstrip(',').split(',')
    if len(f) >= 5 and f[4] == 'WEAPON':
        nm[f[0].strip()] = f[2].strip()

# wiki 全量武器表：名字(2) 威力(8) ダウンポイント(?)
wk = list(csv.DictReader(io.open(os.path.join(ROOT, 'gow_wiki/data/weapons_fixed.csv'),
                                 encoding='utf-8-sig')))

o = io.open(OUT, 'w', encoding='utf-8')
o.write('# table36 POWER=%d  item.csv WEAPON=%d  wiki=%d\n' % (len(pw), len(nm), len(wk)))
o.write('# wiki 列名: %s\n' % (list(wk[0].keys()),))

by_name = collections.defaultdict(list)
for r in wk:
    by_name[(r.get('武器名') or '').strip()].append(r)

miss = [wid for wid in pw if not nm.get(wid)]
o.write('# 表36 有 POWER 但 item.csv 无名字: %d  %s\n' % (len(miss), miss[:10]))

amb = 0
nomatch = []
for wid in pw:
    name = nm.get(wid, '')
    rs = by_name.get(name, [])
    dps = set((r.get('ダウンポイント') or '').strip() for r in rs)
    if not rs:
        nomatch.append((wid, name))
    elif len(dps) > 1:
        amb += 1
        if amb <= 8:
            o.write('# 歧义 %s %s -> DP%s\n' % (wid, name, sorted(dps)))
o.write('# 无 wiki 匹配: %d\n' % len(nomatch))
for wid, name in nomatch[:20]:
    o.write('#   %s %r POWER=%s\n' % (wid, name, pw[wid]))
o.write('# DP 歧义: %d\n' % amb)

o.write('# 样例 20 条（id, name, POWER, wikiDP, wiki威力）\n')
n = 0
for wid in sorted(pw):
    name = nm.get(wid, '')
    rs = by_name.get(name)
    if not rs:
        continue
    o.write('%s\t%r\tPOWER=%s\tDP=%r\twiki威力=%r\n'
            % (wid, name, pw[wid], rs[0].get('ダウンポイント'), rs[0].get('威力')))
    n += 1
    if n >= 20:
        break
o.close()
print('wrote', OUT)
