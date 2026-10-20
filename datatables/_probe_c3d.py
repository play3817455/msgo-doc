# -*- coding: utf-8 -*-
"""C3 取证 ③：把库里「怪带」的键拉出来，看它的 sidecar 整行是哪个列等于那个值。"""
import os, sys, csv, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import psycopg
from restore_purged_weapon_keys import DSN

SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
rows = [r for r in csv.reader(
    open(SIDE, encoding='utf-8', errors='replace', newline='').read().replace('\r\n', '\n').split('\n'))
    if r and any(x.strip() for x in r)]
H = [h.strip() for h in rows[0]]
S = {}
for r in rows[1:]:
    if len(r) > 1 and r[1].strip().isdigit():
        S[r[1].strip()] = r

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name)='RAPIDDELAY'""")
    rap = cur.fetchall()

WEIRD = {200,300,330,350,360,390,400,420,450,480,500,510,530,540,560,570,580,600,620,630,640,660,
         680,690,700,710,720,740,750,760,780,810,840,870,880,900,940,960,1170,1200,1230,1667,
         2250,2500,2917,3333,3750,4167,5000}
byv = collections.defaultdict(list)
for k, v in rap:
    byv[float(v)].append(k)

print("=== 「怪带」每个值挑 1 个键，看它 sidecar 整行哪列对得上 ===")
print("列头：", " | ".join("%d:%s" % (i, H[i]) for i in (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)))
for v in sorted(WEIRD):
    ks = byv.get(float(v))
    if not ks:
        continue
    k = ks[0]
    r = S.get(k, S.get('2' + k[1:5] + k[-4:], None))
    if not r:
        # 9 位键在 sidecar 里可能不直接匹配，改用 5+4 规则
        cand = [x for x in S if x[:9] == k[:9]]
        r = S[cand[0]] if cand else None
    if not r:
        print("  %-8s key=%-10s (sidecar 无此键, n=%d)" % (v, k, len(ks)))
        continue
    cols = [(i, r[i].strip()) for i in range(6, 22) if i < len(r)]
    hit = [i for i, x in cols if x.replace('.', '').lstrip('-').isdigit() and abs(float(x) - v) < 1e-6]
    print("  %-8s key=%-10s sidecar[%s]  命中列=%s  %s" % (
        v, k, r[1].strip(), hit, " ".join("%d=%s" % (i, x) for i, x in cols)))

print()
print("=== 对照：raw 带的键，sidecar col12 是多少 ===")
for v in [0.110657, 0.12458, 0.399457, 1.391257, 1.999257]:
    for k in byv.get(v, [])[:2]:
        cand = [x for x in S if x[:9] == k[:9]]
        if cand:
            r = S[cand[0]]
            print("  raw %-9s key=%-10s sidecar col12=%-6s col10威力=%-6s col13射程=%s"
                  % (v, k, r[12].strip(), r[10].strip(), r[13].strip()))
        else:
            print("  raw %-9s key=%-10s (sidecar 无)" % (v, k))

print()
print("=== 对照：显示带（1480 等）的键，sidecar col12 是多少 ===")
for v in [1480, 1466, 1484, 1421, 1170, 1230]:
    for k in byv.get(float(v), [])[:3]:
        cand = [x for x in S if x[:9] == k[:9]]
        if cand:
            r = S[cand[0]]
            print("  disp %-6s key=%-10s sidecar col12=%-6s col13射程=%s" % (v, k, r[12].strip(), r[13].strip()))
        else:
            print("  disp %-6s key=%-10s (sidecar 无)" % (v, k))
