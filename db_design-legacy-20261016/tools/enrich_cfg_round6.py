#!/usr/bin/env python3
"""Round 6 cfg enrichment: remaining small tables — enum gaps + column fixes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = ROOT / "db_design" / "schema" / "cfg" / "tables"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

# Reuse MD writer from round 5
sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrich_cfg_round5 import enum_values, recount, write_md  # noqa: E402

GAP_MEANING = "CSV 列存在但 IDA 读表未单独取证（默认 0）"


def seq_enum(prefix: str, count: int) -> list[dict]:
    return [{"name": f"{prefix}{i}", "value": i} for i in range(count + 1)]


def patch_col(
    data: dict,
    csv_index: int,
    *,
    match_name: str | None = None,
    **kw,
) -> None:
    candidates = [c for c in data["columns"] if c.get("csv_index") == csv_index]
    if match_name is not None:
        candidates = [c for c in candidates if c.get("name") == match_name]
    elif len(candidates) > 1:
        raise KeyError(
            f"{data['id']} csv_index={csv_index} is ambiguous; pass match_name="
            + str([c.get("name") for c in candidates])
        )
    if not candidates:
        raise KeyError(f"{data['id']} missing csv_index={csv_index} match_name={match_name}")
    c = candidates[0]
    if kw.get("meaning"):
        kw.setdefault("display_name", kw["meaning"].split("（")[0][:28])
    for k, v in kw.items():
        if v is None:
            c.pop(k, None)
        else:
            c[k] = v


def pop_key(data: dict, csv_index: int, key: str) -> None:
    for c in data["columns"]:
        if c.get("csv_index") == csv_index:
            c.pop(key, None)
            return


def enrich_lvup_clan(enums: dict) -> dict:
    path = TABLES_DIR / "LVUP_CLAN.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    rokaku = seq_enum("ROKAKU_LV", 5)
    shop = seq_enum("SHOP_LV", 21)
    deck = seq_enum("DECKCOST_LV", 5)
    discount = seq_enum("DISCOUNT_LV", 10)

    patch_col(
        data,
        1,
        name="member_cap",
        db_column="member_cap",
        meaning="成员上限（u32 col1 → +0）",
        display_name="成员上限",
        status="confirmed",
        confidence="★确证",
        memory_offset=0,
    )
    patch_col(
        data,
        4,
        meaning="升级经验基数（u32 col4 → +12）",
        display_name="经验基数",
        status="confirmed",
        confidence="★确证",
    )
    patch_col(
        data,
        5,
        meaning="升级经验增量（u32 col5 → +16；与 col4 合成总需求）",
        display_name="经验增量",
        status="confirmed",
        confidence="★确证",
    )
    patch_col(
        data,
        6,
        name="rokaku_level",
        db_column="rokaku_level",
        meaning="着陆平台等级档（enum col6 sub_578EE0：ROKAKU_LV0..5 → +28）",
        display_name="着陆平台等级",
        status="confirmed",
        confidence="★确证",
        enum_converter="sub_578EE0",
        enum_values=rokaku,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        7,
        meaning="部队 GP 加成（u32 col7 → +32）",
        display_name="GP 加成",
        status="confirmed",
        confidence="○ASM确证",
    )
    patch_col(
        data,
        8,
        name="shop_level",
        db_column="shop_level",
        meaning="部队商店等级（enum col8 sub_5790B0：SHOP_LV0..21 → +36）",
        display_name="商店等级",
        status="confirmed",
        confidence="★确证",
        enum_converter="sub_5790B0",
        enum_values=shop,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        9,
        name="deck_cost_level",
        db_column="deck_cost_level",
        meaning="卡组 COST 上限档（enum col9 sub_579500：DECKCOST_LV0..5 → +40）",
        display_name="卡组 COST 档",
        status="confirmed",
        confidence="★确证",
        enum_converter="sub_579500",
        enum_values=deck,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        10,
        name="bonus_gp",
        db_column="bonus_gp",
        type="u32",
        meaning="等级奖励 GP 数（u32 col10 → +44）",
        display_name="奖励 GP",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=44,
    )
    pop_key(data, 10, "enum_converter")
    pop_key(data, 10, "enum_doc")
    patch_col(
        data,
        11,
        name="discount_level",
        db_column="discount_level",
        meaning="商店折扣档（enum col11 sub_5796D0：DISCOUNT_LV0..10 → +48）",
        display_name="折扣档",
        status="confirmed",
        confidence="★确证",
        enum_converter="sub_5796D0",
        enum_values=discount,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        12,
        meaning="扩展参数（u32 col12 → +52）",
        display_name="扩展参数",
        status="confirmed",
        confidence="○ASM确证",
    )
    recount(data)
    return data


def enrich_banner_info() -> dict:
    data = json.loads((TABLES_DIR / "BANNER_INFO.json").read_text(encoding="utf-8"))
    str_cols = [
        (1, "display_scene", "显示场景标签（wstring col1；sub_BBB130→+4，无固定枚举表）"),
        (2, "banner_type", "横幅类型标签（wstring col2 → +32）"),
        (3, "priority", "显示优先级标签（wstring col3 → +60）"),
        (4, "link_type", "链接类型标签（wstring col4 → +88）"),
    ]
    for ci, name, meaning in str_cols:
        patch_col(
            data,
            ci,
            name=name,
            db_column=name,
            type="str",
            meaning=meaning,
            display_name=meaning.split("（")[0],
            status="confirmed",
            confidence="★确证",
            asm_reader="sub_56FF30",
        )
        pop_key(data, ci, "enum_converter")
        pop_key(data, ci, "enum_values")
        pop_key(data, ci, "enum_doc")

    patch_col(
        data,
        5,
        asm_va="0x57018c",
        status="confirmed",
    )
    patch_col(
        data,
        6,
        name="display_period",
        db_column="display_period",
        type="str",
        meaning="显示时段（str col6/7；sub_56FDA0 解析 /// ::: 日期时间格式 → +116/+128）",
        display_name="显示时段",
        status="confirmed",
        confidence="★确证",
        asm_va="0x5701a0",
        asm_reader="sub_56FF30",
        memory_offset=128,
    )
    pop_key(data, 6, "enum_converter")
    patch_col(
        data,
        7,
        meaning="跳转链接 ID（u32 col7）",
        display_name="链接 ID",
        status="confirmed",
        confidence="★确证",
    )
    recount(data)
    return data


def enrich_module_bonus_lot() -> dict:
    data = json.loads((TABLES_DIR / "MODULE_BONUS_LOT.json").read_text(encoding="utf-8"))
    role_enum = [
        {"name": n, "value": v}
        for n, v in [
            ("ASSAULT_A", 1),
            ("ASSAULT_B", 2),
            ("SNIPE", 3),
            ("CANNON", 4),
            ("SUPPORT", 5),
        ]
    ]
    rank_enum = enum_values(json.loads(ENUMS_JSON.read_text(encoding="utf-8")), "sub_580610")

    patch_col(
        data,
        0,
        type="str",
        meaning="抽取键（str col0；如 ASSAULT_A×RANK1 组合键，原样存储）",
        display_name="抽取键",
        status="confirmed",
    )
    pop_key(data, 0, "enum_converter")
    patch_col(
        data,
        1,
        meaning="战斗角色类别（str enum col1；sub_5804F0 词表：ASSAULT_A/SNIPE/CANNON/SUPPORT 等）",
        display_name="角色类别",
        enum_converter="sub_5804F0",
        enum_values=role_enum,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        2,
        display_name="抽取权重",
        meaning="抽取权重（u32 col2）",
    )
    patch_col(
        data,
        5,
        display_name="加成组 ID",
        meaning="目标 MODULE_BONUS.bonus_group（u32 col5）",
    )
    patch_col(
        data,
        6,
        type="str",
        meaning="奖励类型（str col6；原样字符串，读表无独立转换函数）",
        display_name="奖励类型",
        status="confirmed",
    )
    for ci, dn in [(7, "奖励参数 A"), (8, "奖励参数 B"), (9, "奖励参数 C")]:
        patch_col(data, ci, display_name=dn)

    _ = rank_enum  # RANK1..5 documented in CHARA_PARAM / sub_580610
    recount(data)
    return data


def enrich_season_class_info() -> dict:
    data = json.loads((TABLES_DIR / "SEASON_CLASS_IMFORMATION.json").read_text(encoding="utf-8"))
    patch_col(
        data,
        1,
        type="str",
        meaning="阶级名称（wstring col1 sub_402310 → +4）",
        display_name="阶级名称",
        status="confirmed",
        confidence="★确证",
        asm_reader="sub_5900A0",
        asm_va="0x5900e1",
    )
    pop_key(data, 1, "enum_converter")
    u16_cols = [
        (2, "rank_min", "+32", "适用排名下限"),
        (3, "rank_max", "+34", "适用排名上限"),
        (4, "point_threshold", "+36", "阶级点数阈值"),
        (5, "promotion_wins", "+38", "升阶所需胜场"),
        (6, "demotion_losses", "+40", "降阶败场阈值"),
        (7, "season_bonus", "+44", "赛季加成系数"),
        (8, "icon_id", "+46", "阶级图标 ID"),
        (9, "display_color", "+48", "UI 显示颜色"),
    ]
    for ci, name, off, label in u16_cols:
        patch_col(
            data,
            ci,
            name=name,
            db_column=name,
            type="u16",
            memory_offset=int(off.replace("+", "")),
            meaning=f"{label}（u16 col{ci} → {off}）",
            display_name=label,
            status="confirmed",
            confidence="★确证",
            asm_reader="sub_5900A0",
        )
    patch_col(
        data,
        10,
        type="u16",
        memory_offset=50,
        status="confirmed",
        confidence="★确证",
    )
    patch_col(
        data,
        11,
        type="u16",
        memory_offset=52,
        status="confirmed",
        confidence="★确证",
    )
    recount(data)
    return data


def enrich_season_class_up_reward() -> dict:
    data = json.loads((TABLES_DIR / "SEASON_CLASS_UP_REWARD.json").read_text(encoding="utf-8"))
    patch_col(
        data,
        1,
        name="reward_param",
        db_column="reward_param",
        type="u32",
        meaning="奖励参数 A（u32 col1 → +4；ASM 直读 u32）",
        display_name="奖励参数 A",
        status="confirmed",
        confidence="★确证",
        asm_va="0x590f14",
        asm_reader="sub_590ED0",
    )
    pop_key(data, 1, "enum_converter")
    patch_col(
        data,
        2,
        name="reward_title",
        db_column="reward_title",
        type="str",
        meaning="奖励标题（wstring col2 sub_402310 → +8）",
        display_name="奖励标题",
        status="confirmed",
        confidence="★确证",
        asm_va="0x590f1d",
        asm_reader="sub_590ED0",
    )
    pop_key(data, 2, "enum_converter")
    patch_col(
        data,
        3,
        name="primary_reward_value",
        db_column="primary_reward_value",
        meaning="主奖励数值（u32 col3 → +36；GP 或物品 ID 依配置）",
        display_name="主奖励数值",
        status="confirmed",
        confidence="○ASM确证",
        asm_va="0x590f61",
        memory_offset=36,
    )
    patch_col(
        data,
        4,
        name="reward_item_id",
        meaning="奖励物品 ID（u32 col4 → ITEM；首槽）",
        display_name="奖励物品 ID",
        status="confirmed",
        confidence="★确证",
        memory_offset=40,
    )
    patch_col(
        data,
        5,
        name="reward_item_qty",
        meaning="奖励物品数量（u32 col5；首槽）",
        display_name="物品数量",
        status="confirmed",
        confidence="★确证",
        memory_offset=44,
    )
    patch_col(
        data,
        6,
        name="reward_item_name",
        db_column="reward_item_name",
        type="str",
        meaning="奖励物品名称（wstring col6；首槽说明）",
        display_name="物品名称",
        status="confirmed",
        confidence="★确证",
    )
    patch_col(
        data,
        7,
        name="bonus_item_id",
        meaning="附加物品 ID（u32 col7；二槽）",
        display_name="附加物品 ID",
        status="confirmed",
        confidence="★确证",
        memory_offset=112,
    )
    patch_col(
        data,
        8,
        name="bonus_item_qty",
        meaning="附加物品数量（u32 col8；二槽）",
        display_name="附加物品数量",
        status="confirmed",
        confidence="★确证",
        memory_offset=116,
    )
    patch_col(
        data,
        9,
        name="bonus_item_name",
        db_column="bonus_item_name",
        type="str",
        meaning="附加物品名称（wstring col9；二槽说明）",
        display_name="附加物品名称",
        status="confirmed",
        confidence="★确证",
    )
    recount(data)
    return data


def enrich_msma_breakup() -> dict:
    data = json.loads((TABLES_DIR / "MSMA_BREAKUP.json").read_text(encoding="utf-8"))
    faction_ev = [
        {"name": "EFF", "value": 0},
        {"name": "ZEON", "value": 1},
        {"name": "INVALID", "value": -1},
    ]
    breakup_ev = [
        {"name": "SILVER", "value": 0},
        {"name": "GOLD", "value": 1},
        {"name": "PLATINUM", "value": 2},
    ]
    patch_col(
        data,
        1,
        meaning="阵营（enum col1 sub_40CE20：EFF=0 / ZEON=1 / 其它=-1 → +4）",
        display_name="阵营",
        enum_values=faction_ev,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        2,
        meaning="战斗明细引用（enum col2 sub_5812E0 查 MSMA_BATTLE_DETAIL 属性名 → +8）",
        display_name="战斗明细引用",
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        3,
        meaning="拆解产物等级（enum col3 sub_57BDE0：SILVER=0/GOLD=1/PLATINUM=2 → +12）",
        display_name="拆解产物等级",
        enum_values=breakup_ev,
        enum_doc=ENUM_DOC,
    )
    patch_col(
        data,
        4,
        display_name="拆解参数 A",
        meaning="拆解参数 A（u32 col4 → +16）",
        status="confirmed",
        confidence="○ASM确证",
    )
    patch_col(
        data,
        6,
        display_name="拆解参数 B",
        meaning="拆解参数 B（u32 col6 → +20；跳过 col5 空列）",
        status="confirmed",
        confidence="○ASM确证",
    )
    recount(data)
    return data


def enrich_msma_material() -> dict:
    data = json.loads((TABLES_DIR / "MSMA_MATERIAL.json").read_text(encoding="utf-8"))
    mat_ev = [
        {"name": n, "value": v}
        for n, v in [
            ("ARMOR", 0),
            ("GENERATOR", 1),
            ("FRAME", 2),
            ("MANIPULATOR", 3),
            ("SENSOR", 4),
            ("THRUSTER", 5),
            ("SPECIAL", 6),
        ]
    ]
    patch_col(
        data,
        2,
        meaning="素材类别（enum col2 sub_594230：ARMOR/GENERATOR/… → +4）",
        display_name="素材类别",
        status="confirmed",
        confidence="★确证",
        enum_values=mat_ev,
        enum_doc=ENUM_DOC,
    )
    for ci, lbl, off in [
        (3, "base_rate", 8),
        (4, "tier2_rate", 12),
        (5, "tier3_rate", 16),
        (6, "tier4_rate", 20),
        (7, "tier5_rate", 24),
        (8, "tier6_rate", 28),
    ]:
        patch_col(
            data,
            ci,
            meaning=f"开发成功率 {lbl}（float col{ci} → +{off}）",
            display_name=lbl,
            status="confirmed",
            confidence="★确证",
        )
    recount(data)
    return data


def enrich_monthly_bonus(enums: dict) -> dict:
    data = json.loads((TABLES_DIR / "MONTHLY_BONUS_REWARD.json").read_text(encoding="utf-8"))
    login_ev = [
        {"name": "LOGIN", "value": 0},
        {"name": "XWAR", "value": 1},
        {"name": "INVALID", "value": -1},
    ]
    reward_ev = [
        {"name": "GP", "value": 999},
        {"name": "ITEM", "value": 0},
        {"name": "MSMA", "value": 1},
        {"name": "BUILDUP_MSMA", "value": 998},
    ]
    patch_col(
        data,
        1,
        type="u16",
        meaning="年月编码（u16 col1 → +4；YYYYMM 或序数）",
        display_name="年月",
        status="confirmed",
        confidence="★确证",
        memory_offset=4,
    )
    patch_col(
        data,
        2,
        meaning="登录渠道（enum col2 比较链：LOGIN=0 / XWAR=1 / 其它=-1 → +8）",
        display_name="登录渠道",
        status="confirmed",
        confidence="★确证",
        enum_values=login_ev,
        enum_doc=ENUM_DOC,
        memory_offset=8,
    )
    pop_key(data, 2, "enum_converter")
    patch_col(
        data,
        3,
        type="u16",
        meaning="月份内日序（u16 col3 → +12；第几天登录领取）",
        display_name="日序",
        status="confirmed",
        confidence="★确证",
        memory_offset=12,
    )
    patch_col(
        data,
        4,
        meaning="奖励物类型（enum col4 sub_5703A0：GP=999/ITEM=0/MSMA=1/BUILDUP_MSMA=998 → +16）",
        display_name="奖励物类型",
        status="confirmed",
        confidence="★确证",
        enum_values=reward_ev,
        memory_offset=16,
    )
    for ci, name, off in [
        (5, "reward_param_id", 20),
        (6, "reward_quantity", 24),
        (7, "bonus_flag", 28),
    ]:
        patch_col(
            data,
            ci,
            status="confirmed",
            confidence="○ASM确证" if ci == 7 else "★确证",
            memory_offset=off,
        )
    recount(data)
    return data


def enrich_score_config_category() -> dict:
    data = json.loads((TABLES_DIR / "SCORE_CONFIG_CATEGORY.json").read_text(encoding="utf-8"))
    patch_col(
        data,
        0,
        asm_reader="sub_58DDB0",
        asm_va="0x58ddd0",
    )
    patch_col(
        data,
        1,
        name="category_index",
        type="enum",
        meaning="计分分类索引（enum col1 sub_5812E0 查 score_config 行 → 返回 +40 索引）",
        display_name="分类索引",
        status="confirmed",
        confidence="★确证",
        enum_converter="sub_5812E0",
        enum_doc=ENUM_DOC,
        asm_reader="sub_58DDB0",
        asm_va="0x58ddf3",
    )
    recount(data)
    return data


def enrich_item_part() -> dict:
    data = json.loads((TABLES_DIR / "ITEM_PART.json").read_text(encoding="utf-8"))
    numeric_str_note = "（numeric str→sub_CC6CA8/strtol；无命名字面量表）"
    patch_col(
        data,
        18,
        match_name="key_action_a",
        name="key_action_a",
        type="str",
        meaning=f"键位/动作 A {numeric_str_note}",
        display_name="键位动作 A",
        enum_converter="sub_CC6CA8",
        enum_doc=ENUM_DOC,
        enum_values=None,
    )
    patch_col(
        data,
        19,
        match_name="key_action_b",
        name="key_action_b",
        type="str",
        meaning=f"键位/动作 B {numeric_str_note}",
        display_name="键位动作 B",
        enum_converter="sub_CC6CA8",
        enum_doc=ENUM_DOC,
        enum_values=None,
    )
    patch_col(
        data,
        18,
        match_name="loop_param_value",
        name="loop_param_value",
        type="float",
        meaning="循环参数值（float col18 → +80；8 组 effect_scope×stat 循环）",
        display_name="循环参数值",
        memory_offset=80,
        asm_va="0x59580e",
        enum_converter=None,
        enum_doc=None,
    )
    recount(data)
    return data


def stats(data: dict) -> dict:
    enum_filled = sum(
        1
        for c in data.get("columns", [])
        if c.get("type") == "enum" and c.get("enum_values")
    )
    enum_cols = sum(1 for c in data.get("columns", []) if c.get("type") == "enum")
    return {
        "confirmed": data.get("column_confirmed", 0),
        "partial": data.get("column_partial", 0),
        "gap": data.get("column_gap", 0),
        "enum_cols": enum_cols,
        "enum_filled": enum_filled,
    }


def main() -> None:
    enums = json.loads(ENUMS_JSON.read_text(encoding="utf-8"))
    builders = [
        ("LVUP_CLAN", lambda: enrich_lvup_clan(enums)),
        ("BANNER_INFO", enrich_banner_info),
        ("MODULE_BONUS_LOT", enrich_module_bonus_lot),
        ("SEASON_CLASS_IMFORMATION", enrich_season_class_info),
        ("SEASON_CLASS_UP_REWARD", enrich_season_class_up_reward),
        ("MSMA_BREAKUP", enrich_msma_breakup),
        ("MSMA_MATERIAL", enrich_msma_material),
        ("MONTHLY_BONUS_REWARD", lambda: enrich_monthly_bonus(enums)),
        ("SCORE_CONFIG_CATEGORY", enrich_score_config_category),
        ("ITEM_PART", enrich_item_part),
    ]
    print("=== Round 6 cfg enrichment ===\n")
    for tid, builder in builders:
        data = builder()
        path = TABLES_DIR / f"{tid}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_md(data)
        s = stats(data)
        print(
            f"{tid}: confirmed={s['confirmed']} partial={s['partial']} gap={s['gap']} "
            f"enum={s['enum_filled']}/{s['enum_cols']}"
        )


if __name__ == "__main__":
    main()
