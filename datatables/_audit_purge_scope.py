# -*- coding: utf-8 -*-
import csv, collections, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

def norm(k):
    k = k.strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k

RB = r"datatables\_rollback\20261004_234510_purge36_rows.csv"
keys = collections.Counter(r["weapon_id_key"].strip() for r in csv.DictReader(open(RB, encoding="utf-8")))
dist = collections.Counter(len(k) for k in keys)
print("被删 #36：%d 键 / %d 行；键长分布 %s" % (len(keys), sum(keys.values()), dict(sorted(dist.items()))))
print("  其中 ≤8 位（= 线上 u32 < 1e8，经 FormatItemKey 补零后正是这些键）: %d"
      % sum(v for k, v in dist.items() if k <= 8))
print("  ≥9 位（不补零）: %d" % sum(v for k, v in dist.items() if k >= 9))

HAND = [("2840151", 0), ("4840201", 0), ("2841701", 1), ("2711603", 2), ("1010401", 2), ("3010101", 2)]
print()
print("=== 服务端 0x1E2F.witem_id 下发的号，在库里的现状 ===")
print("%-10s %-10s %-10s %s" % ("线上u32", "FormatItemKey", "库里键", "结果"))
conn = psycopg.connect(DSN)
cur = conn.cursor()
for wid, idx in HAND:
    fk = str(wid).zfill(8)
    cur.execute("""select btrim(weapon_id_key),
                          max(case when btrim(attr_name)='POWER' then btrim(attr_value) end)
                     from cfg."WEAPON_BATTLE_DETAIL"
                    where (btrim(weapon_id_key) ~ '^[0-9]{1,8}$' and lpad(btrim(weapon_id_key),8,'0') = %s)
                       or btrim(weapon_id_key) = %s
                    group by 1""", (fk, fk))
    r = cur.fetchall()
    print("%-10s %-10s %-10s %s" % (wid, fk, r[0][0] if r else "—",
          ("POWER=%s" % r[0][1]) if r else "★查不到 ⇒ HasPower=false ⇒ 不结算伤害"))

cur.execute("""select count(distinct btrim(weapon_id_key)),
                      count(*) filter (where btrim(attr_name)='POWER'),
                      count(*) filter (where btrim(attr_name)='RANGE'),
                      count(*) filter (where btrim(attr_name)='RAPIDDELAY')
                 from cfg."WEAPON_BATTLE_DETAIL" """)
print()
print("现库 #36：键 %s / POWER 行 %s / RANGE 行 %s / RAPIDDELAY 行 %s" % cur.fetchone())
print("（运行时日志同口径：「1630 把武器（POWER 1628 / RANGE 1477 / RAPIDDELAY 528）」，与上表一致 ⇒ 启动时读的就是这份被删过的库）")
