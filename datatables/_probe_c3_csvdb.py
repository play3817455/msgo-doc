# -*- coding: utf-8 -*-
"""CSV ↔ 库 一致性哨：只查 #36 两族（RAPIDDELAY / COOLTIME）."""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

T36 = F.T36
rows = F.rd(T36)
body = [r for r in rows if not r[0].lstrip("\ufeff").startswith("#")]
c = collections.Counter(r[0].strip() for r in body)
print("CSV body 行数 %d" % len(body))
for a in F.ATTRS:
    print("  CSV %-11s %d" % (a, c[a]))

with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select count(*) from cfg."WEAPON_BATTLE_DETAIL"')
    print("DB 全表 %d" % cur.fetchone()[0])
    cur.execute('select btrim(attr_name), count(*) from cfg."WEAPON_BATTLE_DETAIL" group by 1')
    db = dict(cur.fetchall())
    for a in F.ATTRS:
        print("  DB  %-11s %d" % (a, db.get(a, 0)))
    cur.execute('select count(distinct btrim(weapon_id_key)) from cfg."WEAPON_BATTLE_DETAIL" '
                'where btrim(attr_name) = any(%s)', (list(F.ATTRS),))
    print("  DB  两族 distinct 键 %d" % cur.fetchone()[0])

# 逐值比对：两族的 (键, 属性) → 值
db_pairs = {}
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value) '
                'from cfg."WEAPON_BATTLE_DETAIL" where btrim(attr_name) = any(%s)', (list(F.ATTRS),))
    for k, a, v in cur.fetchall():
        db_pairs[(F.norm_key(k), a)] = v
csv_pairs = {}
for r in body:
    a = r[0].strip()
    if a in F.ATTRS:
        csv_pairs[(F.norm_key(r[1].strip()), a)] = r[2].strip()
only_db = sorted(set(db_pairs) - set(csv_pairs))
only_csv = sorted(set(csv_pairs) - set(db_pairs))
diff = sorted(k for k in set(db_pairs) & set(csv_pairs) if db_pairs[k] != csv_pairs[k])
print()
print("两族 pair：库 %d / CSV %d" % (len(db_pairs), len(csv_pairs)))
print("只在库 %d %s" % (len(only_db), only_db[:8]))
print("只在 CSV %d %s" % (len(only_csv), only_csv[:8]))
print("值不一致 %d %s" % (len(diff), [(k, db_pairs[k], csv_pairs[k]) for k in diff[:8]]))
bad = {k: v for (k, a), v in db_pairs.items() if a == "RAPIDDELAY" and not RAW.rapid_is_raw_domain(v)}
print("域外 RAPIDDELAY（库） %d" % len(bad))
