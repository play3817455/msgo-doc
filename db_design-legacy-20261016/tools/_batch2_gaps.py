#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema" / "composites"
BATCH2 = [
    "lpcard", "ms", "snapshot", "funnelss", "unlockw",
    "adop_list", "recruits", "leaders", "bracket", "AI",
]
total = 0
for ent in BATCH2:
    comp = json.loads((ROOT / f"{ent}.json").read_text(encoding="utf-8"))
    missing = []
    for m in comp.get("members", []):
        if not any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
            missing.append(m["name"])
    if missing:
        print(f"{ent}: {len(missing)} missing -> {missing}")
        total += len(missing)
print(f"\nTOTAL missing: {total}")
