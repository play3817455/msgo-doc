# -*- coding: utf-8 -*-
"""item.csv 有没有非空图标列（决定 gen_weapon_tables_wiki.py --apply 会不会抹掉图标）。"""
import collections
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DF = os.path.join(ROOT, "server", "datafiles", "lounge", "item")

for fn in ("item.csv", "item.csv.bak_before_weapon_icons"):
    p = os.path.join(DF, fn)
    if not os.path.exists(p):
        print("%s 不存在" % fn)
        continue
    rows = [r for r in csv.reader(open(p, encoding="utf-8", errors="replace")
                                  .read().replace("\r\n", "\n").split("\n"))
            if r and any(x.strip() for x in r)]
    body = [r for r in rows if not r[0].lstrip("\ufeff").startswith("#")]
    nz = collections.Counter()
    for r in body:
        for i in range(5, min(8, len(r))):
            if r[i].strip():
                nz[i] += 1
    print("%-34s 数据 %5d 行；col5/6/7 非空计数 %s" % (fn, len(body), dict(sorted(nz.items()))))
    for r in body:
        if any(r[i].strip() for i in range(5, min(8, len(r)))):
            print("     例: %s" % ",".join(r[:8]))
            break
