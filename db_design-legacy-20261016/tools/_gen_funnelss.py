#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO = "protocol_analysis/commands/SC-0x717D-battle-entity_msma_appear/README.md"
PROTO1B67 = "protocol_analysis/commands/SC-0x1B67-battle-funnel_snapshot_all/README.md"
CMD = "SC-0x717D-battle-entity_msma_appear"

members_spec = [
    ("ent_id", 4, "u32", "实体 ID"),
    ("wslot_idx", 1, "i8", "武器槽索引"),
    ("move_info", 5, "u8[5]", "移动/姿态信息（5B 定长）"),
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
        "disposition": "EVENT",
        "wire_sources": [{
            "command": CMD,
            "struct": "funnelss",
            "field_name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "protocol_path": PROTO,
            "section": "§3",
            "reader": "sub_B081C0",
            "printer": "sub_B0BF80",
            "layout_ref": f"{PROTO1B67} §3（snapshot_arr 元素互证）",
        }],
    })
    off += length

assert off == 10

comp = {
    "id": "funnelss",
    "title": "浮游炮子机 funnelss（10B 线 / 12B 槽）",
    "length": 10,
    "status": "complete",
    "reader": "sub_B081C0",
    "printer": "sub_B0BF80",
    "memory_claim": 12,
    "wire_layout": "4+1+5×u8",
    "evidence": {
        "commands": [CMD, "SC-0x7621-battle-entity_msma_appear_self", "SC-0x1B67-battle-funnel_snapshot_all"],
        "protocol_paths": [PROTO, PROTO1B67],
        "note": "与 1B67 snapshot_arr 元素同读器；717D 称 funnelss",
    },
    "members": members,
}
(ROOT / "composites" / "funnelss.json").write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

entity = {
    "id": "funnelss",
    "title": "浮游炮子机快照",
    "description": "funnel 快照元素（10B 线长）",
    "table_ref": "tbl_funnelss",
    "disposition": "EVENT",
    "wire_forms": [{
        "name": "funnelss",
        "length": 10,
        "memory_claim": 12,
        "commands": [CMD, "SC-0x7621-battle-entity_msma_appear_self", "SC-0x1B67-battle-funnel_snapshot_all"],
        "protocol_path": PROTO,
    }],
    "fields": members,
}
(ROOT / "entities" / "funnelss.json").write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

table = {
    "id": "tbl_funnelss",
    "title": "浮游炮子机快照",
    "status": "complete",
    "table_disposition": "EVENT",
    "purpose": "funnelss 10B 线格式；3 成员（sub_B081C0/sub_B0BF80）；槽 12B",
    "entity_ref": "funnelss",
    "evidence_commands": [CMD, "SC-0x7621-battle-entity_msma_appear_self"],
    "column_groups": [{"name": "funnelss（10B · 3 成员）", "columns": ["funnelss"]}],
    "columns": [{
        "name": "funnelss",
        "disposition": "COMPOSITE",
        "composite_ref": "funnelss",
        "meaning": "浮游炮子机（日志 `funnelss=`；claim 12 / 线长 10）",
        "wire_sources": [
            {"command": CMD, "struct": "funnelss", "field_name": "funnelss", "offset": 292, "length": 10,
             "wire_type": "struct<funnelss>", "protocol_path": PROTO, "section": "§3",
             "reader": "sub_B081C0", "printer": "sub_B0BF80", "evidence_va": "0xB1EC29"},
            {"command": "SC-0x7621-battle-entity_msma_appear_self", "struct": "funnelss", "field_name": "funnelss",
             "offset": 285, "length": 10, "wire_type": "struct<funnelss>",
             "protocol_path": "protocol_analysis/commands/SC-0x7621-battle-entity_msma_appear_self/README.md",
             "section": "§3", "reader": "sub_B081C0", "evidence_va": "0xB20136"},
        ],
    }],
}
(ROOT / "_legacy_tables" / "tbl_funnelss.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(members), off)
