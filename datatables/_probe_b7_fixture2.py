# -*- coding: utf-8 -*-
"""临时探针 2：wiki 表里 威力→ダウンポイント 是否是函数（决定 fixture 能否按值 join）。"""
import collections, csv, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, '_probe_b7_fixture2.txt')

wk = list(csv.DictReader(io.open(os.path.join(ROOT, 'gow_wiki/data/weapons_fixed.csv'),
                                 encoding='utf-8-sig')))


def iv(s):
    v = re.findall(r'-?\d+', (s or '').replace(',', ''))
    return int(v[0]) if v else None


by_pw = collections.defaultdict(set)
by_pw_mode = collections.defaultdict(set)
by_pw_name = collections.defaultdict(set)
for r in wk:
    p, d = iv(r.get('威力')), iv(r.get('ダウンポイント'))
    if p is None or d is None:
        continue
    by_pw[p].add(d)
    by_pw_mode[(p, (r.get('モード') or '').strip())].add(d)

o = io.open(OUT, 'w', encoding='utf-8')
o.write('# wiki 行=%d  有(威力,DP)=%d\n' % (len(wk), sum(len(v) for v in by_pw.values())))
multi = {k: v for k, v in by_pw.items() if len(v) > 1}
o.write('# 威力 -> DP 多值 的 威力值: %d / %d\n' % (len(multi), len(by_pw)))
for k in sorted(multi)[:20]:
    o.write('#   pw=%s -> %s\n' % (k, sorted(multi[k])))
mm = {k: v for k, v in by_pw_mode.items() if len(v) > 1}
o.write('# (威力,モード) -> DP 多值: %d / %d\n' % (len(mm), len(by_pw_mode)))

# 单值映射：DP 与 威力 的关系
one = {k: sorted(v)[0] for k, v in by_pw.items() if len(v) == 1}
o.write('# 单值 威力->DP 样例(20)\n')
for k in sorted(one)[:20]:
    o.write('#   pw=%-6s dp=%s  floor(pw/10)=%s ceil(pw/10)=%s\n'
            % (k, one[k], k // 10, -(-k // 10)))

# 与 weapons_combat_calc.csv 的 ダメージ 列对账（Python 侧口径）
COMBAT = os.path.join(ROOT, 'gow_wiki/data/weapons_combat_calc.csv')
bad = 0
n = 0
for r in csv.DictReader(io.open(COMBAT, encoding='utf-8-sig')):
    p, d = iv(r.get('威力')), iv(r.get('ダメージ'))
    if p is None or d is None:
        continue
    n += 1
    if -(-p // 10) != d:
        bad += 1
        if bad <= 5:
            o.write('#  ceil 不符: %s pw=%s dmg=%s\n' % (r.get('武器'), p, d))
o.write('# combat_calc 行=%d  ceil(pw/10) 不符=%d\n' % (n, bad))
o.close()
print('wrote', OUT)
