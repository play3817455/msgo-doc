# -*- coding: utf-8 -*-
"""list_unmapped2.py —— 列出还没进 match_model_names.py CODE_NAME 的内部代号（按系列分组，紧凑）。"""
import ast
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))


def load_dict(path, name):
    tree = ast.parse(open(path, encoding='utf-8').read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, 'id', '') == name for t in n.targets):
            return ast.literal_eval(n.value)
    return {}


KEY = load_dict(os.path.join(HERE, 'match_model_names.py'), 'CODE_NAME')
# 目录代号表
dirs = []
for l in open(os.path.join(HERE, 'names', 'chara模型代号.csv'), encoding='utf-8').read().splitlines():
    if not l or l.startswith('#'):
        continue
    f = l.rstrip(',').split(',')
    if len(f) >= 5 and f[3]:
        dirs.append((int(f[0]), int(f[1]), int(f[2]), f[3]))

grp = {}
for a, b, c, codes in dirs:
    for code in codes.split('/'):
        if code not in KEY:
            grp.setdefault((a, b), []).append((c, code))

flt = sys.argv[1] if len(sys.argv) > 1 else None
tot = 0
for (a, b), lst in sorted(grp.items()):
    key = '%02d%02d' % (a, b)
    if flt and flt not in key:
        continue
    # 去重 code
    uniq = sorted(set(cd for _, cd in lst))
    tot += len(uniq)
    print('chara/%02d/%02d  %2d 个未配代号: %s' % (a, b, len(uniq), ' '.join(uniq)))
print('合计未配代号 %d 个' % tot)
