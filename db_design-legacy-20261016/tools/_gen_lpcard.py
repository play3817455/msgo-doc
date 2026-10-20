#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO = "protocol_analysis/commands/SC-0x7051-lounge-clan_memberlist_get_r/README.md"
CMD = "SC-0x7051-lounge-clan_memberlist_get_r"

members_spec = [
    ("pilot_id", 4, "u32", "机师 ID"),
    ("name", 25, "char[25]", "名称"),
    ("last_in", 4, "u32", "最后登录时间"),
    ("troops", 1, "u8", "势力/阵营"),
    ("level", 1, "u8", "等级"),
    ("mil_class", 1, "u8", "军衔"),
    ("byword", 2, "u16", "座右铭 ID"),
    ("avatar", 18, "avatar", "外观（18B 子结构）", "avatar"),
    ("clan_id", 4, "u32", "战队 ID"),
    ("clan_name", 31, "char[31]", "战队名称"),
    ("clan_emb_base", 1, "u8", "战队徽章底"),
    ("clan_emb_parts1", 1, "u8", "战队徽章部件1"),
    ("clan_emb_parts2", 1, "u8", "战队徽章部件2"),
    ("clan_memb_exp", 4, "u32", "战队成员经验"),
    ("clan_memb_exp_use", 4, "u32", "战队成员经验使用量"),
    ("channel_id", 1, "u8", "频道 ID"),
    ("capture_bonus_state", 1, "u8", "占点加成状态"),
    ("capture_bonus_limit", 4, "u32", "占点加成上限"),
    ("rokaku_pt_use", 4, "u32", "络格点数使用"),
    ("state_bits", 1, "u8", "状态位"),
]

off = 0
members = []
for item in members_spec:
    name, length, wtype, meaning = item[:4]
    comp_ref = item[4] if len(item) > 4 else None
    m = {
        "name": name, "offset": off, "length": length, "wire_type": wtype,
        "meaning": meaning, "disposition": "PERSIST",
        "wire_sources": [{
            "command": CMD, "struct": "lpcard", "field_name": name,
            "offset": off, "length": length, "wire_type": wtype,
            "protocol_path": PROTO, "section": "§3 / notes.md",
            "reader": "sub_B43100", "printer": "sub_B49580",
        }],
    }
    if comp_ref:
        m["composite_ref"] = comp_ref
    members.append(m)
    off += length

comp = {
    "id": "lpcard", "title": "轻量成员卡片 lpcard（113B 线 / 132B 槽）",
    "length": 113, "status": "complete", "reader": "sub_B43100", "printer": "sub_B49580",
    "memory_claim": 132,
    "wire_layout": "4+25+4+1+1+1+2+18+4+31+1+1+1+4+4+1+1+4+4+1",
    "evidence": {
        "commands": [CMD, "SC-0x8E92-lounge-clan_info_get_self_r"],
        "protocol_paths": [PROTO, "protocol_analysis/commands/SC-0x8E92-lounge-clan_info_get_self_r/README.md"],
        "note": "20 成员名 sub_B49580；8E92 同读器称 member_info",
    },
    "members": members,
}
(ROOT / "composites" / "lpcard.json").write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

entity = {
    "id": "lpcard", "title": "轻量成员卡片",
    "description": "战队成员列表卡片（113B 线长）", "table_ref": "tbl_lpcard", "disposition": "PERSIST",
    "wire_forms": [{"name": "lpcard", "length": 113, "memory_claim": 132, "commands": [CMD], "protocol_path": PROTO}],
    "fields": members,
}
(ROOT / "entities" / "lpcard.json").write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

table = {
    "id": "tbl_lpcard", "title": "轻量成员卡片", "status": "complete", "table_disposition": "PERSIST",
    "purpose": "持久化 lpcard 113B 线格式；20 成员（sub_B43100/sub_B49580）；槽步进 132",
    "entity_ref": "lpcard", "evidence_commands": [CMD],
    "column_groups": [{"name": "lpcard（113B · 20 成员）", "columns": ["lpcard"]}],
    "columns": [{
        "name": "lpcard", "disposition": "COMPOSITE", "composite_ref": "lpcard",
        "meaning": "战队成员卡片列表元素（113B 线长 / 132B 槽；日志串 `lpcard={`）",
        "wire_sources": [{
            "command": CMD, "struct": "lpcard", "field_name": "lpcard", "offset": 8, "length": 113,
            "wire_type": "array<struct<lpcard>,N>", "protocol_path": PROTO, "section": "§3",
            "reader": "sub_B43100", "printer": "sub_B49580", "evidence_va": "0xB65FCD",
            "notes": "N≤50；槽步进 0x84=132",
        }],
    }],
}
(ROOT / "_legacy_tables" / "tbl_lpcard.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(members), off)
