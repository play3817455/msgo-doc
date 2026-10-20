# -*- coding: utf-8 -*-
"""batch8 DB 改名后数据留存抽查"""
import io
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute('select count(*) from cfg."CHARA_MODEL"')
    print("CHARA_MODEL rows", cur.fetchone()[0])
    cur.execute(
        'select model_pack_id, mesh_pair0_a, mesh_pair7_b, render_flag_44, render_param_46, '
        'lod_distance, flag_lod_54, light_color_x, light_color_y, flag_shadow, flag_render_62 '
        'from cfg."CHARA_MODEL" order by _row_id limit 3'
    )
    for r in cur.fetchall():
        print("  ", r)
    cur.execute(
        "select count(*) filter (where coalesce(lod_distance,'')<>''), "
        "count(*) filter (where coalesce(mesh_pair0_a,'')<>''), "
        "count(*) filter (where coalesce(light_color_x,'')<>''), "
        "count(*) filter (where coalesce(flag_shadow,'')<>'') from cfg.\"CHARA_MODEL\""
    )
    print("  非空计数 lod_distance/mesh_pair0_a/light_color_x/flag_shadow =", cur.fetchone())
    cur.execute('select count(*) from cfg."MSMA_WEAPONSET"')
    print("MSMA_WEAPONSET rows", cur.fetchone()[0])
    cur.execute('select weapon_group_id,reserved_u32_1,weapon_item_id,reserved_u32_3 from cfg."MSMA_WEAPONSET" order by _row_id limit 3')
    for r in cur.fetchall():
        print("  ", r)
