#!/usr/bin/env python3
"""一次性取证脚本（不进门禁）：把 B6 的 93 条 battle C→S 的线形事实抽出来。

只读 `protocol_analysis/commands/CS-*-battle-*/` 的 README §1/§2 与 `fields.csv`：
  opcode / 命令名 / 配对命令（README 里的「配对命令」行）/ 字段数与字段名序 / 声明容量。

输出 TSV，便于人工做「中转 / 权威 / 本地」三分类。
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CMDS = ROOT / "protocol_analysis" / "commands"


def one(dir_name: str) -> dict:
    d = CMDS / dir_name
    readme = (d / "README.md").read_text(encoding="utf-8")

    def grab(label: str) -> str:
        m = re.search(r"\|\s*" + label + r"\s*\|\s*([^|]*?)\s*\|", readme)
        return m.group(1).strip() if m else ""

    m = re.search(r"\|\s*配对命令[^|]*\|\s*([^|]*)\|", readme)
    pair = m.group(1).strip() if m else ""
    pairs = re.findall(r"`(SC-0x[0-9A-Fa-f]{4}-[a-z]+-[a-z0-9_]+)`", pair)

    fields = []
    fp = d / "fields.csv"
    if fp.exists():
        with fp.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                name = (row.get("字段名") or "").strip()
                if name and name != "opcode":
                    fields.append(name)
    return {
        "dir": dir_name,
        "opcode": grab("opcode"),
        "name": grab("命令名"),
        "pair_raw": pair,
        "pairs": pairs,
        "nfields": grab("字段数"),
        "fields": fields,
        "cap": grab("声明容量"),
        "summary": grab("结论"),
    }


def main() -> int:
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    dirs = sorted(p.name for p in CMDS.iterdir()
                  if p.is_dir() and re.match(r"cs-0x[0-9a-f]{4}-battle-", p.name.lower()))
    for dn in dirs:
        r = one(dn)
        if want and r["name"] != want:
            continue
        print("\t".join([
            r["opcode"], r["name"], r["nfields"], r["cap"],
            ",".join(r["pairs"]) or "-",
            "|".join(r["fields"]) or "-",
            r["summary"][:40],
        ]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
