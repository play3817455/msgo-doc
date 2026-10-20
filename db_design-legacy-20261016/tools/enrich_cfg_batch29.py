#!/usr/bin/env python3
"""Enrich batch-29 CFG tables to AI_WEAPON_PARAM quality (JSON + MD)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "tables"
DATATABLES = ROOT / "datatables" / "01-列注释"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

TABLE_IDS = [
    "OVER_CUSTOM", "OVER_CUSTOM_CUPSULE", "OVER_CUSTOM_DEVELOP", "OVERHAUL",
    "LVUP_MSMA", "LVUP_PILOT", "LVUP_PILOT_CLASS", "LVUP_PILOT_EXAM",
    "LVUP_CLAN", "LVUP_FAVMS", "DAILY_RECORD", "CLAN_CHALLENGE",
    "TROOP_CHALLENGE", "NETCAFE_CHALLENGE", "BEGINNER_CHALLENGE",
    "CHALLENGE_HIGHSCORE", "PLAY_BONUS_REWARD", "MONTHLY_BONUS_REWARD",
    "SEASON_CLASS_IMFORMATION", "SEASON_CLASS_UP_REWARD",
    "SEASON_RANKERBATTLE_REWARD", "SCORE_CONFIG_CATEGORY", "TREND_DATA_WEAPON",
    "FORCEGAUGE_INFO", "PLAYER_NAVI", "BYWORD", "BGMPACKAGE", "BANNER_INFO",
    "AUTOEXEC",
]

# csv_index -> patch fields
COL = dict  # shorthand typing hint

STAT_46_MEANING = (
    "战绩统计项（enum sub_592DB0，46 项：VERSUS/WIN/KILL/SCORE_* 等；"
    "与客户端「战斗记录」页签及 badge_config リボンタイプ 同源）"
)
STAT_46_CLAN = (
    "部队挑战统计项（enum sub_571D00，46 项 + PERFECT；"
    "与 DAILY_RECORD 同一套战绩体系，换到部队维度）"
)
STAT_46_TROOP = STAT_46_MEANING.replace("sub_592DB0", "sub_592DB0").replace(
    "战斗记录", "势力挑战"
)
STAT_46_NETCAFE = (
    "网吧挑战统计项（enum sub_5874A0，46 项 + NETCAFE；"
    "与 DAILY_RECORD 同一套战绩体系）"
)
REWARD_TYPE = {
    "name": "reward_type",
    "meaning": "奖励物类型（enum sub_5703A0：GP/ITEM/MSMA/BUILDUP_MSMA）",
    "display_name": "奖励物类型（GP/ITEM/MSMA/BUILDUP_MSMA）",
    "confidence": "★确证",
    "status": "confirmed",
    "enum_converter": "sub_5703A0",
}

SEMANTICS: dict[str, dict[int, dict]] = {
    "AUTOEXEC": {},
    "OVER_CUSTOM": {
        0: {"name": "custom_id", "meaning": "超改方案 ID（主键；CMSMAOverCustomTable 索引键）", "display_name": "超改方案 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "msma_id", "meaning": "目标机体 ID（col1 → CHARA_PARAM 主键）", "display_name": "目标机体 ID", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "stage", "meaning": "超改阶段序号（col2；同一机体多段超改的 tier）", "display_name": "超改阶段", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "cost_points", "meaning": "消耗超改点数（u16 col4；与 OVER_CUSTOM_CUPSULE 点数道具联动）", "display_name": "消耗超改点数", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "develop_cost", "meaning": "开发/素材消耗参数（u32 col5）", "display_name": "开发消耗参数", "confidence": "○ASM确证", "status": "partial"},
        7: {"name": "stat_bonus_a", "meaning": "能力加成 A（u16 col7；写入机体超改补正槽）", "display_name": "能力加成 A", "confidence": "○ASM确证", "status": "partial"},
        8: {"name": "bonus_param", "meaning": "加成关联参数（u32 col8；具体属性 ID 或倍率索引）", "display_name": "加成关联参数", "confidence": "△", "status": "partial"},
        10: {"name": "stat_bonus_b", "meaning": "能力加成 B（u16 col10）", "display_name": "能力加成 B", "confidence": "○ASM确证", "status": "partial"},
        11: {"name": "stat_bonus_c", "meaning": "能力加成 C（u16 col11）", "display_name": "能力加成 C", "confidence": "○ASM确证", "status": "partial"},
        12: {"name": "extra_param", "meaning": "扩展参数（u32 col12）", "display_name": "扩展参数", "confidence": "△", "status": "partial"},
    },
    "OVER_CUSTOM_CUPSULE": {
        0: {"name": "item_id", "meaning": "超改点数胶囊物品 ID（主键；→ ITEM 表）", "display_name": "胶囊物品 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "point_value", "meaning": "使用后获得超改点数（col1 u32）", "display_name": "超改点数", "confidence": "○ASM确证", "status": "confirmed"},
        3: {"name": "bonus_rate", "meaning": "点数倍率/附加参数（u32 col3；未读 col2 默认 0）", "display_name": "点数倍率参数", "confidence": "△", "status": "partial"},
    },
    "OVER_CUSTOM_DEVELOP": {
        0: {"name": "recipe_id", "meaning": "超改开发配方 ID（主键）", "display_name": "配方 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "msma_id", "meaning": "目标机体 ID", "display_name": "目标机体 ID", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "stage", "meaning": "超改阶段", "display_name": "超改阶段", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "material_id", "meaning": "消耗素材物品 ID（→ ITEM）", "display_name": "消耗素材 ID", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "material_qty", "meaning": "素材消耗数量", "display_name": "素材数量", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "gp_cost", "meaning": "GP 开发费用", "display_name": "GP 费用", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "success_rate", "meaning": "开发成功率或权重（u32 col6）", "display_name": "成功率/权重", "confidence": "△", "status": "partial"},
    },
    "OVERHAUL": {
        0: {"name": "overhaul_id", "meaning": "大修方案 ID（主键；COverHaulTable）", "display_name": "大修 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "overhaul_name", "meaning": "大修方案名称（wstring col1）", "display_name": "方案名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        2: {"name": "msma_id", "meaning": "目标机体 ID（col2 → CHARA_PARAM）", "display_name": "目标机体 ID", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "rank_requirement", "meaning": "机体稀有度/等级需求（col3）", "display_name": "等级需求", "confidence": "△", "status": "partial"},
        4: {"name": "gp_cost", "meaning": "GP 翻新费用（col4）", "display_name": "GP 费用", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "base_param", "meaning": "基础参数（col6）", "display_name": "基础参数", "confidence": "△", "status": "partial"},
        7: {"name": "material_id_1", "meaning": "素材 1 物品 ID（col7；3 组循环素材槽）", "display_name": "素材 1 ID", "confidence": "○ASM确证", "status": "partial"},
        8: {"name": "material_name_1", "meaning": "素材 1 名称（wstring col8）", "display_name": "素材 1 名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        9: {"name": "material_qty_1", "meaning": "素材 1 数量（col9）", "display_name": "素材 1 数量", "confidence": "○ASM确证", "status": "partial"},
        11: {"name": "material_id_2", "meaning": "素材 2 物品 ID（col11）", "display_name": "素材 2 ID", "confidence": "○ASM确证", "status": "partial"},
        14: {"name": "material_id_3", "meaning": "素材 3 物品 ID（col14）", "display_name": "素材 3 ID", "confidence": "○ASM确证", "status": "partial"},
    },
    "LVUP_MSMA": {
        0: {"name": "ms_level", "meaning": "机体等级（u8 主键；本地表 CLvupMsmaTable，不下发）", "display_name": "机体等级", "confidence": "★确证", "status": "confirmed", "type": "u8"},
        1: {"name": "level_name", "meaning": "等级显示名称（wstring col1）", "display_name": "等级名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        2: {"name": "exp_required", "meaning": "升级所需经验（u32 col2）", "display_name": "升级所需经验", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "stat_bonus", "meaning": "等级属性加成（u32 col3）", "display_name": "属性加成", "confidence": "△", "status": "partial"},
        4: {"name": "unlock_skill", "meaning": "解锁技能/能力 ID（u32 col4）", "display_name": "解锁能力", "confidence": "△", "status": "partial"},
    },
    "LVUP_PILOT": {
        0: {"name": "pilot_level", "meaning": "机师等级（u8 主键 col0）", "display_name": "机师等级", "confidence": "★确证", "status": "confirmed", "type": "u8"},
        1: {"name": "level_name", "meaning": "等级显示名称（wstring col1；sub_456D90→sub_4029E0）", "display_name": "等级名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        35: {"name": "exp_multiplier", "meaning": "经验倍率（float col35 × flt_D6AE54；读表后客户端清零，仅服务端配置用）", "display_name": "经验倍率", "confidence": "○ASM确证", "status": "partial", "type": "float"},
        36: {"name": "flag_milestone", "meaning": "里程碑标志（bool col36；!=0 触发特殊等级事件）", "display_name": "里程碑标志", "confidence": "○ASM确证", "status": "partial", "type": "bool"},
        37: {"name": "unlock_param", "meaning": "解锁关联参数（u32 col37）", "display_name": "解锁参数", "confidence": "△", "status": "partial"},
        38: {"name": "flag_special", "meaning": "特殊等级标志（bool col38）", "display_name": "特殊等级标志", "confidence": "○ASM确证", "status": "partial", "type": "bool"},
        41: {"name": "reward_id", "meaning": "等级达成奖励 ID（u32 col41 → +52）", "display_name": "达成奖励 ID", "confidence": "△", "status": "partial"},
        42: {"name": "bonus_gp", "meaning": "等级奖励 GP（u32 col42 → +48）", "display_name": "奖励 GP", "confidence": "△", "status": "partial"},
        44: {"name": "skill_point", "meaning": "获得技能点/属性点（u32 col44）", "display_name": "技能/属性点", "confidence": "△", "status": "partial"},
    },
    "LVUP_PILOT_CLASS": {
        0: {"name": "class_id", "meaning": "军衔等级 ID（u8 主键）", "display_name": "军衔 ID", "confidence": "★确证", "status": "confirmed", "type": "u8"},
        1: {"name": "rank_point_threshold", "meaning": "军衔点数阈值（col1；客户端 %10000 分段算法）", "display_name": "军衔点数阈值", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "reserved_flag", "meaning": "保留标志（u8 col2，CSV 通常 0）", "display_name": "保留标志", "confidence": "○ASM确证", "status": "partial", "type": "u8"},
        3: {"name": "rank_name", "meaning": "军衔名称（wstring col3）", "display_name": "军衔名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        4: {"name": "requirement_value", "meaning": "升级需求数值（col4；对战/任务达成量）", "display_name": "升级需求值", "confidence": "○ASM确证", "status": "partial"},
    },
    "LVUP_PILOT_EXAM": {
        0: {"name": "exam_level", "meaning": "考核等级（u8 主键）", "display_name": "考核等级", "confidence": "★确证", "status": "confirmed", "type": "u8"},
        1: {"name": "exam_name", "meaning": "考核名称（wstring col1）", "display_name": "考核名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        2: {"name": "exp_required", "meaning": "考核所需经验（u32 col2）", "display_name": "考核所需经验", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "pass_score", "meaning": "合格分数线（u32 col3）", "display_name": "合格分数线", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "bonus_param", "meaning": "考核通过奖励参数（u32 col4）", "display_name": "通过奖励参数", "confidence": "△", "status": "partial"},
    },
    "LVUP_CLAN": {
        0: {"name": "clan_level", "meaning": "部队等级（u8 col0 主键）", "display_name": "部队等级", "confidence": "★确证", "status": "confirmed", "type": "u8"},
        1: {"name": "member_cap", "meaning": "成员上限（u32 col1）", "display_name": "成员上限", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "mechanic_level", "meaning": "部队机械师等级档（enum col3；MECHANIC_LV0..LV10）", "display_name": "机械师等级档", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_578C50"},
        4: {"name": "exp_base", "meaning": "升级经验基数（col4）", "display_name": "经验基数", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "exp_increment", "meaning": "升级经验增量（col5；与 col4 合成总需求）", "display_name": "经验增量", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "facility_unlock", "meaning": "设施解锁类型（enum col6）", "display_name": "设施解锁", "confidence": "○ASM确证", "status": "partial", "type": "enum", "enum_converter": "sub_578EE0"},
        7: {"name": "gp_bonus", "meaning": "部队 GP 加成（u32 col7）", "display_name": "GP 加成", "confidence": "△", "status": "partial"},
        8: {"name": "permission_flag", "meaning": "权限标志（enum col8）", "display_name": "权限标志", "confidence": "○ASM确证", "status": "partial", "type": "enum", "enum_converter": "sub_5790B0"},
        9: {"name": "shop_level", "meaning": "部队商店等级（enum col9）", "display_name": "商店等级", "confidence": "○ASM确证", "status": "partial", "type": "enum", "enum_converter": "sub_579500"},
        10: {"name": "bonus_type", "meaning": "等级奖励类型（enum col10）", "display_name": "等级奖励类型", "confidence": "○ASM确证", "status": "partial", "type": "enum", "enum_converter": "sub_5796D0"},
        11: {"name": "bonus_value", "meaning": "等级奖励数值（u32 col11）", "display_name": "等级奖励数值", "confidence": "△", "status": "partial"},
        12: {"name": "extra_param", "meaning": "扩展参数（u32 col12）", "display_name": "扩展参数", "confidence": "△", "status": "partial"},
    },
    "LVUP_FAVMS": {
        0: {"name": "fav_level", "meaning": "爱机等级（u8 主键）", "display_name": "爱机等级", "confidence": "★确证", "status": "confirmed", "type": "u8"},
        1: {"name": "exp_required", "meaning": "升级所需经验（u32 col1）", "display_name": "升级所需经验", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "stat_bonus", "meaning": "爱机属性加成（u32 col2）", "display_name": "属性加成", "confidence": "△", "status": "partial"},
    },
    "DAILY_RECORD": {
        0: {"name": "record_id", "meaning": "战绩统计行 ID（主键；与 badge_config リボンID 一一对应）", "display_name": "统计行 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "display_group", "meaning": "UI 显示分组/排序（u8 col1）", "display_name": "显示分组", "confidence": "○ASM确证", "status": "partial", "type": "u8"},
        4: {"name": "stat_type", "meaning": STAT_46_MEANING, "display_name": "战绩统计项", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_592DB0"},
        5: {"name": "unit_type", "meaning": "统计单位类型/辅助参数（u32 col5；badge_config「单位」列同源）", "display_name": "统计单位", "confidence": "△", "status": "partial"},
        8: {"name": "display_order", "meaning": "列表排序权重（u32 col8）", "display_name": "排序权重", "confidence": "△", "status": "partial"},
        10: {"name": "badge_tier_ref", "meaning": "绶带等级参照（enum col10 sub_587540：BRONZE/SILVER/GOLD）", "display_name": "绶带等级参照", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_587540"},
        11: {"name": "bronze_threshold", "meaning": "铜绶带获得条件值（u32 col11 ↔ badge_config 銅リボン）", "display_name": "铜绶带条件值", "confidence": "★确证", "status": "confirmed"},
        12: {"name": "silver_threshold", "meaning": "银绶带获得条件值（u32 col12 ↔ badge_config 銀リボン）", "display_name": "银绶带条件值", "confidence": "★确证", "status": "confirmed"},
        14: {"name": "bronze_icon_id", "meaning": "铜绶带图标 ID（u32 col14 ↔ badge_config 銅アイコン）", "display_name": "铜绶带图标", "confidence": "★确证", "status": "confirmed"},
        15: {"name": "silver_icon_id", "meaning": "银绶带图标 ID（u32 col15）", "display_name": "银绶带图标", "confidence": "★确证", "status": "confirmed"},
        17: {"name": "gold_icon_id", "meaning": "金绶带图标 ID（u32 col17）", "display_name": "金绶带图标", "confidence": "★确证", "status": "confirmed"},
        18: {"name": "stat_title", "meaning": "统计项显示标题（wstring col18）", "display_name": "统计标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        19: {"name": "stat_description", "meaning": "统计项说明（wstring col19；badge_config 説明文同源）", "display_name": "统计说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
    },
    "CLAN_CHALLENGE": {
        0: {"name": "challenge_id", "meaning": "部队挑战 ID（主键）", "display_name": "挑战 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "display_group", "meaning": "UI 显示分组（u8 col1）", "display_name": "显示分组", "confidence": "○ASM确证", "status": "partial", "type": "u8"},
        4: {"name": "stat_type", "meaning": STAT_46_CLAN, "display_name": "挑战统计项", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_571D00"},
        5: {"name": "target_value", "meaning": "部队累计目标值（u32 col5 → +12）", "display_name": "累计目标值", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "reward_gp", "meaning": "达成奖励 GP（u32 col11 → +16）", "display_name": "奖励 GP", "confidence": "△", "status": "partial"},
        7: {"name": "reward_item_id", "meaning": "达成奖励物品 ID（u32 col12 → +20）", "display_name": "奖励物品 ID", "confidence": "△", "status": "partial"},
        8: {"name": "reward_qty", "meaning": "奖励物品数量（u32 col14 → +24）", "display_name": "奖励数量", "confidence": "△", "status": "partial"},
        11: {"name": "reward_gp", "meaning": "达成奖励 GP（u32 col11）", "display_name": "奖励 GP", "confidence": "△", "status": "partial"},
        12: {"name": "reward_item_id", "meaning": "达成奖励物品 ID（u32 col12 → ITEM）", "display_name": "奖励物品 ID", "confidence": "△", "status": "partial"},
        14: {"name": "reward_qty", "meaning": "奖励物品数量（u32 col14）", "display_name": "奖励数量", "confidence": "△", "status": "partial"},
        15: {"name": "clan_point", "meaning": "部队点数奖励（u32 col15）", "display_name": "部队点数", "confidence": "△", "status": "partial"},
        17: {"name": "bonus_param", "meaning": "附加奖励参数（u32 col17）", "display_name": "附加参数", "confidence": "△", "status": "partial"},
        18: {"name": "challenge_title", "meaning": "挑战标题（wstring col18）", "display_name": "挑战标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        19: {"name": "challenge_desc", "meaning": "挑战说明（wstring col19）", "display_name": "挑战说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
    },
    "TROOP_CHALLENGE": {
        0: {"name": "challenge_id", "meaning": "势力挑战 ID（主键；联邦/吉翁阵营挑战）", "display_name": "挑战 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "troop_faction", "meaning": "目标势力/阵营（u8 col1）", "display_name": "目标势力", "confidence": "○ASM确证", "status": "partial", "type": "u8"},
        4: {"name": "stat_type", "meaning": STAT_46_TROOP, "display_name": "挑战统计项", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_592DB0"},
        5: {"name": "target_value", "meaning": "势力累计目标值（u32 col5）", "display_name": "累计目标值", "confidence": "○ASM确证", "status": "partial"},
        10: {"name": "badge_tier_ref", "meaning": "绶带等级参照（enum col10 sub_587540）", "display_name": "绶带等级参照", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_587540"},
        18: {"name": "challenge_title", "meaning": "挑战标题（wstring col18）", "display_name": "挑战标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        19: {"name": "challenge_desc", "meaning": "挑战说明（wstring col19）", "display_name": "挑战说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
    },
    "NETCAFE_CHALLENGE": {
        0: {"name": "challenge_id", "meaning": "网吧挑战 ID（主键）", "display_name": "挑战 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "display_group", "meaning": "UI 显示分组（u8 col1）", "display_name": "显示分组", "confidence": "○ASM确证", "status": "partial", "type": "u8"},
        4: {"name": "stat_type", "meaning": STAT_46_NETCAFE, "display_name": "挑战统计项", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_5874A0"},
        5: {"name": "target_value", "meaning": "网吧累计目标值（u32 col5）", "display_name": "累计目标值", "confidence": "○ASM确证", "status": "partial"},
        10: {"name": "badge_tier_ref", "meaning": "绶带等级参照（enum col10 sub_587540）", "display_name": "绶带等级参照", "confidence": "★确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_587540"},
        18: {"name": "challenge_title", "meaning": "挑战标题（wstring col18）", "display_name": "挑战标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        19: {"name": "challenge_desc", "meaning": "挑战说明（wstring col19）", "display_name": "挑战说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
    },
    "BEGINNER_CHALLENGE": {
        0: {"name": "challenge_id", "meaning": "新手挑战 ID（主键）", "display_name": "挑战 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "sort_order", "meaning": "显示排序（u32 col1）", "display_name": "显示排序", "confidence": "○ASM确证", "status": "partial"},
        2: {**REWARD_TYPE},
        3: {"name": "reward_param_id", "meaning": "奖励物 ID（u32 col3；依 reward_type 解释为物品/机体/强化 ID）", "display_name": "奖励物 ID", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "reward_quantity", "meaning": "奖励数量（u32 col4）", "display_name": "奖励数量", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "condition_param", "meaning": "达成条件参数（u32 col5）", "display_name": "达成条件", "confidence": "△", "status": "partial"},
    },
    "CHALLENGE_HIGHSCORE": {
        0: {"name": "highscore_id", "meaning": "协作挑战排行 ID（主键）", "display_name": "排行 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "mission_id", "meaning": "关联协作战任务 ID（u32 col1 → MISSION_COOP）", "display_name": "任务 ID", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "rank_title", "meaning": "排行档位标题（wstring col2）", "display_name": "档位标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        3: {"name": "rank_description", "meaning": "排行说明（wstring col3）", "display_name": "排行说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
        4: {"name": "reward_title", "meaning": "奖励标题（wstring col4）", "display_name": "奖励标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        5: {"name": "reward_desc", "meaning": "奖励说明（wstring col5）", "display_name": "奖励说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
        6: {"name": "ui_label", "meaning": "UI 标签文本（wstring col6）", "display_name": "UI 标签", "confidence": "★确证", "status": "confirmed", "type": "str"},
        7: {"name": "footer_text", "meaning": "页脚/备注文本（wstring col7）", "display_name": "备注文本", "confidence": "★确证", "status": "confirmed", "type": "str"},
        8: {"name": "score_threshold", "meaning": "上榜分数阈值（u32 col8）", "display_name": "分数阈值", "confidence": "○ASM确证", "status": "partial"},
        9: {"name": "reward_gp", "meaning": "达成奖励 GP（u32 col9）", "display_name": "奖励 GP", "confidence": "○ASM确证", "status": "partial"},
    },
    "PLAY_BONUS_REWARD": {
        0: {"name": "bonus_id", "meaning": "游玩奖励 ID（主键）", "display_name": "奖励 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "play_count_min", "meaning": "最低游玩场次（u32 col1 → +8）", "display_name": "最低场次", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "play_count_max", "meaning": "最高游玩场次（u32 col2）", "display_name": "最高场次", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "time_minutes", "meaning": "最低游玩时长分钟（u32 col3）", "display_name": "最低时长(分)", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "reward_gp", "meaning": "奖励 GP（u16 col4）", "display_name": "奖励 GP", "confidence": "○ASM确证", "status": "partial", "type": "u16"},
        5: {"name": "reward_item_qty", "meaning": "奖励物品数量（u16 col5）", "display_name": "物品数量", "confidence": "○ASM确证", "status": "partial", "type": "u16"},
        6: {"name": "reward_item_id", "meaning": "奖励物品 ID（u32 col6 → ITEM）", "display_name": "奖励物品 ID", "confidence": "○ASM确证", "status": "partial"},
        7: {"name": "battle_mode_code", "meaning": "适用战斗模式编码（u32 col7；高 8 位解码为 1/5/6/99 模式过滤）", "display_name": "战斗模式编码", "confidence": "○ASM确证", "status": "partial"},
        9: {"name": "bonus_flag", "meaning": "奖励标志/倍率（u32 col9）", "display_name": "奖励标志", "confidence": "△", "status": "partial"},
    },
    "MONTHLY_BONUS_REWARD": {
        0: {"name": "reward_id", "meaning": "月度奖励 ID（主键）", "display_name": "奖励 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "year_month", "meaning": "年月编码（u16 col1；YYYYMM 或序数）", "display_name": "年月", "confidence": "○ASM确证", "status": "partial", "type": "u16"},
        2: {"name": "login_channel", "meaning": "登录渠道（比较链 col2：LOGIN=1 / XWAR=-1）", "display_name": "登录渠道", "confidence": "★确证", "status": "confirmed"},
        3: {"name": "day_of_month", "meaning": "月份内日序（u16 col3；第几天登录领取）", "display_name": "日序", "confidence": "○ASM确证", "status": "partial", "type": "u16"},
        4: {**REWARD_TYPE},
        5: {"name": "reward_param_id", "meaning": "奖励物 ID（u32 col5）", "display_name": "奖励物 ID", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "reward_quantity", "meaning": "奖励数量（u32 col6）", "display_name": "奖励数量", "confidence": "○ASM确证", "status": "partial"},
        7: {"name": "bonus_flag", "meaning": "附加标志（u32 col7）", "display_name": "附加标志", "confidence": "△", "status": "partial"},
    },
    "SEASON_CLASS_IMFORMATION": {
        0: {"name": "class_id", "meaning": "赛季阶级 ID（主键）", "display_name": "阶级 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "class_name", "meaning": "阶级名称（文本 enum col1 sub_402310）", "display_name": "阶级名称", "confidence": "○ASM确证", "status": "partial", "type": "enum", "enum_converter": "sub_402310"},
        2: {"name": "rank_min", "meaning": "适用排名下限（u32 col2）", "display_name": "排名下限", "confidence": "△", "status": "partial"},
        3: {"name": "rank_max", "meaning": "适用排名上限（u32 col3）", "display_name": "排名上限", "confidence": "△", "status": "partial"},
        4: {"name": "point_threshold", "meaning": "阶级点数阈值（u32 col4）", "display_name": "点数阈值", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "promotion_wins", "meaning": "升阶所需胜场（u32 col5）", "display_name": "升阶胜场", "confidence": "△", "status": "partial"},
        6: {"name": "demotion_losses", "meaning": "降阶败场阈值（u32 col6）", "display_name": "降阶败场", "confidence": "△", "status": "partial"},
        7: {"name": "season_bonus", "meaning": "赛季加成系数（u32 col7）", "display_name": "赛季加成", "confidence": "△", "status": "partial"},
        8: {"name": "icon_id", "meaning": "阶级图标 ID（u32 col8）", "display_name": "图标 ID", "confidence": "○ASM确证", "status": "partial"},
        9: {"name": "display_color", "meaning": "UI 显示颜色（u32 col9）", "display_name": "显示颜色", "confidence": "△", "status": "partial"},
        10: {"name": "tier_min", "meaning": "阶级段下限（u16 col10）", "display_name": "段下限", "confidence": "△", "status": "partial", "type": "u16"},
        11: {"name": "tier_max", "meaning": "阶级段上限（u16 col11）", "display_name": "段上限", "confidence": "△", "status": "partial", "type": "u16"},
    },
    "SEASON_CLASS_UP_REWARD": {
        0: {"name": "class_id", "meaning": "赛季阶级 ID（主键；→ SEASON_CLASS_IMFORMATION）", "display_name": "阶级 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "reward_title", "meaning": "奖励标题（文本 enum col1 sub_402310）", "display_name": "奖励标题", "confidence": "○ASM确证", "status": "partial", "type": "enum", "enum_converter": "sub_402310"},
        2: {"name": "reward_gp", "meaning": "升阶奖励 GP（u32 col2）", "display_name": "奖励 GP", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "reward_item_id", "meaning": "升阶奖励物品 ID（u32 col3 → ITEM）", "display_name": "奖励物品 ID", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "reward_item_qty", "meaning": "奖励物品数量（u32 col4）", "display_name": "物品数量", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "bonus_gp", "meaning": "附加 GP 奖励（u32 col5 → +44）", "display_name": "附加 GP", "confidence": "○ASM确证", "status": "partial"},
        7: {"name": "bonus_item_id", "meaning": "附加物品 ID（u32 col7 → +112）", "display_name": "附加物品 ID", "confidence": "○ASM确证", "status": "partial"},
        8: {"name": "bonus_item_qty", "meaning": "附加物品数量（u32 col8 → +116）", "display_name": "附加物品数量", "confidence": "○ASM确证", "status": "partial"},
    },
    "SEASON_RANKERBATTLE_REWARD": {
        0: {"name": "reward_id", "meaning": "排名战奖励 ID（主键）", "display_name": "奖励 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "season_id", "meaning": "赛季 ID（u32 col1）", "display_name": "赛季 ID", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "rank_min", "meaning": "适用排名下限（u32 col2）", "display_name": "排名下限", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "rank_max", "meaning": "适用排名上限（u32 col3）", "display_name": "排名上限", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "reward_gp", "meaning": "排名奖励 GP（u32 col4）", "display_name": "奖励 GP", "confidence": "○ASM确证", "status": "partial"},
        5: {"name": "reward_item_id", "meaning": "排名奖励物品 ID（u32 col5）", "display_name": "奖励物品 ID", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "reward_item_qty", "meaning": "奖励物品数量（u32 col6）", "display_name": "物品数量", "confidence": "○ASM确证", "status": "partial"},
        7: {"name": "bonus_title_id", "meaning": "奖励称号 ID（u32 col7 → BYWORD）", "display_name": "称号 ID", "confidence": "△", "status": "partial"},
    },
    "SCORE_CONFIG_CATEGORY": {
        0: {"name": "category_name", "meaning": "计分分类名称（wstring col0；任务计分项归类标签）", "display_name": "分类名称", "confidence": "★确证", "status": "confirmed", "type": "str"},
        1: {"name": "category_index", "meaning": "计分分类索引（enum col1；客户端 score_config 分组键）", "display_name": "分类索引", "confidence": "○ASM确证", "status": "partial", "type": "enum"},
    },
    "TREND_DATA_WEAPON": {
        0: {"name": "weapon_trend_id", "meaning": "武器趋势行 ID（主键）", "display_name": "趋势 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "weapon_id", "meaning": "武器 ID（→ WEAPON_SETTING col0）", "display_name": "武器 ID", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "usage_rate", "meaning": "使用率/流行度（u32 col2；百分比×100 或权重）", "display_name": "使用率", "confidence": "△", "status": "partial"},
        3: {"name": "win_rate", "meaning": "胜率统计（u32 col3）", "display_name": "胜率", "confidence": "△", "status": "partial"},
        4: {"name": "pick_rate", "meaning": "选取率（u32 col4）", "display_name": "选取率", "confidence": "△", "status": "partial"},
        5: {"name": "trend_rank", "meaning": "趋势排名（u32 col5）", "display_name": "趋势排名", "confidence": "△", "status": "partial"},
        6: {"name": "msma_id", "meaning": "关联机体 ID（u32 col6；配装推荐机体）", "display_name": "关联机体", "confidence": "△", "status": "partial"},
        7: {"name": "period_id", "meaning": "统计周期 ID（u32 col7）", "display_name": "统计周期", "confidence": "△", "status": "partial"},
        8: {"name": "sample_count", "meaning": "样本数量（u32 col8）", "display_name": "样本数", "confidence": "△", "status": "partial"},
        9: {"name": "recommend_score", "meaning": "推荐分数（u32 col9）", "display_name": "推荐分", "confidence": "△", "status": "partial"},
        10: {"name": "display_flag", "meaning": "大厅显示标志（u32 col10）", "display_name": "显示标志", "confidence": "△", "status": "partial"},
    },
    "FORCEGAUGE_INFO": {
        0: {"name": "gauge_id", "meaning": "战力槽 ID（主键；CForceGaugeTable）", "display_name": "战力槽 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "gauge_name", "meaning": "战力槽名称参数（u32 col1）", "display_name": "名称参数", "confidence": "○ASM确证", "status": "partial"},
        2: {"name": "max_value", "meaning": "槽最大值（u32 col2）", "display_name": "最大值", "confidence": "○ASM确证", "status": "partial"},
        3: {"name": "recover_rate", "meaning": "恢复速率（u32 col3）", "display_name": "恢复速率", "confidence": "△", "status": "partial"},
        4: {"name": "decay_rate", "meaning": "衰减速率（u32 col4）", "display_name": "衰减速率", "confidence": "△", "status": "partial"},
        5: {"name": "trigger_threshold", "meaning": "触发阈值（u32 col5）", "display_name": "触发阈值", "confidence": "△", "status": "partial"},
        6: {"name": "effect_id", "meaning": "关联效果 ID（u32 col6）", "display_name": "效果 ID", "confidence": "△", "status": "partial"},
        7: {"name": "display_order", "meaning": "UI 排序（u32 col7）", "display_name": "排序", "confidence": "△", "status": "partial"},
        8: {"name": "gauge_label", "meaning": "战力槽显示标签（wstring col8）", "display_name": "显示标签", "confidence": "★确证", "status": "confirmed", "type": "str"},
        9: {"name": "icon_id", "meaning": "图标 ID（u32 col9）", "display_name": "图标 ID", "confidence": "○ASM确证", "status": "partial"},
        10: {"name": "color_code", "meaning": "UI 颜色编码（u32 col10）", "display_name": "颜色编码", "confidence": "△", "status": "partial"},
        11: {"name": "buff_id", "meaning": "满槽触发 Buff ID（u32 col11 → BUFF）", "display_name": "Buff ID", "confidence": "△", "status": "partial"},
        12: {"name": "gauge_description", "meaning": "战力槽说明（wstring col12）", "display_name": "说明文本", "confidence": "★确证", "status": "confirmed", "type": "str"},
        13: {"name": "extra_param", "meaning": "扩展参数（u32 col13）", "display_name": "扩展参数", "confidence": "△", "status": "partial"},
    },
    "PLAYER_NAVI": {
        0: {"name": "navi_id", "meaning": "引导步骤 ID（主键；对应 0xF0C4 player_navi_get_list）", "display_name": "引导 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "step_title", "meaning": "引导步骤标题（wstring col1）", "display_name": "步骤标题", "confidence": "★确证", "status": "confirmed", "type": "str"},
        2: {"name": "step_body", "meaning": "引导正文（wstring col2）", "display_name": "引导正文", "confidence": "★确证", "status": "confirmed", "type": "str"},
        3: {"name": "trigger_condition", "meaning": "触发条件码（u32 col3）", "display_name": "触发条件", "confidence": "○ASM确证", "status": "partial"},
        4: {"name": "ui_target", "meaning": "UI 锚点/目标控件名（wstring col4）", "display_name": "UI 锚点", "confidence": "★确证", "status": "confirmed", "type": "str"},
        5: {"name": "priority", "meaning": "引导优先级（u32 col5）", "display_name": "优先级", "confidence": "○ASM确证", "status": "partial"},
        6: {"name": "repeat_flag", "meaning": "可重复显示标志（u32 col6）", "display_name": "可重复标志", "confidence": "△", "status": "partial"},
        7: {"name": "next_navi_id", "meaning": "下一步引导 ID（u32 col7；链式教程）", "display_name": "下一步 ID", "confidence": "○ASM确证", "status": "partial"},
    },
    "BYWORD": {
        0: {"name": "byword_id", "meaning": "称号 ID（主键；机师记录 byword u16 字段引用）", "display_name": "称号 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "display_order", "meaning": "显示排序（u32 col1）", "display_name": "显示排序", "confidence": "○ASM确证", "status": "confirmed"},
        2: {"name": "prefix_text", "meaning": "称号前缀文本（wstring col2）", "display_name": "前缀文本", "confidence": "★确证", "status": "confirmed", "type": "str"},
        3: {"name": "suffix_text", "meaning": "称号后缀文本（wstring col3）", "display_name": "后缀文本", "confidence": "★确证", "status": "confirmed", "type": "str"},
        4: {"name": "title_text", "meaning": "称号主文本（wstring col4）", "display_name": "主文本", "confidence": "★确证", "status": "confirmed", "type": "str"},
        5: {"name": "description", "meaning": "称号说明（wstring col5）", "display_name": "说明", "confidence": "★确证", "status": "confirmed", "type": "str"},
        6: {"name": "byword_type", "meaning": "称号类型（enum col6 sub_570E80；决定显示槽位/颜色）", "display_name": "称号类型", "confidence": "○ASM确证", "status": "confirmed", "type": "enum", "enum_converter": "sub_570E80"},
    },
    "BGMPACKAGE": {
        0: {"name": "package_id", "meaning": "BGM 包 ID（主键；本地表，近亲 settings/bgm.csv BGMパックID）", "display_name": "BGM 包 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "field_bgm_id", "meaning": "战场 BGM ID（col1 → 本地 bgm.csv BGM-ID）", "display_name": "战场 BGM ID", "confidence": "★确证", "status": "confirmed"},
        2: {"name": "ace_bgm_id", "meaning": "Ace 击破 BGM ID（col2）", "display_name": "Ace BGM ID", "confidence": "★确证", "status": "confirmed"},
        3: {"name": "bgm_asset_path", "meaning": "BGM 资源路径/备注（wstring col3）", "display_name": "资源路径", "confidence": "★确证", "status": "confirmed", "type": "str"},
        4: {"name": "force_bgm_enabled", "meaning": "强制 BGM 开关（bool col4>0）", "display_name": "强制 BGM", "confidence": "★确证", "status": "confirmed", "type": "bool"},
        5: {"name": "ace_bgm_enabled", "meaning": "Ace BGM 开关（bool col5>0）", "display_name": "Ace BGM", "confidence": "★确证", "status": "confirmed", "type": "bool"},
        6: {"name": "field_bgm_enabled", "meaning": "战场 BGM 开关（bool col6>0）", "display_name": "战场 BGM", "confidence": "★确证", "status": "confirmed", "type": "bool"},
    },
    "BANNER_INFO": {
        0: {"name": "banner_id", "meaning": "公告横幅 ID（主键；资源 interface/）", "display_name": "横幅 ID", "confidence": "★确证", "status": "confirmed"},
        1: {"name": "display_scene", "meaning": "显示场景（enum col1；大厅/战斗/登录等，转换函数未导出字面量）", "display_name": "显示场景", "confidence": "○ASM确证", "status": "partial", "type": "enum"},
        2: {"name": "banner_type", "meaning": "横幅类型（enum col2）", "display_name": "横幅类型", "confidence": "○ASM确证", "status": "partial", "type": "enum"},
        3: {"name": "priority", "meaning": "显示优先级（enum col3）", "display_name": "优先级", "confidence": "○ASM确证", "status": "partial", "type": "enum"},
        4: {"name": "link_type", "meaning": "链接类型（enum col4）", "display_name": "链接类型", "confidence": "○ASM确证", "status": "partial", "type": "enum"},
        5: {"name": "image_path", "meaning": "横幅图片路径（str col5 sub_BBB4F0；→ interface/ 资源）", "display_name": "图片路径", "confidence": "★确证", "status": "confirmed", "type": "str"},
        6: {"name": "display_duration", "meaning": "显示时长/轮播权重（enum col6）", "display_name": "显示时长", "confidence": "○ASM确证", "status": "partial", "type": "enum"},
        7: {"name": "link_url_id", "meaning": "跳转链接 ID（u32 col7）", "display_name": "链接 ID", "confidence": "○ASM确证", "status": "partial"},
    },
}

# shared challenge reward columns (CLAN/TROOP/NETCAFE)
for _tbl, _enum, _enum_doc in (
    ("CLAN_CHALLENGE", "sub_571D00", STAT_46_CLAN),
    ("TROOP_CHALLENGE", "sub_592DB0", STAT_46_TROOP),
    ("NETCAFE_CHALLENGE", "sub_5874A0", STAT_46_NETCAFE),
):
    for _ci, _patch in {
        11: {"name": "reward_gp", "meaning": "达成奖励 GP（u32 col11）", "display_name": "奖励 GP", "confidence": "△", "status": "partial"},
        12: {"name": "reward_item_id", "meaning": "达成奖励物品 ID（u32 col12 → ITEM）", "display_name": "奖励物品 ID", "confidence": "△", "status": "partial"},
        14: {"name": "reward_qty", "meaning": "奖励物品数量（u32 col14）", "display_name": "奖励数量", "confidence": "△", "status": "partial"},
        15: {"name": "bonus_point", "meaning": "附加点数/积分（u32 col15）", "display_name": "附加积分", "confidence": "△", "status": "partial"},
        17: {"name": "bonus_param", "meaning": "附加奖励参数（u32 col17）", "display_name": "附加参数", "confidence": "△", "status": "partial"},
    }.items():
        if _ci not in SEMANTICS.get(_tbl, {}):
            SEMANTICS.setdefault(_tbl, {})[_ci] = _patch

# PLAYER_NAVI extra columns
for _ci, _patch in {
    8: {"name": "screen_id", "meaning": "触发界面 ID（u32 col8）", "display_name": "界面 ID", "confidence": "△", "status": "partial"},
    9: {"name": "min_level", "meaning": "最低机师等级要求（u32 col9）", "display_name": "最低等级", "confidence": "△", "status": "partial"},
    10: {"name": "max_level", "meaning": "最高机师等级（u32 col10；0=不限）", "display_name": "最高等级", "confidence": "△", "status": "partial"},
    11: {"name": "mission_id", "meaning": "关联任务 ID（u32 col11）", "display_name": "任务 ID", "confidence": "△", "status": "partial"},
    12: {"name": "dialog_style", "meaning": "对话框样式（u32 col12）", "display_name": "对话框样式", "confidence": "△", "status": "partial"},
    13: {"name": "voice_id", "meaning": "语音 ID（u32 col13）", "display_name": "语音 ID", "confidence": "△", "status": "partial"},
    14: {"name": "image_id", "meaning": "插图资源 ID（u32 col14）", "display_name": "插图 ID", "confidence": "△", "status": "partial"},
    15: {"name": "skip_allowed", "meaning": "允许跳过标志（u32 col15）", "display_name": "允许跳过", "confidence": "△", "status": "partial"},
}.items():
    SEMANTICS.setdefault("PLAYER_NAVI", {})[_ci] = _patch

# LVUP_PILOT_CLASS extra - read from json indices
for _ci, _patch in {
    5: {"name": "requirement_type", "meaning": "需求类型（enum col5）", "display_name": "需求类型", "confidence": "△", "status": "partial"},
    6: {"name": "requirement_param", "meaning": "需求参数（u32 col6）", "display_name": "需求参数", "confidence": "△", "status": "partial"},
    7: {"name": "reward_gp", "meaning": "升阶奖励 GP（u32 col7）", "display_name": "奖励 GP", "confidence": "△", "status": "partial"},
    8: {"name": "reward_item_id", "meaning": "升阶奖励物品 ID（u32 col8）", "display_name": "奖励物品", "confidence": "△", "status": "partial"},
    9: {"name": "unlock_byword_id", "meaning": "解锁称号 ID（u32 col9 → BYWORD）", "display_name": "解锁称号", "confidence": "△", "status": "partial"},
}.items():
    SEMANTICS.setdefault("LVUP_PILOT_CLASS", {})[_ci] = _patch

# LVUP_FAVMS extra
for _ci, _patch in {
    3: {"name": "bonus_param_a", "meaning": "爱机加成参数 A（u32 col3）", "display_name": "加成参数 A", "confidence": "△", "status": "partial"},
    4: {"name": "bonus_param_b", "meaning": "爱机加成参数 B（u32 col4）", "display_name": "加成参数 B", "confidence": "△", "status": "partial"},
    5: {"name": "unlock_msma_id", "meaning": "解锁机体 ID（u32 col5）", "display_name": "解锁机体", "confidence": "△", "status": "partial"},
}.items():
    SEMANTICS.setdefault("LVUP_FAVMS", {})[_ci] = _patch

PURPOSE_PATCHES = {
    "AUTOEXEC": "服务端启动脚本（autoexec_sv.cfg 脚本方言，**不是 CSV**；控制服务端初始化、表加载顺序与调试开关）",
    "OVER_CUSTOM": "机体超改（Over Custom）方案：按机体+阶段定义点数消耗与能力加成",
    "DAILY_RECORD": "机师每日战绩统计定义：46 项战斗统计 + 铜/银/金绶带阈值（与 badge_config 同源）",
    "CLAN_CHALLENGE": "部队（Clan）挑战：部队全员累计 46 项战绩达成目标后发放奖励",
    "TROOP_CHALLENGE": "势力挑战（联邦/吉翁）：阵营维度累计战绩挑战",
    "NETCAFE_CHALLENGE": "网吧挑战：网吧登录用户的专属战绩挑战",
    "PLAY_BONUS_REWARD": "游玩场次/时长奖励：按战斗模式过滤的发放规则",
    "MONTHLY_BONUS_REWARD": "月度登录奖励：按年月+日序+渠道发放 GP/物品",
    "FORCEGAUGE_INFO": "战力槽（Force Gauge）定义：战斗内蓄力槽最大值/恢复/触发 Buff",
    "PLAYER_NAVI": "新手引导（Navi）步骤链：UI 锚点 + 触发条件 + 链式 next_id",
    "TREND_DATA_WEAPON": "武器流行趋势数据：使用率/胜率/选取率统计（推荐配装参考）",
    "SCORE_CONFIG_CATEGORY": "任务计分分类：将 score_config 计分项按类别分组",
}


def load_enums() -> dict:
    if ENUMS_JSON.is_file():
        return json.loads(ENUMS_JSON.read_text(encoding="utf-8"))
    return {}


def enum_values(enums: dict, fn: str) -> list[dict] | None:
    r = enums.get(fn)
    if not r:
        return None
    if r.get("shape") == "table" and r.get("table"):
        return [{"name": n, "value": v} for n, v in r["table"]]
    lits, consts = r.get("lits") or [], r.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    return None


def apply_semantics(data: dict, enums: dict) -> int:
    tid = data["id"]
    patches = SEMANTICS.get(tid, {})
    if tid in PURPOSE_PATCHES:
        data["purpose"] = PURPOSE_PATCHES[tid]
    n = 0
    for col in data.get("columns", []):
        idx = col.get("csv_index")
        if idx is None or idx not in patches:
            continue
        p = patches[idx]
        for k, v in p.items():
            if col.get(k) != v:
                col[k] = v
                n += 1
        col["db_column"] = p.get("name", col.get("db_column"))
        if p.get("display_name"):
            col["display_name"] = p["display_name"]
        if p.get("confidence"):
            col["confidence"] = p["confidence"]
        fn = col.get("enum_converter")
        if fn:
            vals = enum_values(enums, fn)
            if vals:
                col["enum_values"] = vals
                col["enum_doc"] = ENUM_DOC
    # stats
    cols = data.get("columns", [])
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_pending"] = sum(1 for c in cols if c.get("status") == "pending")
    data["column_gap"] = sum(1 for c in cols if c.get("status") == "gap")
    data["column_defined"] = len(cols)
    return n


def fmt_type(col: dict) -> str:
    t = col.get("type", "u32")
    fn = col.get("enum_converter")
    if t == "enum" and fn:
        return f"enum `{fn}`"
    if t == "str":
        return "str"
    if t == "float":
        return "float"
    if t == "bool":
        return "bool"
    if t in ("u8", "u16"):
        return t
    return "u32"


def write_md(data: dict) -> None:
    md_path = ROOT / data.get("source_md", "")
    if not md_path.is_file():
        md_path = DATATABLES / Path(data["source_md"]).name
    tid = data["id"]
    csv_path = data.get("csv_path", "")
    purpose = data.get("purpose", "")
    asm = data.get("asm_reader") or "None"
    cc = data.get("column_count", 0)

    if tid == "AUTOEXEC":
        content = f"""# AUTOEXEC ｜ `{csv_path}`

