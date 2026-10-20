#!/usr/bin/env python3
"""Patch batch-3 ASM audit gaps and layout_same_as aliases."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
TODAY = str(date.today())

GAPS: dict[str, dict[str, str]] = {
    "rankself": {
        "entry_until_es": "0xB4651E",
        "eventscores": "0xB46536",
    },
    "ranking": {
        "troops": "0xB465C9",
        "level": "0xB465DF",
        "clan_id": "0xB465F2",
        "clan_name": "0xB46610",
        "emb_base": "0xB46627",
        "emb_parts1": "0xB46639",
        "emb_parts2": "0xB4664B",
        "score": "0xB4665D",
        "avatar": "0xB46668",
    },
    "sort_info": {
        "style_value": "0xB462C4",
    },
}

TABLE_MAP = {
    "item_list": "tbl_item_list",
    "party_member_stat": "tbl_party_member_stat",
    "order": "tbl_order",
    "rankself": "tbl_rankself",
    "ranking": "tbl_ranking",
    "special_a_next": "tbl_special_a_next",
    "sort_info": "tbl_sort_info",
    "special_a_info": "tbl_special_a_info",
    "ranking_info": "tbl_ranking_info",
    "toppilots": "tbl_toppilots",
}

LAYOUT_SAME_AS = {
    "special_a_info": "rankself",
    "ranking_info": "order",
    "toppilots": "ranking",
}


def patch_composite(comp_id: str, gaps: dict[str, str]) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    reader_fn = data.get("reader")
    for m in data.get("members", []):
        va = gaps.get(m["name"])
        if not va:
            continue
        for ws in m.get("wire_sources", []):
            if ws.get("reader") and reader_fn and ws["reader"] != reader_fn:
                if not m.get("composite_ref"):
                    continue
            if "|" in str(ws.get("evidence_va", "")):
                continue
            ws["evidence_va"] = va
            if m.get("composite_ref") and ws.get("reader") != reader_fn:
                ws["evidence_call_site"] = reader_fn
        m["asm_verified"] = True
        m["asm_evidence_va"] = va
        m["asm_audit_date"] = TODAY
        n += 1

    members = data.get("members", [])
    missing = [
        x["name"]
        for x in members
        if not any(ws.get("evidence_va") for ws in x.get("wire_sources", []))
    ]
    fn = data.get("reader") or data.get("writer")
    data["asm_audit"] = {
        "verified": TODAY,
        "function": fn,
        "composite_length": data.get("length"),
        "fields_patched": n,
        "fields_missing_va": len(missing),
        "status": "pass" if not missing else "pass_with_gaps",
        "note": "gaps patched via _patch_asm_batch3.py IDA decompile",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        print(f"  {comp_id}: still missing {missing}")
    return n


def stamp_layout_alias(alias_id: str, source_id: str) -> None:
    src = json.loads((COMP / f"{source_id}.json").read_text(encoding="utf-8"))
    path = COMP / f"{alias_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["asm_audit"] = {
        "verified": TODAY,
        "function": data.get("reader") or src.get("reader"),
        "composite_length": data.get("length"),
        "layout_same_as": source_id,
        "source_asm_audit": src.get("asm_audit", {}),
        "status": src.get("asm_audit", {}).get("status", "pass"),
        "note": f"成员与 evidence_va 见 composite {source_id}",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tbl = TABLES / f"tbl_{alias_id}.json"
    if tbl.exists():
        td = json.loads(tbl.read_text(encoding="utf-8"))
        td["asm_audit"] = {
            "composite_ref": alias_id,
            "layout_same_as": source_id,
            "status": data["asm_audit"]["status"],
            "updated": TODAY,
        }
        tbl.write_text(json.dumps(td, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def patch_table(tbl_id: str, comp_id: str) -> None:
    path = TABLES / f"{tbl_id}.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    comp = json.loads((COMP / f"{comp_id}.json").read_text(encoding="utf-8"))
    comp_names = {m["name"]: m for m in comp.get("members", [])}
    for col in data.get("columns", []):
        if col.get("composite_ref") == comp_id:
            col["asm_verified"] = comp["asm_audit"]["status"] == "pass"
        elif col["name"] in comp_names:
            m = comp_names[col["name"]]
            if m.get("asm_evidence_va"):
                col["asm_verified"] = True
    data["asm_audit"] = {
        "composite_ref": comp_id,
        "status": comp["asm_audit"]["status"],
        "updated": TODAY,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def count_va_gaps() -> int:
    total = 0
    for comp_id in ("item_list", "party_member_stat", "order", "rankself", "ranking", "special_a_next", "sort_info"):
        data = json.loads((COMP / f"{comp_id}.json").read_text(encoding="utf-8"))
        for m in data.get("members", []):
            if not any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
                total += 1
    return total


def main() -> None:
    total = 0
    for comp_id, gaps in GAPS.items():
        n = patch_composite(comp_id, gaps)
        total += n
        patch_table(TABLE_MAP[comp_id], comp_id)
        print(f"{comp_id}: patched {n} fields")

    for alias, source in LAYOUT_SAME_AS.items():
        stamp_layout_alias(alias, source)
        print(f"{alias}: stamped layout_same_as -> {source}")

    for comp_id in TABLE_MAP:
        if comp_id in LAYOUT_SAME_AS:
            continue
        if comp_id in GAPS:
            continue
        if (COMP / f"{comp_id}.json").exists():
            patch_table(TABLE_MAP[comp_id], comp_id)

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 3:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Total patched: {total}, batch3 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
