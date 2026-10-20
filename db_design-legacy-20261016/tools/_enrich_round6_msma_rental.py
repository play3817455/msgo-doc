#!/usr/bin/env python3
"""Round 6: MSMA_RENTAL cfg enrichment — sync CHARA_PARAM + rental-specific IDA."""

from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "db_design" / "schema" / "cfg" / "tables"
DATATABLES = ROOT / "datatables" / "01-列注释"

sys.path.insert(0, str(Path(__file__).parent))
from _enrich_msma_batch17 import gen_md_table, patch_col, recalc_stats  # noqa: E402

# cap_flag bit → (meaning_suffix, consumer, display_name)
CAP_FLAG_ENRICH = {
    16: (
        "能力位 +840 bit2（CSV→sub_582390；位图写入 +840，暂无独立 runtime test  xref）",
        None,
        "能力位 b840.2",
        "partial",
    ),
    17: ("能力位 +840 bit3", None, "能力位 b840.3", "partial"),
    18: ("能力位 +840 bit4（sub_477C10 机体能力门控 OR sub_67FEB0）", "sub_477C10", "能力位 b840.4", "confirmed"),
    19: ("能力位 +840 bit5", None, "能力位 b840.5", "partial"),
    20: ("能力位 +840 bit6", None, "能力位 b840.6", "partial"),
    21: ("能力位 +840 bit7", None, "能力位 b840.7", "partial"),
    22: ("能力位 +841 bit0", None, "能力位 b841.0", "partial"),
    24: ("能力位 +841 bit2", None, "能力位 b841.2", "partial"),
    25: (
        "能力位 +841 bit3（sub_48FF00 运行时状态位同步 +841 bit3）",
        "sub_48FF00",
        "能力位 b841.3",
        "confirmed",
    ),
    26: ("能力位 +841 bit4", None, "能力位 b841.4", "partial"),
    27: ("能力位 +841 bit5", None, "能力位 b841.5", "partial"),
    28: ("能力位 +841 bit6", None, "能力位 b841.6", "partial"),
    29: ("能力位 +841 bit7", None, "能力位 b841.7", "partial"),
    30: (
        "能力位 +842 bit0（deployable case10 推进补给门控 sub_4E7FF0→+842 bit0）",
        "sub_4E7FF0",
        "推进补给门控",
        "confirmed",
    ),
    31: ("能力位 +841 bit1（sub_7E7600 机库 UI 分支门控）", "sub_7E7600", "能力位 b841.1", "confirmed"),
    34: ("能力位 +842 bit3", None, "能力位 b842.3", "partial"),
}

# Short Chinese display names (shared with CHARA_PARAM where applicable)
DISPLAY = {
    0: "租借机体ID",
    1: "资源 ID 低32",
    2: "资源 ID 高32",
    3: "世代",
    4: "阶级",
    5: "名称",
    6: "说明",
    7: "战斗角色",
    8: "阵营",
    9: "宇宙适性",
    10: "水中适性",
    11: "地面适性",
    13: "变换备用武装",
    15: "近战连锁",
    35: "实体类别",
    36: "数值缩放A",
    37: "数值缩放B",
    38: "武器组ID",
    42: "关联表ID",
    44: "装备组合ID",
    48: "可部署类型",
    49: "系列分类",
    52: "喷射容量基值",
    56: "附加资源0",
    58: "附加资源1",
    60: "附加资源2",
    62: "附加资源3",
    64: "附加资源4",
    67: "附加资源5",
    69: "附加资源6",
    71: "附加资源7",
    73: "附加资源8",
    79: "附加资源9",
    83: "紧急返回基值",
    85: "搭载量基值",
    86: "喷射蓄力基值",
    87: "Flavor 文本",
    88: "列表分类ID",
    89: "最高速度基值",
    90: "装甲基值",
    91: "推进速度基值",
    46: "租借 GP 费用",
    47: "租借时长秒",
    32: "双模式标志",
}

GAP_MEANING = "CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图）"


def sync_from_chara(rental: dict, chara: dict) -> None:
    by_idx = {c["csv_index"]: c for c in chara["columns"]}
    for c in rental["columns"]:
        idx = c.get("csv_index")
        src = by_idx.get(idx)
        if not src:
            continue
        # Skip rental-only cols 46/47
        if idx in (46, 47):
            continue
        for k in (
            "name", "db_column", "meaning", "type", "memory_offset",
            "enum_converter", "enum_values", "enum_doc", "confidence",
            "status", "asm_va", "parse", "read_order",
        ):
            if src.get(k) is not None:
                c[k] = deepcopy(src[k])
        if src.get("display_name"):
            c["display_name"] = src["display_name"]
        elif src.get("meaning"):
            c["display_name"] = src["meaning"]


