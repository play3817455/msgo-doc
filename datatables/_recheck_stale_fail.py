# -*- coding: utf-8 -*-
"""对 550200 那次旧失败清单里的 9 位 id 做现库复查（那些 id 若不在了，说明失败是旧状态）。"""
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

# 旧失败清单里的 9 位 id（+ 6 把短号报警号）
NINE = ["210002102", "214407001", "214403301", "214804201", "214701103", "226105101",
        "212002102", "214405101", "215604201", "210002001", "214413601", "215503602"]
SHORT = ["2600151", "2012401", "2240601", "12520101", "2210351", "2600101"]

conn = psycopg.connect("postgresql://postgres:admin123@127.0.0.1:5432/msgo")
cur = conn.cursor()
cur.execute('select count(distinct btrim(weapon_id_key)) from cfg."WEAPON_BATTLE_DETAIL"')
print("#36 现库唯一键 = %d（旧失败那次是 2474）" % cur.fetchone()[0])
print()
print("=== 旧失败清单里的 9 位 id 现库状态 ===")
for k in NINE:
    cur.execute('''select btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                    where btrim(weapon_id_key)=%s and btrim(attr_name)='POWER' ''', (k,))
    r = cur.fetchone()
    print("   %-11s %s" % (k, ("POWER(raw)=%s" % r[0]) if r else "（已不在 #36）"))
print()
print("=== 6 把短号报警号现库状态（含零填充形）===")
for k in SHORT:
    cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                    where btrim(weapon_id_key) in (%s,%s) and btrim(attr_name)='POWER' ''',
                (k, k.zfill(8)))
    print("   %-9s %s" % (k, cur.fetchall() or "（已不在 #36）"))
print()
cur.execute('''select btrim(weapon_id_key), btrim(attr_value) from cfg."WEAPON_BATTLE_DETAIL"
                where btrim(attr_name)='POWER' ''')
low = sorted(((float(v), k) for k, v in cur.fetchall() if float(v) < 120))
print("=== 现库 POWER(raw) < 120 的键（最弱族），共 %d 个 ===" % len(low))
for v, k in low[:16]:
    print("   %-11s %g  -> %g/发" % (k, v, v))
conn.close()
