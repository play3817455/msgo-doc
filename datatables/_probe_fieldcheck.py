# -*- coding: utf-8 -*-
"""逐字段核对：种子首行 vs 库首行（按 csv_index）。-> datatables/_out_fieldcheck.txt"""
import io
import os

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
OUT = os.path.join(HERE, "_out_fieldcheck.txt")

CASES = [
    ("#65 ITEM", "item/item.csv", "ITEM"),
    ("#34 MSMA_BATTLE_DETAIL", "msma/msma_battle_detail.csv", "MSMA_BATTLE_DETAIL"),
]

rep = io.StringIO()
for label, rel, tbl in CASES:
    rep.write("=" * 80 + "\n## %s\n" % label)
    p = os.path.join(LOUNGE, rel)
    with open(p, "rb") as f:
        raw = f.read()
    rep.write("文件 %s  %d 字节  BOM=%s  行尾 CRLF=%s\n"
              % (rel, len(raw), raw[:3] == b"\xef\xbb\xbf", b"\r\n" in raw))
    data = [l for l in raw.decode("utf-8", "replace").split("\r\n")
            if l.strip() and not l.startswith("#")]
    rep.write("数据行 %d\n" % len(data))
    for i in range(3):
        fields = data[i].split(",")
        rep.write("  种子行%d 字段数=%d:\n" % (i, len(fields)))
        for j, f in enumerate(fields):
            rep.write("      csv%-2d %r\n" % (j, f))
    with psycopg.connect(DSN, autocommit=True) as c:
        cur = c.cursor()
        cur.execute("""select column_name from information_schema.columns
                       where table_schema='cfg' and table_name=%s and column_name<>'_row_id'
                       order by ordinal_position""", (tbl,))
        cols = [r[0] for r in cur.fetchall()]
        cur.execute('select %s from cfg."%s" order by _row_id limit 3'
                    % (", ".join('"%s"' % x for x in cols), tbl))
        for i, r in enumerate(cur.fetchall()):
            rep.write("  库行%d:\n" % i)
            for j, (cn, v) in enumerate(zip(cols, r)):
                rep.write("      csv%-2d %-16s %r\n" % (j, cn, v))
    rep.write("\n")

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print("wrote", OUT)
