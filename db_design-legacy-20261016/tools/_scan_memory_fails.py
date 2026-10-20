#!/usr/bin/env python3
"""List composites/tables failing memory slot audit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"


def main() -> None:
    fails: list[tuple[str, list[str]]] = []
    skipped = passed = 0

    for p in sorted(COMP.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("status") != "complete":
            continue
        mem = (d.get("asm_audit") or {}).get("memory")
        if not mem:
            continue
        st = mem.get("status")
        if st == "pass":
            passed += 1
        elif st == "fail":
            fails.append((d["id"], mem.get("issues", [])))
        else:
            skipped += 1

    print(f"Memory audit: {passed} pass, {len(fails)} fail\n")
    for comp_id, issues in fails:
        print(f"  {comp_id}")
        for i in issues[:6]:
            print(f"    - {i}")
        print()


if __name__ == "__main__":
    main()
