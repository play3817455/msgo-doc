#!/usr/bin/env python3
"""Batch ASM audit: verify composite member offsets/lengths and stamp asm_verified."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
COMPOSITES = SCHEMA / "composites"
TABLES = SCHEMA / "_legacy_tables"
QUEUE = SCHEMA / "_meta" / "asm_audit_queue.json"

# Known helper wire sizes (from prior IDA analysis)
HELPER_WIRE = {
    "sub_B02DF0": 2,
    "sub_B02DD0": 4,
    "sub_B02D80": 4,
    "sub_B02DA0": 2,
    "sub_B06290": 18,
    "sub_B06230": 1,
    "sub_B061C0": 1,
    "sub_B434F0": 22,
}


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def tbl_to_entity(tbl_id: str) -> str:
    return tbl_id.removeprefix("tbl_")


def wire_members(members: list[dict]) -> list[dict]:
    return [m for m in members if not m.get("memory_only")]


def check_member_chain(
    members: list[dict],
    expected_len: int | None,
    *,
    label: str = "wire",
) -> list[str]:
    issues: list[str] = []
    if not members:
        return issues
    sorted_m = sorted(members, key=lambda m: m.get("offset", -1))
    off = 0
    for m in sorted_m:
        mo = m.get("offset", -1)
        ml = m.get("length", 0)
        if mo != off:
            issues.append(f"{m['name']}: expected {label} offset {off}, got {mo}")
        if ml <= 0:
            issues.append(f"{m['name']}: invalid length {ml}")
        off = mo + ml
    if expected_len is not None and off != expected_len:
        issues.append(f"{label} chain ends at {off}, composite.length={expected_len}")
    return issues


def primary_wire_source(member: dict, rw: str | None) -> dict | None:
    sources = member.get("wire_sources") or []
    if not sources:
        return None
    mo = member.get("offset")
    matching = [
        ws
        for ws in sources
        if rw and (ws.get("reader") == rw or ws.get("writer") == rw)
    ]
    if matching:
        for ws in matching:
            if ws.get("offset") == mo:
                return ws
        return matching[0]
    return sources[0]


def primary_rw(composite: dict) -> tuple[str | None, str | None]:
    return composite.get("reader"), composite.get("writer")


def audit_table(tbl_id: str, ida_totals: dict | None = None) -> dict:
    ent = tbl_to_entity(tbl_id)
    comp_path = COMPOSITES / f"{ent}.json"
    tbl_path = TABLES / f"{tbl_id}.json"
    if not comp_path.exists():
        return {"table": tbl_id, "error": f"missing composite {comp_path.name}"}

    comp = load_json(comp_path)
    members = comp.get("members", [])
    layout_src = comp.get("layout_same_as")
    if not members and layout_src:
        src_path = COMPOSITES / f"{layout_src}.json"
        if src_path.exists():
            src_comp = load_json(src_path)
            members = src_comp.get("members", [])
            comp = {**comp, "_audit_members_from": layout_src}
    length = comp.get("length")
    reader, writer = primary_rw(comp)
    rw = reader or writer

    wire = wire_members(members)
    issues = check_member_chain(wire, length, label="wire")

    # IDA total cross-check
    ida_key = None
    if ida_totals:
        for k, v in ida_totals.items():
            if ent in k or k.endswith(ent.split("_")[0]):
                ida_key = k
                break
        if rw and ida_totals.get(rw):
            ida_total = ida_totals[rw].get("total")
            if ida_total is not None and length is not None and ida_total != length:
                issues.append(f"IDA {rw} total={ida_total} != length={length}")

    fields_ok = 0
    fields_fail = 0
    for m in members:
        m_issues = []
        if not m.get("wire_sources"):
            m_issues.append("missing wire_sources")
        else:
            ws0 = primary_wire_source(m, rw)
            if ws0 is None:
                m_issues.append("missing wire_sources")
            else:
                if not m.get("memory_only"):
                    if ws0.get("offset") != m.get("offset"):
                        m_issues.append(
                            f"wire_sources offset {ws0.get('offset')} != member {m.get('offset')}"
                        )
                if ws0.get("length") != m.get("length"):
                    m_issues.append(
                        f"wire_sources length {ws0.get('length')} != member {m.get('length')}"
                    )
        if m_issues:
            fields_fail += 1
            issues.extend([f"{m['name']}: {x}" for x in m_issues])
        else:
            fields_ok += 1
            m["asm_verified"] = True
            m["asm_audit_date"] = str(date.today())
            pws = primary_wire_source(m, rw)
            if pws and pws.get("evidence_va"):
                m["asm_evidence_va"] = pws["evidence_va"]

    comp["asm_audit"] = {
        "verified": str(date.today()),
        "reader": reader,
        "writer": writer,
        "total_bytes": length,
        "fields_ok": fields_ok,
        "fields_fail": fields_fail,
        "issues": issues,
        "status": "pass" if not issues else "fail",
    }
    save_json(comp_path, comp)

    # stamp table columns that map 1:1 to composite members
    if tbl_path.exists():
        tbl = load_json(tbl_path)
        comp_names = {m["name"] for m in members}
        for col in tbl.get("columns", []):
            if col.get("composite_ref"):
                col["asm_verified"] = comp["asm_audit"]["status"] == "pass"
            elif col["name"] in comp_names:
                col["asm_verified"] = comp["asm_audit"]["status"] == "pass"
        tbl["asm_audit"] = {
            "composite_ref": ent,
            "status": comp["asm_audit"]["status"],
            "issues_count": len(issues),
        }
        save_json(tbl_path, tbl)

    return {
        "table": tbl_id,
        "composite": ent,
        "reader": reader,
        "writer": writer,
        "length": length,
        "members": len(members),
        "fields_ok": fields_ok,
        "fields_fail": fields_fail,
        "status": comp["asm_audit"]["status"],
        "issues": issues,
    }


def run_batch(batch_id: int, ida_totals: dict | None = None) -> list[dict]:
    queue = load_json(QUEUE)
    batch = next(b for b in queue["batches"] if b["id"] == batch_id)
    results = [audit_table(t, ida_totals) for t in batch["tables"]]

    all_pass = all(r.get("status") == "pass" for r in results if "error" not in r)
    batch["status"] = "complete" if all_pass else "complete_with_issues"
    batch["audited"] = str(date.today())
    batch["summary"] = {
        "pass": sum(1 for r in results if r.get("status") == "pass"),
        "fail": sum(1 for r in results if r.get("status") == "fail"),
        "error": sum(1 for r in results if "error" in r),
    }
    if batch_id not in queue.get("completed_batches", []):
        queue.setdefault("completed_batches", []).append(batch_id)
    queue["updated"] = str(date.today())
    save_json(QUEUE, queue)
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="ASM audit batch runner")
    ap.add_argument("batch", type=int, help="Batch id (1-8)")
    ap.add_argument("--ida-json", type=Path, help="Optional IDA totals JSON")
    args = ap.parse_args()

    ida_totals = None
    if args.ida_json and args.ida_json.exists():
        ida_totals = load_json(args.ida_json)

    results = run_batch(args.batch, ida_totals)
    for r in results:
        status = r.get("status", r.get("error", "?"))
        print(
            f"{r['table']:30} {status:8} "
            f"members={r.get('members', '?')} ok={r.get('fields_ok', '?')} "
            f"issues={len(r.get('issues', []))}"
        )
        for iss in r.get("issues", [])[:5]:
            print(f"  ! {iss}")


if __name__ == "__main__":
    main()
