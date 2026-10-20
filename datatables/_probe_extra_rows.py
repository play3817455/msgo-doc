# -*- coding: utf-8 -*-
"""#65 ITEM / #34 MSMA_BATTLE_DETAIL：库比种子多出来的行是什么？-> datatables/_out_extra_rows.txt"""
import io
import os
from collections import Counter

import psycopg

DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOUNGE = os.path.join(ROOT, "server", "datafiles", "lounge")
OUT = os.path.join(HERE, "_out_extra_rows.txt")

CASES = [
    ("#65 ITEM", "item/item.csv", "ITEM"),
    ("#34 MSMA_BATTLE_DETAIL", "msma/msma_battle_detail.csv", "MSMA_BATTLE_DETAIL"),
]

rep = io.StringIO()
for label, rel, tbl in CASES:
    rep.write("=" * 90 + "\n## %s\n" % label)
    seedkeys = []
    with open(os.path.join(LOUNGE, rel), "rb") as f:
        raw = f.read()
    for ln in raw.decode("utf-8", "replace").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        p = ln.split(",")
        seedkeys.append(tuple(x.strip() for x in p[:3]))
    seedset = set(seedkeys)

    with psycopg.connect(DSN, autocommit=True) as c:
        cur = c.cursor()
        cur.execute("""select column_name from information_schema.columns
                       where table_schema='cfg' and table_name=%s and column_name<>'_row_id'
                       order by ordinal_position""", (tbl,))
        cols = [r[0] for r in cur.fetchall()]
        cur.execute('select %s from cfg."%s" order by _row_id'
                    % (", ".join('btrim("%s")' % x for x in cols), tbl))
        dbrows = [tuple("" if v is None else v for v in r) for r in cur.fetchall()]

    dbkeys = [r[:3] for r in dbrows]
    onlydb = [r for r in dbrows if r[:3] not in seedset]
    onlyseed = [k for k in seedkeys if k not in set(dbkeys)]
    rep.write("种子行 %d ／ 库行 %d ／ 库键唯一 %d ／ 只在库 %d ／ 只在种子 %d\n"
              % (len(seedkeys), len(dbrows), len(set(dbkeys)), len(onlydb), len(onlyseed)))
    rep.write("列：%s\n" % cols)
    if onlyseed:
        rep.write("只在种子的键（前 20）：%s\n" % (onlyseed[:20],))
    rep.write("\n只在库前 25 行：\n")
    for r in onlydb[:25]:
        rep.write("   %s\n" % (r,))
    rep.write("只在库后 10 行：\n")
    for r in onlydb[-10:]:
        rep.write("   %s\n" % (r,))
    rep.write("\n只在库 col0 形态（长度/前缀）：%s\n"
              % dict(Counter((len(r[0]), r[0][:2]) for r in onlydb)))
    rep.write("\n库中 col0 相同但整行不同的重复：%s\n"
              % dict(Counter(k for k in dbkeys if dbkeys.count(k) > 1).most_common(6)))
    rep.write("\n")

open(OUT, "w", encoding="utf-8").write(rep.getvalue())
print("wrote", OUT)
