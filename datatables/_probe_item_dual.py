# -*- coding: utf-8 -*-
"""ITEM：7 位短号与 8 位补零号是否**同时存在**（同号双形）？-> datatables/_out_item_dual.txt"""
import io
import os
from collections import defaultdict

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out_item_dual.txt")


def norm(k):
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute('select btrim(item_id), btrim(name), btrim(item_type) from cfg."ITEM"')
    rows = [(k, n, t) for k, n, t in cur.fetchall()]

by_norm = defaultdict(list)
for k, n, t in rows:
    by_norm[norm(k)].append((k, n, t))

dual = {k: v for k, v in by_norm.items() if len(v) > 1}

rep = io.StringIO()
rep.write("库行 %d ／ 归一化键 %d ／ **同号多行** %d\n\n" % (len(rows), len(by_norm), len(dual)))
rep.write("== 同号多行样例（前 25）==\n")
for k in sorted(dual)[:25]:
    rep.write("  %s\n" % k)
    for kk, n, t in dual[k]:
        rep.write("     %-10s %-14s %s\n" % (kk, t, n))

cur_ids = ["1010101", "01010101", "1010401", "01010401", "10840101", "2840151", "02840151"]
rep.write("\n== 指定号 ==\n")
for k in cur_ids:
    hits = [r for r in rows if r[0] == k]
    rep.write("  %-10s %s\n" % (k, hits if hits else "（无此行）"))

rep.write("\n== 同号多行里 item_type 组合分布 ==\n")
from collections import Counter
rep.write("  %s\n" % dict(Counter(tuple(sorted(x[2] for x in v)) for v in dual.values())))

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print("wrote", OUT)
