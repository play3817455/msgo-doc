# -*- coding: utf-8 -*-
"""test_series_order.py —— 检验"同一 L2 系列内，资源目录 C 号顺序 = 名册顺序"。

若成立 ⇒ 可把整个系列一次性对齐（一次性覆盖数百台）。
做法：用已确认的映射，按 (L1,L2) 分组，把已知的 (C, 名册序号) 排序打印，看是否单调。
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = os.path.join(ROOT, 'unpackdat', 'settings')


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


# 名册（保持文件顺序 = 内部序号）
roster, ridx = [], {}
for f in rows(os.path.join(S, 'favms_ok_list.csv')):
    m = re.match(r'^(\d{7})', ''.join(f))
    if m:
        rid = m.group(1)
        if rid not in ridx:
            ridx[rid] = len(roster)
            roster.append((rid, f[1] if len(f) > 1 else ''))

# 已确认映射：練度ID → 模型坐标
known = []
for fn in ('模型号映射-合并.csv',):
    for f in rows(os.path.join(HERE, 'names', fn)):
        if len(f) > 1 and re.fullmatch(r'\d{7}', f[0]) and re.fullmatch(r'\d{9}', f[1]):
            v = int(f[1])
            known.append((f[0], v // 10**8, (v // 10**6) % 100, (v // 100) % 10000, f[2] if len(f) > 2 else ''))
print('名册 %d 台 ｜ 已确认 %d 台' % (len(roster), len(known)))

grp = {}
for rid, a, b, c, nm in known:
    grp.setdefault((a, b), []).append((c, ridx.get(rid, -1), rid, nm))

print()
print('=== 按系列分组：C 号 vs 名册序号（看是否单调递增）===')
for (a, b), lst in sorted(grp.items()):
    lst.sort()
    inc = sum(1 for i in range(1, len(lst)) if lst[i][1] >= lst[i - 1][1])
    flag = '✓单调' if inc == len(lst) - 1 else '✗'
    print('chara/%02d/%02d  已知 %2d 台  %s  (名册序号 %d..%d)'
          % (a, b, len(lst), flag, lst[0][1], lst[-1][1]))
    print('     ' + ' | '.join('%04d→%d' % (c, i) for c, i, _, _ in lst[:14]))
