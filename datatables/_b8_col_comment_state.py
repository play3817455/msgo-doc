# -*- coding: utf-8 -*-
"""看 cfg.* 是否有 PostgreSQL 列注释（COMMENT ON COLUMN），以及 meta.cfg_table_def.column_defs 是否为最新"""
import io
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute(
        "select count(*) from pg_description d join pg_class cl on cl.oid=d.objoid "
        "join pg_namespace n on n.oid=cl.relnamespace where n.nspname='cfg'"
    )
    print("cfg.* 上有注释的对象数 =", cur.fetchone()[0])
    cur.execute(
        "select table_name, jsonb_array_length(column_defs) from meta.cfg_table_def "
        "where table_name in ('CHARA_MODEL','CHARA_PARAM','MSMA_RENTAL','MSMA_WEAPONSET','ITEM_PART') "
        "order by table_name"
    )
    for r in cur.fetchall():
        print("  column_defs 列数", r)
    cur.execute(
        "select jsonb_pretty(column_defs->13) from meta.cfg_table_def where table_name='CHARA_MODEL'"
    )
    print(cur.fetchone()[0])
