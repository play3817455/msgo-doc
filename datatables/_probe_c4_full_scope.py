# -*- coding: utf-8 -*-
"""C4 全量口径体检：#36 每个属性的库值，按 IDA 口径域统计越域行 + 落到哪些键。"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
import fix_rapid_delay_units as F  # noqa: E402
import weapon_client_raw as RAW  # noqa: E402

# ── 口径域（由 weapon_client_raw 的换算反推 + 真库实测）
#   POWER      raw = panel/10，面板实测 200..34000 ⇒ |raw| ≤ 3400（回复系可为负）
#   STABILITY  raw = mem/100，面板 = trunc((500−mem)×2+0.4) ⇒ mem ∈ (0,500] ⇒ raw ∈ (0,5]
#   RELOAD     raw = 10 − panel/100，面板 0..1000 ⇒ raw ∈ [0,10]
#   LOCKON_CAM raw ≈ panel/10，面板 = trunc(raw×10+0.4)
#   RANGE / HIGH_LOCKON / RECOIL / SWITCHTIME / SHIELD  原样或不参与本套
DOMAIN = {
    'POWER': (-3400.0, 3400.0),
    'STABILITY': (0.0, 5.0),
    'RELOAD': (0.0, 10.0),
    'RAPIDDELAY': (RAW.RAPID_RAW_LO, RAW.RAPID_RAW_HI),
    'COOLTIME': (RAW.RAPID_RAW_LO, RAW.RAPID_RAW_HI),
}

side = F.rd(F.SIDE)
S = [r for r in side if r and r[0].strip().isdigit()]
S_keys = {F.norm_key(r[1]) for r in S if len(r) > 1 and r[1].strip()}

with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(weapon_id_key), btrim(attr_name), btrim(attr_value) '
                'from cfg."WEAPON_BATTLE_DETAIL"')
    rows = cur.fetchall()

# LOCKON_CAM 的域先从**sidecar 生成的那批**（= 有权威来源的）里量出来
lock_ok = []
for k, a, v in rows:
    if a.strip() in ('LOCKON_CAM',) and F.norm_key(k) in S_keys:
        try:
            lock_ok.append(float(v))
        except ValueError:
            pass
lock_ok.sort()
print('LOCKON_CAM 的 sidecar 权威样本 %d 个：min=%.6f max=%.6f' % (len(lock_ok), lock_ok[0], lock_ok[-1]))
DOMAIN['LOCKON_CAM'] = (0.0, lock_ok[-1] * 1.001)

by_attr = collections.defaultdict(lambda: [0, 0, collections.Counter()])
bad_keys_all = collections.Counter()
for k, a, v in rows:
    a = a.strip()
    lo, hi = DOMAIN.get(a, (None, None))
    if lo is None:
        continue
    try:
        f = float(v)
    except ValueError:
        by_attr[a][1] += 1
        continue
    nk = F.norm_key(k.strip())
    if lo <= f <= hi:
        by_attr[a][0] += 1
    else:
        by_attr[a][1] += 1
        by_attr[a][2][nk] += 1
        bad_keys_all[nk] += 1

print()
print('%-12s %8s %8s %8s   越域键（前 12）' % ('attr', '域内', '越域', '合计'))
for a in sorted(DOMAIN):
    inn, out, ctr = by_attr[a]
    print('%-12s %8d %8d %8d   %s' % (a, inn, out, inn + out, list(ctr)[:12]))

name_of = {}
with psycopg.connect(F.DSN) as conn:
    cur = conn.cursor()
    cur.execute('select btrim(item_id::text), btrim(name::text) from cfg."ITEM"')
    for k, n in cur.fetchall():
        name_of[F.norm_key(k)] = n

print()
print('=== 有越域行的键共 %d 个（按越域行数排序，前 40）===' % len(bad_keys_all))
for k, n in bad_keys_all.most_common(40):
    print('   %-12s 越域 %d 行  in_sidecar=%-5s  %s'
          % (k, n, k in S_keys, name_of.get(k, '(库无名)')))
print()
print('其中 in_sidecar=True 的键：%s'
      % sorted(k for k in bad_keys_all if k in S_keys))
