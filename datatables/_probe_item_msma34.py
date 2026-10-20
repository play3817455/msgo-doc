# -*- coding: utf-8 -*-
"""#65 ITEM / #34 MSMA_BATTLE_DETAIL 种子 vs 库 差异定性。只读。"""
import os
from collections import Counter

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")

CASES = [
    ("65 ITEM", "item/item.csv", "ITEM", 8),
    ("34 MSMA_BATTLE_DETAIL", "msma/msma_battle_detail.csv", "MSMA_BATTLE_DETAIL", 3),
]


def seed_rows(rel):
    p = os.path.join(LOUNGE, rel)
    if not os.path.exists(p):
        return None, None
    with open(p, "rb") as f:
        raw = f.read()
    lines = [l for l in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
             if l.strip() and not l.lstrip().startswith("#")]
    return lines, os.path.getsize(p)


for label, rel, tbl, ncol in CASES:
    print("=" * 70)
    print("##", label)
    lines, size = seed_rows(rel)
    print("  种子: %s 行, %d 字节, 首行字段数=%d" %
          (len(lines) if lines else "缺", size or 0, len(lines[0].split(",")) if lines else -1))
    if lines:
        print("  首 3 行:")
        for l in lines[:3]:
            print("     %r" % l)
        print("  末 3 行:")
        for l in lines[-3:]:
            print("     %r" % l)
        c = Counter(len(l.split(",")) for l in lines)
        print("  字段数分布:", dict(sorted(c.items())))
        k0 = Counter(l.split(",")[0].strip() for l in lines)
        print("  col0 唯一值 %d ／ %d 行；重复最多的: %s" %
              (len(k0), len(lines), k0.most_common(4)))
    with psycopg.connect(DSN) as c:
        cur = c.cursor()
        cur.execute('select count(*) from cfg."%s"' % tbl)
        n = cur.fetchone()[0]
        cur.execute("""select column_name from information_schema.columns
                       where table_schema='cfg' and table_name=%s and column_name<>'_row_id'
                       order by ordinal_position""", (tbl,))
        cols = [r[0] for r in cur.fetchall()]
        print("  库: %d 行, 列 %s" % (n, cols))
        k = cols[0]
        cur.execute('select count(distinct btrim("%s")) from cfg."%s"' % (k, tbl))
        print("  库 distinct(%s) = %d" % (k, cur.fetchone()[0]))
        cur.execute('select * from cfg."%s" order by _row_id limit 3' % tbl)
        for r in cur.fetchall():
            print("     %r" % (r,))
        cur.execute('select * from cfg."%s" order by _row_id desc limit 3' % tbl)
        for r in cur.fetchall():
            print("     %r" % (r,))
