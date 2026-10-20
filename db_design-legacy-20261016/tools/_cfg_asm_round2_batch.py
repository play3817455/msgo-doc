#!/usr/bin/env python3
"""CFG ASM Round 2 — finish OVER_CUSTOM, MODULE, MODULE_BONUS_LOT, MSMA_MISSIONUNIT, MSMA_COLORSET."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "db_design" / "schema" / "cfg" / "tables"
sys.path.insert(0, str(ROOT / "db_design" / "tools"))
from merge_cfg_asm import finalize_table  # noqa: E402

PARTIAL = {"status": "partial", "confidence": "△"}


def col(data: dict, idx: int) -> dict:
    for c in data["columns"]:
        if c["csv_index"] == idx:
            return c
    raise KeyError(idx)


def patch_over_custom() -> None:
    path = TABLES / "OVER_CUSTOM.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for idx in [2, 5, 7, 8, 10, 11, 12]:
        col(data, idx).update(PARTIAL)
    data = finalize_table(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OVER_CUSTOM: asm={data['asm_status']} pending={data['column_pending']} gap={data['column_gap']}")


def patch_module() -> None:
    path = TABLES / "MODULE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for idx in [2, 3, 4, 8]:
        col(data, idx).update(PARTIAL)
    col(data, 5).update(
        {
            **PARTIAL,
            "read_order": 5,
            "db_column": "param_5",
            "name": "param_u32_5",
            "display_name": "整型参数 col5",
            "meaning": "整型参数 col5",
            "memory_offset": 16,
            "asm_va": "0x5a2e00",
            "asm_reader": "sub_5A2DB0",
        }
    )
    c6 = col(data, 6)
    c6.clear()
    c6.update(
        {
            "read_order": None,
            "csv_index": 6,
            "db_column": "col6",
            "type": "u32",
            "meaning": "CSV 列存在但 IDA 读表未单独取证（默认 0）",
            "confidence": "",
            "status": "gap",
            "name": "reserved_u32_6",
            "display_name": "CSV 列存在但 IDA 读表未单独取证（默认 0）",
        }
    )
    data = finalize_table(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"MODULE: asm={data['asm_status']} pending={data['column_pending']} gap={data['column_gap']}")


def patch_module_bonus_lot() -> None:
    path = TABLES / "MODULE_BONUS_LOT.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for idx in [2, 5, 7, 8, 9]:
        col(data, idx).update(PARTIAL)
    data = finalize_table(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"MODULE_BONUS_LOT: asm={data['asm_status']} pending={data['column_pending']} gap={data['column_gap']}")


def patch_msma_missionunit() -> None:
    path = TABLES / "MSMA_MISSIONUNIT.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for idx in [1, 4, 5, 6, 8]:
        col(data, idx).update(PARTIAL)
    data = finalize_table(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"MSMA_MISSIONUNIT: asm={data['asm_status']} pending={data['column_pending']} gap={data['column_gap']}")


def patch_msma_colorset() -> None:
    path = TABLES / "MSMA_COLORSET.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for idx in [2, 4, 11, 16, 17, 20]:
        col(data, idx).update(PARTIAL)
    data = finalize_table(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"MSMA_COLORSET: asm={data['asm_status']} pending={data['column_pending']} gap={data['column_gap']}")


def main() -> None:
    patch_over_custom()
    patch_module()
    patch_module_bonus_lot()
    patch_msma_missionunit()
    patch_msma_colorset()


if __name__ == "__main__":
    main()
