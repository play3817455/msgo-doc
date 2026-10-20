#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema" / "composites"
BATCH3 = [
    "item_list", "party_member_stat", "order", "rankself", "ranking",
    "special_a_next", "sort_info",
]
for ent in BATCH3:
    comp = json.loads((ROOT / f"{ent}.json").read_text(encoding="utf-8"))
    missing = [
        m["name"]
        for m in comp.get("members", [])
        if not any(ws.get("evidence_va") for ws in m.get("wire_sources", []))
    ]
    if missing:
        print(f"{ent}: {missing}")