def apply_rental_specific(d: dict) -> None:
    patch_col(
        d, 0,
        meaning="租借机体ID（主键；同 CHARA_PARAM col0；机库「租用机体」列表键 sub_581200）",
        display_name="租借机体ID",
        status="confirmed",
        confidence="★确证",
    )
    patch_col(
        d, 46,
        name="rental_cost_gp",
        db_column="rental_cost_gp",
        meaning="租借 GP 费用（col46→+400；sub_582EC0 机库租用合并读 +400；对照 MODULE_RENTAL rental_cost_gp @+8）",
        display_name="租借 GP 费用",
        status="confirmed",
        confidence="★确证",
        memory_offset=400,
        asm_va="0x582849",
    )
    patch_col(
        d, 47,
        name="rental_duration_sec",
        db_column="rental_duration_sec",
        meaning="租借时长秒（col47→+404；sub_582EC0 读 +404 写回机体行；对照 MODULE_RENTAL duration_sec @+12）",
        display_name="租借时长秒",
        status="confirmed",
        confidence="★确证",
        memory_offset=404,
        asm_va="0x58285c",
    )


def apply_cap_flags(d: dict) -> None:
    for csv_idx, (meaning, consumer, display, status) in CAP_FLAG_ENRICH.items():
        kw = dict(meaning=meaning, status=status)
        if status == "confirmed":
            kw["confidence"] = "★确证"
        if consumer and consumer not in meaning:
            kw["meaning"] = f"{meaning.split('（')[0]}（{consumer}）"
        patch_col(d, csv_idx, **kw)
        for c in d["columns"]:
            if c.get("csv_index") == csv_idx:
                c["display_name"] = display
                break


def apply_display_names(d: dict) -> None:
    for c in d["columns"]:
        idx = c.get("csv_index")
        if idx in DISPLAY:
            c["display_name"] = DISPLAY[idx]
        if c.get("status") == "gap":
            c["meaning"] = GAP_MEANING
            c["display_name"] = f"保留列 col{idx}"


def battle_detail_key_meanings(d: dict) -> None:
    slots = [
        (56, 436, "RESPAWN_TIME"), (58, 464, "WARP_TIME"), (60, 492, "COST"),
        (62, 520, "MAX_HP"), (64, 548, "ENERGY"), (67, 576, "MOVE"),
        (69, 604, "BOOST_GAUGEMAX"), (71, 632, "BOOST_GAUGEHEAL"),
        (73, 660, "BOOST_SPEED"), (79, 688, "JUMP"),
    ]
    for csv_i, off, attr in slots:
        patch_col(
            d, csv_i,
            meaning=f"战力子表键 {attr}（col{csv_i}→+{off}；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等）",
            display_name=f"战力子表槽·{attr}",
            status="confirmed",
            confidence="★确证",
        )


def gen_md_with_gaps(data: dict) -> str:
    base = gen_md_table(data)
    gap_cols = [c for c in data["columns"] if c.get("status") == "gap"]
    if not gap_cols:
        return base
    lines = base.rstrip().splitlines()
    # Insert gap section before 填写规则
    insert_at = next(i for i, ln in enumerate(lines) if ln.startswith("**填写规则**"))
    gap_lines = [
        "",
        "## Gap 列（sub_582390 未读取；同 CHARA_PARAM）",
        "",
        "| CSV# | 订案名 | 说明 |",
        "|---|---|---|",
    ]
    for c in gap_cols:
        gap_lines.append(
            f"| `{c['csv_index']}` | `{c.get('name', c.get('db_column'))}` | {GAP_MEANING} |"
        )
    gap_lines.append("")
    return "\n".join(lines[:insert_at] + gap_lines + lines[insert_at:] + ["\n"])


def count_stats(data: dict) -> tuple[int, int, int]:
    cols = data["columns"]
    return (
        sum(1 for c in cols if c.get("status") == "confirmed"),
        sum(1 for c in cols if c.get("status") == "partial"),
        sum(1 for c in cols if c.get("status") == "gap"),
    )


def main() -> None:
    chara_path = TABLES / "CHARA_PARAM.json"
    rental_path = TABLES / "MSMA_RENTAL.json"
    chara = json.loads(chara_path.read_text(encoding="utf-8"))
    rental = json.loads(rental_path.read_text(encoding="utf-8"))
    before = count_stats(rental)

    rental["purpose"] = "机体租借参数（复用 CHARA_PARAM 读表 sub_582390，列布局相同；sub_582E90 加载）"
    rental["asm_reader"] = "sub_582390"
    rental["asm_status"] = "complete"

    sync_from_chara(rental, chara)
    apply_rental_specific(rental)
    apply_cap_flags(rental)
    battle_detail_key_meanings(rental)
    apply_display_names(rental)
    recalc_stats(rental)

    after = count_stats(rental)
    rental_path.write_text(json.dumps(rental, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md_path = ROOT / rental.get("source_md", "")
    if md_path.is_file():
        md_path.write_text(gen_md_with_gaps(rental), encoding="utf-8")

    print(f"MSMA_RENTAL confirmed: {before[0]} -> {after[0]}")
    print(f"MSMA_RENTAL partial:   {before[1]} -> {after[1]}")
    print(f"MSMA_RENTAL gap:       {before[2]} -> {after[2]}")


if __name__ == "__main__":
    main()
