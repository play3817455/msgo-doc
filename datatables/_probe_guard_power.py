# -*- coding: utf-8 -*-
"""真库探针：受保护的 18 个短号 POWER 是多少；低 POWER 键按位数分布；unlockw 到底存了啥。"""
import csv
import collections
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = ["04010101", "04840401", "02840151", "04842501", "10020101", "01010401",
         "02200101", "04840201", "02841701", "04200101", "04200151", "08010101",
         "02840101", "03010101", "10840501", "10840101", "04840601", "02711603"]
conn = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo")
cur = conn.cursor()

print("=== #36 里 18 个受保护短号的 POWER（若 <120 则仍会拖挂 TTK 哨）===")
for g in GUARD:
    cur.execute('''select btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                    where btrim(weapon_id_key)=%s and btrim(attr_name)='POWER' ''', (g,))
    r = cur.fetchone()
    if r:
        print("   %-9s POWER(raw)=%-10s  -> 面板 %s" % (g, r[0], float(r[0]) * 10))
print()

print("=== #36 全部 POWER 按键位数（找低值族）===")
cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' ''')
by = collections.defaultdict(list)
for k, v in cur.fetchall():
    try:
        by[len(k)].append((k, float(v)))
    except Exception:
        pass
for ln in sorted(by):
    xs = sorted(x for _, x in by[ln])
    low = [(k, v) for k, v in by[ln] if v < 100]
    print("  %d 位：n=%-5d min=%-9.1f 中位=%-9.1f max=%-9.1f | POWER<100 的 %d 个"
          % (ln, len(xs), xs[0], xs[len(xs) // 2], xs[-1], len(low)))
print()

print("=== game.unlockw 的 37 个 item_id ===")
cur.execute("select distinct btrim(item_id::text) from game.unlockw")
u = sorted(k for (k,) in cur.fetchall())
print("  ", u)
print()
print("=== cfg.ITEM 里这些短号是否也带零填充孪生键 ===")
for probe in ("1010401", "01010401", "10101", "010101", "01010101", "2200101", "02200101"):
    cur.execute('''select btrim(item_id), btrim(name), btrim(item_type) from cfg."ITEM"
                    where btrim(item_id)=%s''', (probe,))
    r = cur.fetchone()
    print("   %-9s %s" % (probe, r if r else "（无）"))
conn.close()
