# -*- coding: utf-8 -*-
"""C4 判决：17 个非 sidecar 键，CSV 与 库 逐个属性并排 + 原值域判定。"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
from _probe_c4_scope import verdict  # noqa: E402

side = F.rd(F.SIDE)
S = [r for r in side if r and r[0].strip().isdigit()]
S_keys = {F.norm_key(r[1]) for r in S if len(r) > 1 and r[1].strip()}

body = [r for r in F.rd(F.T36) if not r[0].lstrip('\ufeff').startswith('#')]
KEYS = sorted({F.norm_key(r[1].strip()) for r in body
               if F.norm_key(r[1].strip()) not in S_keys})

csvm = collections.defaultdict(dict)
for r in body:
    csvm[F.norm_key(r[1].strip())][r[0].strip()] = r[2].strip()

dbm = collections.defaultdict(dict)
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value) '
                'from cfg."WEAPON_BATTLE_DETAIL"')
    for k, a, v in cur.fetchall():
        dbm[F.norm_key(k)][a.strip()] = v

ATTRS = ['POWER', 'STABILITY', 'RANGE', 'RELOAD', 'LOCKON_CAM', 'HIGH_LOCKON',
         'RAPIDDELAY', 'COOLTIME']
csv_bad = db_bad = both_same = 0
print('%-12s %-12s %-14s %-6s %-14s %-6s %s' %
      ('key', 'attr', 'CSV', '域', 'DB', '域', '一致?'))
for k in KEYS:
    for a in ATTRS:
        c, d = csvm[k].get(a), dbm[k].get(a)
        if c is None and d is None:
            continue
        cok = verdict(a, c)[0] if c is not None else None
        dok = verdict(a, d)[0] if d is not None else None
        if cok is False:
            csv_bad += 1
        if dok is False:
            db_bad += 1
        same = (c == d)
        if same:
            both_same += 1
        tag = lambda o: '-' if o is None else ('OK' if o else '✗越域')
        print('%-12s %-12s %-14s %-10s %-14s %-6s %s' %
              (k, a, c if c is not None else '—', tag(cok),
               d if d is not None else '—', tag(dok), '✓' if same else '✗'))
    print()
print('CSV 越域 %d 行 / 库越域 %d 行 / 两侧一致 %d 行' % (csv_bad, db_bad, both_same))
