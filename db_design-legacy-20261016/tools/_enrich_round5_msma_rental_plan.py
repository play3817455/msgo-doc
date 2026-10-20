#!/usr/bin/env python3
"""Round 5: MSMA_RENTAL + MSMA_PLAN cfg enrichment + MD sync."""

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
from _enrich_msma_batch17 import enrich_rental, gen_md_table, patch_col  # noqa: E402


def count_stats(data: dict) -> tuple[int, int, int]:
    cols = data.get("columns", [])
    conf = sum(1 for c in cols if c.get("status") == "confirmed")
    part = sum(1 for c in cols if c.get("status") == "partial")
    gap = sum(1 for c in cols if c.get("status") == "gap")
    return conf, part, gap


def apply_rental_overrides(d: dict) -> None:
    """MSMA_RENTAL-only semantics on top of CHARA_PARAM mirror."""
    patch_col(
        d,
        0,
        meaning="租借机体ID（主键；同 CHARA_PARAM col0；机库「租用机体」列表键）",
        display_name="租借机体ID",
    )
    # Rental GP cost / duration — same mem offsets as CHARA_PARAM col46/47 but rental UI semantics
    # sub_582390 col46→+400 / col47→+404; hangar rental pane reads MSMA_RENTAL row via dword_11E3F14
    patch_col(
        d,
        46,
        name="rental_cost_gp",
        db_column="rental_cost_gp",
        meaning="租借 GP 费用（col46→+400；MSMA_RENTAL 表语境；对照 MODULE_RENTAL rental_cost_gp @+8）",
        display_name="租借 GP 费用",
        status="partial",
        confidence="○ASM确证",
        memory_offset=400,
    )
    patch_col(
        d,
        47,
        name="rental_duration_sec",
        db_column="rental_duration_sec",
        meaning="租借时长秒（col47→+404；MSMA_RENTAL 表语境；对照 MODULE_RENTAL duration_sec @+12）",
        display_name="租借时长秒",
        status="partial",
        confidence="○ASM确证",
        memory_offset=404,
    )


