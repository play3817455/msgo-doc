# -*- coding: utf-8 -*-
"""只读：把 10 条畸形 csv 行的**原始文本**连同切列结果打出来，判"逗号在哪"。"""
import csv
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = json.load(io.open(os.path.join(ROOT, "schema", "commands", "index.json"), encoding="utf-8"))
PROTO = os.path.join(os.path.dirname(ROOT), "protocol_analysis", "commands")

for e in IDX["fields_needing_review"]:
    cid, line = e["command"], e["csv_line"]
    p = os.path.join(PROTO, cid, "fields.csv")
    raw = io.open(p, encoding="utf-8-sig").read().splitlines()
    text = raw[line - 1] if 0 < line <= len(raw) else "<缺行>"
    cols = next(csv.reader([text]))
    print("=" * 110)
    print("%s  seq=%s name=%s  (file line %d)" % (cid, e["seq"], e["name"], line))
    print("  原文: %s" % text)
    print("  切列 %d 个:" % len(cols))
    for n, c in enumerate(cols, 1):
        print("     %2d | %s" % (n, c))
