#!/usr/bin/env python3
"""Enrich 21 cfg table schemas + datatables MD to AI_WEAPON_PARAM quality."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "db_design" / "schema" / "cfg" / "tables"
ENUMS = json.loads((ROOT / "reverse-login-chain" / "formats" / "enums.json").read_text(encoding="utf-8"))
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

TABLE_IDS = [
    "MISSION_GROUP", "MISSION_COOP", "MISSION_VS", "MISSION_EXTRULE", "MISSION_SAFETY_AREA",
    "MISSION_XWAR_BANPICK", "COMMANDER_NPC", "COMMANDER_SUPPORT", "COMBAT_OPERATION", "QUEST",
    "ITEM", "ITEM_PART", "ITEM_USE", "ITEM_TOKEN", "ITEMPACK_INFO", "GACHA",
    "MODULE", "MODULE_DEVELOP", "MODULE_RENTAL", "MODULE_BONUS", "MODULE_BONUS_LOT",
]


def enum_table(fn: str) -> list[dict] | None:
    r = ENUMS.get(fn)
    if not r:
        return None
    if r.get("shape") == "table" and r.get("table"):
        return [{"name": n, "value": v} for n, v in r["table"]]
    lits, consts = r.get("lits") or [], r.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    if lits:
        return [{"name": n, "value": i} for i, n in enumerate(lits)]
    return None


def apply_col(c: dict, **kw) -> None:
    for k, v in kw.items():
        if v is not None:
            c[k] = v
    if kw.get("status") == "confirmed":
        c["confidence"] = kw.get("confidence") or "★确证"
    c["display_name"] = kw.get("display_name") or kw.get("meaning") or c.get("display_name", "")


def recount(data: dict) -> None:
    cols = data.get("columns", [])
    confirmed = partial = pending = gap = 0
    for c in cols:
        st = c.get("status", "")
        if st == "confirmed":
            confirmed += 1
        elif st == "partial":
            partial += 1
        elif st == "gap":
            gap += 1
        else:
            pending += 1
    data["column_defined"] = len(cols)
    data["column_confirmed"] = confirmed
    data["column_partial"] = partial
    data["column_pending"] = pending
    data["column_gap"] = gap


def col_by(data: dict, **keys) -> dict | None:
    for c in data["columns"]:
        if all(c.get(k) == v for k, v in keys.items()):
            return c
    return None


def patch_enum(c: dict, fn: str, values: list[dict] | None = None) -> None:
    c["enum_converter"] = fn
    c["enum_doc"] = ENUM_DOC
    c["enum_values"] = values or enum_table(fn) or c.get("enum_values")


# --- shared enum blocks ---
FACTION = [{"name": "NEUTRAL", "value": -1}, {"name": "EFF", "value": 0}, {"name": "ZEON", "value": 1}]
SUPPORT_TYPE = [
    {"name": "BOMB", "value": 0}, {"name": "CARPET_BOMB", "value": 1}, {"name": "TENDER", "value": 2},
    {"name": "SEARCH", "value": 3}, {"name": "MINOVSKY", "value": 4}, {"name": "SOLAR_RAY", "value": 5},
    {"name": "SUMMON_MA", "value": 6}, {"name": "SUMMON_ACE", "value": 7}, {"name": "BATTLE_SHIP", "value": 8},
    {"name": "ASSAULT_SHIP", "value": 9}, {"name": "ORATION", "value": 10}, {"name": "PATROL_AIRCRAFT", "value": 11},
    {"name": "AAG", "value": 12}, {"name": "GUNTURRET", "value": 13}, {"name": "EQPARTS_EXEC_A", "value": 14},
    {"name": "EQPARTS_EXEC_B", "value": 15}, {"name": "EQPARTS_EXEC_C", "value": 16}, {"name": "EQPARTS_EXEC_D", "value": 17},
    {"name": "EQPARTS_EXEC_E", "value": 18}, {"name": "GRENADE_NET", "value": 19}, {"name": "GRENADE_TUMBLE", "value": 20},
    {"name": "WALL", "value": 21}, {"name": "DUMMY_BEACON", "value": 22}, {"name": "TRANSPORT_SHIP", "value": 23},
    {"name": "STGARMS_OLD", "value": 24}, {"name": "STGARMS1", "value": 25}, {"name": "STGARMS2", "value": 26},
    {"name": "SUBFLIGHT", "value": 27}, {"name": "ASSAULT_STGHOLD", "value": 28}, {"name": "RIDE_ACE", "value": 29},
    {"name": "JAMMING", "value": 30},
]
VS_MODE = [
    {"name": "VS_TEAM_DEATHMATCH", "value": 0}, {"name": "VS_DOMINATION", "value": 1},
    {"name": "VS_CORE_DESTROY", "value": 2}, {"name": "VS_DEMOLITION", "value": 3},
    {"name": "VS_HEADQUARTERS", "value": 4}, {"name": "VS_MARCH", "value": 5},
]
VS_SUBMODE = [
    {"name": "RPOST_DIFF", "value": 0}, {"name": "DOT_DMG", "value": 1}, {"name": "BATTLEAREA", "value": 2},
    {"name": "HEADQUARTERS", "value": 3}, {"name": "CONQUEST", "value": 4},
]
GACHA_POOL = [{"name": "NORMAL", "value": 0}, {"name": "SINGLE", "value": 1}, {"name": "SINGLE_NORESET", "value": 2}]
TOKEN_TYPE = [{"name": "MSMA_STORAGE", "value": 1}, {"name": "MSMA_DECKCOST", "value": 2}]
MODULE_CAT = enum_table("sub_5A2CC0") or []


def enrich_mission_group(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), name="group_id", db_column="group_id",
              meaning="主键；CMissionGroupTable 索引键（sub_59E830 按 group_id 查行）", status="confirmed", memory_offset=0)
    apply_col(col_by(d, csv_index=1), name="group_name", db_column="group_name",
              meaning="分组显示名（wstring @+4；任务列表 UI 归类标签）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=2), name="sort_order", db_column="sort_order",
              meaning="列表排序权重（u32；sub_59E8A0 col2→v12，越大越靠前）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=3), name="group_tag", db_column="group_tag",
              meaning="分组内部 tag（wstring；sub_4318B0 匹配后置关联任务 byte+100=1）", status="confirmed", memory_offset=12)


def enrich_mission_coop(d: dict) -> None:
    patches = {
        0: ("mission_id", "主键；协作战任务 ID（与 AI 脚本 mission id 对应）", 4),
        1: ("map_id", "地图 ID（u32 @+8；关联 map 资源）", 8),
        2: ("thumbnail_id", "缩略图/图标 ID（u32 @+40）", 40),
        3: ("faction", "势力限制：EFF/ZEON（sub_40CE20 @+80；空=不限）", 80),
        4: ("rule_param", "规则参数 u32（@+84；col49=1 时强制写入 256）", 84),
        5: ("min_players", "最少玩家数（u32 @+44）", 44),
        6: ("flag_ranked", "排位战标志（bool bit0 @+56）", 56),  # csv6
        7: ("flag_private", "私人房间标志（bool bit1 @+56）", 56),
        8: ("flag_clan", "部队战标志（bool bit2 @+56）", 56),
        9: ("coop_mode", "协作模式：COOP_CORE_DESTROY/COOP_WAVE（enum @+48）", 48),
        10: ("coop_subtype", "子模式：BASE_DEFENSE/TIME_ATTACK（enum @+52）", 52),
        11: ("script_bundle_id", "脚本资源包 ID（u32 @+200；sub_744680 查关联）", 200),
        12: ("mission_name", "任务名称（wstring @+88）", 88),
        13: ("recommended_rank", "推荐等级/军衔（u16 @+208）", 208),
        14: ("min_rank", "最低等级（u16 @+58）", 58),
        15: ("max_rank", "最高等级（u16 @+60）", 60),
        16: ("time_limit_sec", "时间限制秒（u32 @+68）", 68),
        19: ("respawn_limit", "重生次数上限（u16 @+72）", 72),
        37: ("briefing_text", "任务简报文本（wstring col37 @+116）", 116),
        38: ("objective_text", "目标说明文本（wstring col38 @+144）", 144),
        39: ("result_text", "结算说明文本（wstring col39 @+172）", 172),
        47: ("flag_tutorial", "教程任务标志（bool @+204）", 204),
        48: ("flag_event", "活动任务标志（bool @+205）", 205),
        49: ("flag_force_rule256", "强制规则 256 标志（bool @+206→col4=256）", 206),
        52: ("flag_allow_spectate", "允许观战标志（bool @+210；需 col47=1）", 210),
    }
    for idx, (name, meaning, off) in patches.items():
        c = col_by(d, csv_index=idx)
        if not c:
            continue
        kw = dict(name=name, db_column=name, meaning=meaning, status="confirmed", memory_offset=off)
        if idx == 3:
            kw["type"] = "enum"
            kw["enum_converter"] = "sub_40CE20"
            kw["enum_values"] = [{"name": "EFF", "value": 0}, {"name": "ZEON", "value": 1}]
        if idx in (9, 10):
            kw["type"] = "enum"
            if idx == 9:
                kw["enum_values"] = [
                    {"name": "COOP_CORE_DESTROY", "value": 11},
                    {"name": "COOP_WAVE", "value": 12},
                    {"name": "COOP_WAVE_ALT", "value": 10},
                ]
            else:
                kw["enum_values"] = [
                    {"name": "BASE_DEFENSE", "value": 1},
                    {"name": "TIME_ATTACK", "value": 0},
                    {"name": "TIME_ATTACK_ALT", "value": 2},
                ]
        if idx in (6, 7, 8, 47, 48, 49, 52):
            kw["type"] = "bool"
        elif idx == 5:
            kw["type"] = "u32"
        apply_col(c, **kw)


def enrich_mission_vs(d: dict) -> None:
    patches = {
        0: ("mission_id", "主键；对战任务 ID（= AI 脚本 8 位 id，sub_629120 查表）", 4),
        1: ("map_id", "地图 ID（u32 @+8）", 8),
        2: ("mode_param", "模式参数 u32（@+40）", 40),
        3: ("mission_name", "任务名称（wstring @+12）", 12),
        4: ("description", "任务说明（wstring @+92）", 92),
        5: ("rule_param", "规则参数 u32（@+44）", 44),
        13: ("flag_ranked", "地图环境地面标记：地图信息窗口 Ground on/off（bool bit0 @+56；旧物理名待迁移）", 56),
        14: ("flag_private", "地图环境水中标记：地图信息窗口 Underwater on/off（bool bit1 @+56；旧物理名待迁移）", 56),
        15: ("flag_clan", "地图环境宇宙标记：地图信息窗口 Space on/off（bool bit2 @+56；旧物理名待迁移）", 56),
        16: ("vs_mode", "对战模式（sub_59FA70 @+48：TD/DOM/CORE…）", 48),
        17: ("vs_submode", "子模式（sub_59FB20 @+52：RPOST_DIFF/DOT_DMG…）", 52),
        18: ("faction", "势力：EFF/ZEON（sub_40CE20 @+88）", 88),
        23: ("flag_spectate", "允许观战（bool @+80）", 80),
        26: ("flag_custom", "自定义房间（bool @+81）", 81),
        27: ("flag_event", "活动房（bool @+82）", 82),
        28: ("flag_tournament", "锦标赛（bool @+83）", 83),
        31: ("score_param_a", "计分参数 A（u32 @+156）", 156),
        32: ("score_param_b", "计分参数 B（u32 @+152）", 152),
        33: ("score_param_c", "计分参数 C（u32 @+148）", 148),
        34: ("score_param_d", "计分参数 D（u32 @+144）", 144),
        35: ("score_param_e", "计分参数 E（u32 @+140）", 140),
        38: ("min_rank", "最低等级（u16 @+58）", 58),
        39: ("max_rank", "最高等级（u16 @+60）", 60),
        40: ("time_limit_sec", "时间限制秒（u32 @+68）", 68),
        41: ("respawn_limit", "重生上限（u16 @+72）", 72),
        44: ("team_size", "队伍人数（u16 @+128）", 128),
        55: ("reward_gp", "GP 奖励基数（u32 @+160）", 160),
        56: ("reward_exp", "经验奖励基数（u32 @+164）", 164),
        57: ("recommended_ms_cost", "推荐机体 cost（u16 @+120）", 120),
        58: ("max_ms_cost", "最大机体 cost（u16 @+122）", 122),
        59: ("banpick_rule_id", "BanPick 规则 ID（u32 @+124→MISSION_XWAR_BANPICK）", 124),
        60: ("sort_order", "列表排序（u16 @+130）", 130),
        63: ("thumbnail_id", "缩略图 ID（u16 @+132）", 132),
        74: ("script_flags", "脚本标志 u32（@+168；30112300/30121320 时置 1）", 168),
    }
    for idx, (name, meaning, off) in patches.items():
        c = col_by(d, csv_index=idx)
        if not c:
            continue
        kw = dict(name=name, db_column=name, meaning=meaning, status="confirmed", memory_offset=off)
        if idx == 16:
            patch_enum(c, "sub_59FA70", VS_MODE)
        elif idx == 17:
            patch_enum(c, "sub_59FB20", VS_SUBMODE)
        elif idx == 18:
            kw["type"] = "enum"
            kw["enum_values"] = [{"name": "EFF", "value": 0}, {"name": "ZEON", "value": 1}]
        elif idx in (13, 14, 15, 23, 26, 27, 28):
            kw["type"] = "bool"
        apply_col(c, **kw)


def enrich_mission_extrule(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；附加规则 ID", status="confirmed")
    c1 = col_by(d, csv_index=1)
    if c1:
        apply_col(c1, name="rule_label", db_column="rule_label", type="str",
                  meaning="规则说明文本（col1 预留；读表未写入内存，默认空）", status="confirmed")
    apply_col(col_by(d, csv_index=2), name="rule_type", meaning="规则类型：LIMIT_MS_SET/NEWBIE_LIMIT_MS/NEWBIE_VS_XWAR/BAN_PICK", status="confirmed")
    apply_col(col_by(d, csv_index=3), name="param_a", meaning="限制项 A：MS_COST/BTLTYPE_ENABLE/BTLTYPE_DISABLE/MS_TROOPS", status="confirmed")
    apply_col(col_by(d, csv_index=4), name="param_b", meaning="限制项 B（与 param_a 同枚举域 sub_59E0F0）", status="confirmed")
    apply_col(col_by(d, csv_index=5), name="param_value", db_column="param_value",
              meaning="限制数值（u32 @+12；如机体 cost 上限/禁机体 ID）", status="confirmed", memory_offset=12)


def enrich_mission_safety_area(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), name="area_id", db_column="area_id",
              meaning="安全区 ID（col0 预留；读表从 col1 起，默认 0）", status="gap")
    for idx, name, off in [
        (1, "min_x", 0), (2, "min_y", 4), (3, "min_z", 8),
        (4, "max_x", 12), (5, "max_y", 16), (6, "max_z", 20),
    ]:
        apply_col(col_by(d, csv_index=idx), name=name, db_column=name,
                  meaning=f"安全区 AABB {name}（float @+{off}；sub_BBB470）", status="confirmed", memory_offset=off)


def enrich_mission_xwar_banpick(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；XWAR Ban/Pick 规则 ID", status="confirmed")
    apply_col(col_by(d, csv_index=1), name="banpick_mode", db_column="banpick_mode",
              meaning="Ban/Pick 模式（u32 @+4；0=标准 1=快速）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=2), name="pick_count", meaning="Pick 阶段可选机体数（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=3), name="ban_ms_id", meaning="默认 Ban 机体 ID（u32 @+12；0=无）", status="confirmed", memory_offset=12)


def enrich_commander_npc(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；指挥官 ID", status="confirmed")
    apply_col(col_by(d, csv_index=1), name="npc_model_id", db_column="npc_model_id",
              meaning="NPC 模型 ID（u32 @+4；关联 chara 资源）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=2), name="portrait_id", db_column="portrait_id",
              meaning="头像/立绘 ID（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=3), name="commander_name", db_column="commander_name",
              meaning="指挥官名称（wstring @+12）", status="confirmed", memory_offset=12)
    apply_col(col_by(d, csv_index=4), name="description", db_column="description",
              meaning="指挥官说明（wstring @+40）", status="confirmed", memory_offset=40)
    c5 = col_by(d, csv_index=5)
    if c5:
        apply_col(c5, name="faction", db_column="faction", type="enum",
                  meaning="势力：NEUTRAL/EFF/ZEON（sub_572C30 @+68）", status="confirmed", memory_offset=68)
        patch_enum(c5, "sub_572C30", FACTION)
    apply_col(col_by(d, csv_index=6), name="voice_group_id", db_column="voice_group_id",
              meaning="语音组 ID（u32 @+72；cutin_voice_*_commander.csv）", status="confirmed", memory_offset=72)
    apply_col(col_by(d, csv_index=7), name="slot1_cost", db_column="slot1_cost",
              meaning="支援槽1 消耗（u16 @+88；csv12）", status="confirmed", memory_offset=88)
    apply_col(col_by(d, csv_index=8), name="slot2_cost", db_column="slot2_cost",
              meaning="支援槽2 消耗（u16 @+92；csv13）", status="confirmed", memory_offset=92)
    apply_col(col_by(d, csv_index=9), name="slot1_cooldown", db_column="slot1_cooldown",
              meaning="支援槽1 冷却秒（u32 @+220；csv14）", status="confirmed", memory_offset=220)
    apply_col(col_by(d, csv_index=10), name="slot3_cost", db_column="slot3_cost",
              meaning="支援槽3 消耗（u16 @+94；csv17）", status="confirmed", memory_offset=94)
    c11 = col_by(d, csv_index=11)
    if c11:
        apply_col(c11, name="support_type_1", db_column="support_type_1", type="enum",
                  meaning="支援类型槽1（sub_572CD0；BOMB/TENDER/SEARCH…共 12 槽循环）", status="confirmed", memory_offset=224)
        patch_enum(c11, "sub_572CD0", SUPPORT_TYPE)
    apply_col(col_by(d, csv_index=12), name="unlock_mission_id", db_column="unlock_mission_id",
              meaning="解锁任务 ID（u32 @+80；csv19）", status="confirmed", memory_offset=80)


def enrich_commander_support(d: dict) -> None:
    """sub_574300 reads csv 3,4,7,8,11,12 into runtime commander-support row."""
    mapping = [
        (0, None, "support_id", "u32", "主键；支援技能 ID（col0 表头键）", None),
        (1, None, "reserved_u32_1", "u32", "CSV 列存在但读表未单独取证（默认 0）", None),
        (2, None, "reserved_u32_2", "u32", "CSV 列存在但读表未单独取证（默认 0）", None),
        (3, 1, "use_cost", "u16", "发动消耗（u16 @+292；csv3）", 292),
        (4, 2, "cooldown_sec", "u16", "冷却时间秒（u16 @+294；csv4）", 294),
        (7, 3, "effect_param_a", "u32", "效果参数 A（u32 @+324；csv7）", 324),
        (8, 4, "linked_commander_id", "u32", "关联指挥官 ID（u32 @+332→查 COMMANDER_NPC 名称 @+296）", 332),
        (11, 5, "effect_param_b", "u32", "效果参数 B（u32 @+328；csv11）", 328),
        (12, 6, "effect_radius", "float", "效果半径（float @+340 = csv12 × flt_D69A58）", 340),
    ]
    d["columns"] = []
    for csv_i, ro, name, typ, meaning, mem in mapping:
        st = "confirmed" if ro else "gap"
        col = {
            "read_order": ro, "csv_index": csv_i, "db_column": name, "name": name, "type": typ,
            "meaning": meaning, "display_name": meaning, "status": st,
            "confidence": "★确证" if st == "confirmed" else "",
        }
        if mem is not None:
            col["memory_offset"] = mem
        if ro:
            col["asm_reader"] = "sub_574300"
        d["columns"].append(col)


def enrich_combat_operation(d: dict) -> None:
    """sub_572560 reads csv 0,7,8,9,10,11,12 — not sequential 1-6."""
    mapping = [
        (0, 1, "operation_id", "u32", "主键；战术指令 ID（ATTACK/DEFENSE/MOVE/SPECIAL 族）", 0, "sub_572560", "0x57258d"),
        (7, 2, "title_text", "str", "指令标题（wstring @+4；UI 显示名）", 4, "sub_572560", "0x5725a3"),
        (8, 3, "cast_time_sec", "float", "发动耗时秒（float @+32；sub_BBB470 col8）", 32, "sub_572560", "0x5725e1"),
        (9, 4, "target_filter", "u32", "目标筛选 ID（u32 @+36；battle-combat_operation_target_change）", 36, "sub_572560", "0x5725f8"),
        (10, 5, "description", "str", "指令说明（wstring @+40）", 40, "sub_572560", "0x5725fb"),
        (11, 6, "effect_duration_sec", "float", "效果持续秒（float @+68；sub_BBB470 col11）", 68, "sub_572560", "0x572650"),
        (12, 7, "container_collect_id", "u32", "容器收集 ID（u32 @+72；SC-0x6295 关联）", 72, "sub_572560", "0x572656"),
    ]
    d["columns"] = []
    for csv_i, ro, name, typ, meaning, mem, reader, va in mapping:
        d["columns"].append({
            "read_order": ro, "csv_index": csv_i, "db_column": name, "name": name, "type": typ,
            "meaning": meaning, "display_name": meaning, "status": "confirmed", "confidence": "★确证",
            "memory_offset": mem, "asm_reader": reader, "asm_va": va,
        })


def enrich_quest(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；委托/任务 ID", status="confirmed")
    apply_col(col_by(d, csv_index=1), name="quest_type", meaning="任务类型（u32 @+4；区分日常/成就/活动）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=2), name="title", meaning="任务标题（wstring @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=3), name="description", meaning="任务说明（wstring @+36）", status="confirmed", memory_offset=36)
    apply_col(col_by(d, csv_index=4), name="reward_table_id", db_column="reward_table_id",
              meaning="奖励表行 ID（u32 @+64；csv24=0x18 指向奖励配置）", status="confirmed", memory_offset=64)


def enrich_item(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；物品 ID（ITEM 族外键）", status="confirmed")
    apply_col(col_by(d, csv_index=1), meaning="排序/分组 ID（u32 @+4；背包/UI 归类）", status="confirmed")
    apply_col(col_by(d, csv_index=2), meaning="物品名称（wstring @+8）", status="confirmed")
    apply_col(col_by(d, csv_index=3), meaning="物品说明（wstring @+36）", status="confirmed")
    c = col_by(d, csv_index=4)
    if c:
        apply_col(c, name="item_type", meaning="物品类型（enum @+64；WEAPON/REPAIR/PARTS/TOKEN…共 25 值）", status="confirmed")
        patch_enum(c, "sub_593770")
    apply_col(col_by(d, csv_index=5), name="stack_limit", meaning="堆叠上限（u16 @+74）", status="confirmed", memory_offset=74)
    apply_col(col_by(d, csv_index=6), name="linked_table_id", meaning="关联表行 ID（u32 @+68；ITEM_USE/TOKEN 查目标）", status="confirmed", memory_offset=68)
    apply_col(col_by(d, csv_index=7), name="icon_variant", meaning="图标变体（u16 @+72）", status="confirmed", memory_offset=72)


def enrich_item_part(d: dict) -> None:
    by_ro = {c.get("read_order"): c for c in d["columns"]}
    ro_patches = {
        1: ("item_part_id", "主键；装备零件 ID", 0),
        2: ("linked_item_id", "关联 ITEM 行 ID（u32 @+4）", 4),
        3: ("part_group_id", "零件组 ID（u32 @+8）", 8),
        4: ("target_category", "作用大类：MS/WEAPON/ARMOR/OTHER（sub_5954A0 @+12）", 12),
        5: ("trigger_threshold_a", "触发条件阈值 A（float @+16；与 col10 触发类型配合）", 16),
        6: ("trigger_threshold_b", "触发条件阈值 B（float @+20）", 20),
        7: ("trigger_threshold_c", "触发条件阈值 C（float @+24）", 24),
        8: ("trigger_threshold_d", "触发条件阈值 D（float @+28）", 28),
        9: ("trigger_threshold_e", "触发条件阈值 E（float @+32）", 32),
        10: ("trigger_type_primary", "主触发时机（sub_5951D0 @+36：SPAWN/KILL/ARMOR_RATE…）", 36),
        11: ("effect_magnitude", "效果幅度（float @+40；写入机体/武器参数）", 40),
        12: ("trigger_type_secondary", "副触发时机（sub_5951D0 @+44）", 44),
        13: ("trigger_param_u32", "触发附加整型（u32 @+68；csv13 整型读法）", 68),
        14: ("param_mod_value", "参数修改值（float @+48；csv13 浮点读法，与 col16/17 成对）", 48),
        15: ("param_mod_value_b", "参数修改值 B（float @+52）", 52),
        16: ("param_mod_value_c", "参数修改值 C（float @+56）", 56),
        17: ("effect_scope", "作用对象范围（sub_5952C0：MS/WEAPON_SLOT_MAIN…）", None),
        18: ("stat_name", "机体/武器参数名（sub_5953B0：MS_ARMOR/W_POWER…）", None),
        19: ("key_action_a", "键位/动作 A（sub_CC6CA8；stat=MS_BOOST_GAUGE_RECOV 时启用）", None),
        20: ("key_action_b", "键位/动作 B（sub_CC6CA8）", None),
        21: ("loop_param_value", "循环参数值（float；8 组 effect_scope×stat 循环）", 80),
        22: ("priority", "优先级（u32 @+64）", 64),
        23: ("stack_rule", "叠加规则 ID（u32 @+60）", 60),
    }
    for ro, (name, meaning, mem) in ro_patches.items():
        c = by_ro.get(ro)
        if not c:
            continue
        kw = dict(name=name, db_column=name, meaning=meaning, status="confirmed")
        if mem is not None:
            kw["memory_offset"] = mem
        apply_col(c, **kw)
    for ro in (19, 20):
        c = by_ro.get(ro)
        if c and c.get("type") == "enum":
            c["enum_converter"] = "sub_CC6CA8"
            c["enum_doc"] = ENUM_DOC


def enrich_item_use(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), name="use_item_id", meaning="主键；消耗品行 ID（= ITEM.linked_table_id）", status="confirmed")
    apply_col(col_by(d, csv_index=2), name="linked_item_id", meaning="关联 ITEM.item_id（u32 @+32）", status="confirmed", memory_offset=32)
    apply_col(col_by(d, csv_index=3), name="enabled_flag", db_column="enabled_flag", type="bool",
              meaning="启用标志（u32 @+36；0=禁用该消耗品效果）", status="confirmed", memory_offset=36)


def enrich_item_token(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；代币物品 ID", status="confirmed")
    c = col_by(d, csv_index=2)
    if c:
        apply_col(c, name="token_type", meaning="代币类型：MSMA_STORAGE/MSMA_DECKCOST（sub_595870 @+4）", status="confirmed", memory_offset=4)
        patch_enum(c, "sub_595870", TOKEN_TYPE)
    apply_col(col_by(d, csv_index=3), name="token_value", db_column="token_value", meaning="代币面值/数量（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=4), name="expire_rule", db_column="expire_rule", meaning="过期规则 ID（u32 @+12；0=不过期）", status="confirmed", memory_offset=12)


def enrich_itempack(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；物品包 ID", status="confirmed")
    apply_col(col_by(d, csv_index=1), name="pack_item_id", meaning="包内物品 ITEM.item_id（u32 @+4）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=2), name="quantity", meaning="数量（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=3), name="drop_weight", db_column="drop_weight", meaning="掉落权重（u32 @+12；加权随机时）", status="confirmed", memory_offset=12)


def enrich_gacha(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；扭蛋池 ID", status="confirmed")
    apply_col(col_by(d, csv_index=1), name="display_order", db_column="display_order", meaning="UI 排序（u32 @+4）", status="confirmed")
    apply_col(col_by(d, csv_index=2), name="gacha_name", db_column="gacha_name", meaning="扭蛋池名称（wstring @+8）", status="confirmed")
    apply_col(col_by(d, csv_index=3), name="description", db_column="description", meaning="扭蛋池说明（wstring @+36）", status="confirmed")
    c4 = col_by(d, csv_index=4)
    if c4:
        apply_col(c4, name="currency_type", db_column="currency_type", meaning="消耗货币：GP/CP/CP_EX/CN_LOCAL…（sub_578090 @+64）", status="confirmed")
        patch_enum(c4, "sub_578090")
    c5 = col_by(d, csv_index=5)
    if c5:
        apply_col(c5, name="draw_mode", db_column="draw_mode", meaning="抽取模式：NORMAL/SINGLE/SINGLE_NORESET（sub_578130 @+68）", status="confirmed")
        patch_enum(c5, "sub_578130", GACHA_POOL)
    bool_cols = {6: "flag_visible", 7: "flag_limited", 8: "flag_new", 19: "flag_recommend", 20: "flag_hidden"}
    for idx, name in bool_cols.items():
        c = col_by(d, csv_index=idx)
        if c:
            apply_col(c, name=name, db_column=name, type="bool", meaning=f"开关位 {name}（!=0⇒true）", status="confirmed")
    u32_map = {
        9: ("single_cost", "单抽价格"), 10: ("ten_cost", "十连价格"), 11: ("ticket_item_id", "所需票券 ITEM ID"),
        12: ("start_time", "开始时间戳"), 13: ("end_time", "结束时间戳"), 14: ("banner_id", "横幅 ID"),
        15: ("pity_counter", "保底计数"), 16: ("pity_rare_id", "保底稀有 ID"), 17: ("daily_limit", "每日上限"),
        18: ("total_limit", "总次数上限"), 22: ("pool_group", "池分组 ID"), 24: ("ui_layout_id", "UI 布局 ID"),
        26: ("bonus_item_id", "附赠物品 ID"), 39: ("season_id", "赛季 ID"), 41: ("related_gacha_id", "关联池 ID"),
    }
    for idx, (name, desc) in u32_map.items():
        c = col_by(d, csv_index=idx)
        if c:
            apply_col(c, name=name.strip(), db_column=name.strip(), meaning=f"{desc}（u32 col{idx}）", status="confirmed")
    for idx in (30, 32, 34):
        ca, cb = col_by(d, csv_index=idx), col_by(d, csv_index=idx + 1)
        if ca:
            apply_col(ca, name=f"rate_pair_{idx}a", db_column=f"rate_pair_{idx}a", meaning=f"概率对 A（col{idx}；与 col{idx+1} 成对）", status="confirmed")
        if cb:
            apply_col(cb, name=f"rate_rarity_{idx}b", db_column=f"rate_rarity_{idx}b", type="enum",
                      meaning=f"稀有度/捆绑类型（col{idx+1}；sub_577FF0：FREE_PLAY_BUNDLE 等）", status="confirmed")
            patch_enum(cb, "sub_577FF0", [{"name": "FREE_PLAY_BUNDLE", "value": 0}])
    c38 = col_by(d, csv_index=38)
    if c38:
        apply_col(c38, name="bundle_type", db_column="bundle_type", meaning="捆绑类型（sub_577F50：PLAY_BUNDLE_BC_ONLY 等）", status="confirmed")
        patch_enum(c38, "sub_577F50", [{"name": "PLAY_BUNDLE_BC_ONLY", "value": 0}])
    c40 = col_by(d, csv_index=40)
    if c40:
        apply_col(c40, name="play_bundle_type", db_column="play_bundle_type", type="enum",
                  meaning="游玩捆绑类型（sub_577FF0 col40：FREE_PLAY_BUNDLE）", status="confirmed")
        patch_enum(c40, "sub_577FF0", [{"name": "FREE_PLAY_BUNDLE", "value": 0}])


def enrich_module(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；模块 ID（固有模块定义）", status="confirmed")
    apply_col(col_by(d, csv_index=2), name="linked_item_id", db_column="linked_item_id", meaning="关联 ITEM 行（u32 @+20）", status="confirmed", memory_offset=20)
    apply_col(col_by(d, csv_index=3), name="slot_index", db_column="slot_index", meaning="模块槽位序号（u32 @+4）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=4), name="param_a", db_column="param_a", meaning="参数 A（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=5), name="param_b", db_column="param_b", meaning="参数 B（u32 @+16）", status="confirmed", memory_offset=16)
    c7 = col_by(d, csv_index=7)
    if c7:
        apply_col(c7, name="module_category", meaning="模块类别：ATTACK/DEFENSE/MOVE/SPECIAL（sub_5A2CC0 @+24）", status="confirmed", memory_offset=24)
        patch_enum(c7, "sub_5A2CC0", MODULE_CAT)
    apply_col(col_by(d, csv_index=8), name="unlock_level", db_column="unlock_level", meaning="解锁等级（u32 @+28）", status="confirmed", memory_offset=28)


def enrich_module_develop(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；模块开发配方 ID", status="confirmed")
    apply_col(col_by(d, csv_index=2), name="module_id", meaning="目标 MODULE.module_id（u32 @+28）", status="confirmed", memory_offset=28)
    apply_col(col_by(d, csv_index=3), name="develop_time_sec", db_column="develop_time_sec", meaning="开发耗时秒（u32 @+32）", status="confirmed", memory_offset=32)
    apply_col(col_by(d, csv_index=4), name="material_item_id", db_column="material_item_id", meaning="材料 ITEM ID（u32 @+4；配对循环第1组）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=6), name="material_qty", db_column="material_qty", meaning="材料数量（u32 @+8）", status="confirmed", memory_offset=8)


def enrich_module_rental(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), meaning="主键；模块租借 ID", status="confirmed")
    apply_col(col_by(d, csv_index=4), name="module_id", meaning="MODULE.module_id（u32 @+4）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=5), name="rental_cost_gp", db_column="rental_cost_gp", meaning="租借 GP 费用（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=6), name="duration_sec", db_column="duration_sec", meaning="租借时长秒（u32 @+12）", status="confirmed", memory_offset=12)
    apply_col(col_by(d, csv_index=7), name="max_rental_count", db_column="max_rental_count", meaning="最大租借次数（u32 @+16）", status="confirmed", memory_offset=16)


def enrich_module_bonus(d: dict) -> None:
    apply_col(col_by(d, csv_index=1), name="bonus_group", meaning="加成组 ID（u32 @+0；同组 8 路循环）", status="confirmed", memory_offset=0)
    apply_col(col_by(d, csv_index=2), name="stat_id_a", db_column="stat_id_a", meaning="属性 ID A（u32 @+4；8 组循环第1项）", status="confirmed", memory_offset=4)
    apply_col(col_by(d, csv_index=4), name="stat_id_b", db_column="stat_id_b", meaning="属性 ID B（u32 @+8）", status="confirmed", memory_offset=8)
    apply_col(col_by(d, csv_index=5), name="stat_value", db_column="stat_value", meaning="加成数值（u32 @+12）", status="confirmed", memory_offset=12)


def enrich_module_bonus_lot(d: dict) -> None:
    apply_col(col_by(d, csv_index=0), name="lot_key", meaning="抽取键（str enum col0；如 ASSAULT_A×RANK1）", status="confirmed")
    apply_col(col_by(d, csv_index=1), name="lot_category", meaning="抽取类别（str enum col1：ASSAULT_A/SNIPE/CANNON/SUPPORT）", status="confirmed")
    apply_col(col_by(d, csv_index=2), name="weight", meaning="抽取权重（u32 col2）", status="confirmed")
    apply_col(col_by(d, csv_index=5), name="bonus_group_id", db_column="bonus_group_id", meaning="目标 MODULE_BONUS.bonus_group（u32 col5）", status="confirmed")
    apply_col(col_by(d, csv_index=6), name="reward_type", meaning="奖励类型（str enum col6）", status="confirmed")
    apply_col(col_by(d, csv_index=7), name="reward_param_a", db_column="reward_param_a", meaning="奖励参数 A（u32 col7）", status="confirmed")
    apply_col(col_by(d, csv_index=8), name="reward_param_b", db_column="reward_param_b", meaning="奖励参数 B（u32 col8）", status="confirmed")
    apply_col(col_by(d, csv_index=9), name="reward_param_c", db_column="reward_param_c", meaning="奖励参数 C（u32 col9）", status="confirmed")


ENRICHERS = {
    "MISSION_GROUP": enrich_mission_group,
    "MISSION_COOP": enrich_mission_coop,
    "MISSION_VS": enrich_mission_vs,
    "MISSION_EXTRULE": enrich_mission_extrule,
    "MISSION_SAFETY_AREA": enrich_mission_safety_area,
    "MISSION_XWAR_BANPICK": enrich_mission_xwar_banpick,
    "COMMANDER_NPC": enrich_commander_npc,
    "COMMANDER_SUPPORT": enrich_commander_support,
    "COMBAT_OPERATION": enrich_combat_operation,
    "QUEST": enrich_quest,
    "ITEM": enrich_item,
    "ITEM_PART": enrich_item_part,
    "ITEM_USE": enrich_item_use,
    "ITEM_TOKEN": enrich_item_token,
    "ITEMPACK_INFO": enrich_itempack,
    "GACHA": enrich_gacha,
    "MODULE": enrich_module,
    "MODULE_DEVELOP": enrich_module_develop,
    "MODULE_RENTAL": enrich_module_rental,
    "MODULE_BONUS": enrich_module_bonus,
    "MODULE_BONUS_LOT": enrich_module_bonus_lot,
}


def write_md(data: dict) -> None:
    md_path = ROOT / data.get("source_md", "")
    if not md_path.is_file():
        md_path = ROOT / "datatables" / "01-列注释" / Path(data["source_md"]).name
    cols = sorted(
        [c for c in data.get("columns", []) if c.get("read_order") is not None],
        key=lambda x: x.get("read_order") or 0,
    )
    lines = [
        f"# {data['id']} ｜ `{data['csv_path']}`",
        "",
        f"- **用途**：{data.get('purpose', '')}",
        f"- 表ID `{data.get('table_id')}` ｜ 下载序 `{data.get('download_order')}` ｜ 类名 `{data.get('class_name')}`",
        f"- 逐列读取函数 `{data.get('asm_reader', '')}` ｜ **列数 {data.get('column_count', len(cols))}**",
        "",
        "| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |",
        "|---|---|---|---|---|---|",
    ]
    for i, c in enumerate(cols, 1):
        ro = c.get("read_order") or i
        csv_i = c.get("csv_index", "?")
        name = c.get("name") or c.get("db_column", "?")
        typ = c.get("type", "?")
        if c.get("enum_converter"):
            typ = f"enum `{c['enum_converter']}`"
        mem = c.get("memory_offset")
        mem_s = f"+{mem}" if mem is not None else "—"
        meaning = re.sub(r"\*+", "", c.get("meaning", "")).strip()
        lines.append(f"| {ro} | `{csv_i}` | `{name}` | {typ} | {mem_s} | {meaning} |")
    lines += [
        "",
        "**填写规则**：",
        "- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。",
        "- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。",
        "- 越界列 = 0；每个数据行至少 1 个单元格。",
        "",
    ]
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for tid in TABLE_IDS:
        path = TABLES / f"{tid}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        ENRICHERS[tid](data)
        recount(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_md(data)
        cc, cp = data["column_confirmed"], data["column_partial"]
        print(f"{tid}: confirmed={cc} partial={cp} gap={data['column_gap']}")


if __name__ == "__main__":
    main()
