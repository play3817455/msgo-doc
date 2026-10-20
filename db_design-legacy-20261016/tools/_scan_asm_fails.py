#!/usr/bin/env python3
"""Scan all table/composite asm_audit failures."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
QUEUE = ROOT / "schema" / "_meta" / "asm_audit_queue.json"


def main() -> None:
    seen: set[str] = set()
    fails: list[tuple[str, str, list[str]]] = []

    for p in sorted(TABLES.glob("tbl_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        audit = d.get("asm_audit", {})
        if audit.get("status") != "fail":
            continue
        ent = d.get("asm_audit", {}).get("composite_ref") or p.stem.removeprefix("tbl_")
        comp = json.loads((COMP / f"{ent}.json").read_text(encoding="utf-8"))
        issues = comp.get("asm_audit", {}).get("issues", [])
        fails.append((p.stem, ent, issues))
        seen.add(ent)

    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    print(f"Total failing tables: {len(fails)}\n")
    by_batch: dict[int, list] = {}
    for b in q["batches"]:
        for t in b.get("tables", []):
            for tbl, ent, issues in fails:
                if tbl == t:
                    by_batch.setdefault(b["id"], []).append((tbl, ent, issues))

    for bid in sorted(by_batch):
        print(f"=== Batch #{bid} ({len(by_batch[bid])} fail) ===")
        for tbl, ent, issues in by_batch[bid]:
            print(f"  {tbl} ({ent})")
            for i in issues[:6]:
                print(f"    - {i}")
            if len(issues) > 6:
                print(f"    ... +{len(issues)-6} more")
        print()


if __name__ == "__main__":
    main()
