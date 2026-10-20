#!/usr/bin/env python3
"""Patch batch-2 ASM audit gaps: evidence_va from IDA decompile/disasm."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
TODAY = str(date.today())

# composite_id -> { field_name: evidence_va }
GAPS: dict[str, dict[str, str]] = {
    "lpcard": {
        "clan_emb_base": "0xB43213",
        "clan_emb_parts1": "0xB4321A",
        "clan_emb_parts2": "0xB4322B",
        "clan_memb_exp": "0xB4323C",
        "clan_memb_exp_use": "0xB4324D",
        "channel_id": "0xB4325E",
        "capture_bonus_state": "0xB4326F",
        "capture_bonus_limit": "0xB43280",
        "rokaku_pt_use": "0xB43291",
        "state_bits": "0xB432AE",
    },
    "ms": {
        "is_exdeck": "0xB07157",
        "is_rokaku": "0xB07170",
        "rokakums_limit_use": "0xB0718F",
        "respawn_wait_sec": "0xB071A6",
        "respawn_wait_max": "0xB071BD",
        "is_reduce_respawn_wait": "0xB071CC",
        "is_extrule_invalid": "0xB071E1",
        "is_heroms": "0xB071F6",
        "level_gauge_now_level": "0xB07213",
    },
    "unlockw": {
        "spticket_success_wp": "0xB43A48",
        "spticket_greatest_wp": "0xB43A5B",
    },
    "recruits": {
        "pstat": "0xB45487",
        "is_lock": "0xB4549D",
        "remain_minutes": "0xB454A4",
        "party_type": "0xB454BE",
    },
    "AI": {
        "param_id": "0xB07283",
        "action_type": "0xB07296",
        "move_spd": "0xB072B1",
        "hate_ent_id": "0xB072F9",
        "hate_val": "0xB07322",
        "pop_init_x": "0xB07345",
        "pop_init_y": "0xB0735D",
        "pop_init_z": "0xB07378",
        "pop_init_dir": "0xB07393",
        "fire_start_x": "0xB073AE",
        "fire_start_y": "0xB073C9",
        "fire_start_z": "0xB073E4",
        "fire_end_x": "0xB073FF",
        "fire_end_y": "0xB07421",
        "fire_end_z": "0xB07425",
        "move_end_x": "0xB0743D",
        "move_end_y": "0xB07455",
        "move_end_z": "0xB0746D",
        "order_kind": "0xB07485",
        "order_param": "0xB07499",
        "group_id": "0xB074AD",
        "center_ms_entid": "0xB074C1",
        "route_number": "0xB074D5",
        "formation_id": "0xB074E9",
        "formation_number": "0xB074FD",
        "stuck_escape": "0xB07520",
    },
    "leaders": {
        "level": "0xB45518",
        "rate_vslocal": "0xB4552B",
        "is_leader": "0xB45545",
        "avatar": "0xB4554A",
        "pstat": "0xB45564",
    },
    "bracket_node": {
        "node_id": "0xB46FDA",
        "is_valid": "0xB46FEC",
        "win_team_id": "0xB46FFC",
        "team_tr_a": "0xB47016",
        "team_id_a": "0xB4701A",
        "team_tr_b": "0xB4702B",
        "team_id_b": "0xB47045",
    },
}

TABLE_MAP = {
    "lpcard": "tbl_lpcard",
    "ms": "tbl_ms",
    "snapshot": "tbl_snapshot",
    "funnelss": "tbl_funnelss",
    "unlockw": "tbl_unlockw",
    "adop_list": "tbl_adop_list",
    "recruits": "tbl_recruits",
    "leaders": "tbl_leaders",
    "bracket": "tbl_bracket",
    "AI": "tbl_AI",
    "bracket_node": "tbl_bracket",
}


def patch_composite(comp_id: str, gaps: dict[str, str]) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for m in data.get("members", []):
        va = gaps.get(m["name"])
        if not va:
            continue
        reader_fn = data.get("reader")
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
        "note": "gaps patched via _patch_asm_batch2.py IDA decompile",
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
    comp_names = {m["name"]: m for m in comp.get("members", [])}
    for col in data.get("columns", []):
        if col.get("composite_ref") == comp_id:
            col["asm_verified"] = comp["asm_audit"]["status"] == "pass"
        elif col["name"] in comp_names:
            m = comp_names[col["name"]]
            if m.get("asm_evidence_va"):
                col["asm_verified"] = True
    if comp_id != "bracket_node":
        data["asm_audit"] = {
            "composite_ref": comp_id,
            "status": comp["asm_audit"]["status"],
            "updated": TODAY,
        }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def count_va_gaps() -> int:
    total = 0
    for comp_id in TABLE_MAP:
        if comp_id == "bracket_node":
            continue
        path = COMP / f"{comp_id}.json"
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for m in data.get("members", []):
            if not any(ws.get("evidence_va") for ws in m.get("wire_sources", [])):
                total += 1
    return total


def main() -> None:
    total = 0
    patched_comps: set[str] = set()
    for comp_id, gaps in GAPS.items():
        n = patch_composite(comp_id, gaps)
        total += n
        patched_comps.add(comp_id)
        tbl = TABLE_MAP.get(comp_id)
        if tbl:
            patch_table(tbl, comp_id)
        print(f"{comp_id}: patched {n} fields")

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 2:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Total patched: {total}, batch2 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
