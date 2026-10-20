# -*- coding: utf-8 -*-
"""打印若干 cfg 表的物理列（按 ordinal_position）与行数：python _probe_cols.py T1 T2 ..."""
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in sys.argv[1:]:
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        cols = [r[0] for r in cur.fetchall()]
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        n = cur.fetchone()[0]
        print(f"[{t}] {len(cols)} 列 / {n} 行")
        print("   " + " | ".join(cols))
        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        row = cur.fetchone()
        if row and row[0]:
            raw = row[0].decode("utf-8", "replace") if isinstance(row[0], (bytes, bytearray)) else row[0]
            lines = [l.rstrip("\r") for l in raw.split("\n") if l.strip() and not l.strip().startswith("#")]
            print(f"   manifest {len(lines)} 行，前 3 行:")
            for l in lines[:3]:
                print("     " + l)
        else:
            print("   manifest: 无")
