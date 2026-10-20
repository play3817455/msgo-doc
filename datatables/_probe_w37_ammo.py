# -*- coding: utf-8 -*-
"""看那 3 个补进来的行 ammo_type_id / parent_setting_id 到底是什么（引号化，区分 NULL 与空串）。"""
import os

import psycopg
import pandas as pd

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
IDS = ("212301109", "212301110", "223005102")

with psycopg.connect(DSN) as c:
    d = pd.read_sql(
        'SELECT btrim(weapon_setting_id) AS sid,'
        ' quote_nullable(ammo_type_id) AS ammo,'
        ' quote_nullable(shop_item_id) AS shop,'
        ' quote_nullable(parent_setting_id) AS par,'
        ' quote_nullable(weapon_category) AS cat,'
        ' quote_nullable(model_id_lo) AS mlo'
        ' FROM cfg."WEAPON_SETTING" WHERE btrim(weapon_setting_id) = ANY(%(ids)s)',
        c, params={"ids": list(IDS)})
    print("=== 3 个补进来的行 ===")
    print(d.to_string(index=False))

with psycopg.connect(DSN) as c:
    d = pd.read_sql(
        'SELECT quote_nullable(ammo_type_id) AS ammo, count(*) AS n'
        ' FROM cfg."WEAPON_SETTING" GROUP BY 1 ORDER BY 1', c)
    print()
    print("=== 全表 ammo_type_id 分布（quoted）===")
    print(d.to_string(index=False))

with psycopg.connect(DSN) as c:
    d = pd.read_sql(
        "SELECT btrim(weapon_setting_id) AS sid, quote_nullable(ammo_type_id) AS ammo"
        ' FROM cfg."WEAPON_SETTING"'
        " WHERE ammo_type_id IS NULL OR btrim(ammo_type_id) IN ('', '0')"
        ' ORDER BY 1', c)
    print()
    print("=== ammo 为空/NULL/0 的行（%d 行）===" % len(d))
    print(d.to_string(index=False))
