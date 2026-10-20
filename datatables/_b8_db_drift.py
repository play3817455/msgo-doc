# -*- coding: utf-8 -*-
"""全库列漂移体检：schema(csv_index 序) vs PostgreSQL cfg.* 物理列序。

只读，不改库。输出三类：
  EXTRA  库里有、schema 没有（旧名残留 ⇒ 导出列序错位）
  MISS    schema 有、库里没有（sync 会自动 ADD 到末尾）
  REORDER 集合相同但顺序不同（同样错位）
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
SCHEMA_DIR = os.path.join("db_design", "schema", "cfg", "tables")


def load_specs():
    specs = []
    for fn in sorted(os.listdir(SCHEMA_DIR)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(SCHEMA_DIR, fn), encoding="utf-8") as f:
            d = json.load(f)
        if d.get("skip_db"):
            continue
        cols = sorted(d.get("columns", []), key=lambda c: c.get("csv_index", 0))
        # DataColumnNames 含 csv_index 0（行键列）；物理列名权威字段 db_column
        want = [c.get("db_column") or c.get("name") or f"col{c['csv_index']}" for c in cols]
        specs.append((d.get("table") or d.get("id") or fn[:-5], want))
    return specs


def main():
    specs = load_specs()
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        bad = 0
        for table, want in specs:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema='cfg' and table_name=%s and column_name<>'_row_id' "
                "order by ordinal_position",
                (table,),
            )
            got = [r[0] for r in cur.fetchall()]
            if not got:
                print(f"-- {table}: 库中无此表 (schema {len(want)} 列)")
                continue
            extra = [c for c in got if c not in set(want)]
            miss = [c for c in want if c not in set(got)]
            reorder = (not extra and not miss and len(want) == len(got)
                       and any(a != b for a, b in zip(want, got)))
            if not (extra or miss or reorder):
                continue
            bad += 1
            print(f"!! {table}: schema {len(want)} / db {len(got)}")
            if extra:
                print(f"   EXTRA({len(extra)}) {extra}")
            if miss:
                print(f"   MISS({len(miss)}) {miss}")
            if reorder:
                diff = [(i, w, g) for i, (w, g) in enumerate(zip(want, got)) if w != g]
                print(f"   REORDER {len(diff)} 处:")
                for i, w, g in diff:
                    print(f"      [{i}] db={g} -> want={w}")
        print(f"== 漂移表 {bad} / 受检 {len(specs)}")


if __name__ == "__main__":
    main()
