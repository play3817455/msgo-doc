# -*- coding: utf-8 -*-
"""第 7 批前置：读三张表的物理列序 / 类型 / 默认值 / 约束 / 行数，为「物理重排」做准备。"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TABLES = ["COMMANDER_NPC", "MISSION_XWAR_BANPICK", "AI_PARAM"]

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        cur.execute(
            """SELECT ordinal_position, column_name, data_type, is_nullable,
                      coalesce(column_default,''), coalesce(character_maximum_length,0)
               FROM information_schema.columns
               WHERE table_schema='cfg' AND table_name=%s ORDER BY ordinal_position""", (t,))
        print(f"=== {t} 列 {cur.rowcount}")
        for r in cur.fetchall():
            print("   ", r)
        cur.execute(
            """SELECT con.conname, con.contype, pg_get_constraintdef(con.oid)
               FROM pg_constraint con JOIN pg_class c ON c.oid=con.conrelid
               JOIN pg_namespace n ON n.oid=c.relnamespace
               WHERE n.nspname='cfg' AND c.relname=%s""", (t,))
        print("    约束:", cur.fetchall())
        cur.execute(
            """SELECT indexname, indexdef FROM pg_indexes
               WHERE schemaname='cfg' AND tablename=%s""", (t,))
        print("    索引:", cur.fetchall())
