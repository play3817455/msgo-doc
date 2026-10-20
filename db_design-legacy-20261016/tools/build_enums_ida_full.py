#!/usr/bin/env python3
"""Merge enums.json + IDA metadata into schema/cfg/enums_ida.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUMS_IDA_OUT = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enums_ida.json"
GLOSSARY = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "enum_glossary_zh.json"
TABLES_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "tables"

# IDA-verified: fn -> metadata
IDA_META: dict[str, dict] = {
    "sub_402310": {"kind": "string_copy", "asm_va": "0x402310", "title_zh": "CSV 窄串拷贝", "desc_zh": "std::string 子串拷贝；用于路径/模块名/开关字符串列。", "ida_note": "sub_402310(this,a2,offset,len) → sub_CC52A2 拷贝。"},
    "sub_CC6CA8": {"kind": "int_parse", "asm_va": "0xCC6CA8", "title_zh": "整型解析 (strtol)", "desc_zh": "sub_CC6CA8→sub_CC6F5A→sub_CC6D2F。", "ida_note": "解析十/八/十六进制整数字符串。"},
    "sub_CC7056": {"kind": "float_parse", "asm_va": "0xCC7056", "title_zh": "浮点解析 (strtod)", "desc_zh": "CSV 角度/小数 → double；AI 武器俯仰再转弧度。", "ida_note": "sub_CC7056→sub_CC6FAD。"},
    "sub_BBB4F0": {"kind": "banner_row_lookup", "asm_va": "0xBBB4F0", "title_zh": "Banner 行图片路径", "desc_zh": "按行号从 banner 表取图片路径。", "ida_note": "sub_456D90→sub_BBB250。"},
    "sub_40CE20": {"kind": "string_equal", "asm_va": "0x40CE20", "title_zh": "字符串相等比较", "desc_zh": "通用 strcmp 链：YES/NO、阵营、模式名等（同一函数多种 CSV 语义）。", "ida_note": "多列复用；表详情页不展开全量取值。"},
    "sub_5812E0": {"kind": "table_lookup", "asm_va": "0x5812E0", "title_zh": "战斗明细属性名", "desc_zh": "MSMA_BATTLE_DETAIL 属性名→子表编号；词表 sub_57BD40。", "data_refs": ["off_D7A298", "dword_D7A29C", "sub_57BD40"], "ida_note": "sub_596780 红黑树查属性名节点。"},
    "sub_570950": {"asm_va": "0x570950", "data_refs": ["off_D77BA8", "dword_D77BAC"], "title_zh": "弹药/对象伤害属性", "desc_zh": "bullet.csv damage_type 词表。"},
    "sub_570E80": {"asm_va": "0x570E80", "title_zh": "称号/口令类型", "desc_zh": "byword.csv col6。"},
    "sub_571290": {"asm_va": "0x571290", "data_refs": ["off_D77D38", "dword_D77D3C"], "title_zh": "模型装备挂点", "desc_zh": "msma_model col53 持握/挂点类型。"},
    "sub_570660": {"asm_va": "0x570660", "data_refs": ["off_D77A68", "dword_D77A6C"], "title_zh": "Buff 类别", "desc_zh": "buff.csv col7。"},
    "sub_5703A0": {"asm_va": "0x5703A0", "title_zh": "奖励类型", "desc_zh": "beginner_challenge 奖励：GP/ITEM/MSMA/BUILDUP_MSMA。"},
    "sub_572C30": {"asm_va": "0x572C30", "data_refs": ["off_D78084", "dword_D78088"], "title_zh": "势力", "desc_zh": "commander_npc col5：NEUTRAL/EFF/ZEON。"},
    "sub_572CD0": {"asm_va": "0x572CD0", "data_refs": ["off_D780B0", "dword_D780B4"], "title_zh": "支援呼叫类型", "desc_zh": "commander_npc col18 支援技能类型。"},
    "sub_577F50": {"asm_va": "0x577F50", "title_zh": "扭蛋播放限制", "desc_zh": "gacha col29：PLAY_BUNDLE_BC_ONLY。"},
    "sub_577FF0": {"asm_va": "0x577FF0", "title_zh": "免费扭蛋包", "desc_zh": "gacha col31：FREE_PLAY_BUNDLE。"},
    "sub_578130": {"asm_va": "0x578130", "data_refs": ["off_D790E4", "dword_D790E8"], "title_zh": "扭蛋抽取模式", "desc_zh": "NORMAL/SINGLE/SINGLE_NORESET。"},
    "sub_578EE0": {"asm_va": "0x578EE0", "title_zh": "登录平台等级", "desc_zh": "lvup_clan col6：ROKAKU_LV0..5（索引 0..5）。"},
    "sub_5790B0": {"asm_va": "0x5790B0", "title_zh": "商店等级", "desc_zh": "lvup_clan col8：SHOP_LV0..21。"},
    "sub_579500": {"asm_va": "0x579500", "title_zh": "卡组 COST 等级", "desc_zh": "lvup_clan col9：DECKCOST_LV0..5。"},
    "sub_5796D0": {"asm_va": "0x5796D0", "title_zh": "折扣等级", "desc_zh": "lvup_clan col11：DISCOUNT_LV0..10。"},
    "sub_579FC0": {"asm_va": "0x579FC0", "data_refs": ["off_D79430", "dword_D79434"], "title_zh": "成长统计项", "desc_zh": "lvup_exam col1 统计/战绩项。"},
    "sub_57BDE0": {"asm_va": "0x57BDE0", "title_zh": "分解稀有度", "desc_zh": "msma_breakup col3：GOLD/SILVER/PLATINUM。"},
    "sub_580560": {"asm_va": "0x580560", "data_refs": ["off_D7ACA8", "dword_D7ACB0"], "title_zh": "机体系列位标志", "desc_zh": "msma_settings col8 系列 bitmask。"},
    "sub_5806B0": {"asm_va": "0x5806B0", "title_zh": "实体类别", "desc_zh": "msma_settings col35 地图实体类型。"},
    "sub_580BA0": {"asm_va": "0x580BA0", "data_refs": ["off_D7B2B8", "off_D7B2C0", "dword_D7B2BC"], "title_zh": "可部署对象", "desc_zh": "msma_settings col48。"},
    "sub_580C40": {"asm_va": "0x580C40", "title_zh": "出生后控制器选择", "desc_zh": "582390 CSV49经580C40写CHARA_PARAM+416：NORMAL=1、MA=2、AAG=4、BATTERY=10、BATTLESHIP=11、MARCH=15；空值及未匹配文本默认NORMAL=1，精确比较不去空格。4C2D20→4BFF00自身type=3初始化及6729F0普通finishRespawn分支把此值交给容器虚表+48→4C9A80选择自身控制器；1选择4EAFB0普通SelfTargetView，2选择4DDE90变体。该switch未处理15，其他调用场景/逐机体原服值未穷举。旧“系列分类”名称不足以描述已确认运行用途；保留物理DB列名series_class。不能将空值当作零控制器，也不据此证明现场落地。"},
    "sub_5804F0": {"asm_va": "0x5804F0", "data_refs": ["off_D7A8B0", "dword_D7A8B4"], "title_zh": "战斗角色/扩展角色", "desc_zh": "msma_settings col7：ASSAULT/SNIPE/CANNON/SUPPORT 及 EX_*。"},
    "sub_5854E0": {"asm_va": "0x5854E0", "title_zh": "发行区域", "desc_zh": "JAPAN/CHINA/ALL。"},
    "sub_58B5A0": {"asm_va": "0x58B5A0", "title_zh": "VIP 配色门槛", "desc_zh": "msma_color_set col19 VIP 等级（NONE/VIP_ASSOCIATE…VIP_MASTER）；别与发行区域 sub_5854E0 混淆。"},
    "sub_594230": {"asm_va": "0x594230", "data_refs": ["off_D7CBB0", "dword_D7CBB4"], "title_zh": "素材部位", "desc_zh": "MSMA_MATERIAL 部位类型。"},
    "sub_595870": {"asm_va": "0x595870", "data_refs": ["off_D7DED8", "dword_D7DEDC"], "title_zh": "机体仓库类型", "desc_zh": "MSMA_STORAGE/MSMA_DECKCOST。"},
    "sub_59FB20": {"asm_va": "0x59FB20", "title_zh": "子模式", "desc_zh": "mission_vs col17 特殊规则。"},
    "sub_56E570": {"asm_va": "0x56E570", "data_refs": ["off_D77428", "dword_D7742C"], "title_zh": "AI 原则", "desc_zh": "ai_param col1。"},
    "sub_56E610": {"asm_va": "0x56E610", "data_refs": ["off_D77558", "dword_D7755C"], "title_zh": "回避倾向", "desc_zh": "ai_param col2。"},
    "sub_56E750": {"asm_va": "0x56E750", "data_refs": ["off_D77620", "dword_D77624"], "title_zh": "交战距离档", "desc_zh": "NEAR/MIDDLE/FAR/SHIELD。"},
    "sub_56E7F0": {"asm_va": "0x56E7F0", "data_refs": ["off_D77648", "dword_D7764C"], "title_zh": "武器槽位", "desc_zh": "MAIN/EX/SUB1。"},
    "sub_56F3A0": {"asm_va": "0x56F3A0", "data_refs": ["off_D7838C", "dword_D78390"], "title_zh": "格斗方向", "desc_zh": "wrestle col17。"},
    "sub_56F4B0": {"asm_va": "0x56F4B0", "data_refs": ["off_D776B4", "dword_D776B8"], "title_zh": "格斗类型", "desc_zh": "wrestle col7。"},
    "sub_571D00": {"asm_va": "0x571D00", "data_refs": ["off_D77DC8", "dword_D77DCC"], "title_zh": "网咖挑战统计项", "desc_zh": "netcafe_challenge col2。"},
    "sub_575A60": {"asm_va": "0x575A60", "data_refs": ["off_D7838C", "dword_D78390"], "title_zh": "伤害场来源", "desc_zh": "damage_field col4。"},
    "sub_578090": {"asm_va": "0x578090", "data_refs": ["off_D79070", "dword_D79074"], "title_zh": "消耗货币", "desc_zh": "gacha col4 GP/CP 等。"},
    "sub_578C50": {"asm_va": "0x578C50", "title_zh": "机械师等级项", "desc_zh": "lvup_clan col3 cmp-chain。"},
    "sub_57A890": {"asm_va": "0x57A890", "data_refs": ["off_D79738", "dword_D7973C"], "title_zh": "经验券加成类型", "desc_zh": "lvup_pilot col35..38。"},
    "sub_57E1D0": {"asm_va": "0x57E1D0", "data_refs": ["off_D7A3BC", "dword_D7A3C0"], "title_zh": "任务单位职能", "desc_zh": "msma_missionunit col3。"},
    "sub_580610": {"asm_va": "0x580610", "data_refs": ["off_D7B0B0", "dword_D7B0B4"], "title_zh": "阶级 Rank", "desc_zh": "RANK1..RANK5。"},
    "sub_585580": {"asm_va": "0x585580", "title_zh": "装备组合方式", "desc_zh": "weapon_equipcomb col2。"},
    "sub_585FD0": {"asm_va": "0x585FD0", "data_refs": ["off_D7B808", "dword_D7B80C"], "title_zh": "武器类型", "desc_zh": "武装大类 28 项。"},
    "sub_586450": {"asm_va": "0x586450", "title_zh": "武器槽类别", "desc_zh": "MAIN/EX/0。"},
    "sub_5874A0": {"asm_va": "0x5874A0", "data_refs": ["off_D7B9F0", "dword_D7B9F4"], "title_zh": "部队挑战统计项", "desc_zh": "troop_challenge col2。"},
    "sub_587540": {"asm_va": "0x587540", "data_refs": ["off_D7BB80", "dword_D7BB84"], "title_zh": "网咖等级奖励", "desc_zh": "netcafe col 等级档。"},
    "sub_592DB0": {"asm_va": "0x592DB0", "data_refs": ["off_D7C808", "dword_D7C80C"], "title_zh": "战斗统计项", "desc_zh": "score/challenge 统计名。"},
    "sub_593770": {"asm_va": "0x593770", "data_refs": ["off_D7C9B8", "dword_D7C9BC"], "title_zh": "商品类型", "desc_zh": "item.csv col4。"},
    "sub_5951D0": {"asm_va": "0x5951D0", "data_refs": ["off_D7CC28", "dword_D7CC2C"], "title_zh": "装备触发时机", "desc_zh": "equip_parts 触发条件 23 项。"},
    "sub_5952C0": {"asm_va": "0x5952C0", "data_refs": ["off_D7CE40", "dword_D7CE44"], "title_zh": "装备作用范围", "desc_zh": "equip_parts col16。"},
    "sub_5953B0": {"asm_va": "0x5953B0", "data_refs": ["off_D7D158", "dword_D7D15C"], "title_zh": "装备/道具效果名", "desc_zh": "equip_parts col17 效果 ID 129 项。"},
    "sub_5954A0": {"asm_va": "0x5954A0", "data_refs": ["off_D7DEB0", "dword_D7DEB4"], "title_zh": "配置对象大类", "desc_zh": "MS/WEAPON/ARMOR/OTHER。"},
    "sub_5964A0": {"asm_va": "0x5964A0", "data_refs": ["off_D7DFE8", "dword_D7DFEC"], "title_zh": "弹种属性", "desc_zh": "实弹/光束/爆炸/即死。"},
    "sub_596510": {"asm_va": "0x596510", "title_zh": "散布模式", "desc_zh": "weapon_settings col29 cmp-chain。"},
    "sub_5965F0": {"asm_va": "0x5965F0", "title_zh": "连射模式", "desc_zh": "weapon_settings col31 cmp-chain。"},
    "sub_5968A0": {"asm_va": "0x5968A0", "data_refs": ["off_D7E0D8", "dword_D7E0DC"], "title_zh": "装备槽位", "desc_zh": "weapon_settings col13。"},
    "sub_596990": {"asm_va": "0x596990", "data_refs": ["off_D7E160", "dword_D7E164"], "title_zh": "格斗细分类", "desc_zh": "weapon_settings col15。"},
    "sub_596A80": {"asm_va": "0x596A80", "data_refs": ["off_D7E298", "dword_D7E29C"], "title_zh": "攻击属性", "desc_zh": "weapon_settings col16。"},
    "sub_596B70": {"asm_va": "0x596B70", "data_refs": ["off_D7E308", "dword_D7E30C"], "title_zh": "武器子类型", "desc_zh": "weapon_settings col21 52 项。"},
    "sub_596C60": {"asm_va": "0x596C60", "data_refs": ["off_D7E630", "dword_D7E634"], "title_zh": "伤害类型", "desc_zh": "weapon_settings col30。"},
    "sub_596D50": {"asm_va": "0x596D50", "data_refs": ["off_D7E7F0", "dword_D7E7F4"], "title_zh": "锁定状态", "desc_zh": "weapon_settings col128。"},
    "sub_596E40": {"asm_va": "0x596E40", "data_refs": ["off_D7E930", "dword_D7E934"], "title_zh": "武器扩展枚举", "desc_zh": "weapon_settings col146。"},
    "sub_59E070": {"asm_va": "0x59E070", "title_zh": "任务扩展规则类型", "desc_zh": "mission_ext_rule col2。"},
    "sub_59E0F0": {"asm_va": "0x59E0F0", "title_zh": "任务扩展参数 A", "desc_zh": "mission_ext_rule col3/4。"},
    "sub_59FA70": {"asm_va": "0x59FA70", "title_zh": "对战模式", "desc_zh": "mission_vs col16。"},
    "sub_5A2CC0": {"asm_va": "0x5A2CC0", "data_refs": ["off_D7EC0C", "dword_D7EC10"], "title_zh": "动作模块类型", "desc_zh": "ATTACK/DEFENSE/MOVE/SPECIAL。"},
}

# Manual / decompile-only values not in enums.json tables
MANUAL_VALUES: dict[str, list[tuple[str, int]]] = {
    "sub_5703A0": [("GP", 999), ("ITEM", 0), ("MSMA", 1), ("BUILDUP_MSMA", 998)],
    "sub_577F50": [("PLAY_BUNDLE_BC_ONLY", 1)],
    "sub_577FF0": [("FREE_PLAY_BUNDLE", 1)],
    "sub_578EE0": [(f"ROKAKU_LV{i}", i) for i in range(6)],
    "sub_5790B0": [(f"SHOP_LV{i}", i) for i in range(22)],
    "sub_579500": [(f"DECKCOST_LV{i}", i) for i in range(6)],
    "sub_5796D0": [(f"DISCOUNT_LV{i}", i) for i in range(11)],
    "sub_57BDE0": [("GOLD", 1), ("SILVER", 2), ("PLATINUM", 3)],
    "sub_59FB20": [("RPOST_DIFF", 10), ("DOT_DMG", 11), ("BATTLEAREA", 12), ("HEADQUARTERS", 13), ("CONQUEST", 14)],
    "sub_572C30": [("NEUTRAL", 0xFFFFFFFF), ("EFF", 0), ("ZEON", 1)],
    "sub_578130": [("NORMAL", 0), ("SINGLE", 1), ("SINGLE_NORESET", 2)],
    "sub_594230": [
        ("ARMOR", 0), ("GENERATOR", 1), ("FRAME", 2), ("MANIPULATOR", 3),
        ("SENSOR", 4), ("THRUSTER", 5), ("SPECIAL", 6),
    ],
    "sub_595870": [("MSMA_STORAGE", 1), ("MSMA_DECKCOST", 2)],
    "sub_579FC0": [
        ("VERSUS", 1), ("VERSUS_XWAR", 2), ("VERSUS_COMMANDER", 3), ("WIN", 4),
        ("WIN_XWAR", 5), ("WIN_COMMANDER", 6), ("KILL", 7), ("KILL_WRESTLE", 8),
        ("KILL_SHOT", 9), ("KILL_CANNON", 10), ("KILL_THROW", 11), ("KILL_DEPARMS", 12),
        ("KILL_ASSIST", 13), ("SCORE_ATK", 14), ("SCORE_SPT", 15), ("SCORE_CON", 16),
        ("SCORE_TOTAL", 17), ("SCORE_ASSAULT_A", 18), ("SCORE_ASSAULT_B", 19),
        ("SCORE_SNIPE", 20), ("SCORE_CANNON", 21), ("SCORE_SUPPORT", 22),
        ("RESULT_GOLD", 23), ("RESULT_GOLD_RANK", 24), ("RESULT_GOLD_SCORE", 25),
        ("RESULT_GOLD_DSS", 26), ("RESULT_GOLD_CONQUER", 27), ("RESULT_SILVER_RANK", 28),
        ("RESULT_SILVER_SCORE", 29), ("RESULT_BRONZE_RANK", 30), ("RESULT_BRONZE_SCORE", 31),
        ("RESULT_BLUE_RANK", 32), ("RESULT_BLUE_SCORE", 33), ("SEARCH", 34), ("RESURRECT", 35),
        ("MOVE_LEN", 36), ("RESPAWN_DEFEAT", 37), ("RESPAWN_CONQUER", 38), ("DMG_STGHOLD", 39),
        ("DMG_BTLSHIP", 40), ("DMG_TENDER", 41), ("DMG_ACE", 42), ("MAPOBJ_KILL", 43),
        ("BATTERY_KILL", 44), ("CONTAINER", 45), ("PROTECT", 46), ("STGARMS_SET", 47),
        ("STGARMS_LEN", 48), ("ORDER_COMP_PL", 49), ("BADGE_GET", 50), ("DESTROY_STGHOLD", 51),
    ],
    "sub_570660": [
        ("MISSION_EXP_UP", 1), ("MISSION_GP_UP", 2), ("MISSION_RITEM_UP", 3),
        ("MISSION_RARE_POP", 4), ("RESPAWN_TIME_CUT", 5), ("MSMA_PARAM_UP", 6),
        ("SACRIFICE", 7), ("ALLOY_CHIP_GET", 8), ("BUILDUP_UP", 50),
        ("LIMITEDTIME_AVATAR", 51), ("LIMITEDTIME_MS_COLOR", 52),
        ("LIMITEDTIME_MS_EMBLEM", 53),
    ],
    "sub_572CD0": [
        ("BOMB", 0), ("CARPET_BOMB", 1), ("TENDER", 2), ("SEARCH", 3), ("MINOVSKY", 4),
        ("SOLAR_RAY", 5), ("SUMMON_MA", 6), ("SUMMON_ACE", 7), ("BATTLE_SHIP", 8),
        ("ASSAULT_SHIP", 9), ("ORATION", 10), ("PATROL_AIRCRAFT", 11), ("AAG", 12),
        ("GUNTURRET", 13), ("EQPARTS_EXEC_A", 14), ("EQPARTS_EXEC_B", 15),
        ("EQPARTS_EXEC_C", 16), ("EQPARTS_EXEC_D", 17), ("EQPARTS_EXEC_E", 18),
        ("GRENADE_NET", 19), ("GRENADE_TUMBLE", 20), ("WALL", 21), ("DUMMY_BEACON", 22),
        ("TRANSPORT_SHIP", 23), ("STGARMS_OLD", 24), ("STGARMS1", 25), ("STGARMS2", 26),
        ("SUBFLIGHT", 27), ("ASSAULT_STGHOLD", 28), ("RIDE_ACE", 29), ("JAMMING", 30),
    ],
    "sub_5804F0": [
        ("ASSAULT_A", 1), ("ASSAULT_B", 2), ("SNIPE", 3), ("CANNON", 4), ("SUPPORT", 5),
        ("EX_STRONGHOLD", 6), ("EX_RESPAWNPOST", 7), ("EX_DEPLOY_ARMS", 8), ("EX_ITEMBOX", 9),
        ("EX_BOMB", 10), ("EX_TENDER", 11), ("EX_SEARCH", 12), ("EX_MA", 13),
        ("EX_SOLAR_RAY", 14), ("EX_SHIP", 15), ("EX_ARTILLERY", 16), ("EX_AAG", 17),
        ("EX_CONTAINER", 18), ("EX_STG_ARMS", 19), ("EX_BEACON", 20), ("EX_PATROL_AIRCRAFT", 21),
        ("EX_GUNTURRET", 22), ("EX_SUBFLIGHT", 23), ("EX_SUBFLIGHT_LAND", 24),
        ("EX_BULLET_PACK", 25), ("EX_BREAKABLE_OBJ", 26), ("EX_BREAKABLE_DOOR", 27),
        ("EX_CONTROLLER", 28), ("EX_MOVABLE_FLOOR", 29), ("EX_AIRFERRY", 30), ("EX_DEBRIS", 31),
        ("EX_WEAPON", 32), ("EX_DUMMY_BEACON", 33), ("EX_SVCTRL_MOVEATK", 34),
        ("EX_GUIDE_BEACON", 35), ("EX_STGARMS2", 36), ("EX_GUARDIAN", 37),
        ("EX_MARCH_LEADER", 38), ("EX_STRONGHOLD_AAG", 39),
    ],
}

# Keep existing detailed entries from prior enums_ida (5806B0 etc.)
PRESERVE_CONVERTERS = {
    "sub_5806B0", "sub_580560", "sub_580BA0", "sub_580C40", "sub_570950",
    "sub_570E80", "sub_571290", "sub_5854E0", "sub_58B5A0", "sub_5812E0",
    "sub_402310", "sub_CC6CA8", "sub_CC7056", "sub_BBB4F0",
}


def load_glossary() -> dict:
    if GLOSSARY.is_file():
        return json.loads(GLOSSARY.read_text(encoding="utf-8"))
    return {"global_values": {}, "converters": {}}


def label_zh(name: str, g: dict) -> str:
    gv = g.get("global_values", {})
    if name in gv:
        return gv[name]
    parts = re.split(r"[_\-/]+", name)
    token = {
        "NEAR": "近距", "MIDDLE": "中距", "FAR": "远距", "WIN": "胜利", "KILL": "击杀",
        "SCORE": "分数", "ASSAULT": "突击", "SUPPORT": "支援", "SNIPE": "狙击",
        "VERSUS": "对战", "WRESTLE": "格斗", "DECKCOST": "卡组COST", "DISCOUNT": "折扣",
        "SHOP": "商店", "ROKAKU": "登录平台", "LV": "等级", "EX": "EX", "STG": "关卡",
        "MSMA": "机体", "GP": "GP", "ITEM": "道具", "ANYTIME": "随时", "SPAWN": "生成时",
        "DEATH": "死亡时", "ARMOR": "装甲", "WEAPON": "武器", "BOOST": "BOOST",
    }
    out = []
    for p in parts:
        if p in gv:
            out.append(gv[p])
        elif p in token:
            out.append(token[p])
        elif p.isdigit():
            out.append(p)
        else:
            out.append(p.title() if len(p) <= 4 else p)
    return "·".join(out) if out else name


def values_from_enums_json(entry: dict) -> list[dict]:
    if entry.get("table"):
        return [{"name": n, "value": v} for n, v in entry["table"] if n and n != "-"]
    lits = entry.get("lits") or []
    consts = entry.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    if lits:
        return [{"name": n, "value": i} for i, n in enumerate(lits)]
    return []


def load_registry_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    for p in TABLES_DIR.glob("*.json"):
        tbl = json.loads(p.read_text(encoding="utf-8"))
        for c in tbl.get("columns", []):
            conv = c.get("enum_converter")
            if not conv or conv in titles:
                continue
            dn = c.get("display_name") or c.get("name") or ""
            titles[conv] = re.sub(r"\*+", "", dn).split("（")[0].strip()[:60]
    return titles


def main() -> None:
    existing: dict = {}
    if ENUMS_IDA_OUT.is_file():
        existing = json.loads(ENUMS_IDA_OUT.read_text(encoding="utf-8"))
    preserved = {
        k: v for k, v in existing.get("converters", {}).items() if k in PRESERVE_CONVERTERS
    }

    ej = json.loads(ENUMS_JSON.read_text(encoding="utf-8"))
    glossary = load_glossary()
    reg_titles = load_registry_titles()

    converters: dict[str, dict] = dict(preserved)

    all_keys = sorted(set(IDA_META) | set(ej) | set(preserved))
    for conv in all_keys:
        if conv in preserved:
            continue
        meta = dict(IDA_META.get(conv, {}))
        meta.setdefault("kind", "enum")
        meta.setdefault("asm_va", f"0x{conv[4:].upper()}" if conv.startswith("sub_") else "")
        if conv in reg_titles and not meta.get("title_zh"):
            meta["title_zh"] = reg_titles[conv]

        vals: list[dict] = []
        if conv in MANUAL_VALUES:
            vals = [{"name": n, "value": v, "label_zh": label_zh(n, glossary)} for n, v in MANUAL_VALUES[conv]]
        elif conv in ej:
            vals = values_from_enums_json(ej[conv])
            for v in vals:
                v["label_zh"] = label_zh(v["name"], glossary)
                cv = glossary.get("converters", {}).get(conv, {}).get("values", {})
                if v["name"] in cv:
                    v["label_zh"] = cv[v["name"]]

        if vals:
            meta["values"] = vals
        converters[conv] = meta

    out = {
        "_meta": {
            "source": "GundamOnline_CHINA_v15.exe.i64",
            "extracted": "2026-09-21",
            "method": "enums.json + IDA decompile/data_refs + manual cmp-chain",
            "total_converters": len(converters),
        },
        "converters": dict(sorted(converters.items(), key=lambda x: x[0].lower())),
    }
    ENUMS_IDA_OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {ENUMS_IDA_OUT} with {len(converters)} converters")
    for k, v in converters.items():
        n = len(v.get("values") or [])
        if v.get("kind", "enum") == "enum":
            print(f"  {k}: {n} values")


if __name__ == "__main__":
    main()
