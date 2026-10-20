# -*- coding: utf-8 -*-
"""C4 全量取证：CSV 里**非 sidecar 键**的每一行，逐个属性做「原值域」判定。

判据（全部来自 IDA 实测的口径，见 weapon_client_raw.py）：
  POWER      raw ⇒ panel = |raw|×10；面板现实上界 ≈ 7500 ⇒ raw 上界 ≈ 800
  STABILITY  panel = trunc((500 − mem)×2 + 0.4)，raw = mem/100 ⇒ panel 非负要求 mem ≤ 500 ⇒ raw ≤ 5
  RELOAD     panel = trunc((10 − raw)×100 + 0.4) ⇒ raw ∈ [0, 10]
  LOCKON_CAM panel = trunc(raw×10 + 0.4) ⇒ raw ≈ panel/10，面板上界 ≈ 1000 ⇒ raw ≤ 120
  RAPIDDELAY raw ∈ [0.05, 2.01]
  RANGE / HIGH_LOCKON  原样（世界单位），不给判定
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402


def verdict(attr, v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None, ''
    if attr == 'POWER':
        ok = abs(f) <= 800
        return ok, ('面板 %g' % (f * 10)) if not ok else ''
    if attr == 'STABILITY':
        ok = 0 < f <= 5
        return ok, ('面板 %d' % int((500 - f * 100) * RAW._STAB_K + 0.4)) if not ok else ''
    if attr == 'RELOAD':
        ok = 0 <= f <= 10
        return ok, ('面板 %d' % int((10 - f) * 100 + 0.4)) if not ok else ''
    if attr == 'LOCKON_CAM':
        ok = 0 < f <= 120
        return ok, ('面板 %d' % int(f * 10 + 0.4)) if not ok else ''
    if attr in ('RAPIDDELAY', 'COOLTIME'):
        return RAW.rapid_is_raw_domain(v), ''
    return None, ''


side = F.rd(F.SIDE)
S = [r for r in side if r and r[0].strip().isdigit()]
S_keys = {F.norm_key(r[1]) for r in S if len(r) > 1 and r[1].strip()}

body = [r for r in F.rd(F.T36) if not r[0].lstrip('\ufeff').startswith('#')]
nonside = [r for r in body if F.norm_key(r[1].strip()) not in S_keys]
print('CSV 正文 %d 行；非 sidecar 键的行 %d 行；涉及键 %d 个'
      % (len(body), len(nonside), len({F.norm_key(r[1].strip()) for r in nonside})))
print()
print('%-12s %-12s %-14s %-8s %s' % ('key', 'attr', 'CSV值', '原值域', '判定'))
bad = 0
for r in sorted(nonside, key=lambda x: (F.norm_key(x[1].strip()), x[0].strip())):
    k, a, v = F.norm_key(r[1].strip()), r[0].strip(), r[2].strip()
    ok, why = verdict(a, v)
    tag = '' if ok is None else ('OK' if ok else '✗越域')
    if ok is False:
        bad += 1
    print('%-12s %-12s %-14s %-8s %s' % (k, a, v, tag, why))
print()
print('越域行 %d / %d' % (bad, len(nonside)))

# 每组键的「名字」
name_of = {}
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(item_id::text), btrim(name::text) from cfg."ITEM"')
    for k, n in cur.fetchall():
        name_of[F.norm_key(k)] = n
print()
for k in sorted({F.norm_key(r[1].strip()) for r in nonside}):
    print('   %-12s %s' % (k, name_of.get(k, '(库无名)')))
