# -*- coding: utf-8 -*-
import csv, os, sys, io, collections, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '.codebuddy'))
import fpmf_scan as F
GAME = os.path.join(ROOT, '机动战士敢达Online', 'GundamOnline')
P = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_weapon_set.csv')

raw = open(P, 'rb').read()
print('CRLF:', raw.count(b'\r\n') == raw.count(b'\n'), '| BOM:', raw[:3] == b'\xef\xbb\xbf', '| 行数:', raw.count(b'\r\n'))
L = [x for x in raw.decode('utf-8').split('\r\n') if x]
R = [x for x in L if not x.startswith('#')]
print('data rows:', len(R), '| 非31字段:', sum(1 for x in R if len(x.split(',')) != 31))
D = [r for r in csv.reader(R) if r and r[0].strip().isdigit()]
print('可解析:', len(D))

g = collections.Counter(r[0].strip() for r in D)
print('机体组数:', len(g), '| 组大小分布:', dict(collections.Counter(g.values())))

S = [r for r in csv.reader(open(os.path.join(ROOT, 'server/datafiles/lounge/msma/msma_settings.csv'), encoding='utf-8-sig')) if r and r[0].strip().isdigit()]
lids = [r[0].strip() for r in S]
print('settings 机体 %d | 有武器组 %d | 空 %d' % (len(lids), sum(1 for l in lids if l in g), sum(1 for l in lids if l not in g)))
extra = set(g) - set(lids)
print('有武器组但不在 settings 的 lid:', len(extra), sorted(extra)[:8])

_, files = F.load_hed(os.path.join(GAME, 'data', 'item.hed'))
dirs = set()
for f in files:
    p = (f['path'] or f['folder']).lstrip('.\\/').replace('\\', '/').split('/')
    if len(p) >= 2 and p[0] == '02':
        dirs.add(p[1])
print('item/02 目录数:', len(dirs))

# 校验：每个 col2 的 sub4 必须在 dirs 且 sub4[0]==lid[5]，且 ID == '2'+lid[1:5]+sub4
bad = []
for r in D:
    lid, w = r[0].strip(), r[2].strip()
    s4 = w[5:9]
    if len(w) != 9 or w[0] != '2' or w[1:5] != lid[1:5] or s4 != w[5:9] or s4[0] != lid[5] or s4 not in dirs:
        bad.append((lid, w, s4))
print('★ col2 违规（律/资源不符）:', len(bad), bad[:5])
print('★ col2 落资源成功率: %d/%d' % (len(D) - len(bad), len(D)))

print('地区列:', dict(collections.Counter(r[28].strip() for r in D if len(r) > 28)))
print('槽位列:', dict(collections.Counter(r[4].strip() for r in D if len(r) > 4)))
print('类别列:', dict(collections.Counter(r[5].strip() for r in D if len(r) > 5).most_common()))
print('col6 全为1:', all(r[6].strip() == '1' for r in D if len(r) > 6))
print('col7..col27 全空:', all(all(not x.strip() for x in r[7:28]) for r in D))
print('col1/col3 空:', all(not r[1].strip() and not r[3].strip() for r in D if len(r) > 3))
