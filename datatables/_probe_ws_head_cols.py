# -*- coding: utf-8 -*-
"""WEAPON_SETTING 前段列（model/variant u64）真值核查。

背景：sub_597F50 伪码显示
  col2 -> sub_BBB3F0(v5,2) 存 +8/+12（64 位）
  col3 -> sub_BBB3F0(v5,3) 存 +16/+20（64 位）
  col4 -> sub_BBB3F0(v5,4) 存 +24/+28（64 位）
  col5 -> 未见任何取列调用
若 sub_BBB3F0 单列即解析 64 位，则 schema 的 model_id_hi(csv3)/variant_id_hi(csv5) 命名错位。
本脚本用库内实际取值验证（hi 半恒 0 且 csv5 本地语义为 variant_id_hi 时，说明 csv5 客户端根本不读）。
"""
import io
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

COLS = ["weapon_setting_id", "model_id_lo", "model_id_hi", "variant_id_lo", "col5",
        "col6", "bind_model_flag", "shop_item_id", "inherit_parent_bit"]
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute(
        "SELECT " + ",".join(f'"{c}"' for c in COLS) + ' FROM cfg."WEAPON_SETTING" ORDER BY 1 LIMIT 12')
    print(" | ".join(COLS))
    for row in cur.fetchall():
        print(" | ".join(str(v) for v in row))

    stats = ",".join(
        f'count(*) filter (where "{c}"<>0) as nz_{c}' for c in
        ["model_id_hi", "col5", "variant_id_lo", "col6", "col7", "bind_model_flag"])
    cur.execute(f'SELECT count(*) as total, {stats} FROM cfg."WEAPON_SETTING"')
    names = [d.name for d in cur.description]
    print()
    print(dict(zip(names, cur.fetchone())))
