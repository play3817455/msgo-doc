# -*- coding: utf-8 -*-
"""盘点桥表：SET_LIDS 里有桥记录但判定非 OK 的机体（= 最终没有武器组的那批）。"""
import csv, os, io, collections, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BRIDGE = os.path.join(HERE, 'names', '机体-wiki武器页桥.csv')
WIKI   = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
SETTINGS = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_settings.csv')
OUT = os.path.join(HERE, 'names', '_bridge_audit.txt')

def read_csv(p):
    return [r for r in csv.reader(open(p, encoding='utf-8-sig', errors='replace')) if r and any(x.strip() for x in r)]

set_lids = set()
for r in csv.reader(open(SETTINGS, encoding='utf-8-sig', errors='replace')):
    if r and r[0].strip().isdigit():
        set_lids.add(r[0].strip())

wiki_pages = set()
for r in read_csv(WIKI):
    if r and not r[0].startswith('#') and r[0].strip():
        wiki_pages.add(r[0].strip())

B = read_csv(BRIDGE)
hdr = B[0]
rows = [r for r in B[1:] if r and r[0].strip().isdigit()]
# 去重（与生成器同口径）
seen, uniq = set(), []
for r in rows:
    if r[0].strip() in seen:
        continue
    seen.add(r[0].strip()); uniq.append(r)

def col(r, i):
    return (r[i].strip() if len(r) > i else '')

verdicts = collections.Counter()
missing = []
for r in uniq:
    lid = col(r, 0)
    v = col(r, 8)
    if lid not in set_lids:
        verdicts['NOT_IN_SETTINGS'] += 1
        continue
    verdicts[v or '(空)'] += 1
    if v != 'OK':
        missing.append((lid, col(r, 1), col(r, 5), v, col(r, 9)))

L = []
L.append('桥表总行 %d（去重后 %d），msma_settings 机体 %d 台，wiki 页面 %d 个'
         % (len(rows), len(uniq), len(set_lids), len(wiki_pages)))
L.append('判定分布: %s' % dict(verdicts))
L.append('')
L.append('=== SET_LIDS 内判定非 OK 的机体 %d 台 ===' % len(missing))
L.append('%-9s %-30s %-30s %-12s %s' % ('練度ID', '官方中文名', '采用页面', '判定', '备注'))
for m in sorted(missing):
    L.append('%-9s %-30s %-30s %-12s %s' % m)

# 官方名是否能在 wiki 页面名里找到「子串」→ 说明只是页面命名不同
L.append('')
L.append('=== 其中「官方中文名」是某个 wiki 页面名的子串（=别名/后缀差异，可自动修） ===')
auto = []
for lid, zh, page, v, note in sorted(missing):
    if not zh:
        continue
    hits = [p for p in wiki_pages if zh in p]
    if hits:
        auto.append((lid, zh, hits[:3]))
L.append('可自动修 %d 台' % len(auto))
for a in auto[:60]:
    L.append('%-9s %-26s -> %s' % (a[0], a[1], a[2]))

open(OUT, 'w', encoding='utf-8').write('\r\n'.join(L) + '\r\n')
print('wrote', OUT, len(L), 'lines')
