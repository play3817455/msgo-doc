# -*- coding: utf-8 -*-
"""C4：sidecar 表头全展开 + 同武器ID 多行/重复情况 + col14/col15 互斥性。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

side = F.rd(F.SIDE)
hdr = side[0]
print('=== sidecar 表头（共 %d 列）===' % len(hdr))
for i, h in enumerate(hdr):
    print('   col%-3d %s' % (i, h.strip()))

rows = [r for r in side[1:] if len(r) > 1 and r[1].strip().isdigit()]
cnt = collections.Counter(F.norm_key(r[1]) for r in rows)
dup = [k for k, n in cnt.items() if n > 1]
print()
print('sidecar 数据行 %d，唯一武器ID %d，重复的武器ID %d 个' % (len(rows), len(cnt), len(dup)))
for k in dup[:10]:
    print('   %s × %d' % (k, cnt[k]))

# col14 / col15 的填充互斥性
both = only14 = only15 = neither = 0
for r in rows:
    def cell(i):
        return r[i].strip() if i < len(r) else ''
    a = bool(RAW.first_tier(cell(14)))
    b = bool(RAW.first_tier(cell(15)))
    if a and b:
        both += 1
    elif a:
        only14 += 1
    elif b:
        only15 += 1
    else:
        neither += 1
print()
print('col14(装填性能)/col15(装填时间) 填充情况：只填14=%d 只填15=%d 都填=%d 都空=%d'
      % (only14, only15, both, neither))

print()
print('=== 「只填 15」的样本（库 RELOAD 是怎么来的）===')
n = 0
for r in rows:
    def cell(i):
        return r[i].strip() if i < len(r) else ''
    if not RAW.first_tier(cell(14)) and RAW.first_tier(cell(15)):
        print('   %s  %-10s col14=%-8s col15=%-10s' % (F.norm_key(r[1]), cell(3), cell(14), cell(15)))
        n += 1
        if n >= 15:
            break

print()
print('=== 「都填」的样本 ===')
n = 0
for r in rows:
    def cell(i):
        return r[i].strip() if i < len(r) else ''
    if RAW.first_tier(cell(14)) and RAW.first_tier(cell(15)):
        print('   %s  %-10s col14=%-8s col15=%-10s' % (F.norm_key(r[1]), cell(3), cell(14), cell(15)))
        n += 1
        if n >= 15:
            break

# 三个「关键列」的填充率（威力/集弹/连射/射程/装填/锁定）
print()
print('=== 关键列填充率 ===')
for i, nm in ((10, '威力'), (11, '集弹'), (12, '连射'), (13, '射程'), (14, '装填性能'),
              (15, '装填时间'), (16, '锁定'), (17, '红锁')):
    c = sum(1 for r in rows if i < len(r) and RAW.first_tier(r[i]))
    print('   col%-3d %-8s 有值 %4d / %d' % (i, nm, c, len(rows)))
