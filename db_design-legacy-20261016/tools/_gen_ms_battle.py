#!/usr/bin/env python3
"""Build ms composite — battle wire form 244B / slot 264B."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"
PROTO_1E2F = "protocol_analysis/commands/SC-0x1E2F-battle-msma_spawn_list_get_r_one/README.md"
PROTO_717D = "protocol_analysis/commands/SC-0x717D-battle-entity_msma_appear/README.md"
CMD = "SC-0x1E2F-battle-msma_spawn_list_get_r_one"

members_spec = [
    ("uniqid", 8, "u64", "机体唯一 ID"),
    ("msma_id", 4, "u32", "机体模板 ID"),
    ("crew_msma_id", 4, "u32", "乘员机体 ID"),
    ("decal", 4, "u32", "贴纸/标识"),
    ("color", 1, "u8", "配色"),
    ("deck_index", 1, "u8", "卡组索引"),
    ("cost", 4, "u32", " COST"),
    ("is_costover", 1, "u8", "是否超 COST"),
    ("energy_now", 4, "u32", "当前 EN"),
    ("weight_balance", 2, "u16", "重量平衡"),
    ("shield_weight", 2, "u16", "盾重"),
    ("sp_parts", 4, "u32", "特殊部件"),
    ("armor_up", 2, "u16", "装甲强化"),
    ("warp_up", 2, "u16", "传送强化"),
    ("boost_offset", 2, "u16", "推进偏移"),
    ("boost_offset_ns", 2, "u16", "推进偏移（无盾）"),
    ("over_custom_armor", 2, "u16", "超限自定义装甲"),
    ("over_custom_warp", 2, "u16", "超限自定义传送"),
    ("over_custom_level", 2, "u16", "超限自定义等级"),
    ("witem_id", 12, "u32[3]", "武器道具 ID（3）"),
    ("sitem_id", 4, "u32", "副武器道具 ID"),
    ("spitem_id", 4, "u32", "特殊道具 ID"),
    ("wbu_power", 6, "u16[3]", "武器 BU 威力（3）"),
    ("wbu_stability", 6, "u16[3]", "武器 BU 稳定性（3）"),
    ("wbu_rapid", 6, "u16[3]", "武器 BU 连射（3）"),
    ("wbu_shot_range", 6, "u16[3]", "武器 BU 射程（3）"),
    ("wbu_shield_hp", 6, "u16[3]", "武器 BU 盾 HP（3）"),
    ("wbu_eff_time", 6, "u16[3]", "武器 BU 有效时间（3）"),
    ("wbu_eff_range", 6, "u16[3]", "武器 BU 有效范围（3）"),
    ("eq_modules", 40, "u32[10]", "装备模块（10）"),
    ("eq_bonus_modules", 4, "u32", "装备奖励模块"),
    ("eq_rental_modules", 4, "u32", "装备租用模块"),
    ("adop_items_ms", 16, "u32[4]", "采纳项 MS（4）"),
    ("adop_items_eq", 48, "u32[12]", "采纳项装备（12）"),
    ("is_exdeck", 1, "u8", "是否扩展 deck"),
    ("is_rokaku", 1, "u8", "是否络格"),
    ("rokakums_limit_use", 4, "u32", "络格机体限制使用"),
    ("respawn_wait_sec", 2, "u16", "重生等待秒数"),
    ("respawn_wait_max", 2, "u16", "重生等待上限"),
    ("is_reduce_respawn_wait", 1, "u8", "是否缩短重生等待"),
    ("is_extrule_invalid", 1, "u8", "扩展规则无效标志"),
    ("is_heroms", 1, "u8", "是否英雄机体"),
    ("level_gauge_now_level", 4, "u32", "等级 gauge 当前等级"),
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
            "struct": "ms",
            "field_name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "protocol_path": PROTO_1E2F,
            "section": "§3",
            "reader": "sub_B06D80",
            "printer": "sub_B09240",
            "wire_form": "battle_244",
            "layout_ref": f"{PROTO_717D} notes.md",
        }],
    })
    off += length

assert off == 244

comp = {
    "id": "ms",
    "title": "机体 ms（244B 线 / 264B 槽 · battle）",
    "length": 244,
    "status": "complete",
    "reader": "sub_B06D80",
    "printer": "sub_B09240",
    "memory_claim": 264,
    "wire_layout": "717D notes: sub_B06D80=244",
    "evidence": {
        "commands": [CMD, "SC-0x717D-battle-entity_msma_appear", "SC-0x7621-battle-entity_msma_appear_self"],
        "protocol_paths": [PROTO_1E2F, PROTO_717D],
        "note": "battle 线形；lounge 299B（A832/sub_B43570/sub_B49DE0）为另一 wire_form，成员布局不同，勿交叉套用",
        "other_wire_forms": [{
            "name": "ms_lounge_299",
            "length": 299,
            "memory_claim": 312,
            "reader": "sub_B43570",
            "printer": "sub_B49DE0",
            "command": "SC-0xA832-lounge-msma_add",
            "protocol_path": "protocol_analysis/commands/SC-0xA832-lounge-msma_add/README.md",
        }],
    },
    "members": members,
}
(ROOT / "composites" / "ms.json").write_text(json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

entity = {
    "id": "ms",
    "title": "机体",
    "description": "MS 机体；battle 244B / lounge 299B 两种线形",
    "table_ref": "tbl_ms",
    "disposition": "EVENT",
    "wire_forms": [
        {"name": "battle", "length": 244, "memory_claim": 264, "commands": [CMD, "SC-0x717D-battle-entity_msma_appear"], "protocol_path": PROTO_717D},
        {"name": "lounge", "length": 299, "memory_claim": 312, "commands": ["SC-0xA832-lounge-msma_add"], "protocol_path": "protocol_analysis/commands/SC-0xA832-lounge-msma_add/README.md"},
    ],
    "fields": members,
}
(ROOT / "entities" / "ms.json").write_text(json.dumps(entity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

table = {
    "id": "tbl_ms",
    "title": "机体（battle 快照）",
    "status": "complete",
    "table_disposition": "EVENT",
    "purpose": "battle ms 244B 线格式；43 成员（sub_B06D80/sub_B09240）；槽 264B",
    "entity_ref": "ms",
    "evidence_commands": [CMD, "SC-0x717D-battle-entity_msma_appear", "SC-0x7621-battle-entity_msma_appear_self"],
    "column_groups": [{"name": "ms（244B · battle 线形）", "columns": ["ms"]}],
    "columns": [{
        "name": "ms",
        "disposition": "COMPOSITE",
        "composite_ref": "ms",
        "meaning": "机体状态结构（battle 244B 线长 / 264B 槽）",
        "wire_sources": [
            {"command": CMD, "struct": "ms", "field_name": "ms", "offset": 4, "length": 244, "wire_type": "struct<ms>",
             "protocol_path": PROTO_1E2F, "section": "§3", "reader": "sub_B06D80", "printer": "sub_B09240",
             "evidence_va": "0xB11DBA", "notes": "帧表 264 为槽跨度"},
            {"command": "SC-0x717D-battle-entity_msma_appear", "struct": "ms", "field_name": "ms", "offset": 9,
             "length": 244, "wire_type": "struct<ms>", "protocol_path": PROTO_717D, "section": "§3",
             "reader": "sub_B06D80", "evidence_va": "0xB1EBD9"},
        ],
    }],
}
(ROOT / "_legacy_tables" / "tbl_ms.json").write_text(json.dumps(table, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("OK", len(members), "members", off, "B")
