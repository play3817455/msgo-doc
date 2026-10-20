# -*- coding: utf-8 -*-
"""全表体检扫描：schema 声明列 vs 库列、行数三方（种子/库/manifest）。只读。"""
import json
import os
import sys

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCHEMA_DIR = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")

SKIP_COLS = {"_row_id", "_seq"}


def data_rows(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        raw = f.read()
    n = 0
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if ln.strip() and not ln.lstrip().startswith("#"):
            n += 1
    return n


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    cur.execute("""select table_name, string_agg(column_name, E'\\x01' order by ordinal_position)
                   from information_schema.columns where table_schema='cfg'
                   group by table_name""")
    dbcols = {t: [x for x in cs.split("\x01") if x not in SKIP_COLS] for t, cs in cur.fetchall()}
    cur.execute("""select table_name from information_schema.tables where table_schema='cfg'""")
    dbtables = {r[0] for r in cur.fetchall()}
    cur.execute("select file, row_count from meta.cfg_manifest")
    man = dict(cur.fetchall())
    counts = {}
    for t in dbcols:
        if t not in dbtables:
            continue
        try:
            cur.execute('select count(*) from cfg."%s"' % t)
            counts[t] = cur.fetchone()[0]
        except Exception as e:
            counts[t] = "ERR:%s" % e

drift, missing, seeddiff, rowdiff = [], [], [], []
for fn in sorted(os.listdir(SCHEMA_DIR)):
    if not fn.endswith(".json"):
        continue
    spec = json.load(open(os.path.join(SCHEMA_DIR, fn), encoding="utf-8"))
    tid = spec["id"]
    scols = [c["db_column"] for c in spec.get("columns", [])]
    if tid not in dbcols:
        missing.append(tid)
        continue
    dcols = dbcols[tid]
    if scols != dcols:
        drift.append((spec.get("table_id"), tid, scols, dcols))
    seed = os.path.join(ROOT, "server", "datafiles", "lounge", spec.get("csv_path", ""))
    sn = data_rows(seed)
    dn = counts.get(tid)
    mn = man.get(tid)
    if sn is not None and isinstance(dn, int) and sn != dn:
        seeddiff.append((spec.get("table_id"), tid, "种子%d/库%d" % (sn, dn)))
    if isinstance(mn, int) and isinstance(dn, int) and mn != dn:
        rowdiff.append((spec.get("table_id"), tid, "manifest%d/库%d" % (mn, dn)))
    if sn is None:
        seeddiff.append((spec.get("table_id"), tid, "种子文件缺失"))

print("== schema 表 %d ／ 库表 %d ==" % (len(os.listdir(SCHEMA_DIR)), len(dbcols)))
print()
print("== A. 列漂移（schema vs 库）%d ==" % len(drift))
for a, b, s, d in drift:
    print("  #%s %s" % (a, b))
    print("     schema: %s" % s)
    print("     库    : %s" % d)
print()
print("== B. 库缺表 %d ==" % len(missing))
for m in missing:
    print("  %s" % m)
print()
print("== C. 种子 vs 库 行数不符 %d ==" % len(seeddiff))
for a, b, s in seeddiff:
    print("  #%s %s  %s" % (a, b, s))
print()
print("== D. manifest vs 库 行数不符 %d ==" % len(rowdiff))
for a, b, s in rowdiff:
    print("  #%s %s  %s" % (a, b, s))
