# -*- coding: utf-8 -*-
"""看 CHARA_MODEL 源 CSV 各列非空率 + 库里非空率对照"""
import csv
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
spec = json.load(open("db_design/schema/cfg/tables/CHARA_MODEL.json", encoding="utf-8"))
csv_path = spec.get("csv_path")
print("csv_path =", csv_path)


def find(p):
    for root in ("unpacked", "tools", "datatables", "."):
        cand = os.path.join(root, p.replace("/", os.sep))
        if os.path.isfile(cand):
            return cand
        base = os.path.basename(p)
        for dp, _, fns in os.walk(root):
            for f in fns:
                if f.lower() == base.lower():
                    return os.path.join(dp, f)
    return None


path = find(csv_path) if csv_path else None
print("found =", path)
if not path:
    sys.exit(1)

with open(path, "r", encoding="utf-8", errors="replace") as f:
    lines = [l.rstrip("\r\n") for l in f if l.strip() and not l.lstrip().startswith("#")]
rows = [next(csv.reader(io.StringIO(l), skipinitialspace=True)) for l in lines]
ncols = max(len(r) for r in rows)
nonempty = [0] * ncols
for r in rows:
    for i, v in enumerate(r):
        if i < ncols and v.strip():
            nonempty[i] += 1
print("rows =", len(rows), "maxcols =", ncols)
with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for i, col in enumerate(sorted(spec["columns"], key=lambda x: x["csv_index"])):
        if i > 77:
            break
        cur.execute(
            f'select count(*) filter (where coalesce("{col["name"]}",\'\')<>\'\') from cfg."CHARA_MODEL"'
        )
        dbn = cur.fetchone()[0]
        if i in range(16, 32) or i in (0, 1, 2, 44, 46, 53, 54, 58, 59, 60, 62, 71, 72, 73, 74, 75, 76):
            print(f"  [{i:2d}] {col['name']:<18} csv非空 {nonempty[i] if i<ncols else 0:>5} / db非空 {dbn:>5}")
