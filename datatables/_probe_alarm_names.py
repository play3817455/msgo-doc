# -*- coding: utf-8 -*-
"""6 把报警号 & 低 POWER 短号 在 cfg.ITEM 里叫什么名字（有真名=真武器；无行/怪名=孤儿）。"""
import collections
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

ALARM = ["2600151", "2012401", "2240601", "12520101", "2210351", "2600101"]
conn = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo")
cur = conn.cursor()

print("=== 6 把报警号在 cfg.ITEM 里的名字 ===")
for a in ALARM:
    cur.execute('''select btrim(item_id), btrim(name), btrim(item_type) from cfg."ITEM"
                    where btrim(item_id) in (%s, %s)''', (a, a.zfill(8)))
    print("   %-9s / %-9s -> %s" % (a, a.zfill(8), cur.fetchall() or "（ITEM 表里没有）"))
print()

print("=== #36 里 POWER<100 的键在 ITEM 表里有没有名字（这些就是 TTK 哨抓的那批）===")
cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' ''')
low = []
for k, v in cur.fetchall():
    try:
        if float(v) < 100:
            low.append((k, float(v)))
    except Exception:
        pass
low.sort(key=lambda x: x[1])
print("  共 %d 个低威力键" % len(low))
rows = []
for k, v in low[:40]:
    cur.execute('''select btrim(name), btrim(item_type) from cfg."ITEM" where btrim(item_id)=%s''', (k,))
    r = cur.fetchone()
    rows.append("%-9s P=%-7g %s" % (k, v, ("[%s] %s" % r) if r else "（ITEM 无此行）"))
for i in range(0, len(rows), 2):
    print("   " + "  |  ".join(rows[i:i + 2]))
print()

print("=== 对照：9 位族里 POWER<100 的键（362 个）在 ITEM 表的名字抽样 ===")
nine = [k for k, v in [(k, v) for k, v in
                       [(a, b) for a, b in []]] ]
cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' and length(btrim(weapon_id_key))=9''')
n9 = []
for k, v in cur.fetchall():
    try:
        if float(v) < 100:
            n9.append((k, float(v)))
    except Exception:
        pass
n9.sort(key=lambda x: x[1])
for k, v in n9[:10]:
    cur.execute('''select btrim(name), btrim(item_type) from cfg."ITEM" where btrim(item_id)=%s''', (k,))
    r = cur.fetchone()
    print("   %-11s P=%-7g %s" % (k, v, ("[%s] %s" % r) if r else "（ITEM 无此行）"))
conn.close()
