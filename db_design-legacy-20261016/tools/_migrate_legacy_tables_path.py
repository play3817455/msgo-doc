#!/usr/bin/env python3
"""一次性搬迁脚本：把 game.* 旧表目录引用从 `schema/tables` 改到 `schema/_legacy_tables`。

P3 把 76 张旧提议表降级留档（不再驱动 DDL），目录同时改名为 `_legacy_tables/`。
只替换**路径表达式**里紧邻 schema 的那一层 `tables`，不碰：
  * `schema/cfg/tables`（主数据表，仍在用）
  * `relations.get("tables")` 这类 dict 键
  * 文档站点输出目录 `OUT_DIR / "tables"`
动作是幂等的：已经改过的文件不会二次改动。
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATTERNS = [
    (re.compile(r'(ROOT\s*/\s*"schema"\s*/\s*)"tables"'), r'\1"_legacy_tables"'),
    (re.compile(r'(SCHEMA\s*/\s*)"tables"'), r'\1"_legacy_tables"'),
    (re.compile(r'(SCHEMA_DIR\s*/\s*)"tables"'), r'\1"_legacy_tables"'),
    (re.compile(r'(ROOT\s*/\s*)"tables"\s*/\s*'), r'\1"_legacy_tables" / '),
    (re.compile(r'(schema_dir\s*/\s*)"tables"'), r'\1"_legacy_tables"'),
]

TARGETS = sorted((ROOT / "tools").glob("*.py")) + sorted(
    (ROOT.parent / "serverv" / "tools" / "schema_design").glob("*.py")
)


def main() -> None:
    changed = 0
    for path in TARGETS:
        if path.name == Path(__file__).name:
            continue
        text = path.read_text(encoding="utf-8")
        out = text
        for rx, repl in PATTERNS:
            out = rx.sub(repl, out)
        if out != text:
            path.write_text(out, encoding="utf-8")
            changed += 1
            print(f"updated {path.name}")
    print(f"{changed} 个文件已更新")


if __name__ == "__main__":
    main()
