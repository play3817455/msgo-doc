#!/usr/bin/env python3
"""Repair MD column table rows from schema JSON."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TABLES = [
    "WEAPON_SETTING",
    "WEAPON_BATTLE_DETAIL",
    "WRESTLE_PARAM",
    "BULLET",
    "BUILDUP_WEAPON",
    "CHARA_PARAM",
    "CHARA_MODEL",
    "DAMAGE_FIELD_PARAM",
    "BUFF",
    "ACTION_MODULE_INFO",
    "AI_PARAM",
]


def cell_for(col: dict) -> str:
    disp = col.get("display_name") or col.get("name", "")
    meaning = col.get("meaning", disp)
    conf = col.get("confidence", "")
    star = "★" if "确证" in conf or col.get("status") == "confirmed" else ""
    if col.get("enum_converter") and col.get("type") == "enum":
        fn = col["enum_converter"]
        return f"{star}**{disp}**（`{fn}`）— {meaning[:140]}"
    if star:
        return f"★**{disp}** — {meaning[:140]}"
    if len(meaning) > 24:
        return f"{disp} — {meaning[:120]}"
    return meaning


def main() -> None:
    for tid in TABLES:
        data = json.loads(
            (ROOT / "db_design/schema/cfg/tables" / f"{tid}.json").read_text(encoding="utf-8")
        )
        md_path = ROOT / data["source_md"]
        if not md_path.is_file():
            md_path = ROOT / "datatables/01-列注释" / Path(data["source_md"]).name
        lines = md_path.read_text(encoding="utf-8").splitlines()
        col_by_csv = {c["csv_index"]: c for c in data["columns"]}
        out: list[str] = []
        for line in lines:
            if "`" in line and "|" in line:
                m = re.search(r"`(\d+)`", line)
                if m and re.search(r"^\|+\s*\d+\s*\|", line):
                    csv_idx = int(m.group(1))
                    col = col_by_csv.get(csv_idx)
                    if col:
                        ro = (col.get("read_order") or 1) - 1
                        ctype = col.get("type", "u32")
                        line = f"| {ro} | `{csv_idx}` | {ctype} | {cell_for(col)} |"
            out.append(line)
        md_path.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"fixed {md_path.name}")


if __name__ == "__main__":
    main()
