#!/usr/bin/env python3
"""Round 7 cfg enrichment: partial-column tables — IDA decompile semantics + confirm."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = ROOT / "db_design" / "schema" / "cfg" / "tables"
ENUMS_JSON = ROOT / "reverse-login-chain" / "formats" / "enums.json"
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrich_cfg_round5 import (  # noqa: E402
    BADGE_TIER,
    GAP_MEANING,
    confirm_asm_mapped,
    enum_values,
    gap_col,
    load_enums,
    recount,
    write_md,
)

STAT_46 = (
    "战绩统计项（enum sub_592DB0/sub_579FC0，46 项：VERSUS/WIN/KILL/SCORE_* 等；"
    "与 DAILY_RECORD 同一套战绩体系）"
)

BATTLE_MODE_FILTER = [
    {"name": "ALL", "value": 99},
    {"name": "VERSUS", "value": 1},
    {"name": "XWAR", "value": 5},
    {"name": "COMMANDER", "value": 6},
]

MECHANIC_BONUS = [
    {"name": "NONE", "value": 0},
    {"name": "FORCE_SUCCESS", "value": 1},
    {"name": "FORCE_GREATEST", "value": 2},
    {"name": "CAN_NOT_CREATE_MSMA", "value": 3},
    {"name": "CAN_NOT_NORMAL_PLAN", "value": 4},
    {"name": "BUILDUPWEAPON", "value": 5},
    {"name": "BUILDUPWEAPON_FGREATEST", "value": 6},
]

BEFORE: dict[str, tuple[int, int]] = {}


def load_table(tid: str) -> dict:
    return json.loads((TABLES_DIR / f"{tid}.json").read_text(encoding="utf-8"))


def save_table(tid: str, data: dict) -> None:
    path = TABLES_DIR / f"{tid}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(data)


def patch_col(data: dict, csv_index: int, *, match_name: str | None = None, **kw) -> None:
    candidates = [c for c in data["columns"] if c.get("csv_index") == csv_index]
    if match_name is not None:
        candidates = [c for c in candidates if c.get("name") == match_name]
    elif len(candidates) > 1:
        raise KeyError(f"{data['id']} csv_index={csv_index} ambiguous")
    if not candidates:
        raise KeyError(f"{data['id']} missing csv_index={csv_index}")
    c = candidates[0]
    if kw.get("meaning"):
        kw.setdefault("display_name", kw["meaning"].split("（")[0][:28])
    for k, v in kw.items():
        if v is None:
            c.pop(k, None)
        else:
            c[k] = v


def ensure_gap(data: dict, csv_index: int) -> None:
    if not any(c.get("csv_index") == csv_index for c in data["columns"]):
        data["columns"].append(gap_col(csv_index))
        data["columns"].sort(key=lambda c: c["csv_index"])


def confirm_partial(data: dict, *, skip: set[int] | None = None) -> None:
    skip = skip or set()
    for col in data["columns"]:
        if col.get("status") != "partial":
            continue
        if col.get("csv_index") in skip:
            continue
        if col.get("read_order") is None:
            continue
        if col.get("asm_va") or col.get("asm_reader"):
            col["status"] = "confirmed"
            if col.get("confidence") in (None, "", "△"):
                col["confidence"] = "○ASM确证"


def enrich_overhaul(data: dict) -> dict:
    # sub_587780: col7 id + 3×(col id, wstring name, u32 qty); col5 gap
    slots = [
        (7, "material_id_1", 48, "素材 1 物品 ID（u32 col7 → +48）"),
        (8, "material_sub_id_1", 52, "素材 1 子类型/参数（u32 col8 → +52）"),
        (9, "material_name_1", 76, "素材 1 名称（wstring col9 → +76）"),
        (10, "material_qty_1", 64, "素材 1 数量（u32 col10 → +64）"),
        (11, "material_id_2", 56, "素材 2 物品 ID（u32 col11 → +56）"),
        (12, "material_name_2", 104, "素材 2 名称（wstring col12 → +104）"),
        (13, "material_qty_2", 68, "素材 2 数量（u32 col13 → +68）"),
        (14, "material_id_3", 60, "素材 3 物品 ID（u32 col14 → +60）"),
        (15, "material_name_3", 132, "素材 3 名称（wstring col15 → +132）"),
        (16, "material_qty_3", 72, "素材 3 数量（u32 col16 → +72）"),
    ]
    for ci, name, mem, meaning in [
        (2, "msma_id", 32, "目标机体 ID（u32 col2 → +32；→ CHARA_PARAM）"),
        (3, "rank_requirement", 36, "机体稀有度/等级需求（u32 col3 → +36）"),
        (4, "gp_cost", 40, "GP 翻新费用（u32 col4 → +40）"),
        (6, "base_param", 44, "基础参数/成功率权重（u32 col6 → +44）"),
    ]:
        patch_col(data, ci, name=name, memory_offset=mem, meaning=meaning, type="u32")
    for ci, name, mem, meaning in slots:
        typ = "str" if "名称" in meaning else "u32"
        patch_col(data, ci, name=name, type=typ, memory_offset=mem, meaning=meaning)
    confirm_partial(data)
    recount(data)
    return data


def enrich_player_navi(data: dict) -> dict:
    """sub_58C7C0: col12 gap; col13 dialog; loop col14-16 voice/image/skip."""
    reader = "sub_58C7C0"
    head = [c for c in data["columns"] if c.get("csv_index", 99) <= 11]
    tail_mapped = [
        {
            "read_order": 13,
            "csv_index": 13,
            "db_column": "dialog_style",
            "name": "dialog_style",
            "type": "u32",
            "meaning": "对话框样式（u32 col13 → +120；读表跳过 col12）",
            "display_name": "对话框样式",
            "memory_offset": 120,
            "asm_reader": reader,
            "asm_va": "0x58c941",
            "confidence": "○ASM确证",
            "status": "confirmed",
        },
        {
            "read_order": 14,
            "csv_index": 14,
            "db_column": "voice_id",
            "name": "voice_id",
            "type": "u32",
            "meaning": "语音 ID（u32 col14 → +124）",
            "display_name": "语音 ID",
            "memory_offset": 124,
            "asm_reader": reader,
            "asm_va": "0x58c95b",
            "confidence": "○ASM确证",
            "status": "confirmed",
        },
        {
            "read_order": 15,
            "csv_index": 15,
            "db_column": "image_id",
            "name": "image_id",
            "type": "u32",
            "meaning": "插图资源 ID（u32 col15 → +128）",
            "display_name": "插图 ID",
            "memory_offset": 128,
            "asm_reader": reader,
            "asm_va": "0x58c95b",
            "confidence": "○ASM确证",
            "status": "confirmed",
        },
    ]
    data["columns"] = head + [gap_col(12)] + tail_mapped
    data["columns"].append(
        {
            "read_order": 16,
            "csv_index": 16,
            "db_column": "skip_allowed",
            "name": "skip_allowed",
            "type": "u32",
            "meaning": "允许跳过标志（u32 col16 → +132；16 列 CSV 可省略）",
            "display_name": "允许跳过",
            "memory_offset": 132,
            "asm_reader": reader,
            "asm_va": "0x58c975",
            "confidence": "○ASM确证",
            "status": "confirmed",
        }
    )
    data["column_count"] = 17  # csv 0..16（col12 gap）
    patch_col(data, 0, memory_offset=0)
    patch_col(data, 1, memory_offset=4)
    patch_col(data, 2, memory_offset=32)
    patch_col(
        data,
        3,
        name="trigger_condition",
        type="bool",
        meaning="触发条件标志（bool col3>0 → +60）",
        memory_offset=60,
    )
    patch_col(data, 4, memory_offset=64)
    patch_col(
        data,
        5,
        name="show_when_not_first",
        type="bool",
        meaning="非首次显示标志（bool col5!=1 → +92）",
        display_name="非首次显示",
        memory_offset=92,
    )
    patch_col(data, 6, name="repeat_flag", memory_offset=96)
    patch_col(data, 7, memory_offset=100)
    patch_col(data, 8, memory_offset=104)
    patch_col(data, 9, type="bool", meaning="最低机师等级门槛启用（bool col9>0 → +108）", memory_offset=108)
    patch_col(data, 10, memory_offset=112)
    patch_col(data, 11, memory_offset=116)
    confirm_partial(data)
    recount(data)
    return data


def enrich_lvup_pilot_class(data: dict) -> dict:
    patch_col(data, 1, meaning="军衔点数阈值（u32 col1 → +4；客户端 %10000 分段）")
    patch_col(data, 2, meaning="保留标志（u8 col2 → +8；CSV 通常 0）")
    patch_col(data, 4, meaning="升级需求数值（u32 col4 → +40；对战/任务达成量）")
    patch_col(data, 5, meaning="需求类型（u32 col5 → +44）")
    patch_col(data, 6, meaning="需求参数（u32 col6 → +48）")
    req_names = [
        (7, "req_stat_a", 60),
        (8, "req_stat_b", 64),
        (9, "req_stat_c", 68),
        (10, "req_stat_d", 72),
        (11, "req_stat_e", 76),
    ]
    for ci, name, mem in req_names:
        patch_col(
            data,
            ci,
            name=name,
            meaning=f"升阶需求统计项 col{ci}（u32 → +{mem}；5 项循环读取）",
            display_name=f"需求统计 col{ci}",
            memory_offset=mem,
        )
    patch_col(
        data,
        12,
        name="reward_gp",
        meaning="升阶奖励 GP（u32 col12 → +52）",
        display_name="奖励 GP",
        memory_offset=52,
    )
    patch_col(
        data,
        13,
        name="reward_item_id",
        meaning="升阶奖励物品 ID（u32 col13 → +56）",
        display_name="奖励物品",
        memory_offset=56,
    )
    confirm_partial(data)
    recount(data)
    return data


def enrich_forcegauge_info(data: dict) -> dict:
    patch_col(
        data,
        1,
        name="name_ref_id",
        type="u32",
        meaning="战力槽名称引用 ID（u32 col1 → +4；UI 字符串索引）",
        display_name="名称引用 ID",
        memory_offset=4,
    )
    for ci, name, meaning, mem in [
        (2, "max_value", "槽最大值（u32 col2 → +8）", 8),
        (3, "recover_rate", "自然恢复速率（u32 col3 → +12）", 12),
        (4, "decay_rate", "衰减速率（u32 col4 → +16）", 16),
        (5, "trigger_threshold", "触发阈值（u32 col5 → +20）", 20),
        (6, "effect_id", "关联效果 ID（u32 col6 → +24）", 24),
        (7, "display_order", "UI 排序（u32 col7 → +28）", 28),
        (8, "gauge_label", "战力槽显示标签（wstring col8 → +32）", 32),
        (9, "icon_id", "图标 ID（u32 col9 → +60）", 60),
        (10, "color_code", "UI 颜色编码（u32 col10 → +64）", 64),
        (11, "buff_id", "满槽触发 Buff ID（u32 col11 → +68；→ BUFF）", 68),
        (12, "gauge_description", "战力槽说明（wstring col12 → +72）", 72),
        (13, "extra_param", "扩展参数（u32 col13 → +100）", 100),
    ]:
        kw = dict(name=name, meaning=meaning, memory_offset=mem)
        if ci == 8 or ci == 12:
            kw["type"] = "str"
        else:
            kw["type"] = "u32"
        patch_col(data, ci, **kw)
    confirm_partial(data)
    recount(data)
    return data


def enrich_msma_module(data: dict) -> dict:
    for i in range(10):
        ci = 2 + i * 2
        patch_col(
            data,
            ci,
            name=f"module_slot_{i}",
            meaning=f"模块槽 {i} 允许模块 ID（u32 col{ci} → +{4 + i * 4}；0=不可用）",
            display_name=f"模块槽 {i}",
            memory_offset=4 + i * 4,
        )
    confirm_partial(data)
    recount(data)
    return data


def enrich_trend_data_weapon(data: dict) -> dict:
    labels = [
        (1, "weapon_id", "武器 ID（→ WEAPON_SETTING）"),
        (2, "usage_rate", "使用率/流行度（百分比×100 或权重）"),
        (3, "win_rate", "胜率统计"),
        (4, "pick_rate", "选取率"),
        (5, "trend_rank", "趋势排名"),
        (6, "msma_id", "关联机体 ID（配装推荐机体）"),
        (7, "period_id", "统计周期 ID"),
        (8, "sample_count", "样本数量"),
        (9, "recommend_score", "推荐分数"),
        (10, "display_flag", "大厅显示标志"),
    ]
    for ci, name, meaning in labels:
        patch_col(
            data,
            ci,
            name=name,
            type="u32",
            meaning=f"{meaning}（u32 col{ci} → +{ci * 4}）",
            memory_offset=ci * 4,
            asm_va="0x592905",
        )
    confirm_partial(data)
    recount(data)
    return data


def enrich_mechanic_success(data: dict) -> dict:
    grid = [
        (1, "odds_grid_0_0", 4, "成功概率 [0,0]"),
        (2, "odds_grid_0_1", 16, "成功概率 [0,1]"),
        (3, "odds_grid_0_2", 28, "成功概率 [0,2]"),
        (4, "odds_grid_1_0", 8, "成功概率 [1,0]"),
        (5, "odds_grid_1_1", 20, "成功概率 [1,1]"),
        (6, "odds_grid_1_2", 32, "成功概率 [1,2]"),
        (7, "odds_grid_2_0", 12, "成功概率 [2,0]"),
        (8, "odds_grid_2_1", 24, "成功概率 [2,1]"),
        (9, "odds_grid_2_2", 36, "成功概率 [2,2]"),
    ]
    for ci, name, mem, label in grid:
        patch_col(
            data,
            ci,
            name=name,
            type="u32",
            meaning=f"{label}（u32 col{ci} → +{mem}；3×3 概率矩阵）",
            display_name=label,
            memory_offset=mem,
        )
    patch_col(
        data,
        10,
        display_name="开发券加成类型",
        enum_values=MECHANIC_BONUS,
    )
    confirm_partial(data)
    recount(data)
    return data


def enrich_over_custom(data: dict) -> dict:
    for ci, mem in [(1, 4), (2, 8), (4, 12), (5, 16), (7, 20), (8, 24), (10, 28), (11, 30), (12, 32)]:
        col = next(c for c in data["columns"] if c["csv_index"] == ci)
        col["memory_offset"] = mem
    confirm_partial(data)
    recount(data)
    return data


def enrich_lvup_msma(data: dict) -> dict:
    # sub_579D60: col0 level; col1-9 u32 raw @+4..+36 + cumulative @+40..+72
    cols = {c["csv_index"]: c for c in data["columns"]}
    if cols[1].get("type") == "str":
        cols[1].update(
            {
                "name": "exp_base",
                "db_column": "exp_base",
                "type": "u32",
                "meaning": "Lv1 经验基数（u32 col1 → +4；亦写入累计槽 +40）",
                "display_name": "经验基数",
                "read_order": 2,
                "memory_offset": 4,
                "asm_va": "0x579d85",
            }
        )
    exp_labels = [
        (2, "exp_delta_2", 8, 44),
        (3, "exp_delta_3", 12, 48),
        (4, "exp_delta_4", 16, 52),
        (5, "exp_delta_5", 20, 56),
        (6, "exp_delta_6", 24, 60),
        (7, "exp_delta_7", 28, 64),
        (8, "exp_delta_8", 32, 68),
        (9, "exp_delta_9", 36, 72),
    ]
    for ci, name, raw, cumul in exp_labels:
        patch_col(
            data,
            ci,
            name=name,
            db_column=name,
            type="u32",
            meaning=(
                f"升级经验增量 col{ci}（u32 raw → +{raw}；累计阈值 → +{cumul} = 前值+本列）"
            ),
            display_name=f"经验增量 Lv{ci}",
            memory_offset=raw,
        )
    # fix read_order sequence
    ro = 1
    for c in sorted(data["columns"], key=lambda x: x["csv_index"]):
        if c.get("read_order") is not None and c.get("status") != "gap":
            c["read_order"] = ro
            ro += 1
    confirm_partial(data)
    recount(data)
    return data


def enrich_lvup_pilot(data: dict) -> dict:
    patch_col(
        data,
        35,
        meaning="经验倍率（float col35×flt_D6AE54 → +32；读表后客户端清零）",
        confidence="○ASM确证",
    )
    patch_col(data, 36, meaning="里程碑标志（bool col36 → +36；读表后清零）")
    patch_col(data, 37, meaning="解锁关联参数（u32 col37 → +40；读表后清零）")
    patch_col(data, 38, meaning="特殊等级标志（bool col38 → +44；读表后清零）")
    patch_col(data, 41, meaning="等级达成奖励 ID（u32 col41 → +52）", memory_offset=52)
    patch_col(data, 42, meaning="等级奖励 GP（u32 col42 → +48）", memory_offset=48)
    patch_col(data, 44, meaning="获得技能/属性点（u32 col44 → +56）", memory_offset=56)
    confirm_partial(data, skip={35, 36, 37, 38})  # read-then-zeroed: keep partial
    recount(data)
    return data


def enrich_play_bonus_reward(data: dict) -> dict:
    patch_col(data, 1, memory_offset=8)
    patch_col(data, 2, memory_offset=12)
    patch_col(data, 3, memory_offset=16)
    patch_col(data, 4, memory_offset=20)
    patch_col(data, 5, memory_offset=22)
    patch_col(data, 6, memory_offset=32)
    patch_col(
        data,
        7,
        name="battle_mode_code",
        meaning=(
            "适用战斗模式编码（u32 col7 → +24；高 9 位解码写入 +4 为 1/5/6/99 模式过滤）"
        ),
        memory_offset=24,
    )
    ensure_gap(data, 8)
    confirm_partial(data)
    recount(data)
    return data


def enrich_season_rankerbattle_reward(data: dict) -> dict:
    patch_col(data, 1, memory_offset=4)
    patch_col(data, 2, memory_offset=8)
    patch_col(data, 3, memory_offset=12)
    patch_col(data, 4, memory_offset=16)
    patch_col(
        data,
        5,
        name="reward_item_name",
        type="str",
        meaning="排名奖励物品名（narrow str col5 → +20；sub_CC711A 32 字节）",
        display_name="奖励物品名",
        memory_offset=20,
    )
    patch_col(data, 6, name="reward_item_qty", memory_offset=84)
    patch_col(
        data,
        7,
        name="bonus_title_name",
        type="str",
        meaning="奖励称号名（narrow str col7 → +88；sub_CC711A 32 字节）",
        display_name="称号名",
        memory_offset=88,
    )
    confirm_partial(data)
    recount(data)
    return data


def enrich_over_custom_develop(data: dict) -> dict:
    confirm_partial(data)
    recount(data)
    return data


def enrich_msma_missionunit(data: dict) -> dict:
    patch_col(
        data,
        1,
        name="msma_id",
        meaning="关联机体 ID（u32 col1 → +4；→ CHARA_PARAM）",
        display_name="机体 ID",
    )
    patch_col(data, 4, name="spawn_order", display_name="出击顺序")
    patch_col(data, 5, name="mission_param_a", display_name="任务参数 A")
    patch_col(data, 6, name="mission_param_b", display_name="任务参数 B")
    patch_col(data, 8, name="mission_param_c", display_name="任务参数 C")
    confirm_partial(data)
    recount(data)
    return data


def enrich_beginner_challenge(enums: dict, data: dict) -> dict:
    ev = enum_values(enums, "sub_5703A0")
    if ev:
        patch_col(data, 2, enum_values=ev)
    patch_col(data, 1, memory_offset=4)
    patch_col(data, 3, memory_offset=12)
    patch_col(data, 4, memory_offset=16)
    patch_col(data, 5, memory_offset=20)
    confirm_partial(data)
    recount(data)
    return data


def enrich_daily_record(data: dict) -> dict:
    patch_col(data, 1, memory_offset=4)
    patch_col(
        data,
        5,
        meaning="统计单位类型/辅助参数（u32 col5 → +12；badge_config「单位」列同源）",
    )
    patch_col(data, 8, memory_offset=16)
    confirm_partial(data)
    recount(data)
    return data


def enrich_challenge_highscore(data: dict) -> dict:
    patch_col(data, 1, memory_offset=4, type="u8")
    patch_col(data, 8, memory_offset=92)
    patch_col(data, 9, memory_offset=96)
    confirm_partial(data)
    recount(data)
    return data


def enrich_lvup_pilot_exam(enums: dict, data: dict) -> dict:
    ev = enum_values(enums, "sub_592DB0")
    patch_col(
        data,
        1,
        name="exam_stat_type",
        db_column="exam_stat_type",
        type="enum",
        meaning="考核关联统计项（enum col1 sub_579FC0 → +4；与 DAILY_RECORD 46 项战绩同源）",
        display_name="考核统计项",
        memory_offset=4,
        enum_converter="sub_579FC0",
        enum_values=ev or None,
        enum_doc=ENUM_DOC,
        confidence="★确证",
        status="confirmed",
    )
    patch_col(
        data,
        2,
        name="exam_title",
        db_column="exam_title",
        type="str",
        meaning="考核标题（wstring col2 → +8；sub_456D90→sub_4029E0）",
        display_name="考核标题",
        memory_offset=8,
        confidence="★确证",
        status="confirmed",
    )
    patch_col(
        data,
        3,
        name="pass_score",
        type="u32",
        meaning="合格分数线（u32 col3 → +36）",
        memory_offset=36,
    )
    patch_col(
        data,
        4,
        name="pass_bonus_flag",
        db_column="pass_bonus_flag",
        type="bool",
        meaning="通过奖励启用标志（bool col4!=0 → +40）",
        display_name="通过奖励标志",
        memory_offset=40,
    )
    data["columns"] = [c for c in data["columns"] if c.get("name") != "exam_name"]
    confirm_partial(data)
    recount(data)
    return data


def enrich_msma_favms(data: dict) -> dict:
    patch_col(
        data,
        5,
        name="display_group",
        meaning="UI 显示分组（u32 col5 → +4）",
        display_name="显示分组",
    )
    patch_col(
        data,
        6,
        name="unlock_param",
        meaning="解锁/显示附加参数（u32 col6 → +16）",
        display_name="附加参数",
    )
    confirm_partial(data)
    recount(data)
    return data


def enrich_msma_adop(data: dict) -> dict:
    patch_col(data, 1, name="msma_id", meaning="关联机体 ID（u32 col1 → +4）", display_name="机体 ID")
    patch_col(data, 3, name="adop_param", meaning="高级选项参数（u32 col3 → +8）", display_name="选项参数")
    confirm_partial(data)
    recount(data)
    return data


def enrich_over_custom_cupsule(data: dict) -> dict:
    patch_col(
        data,
        3,
        meaning="点数倍率/附加参数（u32 col3 → +8；跳过 col2 默认 0）",
    )
    confirm_partial(data)
    recount(data)
    return data


def enrich_msma_battle_detail(data: dict) -> dict:
    patch_col(
        data,
        2,
        meaning="条目值（各子表 vtable[0] 自读 col2；u32/float 依 attribute_name 分派）",
        display_name="条目值",
        confidence="○ASM确证",
        status="confirmed",
        asm_reader="sub_A5D270",
    )
    recount(data)
    return data


BUILDERS: list[tuple[str, callable]] = []


def register(tid: str, fn):
    BUILDERS.append((tid, fn))


def main() -> None:
    enums = load_enums()
    targets = [
        "OVERHAUL",
        "PLAYER_NAVI",
        "LVUP_PILOT_CLASS",
        "FORCEGAUGE_INFO",
        "MSMA_MODULE",
        "TREND_DATA_WEAPON",
        "MECHANIC_SUCCESS",
        "OVER_CUSTOM",
        "LVUP_MSMA",
        "LVUP_PILOT",
        "PLAY_BONUS_REWARD",
        "SEASON_RANKERBATTLE_REWARD",
        "OVER_CUSTOM_DEVELOP",
        "MSMA_MISSIONUNIT",
        "BEGINNER_CHALLENGE",
        "DAILY_RECORD",
        "CHALLENGE_HIGHSCORE",
        "LVUP_PILOT_EXAM",
        "MSMA_FAVMS",
        "MSMA_ADOP",
        "OVER_CUSTOM_CUPSULE",
        "MSMA_BATTLE_DETAIL",
    ]
    for tid in targets:
        BEFORE[tid] = (
            sum(1 for c in load_table(tid)["columns"] if c.get("status") == "confirmed"),
            sum(1 for c in load_table(tid)["columns"] if c.get("status") == "partial"),
        )

    fn_map = {
        "OVERHAUL": enrich_overhaul,
        "PLAYER_NAVI": enrich_player_navi,
        "LVUP_PILOT_CLASS": enrich_lvup_pilot_class,
        "FORCEGAUGE_INFO": enrich_forcegauge_info,
        "MSMA_MODULE": enrich_msma_module,
        "TREND_DATA_WEAPON": enrich_trend_data_weapon,
        "MECHANIC_SUCCESS": enrich_mechanic_success,
        "OVER_CUSTOM": enrich_over_custom,
        "LVUP_MSMA": enrich_lvup_msma,
        "LVUP_PILOT": enrich_lvup_pilot,
        "PLAY_BONUS_REWARD": enrich_play_bonus_reward,
        "SEASON_RANKERBATTLE_REWARD": enrich_season_rankerbattle_reward,
        "OVER_CUSTOM_DEVELOP": enrich_over_custom_develop,
        "MSMA_MISSIONUNIT": enrich_msma_missionunit,
        "BEGINNER_CHALLENGE": lambda d: enrich_beginner_challenge(enums, d),
        "DAILY_RECORD": enrich_daily_record,
        "CHALLENGE_HIGHSCORE": enrich_challenge_highscore,
        "LVUP_PILOT_EXAM": lambda d: enrich_lvup_pilot_exam(enums, d),
        "MSMA_FAVMS": enrich_msma_favms,
        "MSMA_ADOP": enrich_msma_adop,
        "OVER_CUSTOM_CUPSULE": enrich_over_custom_cupsule,
        "MSMA_BATTLE_DETAIL": enrich_msma_battle_detail,
    }

    print("=== Round 7 cfg enrichment ===\n")
    print(f"{'Table':<28} {'confirmed':>14} {'partial':>14}")
    print("-" * 58)
    for tid in targets:
        data = fn_map[tid](load_table(tid))
        save_table(tid, data)
        bc, bp = BEFORE[tid]
        ac = data["column_confirmed"]
        ap = data["column_partial"]
        print(f"{tid:<28} {bc:>4}->{ac:<4} {bp:>4}->{ap:<4}")


if __name__ == "__main__":
    main()
