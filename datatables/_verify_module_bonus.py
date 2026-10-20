# -*- coding: utf-8 -*-
"""第 6 批验收：`MODULE_BONUS` 行宽 6 → 41；全库列漂移 0；按位置逐格比对原列取值未变；新列 0 NULL。

额外断言（结构自证，来自静态反汇编）：
  * 列数 41 = csv0..csv40；`reader_max_csv_index` == 40；
  * 缝列集合 == {0, 3, 6, 8, 11, 13, 16, 18, 21, 23, 26, 28, 31, 33, 36, 38}（16 个）；
  * 组 k 的三列 = csv {5k-3, 5k-1, 5k} ↔ 内存 {+4+12(k-1), +8+12(k-1), +12+12(k-1)}；
  * 物理列序 == schema 列序（逐列同名同序）⇒ csv_index 与物理位置一一对应。
"""
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
T = "MODULE_BONUS"
SNAP = sorted(glob.glob(os.path.join(HERE, "_rollback", "*_" + T.lower())))[-1]
print("基线快照:", os.path.relpath(SNAP, ROOT))
fail = []

with psycopg.connect(DSN) as conn, conn.cursor() as cur:
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='cfg' ORDER BY table_name")
    got = {}
    for t in [r[0] for r in cur.fetchall()]:
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
    if [c["db_column"] for c in d["columns"]] != got[t]:
        drift.append(t)
print(f"1) 全库列漂移表: {len(drift)} {drift}")
if drift:
    fail.append("列漂移")

d = json.load(open(os.path.join(SCHEMA, T + ".json"), encoding="utf-8"))
cols = d["columns"]
width, rmax = len(cols), d["reader_max_csv_index"]
gap_expect = sorted([0] + [5 * k - 2 for k in range(1, 9)] + [5 * k + 1 for k in range(1, 8)])
gap_got = [c["csv_index"] for c in cols if c["status"] == "gap"]

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
    dbcols = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT count(*) FROM (SELECT " + ", ".join(f'"{c}"' for c in dbcols) +
                f' FROM cfg."{T}") q WHERE ' + " OR ".join(f'"{c}" IS NULL' for c in dbcols))
    nnull = cur.fetchone()[0]
print(f"2) {T}: schema {width} 列｜reader_max csv#{rmax}（需 {rmax + 1}）｜库列 {len(dbcols)}｜"
      f"行 {n}｜manifest 段数 {dist}｜NULL 行 {nnull}")
print(f"   缝列（schema）: {gap_got}")
print(f"   缝列（ASM 推）: {gap_expect}")

# 结构断言：csv 号 ↔ 物理位置 ↔ 内存偏移
bad = []
for i, c in enumerate(cols):
    if c["csv_index"] != i or c["db_column"] != dbcols[i]:
        bad.append(f"csv{c['csv_index']} db={c['db_column']} 物理#{i}={dbcols[i]}")
    if c["status"] != "gap" and i >= 2:
        g = (c["csv_index"] + 3) // 5
        slot = {5 * g - 3: 0, 5 * g - 1: 1, 5 * g: 2}[c["csv_index"]]
        exp = 4 + 12 * (g - 1) + 4 * slot
        if c["memory_offset"] != exp:
            bad.append(f"csv{c['csv_index']} {c['db_column']} mem+{c['memory_offset']} != +{exp}")
print(f"3) 结构断言（csv↔物理位置↔内存偏移）: 违例 {len(bad)}")
for b in bad[:8]:
    print("    ✗", b)

checks = [
    (f"列数 41", width == 41 and len(dbcols) == 41),
    (f"reader_max csv#{rmax} == 40", rmax == 40),
    (f"缝列 == ASM 推定（{len(gap_expect)}）", gap_got == gap_expect and d["column_gap"] == len(gap_expect)),
    (f"读列 25", d["column_confirmed"] == 25),
    (f"manifest 行宽 == 41（单值）", dist == [41]),
    ("行数 64", n == 64),
    ("0 NULL", nnull == 0),
    ("结构断言 0 违例", not bad),
]
for name, ok in checks:
    print(f"   {'✓' if ok else '✗'} {name}")
    if not ok:
        fail.append(name)

# 4) 按位置比对原列取值（改名是 RENAME，位置不变）
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
print(f"4) 位置比对原列（改前 {len(hdr)} 列 × {len(old)} 行 = {len(hdr) * len(old)} 格）："
      f"实比 {checked} 格，差异 {diff}")
print(f"   改前列 {hdr}")
print(f"   改后前 {len(hdr)} 列 {cur_cols[:len(hdr)]}；新列区间 {dbcols[len(hdr)]} .. {dbcols[-1]}")
if diff:
    fail.append("原列取值漂移")

with open(os.path.join(SNAP, T + ".manifest.txt"), encoding="utf-8") as fh:
    old_raw = fh.read()
old_rows = [l for l in old_raw.split("\n") if l.strip() and not l.strip().startswith("#")]
print(f"5) manifest 行宽: 改前 {sorted({r.count(',') + 1 for r in old_rows})} → 改后 {dist}；"
      f"字节 {len(old_raw.encode('utf-8'))} → {len(raw.encode('utf-8'))}")

print("\n验收:", "全部通过 ✓" if not fail else f"✗ 未通过 {fail}")
sys.exit(1 if fail else 0)
