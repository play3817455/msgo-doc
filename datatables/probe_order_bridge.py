# -*- coding: utf-8 -*-
"""probe_order_bridge.py —— 验证"練度ID 顺序 ↔ 资源目录顺序"是否同源。

若两者顺序一致（偏移恒定），就能把 53 条映射推广到全部 696 台
（用户明确：哪怕不是 100% 准确也没事，后续手工修）。
"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))


def rows(p):
    out = []
    for l in open(p, encoding='utf-8', errors='replace').read().replace('\r\n', '\n').split('\n'):
        if l.strip() and not l.lstrip().startswith('#'):
            out.append(l.rstrip(',').split(','))
    return out


UD = os.path.dirname(HERE)
fav = rows(os.path.join(UD, 'unpackdat', 'settings', 'favms_ok_list.csv'))
ids = [f[0].strip() for f in fav if f and f[0].strip()]
print('favms_ok_list: %d 台（練度ID 顺序）' % len(ids))
idx_rid = {k: i for i, k in enumerate(ids)}

cat = rows(os.path.join(HERE, 'names', 'chara目录-ID清单.csv'))
models = [f[0].strip() for f in cat if f and f[0].strip()]
print('chara目录-ID清单: %d 个モデルID' % len(models))
idx_model = {k: i for i, k in enumerate(models)}

# 目录 → モデルID 的"首个"
first_of_dir = {}
for f in cat:
    if len(f) > 5:
        first_of_dir.setdefault(f[5].strip(), f[0].strip())

mp = rows(os.path.join(HERE, 'names', '模型号映射-人工.csv'))
known = [(f[0].strip(), f[2].strip()) for f in mp if len(f) > 2 and f[2].strip()]
print('已知映射 %d 条\n' % len(known))

print('%-9s %5s  %-11s %6s  %6s' % ('練度ID', '序', 'モデルID', '序', '差'))
diffs = []
for rid, model in known:
    a, b = idx_rid.get(rid), idx_model.get(model)
    if a is None or b is None:
        print('%-9s %5s  %-11s %6s  (缺)' % (rid, a, model, b))
        continue
    diffs.append(b - a)
    print('%-9s %5d  %-11s %6d  %6d' % (rid, a, model, b, b - a))

import collections
print()
print('差值分布:', collections.Counter(diffs).most_common(8))
print('★ 若差值高度集中 ⇒ 顺序同源，可据此外推全量；否则需按名字/武器指纹匹配')
