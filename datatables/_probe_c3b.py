# -*- coding: utf-8 -*-
"""C3 取证 ②：sidecar 的「連射」列长什么样，和库里的 RAPIDDELAY 怎么对。"""
import os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '.codebuddy'))
import psycopg
from restore_purged_weapon_keys import DSN
import weapon_client_raw as RAW

SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
rows = [r for r in __import__('csv').reader(
    open(SIDE, encoding='utf-8', errors='replace', newline='').read().replace('\r\n', '\n').split('\n'))
    if r and any(x.strip() for x in r)]
H = rows[0]
print("sidecar 表头 %d 列：" % len(H))
for i, h in enumerate(H):
    print("   [%2d] %s" % (i, h.strip()))
print()
body = [r for r in rows[1:] if len(r) > 20 and r[0].strip().isdigit()]
print("sidecar 数据行 %d" % len(body))

col = 12
vals = collections.Counter()
for r in body:
    if len(r) > col:
        t = RAW.first_tier(r[col])
        vals[t if t else '(空)'] += 1
print()
print("列 [12] 的取值分布（前 40）：")
for k, n in vals.most_common(40):
    print("   %-10s %4d" % (k, n))
nums = sorted(int(float(k)) for k in vals if k != '(空)' and k.replace('.', '').replace('-', '').isdigit())
print("数值列 min=%s max=%s 共 %d 档" % (nums[0], nums[-1], len(nums)))

print()
print("=== 库里 9 位族的 RAPIDDELAY 全量去重（看是不是第三种单位）===")
with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("""select btrim(attr_value), count(*) from cfg."WEAPON_BATTLE_DETAIL"
                   where btrim(attr_name)='RAPIDDELAY' and length(btrim(weapon_id_key))>=9
                   group by 1 order by 1""")
    d = cur.fetchall()
print("  去重档位 %d 个：" % len(d))
print("   ", [float(v) for v, _n in d])
print("  行数合计 %s" % sum(n for _v, n in d))
