# -*- coding: utf-8 -*-
"""C4 取证：#36 全表 CSV ↔ 库 的差异逐行列出（谁多、值差、是否同键重复）。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402

with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select _row_id, btrim(weapon_id_key), btrim(attr_name), btrim(attr_value), '
                'btrim(coalesce(attr_value_2, \'\')) from cfg."WEAPON_BATTLE_DETAIL" '
                'order by _row_id')
    db_rows = cur.fetchall()
print('库 %d 行' % len(db_rows))

rows = F.rd(F.T36)
body = [r for r in rows if not r[0].lstrip('\ufeff').startswith('#')]
print('CSV %d 行' % len(body))

# 同键重复（同 attr+key 多行）—— 库侧
dup = collections.Counter((F.norm_key(k), a) for _r, k, a, _v, _v2 in db_rows)
dups = {p: n for p, n in dup.items() if n > 1}
print('库内同 (key,attr) 重复 pair：%d %s' % (len(dups), list(dups.items())[:10]))

# 同键重复 —— CSV 侧
cdup = collections.Counter((F.norm_key(r[1].strip()), r[0].strip()) for r in body)
cdups = {p: n for p, n in cdup.items() if n > 1}
print('CSV 内同 (key,attr) 重复 pair：%d %s' % (len(cdups), list(cdups.items())[:10]))

db_multi = collections.defaultdict(list)
for rid, k, a, v, v2 in db_rows:
    db_multi[(F.norm_key(k), a)].append((v, v2, rid))
csv_map = collections.defaultdict(list)
for r in body:
    csv_map[(F.norm_key(r[1].strip()), r[0].strip())].append(r[2].strip())

only_db = sorted(set(db_multi) - set(csv_map))
only_csv = sorted(set(csv_map) - set(db_multi))
diff = sorted(p for p in set(db_multi) & set(csv_map)
              if sorted(v for v, _v2, _r in db_multi[p]) != sorted(csv_map[p]))

print()
print('=== 只在库的 pair %d ===' % len(only_db))
for p in only_db:
    for v, v2, rid in db_multi[p]:
        print('   key=%-12s attr=%-12s value=%-16s value2=%-8s _row_id=%d'
              % (p[0], p[1], v, v2, rid))
print()
print('=== 只在 CSV 的 pair %d ===' % len(only_csv))
for p in only_csv[:20]:
    print('   key=%-12s attr=%-12s value=%s' % (p[0], p[1], csv_map[p]))
print()
print('=== 值不一致 pair %d ===' % len(diff))
for p in diff[:20]:
    print('   key=%-12s attr=%-12s 库=%s CSV=%s'
          % (p[0], p[1], [v for v, _v2, _r in db_multi[p]], csv_map[p]))

# 这些只存在于库的键，在 sidecar 里吗？
side = F.rd(F.SIDE)
S = [r for r in side if r and r[0].strip().isdigit()]
S_keys = {F.norm_key(r[1]) for r in S if len(r) > 1 and r[1].strip()}
keep = F.rd(os.path.join(F.HERE, 'names', '可达武器号域.csv'))
W = {F.norm_key(r[0]) for r in keep if r and r[0].strip().isdigit()}
print()
print('=== 只在库的键的来源判定 ===')
for k in sorted({p[0] for p in only_db}):
    print('   %-12s in_sidecar=%-5s in_可达号域=%-5s' % (k, k in S_keys, k in W))
