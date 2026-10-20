#!/usr/bin/env python3
"""Scan protocol_analysis READMEs for documented struct members; emit manifest."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTO = ROOT / "protocol_analysis" / "commands"
OUT = Path(__file__).resolve().parents[1] / "schema" / "_meta" / "struct_manifest.json"

# Frame table row: | seq | off | len | type | `name` | ...
ROW_RE = re.compile(
    r"^\|\s*\d+\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*`?([^`|]+)`?\s*\|\s*([^|]+)\|",
    re.MULTILINE,
)
# §3.1 member: | 0x0 | 4 | u32 | `pilot_id` | meaning |
MEMBER_RE = re.compile(
    r"^\|\s*(0x[0-9A-Fa-f]+|\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+)\|\s*`([^`]+)`\s*\|\s*([^|]+)\|",
    re.MULTILINE,
)
# ### 3.2 `progress` 成员
SUBSECTION_HDR_RE = re.compile(r"^###\s*3\.\d+\s*`?([\w]+)`?\s*成员", re.MULTILINE)
# | 15.1 | +0 | 4 | u32 | `remain_msec` | meaning |
SUBSECTION_MEMBER_RE = re.compile(
    r"^\|\s*[\d.]+\s*\|\s*(\+0x[0-9A-Fa-f]+|\+\d+|0x[0-9A-Fa-f]+|\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+)\|\s*`([^`]+)`\s*\|\s*([^|]+)\|",
    re.MULTILINE,
)


def scan_command(readme: Path) -> list[dict]:
    text = readme.read_text(encoding="utf-8")
    cmd = readme.parent.name
    proto_path = f"protocol_analysis/commands/{cmd}/README.md"
    found = []

    in_31 = "§3.1" in text or "结构体成员" in text
    if in_31:
        for m in MEMBER_RE.finditer(text):
            off, length, wtype, name, meaning = m.groups()
            found.append(
                {
                    "command": cmd,
                    "struct": "_root",
                    "field_name": name.strip(),
                    "offset": off.strip(),
                    "length": int(length.strip()),
                    "wire_type": wtype.strip(),
                    "meaning": meaning.strip(),
                    "protocol_path": proto_path,
                    "section": "§3.1",
                }
            )

    for m in ROW_RE.finditer(text):
        off, length, wtype, name, meaning = m.groups()
        name = name.strip()
        if "." not in name:
            continue
        struct, field = name.split(".", 1)
        found.append(
            {
                "command": cmd,
                "struct": struct,
                "field_name": field,
                "offset_packet": off.strip(),
                "length": length.strip(),
                "wire_type": wtype.strip(),
                "meaning": meaning.strip(),
                "protocol_path": proto_path,
                "section": "§3",
            }
        )

    for hdr in SUBSECTION_HDR_RE.finditer(text):
        struct_name = hdr.group(1)
        section = hdr.group(0).split("`")[0].replace("###", "").strip()
        chunk = text[hdr.end() : hdr.end() + 8000]
        next_hdr = re.search(r"^###\s", chunk, re.MULTILINE)
        if next_hdr:
            chunk = chunk[: next_hdr.start()]
        for m in SUBSECTION_MEMBER_RE.finditer(chunk):
            off, length, wtype, name, meaning = m.groups()
            found.append(
                {
                    "command": cmd,
                    "struct": struct_name,
                    "field_name": name.strip(),
                    "offset": off.strip(),
                    "length": int(length.strip()),
                    "wire_type": wtype.strip(),
                    "meaning": meaning.strip(),
                    "protocol_path": proto_path,
                    "section": section,
                }
            )
    return found


def main() -> None:
    by_struct: dict[str, list] = defaultdict(list)
    for readme in sorted(PROTO.glob("*/README.md")):
        for row in scan_command(readme):
            key = row["struct"]
            by_struct[key].append(row)

    structs = []
    for name in sorted(by_struct.keys()):
        rows = by_struct[name]
        commands = sorted({r["command"] for r in rows})
        structs.append(
            {
                "struct": name,
                "member_rows": len(rows),
                "commands": commands,
                "fields": rows,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_from": "protocol_analysis/commands/*/README.md",
        "struct_count": len(structs),
        "structs": structs,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} ({len(structs)} struct groups)")


if __name__ == "__main__":
    main()
