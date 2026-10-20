# -*- coding: utf-8 -*-
"""C4 取证：9 个短号是不是 9 位 sidecar 武器的「另一种写法」（按名字对齐）。"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

KEYS = ['01010401', '01040101', '01040201', '02200101', '02711603',
        '02840101', '02840151', '10020101', '10840101', '10840501']

# 名字：库 cfg.ITEM（列名先探）
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute("select column_name from information_schema.columns "
                "where table_schema='cfg' and table_name='ITEM' order by ordinal_position")
    cols = [r[0] for r in cur.fetchall()]
print('cfg.ITEM 列：%s' % cols)

name_of = {}
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(item_id::text), btrim(name::text) from cfg."ITEM"')
    for k, n in cur.fetchall():
        name_of[F.norm_key(k)] = n

# sidecar：名字 -> 键
side = F.rd(F.SIDE)
S = [r for r in side if r and r[0].strip().isdigit()]
by_name = collections.defaultdict(set)
for r in S:
    if len(r) > 5 and r[5].strip():
        by_name[r[5].strip()].add(F.norm_key(r[1]))

# 也看 DB 里这些键的名字，以及 #78 的三列
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(item_id::text), btrim(name::text) from cfg."ITEM" where '
                + ' or '.join(["btrim(item_id::text) = %s"] * len(KEYS)),
                tuple(KEYS))
    print()
    print('=== 库 cfg.ITEM 里的名字 ===')
    for k, n in cur.fetchall():
        print('   %-12s %s' % (k, n))

print()
print('=== 短号 → 名字 → sidecar 同名键 ===')
for k in KEYS:
    n = name_of.get(k, '')
    hit = sorted(by_name.get(n, ()))
    print('   %-12s name=%-28s sidecar同名键=%s' % (k, (n or '(库无名)'), hit if hit else '—'))
    if hit:
        for r in S:
            if F.norm_key(r[1]) in hit:
                print('        sidecar 行 col10..col17=%s' % (r[10:18] if len(r) > 17 else r[10:]))
                break
