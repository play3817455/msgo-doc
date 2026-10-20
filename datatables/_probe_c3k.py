# -*- coding: utf-8 -*-
"""C3 取证 ⑨：真库 709 行「原值 ↔ wiki 連射速度」的真值映射表，并核对帧带一致。"""
import os, sys, csv, io, collections, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import psycopg
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@localhost:5432/msgo")
import weapon_client_raw as RAW
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

S = [r for r in csv.reader(open(os.path.join(HERE, 'names', '武器分配明细.csv'),
                                encoding='utf-8', errors='replace')) if r and any(x.strip() for x in r)]
side = {}
for r in S[1:]:
    if len(r) > 12 and r[1].strip().isdigit():
        side[r[1].strip()] = RAW.first_tier(r[12])

K = 0.5263158082962036 * 150.0 * 10.0
def disp(raw):
    if raw <= 0 or raw >= 2.0:
        return 0
    v = (2.0 - raw) * K + 0.4
    return int(math.trunc(v)) if v > 0 else 0
def frames(w):
    return max(1, (1510 - w) // 13 + 6) if w else 0

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name)='RAPIDDELAY'""")
    rap = [(k, float(v)) for k, v in cur.fetchall()]

pairs = collections.defaultdict(collections.Counter)
for k, v in rap:
    w = side.get(k)
    if w:
        pairs[round(v, 6)][int(float(w))] += 1
print("=== 真库原值 → 它那一行的 wiki 連射速度（709 行的真值映射）===")
print("  %-12s %-28s %-8s %-6s %-8s %-6s" % ("原值", "wiki 連射(行数)", "正算白字", "帧", "wiki帧", "差"))
bad = 0
for v in sorted(pairs):
    for w, n in pairs[v].most_common():
        d, f1, f2 = disp(v), frames(disp(v)), frames(w)
        flag = "" if f1 == f2 else "  ← 帧带不一致"
        if f1 != f2:
            bad += 1
        print("  %-12.6f %-28s %-8d %-6d %-8d %-6s%s"
              % (v, "%d (%d行)" % (w, n), d, f1, f2, d - w, flag))
print()
print("帧带不一致的档位数: %d" % bad)
