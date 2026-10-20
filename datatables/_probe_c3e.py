# -*- coding: utf-8 -*-
"""C3 取证 ④：CSV 产物里 RAPIDDELAY/COOLTIME 的分布（CSV 与库是否同源）。"""
import os, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__))
T36 = os.path.join(os.path.dirname(HERE), 'server', 'datafiles', 'lounge', 'item', 'weapon_battle_detail.csv')
raw = open(T36, encoding='utf-8', errors='replace', newline='').read().replace('\r\n', '\n')
rows = [r for r in csv.reader(raw.split('\n')) if r and any(x.strip() for x in r)]
head = rows[0]
print("CSV 表头:", head)
data = [r for r in rows[1:] if len(r) >= 3 and not r[0].lstrip().startswith('#')]
print("数据行 %d" % len(data))
cnt = collections.Counter(r[0].strip() for r in data)
print("属性分布:", dict(cnt))

for attr in ('RAPIDDELAY', 'COOLTIME', 'RANGE'):
    vals = [r[2].strip() for r in data if r[0].strip() == attr]
    if not vals:
        print("\n%s: 无行" % attr)
        continue
    print("\n=== %s 共 %d 行 ===" % (attr, len(vals)))
    print("  原样样例:", vals[:5])
    lo = [v for v in vals if v.replace('.', '').isdigit() and float(v) < 1.0]
    hi = [v for v in vals if v.replace('.', '').isdigit() and float(v) >= 1.0]
    print("  <1.0: %d 行 (样例 %s)" % (len(lo), lo[:5]))
    print("  >=1.0: %d 行 (样例 %s)" % (len(hi), hi[:8]))
    six = [v for v in vals if '.' in v and len(v.split('.')[1]) == 6]
    print("  6 位小数（= 生成器 %.6f 口径）: %d 行" % len(six))
    neg = [v for v in vals if v.startswith('-')]
    print("  负值: %d 行 (样例 %s)" % (len(neg), neg[:5]))
