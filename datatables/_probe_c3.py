# -*- coding: utf-8 -*-
"""C3 取证：RAPIDDELAY 的两套编码到底各是什么、各有多少行。"""
import os, sys, collections, csv
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import psycopg
from restore_purged_weapon_keys import DSN
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import weapon_client_raw as RAW

def shape(k):
    k = k.strip()
    if not k.isdigit():
        return '非数字'
    return '9位+' if len(k) >= 9 else '短号(%d位)' % len(k)

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name)='RAPIDDELAY'""")
    rows = cur.fetchall()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name)='COOLTIME'""")
    cool = cur.fetchall()

print("=== #36 RAPIDDELAY 共 %d 行 ===" % len(rows))
by = collections.defaultdict(list)
for k, v in rows:
    by[shape(k)].append(float(v))
for s in sorted(by):
    vs = sorted(by[s])
    print("  %-12s %4d 行  min=%.6f  max=%.6f  样例 %s" % (s, len(vs), vs[0], vs[-1], vs[:3]))
allv = sorted(float(v) for _k, v in rows)
lo = [v for v in allv if v < 1.0]
hi = [v for v in allv if v >= 1.0]
print("  分带：<1.0 的 %d 行（%s..%s）；>=1.0 的 %d 行（%s..%s）"
      % (len(lo), lo[0] if lo else '-', lo[-1] if lo else '-',
         len(hi), hi[0] if hi else '-', hi[-1] if hi else '-'))
print("  >=1.0 那一带去重后：%s" % sorted(set(hi))[:40])
print("  <1.0 那一带去重后（前 30）: %s" % [round(x, 6) for x in sorted(set(lo))[:30]])

print()
print("=== 两带的可逆性（用 weapon_client_raw.rapid_raw 反推）===")
print("  rapid_raw(面板) -> 原值, 面板=连射显示值")
for p in (1381, 1472, 1481, 1484, 1498, 1510, 1524):
    print("    面板 %-5d -> 原值 %s" % (p, RAW.rapid_raw(p)))
print("  反过来：记忆原值 x 对应的（唯一）面板区间？")

print()
print("=== 9 位族那一带的实际样本（前 20 键）===")
for k, v in sorted(rows)[:0]:
    pass
nine = [(k, float(v)) for k, v in rows if shape(k) == '9位+']
print("  9位族 %d 行；样例 %s" % (len(nine), nine[:6]))
print("  9位族值域 %s..%s" % (min(v for _k, v in nine), max(v for _k, v in nine)))
print()
print("=== COOLTIME 共 %d 行（应与 RAPIDDELAY 同值）===" % len(cool))
byc = collections.defaultdict(list)
for k, v in cool:
    byc[shape(k)].append(float(v))
for s in sorted(byc):
    vs = sorted(byc[s])
    print("  %-12s %4d 行 min=%.6f max=%.6f 样例 %s" % (s, len(vs), vs[0], vs[-1], vs[:3]))
