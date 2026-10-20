#!/usr/bin/env python3
"""Generate pcard composite from pilots_list layout (same sub_B42BB0/sub_B48C10)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO = "protocol_analysis/commands/SC-0xB4B6-lounge-pilotcard_get_r/README.md"
CMD = "SC-0xB4B6-lounge-pilotcard_get_r"

pilots = json.loads((ROOT / "composites" / "pilots_list.json").read_text(encoding="utf-8"))
members = []
for m in pilots["members"]:
    nm = dict(m)
    nm["wire_sources"] = [{
        "command": CMD,
        "struct": "pcard",
        "field_name": m["name"],
        "offset": m["offset"],
        "length": m["length"],
        "wire_type": m["wire_type"],
        "protocol_path": PROTO,
        "section": "§4.3",
        "reader": "sub_B42BB0",
        "printer": "sub_B48C10",
        "same_as": "pilots_list",
    }]
    members.append(nm)

comp = {
    "id": "pcard",
    "title": "驾驶员卡片 pcard（398B 线 / 424B 槽）",
    "length": 398,
    "status": "complete",
    "reader": "sub_B42BB0",
    "printer": "sub_B48C10",
    "memory_claim": 424,
    "wire_layout": pilots["wire_layout"],
    "evidence": {
        "commands": [CMD, "SC-0xE13A-lounge-pilot_list_get_r"],
        "protocol_paths": [
            PROTO,
            "protocol_analysis/commands/SC-0xE13A-lounge-pilot_list_get_r/README.md",
        ],
        "note": "与 pilots_list 同读器/打印器；58 成员名 sub_B48C10；线长 398B §4.3 展开式",
    },
    "members": members,
}
(ROOT / "composites" / "pcard.json").write_text(
    json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

entity = {
    "id": "pcard",
    "title": "驾驶员卡片",
    "description": "pilotcard_get_r 返回的驾驶员卡片（398B 线长）",
    "table_ref": "tbl_pcard",
    "disposition": "PERSIST",
    "wire_forms": [{
        "name": "pcard",
        "length": 398,
        "memory_claim": 424,
        "commands": [CMD],
        "protocol_path": PROTO,
    }],
    "fields": members,
}
(ROOT / "entities" / "pcard.json").write_text(
    json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

table = {
    "id": "tbl_pcard",
    "title": "驾驶员卡片",
    "status": "complete",
    "table_disposition": "PERSIST",
    "purpose": "持久化 pcard 398B 线格式；58 成员（sub_B42BB0/sub_B48C10）；槽步进 424",
    "entity_ref": "pcard",
    "evidence_commands": [CMD],
    "column_groups": [
        {"name": "pcard（398B · 58 成员）", "columns": ["pcard"]},
    ],
    "columns": [{
        "name": "pcard",
        "disposition": "COMPOSITE",
        "composite_ref": "pcard",
        "meaning": "驾驶员卡片数据块（跨度 424B；线长 398B；日志串 `pcard=`）",
        "wire_sources": [{
            "command": CMD,
            "struct": "pcard",
            "field_name": "pcard",
            "offset": 8,
            "length": 398,
            "wire_type": "struct<pcard>",
            "protocol_path": PROTO,
            "section": "§3",
            "reader": "sub_B42BB0",
            "printer": "sub_B48C10",
            "evidence_va": "0xB73FB0",
            "notes": "claim 0x1A8=424；线长 398",
        }],
    }],
}
(ROOT / "_legacy_tables" / "tbl_pcard.json").write_text(
    json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"OK: pcard {len(members)} members")
