# -*- coding: utf-8 -*-
"""通用基线快照：python _snap_tables.py <tag> T1 T2 ...

落到 `datatables/_rollback/<stamp>_<tag>/`：每张表 4 件
  - `<T>.json`           schema 原样
  - `<T>.db.csv`         库全行（含 _row_id）
  - `<T>.manifest.txt`   meta.cfg_manifest.raw_csv 原样
  - `<T>.seed.csv`       `server/datafiles/lounge/<csv_path>` 种子原样
"""
import csv
import io
import os
import shutil
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
SEED_ROOT = os.path.join(ROOT, "server", "datafiles", "lounge")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")

tag = sys.argv[1]
tables = sys.argv[2:]
out = os.path.join(HERE, "_rollback", time.strftime("%Y%m%d-%H%M%S") + "_" + tag)
os.makedirs(out, exist_ok=True)

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    for t in tables:
        shutil.copyfile(os.path.join(SCHEMA, t + ".json"), os.path.join(out, t + ".json"))

        cur.execute(f'SELECT * FROM cfg."{t}" ORDER BY _row_id')
        cols = [d.name for d in cur.description]
        with open(os.path.join(out, t + ".db.csv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(cols)
            rows = 0
            for row in cur:
                w.writerow(["" if v is None else str(v) for v in row])
                rows += 1

        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        r = cur.fetchone()
        raw = (r[0] or "") if r else ""
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
        open(os.path.join(out, t + ".manifest.txt"), "w", encoding="utf-8", newline="").write(raw)

        spec = None
        import json
        spec = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
        rel = spec.get("csv_path") or ""
        seed = os.path.join(SEED_ROOT, *rel.split("/")) if rel else None
        if seed and os.path.isfile(seed):
            shutil.copyfile(seed, os.path.join(out, t + ".seed.csv"))
        print(f"[{t}] 库 {rows} 行 / {len(cols)} 列；manifest {len(raw)} 字节；seed "
              f"{'有' if seed and os.path.isfile(seed) else '无'}")

print("快照目录:", os.path.relpath(out, ROOT))
