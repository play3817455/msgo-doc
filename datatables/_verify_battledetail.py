# -*- coding: utf-8 -*-
"""验收：列漂移 0；两张表列序==schema、行宽==reader 最大列号+1；原列取值逐行未变。"""
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
SNAP = sorted(glob.glob(os.path.join(HERE, "_rollback", "*_battledetail")))[-1]
print("基线快照:", os.path.relpath(SNAP, ROOT))

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    # ---- 1) 全库列漂移
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
        drift.append((t, want, got[t]))
print(f"1) 列漂移表: {len(drift)} {[d[0] for d in drift]}")

# ---- 2) 两张表：列序 / 行宽 / reader 上限
for t in ("WEAPON_BATTLE_DETAIL", "MSMA_BATTLE_DETAIL"):
    d = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
    width = len(d["columns"])
    rmax = d["reader_max_csv_index"]
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute("SELECT raw_csv FROM meta.cfg_manifest WHERE file=%s", (t,))
        raw = cur.fetchone()[0]
        raw = raw.decode("utf-8", "replace") if isinstance(raw, (bytes, bytearray)) else raw
        rows = [l.rstrip("\r") for l in raw.split("\n") if l.strip() and not l.strip().startswith("#")]
        segs = sorted({r.count(",") + 1 for r in rows})
        # 客户端字段数 = 段数（尾逗号即空字段）
        fields = sorted({len(next(csv.reader([r], skipinitialspace=False))) for r in rows})
        cur.execute(f'SELECT count(*) FROM cfg."{t}"')
        n = cur.fetchone()[0]
    print(f"2) {t}: schema {width} 列｜reader_max csv#{rmax}（需 {rmax+1} 列）｜"
          f"库列 {len(got[t])}｜行 {n}")
    print(f"     manifest 段数分布 {segs} → 字段数 {fields}（含尾逗号空位）")

# ---- 3) 原列取值逐行未变
for t in ("WEAPON_BATTLE_DETAIL", "MSMA_BATTLE_DETAIL"):
    old = {}
    with open(os.path.join(SNAP, t + ".db.csv"), encoding="utf-8", newline="") as fh:
        r = csv.reader(fh)
        hdr = next(r)
        for row in r:
            old[row[0]] = dict(zip(hdr, row))
    with psycopg.connect(DSN) as conn, conn.cursor() as cur:
        cur.execute(f'SELECT * FROM cfg."{t}" ORDER BY _row_id')
        cols = [d0.name for d0 in cur.description]
        diff = 0
        checked = 0
        for row in cur:
            m = dict(zip(cols, ["" if v is None else str(v) for v in row]))
            o = old.get(m["_row_id"])
            if o is None:
                diff += 1
                continue
            for c in (hdr if hdr else []):
                if c in ("_row_id",):
                    continue
                checked += 1
                if m.get(c, "") != o.get(c, ""):
                    diff += 1
                    if diff <= 5:
                        print(f"    ✗ {t} row {m['_row_id']} {c}: {o.get(c)!r} → {m.get(c)!r}")
    print(f"3) {t}: 比对 {checked} 个原列值，差异 {diff}")
