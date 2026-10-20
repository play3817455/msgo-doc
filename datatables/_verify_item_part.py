# -*- coding: utf-8 -*-
"""第 5 批验收：`ITEM_PART` 行宽 21 → 50；全库列漂移 0；按位置逐格比对原列取值未变；新列 0 NULL。"""
import csv
import glob
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import psycopg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
T = "ITEM_PART"
SNAP = sorted(glob.glob(os.path.join(HERE, "_rollback", "*_item_part")))[-1]
print("基线快照:", os.path.relpath(SNAP, ROOT))

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    # 1) 全库列漂移
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='cfg' ORDER BY table_name")
    dbt = [r[0] for r in cur.fetchall()]
    got = {}
    for t in dbt:
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        got[t] = [r[0] for r in cur.fetchall()]
drift = []
for fn in sorted(os.listdir(SCHEMA)):
    if not fn.endswith(".json"):
        continue
    d = json.load(open(os.path.join(SCHEMA, fn), encoding="utf-8"))
    t = d.get("table") or d.get("id") or fn[:-5]
    if t not in got:
        continue
    want = [c["db_column"] for c in d["columns"]]
    if want != got[t]:
        drift.append(t)
print(f"1) 列漂移表: {len(drift)} {drift}")

# 2) 列序 / 行宽 / reader 上限 / 新列 NULL
d = json.load(open(os.path.join(SCHEMA, T + ".json"), encoding="utf-8"))
width, rmax = len(d["columns"]), d["reader_max_csv_index"]
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (T,))
    raw = cur.fetchone()[0]
    raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
    rows = [l for l in raw.split("\n") if l.strip() and not l.strip().startswith("#")]
    dist = sorted({r.count(",") + 1 for r in rows})
    cur.execute(f'SELECT count(*) FROM cfg."{T}"')
    n = cur.fetchone()[0]
    cur.execute("""SELECT column_name FROM information_schema.columns
                   WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                   ORDER BY ordinal_position""", (T,))
    cols = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT count(*) FROM (SELECT " + ", ".join(f'"{c}"' for c in cols) +
                f' FROM cfg."{T}") q WHERE ' + " OR ".join(f'"{c}" IS NULL' for c in cols))
    nnull = cur.fetchone()[0]
print(f"2) {T}: schema {width} 列｜reader_max csv#{rmax}（需 {rmax+1}）｜库列 {len(cols)}｜"
      f"行 {n}｜manifest 段数 {dist}｜NULL 行 {nnull}")

# 3) 按位置比对原列取值（改名是 RENAME，位置不变）
with open(os.path.join(SNAP, T + ".db.csv"), encoding="utf-8", newline="") as fh:
    r = csv.reader(fh)
    hdr = next(r)
    old = {row[0]: row for row in r}
with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute(f'SELECT * FROM cfg."{T}" ORDER BY _row_id')
    cur_cols = [x.name for x in cur.description]
    diff = checked = 0
    for row in cur:
        m = ["" if v is None else str(v) for v in row]
        o = old.get(m[cur_cols.index("_row_id")])
        if o is None:
            diff += 1
            continue
        for j in range(len(hdr)):
            checked += 1
            if m[j] != o[j]:
                diff += 1
                if diff <= 5:
                    print(f"    ✗ row {m[0]} 位置 {j}（{hdr[j]} → {cur_cols[j]}）: {o[j]!r} → {m[j]!r}")
print(f"3) 位置比对原列（改前 {len(hdr)} 列 × {len(old)} 行 = {len(hdr) * len(old)} 格）："
      f"实比 {checked} 格，差异 {diff}")
print(f"   新列名区间: {cols[len(hdr)]} .. {cols[-1]}")
