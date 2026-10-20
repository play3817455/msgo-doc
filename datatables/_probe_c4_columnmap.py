# -*- coding: utf-8 -*-
"""C4 列错位判定：对每条越域库行，看它的值等于**哪个属性**的期望原值 ⇒ 抓列错位。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

DOMAIN = {
    'POWER': (-3400.0, 3400.0),
    'STABILITY': (0.0, 5.0),
    'RELOAD': (0.0, 10.0),
    'RAPIDDELAY': (RAW.RAPID_RAW_LO, RAW.RAPID_RAW_HI),
    'COOLTIME': (RAW.RAPID_RAW_LO, RAW.RAPID_RAW_HI),
}

side = F.rd(F.SIDE)
S_rows = {}
S_keys = set()
for r in side:
    if len(r) > 1 and r[1].strip().isdigit():
        k = F.norm_key(r[1])
        S_keys.add(k)
        S_rows[k] = r


def expected(k):
    """键 → {attr: 期望原值字符串}（走生成器同一套换算）。"""
    r = S_rows[k]
    out = {}
    for col, attr, fn in RAW.SIDECAR_36:
        if len(r) <= col:
            continue
        p = RAW.first_tier(r[col])
        if not p:
            continue
        v, _ = RAW.attr_value(attr, p)
        out[attr] = v
    return out


with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value), '
                'btrim(attr_value_2) from cfg."WEAPON_BATTLE_DETAIL"')
    rows = [(F.norm_key(k), a.strip(), v.strip(), v2.strip()) for k, a, v, v2 in cur.fetchall()]

EXP = {}
verdict = collections.Counter()
detail = collections.defaultdict(list)
mismatch_but_in_domain = collections.Counter()

for k, a, v, v2 in rows:
    lo, hi = DOMAIN.get(a, (None, None))
    if lo is None:
        continue
    try:
        f = float(v)
    except ValueError:
        verdict['非数字'] += 1
        continue
    in_dom = lo <= f <= hi
    # 期望值比对（只对 sidecar 键 + 有该列面板的行）
    exp = EXP.get(k)
    if exp is None and k in S_rows:
        exp = EXP[k] = expected(k)
    if exp is None:
        continue
    want = exp.get(a)
    if want is None:
        if not in_dom:
            # 库里多出该属性，而 sidecar 那列是空的 ⇒ 纯残渣
            verdict['残渣(该列无面板)'] += 1
            detail['残渣(该列无面板)'].append((k, a, v))
        continue
    if v == want or (v.replace('.', '', 1).lstrip('-').isdigit() and want.replace('.', '', 1).lstrip('-').isdigit() and abs(float(v) - float(want)) < 1e-4):
        verdict['与生成器一致'] += 1
        continue
    # 值对不上 ⇒ 看它像谁
    src = [oa for oa, ov in exp.items() if oa != a and ov == v]
    if abs(float(v) - float(want)) < 1e-4:
        verdict['一致'] += 1
    if not in_dom:
        if src:
            verdict['越域=其它列的值'] += 1
            detail['越域=其它列的值'].append((k, a, v, want, src))
        else:
            verdict['越域=都不像'] += 1
            detail['越域=都不像'].append((k, a, v, want))
    else:
        verdict['域内但对不上生成器'] += 1
        detail['域内但对不上生成器'].append((k, a, v, want))

print('=== 判定汇总（仅 sidecar 键，7 属性 × 1625 键范围）===')
for k, n in verdict.most_common():
    print('   %-24s %d' % (k, n))

for tag in detail:
    d = detail[tag]
    print()
    print('=== %s（%d 条，示例前 25）===' % (tag, len(d)))
    for x in d[:25]:
        print('   ', x)

print()
print('=== 「域内但对不上生成器」的键分布（是不是集中在少数键上）===')
c = collections.Counter(k for k, *_ in detail['域内但对不上生成器'])
print('   涉及键数 %d，前 20：%s' % (len(c), c.most_common(20)))
