#!/usr/bin/env python3
"""One-off generator for pilots_list composite (398B, 58 members)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"

members_spec = [
    ("pilot_id", 4, "u32", "机师 ID"),
    ("name", 25, "char[25]", "名称"),
    ("last_in", 4, "u32", "最后登录时间"),
    ("troops", 1, "u8", "势力/阵营"),
    ("level", 1, "u8", "等级"),
    ("mil_class", 1, "u8", "军衔"),
    ("byword", 2, "u16", "座右铭 ID"),
    ("avatar", 18, "avatar", "外观（18B 子结构）", "avatar"),
    ("cmdr_fame", 4, "u32", "指挥官声望"),
    ("rate_vslocal", 2, "u16", "本地对战胜率"),
    ("rate_vslocal_4ev", 2, "u16", "活动对战胜率"),
    ("rate_vslocal_clan", 2, "u16", "战队对战胜率"),
]
REC_MEANINGS = {
    "rec_vs": "对战场次", "rec_vs_win": "对战胜场", "rec_vs_lose": "对战败场",
    "rec_vsl_td": "对战塔防场次", "rec_vsl_td_win": "对战塔防胜场", "rec_vsl_td_lose": "对战塔防败场",
    "rec_xwar": "大规模战场次", "rec_xwar_win": "大规模战胜场", "rec_xwar_lose": "大规模战败场",
    "rec_xwar_last1": "上一场大规模战场次", "rec_xwar_win_last1": "上一场大规模战胜场",
    "rec_xwar_lose_last1": "上一场大规模战败场", "rec_xwar_win_term": "本届大规模战胜场",
    "rec_xwar_win_term_last1": "上届大规模战胜场", "rec_cmd": "指挥战场次", "rec_cmd_win": "指挥战胜场",
    "rec_cmd_lose": "指挥战败场", "rec_cmd_last1": "上一场指挥战场次", "rec_cmd_win_last1": "上一场指挥战胜场",
    "rec_cmd_lose_last1": "上一场指挥战败场", "rec_dc": "断线战场次", "rec_dc_win": "断线战胜场",
    "rec_dc_lose": "断线战败场", "score_assault_a": "评分·强袭 A", "score_assault_b": "评分·强袭 B",
    "score_snipe": "评分·狙击", "score_cannon": "评分·炮击", "score_support": "评分·支援",
}
for f, meaning in REC_MEANINGS.items():
    members_spec.append((f, 4, "u32", meaning))
members_spec += [
    ("comment", 116, "char[116]", "自我介绍/评论"),
    ("clan_id", 4, "u32", "战队 ID"),
    ("clan_name", 31, "char[31]", "战队名称"),
    ("clan_emb_base", 1, "u8", "战队徽章底"),
    ("clan_emb_parts1", 1, "u8", "战队徽章部件1"),
    ("clan_emb_parts2", 1, "u8", "战队徽章部件2"),
    ("clan_memb_exp", 4, "u32", "战队成员经验"),
    ("cupteam_id", 4, "u32", "杯赛队伍 ID"),
    ("cupteam_name", 31, "char[31]", "杯赛队伍名称"),
    ("channel_id", 1, "u8", "频道 ID"),
    ("state_bits", 1, "u8", "状态位"),
    ("accum_point", 4, "u32", "累计点数"),
    ("rank", 4, "u32", "排名"),
    ("base_accump", 4, "u32", "基础累计点"),
    ("req_accump", 4, "u32", "需求累计点"),
    ("level_point", 4, "u32", "等级点"),
    ("capture_bonus_state", 1, "u8", "占点加成状态"),
    ("capture_bonus_limit", 4, "u32", "占点加成上限"),
]

off = 0
members = []
for item in members_spec:
    name, length, wtype, meaning = item[:4]
    comp_ref = item[4] if len(item) > 4 else None
    m = {
        "name": name,
        "offset": off,
        "length": length,
        "wire_type": wtype,
        "meaning": meaning,
        "disposition": "PERSIST",
        "wire_sources": [{
            "command": "SC-0xE13A-lounge-pilot_list_get_r",
            "struct": "pilots_list",
            "field_name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "protocol_path": "protocol_analysis/commands/SC-0xE13A-lounge-pilot_list_get_r/README.md",
            "section": "§3",
            "reader": "sub_B42BB0",
            "printer": "sub_B48C10",
            "layout_ref": "protocol_analysis/commands/SC-0xB4B6-lounge-pilotcard_get_r/README.md §4.3",
        }],
    }
    if comp_ref:
        m["composite_ref"] = comp_ref
    members.append(m)
    off += length

assert off == 398

comp = {
    "id": "pilots_list",
    "title": "飞行员列表项 pilots_list（398B 线 / 424B 槽）",
    "length": 398,
    "status": "complete",
    "reader": "sub_B42BB0",
    "printer": "sub_B48C10",
    "memory_claim": 424,
    "wire_layout": "4+25+4+1+1+1+2+18+4+2+2+2+28×4+116+4+31+1+1+1+4+4+31+1+1+4×5+1+4",
    "evidence": {
        "commands": [
            "SC-0xE13A-lounge-pilot_list_get_r",
            "SC-0xB4B6-lounge-pilotcard_get_r",
        ],
        "protocol_paths": [
            "protocol_analysis/commands/SC-0xE13A-lounge-pilot_list_get_r/README.md",
            "protocol_analysis/commands/SC-0xB4B6-lounge-pilotcard_get_r/README.md",
        ],
        "note": "与 pcard 同读器 sub_B42BB0；58 成员名取自打印器 sub_B48C10；线长 398B 由 B4B6 §4.3 展开式确证",
    },
    "members": members,
}
(ROOT / "composites" / "pilots_list.json").write_text(
    json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

entity = {
    "id": "pilots_list",
    "title": "飞行员列表项",
    "description": "地球联邦/吉翁侧飞行员列表单条（398B 线长）；SC-0xE13A pilots_eff/pilots_zeon",
    "table_ref": "tbl_pilots_list",
    "disposition": "PERSIST",
    "wire_forms": [{
        "name": "pilots_list",
        "length": 398,
        "memory_claim": 424,
        "commands": ["SC-0xE13A-lounge-pilot_list_get_r"],
        "protocol_path": "protocol_analysis/commands/SC-0xE13A-lounge-pilot_list_get_r/README.md",
    }],
    "fields": members,
}
(ROOT / "entities" / "pilots_list.json").write_text(
    json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

table = {
    "id": "tbl_pilots_list",
    "title": "飞行员列表项",
    "status": "complete",
    "table_disposition": "PERSIST",
    "purpose": "持久化 pilots_list 398B 线格式；58 成员（sub_B42BB0/sub_B48C10）；槽步进 424",
    "entity_ref": "pilots_list",
    "evidence_commands": ["SC-0xE13A-lounge-pilot_list_get_r"],
    "column_groups": [
        {"name": "pilots_list（398B · 58 成员）", "columns": ["pilots_list"]},
    ],
    "columns": [{
        "name": "pilots_list",
        "disposition": "COMPOSITE",
        "composite_ref": "pilots_list",
        "meaning": "地球联邦/吉翁侧飞行员列表结构（固定 1 元；claim 0x1A8=424；打印器 sub_B48C10）",
        "wire_sources": [{
            "command": "SC-0xE13A-lounge-pilot_list_get_r",
            "struct": "pilots_list",
            "field_name": "pilots_eff",
            "offset": 4,
            "length": 398,
            "wire_type": "struct<pilots_list>",
            "protocol_path": "protocol_analysis/commands/SC-0xE13A-lounge-pilot_list_get_r/README.md",
            "section": "§3",
            "reader": "sub_B42BB0",
            "printer": "sub_B48C10",
            "evidence_va": "0xB82686",
            "notes": "pilots_zeon 同构 @402",
        }],
    }],
}
(ROOT / "_legacy_tables" / "tbl_pilots_list.json").write_text(
    json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"OK: {len(members)} members, {off}B")
