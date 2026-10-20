#!/usr/bin/env python3
"""Patch batch-7 ASM audit gaps and layout_same_as aliases."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TABLES = ROOT / "schema" / "_legacy_tables"
TODAY = str(date.today())

GAPS: dict[str, dict[str, str]] = {
    "intro_info": {
        "notice_body": "0xB461B1",
    },
    "hack_check": {
        "ai_num": "0xB067C5",
        "perf_pre_chara": "0xB067D6",
        "perf_chara": "0xB067E7",
        "perf_ai": "0xB067F8",
        "perf_last": "0xB06809",
        "perf_if": "0xB0681A",
        "perf_rdr": "0xB06830",
    },
    "recruit": {
        "pstat": "0xB45487",
        "is_lock": "0xB4549D",
    },
}

READER_VA: dict[str, dict[str, str]] = {
    "intro_info": {
        "active_time_bits": "0xB46155",
        "play_style": "0xB46168",
        "feature_word": "0xB4618A",
        "notice_body": "0xB461B1",
    },
    "hack_check": {
        "move_spd": "0xB065EB",
        "boost_gauge": "0xB06606",
        "boost_recov": "0xB0661E",
        "boost_consume": "0xB06636",
        "clcheck_result": "0xB0663E",
        "weapon_itemid": "0xB06653",
        "weapon_cooltime": "0xB06668",
        "weapon_rapidtime": "0xB0667D",
        "weapon_reload": "0xB06692",
        "debugger_found": "0xB066A7",
        "proc_ref_count": "0xB066BC",
        "reserved1": "0xB066D1",
        "reserved2": "0xB066E6",
        "weapon_bullet_speed": "0xB066FB",
        "weapon_range": "0xB06710",
        "weapon_charge_time": "0xB06725",
        "weapon_bullet_mgz": "0xB0673A",
        "weapon_bullet_all": "0xB0674F",
        "weapon_batch_fire": "0xB06764",
        "weapon_fired": "0xB06779",
        "wrestle_size": "0xB0678E",
        "wrestle_hack_check_ex": "0xB067A3",
        "fps": "0xB067B4",
        "ai_num": "0xB067C5",
        "perf_pre_chara": "0xB067D6",
        "perf_chara": "0xB067E7",
        "perf_ai": "0xB067F8",
        "perf_last": "0xB06809",
        "perf_if": "0xB0681A",
        "perf_rdr": "0xB06830",
    },
    "lvjudge_hist": {
        "pilot_id": "0xB44769",
        "lv_history": "0xB4478E",
        "lv_history_num": "0xB447AE",
        "lv_history_max": "0xB447C4",
        "xwarwin_history": "0xB447E1",
        "xwarlose_history": "0xB4480B",
        "termstr_now": "0xB4482C",
        "term_old": "0xB44852",
    },
    "unlocked_navi": {
        "navi_id": "0xB434C6",
        "status": "0xB434DA",
    },
    "pointdmg": {
        "gaugedmg": "0xB45784",
    },
    "total_result_wave": {
        "end_wave": "0xB4559A",
        "result_coop": "0xB455C4",
        "rank": "0xB455C4",
        "rank_score": "0xB455DC",
        "container_comp": "0xB455F1",
        "enemyobj_comp": "0xB45613",
        "total_score": "0xB4563E",
    },
    "recruit": {
        "channel_id": "0xB4541A",
        "party_id": "0xB4542F",
        "troops": "0xB45441",
        "member_count": "0xB45454",
        "comment": "0xB4546C",
        "pstat": "0xB45487",
        "is_lock": "0xB4549D",
    },
}

TABLE_MAP = {
    "member": "tbl_member",
    "intro_info": "tbl_intro_info",
    "hack_check": "tbl_hack_check",
    "lvjudge_hist": "tbl_lvjudge_hist",
    "mprogress": "tbl_mprogress",
    "netcafe_challenge_info": "tbl_netcafe_challenge_info",
    "unlocked_navi": "tbl_unlocked_navi",
    "pointdmg": "tbl_pointdmg",
    "total_result_wave": "tbl_total_result_wave",
    "recruit": "tbl_recruit",
}

LAYOUT_SAME_AS = {
    "member": "leaders",
    "mprogress": "progress",
    "netcafe_challenge_info": "challenge_info",
}

MEMBER_COMPS = [
    "intro_info",
    "hack_check",
    "lvjudge_hist",
    "unlocked_navi",
    "pointdmg",
    "total_result_wave",
    "recruit",
]


def merge_reader_va(existing: str, reader_va: str) -> str:
    if "|" in existing:
        parts = existing.split("|")
        return f"{reader_va}|{parts[-1]}"
    if re.match(r"^[0-9A-Fa-f]{5,6}$", existing):
        return f"{reader_va}|{existing}"
    return reader_va


def patch_composite(comp_id: str, gaps: dict[str, str]) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    rw_fn = data.get("reader") or data.get("writer")
    for m in data.get("members", []):
        va = gaps.get(m["name"])
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
    data["asm_audit"] = {
        "verified": TODAY,
        "function": rw_fn,
        "composite_length": data.get("length"),
        "fields_patched": n,
        "fields_missing_va": len(missing),
        "status": "pass" if not missing else "pass_with_gaps",
        "note": "gaps patched via _patch_asm_batch7.py IDA decompile",
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if missing:
        print(f"  {comp_id}: still missing {missing}")
    return n


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
        print(f"{comp_id} gaps: patched {n} fields")

    for comp_id, va_map in READER_VA.items():
        n = patch_reader_paths(comp_id, va_map)
        total += n
        print(f"{comp_id} reader paths: patched {n}")

    for alias, source in LAYOUT_SAME_AS.items():
        stamp_layout_alias(alias, source)
        print(f"{alias}: stamped layout_same_as -> {source}")

    for comp_id, tbl in TABLE_MAP.items():
        patch_table(tbl, comp_id)

    va_gaps = count_va_gaps()
    qpath = ROOT / "schema" / "_meta" / "asm_audit_queue.json"
    q = json.loads(qpath.read_text(encoding="utf-8"))
    for b in q["batches"]:
        if b["id"] == 7:
            b.setdefault("summary", {})
            b["summary"]["va_gaps"] = va_gaps
            b["summary"]["gaps_patched"] = TODAY
    q["updated"] = TODAY
    qpath.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Total patched: {total}, batch7 va_gaps remaining: {va_gaps}")


if __name__ == "__main__":
    main()
