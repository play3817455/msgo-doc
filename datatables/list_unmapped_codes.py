# -*- coding: utf-8 -*-
"""list_unmapped_codes.py —— 盘清"哪些内部代号还没配上練度ID"（按系列分组）。

chara模型代号.csv 列：A,B,C,内部代号(可多个'/'),打包值,出处
用法：python datatables/list_unmapped_codes.py [系列过滤 如 0101]
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def rows(p):
    return [[f.strip() for f in l.rstrip(',').split(',')]
            for l in read(p).replace('\r\n', '\n').split('\n')
            if l.strip() and not l.lstrip().startswith('#')]


done = set()          # 已用的 (A,B,C)
for f in rows(os.path.join(HERE, 'names', '模型号映射-合并.csv')):
    if len(f) > 1 and re.fullmatch(r'\d{9}', f[1] or ''):
        v = int(f[1])
        done.add((v // 10**8, (v // 10**6) % 100, (v // 100) % 10000))

dirs = {}
for f in rows(os.path.join(HERE, 'names', 'chara模型代号.csv')):
    if len(f) < 5:
        continue
    try:
        a, b, c = int(f[0]), int(f[1]), int(f[2])
    except Exception:
        continue
    dirs.setdefault((a, b), []).append((c, f[3], f[4]))

flt = sys.argv[1] if len(sys.argv) > 1 else None
tot = tot_un = n_un = 0
for (a, b), lst in sorted(dirs.items()):
    key = '%02d%02d' % (a, b)
    if flt and flt not in key:
        continue
    un = [x for x in lst if (a, b, x[0]) not in done]
    tot += len(lst)
    tot_un += len(un)
    n_un += len(un)
    print('chara/%02d/%02d 目录%3d 未配%3d %s'
          % (a, b, len(lst), len(un), '✓已配' if not un else ''))
    if flt and un:
        for i in range(0, len(un), 4):
            print('     ' + '  '.join('%04d:%-22s' % (c, cd or '?') for c, cd, _ in un[i:i + 4]))
print('合计 目录 %d ｜ 未配目录 %d ｜ 已配目录 %d' % (tot, tot_un, tot - tot_un))
