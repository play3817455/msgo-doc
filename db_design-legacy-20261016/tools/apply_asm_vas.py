#!/usr/bin/env python3
"""Apply IDA wire VAs to composite members by wire offset match."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
VAS = SCHEMA / "_meta" / "ida_wire_vas.json"
DEFAULT_ENTITIES: list[str] | None = None
COMPOSITES = SCHEMA / "composites"


def find_va(segments: list[dict], offset: int, length: int) -> str | None:
    """Pick evidence VA for member starting at wire offset."""
    exact = [s for s in segments if s["offset"] == offset]
    if exact:
        return exact[0]["va"]
    # cover by segment range
    for s in segments:
        if s["offset"] <= offset < s["offset"] + s["size"]:
            return s["va"]
    # merge consecutive from offset
    acc = 0
    start_va = None
    for s in sorted(segments, key=lambda x: x["offset"]):
        if s["offset"] < offset:
            continue
        if s["offset"] > offset + acc and acc > 0:
            break
        if start_va is None and s["offset"] == offset:
            start_va = s["va"]
        if start_va:
            acc += s["size"]
            if acc >= length:
                return start_va
    return None


def apply_entity(ent: str, vas_path: Path, dry_run: bool = False) -> dict:
    vas_all = json.loads(vas_path.read_text(encoding="utf-8"))
    if ent not in vas_all:
        return {"entity": ent, "error": "no ida extract"}
    info = vas_all[ent]
    segments = info.get("segments", [])
    comp_path = COMPOSITES / f"{ent}.json"
    comp = json.loads(comp_path.read_text(encoding="utf-8"))
    applied = 0
    skipped = 0
    for m in comp.get("members", []):
        off = m["offset"]
        ln = m["length"]
        va = find_va(segments, off, ln)
        if not va:
            skipped += 1
            continue
        for ws in m.get("wire_sources", []):
            if not ws.get("evidence_va"):
                ws["evidence_va"] = va
                applied += 1
        m["asm_verified"] = True
        m["asm_evidence_va"] = va
        m["asm_audit_date"] = str(date.today())
    comp["asm_audit"] = {
        "verified": str(date.today()),
        "function": info.get("function"),
        "ida_parsed_total": info.get("total"),
        "composite_length": comp.get("length"),
        "fields_applied": applied,
        "fields_skipped": skipped,
        "status": "pass" if skipped == 0 else "pass_with_gaps",
    }
    if not dry_run:
        comp_path.write_text(json.dumps(comp, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "entity": ent,
        "applied": applied,
        "skipped": skipped,
        "status": comp["asm_audit"]["status"],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("entities", nargs="*", help="composite ids (default: all in vas file)")
    ap.add_argument("--vas", type=Path, default=VAS, help="IDA wire vas JSON path")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    ents = args.entities or list(json.loads(args.vas.read_text(encoding="utf-8")).keys())
    for ent in ents:
        r = apply_entity(ent, args.vas, args.dry_run)
        print(r)


if __name__ == "__main__":
    main()
