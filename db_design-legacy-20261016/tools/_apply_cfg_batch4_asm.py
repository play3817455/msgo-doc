#!/usr/bin/env python3
"""Merge IDA batch-4 extract + md metadata into schema/cfg/tables/*.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD_DIR = ROOT / "datatables" / "01-列注释"
TABLES_DIR = ROOT / "db_design" / "schema" / "cfg" / "tables"
EXTRACT = ROOT / "db_design" / "schema" / "_meta" / "ida_cfg_batch4_extract.json"
MANIFEST = ROOT / "db_design" / "schema" / "cfg" / "_asm_manifest.json"

BATCH4 = [
    "MISSION_VS", "MISSION_COOP", "MISSION_GROUP", "MISSION_SAFETY_AREA", "MISSION_EXTRULE",
    "MISSION_XWAR_BANPICK", "COMMANDER_NPC", "COMMANDER_SUPPORT", "COMBAT_OPERATION",
    "AI_PARAM", "AI_WEAPON_PARAM", "GACHA", "BYWORD", "QUEST", "BUFF", "DAILY_RECORD",
    "CLAN_CHALLENGE", "TROOP_CHALLENGE", "NETCAFE_CHALLENGE", "CHALLENGE_HIGHSCORE",
    "PLAY_BONUS_REWARD", "BANNER_INFO", "BEGINNER_CHALLENGE", "MONTHLY_BONUS_REWARD",
    "FORCEGAUGE_INFO", "ACTION_MODULE_INFO", "PLAYER_NAVI",
    "SEASON_CLASS_IMFORMATION", "SEASON_CLASS_UP_REWARD", "SEASON_RANKERBATTLE_REWARD",
    "TREND_DATA_WEAPON", "SCORE_CONFIG_CATEGORY", "BGMPACKAGE", "AUTOEXEC",
]

# Skip MSMA_ADOP per user request
SKIP = {"MSMA_ADOP"}

NAME_OVERRIDES: dict[str, dict[int, str]] = {
    "MISSION_GROUP": {0: "group_id", 1: "name", 2: "sort_order", 3: "tag"},
    "MISSION_EXTRULE": {0: "rule_id", 2: "rule_type", 3: "param_a", 4: "param_b", 5: "param_u32", 6: "matrix_u32_0"},
    "MISSION_XWAR_BANPICK": {0: "rule_id", 1: "mode", 2: "pick_count", 3: "ban_ms_id"},
    "MISSION_SAFETY_AREA": {1: "min_x", 2: "min_y", 3: "min_z", 4: "max_x", 5: "max_y", 6: "max_z"},
    "SCORE_CONFIG_CATEGORY": {0: "category_name", 1: "category_index"},
    "BGMPACKAGE": {0: "package_id", 1: "field_bgm_id", 2: "ace_bgm_id", 3: "bgm_path", 4: "force_bgm_enabled", 5: "ace_bgm_enabled", 6: "field_bgm_enabled"},
    "BUFF": {0: "buff_id", 1: "param_u32_1", 2: "name", 7: "buff_category", 8: "param_u32_8", 9: "param_u32_9", 10: "param_u32_10", 11: "param_u32_11"},
    "BYWORD": {0: "byword_id", 1: "param_u32", 2: "text_a", 3: "text_b", 4: "text_c", 5: "text_d", 6: "byword_type"},
    "QUEST": {0: "quest_id", 1: "quest_type", 2: "title", 3: "description", 24: "reward_param"},
    "BEGINNER_CHALLENGE": {0: "challenge_id", 1: "param_1", 2: "param_2", 3: "param_3"},
    "MISSION_VS": {0: "mission_id", 3: "name", 4: "description"},
    "MISSION_COOP": {0: "mission_id", 3: "mission_type"},
    "COMMANDER_NPC": {0: "commander_id", 1: "npc_id"},
    "GACHA": {0: "gacha_id"},
    "AI_PARAM": {0: "ai_param_id"},
    "AI_WEAPON_PARAM": {0: "weapon_param_id"},
    "DAILY_RECORD": {0: "record_id"},
    "CLAN_CHALLENGE": {0: "challenge_id"},
    "TROOP_CHALLENGE": {0: "challenge_id"},
    "NETCAFE_CHALLENGE": {0: "challenge_id"},
    "CHALLENGE_HIGHSCORE": {0: "highscore_id"},
    "PLAY_BONUS_REWARD": {0: "reward_id"},
    "BANNER_INFO": {0: "banner_id"},
    "MONTHLY_BONUS_REWARD": {0: "reward_id"},
    "FORCEGAUGE_INFO": {0: "gauge_id"},
    "ACTION_MODULE_INFO": {0: "module_info_id"},
    "PLAYER_NAVI": {0: "navi_id"},
    "SEASON_CLASS_IMFORMATION": {0: "class_id"},
    "SEASON_CLASS_UP_REWARD": {0: "reward_id"},
    "SEASON_RANKERBATTLE_REWARD": {0: "reward_id"},
    "TREND_DATA_WEAPON": {0: "weapon_trend_id"},
    "COMBAT_OPERATION": {0: "operation_id"},
    "COMMANDER_SUPPORT": {0: "support_id"},
}

TYPE_FROM_IDA = {
    "u32": "u32", "float": "float", "i64": "i64", "str": "str",
    "str_enum": "enum", "enum": "enum", "bool_enum": "bool",
}

VALID_NAME = re.compile(r"^[a-z][a-z0-9_]{0,62}$")


def slug_fallback(table: str, idx: int, typ: str, meaning: str) -> str:
    ov = NAME_OVERRIDES.get(table, {})
    if idx in ov:
        return ov[idx]
    if "主键" in meaning or "索引ID" in meaning:
        return "id" if idx == 0 else f"id_{idx}"
    if "名称" in meaning and typ == "str":
        return "name" if idx <= 3 else f"name_{idx}"
    if "说明" in meaning and typ == "str":
        return "description"
    if typ == "bool":
        return f"flag_bool_{idx}"
    if typ == "enum":
        return f"enum_{idx}"
    if typ == "float":
        return f"param_float_{idx}"
    if typ == "str":
        return f"text_{idx}"
    return f"unknown_{typ}_{idx}"


def upgrade_status(col: dict, has_asm: bool) -> str:
    st = col.get("status", "pending")
    name = col.get("name", "")
    if st == "gap":
        return "gap"
    if st == "confirmed" or (has_asm and name and not name.startswith(("pending_", "field_", "unknown_"))):
        if "★确证" in col.get("confidence", "") or col.get("name") in NAME_OVERRIDES.get(col.get("_table", ""), {}).values():
            return "confirmed"
    if has_asm:
        if st == "pending":
            return "partial"
    return st


def apply_table(table_id: str, extract: dict, manifest: dict) -> dict:
    path = TABLES_DIR / f"{table_id}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if table_id == "AUTOEXEC":
        data["asm_status"] = "complete"
        return data

    ext = extract.get(table_id, {})
    reader = ext.get("reader_func") or manifest.get(table_id, {}).get("reader_func")
    if reader:
        data["asm_reader"] = reader

    by_csv = {c["csv_index"]: c for c in ext.get("columns", [])}
    confirmed = partial = pending = gap = 0

    for col in data.get("columns", []):
        col["_table"] = table_id
        idx = col["csv_index"]
        ida = by_csv.get(idx)
        if ida:
            col["asm_reader"] = reader
            col["asm_va"] = ida.get("asm_va")
            if "memory_offset" in ida:
                col["memory_offset"] = ida["memory_offset"]
            ida_type = TYPE_FROM_IDA.get(ida.get("type", ""), col.get("type", "u32"))
            if ida_type != "u32" or col.get("type") == "u32":
                col["type"] = ida_type

        ov = NAME_OVERRIDES.get(table_id, {})
        if idx in ov:
            col["name"] = ov[idx]
            if "主键" in col.get("meaning", "") or idx == 0:
                col["confidence"] = "★确证"
                col["status"] = "confirmed"
            elif ida:
                col["status"] = "confirmed" if ida.get("type") in ("str", "enum", "float", "bool_enum") else "partial"
        elif col.get("name", "").startswith("pending_"):
            col["name"] = slug_fallback(table_id, idx, col.get("type", "u32"), col.get("meaning", ""))

        has_asm = bool(col.get("asm_va"))
        if col.get("status") not in ("confirmed", "gap"):
            col["status"] = upgrade_status(col, has_asm)

        if col["status"] == "confirmed" and VALID_NAME.match(col["name"]):
            col["db_column"] = col["name"]
        elif not col.get("db_column"):
            col["db_column"] = f"col{idx}"

        st = col["status"]
        if st == "confirmed":
            confirmed += 1
        elif st == "partial":
            partial += 1
        elif st == "gap":
            gap += 1
        else:
            pending += 1
        col.pop("_table", None)

    data["column_confirmed"] = confirmed
    data["column_partial"] = partial
    data["column_pending"] = pending + gap
    data["column_defined"] = len(data["columns"])
    data["asm_status"] = (
        "complete" if pending == 0 and gap == 0 else "partial" if confirmed or partial else "pending"
    )
    return data


def main() -> None:
    extract = json.loads(EXTRACT.read_text(encoding="utf-8"))
    manifest = {t["id"]: t for t in json.loads(MANIFEST.read_text(encoding="utf-8"))["tables"]}

    summary = []
    for tid in BATCH4:
        if tid in SKIP:
            summary.append((tid, "skipped", 0, 0, 0))
            continue
        data = apply_table(tid, extract, manifest)
        path = TABLES_DIR / f"{tid}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary.append((
            tid,
            data.get("asm_status", "?"),
            data.get("column_confirmed", 0),
            data.get("column_partial", 0),
            data.get("column_pending", 0),
        ))
        print(f"{tid}: asm={data['asm_status']} confirmed={data['column_confirmed']} partial={data['column_partial']} pending={data['column_pending']}")

    total_c = sum(s[2] for s in summary if s[1] != "skipped")
    total_p = sum(s[3] for s in summary if s[1] != "skipped")
    complete = sum(1 for s in summary if s[1] == "complete")
    print(f"\nProcessed {len(summary)} tables ({complete} complete), confirmed={total_c} partial={total_p}")


if __name__ == "__main__":
    main()
