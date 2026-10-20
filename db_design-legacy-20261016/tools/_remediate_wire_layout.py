#!/usr/bin/env python3
"""Apply wire vs memory offset remediation patches to composites."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT / "schema" / "composites"
TODAY = str(date.today())

# Manual: wire offset (+ optional memory_offset / memory_only)
PATCHES: dict[str, dict[str, dict]] = {
    "leaders": {
        "avatar": {"offset": 33, "memory_offset": 36},
        "pstat": {"offset": 51, "memory_offset": 60},
    },
    "dc_point": {
        "bef_next": {"memory_only": True, "memory_offset": 12},
        "aft_next": {"memory_only": True, "memory_offset": 24},
    },
    "config": {
        "A_point_max": {"offset": 2, "memory_offset": 4},
        "A_win_cnt": {"offset": 6, "memory_offset": 8},
        "B_troops": {"offset": 10, "memory_offset": 12},
        "B_point_max": {"offset": 12, "memory_offset": 16},
        "B_win_cnt": {"offset": 16, "memory_offset": 20},
        "dotdmg_min": {"offset": 20, "memory_offset": 24},
        "atk_team": {"offset": 24, "memory_offset": 28},
        "round_now": {"offset": 26, "memory_offset": 32},
        "round_max": {"offset": 30, "memory_offset": 36},
    },
    "bgm_desc": {
        "field_bgm_id": {"offset": 1, "memory_offset": 4},
        "ace_bgm_id": {"offset": 5, "memory_offset": 8},
        "force_bgm_id": {"offset": 9, "memory_offset": 12},
        "is_one_shot": {"offset": 13, "memory_offset": 16},
    },
    "recruits": {
        "member_count": {"offset": 9, "memory_offset": 10},
        "comment": {"offset": 11, "memory_offset": 12},
        "pstat": {"offset": 72, "memory_offset": 73},
        "is_lock": {"offset": 73, "memory_offset": 74},
        "remain_minutes": {"offset": 74, "memory_offset": 76},
        "party_type": {"offset": 76, "memory_offset": 80},
    },
    "bracket": {
        "nodes": {"offset": 1, "memory_offset": 2},
    },
    "item_list": {
        "stock": {"offset": 21, "memory_offset": 22},
    },
    "party_member_stat": {
        "rate_vslocal": {"offset": 5, "memory_offset": 6},
        "stat": {"offset": 7, "memory_offset": 8},
        "is_booking": {"offset": 8, "memory_offset": 9},
        "mission_id": {"offset": 9, "memory_offset": 12},
        "avatar": {"offset": 13, "memory_offset": 16},
    },
    "ranking": {
        "clan_id": {"offset": 35, "memory_offset": 36},
        "clan_name": {"offset": 39, "memory_offset": 40},
        "emb_base": {"offset": 70, "memory_offset": 71},
        "emb_parts1": {"offset": 71, "memory_offset": 72},
        "emb_parts2": {"offset": 72, "memory_offset": 73},
        "score": {"offset": 73, "memory_offset": 76},
        "avatar": {"offset": 77, "memory_offset": 80},
    },
    "sort_info": {
        "time_value": {"offset": 13, "memory_offset": 16},
        "style_value": {"offset": 17, "memory_offset": 20},
    },
    "xwar_ext_rule": {
        "param": {"offset": 2, "memory_offset": 4},
        "row0": {"offset": 6, "memory_offset": 8},
        "row1": {"offset": 130, "memory_offset": 132},
        "row2": {"offset": 254, "memory_offset": 260},
        "row3": {"offset": 378, "memory_offset": 388, "length": 124},
    },
}

# Pull wire offset from reader-matching wire_sources when ws.offset != member.offset
AUTO_FROM_WS = [
    "progress",
    "phase_info",
    "bracket_info",
    "buildup_info",
    "check_quest",
    "wave_res",
    "appear_info",
]


def apply_field_patch(m: dict, patch: dict, reader: str | None) -> None:
    if "memory_offset" not in patch and "offset" in patch:
        if "memory_offset" not in m:
            m["memory_offset"] = m["offset"]
    for k, v in patch.items():
        m[k] = v
    if not m.get("memory_only") and "offset" in patch:
        new_off = m.get("offset")
        for ws in m.get("wire_sources", []):
            ws["offset"] = new_off


def apply_patch(comp_id: str, fields: dict[str, dict]) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    reader = data.get("reader") or data.get("writer")
    by_name = {m["name"]: m for m in data.get("members", [])}
    n = 0
    for fname, patch in fields.items():
        m = by_name.get(fname)
        if not m:
            print(f"  skip missing {comp_id}.{fname}")
            continue
        apply_field_patch(m, patch, reader)
        n += 1
    data["wire_memory_remediated"] = TODAY
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def remediate_from_wire_sources(comp_id: str) -> int:
    path = COMP / f"{comp_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    reader = data.get("reader") or data.get("writer")
    if not reader:
        return 0
    n = 0
    for m in data.get("members", []):
        if m.get("memory_only"):
            continue
        primary = None
        for ws in m.get("wire_sources", []):
            fn = ws.get("reader") or ws.get("writer")
            if fn == reader and ws.get("offset") is not None:
                primary = ws
                break
        if not primary or primary["offset"] == m.get("offset"):
            continue
        if "memory_offset" not in m:
            m["memory_offset"] = m["offset"]
        m["offset"] = primary["offset"]
        n += 1
    if n:
        data["wire_memory_remediated"] = TODAY
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def remediate_avatar() -> int:
    """Sync sub_B068B0 reader ws offsets to struct-relative wire layout."""
    path = COMP / "avatar.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    reader = data.get("reader")
    if not reader:
        return 0
    n = 0
    for m in data.get("members", []):
        wire_off = m.get("offset")
        for ws in m.get("wire_sources", []):
            if ws.get("reader") == reader and ws.get("offset") != wire_off:
                ws["offset"] = wire_off
                n += 1
    if n:
        data["wire_memory_remediated"] = TODAY
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def remediate_xwar_tail() -> int:
    path = COMP / "xwar_ext_rule.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    members = data.get("members", [])
    by_name = {m["name"]: m for m in members}
    if "row3" in by_name:
        by_name["row3"]["length"] = 124
        by_name["row3"]["offset"] = 378
    if "tail_pad" not in by_name:
        members.append(
            {
                "name": "tail_pad",
                "offset": 502,
                "length": 12,
                "wire_type": "pad[12]",
                "meaning": "线尾填充至 514B",
                "disposition": "PERSIST",
                "wire_sources": [
                    {
                        "command": "SC-0xCCDF-lounge-xwar_booking_option_get_r",
                        "struct": "xwar_ext_rule",
                        "field_name": "tail_pad",
                        "offset": 502,
                        "length": 12,
                        "wire_type": "pad[12]",
                        "protocol_path": "protocol_analysis/commands/SC-0xCCDF-lounge-xwar_booking_option_get_r/README.md",
                        "section": "§3 / notes.md",
                        "reader": "sub_B08160",
                        "printer": "sub_B0BEC0",
                        "notes": "128×u32 线长 514；row3 后 12B 填充",
                        "evidence_va": "0xB08191",
                    }
                ],
            }
        )
        data["members"] = members
        data["wire_memory_remediated"] = TODAY
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return 1
    return 0


def remediate_ai() -> int:
    path = COMP / "AI.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    reader = data.get("reader")
    n = 0
    head = {
        "param_id": (34, 36),
        "action_type": (38, 40),
        "move_spd": (39, 42),
    }
    for m in data.get("members", []):
        if m["name"] in head:
            wire, mem = head[m["name"]]
            m["memory_offset"] = mem
            m["offset"] = wire
            n += 1
        elif m.get("offset", 0) >= 44:
            mem = m.get("memory_offset", m["offset"])
            m["memory_offset"] = mem
            m["offset"] = mem - 3
            n += 1
        if reader and not m.get("memory_only"):
            for ws in m.get("wire_sources", []):
                if ws.get("reader") == reader:
                    ws["offset"] = m["offset"]
    data["wire_memory_remediated"] = TODAY
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return n


def stamp_alias_from_source(alias_id: str, source_id: str) -> None:
    src_path = COMP / f"{source_id}.json"
    alias_path = COMP / f"{alias_id}.json"
    if not src_path.exists() or not alias_path.exists():
        return
    src = json.loads(src_path.read_text(encoding="utf-8"))
    alias = json.loads(alias_path.read_text(encoding="utf-8"))
    if src.get("asm_audit", {}).get("status") == "pass":
        alias["asm_audit"] = {
            **alias.get("asm_audit", {}),
            "status": "pass",
            "layout_same_as": source_id,
            "source_chain_ok": True,
            "verified": TODAY,
        }
        alias_path.write_text(json.dumps(alias, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    total = 0
    for comp_id, fields in PATCHES.items():
        n = apply_patch(comp_id, fields)
        total += n
        print(f"{comp_id}: manual {n}")

    for comp_id in AUTO_FROM_WS:
        n = remediate_from_wire_sources(comp_id)
        total += n
        print(f"{comp_id}: auto ws {n}")

    n = remediate_ai()
    total += n
    print(f"AI: special {n}")

    n = remediate_avatar()
    total += n
    print(f"avatar: reader ws sync {n}")

    n = remediate_xwar_tail()
    total += n
    print(f"xwar_ext_rule: tail_pad {n}")

    # Aliases with empty members: copy source JSON layout fields via re-read
    for alias, src in (("extrarule_xwar_info", "xwar_ext_rule"), ("toppilots", "ranking")):
        src_data = json.loads((COMP / f"{src}.json").read_text(encoding="utf-8"))
        alias_path = COMP / f"{alias}.json"
        alias_data = json.loads(alias_path.read_text(encoding="utf-8"))
        alias_data["wire_memory_remediated"] = TODAY
        if src_data.get("asm_audit"):
            alias_data["asm_audit"] = {
                **src_data["asm_audit"],
                "layout_same_as": src,
            }
        alias_path.write_text(json.dumps(alias_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{alias}: stamped from {src}")

    for alias, src in (
        ("toppilots", "ranking"),
        ("extrarule_xwar_info", "xwar_ext_rule"),
        ("mprogress", "progress"),
        ("member", "leaders"),
        ("dcpoint_detail", "dc_point"),
    ):
        stamp_alias_from_source(alias, src)

    print(f"Total field updates: {total}")


if __name__ == "__main__":
    main()
