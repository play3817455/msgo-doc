#!/usr/bin/env python3
"""Restore 8 tables/entities lost to generate_all cleanup."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "schema"


def save(rel, obj):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def entity(comp_id, desc, disp, wf, fields=None, same_as=None):
    e = {
        "id": comp_id,
        "title": comp_id,
        "description": desc,
        "table_ref": f"tbl_{comp_id}",
        "disposition": disp,
        "wire_forms": wf,
        "fields": fields or [],
    }
    if same_as:
        e["layout_same_as"] = same_as
    return e


def tbl(tid, title, purpose, disp, entity_ref, group, col, cref, meaning, ws, cmds):
    return {
        "id": tid,
        "title": title,
        "status": "complete",
        "table_disposition": disp,
        "purpose": purpose,
        "entity_ref": entity_ref,
        "evidence_commands": cmds,
        "column_groups": [{"name": group, "columns": [col]}],
        "columns": [{
            "name": col,
            "disposition": "COMPOSITE",
            "composite_ref": cref,
            "meaning": meaning,
            "wire_sources": ws,
        }],
    }


# appear_info
CMD057A = "SC-0x057A-battle-entity_deploy_arms_appear"
P057A = "protocol_analysis/commands/SC-0x057A-battle-entity_deploy_arms_appear/README.md"
save("tables/tbl_appear_info.json", tbl(
    "tbl_appear_info", "部署武装出现", "EVENT appear_info 86B 线；17 成员含 snapshot 嵌套",
    "EVENT", "appear_info", "appear_info（86B · 17 成员）", "appear_info", "appear_info",
    "部署武装出现信息（日志 appear_info=；claim 96 / 线 86）",
    [{"command": CMD057A, "struct": "appear_info", "field_name": "appear_info", "offset": 0, "length": 86,
      "wire_type": "struct", "protocol_path": P057A, "section": "§3", "reader": "sub_B07EC0", "printer": "sub_B0B4B0",
      "evidence_va": "B07ED3|B0B743", "notes": "报文唯一字段；成员见 composite appear_info"}],
    [CMD057A],
))
comp = json.loads((ROOT / "composites/appear_info.json").read_text(encoding="utf-8"))
save("entities/appear_info.json", entity("appear_info", "部署武装出现；86B/96B；17 成员", "EVENT",
    [{"name": "deploy_arms", "length": 86, "memory_claim": 96, "commands": [CMD057A], "protocol_path": P057A,
      "reader": "sub_B07EC0", "printer": "sub_B0B4B0"}],
    [{"name": m["name"], "offset": m["offset"], "length": m["length"], "wire_type": m["wire_type"],
      "meaning": m["meaning"], "disposition": m["disposition"]} for m in comp["members"]]))

# avatar
save("tables/tbl_avatar.json", tbl(
    "tbl_avatar", "飞行员外观", "PERSIST avatar 18B；10 成员（sub_B068B0/sub_B08920）",
    "PERSIST", "avatar", "avatar（18B · 10 成员）", "avatar", "avatar",
    "飞行员外观部件（FD3E 创建 / 43F2 编辑 / E536 应答）",
    [{"command": "CS-0xFD3E-lounge-pilot_create", "struct": "avatar", "field_name": "avatar", "offset": None,
      "length": 18, "wire_type": "struct", "protocol_path": "protocol_analysis/commands/CS-0xFD3E-lounge-pilot_create/README.md",
      "section": "§3", "writer": "sub_B06290", "printer": "sub_B08920", "evidence_va": "B92F0A|B08920",
      "notes": "创建写线；编辑见 CS-43F2 / SC-E536"}],
    ["CS-0xFD3E-lounge-pilot_create", "CS-0x43F2-lounge-pilot_avatar_edit", "SC-0xE536-lounge-pilot_avatar_edit_r"],
))
av = json.loads((ROOT / "composites/avatar.json").read_text(encoding="utf-8"))
save("entities/avatar.json", entity("avatar", "飞行员外观 avatar；18B；10 成员", "PERSIST",
    [{"name": "avatar", "length": 18, "commands": av["evidence"]["commands"], "protocol_path": av["evidence"]["protocol_paths"][0]}],
    [{"name": m["name"], "offset": m["offset"], "length": m["length"], "wire_type": m["wire_type"],
      "meaning": m["meaning"], "disposition": m["disposition"]} for m in av["members"]]))

# dailycup_conf + next
CMD44C1 = "SC-0x44C1-lounge-dailycup_config_update"
P44C1 = "protocol_analysis/commands/SC-0x44C1-lounge-dailycup_config_update/README.md"
save("tables/tbl_dailycup_conf.json", tbl(
    "tbl_dailycup_conf", "每日杯配置", "持久化 dailycup_conf 73B；14 成员",
    "PERSIST", "dailycup_conf", "dailycup_conf（73B · 14 成员）", "dailycup_conf", "dailycup_conf",
    "每日杯配置（日志 dailycup_conf=；claim 80 / 线 73）",
    [{"command": CMD44C1, "struct": "dailycup_conf", "field_name": "dailycup_conf", "offset": 0, "length": 73,
      "wire_type": "struct", "protocol_path": P44C1, "section": "§3", "reader": "sub_B46E80", "printer": "sub_B50A10",
      "evidence_va": "B5DD03|B5DE55"}],
    [CMD44C1],
))
save("tables/tbl_dailycup_conf_next.json", tbl(
    "tbl_dailycup_conf_next", "每日杯配置（次日）", "持久化 dailycup_conf_next 73B；同 dailycup_conf",
    "PERSIST", "dailycup_conf_next", "dailycup_conf_next（73B · 同 dailycup_conf）", "dailycup_conf_next", "dailycup_conf",
    "次日每日杯配置（日志 dailycup_conf_next=；claim 80 / 线 73）",
    [{"command": CMD44C1, "struct": "dailycup_conf_next", "field_name": "dailycup_conf_next", "offset": 80, "length": 73,
      "wire_type": "struct", "protocol_path": P44C1, "section": "§3", "reader": "sub_B46E80", "printer": "sub_B50A10",
      "evidence_va": "B5DD83|B5DE55", "notes": "报文字段 #2；紧接 dailycup_conf 80B 槽"}],
    [CMD44C1],
))
dc = json.loads((ROOT / "composites/dailycup_conf.json").read_text(encoding="utf-8"))
save("entities/dailycup_conf.json", entity("dailycup_conf", "每日杯配置；73B/80B；14 成员", "PERSIST",
    [{"name": "config", "length": 73, "memory_claim": 80, "commands": [CMD44C1], "protocol_path": P44C1}],
    [{"name": m["name"], "offset": m["offset"], "length": m["length"], "wire_type": m["wire_type"],
      "meaning": m["meaning"], "disposition": m["disposition"]} for m in dc["members"]]))
save("entities/dailycup_conf_next.json", entity("dailycup_conf_next", "次日每日杯；同 dailycup_conf", "PERSIST",
    [{"name": "config_next", "length": 73, "memory_claim": 80, "commands": [CMD44C1], "protocol_path": P44C1}],
    [], same_as="dailycup_conf"))

# dc_point + dcpoint_detail
CMD2AAF = "SC-0x2AAF-lounge-dailycup_get_point_r"
P2AAF = "protocol_analysis/commands/SC-0x2AAF-lounge-dailycup_get_point_r/README.md"
CMDD5E6 = "SC-0xD5E6-lounge-result_info"
PD5E6 = "protocol_analysis/commands/SC-0xD5E6-lounge-result_info/README.md"
save("tables/tbl_dc_point.json", tbl(
    "tbl_dc_point", "断线杯积分", "持久化 dc_point 41B 线 + 内存嵌套 bef_next/aft_next",
    "PERSIST", "dc_point", "dc_point（41B 线 / 68B 槽）", "dc_point", "dc_point",
    "每日杯积分明细（日志 dc_point=；线 41 / 槽 68）",
    [{"command": CMD2AAF, "struct": "dc_point", "field_name": "dc_point", "offset": None, "length": 41,
      "wire_type": "struct", "protocol_path": P2AAF, "section": "§3", "reader": "sub_B47120", "printer": "sub_B50F80",
      "evidence_va": "B5A8F8|B50F80"}],
    [CMD2AAF],
))
save("tables/tbl_dcpoint_detail.json", tbl(
    "tbl_dcpoint_detail", "断线扣分详情", "持久化 dcpoint_detail；布局同 dc_point（D5E6）",
    "EVENT", "dcpoint_detail", "dcpoint_detail（41B · 同 dc_point）", "dcpoint_detail", "dc_point",
    "结算断线扣分（日志 dcpoint=；claim 68 / 线 41）",
    [{"command": CMDD5E6, "struct": "dcpoint", "field_name": "dcpoint", "offset": None, "length": 41,
      "wire_type": "struct", "protocol_path": PD5E6, "section": "§3", "reader": "sub_B47120", "printer": "sub_B50F80",
      "evidence_va": "B7DD05|B7E3F8", "notes": "D5E6 可变偏移；成员见 composite dc_point"}],
    [CMDD5E6],
))
dcp = json.loads((ROOT / "composites/dc_point.json").read_text(encoding="utf-8"))
save("entities/dc_point.json", entity("dc_point", "断线杯积分；41B/68B", "PERSIST",
    [{"name": "get_point", "length": 41, "memory_claim": 68, "commands": [CMD2AAF], "protocol_path": P2AAF}],
    [{"name": m["name"], "offset": m["offset"], "length": m["length"], "wire_type": m["wire_type"],
      "meaning": m["meaning"], "disposition": m["disposition"]} for m in dcp["members"]]))
save("entities/dcpoint_detail.json", entity("dcpoint_detail", "结算 dcpoint；同 dc_point", "EVENT",
    [{"name": "result_info", "length": 41, "memory_claim": 68, "commands": [CMDD5E6], "protocol_path": PD5E6}],
    [], same_as="dc_point"))

# exam_state
CMDA204 = "SC-0xA204-lounge-pilot_examination_state"
PA204 = "protocol_analysis/commands/SC-0xA204-lounge-pilot_examination_state/README.md"
save("tables/tbl_exam_state.json", tbl(
    "tbl_exam_state", "考核状态", "持久化 exam_state 68B；同 examination_state",
    "PERSIST", "exam_state", "exam_state（68B · 同 examination_state）", "exam_state", "examination_state",
    "考核状态（日志 exam_state=；claim == 线长 == 68）",
    [{"command": CMDA204, "struct": "exam_state", "field_name": "exam_state", "offset": 4, "length": 68,
      "wire_type": "struct", "protocol_path": PA204, "section": "§3", "reader": "sub_B42330", "printer": "sub_B47910",
      "evidence_va": "B6FB6B|B6FB7A|B47910", "notes": "报文字段 #2；成员见 composite examination_state"}],
    [CMDA204],
))
save("entities/exam_state.json", entity("exam_state", "考核状态；68B；同 examination_state", "PERSIST",
    [{"name": "examination", "length": 68, "memory_claim": 68, "commands": [CMDA204], "protocol_path": PA204}],
    [], same_as="examination_state"))

# friend_histories
CMD9F94 = "SC-0x9F94-lounge-friend_history_get_xworld_r"
P9F94 = "protocol_analysis/commands/SC-0x9F94-lounge-friend_history_get_xworld_r/README.md"
save("tables/tbl_friend_histories.json", tbl(
    "tbl_friend_histories", "好友履历", "持久化 friend_histories 113B；同 lpcard",
    "PERSIST", "friend_histories", "friend_histories（113B · 同 lpcard）", "friend_histories", "lpcard",
    "跨服好友履历元素（日志 friend_histories=；113B 线 / 132B 槽）",
    [{"command": CMD9F94, "struct": "friend_histories", "field_name": "friend_histories", "offset": None,
      "length": 113, "wire_type": "array<struct,113>", "protocol_path": P9F94, "section": "§3",
      "reader": "sub_B43100", "printer": "sub_B49580", "evidence_va": "B6E8F8|B49580",
      "notes": "数组元素；成员见 composite lpcard"}],
    [CMD9F94],
))
save("entities/friend_histories.json", entity("friend_histories", "好友履历；113B/132B；同 lpcard", "PERSIST",
    [{"name": "history", "length": 113, "memory_claim": 132, "commands": [CMD9F94], "protocol_path": P9F94}],
    [], same_as="lpcard"))

print("Restored 8 tables + entities")
