#!/usr/bin/env python3
"""Enrich 17 MSMA/MECHANIC cfg tables to AI_WEAPON_PARAM quality."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "db_design" / "schema" / "cfg" / "tables"
MD_DIR = ROOT / "datatables" / "01-列注释"
ENUMS = json.loads((ROOT / "reverse-login-chain" / "formats" / "enums.json").read_text("utf-8"))
ENUM_DOC = "reverse-login-chain/formats/枚举表.md"

TABLE_IDS = [
    "MSMA_WEAPONSET", "MSMA_WEAPON_EQUIPCOMB", "MSMA_COLORSET", "MSMA_PLAN",
    "MSMA_MODULE", "MSMA_FORMATION", "MSMA_MISSIONUNIT", "MSMA_BATTLE_DETAIL",
    "MSMA_BREAKUP", "MSMA_RENTAL", "MSMA_MATERIAL", "MSMA_ADOP", "MSMA_FAVMS",
    "MSMA_FLIGHT_SET", "MECHANIC_MSMA", "MECHANIC_WEAPON", "MECHANIC_SUCCESS",
]

WEAPON_CATEGORY_ENUM = [
    {"name": n, "value": v}
    for n, v in [
        ("MACHINEGUN", 0), ("MACHINEGUN2", 1), ("MACHINEGUN3", 2), ("SUBMACHINEGUN", 3),
        ("SHOTGUN", 4), ("BEAM_RIFLE", 5), ("BEAM_SPRAYGUN", 6), ("WRESTLE", 7),
        ("CHARGE_RIFLE", 8), ("CHARGE_BAZOOKA", 9), ("SNIPER_RIFLE", 10), ("BEAM_SNIPE", 11),
        ("TRENCH_MORTAR", 12), ("REPAIR", 13), ("SHIELD", 14), ("BAZOOKA", 15),
        ("MISSILE", 16), ("HOWITZER", 17), ("LANDMINE", 18), ("HAND_THROW", 19),
        ("HAND_THROW2", 20), ("RADARPOD", 21), ("REPAIRPOD", 22), ("CAMERAGUN", 23),
        ("BULLET_PACK", 24), ("AAGPOD", 25), ("REPAIR_PACK", 26), ("-", 27),
    ]
]

SLOT_CATEGORY_ENUM = [
    {"name": "MAIN", "value": 0}, {"name": "EX", "value": 1}, {"name": "0", "value": 2},
]

VERDICT_ENUM = [
    {"name": "FIXED", "value": 0}, {"name": "CATEGORY_COMBINATION", "value": 1},
    {"name": "ID_COMBINATION", "value": 2}, {"name": "PERMIT_ID_COMBINATION", "value": 3},
    {"name": "REQUIRED_ID_COMBINATION", "value": 4},
]

MISSION_UNIT_ENUM = [
    {"name": "ATTACK", "value": 0}, {"name": "DEFENSE", "value": 1},
    {"name": "MOVE", "value": 2}, {"name": "SPECIAL", "value": 3},
]

BONUS_TYPE_ENUM = [
    {"name": n, "value": v}
    for n, v in [
        ("NONE", 0), ("FORCE_SUCCESS", 1), ("FORCE_GREATEST", 2),
        ("CAN_NOT_CREATE_MSMA", 3), ("CAN_NOT_NORMAL_PLAN", 4),
        ("BUILDUPWEAPON", 5), ("BUILDUPWEAPON_FGREATEST", 6),
    ]
]


def enum_from_fn(fn: str) -> list[dict] | None:
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


def patch_col(data: dict, csv_index: int, **kw) -> None:
    for c in data["columns"]:
        if c.get("csv_index") == csv_index:
            c.update({k: v for k, v in kw.items() if v is not None})
            if kw.get("meaning"):
                c["display_name"] = kw["meaning"]
            return
    raise KeyError(f"{data['id']} missing csv_index={csv_index}")


def recalc_stats(data: dict) -> None:
    cols = data.get("columns", [])
    data["column_defined"] = len(cols)
    data["column_count"] = data.get("column_count") or len(cols)
    data["column_confirmed"] = sum(1 for c in cols if c.get("status") == "confirmed")
    data["column_partial"] = sum(1 for c in cols if c.get("status") == "partial")
    data["column_gap"] = sum(1 for c in cols if c.get("status") == "gap")
    data["column_pending"] = sum(
        1 for c in cols if c.get("status") not in ("confirmed", "partial", "gap")
    )


def enrich_weaponset(d: dict) -> None:
    patch_col(d, 0, name="weapon_group_id", db_column="weapon_group_id",
              meaning="武器组ID（主键）；消费方 sub_581690 以机体+372 查组，最多收集 3 把启用武器",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 2, name="weapon_item_id", db_column="weapon_item_id",
              meaning="武器物品ID → ITEM 表（dword_11E3F08）；无效 ID 静默跳过",
              status="confirmed", confidence="★确证", memory_offset=4)
    patch_col(d, 4, name="slot_category", db_column="slot_category",
              meaning="槽位类别：MAIN 主武装 / EX 副武装（sub_586450）",
              status="confirmed", confidence="★确证", memory_offset=24,
              enum_converter="sub_586450", enum_values=SLOT_CATEGORY_ENUM, enum_doc=ENUM_DOC)
    patch_col(d, 5, name="weapon_category", db_column="weapon_category",
              meaning="武器类别（28 值，sub_585FD0）；写错名 ⇒ 0=MACHINEGUN",
              status="confirmed", confidence="★确证", memory_offset=8,
              enum_converter="sub_585FD0", enum_values=WEAPON_CATEGORY_ENUM, enum_doc=ENUM_DOC)
    patch_col(d, 6, name="enabled", db_column="enabled",
              meaning="启用开关（+20）；sub_581690 只收集为真的行到机体+376/+380/+384",
              status="confirmed", confidence="★确证", memory_offset=20, type="bool")
    patch_col(d, 7, name="sort_priority", db_column="sort_priority",
              meaning="排序/优先级 u32（+12）；消费方未确证 gameplay 用途",
              status="partial", confidence="△", memory_offset=12)
    # v39[i]=col8/12/16 (+28/+32/+36); v39[i+3]=col10/14/18; v39[i+6]=col11/15/19
    triples = [
        (8, 28, "a"), (12, 32, "a"), (16, 36, "a"),
        (10, 40, "b"), (14, 44, "b"), (18, 48, "b"),
        (11, 52, "c"), (15, 56, "c"), (19, 60, "c"),
    ]
    for csv_i, off, g in triples:
        patch_col(d, csv_i, name=f"value_group_{g}_{csv_i}", db_column=f"value_group_{g}_{csv_i}",
                  meaning=f"数值组 {g.upper()}（col{csv_i} → +{off}；三组循环写入 v39）",
                  status="partial", confidence="△", memory_offset=off)
    patch_col(d, 22, name="limit_trigger", db_column="limit_trigger",
              meaning="上限触发（+68）；>0 且 col24/25/26 全 ≤0 时 col26 强制 9999",
              status="confirmed", confidence="★确证（规则）", memory_offset=68)
    patch_col(d, 24, name="limit_param_a", db_column="limit_param_a",
              meaning="上限参数 A（+72）；参与 9999 联动判定",
              status="partial", confidence="△", memory_offset=72)
    patch_col(d, 25, name="limit_param_b", db_column="limit_param_b",
              meaning="上限参数 B（+76）；参与 9999 联动判定",
              status="partial", confidence="△", memory_offset=76)
    patch_col(d, 26, name="limit_cap", db_column="limit_cap",
              meaning="数量上限（+80）；col22>0 且 col24/25/26 全 ≤0 ⇒ 强制 9999",
              status="confirmed", confidence="★确证", memory_offset=80)
    patch_col(d, 27, name="extra_param", db_column="extra_param",
              meaning="附加 u32（+84）；语义未定",
              status="partial", confidence="△", memory_offset=84)
    patch_col(d, 28, name="region_gate", db_column="region_gate",
              meaning="地区开关：JAPAN 整行丢弃；CHINA/其他保留（strcmp @0x587359）",
              status="confirmed", confidence="★确证", type="str")


def enrich_equipcomb(d: dict) -> None:
    patch_col(d, 0, name="comb_id", meaning="组合规则ID（主键）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 2, name="verdict_type", meaning="裁定方式（sub_585580）：固定/类别组合/ID组合等",
              status="confirmed", confidence="★确证", memory_offset=0,
              enum_converter="sub_585580", enum_values=VERDICT_ENUM, enum_doc=ENUM_DOC)
    for lbl, idx, off in [("a", 3, 4), ("b", 4, 8), ("c", 5, 12)]:
        patch_col(d, idx, name=f"weapon_category_{lbl}", db_column=f"weapon_category_{lbl}",
                  meaning=f"武器类别 {lbl.upper()}（sub_585FD0，+{off}）",
                  status="confirmed", confidence="★确证", memory_offset=off,
                  enum_converter="sub_585FD0", enum_values=WEAPON_CATEGORY_ENUM, enum_doc=ENUM_DOC)
    patch_col(d, 6, name="rule_param_a", meaning="规则附加参数 A（+16）",
              status="partial", confidence="△", memory_offset=16)
    patch_col(d, 8, name="rule_param_b", meaning="规则附加参数 B（+20）",
              status="partial", confidence="△", memory_offset=20)
    patch_col(d, 10, name="region_gate",
              meaning="地区开关：CHINA 保留 / JAPAN 丢弃（sub_5854E0 @0x585b0c）",
              status="confirmed", confidence="★确证", type="str", enum_converter="sub_5854E0")


def enrich_colorset(d: dict) -> None:
    patch_col(d, 0, name="color_group_id", meaning="配色组ID（主键）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 2, name="color_entry_id", meaning="配色条目序号（+4 邻域）；与组ID配对",
              status="partial", confidence="△", memory_offset=4)
    patch_col(d, 3, name="name", meaning="配色名称（wstring，sub_456D90 @0x57d102）",
              status="confirmed", confidence="★确证", type="str")
    patch_col(d, 4, name="display_flag", meaning="显示/排序标志 u32（语义未定）",
              status="partial", confidence="△", memory_offset=8)
    patch_col(d, 5, name="price_a_trigger",
              meaning="A组买价/触发值（+20）；>0 且 col7≤0 ⇒ col7 强制 9999",
              status="confirmed", confidence="★确证（规则）", memory_offset=20)
    patch_col(d, 7, name="price_a_cap",
              meaning="A组库存/上限（+28）；col5>0 且本列≤0 ⇒ 9999",
              status="confirmed", confidence="★确证", memory_offset=28)
    patch_col(d, 8, name="price_b_trigger",
              meaning="B组买价/触发值（+32）；>0 且 col10≤0 ⇒ col10 强制 9999",
              status="confirmed", confidence="★确证（规则）", memory_offset=32)
    patch_col(d, 10, name="price_b_cap",
              meaning="B组库存/上限（+40）；col8>0 且本列≤0 ⇒ 9999",
              status="confirmed", confidence="★确证", memory_offset=40)
    patch_col(d, 11, name="color_param_11", meaning="附加参数 u32（+44）",
              status="partial", confidence="△", memory_offset=44)
    patch_col(d, 14, name="price_c_trigger",
              meaning="C组触发值（+56）；>0 且 col16/17/18 全≤0 ⇒ col18 强制 9999",
              status="confirmed", confidence="★确证（规则）", memory_offset=56)
    patch_col(d, 16, name="price_c_param_a", meaning="C组参数 A（+64）",
              status="partial", confidence="△", memory_offset=64)
    patch_col(d, 17, name="price_c_param_b", meaning="C组参数 B（+68）",
              status="partial", confidence="△", memory_offset=68)
    patch_col(d, 18, name="price_c_cap",
              meaning="C组上限（+72）；col14>0 且 col16/17/18 全≤0 ⇒ 9999",
              status="confirmed", confidence="★确证", memory_offset=72)
    patch_col(d, 19, name="vip_gate",
              meaning="VIP 会员等级门槛（sub_58B5A0 比对 NONE/VIP_ASSOCIATE…VIP_MASTER ⇒ 0..6；非地理区域）",
              status="confirmed", confidence="★确证", type="str", enum_converter="sub_58B5A0")
    patch_col(d, 20, name="extra_param_20", meaning="附加 u32（+76）",
              status="partial", confidence="△", memory_offset=76)


def enrich_plan(d: dict) -> None:
    patch_col(d, 0, name="plan_id", meaning="图纸 ID（主键；col0 → a3[0]）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 2, name="plan_group_key",
              meaning="图纸分组键（col2 → a3[5]）；sub_594D40 插入索引向量",
              status="partial", confidence="○ASM确证", memory_offset=20)
    for csv_i, off, lbl in [(7, 8, "header_a"), (9, 12, "header_b"), (11, 16, "header_c"), (13, 56, "header_d")]:
        patch_col(d, csv_i, name=f"plan_{lbl}", db_column=f"plan_{lbl}",
                  meaning=f"图纸头参数 {lbl}（col{csv_i} → +{off}）",
                  status="partial", confidence="○ASM确证", memory_offset=off)
    slots = [
        (15, 16, 60, 92, 0), (18, 19, 96, 128, 1), (21, 22, 132, 172, 2),
        (24, 25, 168, 208, 3), (27, 28, 204, 244, 4), (30, 31, 240, 280, 5),
        (33, 34, 276, 316, 6), (36, 37, 312, 352, 7), (39, 40, 348, 388, 8),
        (42, 43, 384, 424, 9), (45, 46, 420, 460, 10), (48, 49, 456, 496, 11),
    ]
    for qty_csv, item_csv, qty_off, item_off, n in slots:
        patch_col(d, qty_csv, name=f"slot_{n}_qty", db_column=f"slot_{n}_qty",
                  meaning=f"材料槽 {n} 数量（col{qty_csv} → +{qty_off}）",
                  status="partial", confidence="○ASM确证", memory_offset=qty_off)
        patch_col(d, item_csv, name=f"slot_{n}_item_id", db_column=f"slot_{n}_item_id",
                  meaning=f"材料槽 {n} 物品ID（col{item_csv} → +{item_off}；sub_5944D0 查 ITEM）",
                  status="partial", confidence="○ASM确证", memory_offset=item_off)
    patch_col(d, 51, name="plan_footer_param",
              meaning="图纸尾参数（col51 → a3[123]）",
              status="partial", confidence="○ASM确证", memory_offset=492)


def enrich_module(d: dict) -> None:
    patch_col(d, 0, name="msma_id", meaning="机体ID（主键；col0 → +0）",
              status="confirmed", confidence="★确证", memory_offset=0)
    for i, csv_i in enumerate(range(2, 22, 2)):
        patch_col(d, csv_i, name=f"module_slot_{i}", db_column=f"module_slot_{i}",
                  meaning=f"模块槽 {i} 允许模块ID（col{csv_i} → +{4*(i+1)}；0=不可用）",
                  status="partial", confidence="○ASM确证", memory_offset=4 * (i + 1))


def enrich_formation(d: dict) -> None:
    patch_col(d, 0, name="formation_id", meaning="NPC 编队ID（主键）",
              status="confirmed", confidence="★确证", memory_offset=0)
    for i in range(8):
        csv_a, csv_b = 2 + i * 2, 3 + i * 2
        off = 4 + i * 12
        patch_col(d, csv_a, name=f"slot_{i}_angle", db_column=f"slot_{i}_angle",
                  meaning=f"槽位{i} 角度输入（col{csv_a}×flt_D69A68 → sin/cos @+{off}）",
                  status="confirmed", confidence="★确证", memory_offset=off, type="float")
        patch_col(d, csv_b, name=f"slot_{i}_radius", db_column=f"slot_{i}_radius",
                  meaning=f"槽位{i} 半径/第三分量（col{csv_b} 直写 float @+{off+8}）",
                  status="confirmed", confidence="★确证", memory_offset=off + 8, type="float")


def enrich_missionunit(d: dict) -> None:
    patch_col(d, 0, name="unit_id", meaning="任务单位ID（主键）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 1, name="msma_ref", meaning="关联机体/单位引用 u32（+4）",
              status="partial", confidence="△", memory_offset=4)
    patch_col(d, 3, name="unit_role", meaning="单位职能（sub_57E1D0）：ATTACK/DEFENSE/MOVE/SPECIAL",
              status="confirmed", confidence="★确证", memory_offset=8, type="enum",
              enum_converter="sub_57E1D0", enum_values=MISSION_UNIT_ENUM, enum_doc=ENUM_DOC)
    patch_col(d, 4, name="spawn_order", meaning="出击顺序（+12）；读表时更新全局最小值 this[4]",
              status="partial", confidence="○ASM确证", memory_offset=12)
    patch_col(d, 5, name="param_5", meaning="任务参数 u32（+16）",
              status="partial", confidence="△", memory_offset=16)
    patch_col(d, 6, name="param_6", meaning="任务参数 u32（+20）",
              status="partial", confidence="△", memory_offset=20)
    patch_col(d, 8, name="param_8", meaning="任务参数 u32（+24）",
              status="partial", confidence="△", memory_offset=24)


def enrich_breakup(d: dict) -> None:
    patch_col(d, 0, name="breakup_id", meaning="拆解配置ID（主键；通常=机体ID）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 1, name="faction", meaning="阵营（sub_40CE20：ZEON 等；+4）",
              status="confirmed", confidence="★确证", memory_offset=4, type="enum",
              enum_converter="sub_40CE20", enum_doc=ENUM_DOC)
    patch_col(d, 2, name="battle_detail_ref",
              meaning="战斗明细引用（sub_5812E0 查 MSMA_BATTLE_DETAIL 子表指针；+8）",
              status="confirmed", confidence="★确证", memory_offset=8, type="enum",
              enum_converter="sub_5812E0", enum_doc=ENUM_DOC)
    patch_col(d, 3, name="breakup_type", meaning="拆解类型（sub_57BDE0；+12）",
              status="confirmed", confidence="★确证", memory_offset=12, type="enum",
              enum_converter="sub_57BDE0", enum_doc=ENUM_DOC)
    patch_col(d, 4, name="breakup_param_a", meaning="拆解参数 A（+16）",
              status="partial", confidence="△", memory_offset=16)
    patch_col(d, 6, name="breakup_param_b", meaning="拆解参数 B（+20；跳过 col5 空列）",
              status="partial", confidence="△", memory_offset=20)


def enrich_material(d: dict) -> None:
    patch_col(d, 0, name="material_id", meaning="素材类型ID（主键）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 2, name="material_type", meaning="素材类别（sub_594230 字符串→枚举；+4）",
              status="partial", confidence="○ASM确证", memory_offset=4, type="enum",
              enum_converter="sub_594230", enum_doc=ENUM_DOC)
    labels = ["base_rate", "tier2_rate", "tier3_rate", "tier4_rate", "tier5_rate", "tier6_rate"]
    for i, (csv_i, lbl) in enumerate(zip(range(3, 9), labels)):
        patch_col(d, csv_i, name=lbl, db_column=lbl,
                  meaning=f"开发成功率系数 {lbl}（col{csv_i} float → +{8+4*i}）",
                  status="partial", confidence="○ASM确证", memory_offset=8 + 4 * i, type="float")


def enrich_adop(d: dict) -> None:
    patch_col(d, 0, name="adop_id", meaning="高级选项ID（主键 u16；col0 → +0）",
              status="confirmed", confidence="★确证", memory_offset=0, type="u16")
    patch_col(d, 1, name="option_param_a", meaning="选项参数 A（+4）",
              status="partial", confidence="△", memory_offset=4)
    patch_col(d, 3, name="option_param_b", meaning="选项参数 B（+8；跳过 col2 空列）",
              status="partial", confidence="△", memory_offset=8)


def enrich_favms(d: dict) -> None:
    patch_col(d, 0, name="fav_id", meaning="喜爱条目ID（主键）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 3, name="msma_id", meaning="机体ID（col3 → +12；→ CHARA_PARAM 查机体）",
              status="confirmed", confidence="★确证", memory_offset=12)
    patch_col(d, 4, name="sort_order", meaning="列表排序权重（col4 → +8）",
              status="confirmed", confidence="★确证", memory_offset=8)
    patch_col(d, 5, name="fav_param_a", meaning="附加参数 A（col5 → +4）",
              status="partial", confidence="△", memory_offset=4)
    patch_col(d, 6, name="fav_param_b", meaning="附加参数 B（col6 → +16）",
              status="partial", confidence="△", memory_offset=16)


def enrich_mechanic_msma(d: dict) -> None:
    """sub_57A410: interleaved ×10 arrays a3[0..5] and a3[7..12]."""
    pairs = [
        (1, 0, 0), (2, 7, 28), (3, 1, 4), (4, 8, 32), (5, 2, 8), (6, 9, 36),
        (7, 3, 12), (8, 10, 40), (9, 4, 16), (10, 11, 44), (11, 5, 20), (12, 12, 48),
    ]
    for csv_i, a3_idx, off in pairs:
        is_cost = a3_idx < 7
        name = f"{'material_cost' if is_cost else 'success_rate'}_{a3_idx if is_cost else a3_idx - 7}"
        patch_col(d, csv_i, name=name, db_column=name,
                  meaning=f"{'素材消耗' if is_cost else '成功率'} col{csv_i}（×10 存 +{off}，a3[{a3_idx}]）",
                  status="confirmed", confidence="★确证（×10+布局）",
                  memory_offset=off, parse="x10")


def enrich_mechanic_weapon(d: dict) -> None:
    pairs = [
        (1, 0, 0), (2, 10, 40), (3, 1, 4), (4, 11, 44), (5, 2, 8), (6, 12, 48),
        (7, 3, 12), (8, 13, 52), (9, 4, 16), (10, 14, 56), (11, 5, 20), (12, 15, 60),
        (13, 6, 24), (14, 16, 64), (15, 7, 28), (16, 17, 68), (17, 8, 32), (18, 18, 72),
        (19, 9, 36), (20, 19, 76),
    ]
    for csv_i, a3_idx, off in pairs:
        is_cost = a3_idx < 10
        slot = a3_idx if is_cost else a3_idx - 10
        name = f"{'material_cost' if is_cost else 'success_rate'}_{slot}"
        patch_col(d, csv_i, name=name, db_column=name,
                  meaning=f"{'素材消耗' if is_cost else '成功率'} col{csv_i}（×10 存 +{off}，a3[{a3_idx}]）",
                  status="confirmed", confidence="★确证（×10+布局）",
                  memory_offset=off, parse="x10")


def enrich_mechanic_success(d: dict) -> None:
    patch_col(d, 0, name="odds_key", meaning="概率键（`INITIAL_ODDS`⇒0，否则 sub_CC6CA8）",
              status="confirmed", confidence="★确证", memory_offset=0, type="enum",
              enum_converter="sub_CC6CA8", enum_doc=ENUM_DOC)
    grid = [
        (1, 1, 4, "odds_grid_0_0"), (2, 4, 16, "odds_grid_0_1"), (3, 7, 28, "odds_grid_0_2"),
        (4, 2, 8, "odds_grid_1_0"), (5, 5, 20, "odds_grid_1_1"), (6, 8, 32, "odds_grid_1_2"),
        (7, 3, 12, "odds_grid_2_0"), (8, 6, 24, "odds_grid_2_1"), (9, 9, 36, "odds_grid_2_2"),
    ]
    for csv_i, a3_i, off, name in grid:
        patch_col(d, csv_i, name=name, db_column=name,
                  meaning=f"成功概率矩阵 col{csv_i}（a3[{a3_i}] → +{off}）",
                  status="partial", confidence="○ASM确证", memory_offset=off)
    patch_col(d, 10, name="bonus_type",
              meaning="开发券加成类型（sub_57A890：NONE/FORCE_SUCCESS/FORCE_GREATEST/…）",
              status="confirmed", confidence="★确证", memory_offset=40, type="enum",
              enum_converter="sub_57A890", enum_values=BONUS_TYPE_ENUM, enum_doc=ENUM_DOC)


def enrich_battle_detail(d: dict) -> None:
    patch_col(d, 0, name="attribute_name",
              meaning="属性名（sub_456D90→sub_57BD40 词表分派 13 张子表）",
              status="confirmed", confidence="★确证")
    patch_col(d, 1, name="entry_key",
              meaning="条目键（字符串；运行时写入机体对象 +436）",
              status="confirmed", confidence="★确证")
    patch_col(d, 2, name="entry_value",
              meaning="条目值（各子表 vtable[0] 自读；u32 或 float，依属性名而定）",
              status="partial", confidence="△")


def enrich_flight_set(d: dict) -> None:
    patch_col(d, 0, name="msma_id", meaning="机体ID（主键；col0 → +0）",
              status="confirmed", confidence="★确证", memory_offset=0)
    patch_col(d, 4, name="flight_flags_a", meaning="飞行标志/模式 A（u32 +44）",
              status="partial", confidence="○ASM确证", memory_offset=44)
    patch_col(d, 5, name="flight_flags_b", meaning="飞行标志/模式 B（u32 +48）",
              status="partial", confidence="○ASM确证", memory_offset=48)
    float_map = [
        (6, 4, "hover_base"), (7, 56, "hover_param_b"), (8, 60, "hover_param_c"),
        (9, 8, "boost_accel"), (10, 12, "boost_speed"), (11, 16, "boost_drain"),
        (12, 20, "gravity_scale"), (13, 32, "pitch_rate"), (14, 36, "yaw_rate"),
        (15, 40, "roll_rate"), (16, 24, "float_height"), (17, 28, "float_damp"),
        (18, 64, "transform_time"), (19, 68, "landing_speed"), (20, 72, "takeoff_speed"),
        (21, 76, "air_brake"), (22, 80, "stall_threshold"), (23, 84, "flight_param_23"),
        (26, 88, "funnel_param_a"), (27, 92, "funnel_param_b"),
        (28, 96, "funnel_param_c"), (29, 100, "funnel_param_d"),
    ]
    for csv_i, off, name in float_map:
        patch_col(d, csv_i, name=name, db_column=name,
                  meaning=f"飞行/浮游 float 参数（col{csv_i} → +{off}）",
                  status="partial", confidence="○ASM确证", memory_offset=off, type="float")
    patch_col(d, 24, name="flight_u32_24", meaning="飞行 u32 参数（+108）",
              status="partial", confidence="○ASM确证", memory_offset=108)
    patch_col(d, 25, name="flight_u32_25", meaning="飞行 u32 参数（+52）",
              status="partial", confidence="○ASM确证", memory_offset=52)
    patch_col(d, 30, name="flight_u32_30", meaning="飞行 u32 参数（+104）",
              status="partial", confidence="○ASM确证", memory_offset=104)


def enrich_rental(d: dict) -> None:
    """Mirror CHARA_PARAM column semantics (same reader sub_582390)."""
    chara = json.loads((TABLES / "CHARA_PARAM.json").read_text("utf-8"))
    by_idx = {c["csv_index"]: c for c in chara["columns"]}
    d["purpose"] = "机体租借参数（复用 CHARA_PARAM 读表 sub_582390，列布局相同）"
    for c in d["columns"]:
        src = by_idx.get(c.get("csv_index"))
        if not src:
            continue
        for k in ("name", "db_column", "meaning", "type", "memory_offset", "enum_converter",
                  "enum_values", "enum_doc", "confidence", "status", "asm_va", "parse"):
            if src.get(k) is not None:
                c[k] = deepcopy(src[k])
        if src.get("meaning"):
            c["display_name"] = src["meaning"]
        if c.get("name") == "msma_id":
            c["meaning"] = "租借机体ID（主键；同 CHARA_PARAM col0）"


ENRICHERS = {
    "MSMA_WEAPONSET": enrich_weaponset,
    "MSMA_WEAPON_EQUIPCOMB": enrich_equipcomb,
    "MSMA_COLORSET": enrich_colorset,
    "MSMA_PLAN": enrich_plan,
    "MSMA_MODULE": enrich_module,
    "MSMA_FORMATION": enrich_formation,
    "MSMA_MISSIONUNIT": enrich_missionunit,
    "MSMA_BATTLE_DETAIL": enrich_battle_detail,
    "MSMA_BREAKUP": enrich_breakup,
    "MSMA_MATERIAL": enrich_material,
    "MSMA_ADOP": enrich_adop,
    "MSMA_FAVMS": enrich_favms,
    "MSMA_FLIGHT_SET": enrich_flight_set,
    "MSMA_RENTAL": enrich_rental,
    "MECHANIC_MSMA": enrich_mechanic_msma,
    "MECHANIC_WEAPON": enrich_mechanic_weapon,
    "MECHANIC_SUCCESS": enrich_mechanic_success,
}


def gen_md_table(data: dict) -> str:
    lines = [
        f"# {data['id']} ｜ `{data.get('csv_path', '')}`",
        "",
        f"- **用途**：{data.get('purpose', '').lstrip('★**').rstrip('**')}",
        f"- 表ID `{data.get('table_id')}` ｜ 下载序 `{data.get('download_order')}` ｜ "
        f"类名 `{data.get('class_name', '')}` ｜ 逐列读取 `{data.get('asm_reader', '')}`",
        f"- 列数 {data.get('column_count', data.get('column_defined', '?'))} ｜ "
        f"确证 {data.get('column_confirmed', 0)} ｜ 部分 {data.get('column_partial', 0)} ｜ gap {data.get('column_gap', 0)}",
        "",
        "| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |",
        "|---|---|---|---|---|---|",
    ]
    ro = 0
    for c in data.get("columns", []):
        if c.get("status") == "gap":
            continue
        if c.get("read_order") is not None:
            ro = c["read_order"]
        elif c.get("read_order") is None and c.get("status") != "gap":
            ro += 1
        mem = c.get("memory_offset")
        mem_s = f"+{mem}" if mem is not None else "—"
        typ = c.get("type", "u32")
        if c.get("enum_converter"):
            typ = f"enum `{c['enum_converter']}`"
        meaning = c.get("meaning", "")
        meaning = re.sub(r"\s+", " ", meaning)[:120]
        lines.append(
            f"| {ro} | `{c.get('csv_index')}` | `{c.get('name', c.get('db_column'))}` | "
            f"{typ} | {mem_s} | {meaning} |"
        )
    lines.extend([
        "",
        "**填写规则**：",
        "- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。",
        "- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。",
        "- **越界列 = 0**：只需写到最大有效列号。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    summaries = []
    for tid in TABLE_IDS:
        path = TABLES / f"{tid}.json"
        if not path.is_file():
            summaries.append((tid, "missing", ""))
            continue
        data = json.loads(path.read_text("utf-8"))
        before_c = data.get("column_confirmed", 0)
        before_p = data.get("column_partial", 0)
        fn = ENRICHERS.get(tid)
        if fn:
            fn(data)
        recalc_stats(data)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        md_rel = data.get("source_md", "")
        if md_rel:
            md_path = ROOT / md_rel
            if not md_path.is_file():
                md_path = MD_DIR / Path(md_rel).name
            md_path.write_text(gen_md_table(data), encoding="utf-8")
        renames = [
            c["name"] for c in data["columns"]
            if c.get("status") != "gap" and not c["name"].startswith(("col", "unknown_", "param_u32", "reserved_"))
        ][:3]
        summaries.append((
            tid,
            f"{data['column_confirmed']}/{data['column_partial']}/{data['column_gap']}",
            f"Δconf +{data['column_confirmed']-before_c}; top: {', '.join(renames)}",
        ))

    print("=== per-table summary ===")
    for tid, counts, note in summaries:
        print(f"  {tid}: confirmed/partial/gap={counts} | {note}")


if __name__ == "__main__":
    main()
