# -*- coding: utf-8 -*-
"""第 7 批前置：看三张表当前下发件（manifest）形态 + 是否有视图依赖（决定能否重建表重排物理列）。"""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
TABLES = ["COMMANDER_NPC", "MISSION_XWAR_BANPICK", "AI_PARAM"]

Q_VIEW = """
SELECT DISTINCT dn.nspname AS view_schema, dv.relname AS view_name, src.relname AS src_table
FROM pg_depend d
JOIN pg_rewrite rw ON rw.oid = d.objid
JOIN pg_class dv ON dv.oid = rw.ev_class
JOIN pg_namespace dn ON dn.oid = dv.relnamespace
JOIN pg_class src ON src.oid = d.refobjid
JOIN pg_namespace sn ON sn.oid = src.relnamespace
WHERE sn.nspname = 'cfg' AND dv.relkind IN ('v','m')
"""

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        row = cur.fetchone()
        raw = row[0] if row else ""
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else (raw or "")
        lines = [l for l in raw.split("\n") if l.strip() and not l.strip().startswith("#")]
        widths = sorted({l.count(",") + 1 for l in lines})
        print(f"=== {t}: bytes={len(raw.encode('utf-8'))} rows={len(lines)} widths={widths}")
        for l in lines[:3]:
            print("    ", l[:220])
    cur.execute(Q_VIEW)
    print("依赖 cfg 的视图:", cur.fetchall())
