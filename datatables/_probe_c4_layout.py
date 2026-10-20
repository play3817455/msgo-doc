# -*- coding: utf-8 -*-
"""C4：sidecar 1625 行的「版面自洽」体检（列号按 sidecar 表头：
   6重量 7弹数 8射击模式 9倒地值 10威力 11集弹 12连射 13射程 14装填性能 15装填时间 16锁定 17红锁）。"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

rows = F.rd(F.SIDE)
hdr = rows[0]
data = [r for r in rows[1:] if len(r) > 1 and r[1].strip().isdigit()]
print('sidecar %d 行，表头 = %s' % (len(data), [h.strip() for h in hdr]))

MODE = re.compile(r'(自动|单发|齐射|连射|蓄力|手动|散射|扩散|连装|二连|3连|２连|2连|轮射|投掷|格斗|照射)')
NUM = re.compile(r'^-?[\d,]+(\.\d+)?$')


def cell(r, i):
    return r[i].strip() if i < len(r) else ''


AXIS = {
    10: ('威力', 0, 40000),
    11: ('集弹性能', 0, 1000),
    12: ('连射速度', 0, 5000),
    13: ('射程距离', 0, 4000),
    14: ('装填性能', 0, 1000),
    15: ('装填时间', 0, 1000),
    16: ('锁定', 0, 3000),
    17: ('红锁距离', 0, 4000),
}

bad_mode, bad_weight = [], []
bad_axis = collections.Counter()
ex = collections.defaultdict(list)

for r in data:
    k = F.norm_key(r[1])
    if cell(r, 8) and not MODE.search(cell(r, 8)):
        bad_mode.append((k, cell(r, 5), cell(r, 8), cell(r, 9)))
    if cell(r, 6) and not NUM.match(cell(r, 6)):
        bad_weight.append((k, cell(r, 5), cell(r, 6)))
    for i, (nm, lo, hi) in AXIS.items():
        t = RAW.first_tier(cell(r, i))
        if not t:
            continue
        v = abs(float(t))
        if not (lo <= v <= hi):
            bad_axis[nm] += 1
            if len(ex[nm]) < 6:
                ex[nm].append((k, cell(r, 5), t))

print()
print('★ 射击模式列不像模式的行：%d' % len(bad_mode))
for x in bad_mode[:15]:
    print('    键=%s 名=%-14s 模式列=%-12s 倒地列=%s' % x)
print()
print('★ 重量列不是数字的行：%d' % len(bad_weight))
for x in bad_weight[:10]:
    print('    ', x)
print()
print('★ 面板轴越界（说明该属性的值不是面板值/被串位）：')
for nm, n in bad_axis.most_common():
    print('    %-8s 越界 %4d  例：%s' % (nm, n, ex[nm]))
