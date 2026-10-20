#!/usr/bin/env python3
"""Extract per-table IDA reader functions from datatables/01-列注释/*.md"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MD_DIR = ROOT / "datatables" / "01-列注释"
OUT = Path(__file__).resolve().parents[1] / "schema" / "cfg" / "_asm_manifest.json"

TITLE_RE = re.compile(r"^#\s+(\S+)\s+[｜|]")
READER_RE = re.compile(r"逐列读取(?:函数)?\s+`(sub_[0-9A-Fa-f]+)`")
READER_ALT_RE = re.compile(r"逐列读取\s+`(sub_[0-9A-Fa-f]+)`")
COL_COUNT_RE = re.compile(r"\*\*列数\s+(\d+)\*\*")
TABLE_ID_RE = re.compile(r"表ID\s+`(\d+)`")
CLASS_RE = re.compile(r"类名\s+`([^`]+)`")
GLOBAL_RE = re.compile(r"全局\s+`(dword_[0-9A-Fa-f]+)`")


def main() -> None:
    entries = []
    for md in sorted(MD_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        title = TITLE_RE.search(text)
        if not title:
            continue
        table = title.group(1).strip()
        reader = READER_RE.search(text) or READER_ALT_RE.search(text)
        col_m = COL_COUNT_RE.search(text)
        entries.append(
            {
                "id": table,
                "source_md": str(md.relative_to(ROOT)).replace("\\", "/"),
                "reader_func": reader.group(1) if reader else None,
                "column_count": int(col_m.group(1)) if col_m else None,
                "table_id": (TABLE_ID_RE.search(text) or [None])[0],
                "class_name": (CLASS_RE.search(text) or [None])[0],
                "global_var": (GLOBAL_RE.search(text) or [None])[0],
            }
        )
    OUT.write_text(json.dumps({"tables": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with_reader = sum(1 for e in entries if e["reader_func"])
    print(f"wrote {OUT} ({len(entries)} tables, {with_reader} with reader_func)")


if __name__ == "__main__":
    main()
