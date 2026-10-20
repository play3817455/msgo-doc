#!/usr/bin/env python3
"""Memory slot chain audit for composites with memory_offset / memory_claim."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
META = ROOT / "schema" / "_meta"

SLOT_NOTE = re.compile(r"槽内 offset (\d+)")


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_ida_memory_maps() -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for p in sorted(META.glob("ida_memory_slots_batch*.json")):
        data = load_json(p)
        merged.update(data)
    return merged


def resolve_members(comp: dict, composites: dict[str, dict]) -> list[dict]:
    members = comp.get("members", [])
    if not members and comp.get("layout_same_as"):
        src = composites.get(comp["layout_same_as"])
        if src:
            return src.get("members", [])
    return members


def explicit_memory_offset(m: dict) -> int | None:
    """Only fields with declared memory slot (not wire fallback)."""
    if m.get("memory_only") or "memory_offset" in m:
        return m.get("memory_offset")
    return None


def needs_memory_audit(comp: dict, members: list[dict]) -> bool:
    claim = comp.get("memory_claim")
    if claim is not None and comp.get("length") is not None and claim != comp["length"]:
        return True
    return any(m.get("memory_offset") is not None or m.get("memory_only") for m in members)


def slot_hints_from_notes(m: dict) -> list[int]:
    hints: list[int] = []
    for ws in m.get("wire_sources", []):
        note = ws.get("notes") or ""
        hit = SLOT_NOTE.search(note)
        if hit:
            hints.append(int(hit.group(1)))
    return hints


def nearest_ida_slot(ida: dict, mem_off: int) -> int | None:
    slots = ida.get("slots") or []
    if mem_off in slots:
        return mem_off
    for s in slots:
        if abs(s - mem_off) <= 3:
            return s
    return None


def check_memory_chain(
    members: list[dict],
    memory_claim: int | None,
) -> list[str]:
    issues: list[str] = []
    slotted = []
    for m in members:
        mo = explicit_memory_offset(m)
        if mo is None:
            continue
        slotted.append((mo, m))
    if not slotted:
        return issues

    slotted.sort(key=lambda x: x[0])
    for i in range(len(slotted) - 1):
        off, m = slotted[i]
        off2, m2 = slotted[i + 1]
        end = off + m.get("length", 0)
        if end > off2:
            issues.append(
                f"{m['name']}/{m2['name']}: memory overlap {off}+{m.get('length')} > {off2}"
            )

    if memory_claim is not None:
        last_off, last_m = slotted[-1]
        end = last_off + last_m.get("length", 0)
        if end > memory_claim:
            issues.append(
                f"memory chain ends at {end}, memory_claim={memory_claim} ({last_m['name']})"
            )
    return issues


def audit_composite(
    comp_id: str, composites: dict[str, dict], ida_maps: dict[str, dict], save: bool = True
) -> dict:
    comp = composites[comp_id]
    members = resolve_members(comp, composites)
    if not needs_memory_audit(comp, members):
        return {
            "composite": comp_id,
            "skipped": True,
            "reason": "wire==memory (no memory_offset, claim==length)",
        }

    reader = comp.get("reader")
    ida = ida_maps.get(comp_id, {})
    memory_claim = comp.get("memory_claim")
    issues: list[str] = []
    fields_ok = fields_fail = fields_skip = 0
    mem_fields = 0

    for m in members:
        if m.get("memory_only"):
            mo = m.get("memory_offset")
            mem_fields += 1
            if mo is None:
                fields_fail += 1
                issues.append(f"{m['name']}: memory_only but missing memory_offset")
                continue
            if ida.get("slots") and mo not in ida["slots"] and nearest_ida_slot(ida, mo) is None:
                issues.append(f"{m['name']}: memory_offset {mo} not in IDA reader slots {ida['slots'][:8]}")
            fields_ok += 1
            continue

        if "memory_offset" not in m:
            continue
        mem_fields += 1
        mo = m["memory_offset"]
        wire = m.get("offset")
        hints = slot_hints_from_notes(m)

        if hints:
            hint = min(hints)
            # Notes often mark padding *after* prior field, not the field start.
            if mo > hint and mo - hint > 64:
                issues.append(
                    f"{m['name']}: memory_offset {mo} far from notes slot hint {hint}"
                )

        if ida.get("slots"):
            near = nearest_ida_slot(ida, mo)
            if near is None:
                issues.append(
                    f"{m['name']}: memory_offset {mo} not matched in IDA reader slots"
                )
            elif near != mo:
                issues.append(
                    f"{m['name']}: memory_offset {mo} != nearest IDA slot {near}"
                )

        if wire is not None and mo < wire:
            issues.append(f"{m['name']}: memory_offset {mo} < wire offset {wire}")

        field_issues = [i for i in issues if i.startswith(f"{m['name']}:")]
        if field_issues:
            fields_fail += 1
        else:
            fields_ok += 1

    chain_issues = check_memory_chain(members, memory_claim)
    issues.extend(chain_issues)

    status = "pass" if not issues else "fail"
    result = {
        "composite": comp_id,
        "reader": reader,
        "memory_claim": memory_claim,
        "wire_length": comp.get("length"),
        "mem_fields": mem_fields,
        "fields_ok": fields_ok,
        "fields_fail": fields_fail,
        "fields_skip": fields_skip,
        "ida_slots": len(ida.get("slots") or []),
        "issues": issues,
        "status": status,
    }

    comp.setdefault("asm_audit", {})
    # 就地更新：本脚本只拥有下面 6 个键，`note` / `memory_claim` / `manual_batch`
    # 等人工证据是**手写**的，整体替换会静默抹掉（2026-09-24 踩过：一次全量重跑
    # 抹掉 113 个复合体的手写注记，靠 backup 目录才恢复回来）。
    mem = comp["asm_audit"].setdefault("memory", {})
    mem.update({
        "verified": str(date.today()),
        "status": status,
        "mem_fields": mem_fields,
        "fields_ok": fields_ok,
        "fields_fail": fields_fail,
        "issues": issues,
    })
    if save:
        save_json(COMP / f"{comp_id}.json", comp)
    return result


def audit_all(composites: dict[str, dict], ida_maps: dict[str, dict]) -> list[dict]:
    results = []
    for comp_id in sorted(composites):
        comp = composites[comp_id]
        if comp.get("status") != "complete":
            continue
        r = audit_composite(comp_id, composites, ida_maps)
        results.append(r)
        if r.get("skipped"):
            continue
        stamp_tables(comp_id, r)
    return results


def stamp_tables(comp_id: str, result: dict) -> None:
    for p in TABLES.glob("tbl_*.json"):
        tbl = load_json(p)
        ref = tbl.get("entity_ref") or tbl.get("asm_audit", {}).get("composite_ref")
        for col in tbl.get("columns", []):
            if col.get("composite_ref") == comp_id:
                ref = comp_id
        if ref != comp_id and tbl.get("id", "").removeprefix("tbl_") != comp_id:
            continue
        tbl.setdefault("asm_audit", {})
        tbl["asm_audit"]["memory_status"] = result.get("status")
        tbl["asm_audit"]["memory_issues_count"] = len(result.get("issues", []))
        save_json(p, tbl)


def load_composites() -> dict[str, dict]:
    out = {}
    for p in COMP.glob("*.json"):
        d = load_json(p)
        out[d.get("id") or p.stem] = d
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Memory slot chain audit")
    ap.add_argument("--composite", help="Audit single composite id")
    ap.add_argument("--no-save", action="store_true", help="Dry run without writing JSON")
    args = ap.parse_args()

    composites = load_composites()
    ida_maps = load_ida_memory_maps()

    if args.composite:
        if args.no_save:
            r = audit_composite(args.composite, composites, ida_maps, save=False)
            print(json.dumps(r, indent=2, ensure_ascii=False))
            return
        results = [audit_composite(args.composite, composites, ida_maps)]
    else:
        results = audit_all(composites, ida_maps)

    active = [r for r in results if not r.get("skipped")]
    passed = sum(1 for r in active if r.get("status") == "pass")
    failed = sum(1 for r in active if r.get("status") == "fail")
    skipped = sum(1 for r in results if r.get("skipped"))

    print(f"Memory audit: {passed} pass, {failed} fail, {skipped} skipped (no mem diff)")
    for r in active:
        if r.get("status") != "pass":
            print(f"  FAIL {r['composite']:24} issues={len(r.get('issues', []))}")
            for iss in r.get("issues", [])[:4]:
                print(f"    ! {iss}")


if __name__ == "__main__":
    main()
