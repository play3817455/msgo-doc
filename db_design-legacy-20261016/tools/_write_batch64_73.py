#!/usr/bin/env python3
"""One-shot writer for completion batch #64-73 (remaining 10 tables)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema"
COMP = SCHEMA / "composites"
ENT = SCHEMA / "entities"
TBL = SCHEMA / "_legacy_tables"


def ws(cmd, struct, field, offset, length, wtype, path, reader, printer, va, notes=None):
    d = {
        "command": cmd,
        "struct": struct,
        "field_name": field,
        "offset": offset,
        "length": length,
        "wire_type": wtype,
        "protocol_path": path,
        "section": "§3",
        "reader": reader,
        "printer": printer,
        "evidence_va": va,
    }
    if notes:
        d["notes"] = notes
    return d


def member(name, offset, length, wtype, meaning, disp, sources):
    return {
        "name": name,
        "offset": offset,
        "length": length,
        "wire_type": wtype,
        "meaning": meaning,
        "disposition": disp,
        "wire_sources": sources,
    }


def write(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def entity_from_composite(comp: dict, desc: str, disp: str, wire_forms: list) -> dict:
    return {
        "id": comp["id"],
        "title": comp["id"],
        "description": desc,
        "table_ref": f"tbl_{comp['id']}",
        "disposition": disp,
        "wire_forms": wire_forms,
        "fields": [
            {
                "name": m["name"],
                "offset": m["offset"],
                "length": m["length"],
                "wire_type": m["wire_type"],
                "meaning": m["meaning"],
                "disposition": m["disposition"],
            }
            for m in comp.get("members", [])
        ],
    }


def entity_alias(comp_id: str, desc: str, disp: str, wire_forms: list, canonical: str) -> dict:
    return {
        "id": comp_id,
        "title": comp_id,
        "description": desc,
        "table_ref": f"tbl_{comp_id}",
        "disposition": disp,
        "wire_forms": wire_forms,
        "layout_same_as": canonical,
        "fields": [],
    }


def table_complete(tid, title, purpose, disp, entity, col_name, composite_ref, meaning, sources, cmds):
    return {
        "id": tid,
        "title": title,
        "status": "complete",
        "table_disposition": disp,
        "purpose": purpose,
        "entity_ref": entity,
        "evidence_commands": cmds,
        "column_groups": [{"name": col_name, "columns": [col_name.split("（")[0].strip()]}],
        "columns": [
            {
                "name": col_name.split("（")[0].strip(),
                "disposition": "COMPOSITE",
                "composite_ref": composite_ref,
                "meaning": meaning,
                "wire_sources": sources,
            }
        ],
    }


# --- #64 lvjudge_hist ---
DC47 = "protocol_analysis/commands/SC-0xDC47-lounge-pilot_record_get_r/README.md"
CMD_DC47 = "SC-0xDC47-lounge-pilot_record_get_r"
R_LVH = "sub_B44750"
P_LVH = "sub_B4BE80"
VA_LVH = "B80C7B|B80C8A|B4BE80"

lvjudge_members = [
    member("pilot_id", 0, 4, "u32", "机师 ID", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "pilot_id", 0, 4, "u32", DC47, R_LVH, P_LVH, VA_LVH, "DC47 字段 #8 内；claim 372 / 线 369")]),
    member("lv_history", 4, 96, "u32[24]", "等级历史（24 档）", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "lv_history", 4, 96, "u32[24]", DC47, R_LVH, P_LVH, VA_LVH)]),
    member("lv_history_num", 100, 4, "u32", "等级历史有效条数", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "lv_history_num", 100, 4, "u32", DC47, R_LVH, P_LVH, VA_LVH)]),
    member("lv_history_max", 104, 4, "u32", "等级历史最大条数", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "lv_history_max", 104, 4, "u32", DC47, R_LVH, P_LVH, VA_LVH)]),
    member("xwarwin_history", 108, 48, "u16[24]", "大规模战胜场历史", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "xwarwin_history", 108, 48, "u16[24]", DC47, R_LVH, P_LVH, VA_LVH)]),
    member("xwarlose_history", 156, 48, "u16[24]", "大规模战败场历史", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "xwarlose_history", 156, 48, "u16[24]", DC47, R_LVH, P_LVH, VA_LVH)]),
    member("termstr_now", 204, 65, "u8[65]", "当前赛季串（C 串）", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "termstr_now", 204, 65, "u8[65]", DC47, R_LVH, P_LVH, VA_LVH)]),
    member("term_old", 269, 100, "u32[25]", "历史赛季 ID（25 个）", "PERSIST", [ws(CMD_DC47, "lvjudge_hist", "term_old", 269, 100, "u32[25]", DC47, R_LVH, P_LVH, VA_LVH)]),
]

lvjudge_comp = {
    "id": "lvjudge_hist",
    "title": "等级判定履历 lvjudge_hist（369B 线 / 372B 槽）",
    "length": 369,
    "status": "complete",
    "reader": R_LVH,
    "printer": P_LVH,
    "memory_claim": 372,
    "wire_layout": "u32 + u32[24] + 2×u32 + u16[24] + u16[24] + u8[65] + u32[25]",
    "evidence": {
        "commands": [CMD_DC47],
        "protocol_paths": [DC47],
        "note": "DC47 中 lvjudge_hist=369B 结构体；plvhist 为独立 u16（勿与此表混淆）",
    },
    "members": lvjudge_members,
}
write(COMP / "lvjudge_hist.json", lvjudge_comp)
write(
    ENT / "lvjudge_hist.json",
    entity_from_composite(
        lvjudge_comp,
        "机师等级判定履历；369B 线 / 372B 槽；8 成员（sub_B44750/sub_B4BE80）",
        "PERSIST",
        [{"name": "pilot_record", "length": 369, "memory_claim": 372, "commands": [CMD_DC47], "protocol_path": DC47, "reader": R_LVH, "printer": P_LVH}],
    ),
)
write(
    TBL / "tbl_lvjudge_hist.json",
    table_complete(
        "tbl_lvjudge_hist",
        "等级判定履历",
        "持久化 lvjudge_hist 369B；8 成员（sub_B44750/sub_B4BE80）",
        "PERSIST",
        "lvjudge_hist",
        "lvjudge_hist（369B）",
        "lvjudge_hist",
        "等级判定履历（日志 lvjudge_hist={；claim 372 / 线 369）",
        [
            ws(CMD_DC47, "lvjudge_hist", "lvjudge_hist", 1454, 369, "struct", DC47, R_LVH, P_LVH, "B80C7B|B80F70", "报文字段 #8；成员见 composite lvjudge_hist"),
        ],
        [CMD_DC47],
    ),
)

# --- #65 mprogress alias ---
write(
    COMP / "mprogress.json",
    {
        "id": "mprogress",
        "title": "任务进度 mprogress（= progress 46B/64B）",
        "length": 46,
        "status": "complete",
        "layout_same_as": "progress",
        "reader": "sub_B07880",
        "printer": "sub_B0A820",
        "memory_claim": 64,
        "wire_layout": "同 progress",
        "evidence": {
            "commands": ["SC-0x3E23-battle-game_mission_progress_update"],
            "protocol_paths": ["protocol_analysis/commands/SC-0x3E23-battle-game_mission_progress_update/README.md"],
            "note": "3E23 字段名 mprogress；布局/读取器/打印器同 progress（sub_B07880/sub_B0A820）",
        },
        "members": [],
    },
)
write(
    ENT / "mprogress.json",
    entity_alias(
        "mprogress",
        "战斗任务进度；46B 线 / 64B 槽；同 progress",
        "EVENT",
        [{"name": "mission_progress", "length": 46, "memory_claim": 64, "commands": ["SC-0x3E23-battle-game_mission_progress_update"], "protocol_path": "protocol_analysis/commands/SC-0x3E23-battle-game_mission_progress_update/README.md", "reader": "sub_B07880", "printer": "sub_B0A820"}],
        "progress",
    ),
)
write(
    TBL / "tbl_mprogress.json",
    table_complete(
        "tbl_mprogress",
        "任务进度",
        "持久化 mprogress 46B 线；布局同 progress（sub_B07880/sub_B0A820）",
        "EVENT",
        "mprogress",
        "mprogress（46B · 同 progress）",
        "progress",
        "战斗任务进度（日志 mprogress=；claim 64 / 线 46）",
        [ws("SC-0x3E23-battle-game_mission_progress_update", "mprogress", "mprogress", 0, 46, "struct", "protocol_analysis/commands/SC-0x3E23-battle-game_mission_progress_update/README.md", "sub_B07880", "sub_B0A820", "B14E34|B14ED6", "报文体唯一字段；成员见 composite progress")],
        ["SC-0x3E23-battle-game_mission_progress_update"],
    ),
)

# --- #66 netcafe_challenge_info alias ---
write(
    COMP / "netcafe_challenge_info.json",
    {
        "id": "netcafe_challenge_info",
        "title": "网咖挑战 netcafe_challenge_info（= challenge_info 13B/20B）",
        "length": 13,
        "status": "complete",
        "layout_same_as": "challenge_info",
        "reader": "sub_B07540",
        "printer": "sub_B0A1A0",
        "memory_claim": 60,
        "wire_layout": "同 challenge_info",
        "evidence": {
            "commands": ["SC-0x7626-battle-netcafe_challenge_progress_r"],
            "protocol_paths": ["protocol_analysis/commands/SC-0x7626-battle-netcafe_challenge_progress_r/README.md"],
            "note": "7626 字段名 netcafe_challenge_info；读/打印同 challenge_info；槽 claim 60（sub_B06160）",
        },
        "members": [],
    },
)
write(
    ENT / "netcafe_challenge_info.json",
    entity_alias(
        "netcafe_challenge_info",
        "网咖挑战进度；13B 线 / 60B 槽；同 challenge_info",
        "EVENT",
        [{"name": "netcafe_challenge", "length": 13, "memory_claim": 60, "commands": ["SC-0x7626-battle-netcafe_challenge_progress_r"], "protocol_path": "protocol_analysis/commands/SC-0x7626-battle-netcafe_challenge_progress_r/README.md", "reader": "sub_B07540", "printer": "sub_B0A1A0"}],
        "challenge_info",
    ),
)
write(
    TBL / "tbl_netcafe_challenge_info.json",
    table_complete(
        "tbl_netcafe_challenge_info",
        "网咖挑战进度",
        "EVENT 网咖挑战 netcafe_challenge_info 13B；布局同 challenge_info",
        "EVENT",
        "netcafe_challenge_info",
        "netcafe_challenge_info（13B · 同 challenge_info）",
        "challenge_info",
        "网咖挑战进度（日志 netcafe_challenge_info={；claim 60 / 线 13）",
        [ws("SC-0x7626-battle-netcafe_challenge_progress_r", "netcafe_challenge_info", "netcafe_challenge_info", 0, 13, "struct", "protocol_analysis/commands/SC-0x7626-battle-netcafe_challenge_progress_r/README.md", "sub_B07540", "sub_B0A1A0", "B1FEB6|B0A1A0", "成员见 composite challenge_info")],
        ["SC-0x7626-battle-netcafe_challenge_progress_r"],
    ),
)

# --- #67 unlocked_navi ---
A0BB = "protocol_analysis/commands/SC-0xA0BB-lounge-player_navi_unlock_r/README.md"
CMD_A0BB = "SC-0xA0BB-lounge-player_navi_unlock_r"
unlocked_comp = {
    "id": "unlocked_navi",
    "title": "解锁导航 unlocked_navi（8B）",
    "length": 8,
    "status": "complete",
    "reader": "sub_B434B0",
    "printer": "sub_B49C80",
    "memory_claim": 8,
    "wire_layout": "2×u32",
    "evidence": {"commands": [CMD_A0BB], "protocol_paths": [A0BB], "note": "claim == 线长 == 8"},
    "members": [
        member("navi_id", 0, 4, "u32", "导航 ID", "PERSIST", [ws(CMD_A0BB, "unlocked_navi", "navi_id", 0, 4, "u32", A0BB, "sub_B434B0", "sub_B49C80", "B6F615|B6F6E7")]),
        member("status", 4, 4, "u32", "解锁状态", "PERSIST", [ws(CMD_A0BB, "unlocked_navi", "status", 4, 4, "u32", A0BB, "sub_B434B0", "sub_B49C80", "B6F615|B6F6E7")]),
    ],
}
write(COMP / "unlocked_navi.json", unlocked_comp)
write(ENT / "unlocked_navi.json", entity_from_composite(unlocked_comp, "玩家导航解锁；8B；2 成员", "PERSIST", [{"name": "unlock_r", "length": 8, "commands": [CMD_A0BB], "protocol_path": A0BB}]))
write(
    TBL / "tbl_unlocked_navi.json",
    table_complete(
        "tbl_unlocked_navi",
        "解锁导航",
        "持久化 unlocked_navi 8B；navi_id + status",
        "PERSIST",
        "unlocked_navi",
        "unlocked_navi（8B）",
        "unlocked_navi",
        "解锁的导航信息（日志 unlocked_navi=）",
        [ws(CMD_A0BB, "unlocked_navi", "unlocked_navi", 4, 8, "struct", A0BB, "sub_B434B0", "sub_B49C80", "B6F615|B6F6E7", "报文字段 #2")],
        [CMD_A0BB],
    ),
)

# --- #68 pointdmg ---
D5E6 = "protocol_analysis/commands/SC-0xD5E6-lounge-result_info/README.md"
CMD_D5E6 = "SC-0xD5E6-lounge-result_info"
pointdmg_comp = {
    "id": "pointdmg",
    "title": "点位伤害 pointdmg（12B 线 / 24B 槽）",
    "length": 12,
    "status": "complete",
    "reader": "sub_B45760",
    "printer": "sub_B4DEE0",
    "memory_claim": 24,
    "wire_layout": "u32[3]",
    "evidence": {"commands": [CMD_D5E6], "protocol_paths": [D5E6], "note": "gaugedmg 固定 3 元 u32；sub_B45760 内 cmp …,3"},
    "members": [
        member(
            "gaugedmg",
            0,
            12,
            "u32[3]",
            "量表伤害（3 点）",
            "EVENT",
            [ws(CMD_D5E6, "pointdmg", "gaugedmg", 0, 12, "u32[3]", D5E6, "sub_B45760", "sub_B4DEE0", "B7DE8D|B7E44B", "claim 24 / 线 12；D5E6 可变偏移")],
        ),
    ],
}
write(COMP / "pointdmg.json", pointdmg_comp)
write(ENT / "pointdmg.json", entity_from_composite(pointdmg_comp, "结算点位伤害；12B 线 / 24B 槽", "EVENT", [{"name": "result_info", "length": 12, "memory_claim": 24, "commands": [CMD_D5E6], "protocol_path": D5E6}]))
write(
    TBL / "tbl_pointdmg.json",
    table_complete(
        "tbl_pointdmg",
        "点位伤害",
        "EVENT pointdmg 12B；gaugedmg u32[3]",
        "EVENT",
        "pointdmg",
        "pointdmg（12B）",
        "pointdmg",
        "结算点位伤害（日志 pointdmg= / gaugedmg={；claim 24 / 线 12）",
        [ws(CMD_D5E6, "pointdmg", "pointdmg", None, 12, "struct", D5E6, "sub_B45760", "sub_B4DEE0", "B7DE8D|B7E44B", "D5E6 字段 #21；可变偏移")],
        [CMD_D5E6],
    ),
)

# --- #69 total_result_wave ---
trw_comp = {
    "id": "total_result_wave",
    "title": "波次汇总 total_result_wave（19B 线 / 20B 槽）",
    "length": 19,
    "status": "complete",
    "reader": "sub_B45580",
    "printer": "sub_B4DCC0",
    "memory_claim": 20,
    "wire_layout": "3×u8 + 4×u32（rank 后 1B 槽 padding）",
    "evidence": {"commands": [CMD_D5E6], "protocol_paths": [D5E6], "note": "D5E6 日志串 totalresult_wave="},
    "members": [
        member("end_wave", 0, 1, "u8", "结束波次", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "end_wave", 0, 1, "u8", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251")]),
        member("result_coop", 1, 1, "u8", "协作结果", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "result_coop", 1, 1, "u8", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251")]),
        member("rank", 2, 1, "u8", "排名", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "rank", 2, 1, "u8", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251")]),
        member("rank_score", 3, 4, "u32", "排名分", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "rank_score", 3, 4, "u32", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251", "内存 offset +4（+3 为 padding）")]),
        member("container_comp", 7, 4, "u32", "集装箱完成", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "container_comp", 7, 4, "u32", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251")]),
        member("enemyobj_comp", 11, 4, "u32", "敌方目标完成", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "enemyobj_comp", 11, 4, "u32", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251")]),
        member("total_score", 15, 4, "u32", "总分", "EVENT", [ws(CMD_D5E6, "totalresult_wave", "total_score", 15, 4, "u32", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251")]),
    ],
}
write(COMP / "total_result_wave.json", trw_comp)
write(ENT / "total_result_wave.json", entity_from_composite(trw_comp, "结算波次汇总；19B 线 / 20B 槽；7 成员", "EVENT", [{"name": "result_info", "length": 19, "memory_claim": 20, "commands": [CMD_D5E6], "protocol_path": D5E6}]))
write(
    TBL / "tbl_total_result_wave.json",
    table_complete(
        "tbl_total_result_wave",
        "波次汇总",
        "EVENT total_result_wave 19B；7 成员",
        "EVENT",
        "total_result_wave",
        "total_result_wave（19B）",
        "total_result_wave",
        "结算波次汇总（日志 totalresult_wave=；claim 20 / 线 19）",
        [ws(CMD_D5E6, "totalresult_wave", "totalresult_wave", None, 19, "struct", D5E6, "sub_B45580", "sub_B4DCC0", "B7DCB4|B7E251", "D5E6 字段 #12；可变偏移")],
        [CMD_D5E6],
    ),
)

# --- #70 recruit ---
CMD_305D = "SC-0x305D-lounge-party_recruit_detail_get_r"
P305D = "protocol_analysis/commands/SC-0x305D-lounge-party_recruit_detail_get_r/README.md"
R_REC = "sub_B45400"
P_REC = "sub_B4D840"
VA_REC = "B5ADA5|B4D840"
recruit_fields = [
    ("channel_id", 0, 4, "u32", "频道 ID"),
    ("party_id", 4, 4, "u32", "队伍 ID"),
    ("troops", 8, 1, "i8", "势力"),
    ("member_count", 9, 2, "u16", "队伍人数"),
    ("comment", 11, 61, "bytes[61]", "招募留言（定长 61B）"),
    ("pstat", 72, 1, "i8", "队伍状态"),
    ("is_lock", 73, 1, "i8", "是否上锁"),
]
recruit_members = [
    member(n, o, l, t, m, "PERSIST", [ws(CMD_305D, "recruit", n, o, l, t, P305D, R_REC, P_REC, VA_REC, "74B 线 / 84B 槽；≠ recruits 80B")])
    for n, o, l, t, m in recruit_fields
]
recruit_comp = {
    "id": "recruit",
    "title": "招募详情 recruit（74B 线 / 84B 槽）",
    "length": 74,
    "status": "complete",
    "reader": R_REC,
    "printer": P_REC,
    "memory_claim": 84,
    "wire_layout": "2×u32 + i8 + u16 + bytes[61] + 2×i8",
    "evidence": {"commands": [CMD_305D], "protocol_paths": [P305D], "note": "305D 单条 recruit；recruits（B43F）为 80B 列表元素"},
    "members": recruit_members,
}
write(COMP / "recruit.json", recruit_comp)
write(ENT / "recruit.json", entity_from_composite(recruit_comp, "队伍招募详情；74B 线 / 84B 槽；7 成员", "PERSIST", [{"name": "recruit_detail", "length": 74, "memory_claim": 84, "commands": [CMD_305D], "protocol_path": P305D}]))
write(
    TBL / "tbl_recruit.json",
    table_complete(
        "tbl_recruit",
        "招募详情",
        "持久化 recruit 74B；7 成员（sub_B45400/sub_B4D840）",
        "PERSIST",
        "recruit",
        "recruit（74B）",
        "recruit",
        "招募信息（日志 recruit=；74B 线 / 84B 槽）",
        [ws(CMD_305D, "recruit", "recruit", 4, 74, "struct", P305D, R_REC, P_REC, VA_REC, "报文字段 #2（offset 4 起）")],
        [CMD_305D],
    ),
)

# --- #71 replay_info ---
A148 = "protocol_analysis/commands/SC-0xA148-lounge-season_rankerbattle_replay_info/README.md"
CMD_A148 = "SC-0xA148-lounge-season_rankerbattle_replay_info"
R_REP = "sub_B47340"
P_REP = "sub_B513F0"
VA_REP = "B6F946|B6FA42"
replay_members = [
    member("id", 0, 8, "u64", "录像 ID", "PERSIST", [ws(CMD_A148, "replay_info", "id", 0, 8, "u64", A148, R_REP, P_REP, VA_REP)]),
    member("missionId", 8, 4, "u32", "任务 ID", "PERSIST", [ws(CMD_A148, "replay_info", "missionId", 8, 4, "u32", A148, R_REP, P_REP, VA_REP)]),
    member("time", 12, 4, "u32", "时间戳", "PERSIST", [ws(CMD_A148, "replay_info", "time", 12, 4, "u32", A148, R_REP, P_REP, VA_REP)]),
    member("troopsA", 16, 1, "u8", "A 方势力", "PERSIST", [ws(CMD_A148, "replay_info", "troopsA", 16, 1, "u8", A148, R_REP, P_REP, VA_REP)]),
    member("troopsB", 17, 1, "u8", "B 方势力", "PERSIST", [ws(CMD_A148, "replay_info", "troopsB", 17, 1, "u8", A148, R_REP, P_REP, VA_REP)]),
    member("endDate", 18, 4, "u32", "结束日期", "PERSIST", [ws(CMD_A148, "replay_info", "endDate", 18, 4, "u32", A148, R_REP, P_REP, VA_REP, "内存 +20（u8×2 后 padding）")]),
    member("top_pilot_id_troopsA", 22, 4, "u32", "A 方最高分机师 ID", "PERSIST", [ws(CMD_A148, "replay_info", "top_pilot_id_troopsA", 22, 4, "u32", A148, R_REP, P_REP, VA_REP)]),
    member("top_world_id_troopsA", 26, 4, "u32", "A 方最高分世界 ID", "PERSIST", [ws(CMD_A148, "replay_info", "top_world_id_troopsA", 26, 4, "u32", A148, R_REP, P_REP, VA_REP)]),
    member("top_pilot_id_troopsB", 30, 4, "u32", "B 方最高分机师 ID", "PERSIST", [ws(CMD_A148, "replay_info", "top_pilot_id_troopsB", 30, 4, "u32", A148, R_REP, P_REP, VA_REP)]),
    member("top_world_id_troopsB", 34, 4, "u32", "B 方最高分世界 ID", "PERSIST", [ws(CMD_A148, "replay_info", "top_world_id_troopsB", 34, 4, "u32", A148, R_REP, P_REP, VA_REP)]),
]
replay_comp = {
    "id": "replay_info",
    "title": "录像信息 replay_info（38B 线 / 40B 槽）",
    "length": 38,
    "status": "complete",
    "reader": R_REP,
    "printer": P_REP,
    "memory_claim": 40,
    "wire_layout": "u64 + 2×u32 + 2×u8 + 5×u32",
    "evidence": {"commands": [CMD_A148], "protocol_paths": [A148], "note": "claim 40（sub_B418C0 +0x28）/ 线 38"},
    "members": replay_members,
}
write(COMP / "replay_info.json", replay_comp)
write(ENT / "replay_info.json", entity_from_composite(replay_comp, "赛季排位战录像；38B 线 / 40B 槽；10 成员", "PERSIST", [{"name": "replay", "length": 38, "memory_claim": 40, "commands": [CMD_A148], "protocol_path": A148}]))
write(
    TBL / "tbl_replay_info.json",
    table_complete(
        "tbl_replay_info",
        "录像信息",
        "持久化 replay_info 38B；10 成员（sub_B47340/sub_B513F0）",
        "PERSIST",
        "replay_info",
        "replay_info（38B）",
        "replay_info",
        "赛季排位战录像信息（日志 replay_info=；claim 40 / 线 38）",
        [ws(CMD_A148, "replay_info", "replay_info", 0, 38, "struct", A148, R_REP, P_REP, VA_REP, "A148 字段 #1")],
        [CMD_A148],
    ),
)

# --- #72 season_rb_conf ---
CMD_63D3 = "SC-0x63D3-lounge-season_rankerbattle_config_update"
P63D3 = "protocol_analysis/commands/SC-0x63D3-lounge-season_rankerbattle_config_update/README.md"
R_SRB = "sub_B471E0"
P_SRB = "sub_B51120"
VA_SRB = "B64CA5|B64D92"
season_fields = [
    ("state", 0, "赛季状态"),
    ("tournament_id", 4, "锦标赛 ID"),
    ("mode", 8, "模式"),
    ("open_date", 12, "开放日期"),
    ("booking_start", 16, "预约开始"),
    ("booking_end", 20, "预约结束"),
    ("mission_id", 24, "任务 ID"),
]
season_members = [
    member(n, o, 4, "u32", m, "PERSIST", [ws(CMD_63D3, "season_rb_conf", n, o, 4, "u32", P63D3, R_SRB, P_SRB, VA_SRB, "52B 线 / 56B 槽")])
    for n, o, m in season_fields
]
season_members.append(
    member(
        "mission_id_dm",
        28,
        16,
        "u32[4]",
        "死亡竞赛任务 ID（4 元）",
        "PERSIST",
        [ws(CMD_63D3, "season_rb_conf", "mission_id_dm", 28, 16, "u32[4]", P63D3, R_SRB, P_SRB, VA_SRB, "打印器 mission_id_dm={ + 3 元")],
    )
)
season_members.extend(
    [
        member("is_end", 44, 4, "u32", "是否已结束", "PERSIST", [ws(CMD_63D3, "season_rb_conf", "is_end", 44, 4, "u32", P63D3, R_SRB, P_SRB, VA_SRB)]),
        member("is_debug", 48, 4, "u32", "调试标志", "PERSIST", [ws(CMD_63D3, "season_rb_conf", "is_debug", 48, 4, "u32", P63D3, R_SRB, P_SRB, VA_SRB)]),
    ]
)
season_comp = {
    "id": "season_rb_conf",
    "title": "赛季排位战配置 season_rb_conf（52B 线 / 56B 槽）",
    "length": 52,
    "status": "complete",
    "reader": R_SRB,
    "printer": P_SRB,
    "memory_claim": 56,
    "wire_layout": "7×u32 + u32[4] + 2×u32",
    "evidence": {
        "commands": [CMD_63D3],
        "protocol_paths": [P63D3],
        "note": "63D3 含 season_rb_conf + season_rb_conf_next（各 52B）；打印器 sub_B51120",
    },
    "members": season_members,
}
write(COMP / "season_rb_conf.json", season_comp)
write(ENT / "season_rb_conf.json", entity_from_composite(season_comp, "赛季排位战配置；52B 线 / 56B 槽；13 成员", "PERSIST", [{"name": "config_update", "length": 52, "memory_claim": 56, "commands": [CMD_63D3], "protocol_path": P63D3}]))
write(
    TBL / "tbl_season_rb_conf.json",
    table_complete(
        "tbl_season_rb_conf",
        "赛季排位战配置",
        "持久化 season_rb_conf 52B；13 成员（sub_B471E0/sub_B51120）",
        "PERSIST",
        "season_rb_conf",
        "season_rb_conf（52B）",
        "season_rb_conf",
        "当期赛季排位战配置（日志 season_rb_conf=；claim 56 / 线 52）",
        [ws(CMD_63D3, "season_rb_conf", "season_rb_conf", 0, 52, "struct", P63D3, R_SRB, P_SRB, VA_SRB, "63D3 字段 #1")],
        [CMD_63D3],
    ),
)

# --- #73 precord ---
PRECORD_FIELDS = [
    ("rec_point", 0, "记录点/总积分"),
    ("kill_cnt", 4, "击杀数"),
    ("kill_wrestle_cnt", 8, "格斗击杀数"),
    ("kill_shot_cnt", 12, "射击击杀数"),
    ("kill_cannon_cnt", 16, "炮击击杀数"),
    ("kill_throw_cnt", 20, "投掷击杀数"),
    ("kill_deparms_cnt", 24, "缴械击杀数"),
    ("kill_assist_cnt", 28, "助攻数"),
    ("mapobj_killcnt", 32, "地图目标破坏数"),
    ("battery_killcnt", 36, "炮台击破数"),
    ("stronghold_killcnt", 40, "据点压制数"),
    ("death_cnt", 44, "死亡数"),
    ("search_cnt", 48, "索敌数"),
    ("resurrect_cnt", 52, "复活数"),
    ("respawn_defeat_cnt", 56, "再出击(败)数"),
    ("respawn_conquer_cnt", 60, "再出击(胜)数"),
    ("container_cnt", 64, "集装箱数"),
    ("protect_cnt", 68, "护卫数"),
    ("stgarms_set_cnt", 72, "据点兵器设置数"),
    ("odrcomp_pl_cnt", 76, "指令完成数"),
    ("move_length", 80, "移动距离"),
    ("stgarms_move_length", 84, "据点兵器移动距离"),
    ("repair_armor", 88, "修理装甲量"),
    ("stghold_damage", 92, "据点守备伤害"),
    ("btlship_damage", 96, "战舰伤害"),
    ("tender_damage", 100, "补给舰伤害"),
    ("ace_damage", 104, "王牌伤害"),
    ("result_gold", 108, "黄金奖牌数"),
    ("result_gold_score", 112, "黄金奖牌分"),
    ("result_gold_rank", 116, "黄金奖牌排名"),
    ("result_gold_dss", 120, "黄金奖牌 DSS"),
    ("result_gold_conquer", 124, "黄金奖牌征服"),
    ("score_atk", 128, "评分·攻击"),
    ("score_spt", 132, "评分·支援"),
    ("score_con", 136, "评分·指挥"),
    ("score_total", 140, "评分·合计"),
    ("score_atk_max", 144, "最高分·攻击"),
    ("score_spt_max", 148, "最高分·支援"),
    ("score_con_max", 152, "最高分·指挥"),
    ("vsl_kill_cnt", 156, "对战击杀数"),
    ("vsl_kill_wrestle_cnt", 160, "对战格斗击杀"),
    ("vsl_kill_shot_cnt", 164, "对战射击击杀"),
    ("vsl_kill_cannon_cnt", 168, "对战炮击击杀"),
    ("vsl_kill_throw_cnt", 172, "对战投掷击杀"),
    ("vsl_kill_deparms_cnt", 176, "对战缴械击杀"),
    ("vsl_kill_assist_cnt", 180, "对战助攻数"),
    ("vsl_death_cnt", 184, "对战死亡数"),
    ("vsl_search_cnt", 188, "对战索敌数"),
    ("vsl_repair_armor", 192, "对战修理量"),
    ("vsl_resurrect_cnt", 196, "对战复活数"),
    ("vsl_td_kill_cnt", 200, "对战塔防击杀"),
    ("vsl_td_death_cnt", 204, "对战塔防死亡"),
    ("vsl_td_score_best", 208, "对战塔防最高分", "u16", 2),
    ("vsl_td_score_total", 210, "对战塔防总分"),
    ("dc_victory", 214, "断线胜利数"),
    ("dc_kill_cnt", 218, "断线击杀数"),
    ("dc_death_cnt", 222, "断线死亡数"),
    ("ms_develop_cnt", 226, "机体开发数"),
    ("ms_buildup_cnt", 230, "机体强化数"),
    ("weapon_unlock_cnt", 234, "武器解锁数"),
    ("weapon_buildup_cnt", 238, "武器强化数"),
]
R_PRE = "sub_B440B0"
P_PRE = "sub_B4B240"
VA_PRE = "B80B8D|B80E08|B4B240"
precord_members = []
for item in PRECORD_FIELDS:
    if len(item) == 5:
        name, off, meaning, wtype, length = item
    else:
        name, off, meaning = item
        wtype, length = "u32", 4
    precord_members.append(
        member(
            name,
            off,
            length,
            wtype,
            meaning,
            "PERSIST",
            [
                ws(
                    CMD_DC47,
                    "precord",
                    name,
                    off,
                    length,
                    wtype,
                    DC47,
                    R_PRE,
                    P_PRE,
                    VA_PRE,
                    "242B 线 / 252B 槽；vsl_td_score_best 为唯一 u16",
                )
            ],
        )
    )
precord_comp = {
    "id": "precord",
    "title": "机师战绩 precord（242B 线 / 252B 槽）",
    "length": 242,
    "status": "complete",
    "reader": R_PRE,
    "printer": P_PRE,
    "memory_claim": 252,
    "wire_layout": "60×u32 + u16（vsl_td_score_best @208）",
    "evidence": {
        "commands": [CMD_DC47],
        "protocol_paths": [DC47],
        "note": "61 字段名 sub_B4B240；u16 后线偏移 = 内存偏移 − 2",
    },
    "members": precord_members,
}
write(COMP / "precord.json", precord_comp)
write(ENT / "precord.json", entity_from_composite(precord_comp, "机师战绩；242B 线 / 252B 槽；61 成员", "PERSIST", [{"name": "pilot_record", "length": 242, "memory_claim": 252, "commands": [CMD_DC47], "protocol_path": DC47}]))
write(
    TBL / "tbl_precord.json",
    table_complete(
        "tbl_precord",
        "机师战绩",
        "持久化 precord 242B；61 成员（sub_B440B0/sub_B4B240）",
        "PERSIST",
        "precord",
        "precord（242B）",
        "precord",
        "机师战绩记录（日志 precord=；claim 252 / 线 242）",
        [ws(CMD_DC47, "precord", "precord", 12, 242, "struct", DC47, R_PRE, P_PRE, VA_PRE, "DC47 字段 #4；成员见 composite precord")],
        [CMD_DC47],
    ),
)

# --- completion_queue + 进度.md ---
queue = {
    "rule": "每张表补全（composite 成员无 TBD、disposition 已定、wire_sources 齐全）后才开下一张",
    "updated": "2026-09-20",
    "completed": json.loads((SCHEMA / "_meta" / "completion_queue.json").read_text(encoding="utf-8"))["completed"]
    + [
        {"id": "tbl_lvjudge_hist", "notes": "8 成员 369B/372B"},
        {"id": "tbl_mprogress", "notes": "同 progress 46B alias"},
        {"id": "tbl_netcafe_challenge_info", "notes": "同 challenge_info 13B alias"},
        {"id": "tbl_unlocked_navi", "notes": "2 成员 8B"},
        {"id": "tbl_pointdmg", "notes": "gaugedmg u32[3] 12B/24B"},
        {"id": "tbl_total_result_wave", "notes": "7 成员 19B/20B"},
        {"id": "tbl_recruit", "notes": "7 成员 74B/84B"},
        {"id": "tbl_replay_info", "notes": "10 成员 38B/40B"},
        {"id": "tbl_season_rb_conf", "notes": "13 成员 52B/56B"},
        {"id": "tbl_precord", "notes": "61 成员 242B/252B"},
    ],
    "in_progress": None,
    "next": None,
    "pending_priority": [],
    "skipped": [
        {"id": "term_str", "reason": "非 73 struct 表；协议字段（NUL 串）已在 B985/C5A9/1CF0 命令 README 记录"}
    ],
}
write(SCHEMA / "_meta" / "completion_queue.json", queue)

progress_tail = """| ✅ | `tbl_lvjudge_hist` | 8 成员 369B/372B |
| ✅ | `tbl_mprogress` | 同 progress 46B alias |
| ✅ | `tbl_netcafe_challenge_info` | 同 challenge_info 13B alias |
| ✅ | `tbl_unlocked_navi` | 2 成员 8B |
| ✅ | `tbl_pointdmg` | gaugedmg u32[3] 12B/24B |
| ✅ | `tbl_total_result_wave` | 7 成员 19B/20B |
| ✅ | `tbl_recruit` | 7 成员 74B/84B |
| ✅ | `tbl_replay_info` | 10 成员 38B/40B |
| ✅ | `tbl_season_rb_conf` | 13 成员 52B/56B |
| ✅ | `tbl_precord` | 61 成员 242B/252B |

**已完成 73 / 73**
"""
prog_path = SCHEMA / "_meta" / "进度.md"
prog_text = prog_path.read_text(encoding="utf-8")
import re

prog_text = re.sub(
    r"\| ⏳ \| 其余 10 表 \| 待排队 \|\n\n\*\*已完成 63 / 73\*\*",
    progress_tail.strip(),
    prog_text,
)
prog_path.write_text(prog_text, encoding="utf-8")

print("Wrote batch #64-73 (10 tables). 73/73 complete.")