def enrich_plan_r5(d: dict) -> None:
    """Name all 32 ASM-mapped cols from sub_594E20 / sub_5944D0 decompile."""
    d["asm_reader"] = "sub_594E20"
    d["asm_status"] = "complete"
    d["purpose"] = "机体图纸（开发计划；材料槽 qty/item_id 对；sub_5944D0 查 ITEM）"

    patch_col(
        d,
        0,
        name="plan_id",
        db_column="plan_id",
        meaning="图纸 ID（主键；col0→a3[0]；sub_594E20 @0x594e39）",
        display_name="图纸 ID",
        status="confirmed",
        confidence="★确证",
        memory_offset=0,
        asm_reader="sub_594E20",
        asm_va="0x594e39",
    )
    patch_col(
        d,
        2,
        name="plan_group_key",
        db_column="plan_group_key",
        meaning="图纸分组键（col2→a3[5]；sub_594D40 插入索引向量 @0x594e4a）",
        display_name="图纸分组键",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=20,
        asm_reader="sub_594E20",
        asm_va="0x594e4a",
    )
    patch_col(
        d,
        5,
        name="plan_sort_order",
        db_column="plan_sort_order",
        meaning="图纸排序/列表序（col5→a3[1]；sub_594E20 @0x594e9d）",
        display_name="图纸排序",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=4,
        asm_reader="sub_594E20",
        asm_va="0x594e9d",
    )
    patch_col(
        d,
        7,
        name="plan_header_a",
        db_column="plan_header_a",
        meaning="图纸头参数 A（col7→a3[2] @+8；sub_594E20 @0x594ebd）",
        display_name="图纸头参数 A",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=8,
        asm_reader="sub_594E20",
        asm_va="0x594ebd",
    )
    patch_col(
        d,
        9,
        name="plan_header_b",
        db_column="plan_header_b",
        meaning="图纸头参数 B（col9→a3[3] @+12；sub_594E20 @0x594ec8）",
        display_name="图纸头参数 B",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=12,
        asm_reader="sub_594E20",
        asm_va="0x594ec8",
    )
    patch_col(
        d,
        11,
        name="plan_header_c",
        db_column="plan_header_c",
        meaning="图纸头参数 C（col11→a3[4] @+16；sub_594E20 @0x594ed3）",
        display_name="图纸头参数 C",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=16,
        asm_reader="sub_594E20",
        asm_va="0x594ed3",
    )
    patch_col(
        d,
        13,
        name="output_item_id",
        db_column="output_item_id",
        meaning="产出物品 ID（col13→a3[14] @+56；sub_5944D0 查 ITEM @0x594ed6）",
        display_name="产出物品 ID",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=56,
        asm_reader="sub_594E20",
        asm_va="0x594ed6",
    )

    slots = [
        (15, 16, 60, 92, 0, "0x594f05", "0x594f08"),
        (18, 19, 96, 128, 1, "0x594f37", "0x594f3a"),
        (21, 22, 132, 172, 2, "0x594f6f", "0x594f75"),
        (24, 25, 168, 208, 3, "0x594faa", "0x594fb0"),
        (27, 28, 204, 244, 4, "0x594fe5", "0x594feb"),
        (30, 31, 240, 280, 5, "0x595020", "0x595026"),
        (33, 34, 276, 316, 6, "0x59505b", "0x595061"),
        (36, 37, 312, 352, 7, "0x595096", "0x59509c"),
        (39, 40, 348, 388, 8, "0x5950d1", "0x5950d7"),
        (42, 43, 384, 424, 9, "0x59510c", "0x595112"),
        (45, 46, 420, 460, 10, "0x595147", "0x59514d"),
        (48, 49, 456, 496, 11, "0x595182", "0x595188"),
    ]
    for qty_csv, item_csv, qty_off, item_off, n, qty_va, item_va in slots:
        patch_col(
            d,
            qty_csv,
            name=f"slot_{n}_qty",
            db_column=f"slot_{n}_qty",
            meaning=f"材料槽 {n} 数量（col{qty_csv}→+{qty_off}；sub_594E20）",
            display_name=f"材料槽{n}数量",
            status="confirmed",
            confidence="○ASM确证",
            memory_offset=qty_off,
            asm_reader="sub_594E20",
            asm_va=qty_va,
        )
        patch_col(
            d,
            item_csv,
            name=f"slot_{n}_item_id",
            db_column=f"slot_{n}_item_id",
            meaning=f"材料槽 {n} 物品ID（col{item_csv}→+{item_off}；sub_5944D0 查 ITEM）",
            display_name=f"材料槽{n}物品ID",
            status="confirmed",
            confidence="○ASM确证",
            memory_offset=item_off,
            asm_reader="sub_594E20",
            asm_va=item_va,
        )

    patch_col(
        d,
        51,
        name="plan_footer_param",
        db_column="plan_footer_param",
        meaning="图纸尾参数（col51→a3[123] @+492；sub_594E20 @0x5951b5）",
        display_name="图纸尾参数",
        status="confirmed",
        confidence="○ASM确证",
        memory_offset=492,
        asm_reader="sub_594E20",
        asm_va="0x5951b5",
    )


def collect_renames(before: dict[int, str], data: dict) -> list[str]:
    out: list[str] = []
    for c in data.get("columns", []):
        idx = c.get("csv_index")
        old = before.get(idx)
        new = c.get("db_column") or c.get("name")
        if old and new and old != new:
            out.append(f"{old}→{new}")
    return out


def main() -> None:
    summary = []
    for tid, fn in [
        ("MSMA_RENTAL", lambda d: (enrich_rental(d), apply_rental_overrides(d))),
        ("MSMA_PLAN", enrich_plan_r5),
    ]:
        path = TABLES / f"{tid}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        name_before = {c["csv_index"]: c.get("db_column", c.get("name", "")) for c in data["columns"]}
        before = count_stats(data)
        fn(data)
        conf, part, gap = count_stats(data)
        data["column_confirmed"] = conf
        data["column_partial"] = part
        data["column_gap"] = gap
        data["column_defined"] = len(data["columns"])
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        md_path = ROOT / data.get("source_md", "")
        if md_path.is_file():
            md_path.write_text(gen_md_table(data), encoding="utf-8")

        renames = collect_renames(name_before, data)
        summary.append((tid, before, (conf, part, gap), renames))

    print("TABLE\tCONF_BEFORE\tPART_BEFORE\tCONF_AFTER\tPART_AFTER\tKEY_RENAMES")
    for tid, before, after, renames in summary:
        rn = ", ".join(renames[:12])
        if len(renames) > 12:
            rn += f" (+{len(renames) - 12} more)"
        print(f"{tid}\t{before[0]}\t{before[1]}\t{after[0]}\t{after[1]}\t{rn}")


if __name__ == "__main__":
    main()
