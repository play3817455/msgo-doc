#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO = "protocol_analysis/commands/SC-0xA832-lounge-msma_add/README.md"
CMD = "SC-0xA832-lounge-msma_add"

members_spec = [
    ("db_index", 1, "u8", "数据库索引"),
    ("equip_wid", 4, "u32", "装备 wide ID"),
    ("adop_set", 8, "u16[4]", "采纳集合（4×u16）"),
]

off = 0
members = []
for name, length, wtype, meaning in members_spec:
    members.append({
        "name": name,
        "offset": off,
        "length": length,
        "wire_type": wtype,
        "meaning": meaning,
        "disposition": "PERSIST",
        "wire_sources": [{
            "command": CMD,
            "struct": "adop_list",
            "field_name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "protocol_path": PROTO,
            "section": "§3 / §4.3",
            "reader": "sub_B43D90",
            "printer": "sub_B4AC50",
        }],
    })
    off += length

assert off == 13

comp = {
    "id": "adop_list",
    "title": "采纳列表项 adop_list（13B 线 / 16B 槽）",
    "length": 13,
    "status": "complete",
    "reader": "sub_B43D90",
    "printer": "sub_B4AC50",
    "memory_claim": 16,
    "wire_layout": "1+4+4×2",
    "evidence": {
        "commands": [CMD],
        "protocol_paths": [PROTO],
        "note": "A832 adop_list 数组元素；上限 31 条",
    },
    "members": members,
}
(ROOT / "composites" / "adop_list.json").write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

entity = {
    "id": "adop_list",
    "title": "采纳列表项",
    "description": "机体采纳装备条目（13B 线长）",
    "table_ref": "tbl_adop_list",
    "disposition": "PERSIST",
    "wire_forms": [{"name": "adop_list", "length": 13, "memory_claim": 16, "commands": [CMD], "protocol_path": PROTO}],
    "fields": members,
}
(ROOT / "entities" / "adop_list.json").write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

table = {
    "id": "tbl_adop_list",
    "title": "采纳列表项",
    "status": "complete",
    "table_disposition": "PERSIST",
    "purpose": "持久化 adop_list 13B 线格式；3 成员（sub_B43D90/sub_B4AC50）；槽 16B",
    "entity_ref": "adop_list",
    "evidence_commands": [CMD],
    "column_groups": [{"name": "adop_list（13B · 3 成员）", "columns": ["adop_list"]}],
    "columns": [{
        "name": "adop_list",
        "disposition": "COMPOSITE",
        "composite_ref": "adop_list",
        "meaning": "采纳列表（元素线长 13 / 槽步进 16；上限 31 条）",
        "wire_sources": [{
            "command": CMD,
            "struct": "adop_list",
            "field_name": "adop_list",
            "offset": None,
            "length": 13,
            "wire_type": "array<struct,13>",
            "protocol_path": PROTO,
            "section": "§3",
            "reader": "sub_B43D90",
            "printer": "sub_B4AC50",
            "evidence_va": "0xB70E68",
            "notes": "变长数组，由 adop_num 驱动",
        }],
    }],
}
(ROOT / "_legacy_tables" / "tbl_adop_list.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(members), off)
