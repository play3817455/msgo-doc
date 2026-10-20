# -*- coding: utf-8 -*-
"""C4 单键透视：sidecar 表头↔值、库行、CSV 行 三方并排。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

KEYS = [x for x in sys.argv[1:] if x.strip()] or ['231301101', '225801109', '251401103', '210001101']

side = F.rd(F.SIDE)
hdr = side[0]
S = {}
for r in side[1:]:
    if len(r) > 1 and r[1].strip().isdigit():
        S[F.norm_key(r[1])] = r

csv_rows = {}
for r in F.rd(F.T36):
    k = F.norm_key(r[1]) if len(r) > 1 else ''
    csv_rows.setdefault(k, []).append(r)

name = {}
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(item_id::text), btrim(name::text) from cfg."ITEM"')
    for k, n in cur.fetchall():
        name[F.norm_key(k)] = n
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value), '
                'btrim(attr_value_2) from cfg."WEAPON_BATTLE_DETAIL"')
    db = [(F.norm_key(k), a.strip(), v.strip(), v2.strip()) for k, a, v, v2 in cur.fetchall()]

for key in KEYS:
    print('=' * 78)
    print('KEY %s   %s' % (key, name.get(key, '(库无名)')))
    print('-' * 78)
    r = S.get(key)
    if r is None:
        print('  sidecar: (无此键)')
    else:
        for i, h in enumerate(hdr):
            if i < len(r) and r[i].strip() and r[i].strip() != '-':
                print('   col%-3d %-22s = %s' % (i, h.strip(), r[i].strip()))
    print('-' * 78)
    print('  库 #36:')
    for k, a, v, v2 in db:
        if k == key:
            print('     %-14s = %-16s (v2=%s)' % (a, v, v2))
    print('  库 #37: (略)')
    print('   CSV 行:')
    for row in csv_rows.get(key, []):
        print('     %s' % (row,))
