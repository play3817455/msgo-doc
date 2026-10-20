#!/usr/bin/env python3
"""Build pilot composite — 159B wire / 176B slot from sub_B06360/sub_B06980/sub_B08AD0."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO_FD3E = "protocol_analysis/commands/CS-0xFD3E-lounge-pilot_create/README.md"
PROTO_C43C = "protocol_analysis/commands/SC-0xC43C-lounge-pilot_create_r/README.md"
PROTO_510F = "protocol_analysis/commands/SC-0x510F-lounge-party_member_add/README.md"
PROTO_BDD6 = "protocol_analysis/commands/SC-0xBDD6-battle-roomlobby_pilot_add/README.md"
CMD_FD3E = "CS-0xFD3E-lounge-pilot_create"
CMD_C43C = "SC-0xC43C-lounge-pilot_create_r"
CMD_510F = "SC-0x510F-lounge-party_member_add"
CMD_BDD6 = "SC-0xBDD6-battle-roomlobby_pilot_add"
WRITER = "sub_B06360"
READER = "sub_B06980"
PRINTER = "sub_B08AD0"
VA = "B8A18E|B08AD0|B06980"

# Wire offsets (decimal) from sub_B06360 sequential consume / FD3E §3.1
members_spec = [
    ("pilot_id", 0, 4, "u32", "驾驶员 ID", "PERSIST"),
    ("name", 4, 25, "char[25]", "驾驶员名（NUL 结尾，定长 25 槽）", "PERSIST"),
    ("troops", 29, 1, "i8", "所属阵营（0=秩序 / 1=抵抗）", "PERSIST"),
    ("level", 30, 1, "i8", "等级", "PERSIST"),
    ("mil_class", 31, 1, "i8", "军衔阶级", "PERSIST"),
    ("byword", 32, 2, "u16", "口头禅（byword 表 ID）", "PERSIST"),
    ("cmdr_fame", 34, 4, "u32", "指挥官功勋", "PERSIST"),
    ("rate_vslocal", 38, 2, "u16", "对本服胜率", "PERSIST"),
    ("rate_vslocal_4ev", 40, 2, "u16", "对本服胜率（4 人战）", "PERSIST"),
    ("rate_vslocal_clan", 42, 2, "u16", "对本服胜率（部队战）", "PERSIST"),
    ("level_point", 44, 4, "u32", "等级点数", "PERSIST"),
    ("avatar", 48, 18, "avatar(18B)", "外观（18B 子结构）", "PERSIST", "avatar"),
    ("clan_id", 66, 4, "u32", "所属部队 ID", "PERSIST"),
    ("clan_name", 70, 31, "char[31]", "部队名（NUL 结尾，定长 31 槽）", "PERSIST"),
    ("clan_emb_base", 101, 1, "i8", "部队徽章底图", "PERSIST"),
    ("clan_emb_parts1", 102, 1, "i8", "部队徽章部件 1", "PERSIST"),
    ("clan_emb_parts2", 103, 1, "i8", "部队徽章部件 2", "PERSIST"),
    ("cupteam_id", 104, 4, "u32", "杯赛队伍 ID", "PERSIST"),
    ("cupteam_name", 108, 31, "char[31]", "杯赛队伍名（NUL 结尾，定长 31 槽）", "PERSIST"),
    ("accum_point", 139, 4, "u32", "累计点数", "PERSIST"),
    ("rank", 143, 4, "u32", "名次/顺位", "PERSIST"),
    ("base_accump", 147, 4, "u32", "基础累计点", "PERSIST"),
    ("req_accump", 151, 4, "u32", "所需累计点", "PERSIST"),
    ("penalty", 155, 4, "u32", "惩罚值", "PERSIST"),
]


def ws(cmd, struct, field, offset, length, wtype, proto, section, reader=None, writer=None, printer=None, notes=None):
    d = {
        "command": cmd,
        "struct": struct,
        "field_name": field,
        "offset": offset,
        "length": length,
        "wire_type": wtype,
        "protocol_path": proto,
        "section": section,
        "evidence_va": VA,
    }
    if reader:
        d["reader"] = reader
    if writer:
        d["writer"] = writer
    if printer:
        d["printer"] = printer
    if notes:
        d["notes"] = notes
    return d


members = []
for item in members_spec:
    name, off, length, wtype, meaning, disp = item[:6]
    cref = item[6] if len(item) > 6 else None
    sources = [
        ws(CMD_FD3E, "pilot", name, off, length, wtype, PROTO_FD3E, "§3.1",
           writer=WRITER, printer=PRINTER, notes="C→S 写线；内存跨度 172B ≠ 线 159B"),
        ws(CMD_C43C, "pilot", name, off, length, wtype, PROTO_C43C, "§3",
           reader=READER, printer=PRINTER, notes="创建应答读线；槽 176B（sub_B05F00）"),
        ws(CMD_510F, "pilot", name, off, length, wtype, PROTO_510F, "§3",
           reader=READER, printer=PRINTER),
        ws(CMD_BDD6, "pilot", name, off, length, wtype, PROTO_BDD6, "§3",
           reader=READER, printer=PRINTER),
    ]
    m = {
        "name": name,
        "offset": off,
        "length": length,
        "wire_type": wtype,
        "meaning": meaning,
        "disposition": disp,
        "wire_sources": sources,
    }
    if cref:
        m["composite_ref"] = cref
    members.append(m)

assert members[-1]["offset"] + members[-1]["length"] == 159

comp = {
    "id": "pilot",
    "title": "机师 pilot（159B 线 / 176B 槽）",
    "length": 159,
    "status": "complete",
    "writer": WRITER,
    "reader": READER,
    "printer": PRINTER,
    "memory_claim": 176,
    "wire_layout": "4+25+1+1+1+2+4+2+2+2+4+18+4+31+1+1+1+4+31+4+4+4+4+4",
    "evidence": {
        "commands": [CMD_FD3E, CMD_C43C, CMD_510F, CMD_BDD6],
        "protocol_paths": [PROTO_FD3E, PROTO_C43C, PROTO_510F, PROTO_BDD6],
        "note": "23 成员名 sub_B08AD0；写线 sub_B06360 / 读线 sub_B06980；398B pilots_list 为另一 wire_form",
        "other_wire_forms": [
            {
                "name": "pilots_list",
                "length": 398,
                "memory_claim": 424,
                "reader": "sub_B42BB0",
                "printer": "sub_B48C10",
                "command": "SC-0xE13A-lounge-pilot_list_get_r",
                "protocol_path": "protocol_analysis/commands/SC-0xE13A-lounge-pilot_list_get_r/README.md",
            }
        ],
    },
    "members": members,
}
(ROOT / "composites" / "pilot.json").write_text(
    json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

# Sync entity fields (159B members only; keep slot/result/pilot_detail extras)
ent_path = ROOT / "entities" / "pilot.json"
entity = json.loads(ent_path.read_text(encoding="utf-8"))
core_names = {m["name"] for m in members}
extras = [f for f in entity.get("fields", []) if f["name"] not in core_names]
entity["fields"] = [
    {
        "name": m["name"],
        "offset": m["offset"],
        "length": m["length"],
        "wire_type": m["wire_type"],
        "meaning": m["meaning"],
        "disposition": m["disposition"],
        **({"composite_ref": m["composite_ref"]} if "composite_ref" in m else {}),
    }
    for m in members
] + extras
entity["wire_forms"][0]["memory_claim"] = 176
entity["wire_forms"][0]["reader"] = READER
entity["wire_forms"][0]["printer"] = PRINTER
ent_path.write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("OK pilot", len(members), "members 159B")
