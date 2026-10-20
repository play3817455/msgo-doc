# -*- coding: utf-8 -*-
"""cfg.* 物理列**原位对齐**：把库里旧列名改名为 schema(csv_index 序) 的名字。

为什么必须原位改名：`ExportTableRawCSV` 按 information_schema 物理顺序取列，
而 `ensureDataTable` 只会 ADD COLUMN（新名追加到末尾）⇒ 一次改名会在库里
留下「旧名(有数据) + 新名(追加空列)」两份，导出给客户端的 CSV 列序全错。

两步重命名（相位一全员挪到临时名，相位二落目标名）可安全处理**改名链**
（如 csv53 reserved→lod_distance 同时 csv54 lod_distance→flag_lod_54）。

数值不动：值跟着列序号走，csv K 列的值永远留在物理第 K 列。

用法：
  python datatables/_b8_db_align.py            # dry-run，只打印将要执行的 SQL
  python datatables/_b8_db_align.py --apply    # 执行（写库）
"""
import io
import json
import os
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
SCHEMA_DIR = os.path.join("db_design", "schema", "cfg", "tables")
TEMP_PREFIX = "__aln_"


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
        # 物理列名权威字段是 db_column（缺失才回落 name）——与 Go DataColumnNames 一致
        want = [c.get("db_column") or c.get("name") or f"col{c['csv_index']}" for c in cols]
        specs.append((d.get("id") or d.get("table") or fn[:-5], want))
    return specs


def db_cols(cur, table):
    cur.execute(
        "select column_name from information_schema.columns "
        "where table_schema='cfg' and table_name=%s and column_name<>'_row_id' "
        "order by ordinal_position",
        (table,),
    )
    return [r[0] for r in cur.fetchall()]


def plan(table, want, got):
    """返回 (sql 列表, 备注列表)。仅当列数一致且集合可改名闭合时才规划。"""
    sql, notes = [], []
    if len(got) > len(want):
        notes.append(f"跳过 {table}: 库列 {len(got)} > schema {len(want)}，多余列无法安全归位（不删数据）")
        return sql, notes
    q = lambda i: psycopg.sql.Identifier(i).as_string(None)
    mism = [i for i in range(len(got)) if got[i] != want[i]]
    if mism:
        # 相位一：错位列全部挪到临时名（腾空所有目标名，改名链安全）
        for i in mism:
            sql.append(f'ALTER TABLE cfg."{table}" RENAME COLUMN {q(got[i])} TO {q(f"{TEMP_PREFIX}{i}")};')
        # 相位二：临时名落目标名
        for i in mism:
            sql.append(f'ALTER TABLE cfg."{table}" RENAME COLUMN {q(f"{TEMP_PREFIX}{i}")} TO {q(want[i])};')
        notes.append(f"{table}: 原位改名 {len(mism)} 列（含改名链）")
    for i in range(len(got), len(want)):
        sql.append(f'ALTER TABLE cfg."{table}" ADD COLUMN IF NOT EXISTS {q(want[i])} TEXT;')
        notes.append(f"{table}: 追加缺失列 [{i}] {want[i]}")
    return sql, notes


def inverse_sql(table, want, got):
    """生成回滚 SQL：把对齐后的名字改回对齐前（同样两步法）。"""
    q = lambda i: psycopg.sql.Identifier(i).as_string(None)
    mism = [i for i in range(min(len(got), len(want))) if got[i] != want[i]]
    if not mism:
        return []
    out = [f'ALTER TABLE cfg."{table}" RENAME COLUMN {q(want[i])} TO {q(f"{TEMP_PREFIX}rb{i}")};'
           for i in mism]
    out += [f'ALTER TABLE cfg."{table}" RENAME COLUMN {q(f"{TEMP_PREFIX}rb{i}")} TO {q(got[i])};'
            for i in mism]
    return out


def main():
    apply = "--apply" in sys.argv
    specs = load_specs()
    all_sql, all_notes, rollback = [], [], []
    with psycopg.connect(DSN) as conn:
        cur = conn.cursor()
        for table, want in specs:
            got = db_cols(cur, table)
            if not got:
                continue
            sql, notes = plan(table, want, got)
            all_sql += sql
            all_notes += notes
            if sql and len(got) == len(want):
                rollback += inverse_sql(table, want, got)
        for n in all_notes:
            print("  ", n)
        print(f"== 计划 SQL {len(all_sql)} 条")
        for s in all_sql:
            print(s)
        if rollback:
            import datetime
            d = os.path.join("datatables", "_rollback")
            os.makedirs(d, exist_ok=True)
            stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            path = os.path.join(d, f"batch8_db_rename_{stamp}_rollback.sql")
            with open(path, "w", encoding="utf-8") as f:
                f.write("-- cfg.* 物理列原位改名回滚（batch8）\n" + "\n".join(rollback) + "\n")
            print(f"== 回滚脚本 {path}")
        if not apply:
            print("(dry-run；加 --apply 执行)")
            return
        if not all_sql:
            print("(无需执行)")
            return
        with conn.transaction():
            for s in all_sql:
                cur.execute(s)
        print(f"== 已执行 {len(all_sql)} 条 DDL")
        # 复核
        bad = 0
        for table, want in specs:
            got = db_cols(cur, table)
            if got and got != want:
                bad += 1
                print(f"!! 仍不对齐 {table}: {len(got)}/{len(want)}")
        print(f"== 复核：不对齐 {bad} 张")


if __name__ == "__main__":
    main()
