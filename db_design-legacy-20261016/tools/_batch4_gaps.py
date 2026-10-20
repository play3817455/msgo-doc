#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema" / "composites"
BATCH4 = [
    "ext_subrule", "xwar_ext_rule", "extrarule_xwar_info", "wbonus",
    "eq_bonus_modules_lot", "buffitem", "buffitem_ex", "config", "progress", "bgm_desc",
]
for ent in BATCH4:
    p = ROOT / f"{ent}.json"
    if not p.exists():
        continue
    comp = json.loads(p.read_text(encoding="utf-8"))
    missing = [
        m["name"]
        for m in comp.get("members", [])
        if not any(ws.get("evidence_va") for ws in m.get("wire_sources", []))
    ]
    bad = [
        m["name"]
        for m in comp.get("members", [])
        if any(ws.get("evidence_va") and not str(ws.get("evidence_va")).lower().startswith("0x") for ws in m.get("wire_sources", []))
    ]
    if missing:
        print(f"{ent}: missing {missing}")
    if bad:
        print(f"{ent}: non-hex VA {bad}")
