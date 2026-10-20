# -*- coding: utf-8 -*-
"""C4 取证：从库统计每个属性的**实测原值域**（用于判定 CSV 的越域行）。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

dbm = collections.defaultdict(list)
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(attr_name), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"')
    for a, v in cur.fetchall():
        try:
            dbm[a.strip()].append(float(v))
        except ValueError:
            pass

print('%-12s %6s %12s %12s %12s %12s' % ('attr', 'n', 'min', 'p50', 'p99', 'max'))
for a in sorted(dbm):
    xs = sorted(dbm[a])
    print('%-12s %6d %12.6f %12.6f %12.6f %12.6f'
          % (a, len(xs), xs[0], xs[len(xs) // 2], xs[int(len(xs) * 0.99)], xs[-1]))

# 用实测域重新判定「两侧都越域」的那 5 个 POWER
print()
print('=== 04840201/04840401/04840601/04842501/08010101 的 POWER ===')
for k in ['04840201', '04840401', '04840601', '04842501', '08010101']:
    v = None
    with psycopg.connect(F.DSN) as conn:
        cur = conn.cursor()
        cur.execute("select btrim(attr_value) from cfg.\"WEAPON_BATTLE_DETAIL\" "
                    "where btrim(attr_name)='POWER' and btrim(weapon_id_key)=%s", (k,))
        r = cur.fetchone()
        v = r[0] if r else None
    print('   %s POWER=%s ⇒ 面板 %s（若按原值）／若它是面板值则原值应为 %s'
          % (k, v, float(v) * 10 if v else '-', RAW.power_raw(float(v)) if v else '-'))
