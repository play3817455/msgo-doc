#!/usr/bin/env python3
"""Manual IDA-backed enrichment for cfg table schemas + MD sync."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = ROOT / "db_design" / "schema" / "cfg" / "tables"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUM_CONV = ROOT / "reverse-login-chain" / "formats" / "_enum_conv.json"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"
DATATABLES = ROOT / "datatables" / "01-列注释"

# Later, target-v15 consumer evidence takes precedence over old field labels.
# Keep the repair overlay shared with the server's schema metadata repair.
sys.path.insert(0, str(ROOT / "serverv" / "tools"))
from patch_runtime_ammo_columns import patch_column as patch_weapon_column
from patch_projectile_columns import patch_column as patch_bullet_column

TARGETS = [
    "WEAPON_SETTING",
    "WEAPON_BATTLE_DETAIL",
    "WRESTLE_PARAM",
    "BULLET",
    "BUILDUP_WEAPON",
    "CHARA_PARAM",
    "CHARA_MODEL",
    "DAMAGE_FIELD_PARAM",
    "BUFF",
    "ACTION_MODULE_INFO",
    "AI_PARAM",
]

ASM_GENERIC = re.compile(
    r"^ASM已映射：|整型参数|浮点参数|数值|u32\s*参数|枚举/类别|field_\d+|^unknown_",
    re.I,
)

# csv_index -> overlay fields
OVERLAYS: dict[str, dict[int, dict]] = {
    "BUFF": {
        0: {
            "name": "buff_id",
            "db_column": "buff_id",
            "display_name": "Buff ID",
            "meaning": "主键；CBuffTable 行键（sub_570750 col0→+0）",
            "memory_offset": 0,
            "status": "confirmed",
            "confidence": "★确证",
        },
        1: {
            "name": "linked_buff_id",
            "db_column": "linked_buff_id",
            "display_name": "关联 Buff",
            "meaning": "关联 buff 行 ID（sub_570750 @+4；同表引用或分组）",
            "memory_offset": 4,
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        2: {
            "name": "display_name_str",
            "db_column": "display_name_str",
            "display_name": "显示名",
            "meaning": "Buff 名称窄串（sub_456D90→sub_4029E0 @+8）",
            "memory_offset": 8,
            "status": "confirmed",
            "confidence": "★确证",
        },
        3: {
            "name": "duration_sec",
            "db_column": "duration_sec",
            "display_name": "持续时间",
            "meaning": "效果持续秒数（sub_570750 col3；读入后参与 +36 标志合成）",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        4: {
            "name": "stack_limit",
            "db_column": "stack_limit",
            "display_name": "叠加上限",
            "meaning": "同类别 buff 最大叠加层（sub_570750 col4）",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        5: {
            "name": "priority",
            "db_column": "priority",
            "display_name": "优先级",
            "meaning": "冲突时优先级（sub_570750 col5；高优先级覆盖低）",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        6: {
            "name": "icon_index",
            "db_column": "icon_index",
            "display_name": "图标索引",
            "meaning": "UI 图标索引（sub_570750 col6）",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        7: {
            "name": "buff_category",
            "db_column": "buff_category",
            "display_name": "Buff 类别",
            "meaning": "增益类别：MISSION_EXP_UP / MSMA_PARAM_UP / BUILDUP_UP 等（sub_570660→+40）",
            "memory_offset": 40,
            "type": "enum",
            "enum_converter": "sub_570660",
            "enum_values": [
                {"name": "MISSION_EXP_UP", "value": 0},
                {"name": "MISSION_GP_UP", "value": 1},
                {"name": "MISSION_RITEM_UP", "value": 2},
                {"name": "MISSION_RARE_POP", "value": 3},
                {"name": "RESPAWN_TIME_CUT", "value": 4},
                {"name": "MSMA_PARAM_UP", "value": 5},
                {"name": "SACRIFICE", "value": 6},
                {"name": "BUILDUP_UP", "value": 7},
                {"name": "LIMITEDTIME_AVATAR", "value": 8},
                {"name": "LIMITEDTIME_MS_COLOR", "value": 9},
                {"name": "LIMITEDTIME_MS_EMBLEM", "value": 10},
                {"name": "ALLOY_CHIP_GET", "value": 11},
            ],
            "enum_doc": ENUM_DOC,
            "status": "confirmed",
            "confidence": "★确证",
        },
        8: {
            "name": "effect_param_0",
            "db_column": "effect_param_0",
            "display_name": "效果参数0",
            "meaning": "类别相关效果强度/倍率（sub_570750 col8→+44 起 4×u32 数组首项）",
            "memory_offset": 44,
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
    },
    "AI_PARAM": {
        0: {
            "name": "ai_param_id",
            "display_name": "AI 参数 ID",
            "meaning": "主键；CAIParam 索引键（sub_56EA00 col0→+0）",
            "memory_offset": 0,
            "status": "confirmed",
            "confidence": "★确证",
        },
        1: {
            "name": "ai_archetype",
            "db_column": "ai_archetype",
            "display_name": "AI 原型",
            "meaning": "NPC 战斗原型：NORMAL/SHIELD/SNIPER/TANK 等（sub_56E570→+4；驱动行为树模板）",
            "memory_offset": 4,
            "status": "confirmed",
            "confidence": "★确证",
        },
        2: {
            "name": "mobility_class",
            "db_column": "mobility_class",
            "display_name": "机动类别",
            "meaning": "地形/机动：LAND/UNDERWATER/AIRCRAFT 等（sub_56E610→+8；寻路约束）",
            "memory_offset": 8,
            "status": "confirmed",
            "confidence": "★确证",
        },
        3: {
            "name": "custom_aim_cone",
            "db_column": "custom_aim_cone",
            "display_name": "自定义瞄准锥",
            "meaning": "启用 CSV 照准角覆盖（col3!=0→+44；否则用机体默认锥）",
            "memory_offset": 44,
            "type": "bool",
            "status": "confirmed",
            "confidence": "★确证",
        },
        4: {
            "name": "aim_pitch_min_deg",
            "display_name": "俯仰下限",
            "meaning": "照准俯仰下限（CSV 度数×π/180 取负存 +12；sub_551CE0 合成俯仰锥）",
            "memory_offset": 12,
            "type": "str_float",
            "parse": "deg_to_rad_neg",
            "status": "confirmed",
            "confidence": "★确证",
        },
        5: {
            "name": "aim_pitch_max_deg",
            "display_name": "俯仰上限",
            "meaning": "照准俯仰上限（度→弧度 +16）",
            "memory_offset": 16,
            "type": "str_float",
            "parse": "deg_to_rad",
            "status": "confirmed",
            "confidence": "★确证",
        },
        6: {
            "name": "aim_yaw_min_deg",
            "display_name": "偏航下限",
            "meaning": "照准偏航下限（度→弧度 +20）",
            "memory_offset": 20,
            "type": "str_float",
            "parse": "deg_to_rad",
            "status": "confirmed",
            "confidence": "★确证",
        },
        7: {
            "name": "aim_yaw_max_neg_deg",
            "display_name": "偏航上限(负)",
            "meaning": "照准偏航上限（度→弧度取负 +24）",
            "memory_offset": 24,
            "type": "str_float",
            "parse": "deg_to_rad_neg",
            "status": "confirmed",
            "confidence": "★确证",
        },
        8: {
            "name": "aim_yaw_max_deg",
            "display_name": "偏航上限",
            "meaning": "照准偏航上限（度→弧度 +28）",
            "memory_offset": 28,
            "type": "str_float",
            "parse": "deg_to_rad",
            "status": "confirmed",
            "confidence": "★确证",
        },
        9: {
            "name": "spread_timing_a",
            "display_name": "集弾系数A",
            "meaning": "集弾/散布计时系数 A（+32；与 AI_WEAPON_PARAM col9 同语义）",
            "memory_offset": 32,
            "status": "confirmed",
            "confidence": "★确证",
        },
        10: {
            "name": "score_weight_x100",
            "display_name": "评分权重",
            "meaning": "AI 目标评分权重×100（col10→+36；选敌优先级缩放）",
            "memory_offset": 36,
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        11: {
            "name": "warning_shot_range_deg",
            "display_name": "警告射击角",
            "meaning": "警告射击阈值角（度→弧度 +40；负值用 flt_D6D398 默认）",
            "memory_offset": 40,
            "type": "str_float",
            "status": "confirmed",
            "confidence": "★确证",
        },
        12: {
            "name": "use_default_spread",
            "display_name": "默认散布",
            "meaning": "使用内置散布默认值（col12→+520 bit0；置位则 +48/+52/+56 写常量）",
            "type": "bool",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        13: {
            "name": "move_wait_flag",
            "display_name": "移动等待",
            "meaning": "移动-射击等待标志（col13→+520 bit2；CGoal_MoveActionWait）",
            "type": "bool",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        14: {
            "name": "burst_fire_flag",
            "display_name": "连射标志",
            "meaning": "连射/点射行为标志（col14→+520 bit1）",
            "type": "bool",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        15: {
            "name": "near_range_weight",
            "display_name": "近距离权重",
            "meaning": "近距离段交战权重（col15→+76 float）",
            "memory_offset": 76,
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        16: {
            "name": "mid_range_weight",
            "display_name": "中距离权重",
            "meaning": "中距离段交战权重（col16→+80）",
            "memory_offset": 80,
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
        17: {
            "name": "sniper_mode_flag",
            "display_name": "狙击模式",
            "meaning": "狙击/精密射击模式（col17→+520 bit3）",
            "type": "bool",
            "status": "confirmed",
            "confidence": "○ASM确证",
        },
    },
    "WEAPON_BATTLE_DETAIL": {
        0: {
            "display_name": "属性名",
            "meaning": "战斗属性名（sub_595CC0 词表→11 张子表分派；POWER/RANGE 等）",
        },
        1: {
            "display_name": "武器键",
            "meaning": "武器 ID 字符串键（col1；与 weapon_settings 行关联）",
        },
        2: {
            "display_name": "属性值",
            "meaning": "属性数值（子表 vtable 读 col2；int/float；POWER 对回复系武器取负）",
        },
    },
    "BUILDUP_WEAPON": {
        0: {
            "name": "buildup_id",
            "db_column": "buildup_id",
            "display_name": "强化 ID",
            "meaning": "主键；CBuildupWeaponTable 行键（sub_570880 col0→+0）",
            "memory_offset": 0,
            "status": "confirmed",
            "confidence": "★确证",
        },
    },
}

# WEAPON_SETTING high-value columns (★ MD + IDA)
WS_OVERLAY = {
    0: ("weapon_setting_id", "武器设置 ID", "主键；CWeaponTable 行键（sub_597F50 @+0）", 0),
    1: ("parent_setting_id", "父行 ID", "继承源 weapon_setting_id（col1→sub_483020 查父行合并空字段）", None),
    2: ("model_id_lo", "模型 ID 低32", "模型资源键低 32 位（i64 @+8，col2+3 成对）", 8),
    3: ("model_id_hi", "模型 ID 高32", "模型资源键高 32 位（i64 @+16）", 16),
    4: ("variant_id_lo", "变体 ID 低32", "武器变体/子型号低 32（i64 @+24）", 24),
    7: ("bind_model_flag", "绑定模型", "非零时强制使用本行模型 ID（@+40）", 40),
    8: ("shop_item_id", "商品 ID", "商店/道具引用 ID（@+44）", 44),
    9: ("inherit_parent_bit", "继承父行位", "从父行继承空字段（+2228 bit6）", 2228),
    10: ("enabled", "启用", "武器槽启用开关（col10→+60 bool）", 60),
    11: ("sort_order", "排序", "UI/装备排序权重（@+48）", 48),
    12: ("cost_points", "消耗点数", "装备消耗/COST（@+52；负值取绝对值）", 52),
    13: ("equip_slot_type", "装备槽位", "ONEHAND/TWOHAND/SHIELD 等（sub_5968A0→+56）", 56),
    14: ("magazine_size", "弹匣容量", "弹匣发数（col14+1 存 @+64）", 64),
    15: ("melee_shield_subtype", "近战盾细分", "射击/格斗/盾子类（sub_596990→+68）", 68),
    16: ("weapon_shot_subtype", "射击子类", "同系射击细分（sub_596A80→+72）", 72),
    17: ("lock_on_flag", "锁定", "可否锁定目标（col17→+76 bool）", 76),
    18: ("close_range_mode", "近距模式", "CLOSE 字符串触发近距射击（sub_40CE20→+80）", 80),
    21: ("weapon_category", "武器功能类", "MACHINEGUN/BEAM/REPAIR 等 52 类（sub_596B70→+84；决定 POWER 符号）", 84),
    22: ("weapon_category_derived", "派生类别", "由 weapon_category 派生（sub_596100→+88）", 88),
    28: ("fire_mode_type", "发射模式", "GUN_RAPID/HOMING/WRESTLE 等（sub_596C60→+96）", 96),
    30: ("damage_attribute", "伤害属性", "SOLID/BEAM/BLAST（sub_5964A0→+108）", 108),
    36: ("weapon_power", "威力", "基础威力（col36 float→+196；回复系类别在消费端取负）", 196),
    38: ("range_meter", "射程", "有效射程米（col38→+312）", 312),
    128: ("status_effect", "附加状态", "RADAR_JAMMING/SLOW/DEBUFF 等（sub_596D50→+2124）", 2124),
    29: ("scatter_pattern", "散布模式", "NORMAL/SCATTERS/SP_BEAM 等（sub_596510→+92 cmp-chain）", 92),
    31: ("lockon_mode", "锁定模式", "NONE/LOCKON/SCOPE/FUNNEL 等（sub_5965F0→+100）", 100),
    74: ("effect_name_list", "特效名列表", "特效资源名列表窄串（col74 sub_402310→+2264）", 2264),
    77: ("hit_effect_list", "命中特效列表", "命中 FX 名列表（col77→+2292）", 2292),
    79: ("muzzle_effect_list", "枪口特效列表", "枪口 FX 名列表（col79→+2320）", 2320),
    81: ("trail_effect_list", "弹道特效列表", "弹道 FX 名列表（col81→+2348）", 2348),
}
for idx, (name, disp, meaning, off) in WS_OVERLAY.items():
    entry: dict = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "★确证" if idx in (13, 15, 21, 28, 30, 128) else "○ASM确证",
    }
    if off is not None:
        entry["memory_offset"] = off
    OVERLAYS.setdefault("WEAPON_SETTING", {})[idx] = entry

# WEAPON_SETTING Round 5 — #36 battle-detail multipliers + ammo/reload/lock/grenade block
WS_R5: dict[int, dict] = {
    40: {
        "name": "accuracy_multiplier",
        "display_name": "命中精度倍率",
        "meaning": "命中精度倍率（col40→+344；缺省 1.0；sub_597F50 末段补默认）",
        "memory_offset": 344,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    43: {
        "name": "recoil_multiplier",
        "display_name": "后坐力倍率",
        "meaning": "后坐力倍率（col43→+460；#36 RECOIL 查键区 +376；sub_597AF0 派生）",
        "memory_offset": 460,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    45: {
        "name": "reload_multiplier",
        "display_name": "装填倍率",
        "meaning": "装填时间倍率（col45→+548；#36 RELOAD 查键区 +464）",
        "memory_offset": 548,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    47: {
        "name": "cooldown_multiplier",
        "display_name": "冷却倍率",
        "meaning": "冷却时间倍率（col47→+636；#36 COOLTIME 查键区 +552）",
        "memory_offset": 636,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    49: {
        "name": "switch_time_multiplier",
        "display_name": "切换倍率",
        "meaning": "武器切换时间倍率（col49→+724；#36 SWITCHTIME 查键区 +640）",
        "memory_offset": 724,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    51: {
        "name": "lockon_multiplier",
        "display_name": "锁定倍率",
        "meaning": "锁定镜头倍率（col51→+812；#36 LOCKON_CAM 查键区 +728）",
        "memory_offset": 812,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    53: {
        "name": "stability_multiplier",
        "display_name": "稳定倍率",
        "meaning": "集弹/稳定倍率（col53→+900；#36 STABILITY 查键区 +816）",
        "memory_offset": 900,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    55: {
        "name": "rapid_delay_multiplier",
        "display_name": "连射延迟倍率",
        "meaning": "连射间隔倍率（col55→+1240；#36 RAPIDDELAY 查键区 +1156）",
        "memory_offset": 1240,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    59: {
        "name": "spread_multiplier",
        "display_name": "散布倍率",
        "meaning": "弹道散布倍率（col59→+1384；STABILITY 散布查键区 +1300）",
        "memory_offset": 1384,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    41: {
        "name": "optional_name_flag",
        "display_name": "可选名称标志",
        "meaning": "col41 非零时写入可选显示名窄串（→+348；sub_4029E0）",
        "memory_offset": 348,
        "type": "enum",
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    56: {
        "name": "optional_effect_flag",
        "display_name": "可选特效标志",
        "meaning": "col56 非零时写入可选特效名列表（→+1244；sub_4029E0）",
        "memory_offset": 1244,
        "type": "enum",
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    57: {
        "name": "optional_sound_flag",
        "display_name": "可选音效标志",
        "meaning": "col57 非零时写入可选音效名列表（→+1272；sub_4029E0）",
        "memory_offset": 1272,
        "type": "enum",
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    67: {
        "name": "ammo_pack_id",
        "display_name": "弹药包 ID",
        "meaning": "备用弹药/消耗道具 ID（col67→+1904；与 col64 弹药类型配套）",
        "memory_offset": 1904,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    68: {
        "name": "bullet_id",
        "display_name": "弹丸 ID",
        "meaning": "CBulletTable 主键（col68→+1908；sub_59A070→sub_4D2620 查弹丸行）",
        "memory_offset": 1908,
        "status": "confirmed",
        "confidence": "★确证",
    },
    69: {
        "name": "projectile_count",
        "display_name": "弹丸数",
        "meaning": "单发弹丸/弹头数量（col69→+1912）",
        "memory_offset": 1912,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    70: {
        "name": "burst_rounds",
        "display_name": "连射轮数",
        "meaning": "连射/点射轮数（col70→+1916）",
        "memory_offset": 1916,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    71: {
        "name": "shot_interval_ms",
        "display_name": "射击间隔",
        "meaning": "连射间隔毫秒（col71→+1920）",
        "memory_offset": 1920,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    72: {
        "name": "muzzle_count",
        "display_name": "枪口数",
        "meaning": "同时发射枪口/炮口数（col72→+1924）",
        "memory_offset": 1924,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    73: {
        "name": "bullet_inherit_setting_id",
        "display_name": "弹丸继承源",
        "meaning": "非零时按此 weapon_setting_id 查父行弹丸参数（col73→+1928；sub_596F30）",
        "memory_offset": 1928,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    103: {
        "name": "shield_absorb_rate",
        "display_name": "盾吸收率",
        "meaning": "SHIELD 复合参数第3项 float（col103→+2020；同 #36 SHIELD→+2020）",
        "memory_offset": 2020,
        "status": "confirmed",
        "confidence": "★确证",
    },
    106: {
        "name": "reload_ammo_per_clip",
        "display_name": "装填发数",
        "meaning": "单次装填填入发数（col106→+2056；sub_596F30 与父行 reload 比对）",
        "memory_offset": 2056,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    107: {
        "name": "reload_time",
        "display_name": "装填时间",
        "meaning": "装填时间秒（col107→+2060；sub_57ECF0 混淆存储；sub_47A230 解码）",
        "memory_offset": 2060,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    108: {
        "name": "lockon_acquire_range",
        "display_name": "锁定捕获距离",
        "meaning": "锁定捕获距离米（col108→+2068；max_lock_count 前置 float 组）",
        "memory_offset": 2068,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    109: {
        "name": "lockon_track_range",
        "display_name": "锁定跟踪距离",
        "meaning": "锁定维持/跟踪距离米（col109→+2072）",
        "memory_offset": 2072,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    110: {
        "name": "homing_grenade_flag",
        "display_name": "诱导榴弹标志",
        "meaning": "标志位 @+8B4h bit4（col110 非零置位；配合 col120-122 诱导弹道）",
        "memory_offset": 2228,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    111: {
        "name": "lockon_cone_deg",
        "display_name": "锁定锥角",
        "meaning": "锁定捕获锥角/FOV（col111→+2076 float）",
        "memory_offset": 2076,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    114: {
        "name": "full_lockon_flag",
        "display_name": "全向锁定标志",
        "meaning": "标志位 @+8B4h bit7（col114 非零置位 @+2228）",
        "memory_offset": 2228,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    115: {
        "name": "lockon_filter_flags",
        "display_name": "锁定过滤",
        "meaning": "锁定目标过滤位（col115→+2084）",
        "memory_offset": 2084,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    116: {
        "name": "lockon_priority",
        "display_name": "锁定优先级",
        "meaning": "多目标锁定时优先级（col116→+2088）",
        "memory_offset": 2088,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    117: {
        "name": "lockon_break_threshold",
        "display_name": "锁定丢失阈值",
        "meaning": "锁定丢失/重捕获阈值（col117→+2092）",
        "memory_offset": 2092,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    118: {
        "name": "projectile_launch_angle",
        "display_name": "发射仰角",
        "meaning": "曲射/榴弹发射仰角（col118→+2096）",
        "memory_offset": 2096,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    119: {
        "name": "projectile_launch_speed",
        "display_name": "发射初速",
        "meaning": "曲射弹道初速（col119→+2100）",
        "memory_offset": 2100,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    120: {
        "name": "grenade_arc_peak",
        "display_name": "榴弹弧顶",
        "meaning": "榴弹弧顶高度/弧度（col120→+2104；sub_596F30 诱导榴弹三元组）",
        "memory_offset": 2104,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    121: {
        "name": "grenade_homing_strength",
        "display_name": "榴弹诱导强度",
        "meaning": "榴弹诱导强度（col121→+2108；sub_596F30 与 col120/122 联动）",
        "memory_offset": 2108,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    122: {
        "name": "grenade_gravity_scale",
        "display_name": "榴弹重力缩放",
        "meaning": "榴弹重力/下落缩放（col122→+2112；sub_596F30 诱导榴弹三元组）",
        "memory_offset": 2112,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    126: {
        "name": "status_duration_sec",
        "display_name": "状态持续时间",
        "meaning": "附加状态持续秒（col126→+2116；col128 status_effect 前置）",
        "memory_offset": 2116,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    127: {
        "name": "status_radius_m",
        "display_name": "状态作用半径",
        "meaning": "附加状态作用半径米（col127→+2120）",
        "memory_offset": 2120,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    129: {
        "name": "status_effect_power",
        "display_name": "状态效果强度",
        "meaning": "附加状态效果强度倍率（col129→+2128；col128 枚举配套）",
        "memory_offset": 2128,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    131: {
        "name": "ui_stat_display_id",
        "display_name": "UI 数值展示",
        "meaning": "武器面板数值展示样式 ID（col131→+2144）",
        "memory_offset": 2144,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    133: {
        "name": "display_overlay_mode",
        "display_name": "展示叠加模式",
        "meaning": "UI 展示叠加模式 1..11（col133→+2229/+2230 位编码；sub_597F50 switch）",
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    134: {
        "name": "variant_id_hi_lo",
        "display_name": "变体 ID 高段低32",
        "meaning": "变体 i64 高段低 32（col134→+32；与 col135 成对）",
        "memory_offset": 32,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    135: {
        "name": "variant_id_hi_hi",
        "display_name": "变体 ID 高段高32",
        "meaning": "变体 i64 高段高 32（col135→+36）",
        "memory_offset": 36,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    139: {
        "name": "projectile_setting_id",
        "display_name": "弹道设置 ID",
        "meaning": "关联弹道/发射物设置 ID（col139→+2208）",
        "memory_offset": 2208,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    140: {
        "name": "spawn_offset_x",
        "display_name": "生成点 X 偏移",
        "meaning": "弹丸/特效生成点 X 偏移（col140→+2212）",
        "memory_offset": 2212,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    141: {
        "name": "spawn_offset_y",
        "display_name": "生成点 Y 偏移",
        "meaning": "弹丸/特效生成点 Y 偏移（col141→+2216）",
        "memory_offset": 2216,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    145: {
        "name": "spawn_offset_z",
        "display_name": "生成点 Z 偏移",
        "meaning": "弹丸/特效生成点 Z 偏移（col145→+2220）",
        "memory_offset": 2220,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    147: {
        "name": "damage_field_burst_cap",
        "display_name": "伤害场上限修正",
        "meaning": "fire_mode=DAMAGE_FIELD_GUN(24) 时连射上限修正（col147→+2136）",
        "memory_offset": 2136,
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
    18: {
        "name": "close_range_mode",
        "db_column": "close_range_mode",
        "enum_values": [{"name": "CLOSE", "value": 1}],
        "meaning": "近距模式：CSV 写 CLOSE 触发近距射击（sub_40CE20→+80 bool）",
        "display_name": "近距模式",
        "status": "confirmed",
        "confidence": "○ASM确证",
    },
}
for idx, entry in WS_R5.items():
    e = dict(entry)
    e.setdefault("db_column", e.get("name", f"col_{idx}"))
    OVERLAYS.setdefault("WEAPON_SETTING", {})[idx] = e

# CHARA_PARAM M01 §4 + Round5 IDA (sub_582390 / sub_64A230 / sub_6218F0)
CP = {
    0: ("msma_id", "練度 ID", "行键=机体定义 ID（sub_582390→+0）", 0, "confirmed", "★确证"),
    1: ("resource_id_lo", "主模型资源键（独立i64）", "582390 CSV1以i64读到+8；4C2D20取该完整键调用4A5470/473390加载主模型。旧物理列名lo不是低32，不能与CSV2拼接。", 8, "confirmed", "★确证"),
    2: ("resource_id_hi", "条件替代模型资源键（独立i64）", "582390 CSV2以i64读到+16；4C2D20在任务/机体条件成立且此键非零时替代主键。旧物理列名hi不是高32；完整切换条件仍待复核。", 16, "partial", "○读入及替代消费者确证"),
    3: ("generation", "世代", "机体世代/系列编号（u16 @+24）", 24, "confirmed", "★确证"),
    4: ("rank", "阶级", "RANK1..RANK5（sub_580610→+408）", 408, "confirmed", "★确证"),
    5: ("name", "名称", "机体名称宽串（sub_456D90 wstring）", 32, "confirmed", "★确证"),
    6: ("description", "说明", "机体说明宽串（sub_456D90）", None, "confirmed", "★确证"),
    7: ("combat_role", "战斗角色", "战斗角色 ASSAULT_A/SNIPE/CANNON/SUPPORT 等（sub_5804F0→+120）", 120, "confirmed", "★确证"),
    8: ("faction", "阵营", "阵营/国家（sub_580560→+128）", 128, "confirmed", "★确证"),
    9: ("terrain_proper_space", "宇宙适性", "宇宙地形适性（col9→+136；sub_64A230 MS_PROPER_SPACE）", 136, "confirmed", "★确证"),
    10: ("terrain_proper_water", "水中适性", "水中地形适性（col10→+140；sub_64A230 MS_PROPER_WATER）", 140, "confirmed", "★确证"),
    11: ("terrain_proper_ground", "地面适性", "地面地形适性（col11→+144；sub_64A230 MS_PROPER_GROUND）", 144, "confirmed", "★确证"),
    35: ("entity_category", "实体类别", "实体类别 NORMAL/BATTLESHIP/TANK/MA 等（sub_5806B0→+368）", 368, "confirmed", "★确证"),
    36: ("stat_scale_a", "数值缩放A", "机体数值缩放系数 A（col36 float→+156；Runtime 装甲/HP 换算 sub_6218F0）", 156, "confirmed", "○ASM确证"),
    37: ("stat_scale_b", "数值缩放B", "机体数值缩放系数 B（col37 float→+160）", 160, "confirmed", "○ASM确证"),
    38: ("weapon_group_id", "武器组ID", "武器组 ID（col38→+372；→ MSMA_WEAPONSET）", 372, "confirmed", "★确证"),
    44: ("equip_comb_id", "装备组合ID", "装备组合 ID（col44→+396；→ MSMA_WEAPON_EQUIPCOMB）", 396, "confirmed", "★确证"),
    42: ("linked_table_id", "关联表ID", "关联配置表行 ID（col42→+392；sub_7D97E0/sub_7D8520 机库升级 UI 遍历；sub_78B690）", 392, "confirmed", "★确证"),
    46: ("shop_recycle_gp", "商店回收GP", "商店回收 GP 基值（col46→+400；sub_887550；MSMA_RENTAL=rental_cost_gp）", 400, "confirmed", "★确证"),
    47: ("hangar_timer_sec", "机库计时秒", "机库/租借计时秒（col47→+404；sub_7DA460/sub_582EC0）", 404, "confirmed", "★确证"),
    48: ("deployable_type", "可部署类型", "可部署类型 RESPAWNPOST/REPAIRPOST/TENDER 等（sub_580BA0→+412）", 412, "confirmed", "★确证"),
    49: ("series_class", "出生后控制器选择", "582390 CSV49经580C40写CHARA_PARAM+416：NORMAL=1、MA=2、AAG=4、BATTERY=10、BATTLESHIP=11、MARCH=15；空值及未匹配文本默认NORMAL=1，精确比较不去空格。4C2D20→4BFF00自身type=3初始化及6729F0普通finishRespawn分支把此值交给容器虚表+48→4C9A80选择自身控制器；1选择4EAFB0普通SelfTargetView，2选择4DDE90变体。该switch未处理15，其他调用场景/逐机体原服值未穷举。旧“系列分类”名称不足以描述已确认运行用途；保留物理DB列名series_class。不能将空值当作零控制器，也不据此证明现场落地。", 416, "confirmed", "★确证"),
    50: ("oc_exp_cp_id", "OC经验CP ID", "OC/经验 CP 选择 ID（col50→+420；sub_847D10）", 420, "confirmed", "★确证"),
    51: ("hangar_list_ui_param", "机库列表UI参数", "机库列表 UI 分支参数（col51→+424；sub_7E25A0/sub_97F077）", 424, "confirmed", "★确证"),
    52: ("payload_capacity_base", "搭载量基值（積載量）", "装备搭载量基值（= 日服「積載量」/ 覆写关键字 `PAYLOAD`）col52→+248；三源一致（sub_61C9A0 idx4 + sub_6246D0 `PAYLOAD` + 表78 `PAYLOAD`）2026-09-28 定案", 248, "confirmed", "★确证"),
    54: ("hangar_ui_slot_a", "机库UI槽A", "机库 UI 控件槽 A（col54→+428；sub_897480/sub_7E94C0）", 428, "confirmed", "★确证"),
    55: ("hangar_ui_slot_b", "机库UI槽B", "机库 UI 控件槽 B（col55→+432；sub_897480/sub_7E94C0）", 432, "confirmed", "★确证"),
    83: ("emergency_return_base", "未定名（原「紧急返回基值」，作废）", "⚠未定名 col83→+252（旧标「紧急返回性能」2026-09-28 作废；表78 关键字 `MODULE_SLOT` 落此处，疑「模块槽位数」）；值已清空", 252, "gap", ""),
    85: ("boost_gauge_base", "未定名（原「喷射容量基值」位，作废）", "⚠未定名 col85→+356（旧标「装备搭载量」2026-09-28 作废 —— 真身 = col52/+248）；值已清空", 356, "gap", ""),
    86: ("boost_charge_base", "未定名（原「喷射蓄力基值」，作废）", "⚠未定名 col86→+256（旧标「喷射蓄力」2026-09-28 作废 —— 真身 = 行 +176 后处理）；值已清空", 256, "gap", ""),
    87: ("flavor_text", "Flavor 文本", "附加说明宽串（col87 sub_456D90）", None, "confirmed", "★确证"),
    88: ("list_category_id", "列表分类ID", "机库/商店列表分类 ID（col88→+32；sub_887550 回收价系数）", 32, "confirmed", "★确证"),
    89: ("max_speed_base", "未定名（原「最高速度基值」，作废）", "⚠未定名 col89→+244（旧标「最高速度」2026-09-28 作废 —— 真身 = 行 +180 float 后处理）；值已清空", 244, "gap", ""),
    90: ("armor_base", "装甲基值", "装甲基础值 u16（col90→+148；Hangar 属性面板 sub_6102C0）", 148, "confirmed", "★确证"),
    91: ("boost_speed_base", "推进速度基值", "推进速度基础值 u16（col91→+152）", 152, "confirmed", "○ASM确证"),
}
CP_FLAGS = {
    13: ("cap_flag_transform_alt", "变换备用武装", "能力位 +840 bit0：变身形态备用武装（sub_49D280）", "confirmed"),
    15: ("cap_flag_melee_chain", "近战连锁", "能力位 +840 bit1：近战连锁攻击门控（sub_4A7B10）", "confirmed"),
    16: ("cap_flag_reserved_b840_2", "能力位 b840.2（预留）", "能力位 +840 bit2（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    17: ("cap_flag_reserved_b840_3", "能力位 b840.3（预留）", "能力位 +840 bit3（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    18: ("cap_flag_mission_transform", "任务变形态", "能力位 +840 bit4：任务/关卡变形态资格（sub_477C10；sub_67FEB0）", "confirmed"),
    19: ("cap_flag_reserved_b840_5", "能力位 b840.5（预留）", "能力位 +840 bit5（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    20: ("cap_flag_reserved_b840_6", "物理积分旁路位 +840 bit6", "582390 CSV20非零规范为CHARA_PARAM+840 bit6；47D230末尾读取此位，4AE900在返回true时跳过53D580物理积分。47D230还包含装备/特殊状态分支，因此此位为0不能证明实际物理更新已开启。旧“无runtime xref/预留”说明错误；其他消费者与原服逐机体取值未穷举。", "confirmed"),
    21: ("cap_flag_reserved_b840_7", "能力位 b840.7（预留）", "能力位 +840 bit7（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    22: ("cap_flag_reserved_b841_0", "能力位 b841.0（预留）", "能力位 +841 bit0（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    24: ("cap_flag_skip_ex_anim", "跳过EX演出", "能力位 +841 bit2：清 0 时跳过 EX 武器演出（sub_7E7600）", "confirmed"),
    25: ("cap_flag_shield_equip", "盾牌装备", "能力位 +841 bit3：盾牌装备能力（sub_474480；sub_48FF00）", "confirmed"),
    26: ("cap_flag_reserved_b841_4", "能力位 b841.4（预留）", "能力位 +841 bit4（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    27: ("cap_flag_reserved_b841_5", "能力位 b841.5（预留）", "能力位 +841 bit5（CSV→sub_582390；无 runtime test xref）", "confirmed"),
    28: ("cap_flag_tender_mode", "工作舰模式", "能力位 +841 bit6：工作舰/母舰 deploy（sub_478DA0；sub_507810）", "confirmed"),
    29: ("cap_flag_reserved_b841_7", "位置碰撞更新旁路位 +841 bit7", "582390 CSV29非零规范为CHARA_PARAM+841 bit7；478DD0读取该位，4AE900在返回true时跳过普通位置/碰撞更新分支（4ADD60或载体引用分支），角色+12 bit0x40000的4A94E0路径在此前独立处理。此位为0不能证明地面碰撞成功。旧“无runtime xref/预留”说明错误；原服逐机体取值未知。", "confirmed"),
    30: ("cap_flag_disable_special", "禁止特殊行动", "能力位 +842 bit0：禁止 deployable 特殊行动（sub_4E7FF0；sub_4EF710）", "confirmed"),
    31: ("cap_flag_dual_slot_ui", "双槽切换UI", "能力位 +841 bit1：机体选择 UI 双槽切换（sub_7E7600；sub_7E4A50）", "confirmed"),
    32: ("cap_flag_dual_mode", "双模式标志", "能力位 +842 bit1：双模式/双形态标志（sub_6218F0→runtime+107）", "confirmed"),
    34: ("cap_flag_no_awakening", "禁止觉醒爆发", "能力位 +842 bit3：禁止觉醒/爆发（sub_4EC960）", "confirmed"),
}
CP_STRINGS = {
    56: ("battle_detail_key_respawn", "战力子表槽·RESPAWN_TIME", "战力子表键 col56→+436；sub_581690 用此串查 MSMA_BATTLE_DETAIL 子表 MSMA_DETAIL_RESPAWN_DATA（词表 RESPAWN_TIME），须与 msma_battle_detail.csv col1 相等"),
    58: ("battle_detail_key_warp", "战力子表槽·WARP_TIME", "战力子表键 col58→+464；查 MSMA_DETAIL_WARPTIME_DATA（WARP_TIME）⇒ 行 +236（紧急返回性能）"),
    60: ("battle_detail_key_cost", "战力子表槽·COST", "战力子表键 col60→+492；查 MSMA_DETAIL_COST_DATA（COST）⇒ 行 +240"),
    62: ("battle_detail_key_max_hp", "战力子表槽·MAX_HP", "战力子表键 col62→+520；查 MSMA_DETAIL_MAX_HP_DATA（MAX_HP）⇒ 行 +164（面板装甲）"),
    64: ("battle_detail_key_energy", "战力子表槽·ENERGY", "战力子表键 col64→+548；查 MSMA_DETAIL_ENERGY_DATA（ENERGY）⇒ 行 +184/+188；表 78 不覆写"),
    67: ("battle_detail_key_move", "战力子表槽·MOVE", "战力子表键 col67→+576；查 MSMA_DETAIL_MOVE_DATA（MOVE）⇒ 行 +180（面板最高速度）；表 78 不覆写"),
    69: ("battle_detail_key_boost_gaugemax", "战力子表槽·BOOST_GAUGEMAX", "战力子表键 col69→+604；查 MSMA_DETAIL_BOOST_GAUGEMAX_DATA（BOOST_GAUGEMAX）⇒ 行 +168（面板喷射容量）"),
    71: ("battle_detail_key_boost_gaugeheal", "战力子表槽·BOOST_GAUGEHEAL", "战力子表键 col71→+632；查 MSMA_DETAIL_BOOST_GAUGEHEAL_DATA（BOOST_GAUGEHEAL）⇒ 行 +176（面板喷射蓄力）"),
    73: ("battle_detail_key_boost_speed", "战力子表槽·BOOST_SPEED", "战力子表键 col73→+660；查 MSMA_DETAIL_BOOST_MOVE_DATA（BOOST_SPEED）⇒ 行 +260..+312"),
    79: ("battle_detail_key_jump", "战力子表槽·JUMP", "战力子表键 col79→+688；查 MSMA_DETAIL_JUMP_DATA（JUMP）⇒ 行 +316..+364；表 78 不覆写"),
}
for idx, row in CP.items():
    name, disp, meaning, off, status, conf = row
    e = {"name": name, "db_column": name, "display_name": disp, "meaning": meaning, "status": status, "confidence": conf}
    if off is not None:
        e["memory_offset"] = off
    if idx in (7, 35, 48, 49):
        e["type"] = "enum"
    if idx in (36, 37):
        e["type"] = "float"
    OVERLAYS.setdefault("CHARA_PARAM", {})[idx] = e
for idx, (name, disp, meaning, status) in CP_FLAGS.items():
    OVERLAYS.setdefault("CHARA_PARAM", {})[idx] = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": status,
        "confidence": "★确证" if status == "confirmed" else "○ASM确证",
        "type": "bool",
    }
for idx, (name, disp, meaning) in CP_STRINGS.items():
    OVERLAYS.setdefault("CHARA_PARAM", {})[idx] = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "★确证",
        "type": "str",
    }

# CHARA_MODEL M01 §3 + Round5 (sub_571380 / sub_571290)
CM = {
    0: ("model_pack_id", "模型打包ID", "行键 u64 模型打包 ID（sub_571380 col0→+0；sub_473390 解码 chara/ 路径）", 0, "confirmed", "★确证"),
    1: ("hangar_scale", "机库缩放", "机库显示缩放（col1 float→+8）", 8, "confirmed", "○ASM确证"),
    2: ("camera_offset_x", "相机偏移X", "机库相机偏移 X（col2→+0C）", 12, "confirmed", "○ASM确证"),
    3: ("camera_offset_y", "相机偏移Y", "机库相机偏移 Y（col3→+10；亦复制到 +18）", 16, "confirmed", "○ASM确证"),
    4: ("camera_offset_z", "相机偏移Z", "机库相机偏移 Z（col4→+14）", 20, "confirmed", "○ASM确证"),
    5: ("camera_distance", "相机距离", "机库相机距离（col5→+1C）", 28, "confirmed", "○ASM确证"),
    7: ("camera_yaw", "相机偏航", "机库相机偏航角（col7→+24）", 36, "confirmed", "○ASM确证"),
    8: ("camera_pitch", "相机俯仰", "机库相机俯仰角（col8→+28）", 40, "confirmed", "○ASM确证"),
    9: ("camera_roll", "相机滚转", "机库相机滚转角（col9→+2C）", 44, "confirmed", "○ASM确证"),
    11: ("camera_fov", "物理积分质量 col11", "物理积分质量输入（571380 CSV11→CHARA_MODEL+48；4A5470/498950送入53D340，写CMassPoint+56并构造质量×重力；53D580在质量为0时直接返回，跳过速度和位移积分）。旧相机FOV名称无此消费链依据；保留旧DB列camera_fov仅为字段寻址兼容。原始逐模型质量值及单位未知，不能按FOV、wiki载重量或武器重量填值；当前579条发布记录均空/0。隔离原始指令验证只证明零质量门，不等于现场落地或完整物理恢复。", 48, "confirmed", "★消费链确证"),
    15: ("camera_target_y", "相机目标Y", "机库相机目标高度（col15→+38）", 56, "confirmed", "○ASM确证"),
    32: ("mesh_path_a", "网格路径A", "主网格路径窄串（col32→+7C；sub_402310）", 0x7C, "confirmed", "★确证"),
    33: ("mesh_path_b", "网格路径B", "副网格路径窄串（col33→+98）", 0x98, "confirmed", "★确证"),
    34: ("mesh_path_c", "网格路径C", "第三网格路径窄串（col34→+B4）", 0xB4, "confirmed", "★确证"),
    35: ("texture_variant", "贴图变体", "贴图变体/配色索引 u8（col35→+D0）", 0xD0, "confirmed", "○ASM确证"),
    36: ("texture_path", "贴图路径", "贴图资源路径窄串（col36→+D4）", 0xD4, "confirmed", "★确证"),
    37: ("render_param_a", "类别1键候选37", "sub_A856E0 将此列解析后的整数作为 fx.csv category=1 查询键；字段业务语义待确认（sub_571380：CSV37→+F0，sub_BBB370）", 0xF0, "partial", "★IDA读取链确证；语义待定"),
    41: ("render_param_b", "渲染参数B", "渲染参数 float（col41→+100）", 0x100, "confirmed", "○ASM确证"),
    42: ("render_param_c", "类别1键候选42", "sub_A856E0 将此列解析后的整数作为 fx.csv category=1 查询键；字段业务语义待确认（sub_571380：CSV42→+104，sub_BBB370）", 0x104, "partial", "★IDA读取链确证；语义待定"),
    50: ("effect_path_a", "特效路径A", "特效资源路径 A（col50→+11C）", 0x11C, "confirmed", "★确证"),
    51: ("effect_path_b", "特效路径B", "特效资源路径 B（col51→+138）", 0x138, "confirmed", "★确证"),
    52: ("effect_path_c", "特效路径C", "特效资源路径 C（col52→+154）", 0x154, "confirmed", "★确证"),
    54: ("lod_distance", "LOD距离", "LOD 切换距离（col54→+170）", 0x170, "confirmed", "○ASM确证"),
    55: ("equip_slot_type", "装备槽类型", "默认可装备槽 ONEHAND/SHOLDER/TWOHAND 等（sub_571290→+178）", 0x178, "confirmed", "★确证"),
    56: ("light_dir_x", "光照方向X", "光照方向 X（col56→+184 三元组）", 0x184, "confirmed", "○ASM确证"),
    57: ("light_dir_y", "光照方向Y", "光照方向 Y（col57→+188）", 0x188, "confirmed", "○ASM确证"),
    59: ("light_color_x", "光照颜色X", "光照颜色/强度 X（col59→+188 第二组）", 0x188, "confirmed", "○ASM确证"),
    61: ("shadow_scale", "阴影缩放", "阴影缩放 float（col61→+194）", 0x194, "confirmed", "○ASM确证"),
    64: ("level_min", "等级下限", "可用等级下限 u16（col64→+1A4；与 col65 归一）", 0x1A4, "confirmed", "○ASM确证"),
    65: ("level_max", "等级上限", "可用等级上限 u16（col65→+1A6；<min 则 =min+1）", 0x1A6, "confirmed", "○ASM确证"),
    68: ("display_mode", "显示模式", "显示模式（col68：1/2 拆为 +1AA/+1AB 两 bool）", 0x1AA, "confirmed", "○ASM确证"),
    71: ("model_id_lo", "模型 ID 低32", "★资源键低 32（col71→+1B4）", 0x1B4, "confirmed", "★确证"),
    72: ("model_id_hi", "模型 ID 高32", "★资源键高 32（col72→+1B8）", 0x1B8, "confirmed", "★确证"),
}
CM_MESH = list(range(16, 26)) + [29, 31]
CM_FLAGS = {
    6: ("flag_mirror_mesh", "镜像网格", "网格镜像开关（col6→+20）", "partial"),
    12: ("flag_hide_shield", "隐藏盾牌", "隐藏盾牌网格（col12→+34）", "partial"),
    13: ("flag_hide_weapon", "隐藏武器", "隐藏武器网格（col13→+35）", "partial"),
    14: ("flag_hide_backpack", "角色可视性条件 col14", "col14→+54（0x36）bool（571380）；477300 在角色+1168 bit1为0，或角色+216非空且本标记为0时返回false；4C7B00对自身角色的该分支不清除隐藏原因2。字段原名、完整用途与各机体原始取值未知；不能称为隐藏背包。2026-10-07只对已核实模型101010101/184302101开启此布尔条件，恢复自身相机隐藏原因2的正常清除路径；这是按目标客户端行为实现的功能兼容策略，不是找回原服取值，不强制清除其他隐藏原因。", "partial"),
    47: ("flag_effect_a", "特效开关A", "特效路径 A 启用（col47→+110）", "partial"),
    48: ("flag_effect_b", "特效开关B", "特效路径 B 启用（col48→+114）", "partial"),
    49: ("flag_effect_c", "特效开关C", "特效路径 C 启用（col49→+118）", "partial"),
    62: ("flag_shadow", "阴影开关", "阴影渲染开关（col62 bool @+194）", "partial"),
    66: ("flag_variant_a", "变体开关A", "模型变体开关 A（col66→+1A8）", "partial"),
    67: ("flag_variant_b", "变体开关B", "模型变体开关 B（col67→+1A9）", "partial"),
    70: ("flag_force_load", "强制加载", "强制加载模型资源（col70→+1B0）", "partial"),
}
CM_DISCARD_STR = {26: "prefetch_str_a", 27: "prefetch_str_b", 28: "prefetch_str_c", 30: "prefetch_str_d"}
for idx, row in CM.items():
    name, disp, meaning, off, status, conf = row
    e = {"name": name, "db_column": name, "display_name": disp, "meaning": meaning, "status": status, "confidence": conf}
    if off is not None:
        e["memory_offset"] = off
    if idx == 55:
        e["type"] = "enum"
        e["enum_converter"] = "sub_571290"
    if idx in (37, 38, 39, 40, 42):
        e["type"] = "u32"
    elif idx == 41:
        e["type"] = "float"  # sub_571380 CSV41 uses sub_BBB470; 37/42 are integer keys.
    OVERLAYS.setdefault("CHARA_MODEL", {})[idx] = e
for n, idx in enumerate(CM_MESH):
    OVERLAYS.setdefault("CHARA_MODEL", {})[idx] = {
        "name": f"mesh_custom_{idx}",
        "db_column": f"mesh_custom_{idx}",
        "display_name": f"网格定制{idx}",
        "meaning": f"网格定制/隐藏参数（col{idx}→mesh 块 u32；对应 msma_mesh_customize）",
        "status": "confirmed",
        "confidence": "○ASM确证",
        "type": "u32",
    }
for idx, (name, disp, meaning, status) in CM_FLAGS.items():
    OVERLAYS.setdefault("CHARA_MODEL", {})[idx] = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": status,
        "confidence": "○ASM确证",
        "type": "bool",
    }
for idx, name in CM_DISCARD_STR.items():
    OVERLAYS.setdefault("CHARA_MODEL", {})[idx] = {
        "name": name,
        "db_column": name,
        "display_name": "预读串(丢弃)",
        "meaning": f"CSV 窄串 col{idx}：读取后立即丢弃，不落内存（sub_571380 预读段）",
        "status": "partial",
        "confidence": "○ASM确证",
        "type": "str",
    }
for idx in (38, 39, 40, 43, 45, 63, 69, 73, 74, 75, 76):
    OVERLAYS.setdefault("CHARA_MODEL", {})[idx] = {
        "name": f"render_u32_{idx}",
        "db_column": f"render_u32_{idx}",
        "display_name": f"渲染参数 u32 {idx}",
        "meaning": f"渲染/材质 u32 参数（col{idx}；sub_571380 读入）",
        "status": "partial",
        "confidence": "○ASM确证",
        "type": "u32",
    }

# WRESTLE_PARAM
WP = {
    0: ("wrestle_param_id", "格斗参数 ID", "主键（sub_56F5F0 col0）", 0),
    4: ("base_damage", "基础伤害", "格斗基础伤害系数（col4 float）", None),
    7: ("hit_type", "命中类型", "NONE/HOMING/HACK_CHECK_EX（sub_56F4B0）", None),
    17: ("attack_hand", "攻击手", "L_HAND/R_HAND/ACTIVE_WEAPON（sub_56F3A0）", None),
}
for idx, (name, disp, meaning, off) in WP.items():
    e = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "★确证" if idx in (7, 17) else "○ASM确证",
    }
    if off is not None:
        e["memory_offset"] = off
    OVERLAYS.setdefault("WRESTLE_PARAM", {})[idx] = e

# BULLET from sub_5709F0 decompile
BL = {
    0: ("bullet_id", "子弹 ID", "主键 CBulletTable（sub_5709F0→+0）", 0),
    3: ("is_beam", "光束弹", "YES/NO 字符串→bool（sub_40CE20→+4）", 4),
    4: ("bullet_type_id", "弹种 ID", "关联弹种/特效（col4→+8）", 8),
    5: ("speed", "弹速", "初速（col5 float→+12）", 12),
    6: ("lifetime", "存活时间", "弹道存活秒（col6→+16）", 16),
    8: ("gravity_scale", "重力", "重力缩放（col8→+20）", 20),
    9: ("penetrate_flag", "穿透", "YES/NO→+24", 24),
    10: ("homing_flag", "制导", "YES/NO→+25", 25),
    11: ("spread_angle", "散布角", "发射散布（col11→+28）", 28),
    19: ("trail_flag", "拖尾", "YES/NO→+60", 60),
    24: ("damage_type", "伤害类型", "伤害属性枚举（sub_570950→+88）", 88),
    38: ("destroy_on_hit", "命中销毁", "YES/NO→+140", 140),
}
for idx, (name, disp, meaning, off) in BL.items():
    e = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "○ASM确证",
    }
    if off is not None:
        e["memory_offset"] = off
    OVERLAYS.setdefault("BULLET", {})[idx] = e

# DAMAGE_FIELD_PARAM sub_575D00
DF = {
    0: ("damage_field_id", "伤害场 ID", "主键（sub_575D00→+0）", 0),
    2: ("radius_inner", "内径", "伤害场内半径（col2→+4；下限 flt_D6A8EC）", 4),
    3: ("radius_outer", "外径", "伤害场外半径（col3→+8；上限 flt_D78388）", 8),
    4: ("emit_source", "发射源", "附着点 NONE/L_HAND/R_HAND/ACTIVE_WEAPON（sub_575A60→+12）", 12),
    5: ("tick_damage_a", "Tick伤害A", "周期伤害系数 A（col5×flt_D91AF8→+16）", 16),
    6: ("tick_damage_b", "Tick伤害B", "周期伤害系数 B（→+20）", 20),
    7: ("tick_damage_c", "Tick伤害C", "周期伤害系数 C（→+24）", 24),
    8: ("duration_sec", "持续时间", "伤害场存活秒（col8→+28）", 28),
    9: ("tick_interval", "Tick间隔", "伤害判定间隔秒（col9→+32）", 32),
    10: ("field_height", "场高度", "垂直作用高度（col10→+36）", 36),
    11: ("field_offset_y", "Y偏移", "相对机体 Y 偏移（col11→+40）", 40),
    12: ("field_offset_z", "Z偏移", "相对机体 Z 偏移（col12→+44）", 44),
    13: ("fx_resource", "特效资源", "FX 资源路径窄串（col13 sub_402310→+48）", 48),
    15: ("damage_falloff", "伤害衰减", "边缘衰减系数（col15→+104）", 104),
    17: ("vertical_scale", "垂直缩放", "垂直范围缩放（col17→+136）", 136),
    19: ("spawn_delay", "生成延迟", "激活延迟秒（col19→+168）", 168),
    20: ("knockback_x", "击退X", "击退向量 X（col20→+256）", 256),
    21: ("knockback_y", "击退Y", "击退向量 Y（col21→+260）", 260),
    22: ("knockback_z", "击退Z", "击退向量 Z（col22→+264）", 264),
}
for idx, (name, disp, meaning, off) in DF.items():
    e = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "★确证" if idx == 4 else "○ASM确证",
    }
    if off is not None:
        e["memory_offset"] = off
    if idx == 4:
        e["type"] = "enum"
        e["enum_converter"] = "sub_575A60"
    OVERLAYS.setdefault("DAMAGE_FIELD_PARAM", {})[idx] = e

# ACTION_MODULE_INFO sub_56DCD0 (col0 unused in reader)
AMI = {
    1: ("offset_x", "偏移X", "模块挂载点 X（col1 float→+0）", 0),
    2: ("offset_y", "偏移Y", "挂载点 Y（col2→+4）", 4),
    3: ("offset_z", "偏移Z", "挂载点 Z（col3→+8）", 8),
    4: ("module_name", "模块名", "动作模块名窄串（col4 sub_402310→+12）", 12),
    5: ("module_type_id", "模块类型", "模块类型 ID（col5→+96）", 96),
    6: ("script_resource", "脚本资源", "脚本/动作资源路径（col6→+100）", 100),
    7: ("enabled", "启用", "模块启用（col7>0→+128 bool）", 128),
    8: ("mesh_resource", "模型资源", "附加模型路径（col8→+136）", 136),
    9: ("fx_resource", "特效资源", "特效资源路径（col9→+164）", 164),
    10: ("action_param_id", "动作参数ID", "关联 action 参数（col10→+196）", 196),
    11: ("blend_time_ms", "混合时间", "动画混合毫秒（col11→+200）", 200),
    12: ("loop_flag", "循环", "动作循环标志（col12→+204）", 204),
    13: ("cancel_on_move", "移动取消", "移动时取消（col13→+205）", 205),
    14: ("sound_resource", "音效资源", "音效路径（col14→+208）", 208),
    15: ("priority", "优先级", "模块优先级（col15→+132）", 132),
    16: ("mirror_flag", "镜像", "左右镜像（col16→+236）", 236),
}
for idx, (name, disp, meaning, off) in AMI.items():
    e = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "○ASM确证",
    }
    if off is not None:
        e["memory_offset"] = off
    if idx in (4, 6, 8, 9, 14):
        e["type"] = "str"
    elif idx in (7, 12, 13, 16):
        e["type"] = "bool"
    OVERLAYS.setdefault("ACTION_MODULE_INFO", {})[idx] = e

OVERLAYS.setdefault("ACTION_MODULE_INFO", {})[0] = {
    "name": "module_row_id",
    "db_column": "module_row_id",
    "display_name": "行 ID",
    "meaning": "CSV 行索引/模块组 ID（sub_56DCD0 不读 col0；表级键）",
    "type": "u32",
    "status": "confirmed",
    "confidence": "○文档",
}

# BUILDUP_WEAPON: 10 slots × (enable bool col1-10, cost×10 col11-20)
for slot in range(1, 11):
    OVERLAYS.setdefault("BUILDUP_WEAPON", {})[slot] = {
        "name": f"slot_{slot}_enabled",
        "db_column": f"slot_{slot}_enabled",
        "display_name": f"槽{slot}启用",
        "meaning": f"强化槽 {slot} 启用位（sub_570880 col{slot}→bool）",
        "type": "bool",
        "status": "confirmed",
        "confidence": "○ASM确证",
    }
    OVERLAYS.setdefault("BUILDUP_WEAPON", {})[slot + 10] = {
        "name": f"slot_{slot}_cost",
        "db_column": f"slot_{slot}_cost",
        "display_name": f"槽{slot}消耗",
        "meaning": f"强化槽 {slot} 消耗点数（col{slot+10}×10 存盘；sub_570880 @+{4+4*(slot-1)}）",
        "type": "u32",
        "status": "confirmed",
        "confidence": "○ASM确证",
    }

# AI_PARAM distance-band block (cols 18+)
AI_EXTRA = {
    18: ("near_band_param", "近距带参数", "近距离段 sub_56E220 块首 float（→+228）", 228),
    20: ("near_weight_a", "近距权重A", "近距离权重 A（col20×flt_D69A58→+232）", 232),
    21: ("near_weight_b", "近距权重B", "近距离权重 B（→+236）", 236),
    23: ("mid_weight_a", "中距权重A", "中距离权重 A（→+340）", 340),
    24: ("mid_weight_b", "中距权重B", "中距离权重 B（→+344）", 344),
    30: ("far_weight_a", "远距权重A", "远距离权重 A（→+448）", 448),
    31: ("far_weight_b", "远距权重B", "远距离权重 B（→+452）", 452),
    32: ("fire_mode_weight_a", "射击模式A", "射击模式权重 A（归一化→+480）", 480),
    33: ("fire_mode_weight_b", "射击模式B", "射击模式权重 B（→+484）", 484),
    34: ("fire_mode_weight_c", "射击模式C", "射击模式权重 C（→+488）", 488),
    39: ("linked_weapon_param_a", "关联武器参A", "关联 AI_WEAPON_PARAM ID（col0x86→+32）", 32),
    40: ("linked_weapon_param_b", "关联武器参B", "关联 AI_WEAPON_PARAM ID（col0x87→+36）", 36),
    41: ("melee_subtype", "近战子类", "WRESTLE 子类（sub_596990→+2224）", 2224),
}
for idx, (name, disp, meaning, off) in AI_EXTRA.items():
    e = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning,
        "status": "confirmed",
        "confidence": "○ASM确证",
    }
    if off is not None:
        e["memory_offset"] = off
    OVERLAYS.setdefault("AI_PARAM", {})[idx] = e

# WRESTLE float columns generic semantic names
WRESTLE_FLOATS = {
    4: ("strike_damage", "打击伤害", "基础打击伤害倍率"),
    8: ("reach_range", "攻击距离", "有效攻击距离"),
    9: ("hitbox_width", "判定宽度", "命中判定宽度"),
    10: ("hitbox_height", "判定高度", "命中判定高度"),
    11: ("startup_sec", "起手时间", "攻击起手秒数"),
    12: ("active_sec", "生效时间", "判定有效窗口"),
    13: ("recovery_sec", "硬直时间", "攻击后硬直"),
    15: ("knockback", "击退", "击退力度"),
    18: ("combo_scale", "连击缩放", "连击段伤害缩放"),
    22: ("guard_damage", "盾伤", "对盾伤害倍率"),
    37: ("stun_value", "眩晕值", "眩晕/Down 累积"),
}
for idx, (name, disp, meaning) in WRESTLE_FLOATS.items():
    OVERLAYS.setdefault("WRESTLE_PARAM", {})[idx] = {
        "name": name,
        "db_column": name,
        "display_name": disp,
        "meaning": meaning + "（sub_56F5F0 col{} float）".format(idx),
        "status": "confirmed",
        "confidence": "○ASM确证",
    }


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def enum_values_from_fn(enums: dict, fn: str) -> list[dict] | None:
    r = enums.get(fn)
    if not r:
        return None
    if r.get("shape") == "table" and r.get("table"):
        return [{"name": n, "value": v} for n, v in r["table"]]
    lits, consts = r.get("lits") or [], r.get("consts") or []
    if lits and len(lits) == len(consts):
        return [{"name": n, "value": v} for n, v in zip(lits, consts)]
    if lits and consts:
        # cmp-chain partial: pair while consts last, then index for rest
        out = [{"name": n, "value": v} for n, v in zip(lits[: len(consts)], consts)]
        for i, n in enumerate(lits[len(consts) :], start=len(consts)):
            out.append({"name": n, "value": i})
        return out
    if lits:
        return [{"name": n, "value": i} for i, n in enumerate(lits)]
    return None


def build_conv_map(conv: dict) -> dict[tuple[str, int], str]:
    out: dict[tuple[str, int], str] = {}
    for fn, uses in conv.items():
        for u in uses:
            try:
                col = int(str(u["col"]).rstrip("u"), 0)
            except ValueError:
                continue
            out[(u["file"], col)] = fn
    return out


def short_display(meaning: str, name: str) -> str:
    if not meaning:
        return name.replace("_", " ")
    m = re.sub(r"★+\**|\**", "", meaning)
    m = re.sub(r"（`sub_[^`]+`[^）]*）", "", m)
    m = re.sub(r"`[^`]+`", "", m)
    m = m.split("；")[0].split(";")[0].split("（")[0].split("(")[0].strip()
    if len(m) > 24:
        m = m[:22] + "…"
    return m or name


def clean_asm_meaning(c: dict) -> str | None:
    m = c.get("meaning", "")
    if not m.startswith("ASM已映射"):
        return None
    name = c.get("name", "field")
    off = c.get("memory_offset")
    reader = c.get("asm_reader", "")
    va = c.get("asm_va", "")
    parts = [f"{name}："]
    if reader:
        parts.append(f"{reader}")
    if off is not None:
        parts.append(f"mem+{off}")
    if va:
        parts.append(va)
    return " ".join(parts)


def apply_overlay(c: dict, ov: dict) -> None:
    for k, v in ov.items():
        if v is not None:
            c[k] = v


def enrich_column(c: dict, table_id: str, csv_path: str, conv_map: dict, enums: dict) -> None:
    idx = c.get("csv_index")
    if idx is None:
        return

    ov = OVERLAYS.get(table_id, {}).get(idx, {})
    if ov:
        apply_overlay(c, ov)

    fn = c.get("enum_converter") or conv_map.get((csv_path, idx))
    if fn and fn != "?":
        c["enum_converter"] = fn
        vals = c.get("enum_values") or enum_values_from_fn(enums, fn)
        if vals:
            c["enum_values"] = vals
            c["enum_doc"] = ENUM_DOC

    cleaned = clean_asm_meaning(c)
    if cleaned and (not c.get("meaning") or c["meaning"].startswith("ASM已映射")):
        c["meaning"] = cleaned

    name = c.get("name", "")
    disp = c.get("display_name", "")
    if c.get("meaning") and (
        not disp
        or disp == c.get("meaning")
        or len(disp) > 40
        or "： sub_" in disp
        or disp.startswith("ASM已映射")
    ):
        c["display_name"] = short_display(c["meaning"], name)

    # Resource-list columns parsed via sub_402310 are string lists, not numeric enums
    if c.get("enum_converter") == "sub_402310" and c.get("type") == "enum":
        c["type"] = "str"
        c.pop("enum_values", None)

    db = c.get("db_column", "")
    if name and not re.match(r"^(field_|unknown_|enum_|col\d|param_u32|float_param_)", name):
        if re.match(r"^(field_|unknown_|enum_|col\d|param_u32|float_param_)", db or ""):
            c["db_column"] = name

    has_sem = name and not re.match(r"^(field_|unknown_|param_u32|enum_\d|flag_\d|cap_flag_b|render_u32_)", name)
    has_asm = c.get("asm_va") or c.get("memory_offset") is not None
    if c.get("status") != "confirmed":
        if ov.get("status") == "partial":
            c["status"] = "partial"
        elif has_sem and (has_asm or c.get("enum_values") or c.get("type") == "str"):
            if not c.get("meaning", "").startswith("浮点参数") and "待定" not in c.get("meaning", ""):
                c["status"] = "confirmed"
                if not c.get("confidence"):
                    c["confidence"] = "○ASM确证"


def sync_md(md_path: Path, data: dict) -> None:
    if not md_path.is_file():
        return
    lines = md_path.read_text(encoding="utf-8").splitlines()
    col_by_csv: dict[int, dict] = {c["csv_index"]: c for c in data.get("columns", [])}
    out: list[str] = []
    for line in lines:
        if line.startswith("|") and "`" in line:
            parts = [p.strip() for p in line.split("|")]
            # | read_order | `csv_idx` | type | meaning |
            if len(parts) >= 5:
                m = re.search(r"`(\d+)`", parts[2])
                if m:
                    csv_idx = int(m.group(1))
                    col = col_by_csv.get(csv_idx)
                    if col:
                        disp = col.get("display_name") or col.get("name", "")
                        meaning = col.get("meaning", disp)
                        conf = col.get("confidence", "")
                        star = "★" if col.get("status") == "confirmed" else ""
                        if col.get("enum_converter") and col.get("type") == "enum":
                            fn = col["enum_converter"]
                            cell = f"{star}**{disp}**（`{fn}`）— {meaning[:140]}"
                        elif star:
                            cell = f"★**{disp}** — {meaning[:140]}"
                        elif len(meaning) > 24:
                            cell = f"{disp} — {meaning[:120]}"
                        else:
                            cell = meaning
                        parts[4] = cell
                        line = "| " + " | ".join(parts[1:4] + [parts[4]]) + " |"
        out.append(line)
    md_path.write_text("\n".join(out) + "\n", encoding="utf-8")


def finalize_stats(data: dict) -> None:
    cols = data.get("columns", [])
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_defined"] = len(cols)


def main() -> None:
    enums = load_json(ENUMS_JSON)
    conv_map = build_conv_map(load_json(ENUM_CONV))
    summary: list[tuple[str, int, int, list[str]]] = []

    for tid in TARGETS:
        path = TABLES_DIR / f"{tid}.json"
        data = load_json(path)
        csv_path = data.get("csv_path", "")
        renames: list[str] = []

        for c in data.get("columns", []):
            old_name = c.get("name")
            enrich_column(c, tid, csv_path, conv_map, enums)
            if old_name and c.get("name") != old_name:
                renames.append(f"{old_name}→{c['name']}")

        if tid in ("WEAPON_SETTING", "BULLET"):
            patch = patch_weapon_column if tid == "WEAPON_SETTING" else patch_bullet_column
            for column in data["columns"]:
                patch(column)
            if tid == "BULLET":
                data["column_count"] = 39
        finalize_stats(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        md_rel = data.get("source_md", "")
        md_path = ROOT / md_rel if md_rel else DATATABLES
        if not md_path.is_file() and md_rel:
            md_path = DATATABLES / Path(md_rel).name
        sync_md(md_path, data)

        summary.append((tid, len(data["columns"]), data["column_confirmed"], renames[:8]))

    print(f"{'TABLE':<22} {'COLS':>5} {'CONF':>5}  NOTABLE RENAMES")
    print("-" * 70)
    for tid, n, conf, renames in summary:
        rn = ", ".join(renames[:4]) if renames else "—"
        if len(renames) > 4:
            rn += f" (+{len(renames)-4})"
        print(f"{tid:<22} {n:>5} {conf:>5}  {rn}")


if __name__ == "__main__":
    main()
