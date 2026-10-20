# -*- coding: utf-8 -*-
"""MSMA_WEAPONSET 修正：schema 的物理列名权威字段是 `db_column`（缺失才回落 name）。

csv1/csv3 是 CSV 无表头的 gap 列 ⇒ Go DataColumnNames 自动命名 col1/col3，
所以物理列名就该叫 col1/col3（name=reserved_u32_1 只是人读别名）。

误改名留下的两列（reserved_u32_1 / reserved_u32_3）持有真实数据，需改回；
cfgsync 随后 ADD 出来的空列 col1/col3 追加在末尾，需删除（确认全 NULL 后）。
"""
import io
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

DSN = "postgresql://postgres:admin123@127.0.0.1:5432/msgo"
T = "MSMA_WEAPONSET"


def cols(cur):
    cur.execute(
        "select column_name from information_schema.columns "
        "where table_schema='cfg' and table_name=%s order by ordinal_position",
        (T,),
    )
    return [r[0] for r in cur.fetchall()]


with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    print("before:", cols(cur))
    cur.execute(f'select count(*) filter (where coalesce("col1",\'\')<>\'\'), '
                f'count(*) filter (where coalesce("col3",\'\')<>\'\') from cfg."{T}"')
    n1, n3 = cur.fetchone()
    print(f"末尾新增列 col1/col3 非空计数 = {n1}/{n3}")
    if n1 or n3:
        print("!! 末尾列有数据，停止（不删数据）")
        sys.exit(1)
    cur.execute(f'select count(*) filter (where coalesce("reserved_u32_1",\'\')<>\'\'), '
                f'count(*) filter (where coalesce("reserved_u32_3",\'\')<>\'\') from cfg."{T}"')
    print(f"原位列 reserved_u32_1/reserved_u32_3 非空计数 = {cur.fetchone()}")
    with conn.transaction():
        cur.execute(f'ALTER TABLE cfg."{T}" DROP COLUMN "col1"')
        cur.execute(f'ALTER TABLE cfg."{T}" DROP COLUMN "col3"')
        cur.execute(f'ALTER TABLE cfg."{T}" RENAME COLUMN "reserved_u32_1" TO "col1"')
        cur.execute(f'ALTER TABLE cfg."{T}" RENAME COLUMN "reserved_u32_3" TO "col3"')
    print("after :", cols(cur))
