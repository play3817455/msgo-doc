#!/usr/bin/env python3
"""Patch batch-6 ASM audit gaps and layout_same_as aliases."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
TODAY = str(date.today())

GAPS: dict[str, dict[str, str]] = {
    "beginner_challenge_info": {
        "archived": "0xB42482",
        "value": "0xB424AC",
    },
    "clan_eff": {
        "reserved": "0xB45F93",
    },
    "examination_state": {
        "interval_cnt": "0xB423D9",
    },
}

TABLE_MAP = {
    "beginner_challenge_info": "tbl_beginner_challenge_info",
    "adop_get": "tbl_adop_get",
    "clan_eff": "tbl_clan_eff",
    "clan_zeon": "tbl_clan_zeon",
    "dailycup_conf": "tbl_dailycup_conf",
    "dailycup_conf_next": "tbl_dailycup_conf_next",
    "dc_point": "tbl_dc_point",
    "dcpoint_detail": "tbl_dcpoint_detail",
    "exam_state": "tbl_exam_state",
    "friend_histories": "tbl_friend_histories",
}

LAYOUT_SAME_AS = {
    "adop_get": "adop_list",
    "clan_zeon": "clan_eff",
    "dailycup_conf_next": "dailycup_conf",
    "dcpoint_detail": "dc_point",
    "exam_state": "examination_state",
    "friend_histories": "lpcard",
}

MEMBER_COMPS = [
    "beginner_challenge_info",
    "clan_eff",
    "dailycup_conf",
    "dc_point",
    "examination_state",
]


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
                continue
            if ws.get("reader") == "sub_B478A0":
                continue
            cur = str(ws.get("evidence_va", ""))
            if cur.lower().startswith("0x"):
                ws["evidence_va"] = va
            elif not cur or cur.startswith("B6FB"):
                ws["evidence_va"] = va
            elif "|" in cur and not cur.split("|")[0].lower().startswith("0x"):
                ws["evidence_va"] = va
            else:
                ws["evidence_va"] = va
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
        "note": "gaps patched via _patch_asm_batch6.py IDA decompile",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        print(f"  {comp_id}: still missing {missing}")
    return n


def fix_examination_state_063e_offsets() -> int:
    """063E wire_sources lack offset/length; audit uses ws[0] as primary."""
    path = COMP / "examination_state.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for m in data.get("members", []):
        for ws in m.get("wire_sources", []):
            if ws.get("command") != "SC-0x063E-lounge-pilot_select_r":
                continue
            if ws.get("offset") is None:
                ws["offset"] = m["offset"]
                n += 1
            if ws.get("length") is None:
                ws["length"] = m["length"]
                n += 1
            if ws.get("wire_type") is None:
                ws["wire_type"] = m.get("wire_type")
            if not ws.get("reader"):
                ws["reader"] = data.get("reader")
            if not ws.get("printer"):
                ws["printer"] = data.get("printer")
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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


def finalize_asm_audit(comp_id: str) -> None:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("asm_audit") and data["asm_audit"].get("verified") == TODAY:
        if comp_id not in GAPS:
            return
    members = data.get("members", [])
    missing = [
        x["name"]
        for x in members
        if not any(ws.get("evidence_va") for ws in x.get("wire_sources", []))
    ]
    data["asm_audit"] = {
        "verified": TODAY,
        "function": data.get("reader") or data.get("writer"),
        "composite_length": data.get("length"),
        "fields_missing_va": len(missing),
        "status": "pass" if not missing else "pass_with_gaps",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def patch_table(tbl_id: str, comp_id: str) -> None:
    path = TABLES / f"{tbl_id}.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    src_id = LAYOUT_SAME_AS.get(comp_id, comp_id)
    comp = json.loads((COMP / f"{src_id}.json").read_text(encoding="utf-8"))
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
    total = 0
    for comp_id, gaps in GAPS.items():
        n = patch_composite(comp_id, gaps)
        total += n
        print(f"{comp_id}: patched {n} fields")

    n = fix_examination_state_063e_offsets()
    total += n
    print(f"examination_state: fixed {n} 063E offset/length fields")

    for comp_id in ("dailycup_conf", "dc_point"):
        finalize_asm_audit(comp_id)

    for alias, source in LAYOUT_SAME_AS.items():
        stamp_layout_alias(alias, source)
        print(f"{alias}: stamped layout_same_as -> {source}")

    for comp_id, tbl in TABLE_MAP.items():
        patch_table(tbl, comp_id)

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 6:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Total patched: {total}, batch6 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
