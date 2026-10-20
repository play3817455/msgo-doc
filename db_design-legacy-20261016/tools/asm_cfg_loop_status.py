#!/usr/bin/env python3
"""Print cfg ASM loop progress; exit 0 when all 79 tables complete."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDX = ROOT / "db_design" / "schema" / "cfg" / "index.json"


def main() -> int:
    idx = json.loads(IDX.read_text(encoding="utf-8"))
    tables = idx["tables"]
    complete = [t for t in tables if t.get("asm_status") == "complete"]
    partial = [t for t in tables if t.get("asm_status") != "complete"]
    pending_cols = sum(t.get("column_pending", 0) for t in tables)
    print(f"tables: {len(complete)}/79 complete, {len(partial)} remaining, {pending_cols} pending columns")
    if partial:
        print("remaining:")
        for t in sorted(partial, key=lambda x: -x.get("column_pending", 0)):
            print(
                f"  {t['id']:32} pending={t.get('column_pending', 0):3} "
                f"gap={t.get('column_gap', 0):3} reader={t.get('reader_func', '')}"
            )
    return 0 if len(partial) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
