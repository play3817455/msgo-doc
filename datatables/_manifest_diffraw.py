# -*- coding: utf-8 -*-
"""对比快照(旧) 与当前库(新) 的 manifest raw_csv，定位差异性质。"""
import io
import os
import pickle
import sys

import psycopg

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
old = pickle.load(open(os.path.join(HERE, "_out_manifest_snapshot.pkl"), "rb"))
DSN = os.environ.get("MSGO_DSN", "postgresql://postgres:admin123@127.0.0.1:5432/msgo")
tables = sys.argv[1:] or ["BYWORD", "BUFF", "PLAY_BONUS_REWARD", "MISSION_GROUP"]
q = "SELECT file, raw_csv FROM meta.cfg_manifest WHERE file = ANY(%s)"
with psycopg.connect(DSN) as c, c.cursor() as cur:
    cur.execute(q, (tables,))
    new = dict(cur.fetchall())

for t in tables:
    o = (old[t][3] or b"").decode("utf-8")
    n = (new[t] or b"").decode("utf-8")
    print(f"### {t}  OLD {len(o)}B / NEW {len(n)}B")
    ol = [x for x in o.split("\n")]
    nl = [x for x in n.split("\n")]
    print("  OLD 前 6 行:")
    for l in ol[:6]:
        print("     ", repr(l[:170]))
    print("  NEW 前 6 行:")
    for l in nl[:6]:
        print("     ", repr(l[:170]))
    print("  行数 OLD/NEW:", len(ol), len(nl))
    print()
