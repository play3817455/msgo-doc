#!/usr/bin/env python3
"""Round 7: MSMA_RENTAL — sync CHARA_PARAM Round 7 + keep rental-specific +400/+404 names."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "db_design" / "schema" / "cfg" / "tables"
DATATABLES = ROOT / "datatables" / "01-列注释"

sys.path.insert(0, str(Path(__file__).parent))
from _enrich_msma_batch17 import gen_md_table, patch_col, recalc_stats  # noqa: E402

GAP_MEANING = "CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图）"

DISPLAY = {
    0: "租借机体ID",
    46: "租借 GP 费用",
    47: "租借时长秒",
}


def sync_from_chara(rental: dict, chara: dict) -> None:
    by_idx = {c["csv_index"]: c for c in chara["columns"]}
    skip_rental_only = {46, 47}
    for c in rental["columns"]:
        idx = c.get("csv_index")
        if idx in skip_rental_only:
            continue
        src = by_idx.get(idx)
        if not src:
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
        meaning="租借时长秒（col47→+404；sub_582EC0 读 +404 写回机体行；sub_7DA460/sub_7D97E0；对照 MODULE_RENTAL duration_sec @+12）",
        display_name="租借时长秒",
        status="confirmed",
        confidence="★确证",
        memory_offset=404,
        asm_va="0x58285c",
    )


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

    sync_from_chara(rental, chara)
    apply_rental_specific(rental)
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


if __name__ == "__main__":
    main()
