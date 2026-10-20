#!/usr/bin/env python3
"""Patch batch-8 ASM audit reader paths from IDA wire VAs."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
IDA_JSON = ROOT / "schema" / "_meta" / "ida_wire_vas_batch8.json"
TODAY = str(date.today())

sys.path.insert(0, str(ROOT / "tools"))
from apply_asm_vas import find_va  # noqa: E402

MEMBER_COMPS = ["replay_info", "season_rb_conf", "precord"]

TABLE_MAP = {
    "replay_info": "tbl_replay_info",
    "season_rb_conf": "tbl_season_rb_conf",
    "precord": "tbl_precord",
}


def norm_va(va: str | None) -> str | None:
    if not va:
        return None
    if va.startswith("0x") or va.startswith("0X"):
        return "0x" + va[2:].upper()
    return va


def merge_reader_va(existing: str, reader_va: str) -> str:
    if "|" in existing:
        parts = existing.split("|")
        if len(parts) >= 3:
            return f"{reader_va}|{parts[1]}|{parts[2]}"
        return f"{reader_va}|{parts[-1]}"
    if re.match(r"^[0-9A-Fa-f]{5,6}$", existing):
        return f"{reader_va}|{existing}"
    return reader_va


def build_va_map(comp_id: str, ida: dict) -> dict[str, str]:
    segs = ida[comp_id]["segments"]
    comp = json.loads((COMP / f"{comp_id}.json").read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for m in comp.get("members", []):
        va = norm_va(find_va(segs, m["offset"], m["length"]))
        if va:
            out[m["name"]] = va
    return out


def patch_reader_paths(comp_id: str, va_map: dict[str, str]) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rw_fn = data.get("reader") or data.get("writer")
    n = 0
    for m in data.get("members", []):
        va = va_map.get(m["name"])
        if not va:
            continue
        for ws in m.get("wire_sources", []):
            fn = ws.get("reader") or ws.get("writer")
            if rw_fn and fn and fn != rw_fn:
                continue
            cur = str(ws.get("evidence_va", ""))
            if cur.lower().startswith("0x") and "|" in cur:
                continue
            ws["evidence_va"] = merge_reader_va(cur, va) if cur else va
            n += 1
        m["asm_verified"] = True
        m["asm_evidence_va"] = va
        m["asm_audit_date"] = TODAY

    missing = [
        x["name"]
        for x in data.get("members", [])
        if not any(ws.get("evidence_va") for ws in x.get("wire_sources", []))
    ]
    ida_info = json.loads(IDA_JSON.read_text(encoding="utf-8")).get(comp_id, {})
    data["asm_audit"] = {
        "verified": TODAY,
        "function": rw_fn,
        "composite_length": data.get("length"),
        "ida_parsed_total": ida_info.get("total"),
        "fields_missing_va": len(missing),
        "status": "pass" if not missing else "pass_with_gaps",
        "note": "reader paths patched via _patch_asm_batch8.py",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        print(f"  {comp_id}: still missing {missing}")
    return n


def patch_table(tbl_id: str, comp_id: str) -> None:
    path = TABLES / f"{tbl_id}.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    comp = json.loads((COMP / f"{comp_id}.json").read_text(encoding="utf-8"))
    audit = comp.get("asm_audit", {})
    comp_names = {m["name"]: m for m in comp.get("members", [])}
    for col in data.get("columns", []):
        if col.get("composite_ref"):
            col["asm_verified"] = audit.get("status") == "pass"
        elif col["name"] in comp_names:
            m = comp_names[col["name"]]
            if m.get("asm_evidence_va") or any(
                ws.get("evidence_va") for ws in m.get("wire_sources", [])
            ):
                col["asm_verified"] = True
    data["asm_audit"] = {
        "composite_ref": comp_id,
        "status": audit.get("status", "pass"),
        "updated": TODAY,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def count_va_gaps() -> int:
    total = 0
    for comp_id in MEMBER_COMPS:
        data = json.loads((COMP / f"{comp_id}.json").read_text(encoding="utf-8"))
        for m in data.get("members", []):
            if not any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
                total += 1
    return total


def main() -> None:
    ida = json.loads(IDA_JSON.read_text(encoding="utf-8"))
    total = 0
    for comp_id in MEMBER_COMPS:
        va_map = build_va_map(comp_id, ida)
        n = patch_reader_paths(comp_id, va_map)
        total += n
        print(f"{comp_id}: patched {n} reader paths ({len(va_map)} fields mapped)")

    for comp_id, tbl in TABLE_MAP.items():
        patch_table(tbl, comp_id)

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 8:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Total patched: {total}, batch8 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