- **用途**：{purpose}
- 表ID `{data.get('table_id', '0')}` ｜ 下载序 `{data.get('download_order', '0')}` ｜ disposition `{data.get('disposition', 'SCRIPT')}`
- **不是 CSV 数据表**：无列定义；服务端启动时按脚本方言执行（见 `server/autoexec_sv.cfg`）

> 本表无需列定义。脚本控制：表加载、调试开关、服务端初始化流程。

**填写规则**：
- 文件编码 **UTF-8**；`#` 开头为注释行
- 语法为服务端 autoexec 脚本方言（非 CSV 列格式）
"""
        md_path.write_text(content, encoding="utf-8")
        return

    lines = [
        f"# {tid} ｜ `{csv_path}`",
        "",
        f"- **用途**：{purpose}",
        f"- 表ID `{data.get('table_id', '')}` ｜ 下载序 `{data.get('download_order', '')}` "
        f"｜ 类名 `{data.get('class_name', '')}` ｜ disposition `{data.get('disposition', '')}`",
        f"- 逐列读取函数 `{asm}` ｜ **列数 {cc}**",
        "",
        "| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |",
        "|---|---|---|---|---|---|",
    ]
    for col in sorted(
        [c for c in data.get("columns", []) if c.get("read_order") is not None],
        key=lambda c: c.get("read_order") or 0,
    ):
        ro = col.get("read_order", "")
        ci = col.get("csv_index", "")
        name = col.get("name", "")
        typ = fmt_type(col)
        mem = col.get("memory_offset")
        mem_s = f"+{mem}" if mem is not None else "—"
        meaning = col.get("meaning", "")
        conf = col.get("confidence", "")
        if conf:
            meaning = f"{meaning}"
        lines.append(f"| {ro} | `{ci}` | `{name}` | {typ} | {mem_s} | {meaning} |")

    gap_cols = [c for c in data.get("columns", []) if c.get("status") == "gap"]
    if gap_cols:
        lines.extend(["", "**Gap 列**（CSV 存在但读表函数跳过，默认 0）："])
        for c in gap_cols:
            lines.append(f"- CSV `{c.get('csv_index')}`：{c.get('meaning', 'reserved')}")

    lines.extend([
        "",
        "**填写规则**：",
        "- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。",
        "- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。",
        "- **越界列 = 0**：只需写到最大列号，后面可省略。",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    import sys
    md_only = "--md-only" in sys.argv
    enums = load_enums()
    for tid in TABLE_IDS:
        path = TABLES_DIR / f"{tid}.json"
        if not path.is_file():
            print(f"SKIP missing {tid}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        n = 0 if md_only else apply_semantics(data, enums)
        if not md_only:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_md(data)
        confirmed = data.get("column_confirmed", 0)
        partial = data.get("column_partial", 0)
        print(f"  {tid}: {n} patches | confirmed={confirmed} partial={partial}")


if __name__ == "__main__":
    main()
