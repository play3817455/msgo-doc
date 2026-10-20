# -*- coding: utf-8 -*-
"""probe_icon2.py —— 用已知 143 台（練度ID + 目录 A,B,C）反推图标命名规则。"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ICON = os.path.join(ROOT, 'unpackdat', 'interface', 'icon', 'battle', 'b')

digits = [f[1:9] for f in sorted(os.listdir(ICON)) if re.match(r'^b\d{8}\.dds$', f)]
ds = set(digits)

known = []
for f in open(os.path.join(HERE, 'names', '模型号映射-补充.csv'), encoding='utf-8').read().split('\n'):
    pass
for fn in ('模型号映射-人工.csv', '模型号映射-补充.csv', '模型号映射-合并.csv'):
    p = os.path.join(HERE, 'names', fn)
    if not os.path.exists(p):
        continue
    for l in open(p, encoding='utf-8').read().replace('\r\n', '\n').split('\n'):
        if not l.strip() or l.startswith('#'):
            continue
        f = [x.strip() for x in l.rstrip(',').split(',')]
        if not re.fullmatch(r'\d{7}', f[0]):
            continue
        m9 = [x for x in f if re.fullmatch(r'\d{9}', x)]
        if m9:
            v = int(m9[0])
            known.append((f[0], v // 10**8, (v // 10**6) % 100, (v // 100) % 10000))
uniq = {k[0]: k for k in known}
known = list(uniq.values())
print('已知 %d 台' % len(known))


def cov(fn, tag):
    ok = 0
    for rid, a, b, c in known:
        for d in fn(rid, a, b, c):
            if d in ds:
                ok += 1
                break
    print('  %-40s 命中 %d / %d' % (tag, ok, len(known)))
    return ok


cov(lambda r, a, b, c: ['%02d%02d%04d' % (a, b, c)], 'A2 B2 C4  (bAABBCCCC)')
cov(lambda r, a, b, c: ['%02d%04d%02d' % (b, c, 1)], 'B2 C4 NN2')
cov(lambda r, a, b, c: ['%02d%02d%04d' % (a, c, b)], 'A2 C2 B4')
cov(lambda r, a, b, c: [r.ljust(8, '0')[:8]], '练度ID(7)补零到8')
cov(lambda r, a, b, c: ['1' + r[:7]], '1+练度ID')
cov(lambda r, a, b, c: [r[:8]], '练度ID 前8')
cov(lambda r, a, b, c: ['%02d%04d%02d' % (a, c, 1)], 'A2 C4 NN1')
cov(lambda r, a, b, c: ['%02d%02d%04d' % (b, c, a)], 'B2 C4 A2')

print()
print('图标里出现过的前 4 位（看是系列还是机体）:')
import collections
print(collections.Counter(d[:4] for d in digits).most_common(12))
print('图标里出现过的后 4 位:')
print(collections.Counter(d[4:] for d in digits).most_common(12))
