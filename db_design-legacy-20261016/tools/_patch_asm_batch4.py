#!/usr/bin/env python3
"""Patch batch-4 ASM audit gaps and layout_same_as aliases."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
TODAY = str(date.today())

GAPS: dict[str, dict[str, str]] = {
    "xwar_ext_rule": {
        "row1": "0xB08191",
        "row2": "0xB08191",
        "row3": "0xB08191",
    },
    "bgm_desc": {
        "is_one_shot": "0xB07E63",
    },
}

TABLE_MAP = {
    "ext_subrule": "tbl_ext_subrule",
    "xwar_ext_rule": "tbl_xwar_ext_rule",
    "extrarule_xwar_info": "tbl_extrarule_xwar_info",
    "wbonus": "tbl_wbonus",
    "eq_bonus_modules_lot": "tbl_eq_bonus_modules_lot",
    "buffitem": "tbl_buffitem",
    "buffitem_ex": "tbl_buffitem_ex",
    "config": "tbl_config",
    "progress": "tbl_progress",
    "bgm_desc": "tbl_bgm_desc",
}

LAYOUT_SAME_AS = {
    "extrarule_xwar_info": "xwar_ext_rule",
    "buffitem_ex": "buffitem",
}

MEMBER_COMPS = [
    "ext_subrule", "xwar_ext_rule", "wbonus", "eq_bonus_modules_lot",
    "buffitem", "config", "progress", "bgm_desc",
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
            if ws.get("evidence_va", "").startswith("0x"):
                continue
            ws["evidence_va"] = va
        if not any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
            for ws in m.get("wire_sources", []):
                if ws.get("reader") and reader_fn and ws["reader"] != reader_fn:
                    continue
                if "|" in str(ws.get("evidence_va", "")):
                    continue
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
        "note": "gaps patched via _patch_asm_batch4.py IDA decompile",
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
        audit = comp.get("asm_audit", {})
        if col.get("composite_ref") == comp_id:
            col["asm_verified"] = audit.get("status") == "pass"
        elif col["name"] in comp_names:
            m = comp_names[col["name"]]
            if m.get("asm_evidence_va") or any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
                col["asm_verified"] = True
    audit = comp.get("asm_audit", {})
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
        patch_table(TABLE_MAP[comp_id], comp_id)
        print(f"{comp_id}: patched {n} fields")

    for alias, source in LAYOUT_SAME_AS.items():
        stamp_layout_alias(alias, source)
        print(f"{alias}: stamped layout_same_as -> {source}")

    # eq_bonus_modules_lot: inline reader loop @ B71220 (already has pipe-form VA)
    eql_path = COMP / "eq_bonus_modules_lot.json"
    eql = json.loads(eql_path.read_text(encoding="utf-8"))
    eql["asm_audit"] = {
        "verified": TODAY,
        "function": "sub_B51930@0xB71220",
        "composite_length": eql.get("length"),
        "fields_missing_va": 0,
        "status": "pass",
        "note": "inline sub_B02DD0×3 cmp edi,3 @ loc_B71220",
    }
    eql_path.write_text(json.dumps(eql, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for comp_id in TABLE_MAP:
        if comp_id in LAYOUT_SAME_AS or comp_id in GAPS:
            continue
        patch_table(TABLE_MAP[comp_id], comp_id)

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 4:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Total patched: {total}, batch4 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
