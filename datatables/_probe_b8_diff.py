# -*- coding: utf-8 -*-
"""第 8 批勘查 2：对 READSET-DIFF 的表，把「仿真 observed」与「schema csv_index」并排打印。"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")
emu = json.load(open(os.path.join(HERE, "_out_emu_readers.json"), encoding="utf-8"))
verdict = json.load(open(os.path.join(HERE, "_out_sweep_verdict.json"), encoding="utf-8"))

TARGETS = ["CHARA_MODEL", "CHARA_PARAM", "MSMA_RENTAL", "ACTION_MODULE_INFO", "SCORE_CONFIG_CATEGORY"]

for t in TARGETS:
    d = json.load(open(os.path.join(SCHEMA, t + ".json"), encoding="utf-8"))
    cols = d["columns"]
    print("=" * 100)
    print(f"{t}  reader={d.get('asm_reader')}  cols={len(cols)}  gap={d.get('column_gap')}")
    # find emu entry
    ent = None
    for k, v in emu.items():
        if t in (v.get("tables") or []):
            ent = (k, v)
            break
    if not ent:
        print("  (no emu entry)")
        continue
    sub, v = ent
    obs = set()
    for m in v.get("modes") or []:
        obs |= set(m.get("observed") or [])
    print(f"  emu sub={sub} declared={len(v.get('declared') or [])} observed={sorted(obs)}")
    print(f"  verdict={verdict['by_table'].get(t)}")
    print(f"  {'csv':>4} {'db_column':28s} {'status':10s} {'type':10s}")
    for c in cols:
        mark = ""
        i = c["csv_index"]
        if i not in obs:
            mark = "  ← 仿真未见"
        print(f"  {i:>4} {c['db_column']:28s} {c.get('status',''):10s} {c.get('type',''):10s}{mark}")
    print()
