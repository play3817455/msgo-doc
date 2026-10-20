#!/usr/bin/env python3
"""Bootstrap column enum_values from enums_ida registry."""

from __future__ import annotations

import json
from pathlib import Path

from cfg_enum_registry import build_registry
from build_cfg_site import load_cfg_tables, MULTI_CONTEXT_CONVERTERS

TABLES_DIR = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "tables"
SCHEMA_INLINE_MAX = 24  # 表详情 schema 内联上限；完整列表在 enums HTML


def main() -> None:
    _, tables = load_cfg_tables()
    registry = build_registry(tables)
    touched = 0
    for path in sorted(TABLES_DIR.glob("*.json")):
        tbl = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for c in tbl.get("columns", []):
            conv = c.get("enum_converter")
            if not conv or conv in MULTI_CONTEXT_CONVERTERS:
                continue
            if c.get("enum_values"):
                continue
            entry = registry.get(conv, {})
            if entry.get("kind", "enum") != "enum":
                continue
            vals = entry.get("values_list") or []
            if not vals:
                continue
            slice_vals = vals[:SCHEMA_INLINE_MAX]
            c["enum_values"] = [
                {"name": v["name"], "value": v.get("value")} for v in slice_vals
            ]
            changed = True
            touched += 1
        if changed:
            path.write_text(json.dumps(tbl, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added enum_values to {touched} columns")


if __name__ == "__main__":
    main()
