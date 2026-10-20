#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO = "protocol_analysis/commands/SC-0xA832-lounge-msma_add/README.md"
CMD = "SC-0xA832-lounge-msma_add"

members_spec = [
    ("item_id", 4, "u32", "道具/武器 ID"),
    ("db_index", 2, "u16", "数据库索引"),
    ("buildup_cnt", 2, "u16", "强化次数"),
    ("buildup_val", 20, "u16[10]", "强化值（10×u16）"),
    ("spticket_success_wp", 1, "u8", "特殊票成功武器点"),
    ("spticket_greatest_wp", 1, "u8", "特殊票最大武器点"),
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
            "struct": "unlockw",
            "field_name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "protocol_path": PROTO,
            "section": "§3 / §4.3",
            "reader": "sub_B439D0",
            "printer": "sub_B4A580",
        }],
    })
    off += length

assert off == 30

comp = {
    "id": "unlockw",
    "title": "解锁武器 unlockw（30B 线 / 32B 槽）",
    "length": 30,
    "status": "complete",
    "reader": "sub_B439D0",
    "printer": "sub_B4A580",
    "memory_claim": 32,
    "wire_layout": "4+2+2+10×2+1+1",
    "evidence": {
        "commands": [CMD],
        "protocol_paths": [PROTO],
        "note": "A832 unlockw 数组元素；亦嵌于 sub_B43A80（48A4）",
    },
    "members": members,
}
(ROOT / "composites" / "unlockw.json").write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

entity = {
    "id": "unlockw",
    "title": "解锁武器",
    "description": "机体解锁武器条目（30B 线长）",
    "table_ref": "tbl_unlockw",
    "disposition": "PERSIST",
    "wire_forms": [{"name": "unlockw", "length": 30, "memory_claim": 32, "commands": [CMD], "protocol_path": PROTO}],
    "fields": members,
}
(ROOT / "entities" / "unlockw.json").write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

table = {
    "id": "tbl_unlockw",
    "title": "解锁武器",
    "status": "complete",
    "table_disposition": "PERSIST",
    "purpose": "持久化 unlockw 30B 线格式；6 成员（sub_B439D0/sub_B4A580）；槽 32B",
    "entity_ref": "unlockw",
    "evidence_commands": [CMD],
    "column_groups": [{"name": "unlockw（30B · 6 成员）", "columns": ["unlockw"]}],
    "columns": [{
        "name": "unlockw",
        "disposition": "COMPOSITE",
        "composite_ref": "unlockw",
        "meaning": "解锁武器列表元素（线长 30 / 槽步进 32；上限 30 条）",
        "wire_sources": [{
            "command": CMD,
            "struct": "unlockw",
            "field_name": "unlockw",
            "offset": None,
            "length": 30,
            "wire_type": "array<struct,30>",
            "protocol_path": PROTO,
            "section": "§3",
            "reader": "sub_B439D0",
            "printer": "sub_B4A580",
            "evidence_va": "0xB70D6B",
            "notes": "变长数组，由 unlockw_num 驱动",
        }],
    }],
}
(ROOT / "_legacy_tables" / "tbl_unlockw.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(members), off)
