# -*- coding: utf-8 -*-
"""第 4 批验收：全库列漂移 0；两张表物理序==schema 序、manifest 行宽==reader 上限+1、
行数不变、**按位置比对**（改名是位置保持的 `RENAME COLUMN`）原列取值逐格未变、新列 0 个 NULL。"""
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
SNAP = sorted(glob.glob(os.path.join(HERE, "_rollback", "*_narrow4")))[-1]
TABLES = ("BEGINNER_CHALLENGE", "CHALLENGE_HIGHSCORE")
print("基线快照:", os.path.relpath(SNAP, ROOT))

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    # 1) 全库列漂移
    cur.execute("""SELECT table_name FROM information_schema.tables
                   WHERE table_schema='cfg' ORDER BY table_name""")
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
    t = d.get("table") or fn[:-5]
    if t not in got:
        continue
    want = [c["db_column"] for c in d["columns"]]
    if want != got[t]:
        drift.append((t, need := [c for c in want if c not in got[t]], [c for c in got[t] if c not in want]))
print(f"1) 列漂移表: {len(drift)} {[d[0] for d in drift]}")

# 2) 两张表：列序 / 行宽 / reader 上限 / 新列 NULL
for t in TABLES:
    d = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
    width = len(d["columns"])
    rmax = d["reader_max_csv_index"]
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        raw = cur.fetchone()[0]
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
        rows = [l.rstrip("\r") for l in raw.split("\n") if l.strip() and not l.strip().startswith("#")]
        fields = sorted({len(next(csv.reader([r]))) for r in rows})
        fcounts = sorted({r.count(",") + 1 for r in rows})
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        n = cur.fetchone()[0]
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='cfg' AND table_name=%s AND column_name<>'_row_id'
                       ORDER BY ordinal_position""", (t,))
        cols = [r[0] for r in cur.fetchall()]
        cur.execute('SELECT count(*) FROM (SELECT ' + ", ".join(f'"{c}"' for c in cols) +
                    f' FROM cfg."{t}") q WHERE ' + " OR ".join(f'"{c}" IS NULL' for c in cols))
        nnull = cur.fetchone()[0]
    print(f"2) {t}: schema {width} 列（gap {d['column_gap']}）｜reader_max csv#{rmax}（需 {rmax+1} 列）｜"
          f"库列 {len(cols)}｜行 {n}｜manifest 段数 {fcounts} → 字段 {fields}｜NULL 行 {nnull}")

# 3) 按位置比对原列取值（改名是 RENAME，位置不变）
for t in TABLES:
    with open(os.path.join(SNAP, t + ".db.csv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh)
        hdr = next(r)
        old = {row[0]: row for row in r}
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute(f'SELECT * FROM cfg."{t}" ORDER BY _row_id')
        cur_cols = [d0.name for d0 in cur.description]
        diff = 0
        checked = 0
        for row in cur:
            m = ["" if v is None else str(v) for v in row]
            rid = m[cur_cols.index("_row_id")]
            o = old.get(rid)
            if o is None:
                diff += 1
                continue
            for j in range(len(hdr)):          # 位置比对：旧第 j 列 == 新第 j 列
                checked += 1
                if m[j] != o[j]:
                    diff += 1
                    if diff <= 5:
                        print(f"    ✗ {t} row {rid} 位置 {j}（{hdr[j]} → {cur_cols[j]}）: {o[j]!r} → {m[j]!r}")
    print(f"3) {t}: 位置比对 {checked} 格，差异 {diff}")
print(f"   快照原列数 {[len(hdr)]}（旧）")
