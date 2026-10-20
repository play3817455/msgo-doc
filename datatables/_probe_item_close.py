# -*- coding: utf-8 -*-
"""ITEM 收口核对：物品ID全集 vs 库；可达武器号域 vs 库 -> datatables/_out_item_close.txt"""
import io
import os
from collections import Counter

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out_item_close.txt")


def rows(name):
    p = os.path.join(HERE, "names", name)
    raw = open(p, "rb").read()
    return [l for l in raw.decode("utf-8-sig").replace("\r\n", "\n").split("\n")
            if l.strip() and not l.lstrip().startswith("#")]


def norm(k):
    k = k.strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


uni = {r.split(",")[0].strip() for r in rows("物品ID全集.csv")}
dom = {r.split(",")[0].strip() for r in rows("可达武器号域.csv")}

with psycopg.connect(DSN, autocommit=True) as c:
    cur = c.cursor()
    cur.execute('select btrim(item_id), btrim(name), btrim(item_type) from cfg."ITEM"')
    db = {k: (n, t) for k, n, t in cur.fetchall()}

rep = io.StringIO()
rep.write("物品ID全集 %d ／ 可达武器号域 %d ／ 库 ITEM %d\n" % (len(uni), len(dom), len(db)))
miss = sorted(uni - set(db))
rep.write("\n== 全集有、库没有 %d ==\n" % len(miss))
for k in miss:
    rep.write("   %s\n" % k)
rep.write("\n== 库有、全集没有 %d ==\n" % len(set(db) - uni))
for k in sorted(set(db) - uni)[:40]:
    rep.write("   %s  %s\n" % (k, db[k]))
rep.write("\n== 可达武器号域 ⊆ 库（按 norm）: %s ==\n"
          % (all(norm(k) in {norm(x) for x in db} for k in dom),))
dbn = {norm(k) for k in db}
rep.write("   域归一 %d ／ 库归一 %d ／ 交 %d\n" % (len({norm(k) for k in dom}), len(dbn),
                                              len({norm(k) for k in dom} & dbn)))
rep.write("   库归一后 item_type 分布: %s\n"
          % dict(Counter(db[k][1] for k in db)))
rep.write("\n== 库 item_id 长度 × item_type ==\n")
cc = Counter((len(k), db[k][1]) for k in db)
for k in sorted(cc):
    rep.write("   %s %s: %d\n" % (k[0], k[1], cc[k]))

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print("wrote", OUT)
