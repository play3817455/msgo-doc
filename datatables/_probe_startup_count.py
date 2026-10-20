# -*- coding: utf-8 -*-
"""复刻 `battledb.LoadWeaponTable`（`serverv/internal/battledb/battledb.go:83-97`）的统计口径，
还原启动日志那句「武器表就位：N 把武器（POWER x / RANGE y / RAPIDDELAY z；cfg 表 36）」。

口径（逐字对齐 Go）：
  N         = len(map) = `GROUP BY ItemKeyExpr(k)` 的组数
  POWER     = `HasPower`   ⇒ 该武器有 `POWER` 行（**不看值**）
  RANGE     = `Range != 0` ⇒ `cfgU32(值) != 0`（round 后 >0 且 ≤ u32max）
  RAPIDDELAY= `RapidDelay != 0` ⇒ 同上 ⇒ 像 `0.124580` 这种会被 round 成 0（**C3 欠账**）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg
from restore_purged_weapon_keys import pad, DSN

NZ = ("%s IS NOT NULL AND btrim(%s) ~ '^-?[0-9]*\\.?[0-9]+$' "
      "AND round(btrim(%s)::numeric) >= 1 AND round(btrim(%s)::numeric) <= 4294967295")
Q = """
SELECT count(*) AS n,
       count(*) FILTER (WHERE p IS NOT NULL) AS np,
       count(*) FILTER (WHERE {R}) AS nr,
       count(*) FILTER (WHERE {D}) AS nd
  FROM (SELECT {K} AS k,
               max(CASE WHEN btrim(attr_name)='POWER'      THEN btrim(attr_value) END) p,
               max(CASE WHEN btrim(attr_name)='RANGE'      THEN btrim(attr_value) END) r,
               max(CASE WHEN btrim(attr_name)='RAPIDDELAY' THEN btrim(attr_value) END) d
          FROM cfg."WEAPON_BATTLE_DETAIL"
         WHERE btrim(weapon_id_key) ~ '^[0-9]+$' AND btrim(attr_name) = ANY(%s)
         GROUP BY 1) t
""".replace("{K}", pad('weapon_id_key')) \
   .replace("{R}", NZ % ('r', 'r', 'r', 'r')) \
   .replace("{D}", NZ % ('d', 'd', 'd', 'd'))

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute(Q, (['POWER', 'RANGE', 'RAPIDDELAY'],))
    n, np_, nr, nd = cur.fetchone()
print("现在：武器表就位：%d 把武器（POWER %d / RANGE %d / RAPIDDELAY %d；cfg 表 36）"
      % (n, np_, nr, nd))
print("日志（2026-10-04 23:52:39 修前）：1630 把武器（POWER 1628 / RANGE 1477 / RAPIDDELAY 528）")
