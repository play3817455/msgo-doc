# -*- coding: utf-8 -*-
"""CHARA_MODEL / CHARA_PARAM 仿真 offset 与 schema 并排对账（临时探针）"""
import io, json, os, sys
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PAIRS = [("sub_571380", "CHARA_MODEL"), ("sub_582390", "CHARA_PARAM")]

d = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
for rk, tn in PAIRS:
    v = d[rk]
    t = json.load(open(os.path.join(ROOT, "db_design", "schema", "cfg", "tables", tn + ".json"), encoding="utf-8"))
    sc = {c.get("csv_index"): c for c in t["columns"]}
    cand = defaultdict(list)
    for s in v["stores"]:
        if s["n"] is None:
            continue
        cand[s["n"]].append((s["off"], s.get("via")))
    print("=" * 100)
    print(tn, rk, " reads=", len(v["observed"]), " stores=", len(v["stores"]), " err=", v["err"])
    print("csv | sim-marker | sim-all | schema-off | status | name")
    keys = sorted(set(list(cand) + [c.get("csv_index") for c in t["columns"]]))
    for n in keys:
        if n is None:
            continue
        hi = [o for o, via in cand.get(n, []) if via in ("marker", "conv-marker")]
        alls = cand.get(n, [])
        c = sc.get(n) or {}
        print("%3d | %-16s | %-20s | %-10s | %-9s | %s" % (
            n, hi, alls, c.get("memory_offset"), c.get("status"), c.get("db_column")))
    print()
