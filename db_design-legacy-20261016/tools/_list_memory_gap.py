#!/usr/bin/env python3
import json
from pathlib import Path

COMP = Path(__file__).resolve().parents[1] / "schema" / "composites"


def members_of(d: dict) -> list:
    m = d.get("members", [])
    if not m and d.get("layout_same_as"):
        src = COMP / f"{d['layout_same_as']}.json"
        if src.exists():
            m = json.loads(src.read_text(encoding="utf-8")).get("members", [])
    return m


def main() -> None:
    need = []
    for p in sorted(COMP.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("status") != "complete":
            continue
        claim, length = d.get("memory_claim"), d.get("length")
        if claim is None or length is None or claim == length:
            continue
        mems = members_of(d)
        tagged = sum(1 for m in mems if m.get("memory_offset") is not None or m.get("memory_only"))
        if tagged < len(mems):
            need.append((d["id"], length, claim, len(mems), tagged, d.get("reader"), d.get("printer")))
    print(f"need memory_offset: {len(need)}")
    for row in need:
        print(
            f"  {row[0]:24} wire={row[1]:5} mem={row[2]:5} "
            f"members={row[3]:2} tagged={row[4]:2} reader={row[5]}"
        )


if __name__ == "__main__":
    main()
