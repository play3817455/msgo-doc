#!/usr/bin/env python3
"""One-off batch: member, intro_info, hack_check composites."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"


def ws(cmd, struct, field, off, length, wtype, proto, section, reader, printer, eva="", notes=""):
    d = {
        "command": cmd,
        "struct": struct,
        "field_name": field,
        "offset": off,
        "length": length,
        "wire_type": wtype,
        "protocol_path": proto,
        "section": section,
        "reader": reader,
        "printer": printer,
    }
    if eva:
        d["evidence_va"] = eva
    if notes:
        d["notes"] = notes
    return d


def write_member():
    CMD = "SC-0x6B15-lounge-btlroom_member_detail_get_r"
    PROTO = "protocol_analysis/commands/SC-0x6B15-lounge-btlroom_member_detail_get_r/README.md"
    READER = "sub_B454D0"
    PRINTER = "sub_B4D9D0"
    leaders = json.loads((ROOT / "composites" / "leaders.json").read_text(encoding="utf-8"))

    alias = {
        "id": "member",
        "title": "房间成员 member（= leaders 52B）",
        "length": 52,
        "status": "complete",
        "layout_same_as": "leaders",
        "reader": READER,
        "printer": PRINTER,
        "memory_claim": 64,
        "wire_layout": leaders["wire_layout"],
        "evidence": {
            "commands": [CMD],
            "protocol_paths": [PROTO],
            "note": "6B15 members 数组元素；布局同 leaders（sub_B454D0/sub_B4D9D0）",
        },
        "members": [],
    }
    (ROOT / "composites" / "member.json").write_text(
        json.dumps(alias, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lp_ent = json.loads((ROOT / "entities" / "leaders.json").read_text(encoding="utf-8"))
    fields = [
        {k: f[k] for k in ("name", "offset", "length", "wire_type", "meaning", "disposition") if k in f}
        for f in lp_ent["fields"]
    ]
    for f in fields:
        if f.get("name") == "avatar":
            f["composite_ref"] = "avatar"

    ent = {
        "id": "member",
        "title": "member",
        "description": "房间成员明细元素；布局同 leaders 52B/64B（sub_B454D0/sub_B4D9D0）",
        "table_ref": "tbl_member",
        "disposition": "PERSIST",
        "wire_forms": [{
            "name": "btlroom_member_detail_get_r",
            "length": 52,
            "memory_claim": 64,
            "commands": [CMD],
            "protocol_path": PROTO,
            "reader": READER,
            "printer": PRINTER,
            "note": "数组元素；N≤51；offset 143",
        }],
        "fields": fields,
    }
    (ROOT / "entities" / "member.json").write_text(
        json.dumps(ent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (ROOT / "_legacy_tables" / "tbl_member.json").write_text(
        json.dumps({
            "id": "tbl_member",
            "title": "房间成员明细",
            "status": "complete",
            "table_disposition": "PERSIST",
            "purpose": "持久化 member 52B 元素；7 成员同 leaders（sub_B454D0/sub_B4D9D0）",
            "entity_ref": "member",
            "evidence_commands": [CMD],
            "column_groups": [{"name": "member（52B · 同 leaders）", "columns": ["member"]}],
            "columns": [{
                "name": "member",
                "disposition": "COMPOSITE",
                "composite_ref": "leaders",
                "meaning": "房间成员列表元素（日志 `members={`；52B 线 / 64B 槽；N≤51）",
                "wire_sources": [ws(
                    CMD, "member", "members", 143, 52, "array<struct,N>", PROTO, "§3",
                    READER, PRINTER, "B656FA|B4D9D0", "52·N 线长；槽步进 0x40=64",
                )],
            }],
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for m in leaders["members"]:
        wss = m.setdefault("wire_sources", [])
        if not any(w.get("command") == CMD for w in wss):
            wss.append(ws(
                CMD, "member", m["name"], m["offset"], m["length"], m["wire_type"],
                PROTO, "§3 / notes.md", READER, PRINTER, "B656FA|B4D9D0",
            ))
    leaders["evidence"]["commands"] = sorted(set(leaders["evidence"].get("commands", []) + [CMD]))
    leaders["evidence"]["protocol_paths"] = sorted(
        set(leaders["evidence"].get("protocol_paths", []) + [PROTO])
    )
    (ROOT / "composites" / "leaders.json").write_text(
        json.dumps(leaders, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_intro_info():
    CMD = "SC-0xA5FE-lounge-clan_introduction_set_r"
    PROTO = "protocol_analysis/commands/SC-0xA5FE-lounge-clan_introduction_set_r/README.md"
    READER = "sub_B46140"
    PRINTER = "sub_B4F080"
    spec = [
        ("active_time_bits", 0, 1, "u8", "活跃时段位图", "B46155|B4F0A9"),
        ("play_style", 1, 1, "u8", "游戏风格", "B46168|B4F0D1"),
        ("feature_word", 2, 112, "u8[112]", "特色词（4×28 字节）", "B46177|B4F0F3"),
        ("notice_body", 114, 433, "u8[433]", "公告正文", "B461AD|B4F156"),
    ]
    members = []
    for name, off, length, wtype, meaning, eva in spec:
        members.append({
            "name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "meaning": meaning,
            "disposition": "PERSIST",
            "wire_sources": [ws(
                CMD, "intro_info", name, off, length, wtype, PROTO, "§4.3",
                READER, PRINTER, eva,
            )],
        })

    comp = {
        "id": "intro_info",
        "title": "战队介绍 intro_info（547B）",
        "length": 547,
        "status": "complete",
        "reader": READER,
        "printer": PRINTER,
        "memory_claim": 547,
        "wire_layout": "u8 + u8 + 4×(28×u8) + 433×u8",
        "evidence": {
            "commands": [CMD],
            "protocol_paths": [PROTO],
            "note": "claim == 线长 == 547（sub_B411F0）",
        },
        "members": members,
    }
    (ROOT / "composites" / "intro_info.json").write_text(
        json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    fields = [
        {k: m[k] for k in ("name", "offset", "length", "wire_type", "meaning", "disposition")}
        for m in members
    ]
    ent = {
        "id": "intro_info",
        "title": "intro_info",
        "description": "战队介绍信息；547B；4 成员（sub_B46140/sub_B4F080）",
        "table_ref": "tbl_intro_info",
        "disposition": "PERSIST",
        "wire_forms": [{
            "name": "clan_introduction_set_r",
            "length": 547,
            "memory_claim": 547,
            "commands": [CMD],
            "protocol_path": PROTO,
            "reader": READER,
            "printer": PRINTER,
            "note": "报文字段 #2（offset 4）",
        }],
        "fields": fields,
    }
    (ROOT / "entities" / "intro_info.json").write_text(
        json.dumps(ent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (ROOT / "_legacy_tables" / "tbl_intro_info.json").write_text(
        json.dumps({
            "id": "tbl_intro_info",
            "title": "战队介绍",
            "status": "complete",
            "table_disposition": "PERSIST",
            "purpose": "持久化 intro_info 547B；4 成员（sub_B46140/sub_B4F080）",
            "entity_ref": "intro_info",
            "evidence_commands": [CMD],
            "column_groups": [{"name": "intro_info（547B · 4 成员）", "columns": ["intro_info"]}],
            "columns": [{
                "name": "intro_info",
                "disposition": "COMPOSITE",
                "composite_ref": "intro_info",
                "meaning": "战队介绍（日志 `intro_info=`；claim == 线长 == 547）",
                "wire_sources": [ws(
                    CMD, "intro_info", "intro_info", 4, 547, "struct", PROTO, "§3",
                    READER, PRINTER, "B708DE|B708ED|B4F080",
                )],
            }],
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_hack_check():
    CMD = "CS-0x421B-battle-pos_move"
    PROTO = "protocol_analysis/commands/CS-0x421B-battle-pos_move/README.md"
    WRITER = "sub_B065D0"
    PRINTER = "sub_B0B9E0"
    spec = [
        ("move_spd", 0, 2, "u16", "移动速度"),
        ("boost_gauge", 2, 2, "u16", "推进剂槽"),
        ("boost_recov", 4, 2, "u16", "推进恢复"),
        ("boost_consume", 6, 2, "u16", "推进消耗"),
        ("clcheck_result", 8, 1, "i8", "客户端校验结果"),
        ("weapon_itemid", 9, 4, "u32", "武器道具 ID"),
        ("weapon_cooltime", 13, 4, "u32", "武器冷却"),
        ("weapon_rapidtime", 17, 4, "u32", "武器连射时间"),
        ("weapon_reload", 21, 4, "u32", "武器装填"),
        ("debugger_found", 25, 1, "u8", "检测到调试器"),
        ("proc_ref_count", 26, 1, "u8", "进程引用计数"),
        ("reserved1", 27, 1, "u8", "保留字节 1"),
        ("reserved2", 28, 1, "u8", "保留字节 2"),
        ("weapon_bullet_speed", 29, 4, "f32", "弹速"),
        ("weapon_range", 33, 2, "u16", "射程"),
        ("weapon_charge_time", 35, 2, "u16", "蓄力时间"),
        ("weapon_bullet_mgz", 37, 2, "u16", "弹匣容量"),
        ("weapon_bullet_all", 39, 2, "u16", "总弹药"),
        ("weapon_batch_fire", 41, 2, "u16", "连射批次"),
        ("weapon_fired", 43, 4, "f32", "已发射弹量"),
        ("wrestle_size", 47, 2, "u16", "格斗尺寸"),
        ("wrestle_hack_check_ex", 49, 1, "u8", "格斗反作弊扩展"),
        ("fps", 50, 4, "f32", "帧率"),
        ("ai_num", 54, 1, "u8", "AI 数量"),
        ("perf_pre_chara", 55, 4, "f32", "性能：角色前"),
        ("perf_chara", 59, 4, "f32", "性能：角色"),
        ("perf_ai", 63, 4, "f32", "性能：AI"),
        ("perf_last", 67, 4, "f32", "性能：末段"),
        ("perf_if", 71, 4, "f32", "性能：接口"),
        ("perf_rdr", 75, 4, "f32", "性能：渲染"),
    ]
    members = []
    for name, off, length, wtype, meaning in spec:
        members.append({
            "name": name,
            "offset": off,
            "length": length,
            "wire_type": wtype,
            "meaning": meaning,
            "disposition": "EVENT",
            "wire_sources": [{
                **ws(
                    CMD, "hack_check", name, off, length, wtype, PROTO, "§3 / notes.md",
                    WRITER, PRINTER, "B3549C|B0B9E0",
                    "C→S 写线原语 sub_B065D0；槽 88 / 线 79",
                ),
                "writer": WRITER,
            }],
        })
        members[-1]["wire_sources"][0].pop("reader", None)

    comp = {
        "id": "hack_check",
        "title": "反作弊自检 hack_check（79B 线 / 88B 槽）",
        "length": 79,
        "status": "complete",
        "writer": WRITER,
        "printer": PRINTER,
        "memory_claim": 88,
        "wire_layout": "4×u16 + i8 + 4×u32 + 4×u8 + f32 + 5×u16 + f32 + u16 + u8 + 6×f32 + u8",
        "evidence": {
            "commands": [CMD],
            "protocol_paths": [PROTO],
            "note": "pos_move 尾部；29 成员名 sub_B0B9E0；线序按 sub_B065D0 写线展开",
        },
        "members": members,
    }
    (ROOT / "composites" / "hack_check.json").write_text(
        json.dumps(comp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    fields = [
        {k: m[k] for k in ("name", "offset", "length", "wire_type", "meaning", "disposition")}
        for m in members
    ]
    ent = {
        "id": "hack_check",
        "title": "hack_check",
        "description": "pos_move 反作弊自检块；79B 线 / 88B 槽；29 成员（sub_B065D0/sub_B0B9E0）",
        "table_ref": "tbl_hack_check",
        "disposition": "EVENT",
        "wire_forms": [{
            "name": "pos_move_hack_check",
            "length": 79,
            "memory_claim": 88,
            "commands": [CMD],
            "protocol_path": PROTO,
            "writer": WRITER,
            "printer": PRINTER,
            "note": "hack_check_count≤1；offset 49",
        }],
        "fields": fields,
    }
    (ROOT / "entities" / "hack_check.json").write_text(
        json.dumps(ent, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (ROOT / "_legacy_tables" / "tbl_hack_check.json").write_text(
        json.dumps({
            "id": "tbl_hack_check",
            "title": "反作弊自检",
            "status": "complete",
            "table_disposition": "EVENT",
            "purpose": "pos_move 反作弊自检 79B；29 成员（sub_B065D0/sub_B0B9E0）",
            "entity_ref": "hack_check",
            "evidence_commands": [CMD],
            "column_groups": [{"name": "hack_check（79B · 29 成员）", "columns": ["hack_check"]}],
            "columns": [{
                "name": "hack_check",
                "disposition": "COMPOSITE",
                "composite_ref": "hack_check",
                "meaning": "反作弊自检项（日志 `hack_check={`；79B 线 / 88B 槽）",
                "wire_sources": [ws(
                    CMD, "hack_check", "hack_check", 49, 79, "array<struct,1>", PROTO, "§3",
                    WRITER, PRINTER, "B3549C|B0B9E0", "hack_check_count≤1；槽步进 0x58=88",
                )],
            }],
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    write_member()
    write_intro_info()
    write_hack_check()
    print("ok")
