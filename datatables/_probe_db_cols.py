# -*- coding: utf-8 -*-
"""看 cfg.CHARA_MODEL / CHARA_PARAM 的 DB 物理列（探针）"""
import io, sys
import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in ("CHARA_MODEL", "CHARA_PARAM", "MSMA_RENTAL", "ITEM_PART"):
        cur.execute(
            "select column_name from information_schema.columns "
            "where table_schema='cfg' and table_name=%s order by ordinal_position",
            (t,),
        )
        cols = [r[0] for r in cur.fetchall()]
        print("==", t, "db cols", len(cols))
        print("   ", cols)
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        print("    rows", cur.fetchone()[0])
