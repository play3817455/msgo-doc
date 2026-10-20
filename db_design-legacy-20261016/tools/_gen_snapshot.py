#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO = "protocol_analysis/commands/SC-0x717D-battle-entity_msma_appear/README.md"
PROTO568 = "protocol_analysis/commands/SC-0x568A-battle-entity_snapshot/README.md"
CMD = "SC-0x717D-battle-entity_msma_appear"

members_spec = [
    ("ent_id", 2, "u16", "实体 ID"),
    ("pos_x", 2, "u16", "位置 X"),
    ("pos_y", 2, "u16", "位置 Y"),
    ("pos_z", 2, "u16", "位置 Z"),
    ("dir", 2, "u16", "朝向"),
    ("target_x", 2, "u16", "目标 X"),
    ("target_y", 2, "u16", "目标 Y"),
    ("target_z", 2, "u16", "目标 Z"),
    ("score1", 2, "u16", "得分 1"),
    ("score2", 2, "u16", "得分 2"),
    ("score3", 2, "u16", "得分 3"),
    ("hp_percent", 1, "u8", "HP 百分比"),
    ("hp_percent_shield", 1, "u8", "盾 HP 百分比"),
    ("down_power", 2, "u16", " DOWN 力量"),
    ("equip_index", 1, "u8", "装备索引"),
    ("water_index", 1, "u8", "水域索引"),
    ("layer_index", 1, "u8", "层索引"),
    ("rideon_ent_id", 2, "u16", "搭乘实体 ID"),
    ("lockon_ent_id", 2, "u16", "锁定实体 ID"),
    ("special_bits", 4, "u32", "特殊状态位"),
    ("special_bits2", 2, "u16", "特殊状态位 2"),
]

off = 0
members = []
for name, length, wtype, meaning in members_spec:
    members.append({
        "name": name,
        "offset": off,
        "length": length,
        "wire_type": wtype,
        "meaning": meaning.strip(),
        "disposition": "EVENT",
        "wire_sources": [{
            "command": CMD,
            "struct": "snapshot",
            "field_name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "protocol_path": PROTO,
            "section": "§3",
            "reader": "sub_B075A0",
            "printer": "sub_B0A260",
            "layout_ref": f"{PROTO568} notes.md",
        }],
    })
    off += length

assert off == 39

comp = {
    "id": "snapshot",
    "title": "实体快照 snapshot（39B 线 / 44B 槽）",
    "length": 39,
    "status": "complete",
    "reader": "sub_B075A0",
    "printer": "sub_B0A260",
    "memory_claim": 44,
    "wire_layout": "4×u16+7×u16+2×u8+u16+3×u8+2×u16+u32+u16",
    "evidence": {
        "commands": [CMD, "SC-0x7621-battle-entity_msma_appear_self", "SC-0x568A-battle-entity_snapshot"],
        "protocol_paths": [PROTO, PROTO568],
        "note": "21 成员 sub_B0A260；funnel 10B 线形（CS-7916/sub_B06850）为另一 wire_form",
        "other_wire_forms": [{
            "name": "funnel_snapshot_10",
            "length": 10,
            "command": "CS-0x7916-battle-funnel_snapshot_self",
            "protocol_path": "protocol_analysis/commands/CS-0x7916-battle-funnel_snapshot_self/README.md",
            "writer": "sub_B06850",
            "members": ["ent_id u32", "wslot_idx i8", "move_info u8[5]"],
        }],
    },
    "members": members,
}
(ROOT / "composites" / "snapshot.json").write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

entity = {
    "id": "snapshot",
    "title": "实体快照",
    "description": "对战实体位置/状态快照（39B 线长）",
    "table_ref": "tbl_snapshot",
    "disposition": "EVENT",
    "wire_forms": [{
        "name": "battle_entity",
        "length": 39,
        "memory_claim": 44,
        "commands": [CMD, "SC-0x7621-battle-entity_msma_appear_self", "SC-0x568A-battle-entity_snapshot"],
        "protocol_path": PROTO,
    }],
    "fields": members,
}
(ROOT / "entities" / "snapshot.json").write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

table = {
    "id": "tbl_snapshot",
    "title": "实体快照",
    "status": "complete",
    "table_disposition": "EVENT",
    "purpose": "battle snapshot 39B 线格式；21 成员（sub_B075A0/sub_B0A260）；槽 44B",
    "entity_ref": "snapshot",
    "evidence_commands": [CMD, "SC-0x7621-battle-entity_msma_appear_self"],
    "column_groups": [{"name": "snapshot（39B · 21 成员）", "columns": ["snapshot"]}],
    "columns": [{
        "name": "snapshot",
        "disposition": "COMPOSITE",
        "composite_ref": "snapshot",
        "meaning": "快照（日志 `snapshot=`；claim 44 / 线长 39）",
        "wire_sources": [
            {"command": CMD, "struct": "snapshot", "field_name": "snapshot", "offset": 253, "length": 39,
             "wire_type": "struct<snapshot>", "protocol_path": PROTO, "section": "§3",
             "reader": "sub_B075A0", "printer": "sub_B0A260", "evidence_va": "0xB1EC01"},
            {"command": "SC-0x7621-battle-entity_msma_appear_self", "struct": "snapshot", "field_name": "snapshot",
             "offset": 246, "length": 39, "wire_type": "struct<snapshot>",
             "protocol_path": "protocol_analysis/commands/SC-0x7621-battle-entity_msma_appear_self/README.md",
             "section": "§3", "reader": "sub_B075A0", "evidence_va": "0xB2010E"},
        ],
    }],
}
(ROOT / "_legacy_tables" / "tbl_snapshot.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(members), off)
