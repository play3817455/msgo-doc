#!/usr/bin/env python3
"""Patch batch-1 ASM audit gaps: add evidence_va to remaining fields."""

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
    "roominfo": {
        "count_eff": "0xB44956",
        "count_zeon": "0xB44967",
        "count_max": "0xB44978",
        "master_pilotid": "0xB44989",
        "master_worldid": "0xB4499A",
    },
    "cinfo": {
        "feature_word": "0xB45B65",
    },
    "pilots_list": {
        "accum_point": "0xB43065",
        "rank": "0xB43079",
        "base_accump": "0xB4308D",
        "req_accump": "0xB430A1",
        "level_point": "0xB430B5",
        "capture_bonus_state": "0xB430C9",
        "capture_bonus_limit": "0xB430E3",
    },
    "pcard": {
        "accum_point": "0xB43065",
        "rank": "0xB43079",
        "base_accump": "0xB4308D",
        "req_accump": "0xB430A1",
        "level_point": "0xB430B5",
        "capture_bonus_state": "0xB430C9",
        "capture_bonus_limit": "0xB430E3",
    },
    "pilot_detail": {
        "heroms_grants": "0xB429BA",
        "heroms_uniqid": "0xB429DD",
        "last_period_bonus": "0xB429F5",
        "daily_battle_bonus_flg": "0xB42A0D",
        "last_daily_battle_bonus": "0xB42A25",
        "check_progress_quest_id": "0xB42A3D",
        "lvjudge_hist": "0xB42A57",
        "pilot_made_timestamp": "0xB42A7A",
        "newpilot_challenge_nextindex": "0xB42A92",
        "newpilot_challenge_last": "0xB42AAA",
        "sc_lv_up_reward_get": "0xB42AC4",
        "sc_lv_max_pre": "0xB42AE9",
        "sc_lv_max": "0xB42B0C",
        "last_pilot_channel_in": "0xB42B20",
        "monthly_bonus_holding_id": "0xB42B34",
        "monthly_bonus_logincnt": "0xB42B48",
        "monthly_bonus_xwarcnt": "0xB42B5C",
        "periodpath_end": "0xB42B70",
        "beginner_challenge_info": "0xB42B91",
    },
}

TABLE_MAP = {
    "roominfo": "tbl_roominfo",
    "cinfo": "tbl_cinfo",
    "pilots_list": "tbl_pilots_list",
    "pcard": "tbl_pcard",
    "pilot_detail": "tbl_pilot_detail",
}


def patch_composite(comp_id: str, gaps: dict[str, str]) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for m in data.get("members", []):
        va = gaps.get(m["name"])
        if not va:
            continue
        for ws in m.get("wire_sources", []):
            ws["evidence_va"] = va
        m["asm_verified"] = True
        m["asm_evidence_va"] = va
        m["asm_audit_date"] = TODAY
        n += 1

    # recompute audit
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
        "fields_patched": n,
        "fields_missing_va": len(missing),
        "status": "pass" if not missing else "pass_with_gaps",
        "note": "gaps patched via _patch_asm_gaps.py IDA disasm",
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
    data["asm_audit"] = {
        "composite_ref": comp_id,
        "status": comp["asm_audit"]["status"],
        "updated": TODAY,
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    total = 0
    for comp_id, gaps in GAPS.items():
        n = patch_composite(comp_id, gaps)
        total += n
        patch_table(TABLE_MAP[comp_id], comp_id)
        print(f"{comp_id}: patched {n} fields")

    # update queue summary
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 1:
            b["summary"]["va_gaps"] = 0
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Total patched: {total}")


if __name__ == "__main__":
    main()
