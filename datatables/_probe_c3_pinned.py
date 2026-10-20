# -*- coding: utf-8 -*-
"""取证：4 个「现役短号」在 sidecar 行集 S 里吗？在允许键域 _W 里吗？"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import weapon_client_raw as RAW  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

PIN = ['01010401', '02711603', '02840101', '02840151']

side = F.rd(F.SIDE)
S = [r for r in side if r and r[0].strip().isdigit()]
S_keys = {F.norm_key(r[1]) for r in S if len(r) > 1 and r[1].strip()}
src = F.sidecar_rapid()

keep_all = F.rd(os.path.join(F.HERE, 'names', '可达武器号域.csv'))
W = {F.norm_key(r[0]) for r in keep_all if r and r[0].strip().isdigit()}

wl = F.rd(os.path.join(F.ROOT, '机动战士敢达Online', 'GundamOnline', 'unpackdat',
                      'settings', 'weapon_wrestle.csv'))
Wr = {F.norm_key(r[0].strip().lstrip('\ufeff')) for r in wl
      if r and r[0].strip().lstrip('\ufeff').isdigit()}

print('sidecar 总行数 S=%d，键数=%d；col12 有值键数=%d' % (len(S), len(S_keys), len(src)))
print('可达武器号域.csv 键数 %d；weapon_wrestle 键数 %d' % (len(W), len(Wr)))
print()
print('%-10s %-6s %-6s %-8s %-6s %s' % ('shortkey', 'in S', 'col12', 'in _W', 'wrestle', 'note'))
for k in PIN:
    r = [x for x in S if len(x) > 1 and F.norm_key(x[1]) == k]
    col12 = ''
    if r:
        col12 = (r[0][12].strip() if len(r[0]) > 12 else '')
    print('%-10s %-6s %-6s %-8s %-6s %s' % (
        k, 'Y' if r else 'n', repr(col12) if r else '-',
        'Y' if k in W else 'n', 'Y' if k in Wr else 'n',
        'sidecar 行在' if r else 'sidecar 无此键'))
    if r:
        print('           整行 col0..col5=%s col10..col17=%s' % (r[0][:6], r[0][10:18]))
