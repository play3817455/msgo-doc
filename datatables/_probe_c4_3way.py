# -*- coding: utf-8 -*-
"""C4 取证（三方对账）：对 9 个「非 sidecar 现役键」比 CSV / 库 / purge 回滚件。"""
import collections
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

KEYS = ['01010401', '01040101', '01040201', '02200101', '02711603',
        '02840101', '02840151', '10020101', '10840101', '10840501']
RB = os.path.join(HERE, '_rollback', '20261004_234510_purge36_rows.csv')

rb = collections.defaultdict(dict)
if os.path.exists(RB):
    with open(RB, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            k = F.norm_key((r.get('weapon_id_key') or '').strip())
            if k in KEYS:
                rb[k][(r.get('attr_name') or '').strip()] = ((r.get('attr_value') or '').strip(),
                                                             (r.get('_row_id') or '').strip())

db = collections.defaultdict(dict)
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value), _row_id, '
                'btrim(coalesce(attr_value_2,\'\')) from cfg."WEAPON_BATTLE_DETAIL" order by _row_id')
    for k, a, v, rid, v2 in cur.fetchall():
        if F.norm_key(k) in KEYS:
            db[F.norm_key(k)][a.strip()] = (v, rid, v2)

csvm = collections.defaultdict(dict)
for r in F.rd(F.T36):
    if r[0].lstrip('\ufeff').startswith('#'):
        continue
    k = F.norm_key(r[1].strip())
    if k in KEYS:
        csvm[k][r[0].strip()] = r[2].strip()

ATTRS = ['POWER', 'STABILITY', 'RANGE', 'RAPIDDELAY', 'COOLTIME', 'RELOAD',
         'LOCKON_CAM', 'RECOIL', 'SWITCHTIME', 'SHIELD', 'HIGH_LOCKON']
for k in KEYS:
    print('=== %s ===' % k)
    print('   %-12s %-22s %-22s %s' % ('attr', 'CSV', 'DB', '回滚件(20261004_234510)'))
    for a in ATTRS:
        c = csvm[k].get(a)
        d = db[k].get(a)
        r = rb[k].get(a)
        if c is None and d is None and r is None:
            continue
        print('   %-12s %-22s %-22s %s' % (
            a, c if c is not None else '-',
            ('%s (id=%s)' % (d[0], d[1])) if d else '-',
            ('%s (id=%s)' % (r[0], r[1])) if r else '-'))
    print()
