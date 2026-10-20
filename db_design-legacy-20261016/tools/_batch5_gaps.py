#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema" / "composites"
BATCH5 = [
    "phase_info", "bracket_info", "block_detail", "buildup_info", "challenge_info",
    "trchallenge_info", "check_quest", "wave_res", "appear_info", "avatar",
]
for ent in BATCH5:
    p = ROOT / f"{ent}.json"
    if not p.exists():
        continue
    comp = json.loads(p.read_text(encoding="utf-8"))
    missing = [
        m["name"]
        for m in comp.get("members", [])
        if not any(ws.get("evidence_va") for ws in m.get("wire_sources", []))
    ]
    no_reader_hex = [
        m["name"]
        for m in comp.get("members", [])
        if m.get("wire_sources")
        and not any(
            str(ws.get("evidence_va", "")).lower().startswith("0x")
            for ws in m["wire_sources"]
            if ws.get("reader") == comp.get("reader")
        )
    ]
    if missing:
        print(f"{ent}: missing {missing}")
    if no_reader_hex:
        print(f"{ent}: no 0x reader VA {no_reader_hex}")
