# -*- coding: utf-8 -*-
"""给指定的表打印「要补的列」清单（reader 真值 - schema 已有）
用法: python _plan_widen.py PLAY_BONUS_REWARD PLAYER_NAVI BUFF MODULE_DEVELOP MISSION_EXTRULE
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
verdict = json.load(open(os.path.join(HERE, "_out_sweep_verdict.json"), encoding="utf-8"))
emu = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
vt = verdict["by_table"]


def find_reader(table):
    for name, v in emu.items():
        if table in v["tables"]:
            return name, v
    return None, None


for t in sys.argv[1:]:
    d = json.load(open(os.path.join(TABLES, t + ".json"), encoding="utf-8"))
    have = {c["csv_index"]: c for c in d["columns"]}
    name, v = find_reader(t)
    read_kind = {}
    for c in v["calls"]:
        if c["n"] is None:
            continue
        read_kind.setdefault(c["n"], c["kind"])
    offs = {}
    for s in v["stores"]:
        if s["n"] is None or s.get("via") not in ("marker", "conv-marker"):
            continue
        offs.setdefault(s["n"], s["off"])
    maxread = max(read_kind)
    print(f"=== {t} reader={name} 现有列={len(have)} (max csv {max(have)}) | reader 读到 0..{maxread}")
    print(f"    dp={d.get('disposition')} csv={d.get('csv_path')}")
    add = [n for n in range(maxread + 1) if n not in have]
    for n in sorted(have):
        c = have[n]
        print(f"    存 {n:3d} {c.get('db_column'):26s} {c.get('type'):8s} {c.get('status'):10s} off={c.get('memory_offset')}")
    print(f"    -- 需补 {len(add)} 列：")
    for n in add:
        k = read_kind.get(n)
        print(f"    +  {n:3d} kind={k} off={offs.get(n)}")
    print()
