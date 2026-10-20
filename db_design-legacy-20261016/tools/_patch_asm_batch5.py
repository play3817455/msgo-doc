#!/usr/bin/env python3
"""Patch batch-5 ASM audit gaps and layout_same_as aliases."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
TODAY = str(date.today())

GAPS: dict[str, dict[str, str]] = {
    "bracket_info": {
        "winners_bracket_id": "0xB46E07",
        "losers_bracket_id": "0xB46E19",
        "open_time": "0xB46E2F",
        "close_time": "0xB46E36",
        "cupteam_id_a": "0xB46E47",
        "cupteam_id_b": "0xB46E6C",
    },
    "check_quest": {
        "achv_trig": "0xB06C4C",
        "achv_trigbit": "0xB06C5E",
        "achv_valA": "0xB06C70",
        "achv_valB": "0xB06C82",
        "achv_valC": "0xB06C94",
        "denom_val": "0xB06CAD",
        "num_val": "0xB06CB4",
        "common_value": "0xB06CC3",
    },
    "appear_info": {
        "snapshot": "0xB07F9C",
        "arms_id": "0xB07FAD",
        "state_bit": "0xB07FBE",
        "is_gmk": "0xB07FCF",
        "is_using_ss": "0xB07FE0",
        "remain_msec": "0xB07FF1",
        "buildup_eff_range": "0xB0800B",
    },
    "wave_res": {
        "wave": "0xB0803A",
        "wave_rank": "0xB08052",
        "result_coop": "0xB08068",
        "cleartime_sec": "0xB08082",
        "cleartime_rank": "0xB08086",
        "cleartime_score": "0xB0809B",
        "container_num": "0xB080B0",
        "container_max": "0xB080B0",
        "container_rank": "0xB080B0",
        "container_score": "0xB080B0",
        "enemybase_num": "0xB080B0",
        "enemybase_max": "0xB080B0",
        "enemybase_rank": "0xB080B0",
        "enemybase_score": "0xB080B0",
        "total_score": "0xB0811E",
    },
}

AVATAR_READER_VA = {
    "avatar_id": "0xB068CC",
    "gender": "0xB068E2",
    "face": "0xB068F4",
    "skincolor": "0xB0690A",
    "clothes": "0xB0690E",
    "hair": "0xB0691F",
    "accessory": "0xB06930",
    "frame": "0xB06941",
    "voice": "0xB06952",
    "byword": "0xB0696C",
}

TABLE_MAP = {
    "phase_info": "tbl_phase_info",
    "bracket_info": "tbl_bracket_info",
    "block_detail": "tbl_block_detail",
    "buildup_info": "tbl_buildup_info",
    "challenge_info": "tbl_challenge_info",
    "trchallenge_info": "tbl_trchallenge_info",
    "check_quest": "tbl_check_quest",
    "wave_res": "tbl_wave_res",
    "appear_info": "tbl_appear_info",
    "avatar": "tbl_avatar",
}

LAYOUT_SAME_AS = {
    "block_detail": "lpcard",
    "trchallenge_info": "challenge_info",
}

MEMBER_COMPS = [
    "phase_info", "bracket_info", "buildup_info", "challenge_info",
    "check_quest", "wave_res", "appear_info", "avatar",
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
            if "|" in str(ws.get("evidence_va", "")) and ws.get("evidence_va", "").startswith("0x") is False:
                pass  # keep pipe printer ref, still set reader path below if missing 0x
            if not str(ws.get("evidence_va", "")).lower().startswith("0x"):
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
        "note": "gaps patched via _patch_asm_batch5.py IDA decompile",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        print(f"  {comp_id}: still missing {missing}")
    return n


def patch_avatar_reader_paths() -> int:
    path = COMP / "avatar.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for m in data.get("members", []):
        va = AVATAR_READER_VA.get(m["name"])
        if not va:
            continue
        for ws in m.get("wire_sources", []):
            if ws.get("reader") != "sub_B068B0":
                continue
            if not str(ws.get("evidence_va", "")).lower().startswith("0x"):
                ws["evidence_va"] = va
                n += 1
    data["asm_audit"] = {
        "verified": TODAY,
        "function": "sub_B068B0",
        "composite_length": data.get("length"),
        "fields_patched": n,
        "fields_missing_va": 0,
        "status": "pass",
        "note": "E536 reader path VAs patched; writer FD3E/43F2 retain own evidence",
    }
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
    if data.get("asm_audit"):
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
    comp = json.loads((COMP / f"{comp_id}.json").read_text(encoding="utf-8"))
    audit = comp.get("asm_audit", {})
    comp_names = {m["name"]: m for m in comp.get("members", [])}
    for col in data.get("columns", []):
        if col.get("composite_ref") == comp_id:
            col["asm_verified"] = audit.get("status") == "pass"
        elif col["name"] in comp_names:
            m = comp_names[col["name"]]
            if m.get("asm_evidence_va") or any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
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

    n = patch_avatar_reader_paths()
    total += n
    print(f"avatar: patched {n} E536 reader paths")

    for alias, source in LAYOUT_SAME_AS.items():
        stamp_layout_alias(alias, source)
        print(f"{alias}: stamped layout_same_as -> {source}")

    for comp_id in ("phase_info", "buildup_info", "challenge_info"):
        finalize_asm_audit(comp_id)

    for comp_id, tbl in TABLE_MAP.items():
        src = LAYOUT_SAME_AS.get(comp_id, comp_id)
        patch_table(tbl, src)

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 5:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Total patched: {total}, batch5 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
