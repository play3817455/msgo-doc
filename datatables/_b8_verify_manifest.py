# -*- coding: utf-8 -*-
"""batch8 验收：改名后的库物理序 == schema 序 == manifest(raw_csv) 列序，且逐格相等。

口径：ExportTableRawCSV 用 DB 物理列序 + _row_id 序拼 raw_csv ⇒
      「manifest 行 i 的第 k 格」必须等于「DB 第 i 行的第 k 列」。
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
TABLES = ["CHARA_MODEL", "MSMA_WEAPONSET", "CHARA_PARAM", "MSMA_RENTAL", "ITEM_PART"]


def schema_names(t):
    d = json.load(open(f"db_design/schema/cfg/tables/{t}.json", encoding="utf-8"))
    cols = sorted(d["columns"], key=lambda c: c["csv_index"])
    return [c.get("db_column") or c.get("name") or f"col{c['csv_index']}" for c in cols]


with psycopg.connect(DSN) as c:
    cur = c.cursor()
    for t in TABLES:
        want = schema_names(t)
        cur.execute(
            "select column_name from information_schema.columns "
            "where table_schema='cfg' and table_name=%s and column_name<>'_row_id' "
            "order by ordinal_position", (t,))
        got = [r[0] for r in cur.fetchall()]
        cur.execute(f'select {", ".join(chr(34)+w+chr(34) for w in want)} from cfg."{t}" order by _row_id')
        rows = [[("" if v is None else v) for v in r] for r in cur.fetchall()]
        cur.execute("select raw_csv from meta.cfg_manifest where file=%s", (t,))
        raw = cur.fetchone()[0].decode("utf-8", "replace")
        ml = [l.rstrip("\r") for l in raw.split("\n")
              if l.strip() and not l.lstrip().startswith("#")]
        print(f"== {t}: schema序==库序 {want == got} / 库行 {len(rows)} / manifest行 {len(ml)}")
        if want != got:
            for i, (a, b) in enumerate(zip(want, got)):
                if a != b:
                    print(f"   !! 序不一致 [{i}] schema={a} db={b}")
            break
        diff = 0
        for i, line in enumerate(ml):
            cells = line.split(",")
            if len(cells) < len(want):
                cells = cells + [""] * (len(want) - len(cells))
            if i >= len(rows):
                diff += 1
                continue
            for k in range(len(want)):
                if (cells[k] or "").strip() != (str(rows[i][k]) or "").strip():
                    diff += 1
                    if diff <= 3:
                        print(f"   !! 行{i} 列{want[k]}: manifest={cells[k]!r} db={rows[i][k]!r}")
                    break
        print(f"   逐格差异行 {diff}")
