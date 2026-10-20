# -*- coding: utf-8 -*-
"""取基线快照：schema JSON / 种子 CSV / DB 行 / manifest（rollback 用）。"""
import io
import os
import shutil
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
STAMP = time.strftime("%Y%m%d-%H%M%S")
OUT = os.path.join(HERE, "_rollback", f"{STAMP}_battledetail")
os.makedirs(OUT, exist_ok=True)

TABLES = {
    "WEAPON_BATTLE_DETAIL": "item/weapon_battle_detail.csv",
    "MSMA_BATTLE_DETAIL": "msma/msma_battle_detail.csv",
}

for t, csv in TABLES.items():
    src = os.path.join(ROOT, "db_design", "schema", "cfg", "tables", t + ".json")
    shutil.copy2(src, os.path.join(OUT, t + ".json"))
    seed = os.path.join(ROOT, "server", "datafiles", "lounge", *csv.split("/"))
    shutil.copy2(seed, os.path.join(OUT, t + ".seed.csv"))

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in TABLES:
        cur.execute(f'SELECT * FROM cfg."{t}" ORDER BY _row_id')
        cols = [d.name for d in cur.description]
        with open(os.path.join(OUT, t + ".db.csv"), "w", encoding="utf-8", newline="") as fh:
            import csv as _csv
            w = _csv.writer(fh)
            w.writerow(cols)
            for row in cur:
                w.writerow(["" if v is None else str(v) for v in row])
        cur.execute("SELECT file, header_text, sha256, row_count, raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        r = cur.fetchone()
        with open(os.path.join(OUT, t + ".manifest.txt"), "wb") as fh:
            if r:
                fh.write((f"file={r[0]}\nsha256={r[2]}\nrow_count={r[3]}\n").encode())
                fh.write(b"--- header_text ---\n" + (r[1] or "").encode("utf-8"))
                fh.write(b"\n--- raw_csv ---\n" + (r[4] or b""))
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        print(f"{t}: DB {cur.fetchone()[0]} 行")
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s ORDER BY ordinal_position""", (t,))
        print("   列:", [x[0] for x in cur.fetchall()])

print("快照目录:", OUT)
