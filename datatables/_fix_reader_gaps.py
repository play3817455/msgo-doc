# -*- coding: utf-8 -*-
"""订正三处 reader 真值标错（依据 datatables/_out_ida_reader_asm.txt + _out_ida_readers_pseudo.txt）：

1) QUEST — `reward_table_id` 的 csv_index 由 **4** 改为 **24**。
   `sub_58DCA0`：push 0/1/2/3 → +0/+4/+8/+36，随后 `push 18h`(=24) → `mov [edi+40h], eax`。
   原 schema 把 `0x18` 记成 csv4，导致缺 csv4..csv23 共 20 个占位列（行宽/库宽 5 < reader 24）。
2) WEAPON_SETTING — 15 列被误标 gap，实际 reader 真读：
   35 37 39 42 44 46 48 50 52 54 58 60 61 62 63
   （`sub_5976F0` 内部就是 `sub_BBB920` 取列；39 直连 `sub_BBB920`）
   为**不动库结构**（避免改名触发 -recreate 丢 1648 行），保留物理列名 colN，仅订正 status/证据。
3) MISSION_COOP — col8 被误标 gap，实际 `push 8` → bit2 @+56；
   同时修正 col5/col6/col7 被整体错位一格的 asm_va（原值指向下一列的位操作）。

用法：python datatables/_fix_reader_gaps.py
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")

log = []


def emit(s=""):
    print(s)
    log.append(s)


def load(t):
    with open(os.path.join(TABLES, t + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def save(t, data):
    with open(os.path.join(TABLES, t + ".json"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def by_idx(data):
    return {c["csv_index"]: c for c in data["columns"]}


# ---------------------------------------------------------------- QUEST
q = load("QUEST")
cols = by_idx(q)
rw = cols[4]
assert rw["db_column"] == "reward_table_id", rw
before = rw["csv_index"]
rw["csv_index"] = 24
rw["read_order"] = 25
rw["meaning"] = (
    "奖励表行 ID（u32 @+64；**CSV col24**，asm `push 18h`=24 → `mov [edi+40h],eax`）"
)
rw["display_name"] = "奖励表行 ID（csv24→+64）"
rw["confidence"] = "★确证"
q["column_count"] = 5  # reader 映射列数：0,1,2,3,24
q["column_gap_note"] = (
    "CSV 行含 col0..col24；reader sub_58DCA0 只取 0,1,2,3,24，"
    "csv 4..23 为占位列（读表跳过）"
)
q["columns_note"] = (
    "★2026-10-05 订正：reward_table_id 原误记 csv_index=4（把 asm 的 0x18 当成 4），"
    "实为 col24；补 csv4..csv23 占位列后行宽 25，与 reader 绝对列号对齐"
)
save("QUEST", q)
emit(f"[QUEST] reward_table_id csv_index {before} → 24；column_count=5；待 merge 补 csv4..csv23 占位列")

# ------------------------------------------------------- WEAPON_SETTING
WS_EVIDENCE = {
    35: ("0x598448", 112, "sub_5978A0 三项名字模板块"),
    37: ("0x5984a2", 284, "wstring 原样"),
    39: ("0x5984f6", 316, "sub_BBB920→sub_56F550（条件追加 fx 后缀）"),
    42: ("0x5985ea", 376, "sub_5978A0 三项名字模板块"),
    44: ("0x598641", 464, "sub_5978A0 三项名字模板块"),
    46: ("0x59869c", 552, "sub_5978A0 三项名字模板块"),
    48: ("0x5986f7", 640, "sub_5978A0 三项名字模板块"),
    50: ("0x598752", 728, "sub_5978A0 三项名字模板块"),
    52: ("0x5987b2", 816, "sub_5978A0 三项名字模板块"),
    54: ("0x598857", 1156, "sub_5978A0 三项名字模板块"),
    58: ("0x5989b6", 1300, "sub_597D00 三项派生块（后两项后缀 +10）"),
    60: ("0x598a0c", 1388, "sub_597D00 三项派生块（后两项后缀 +10）"),
    61: ("0x598a60", 1556, "sub_597D00 三项派生块（后两项后缀 +10）"),
    62: ("0x598aa7", 1640, "sub_597D00 三项派生块（后两项后缀 +10）"),
    63: ("0x598afb", 1808, "sub_597D00 三项派生块（后两项后缀 +10）"),
}

ws = load("WEAPON_SETTING")
ws_cols = by_idx(ws)
fixed = []
for idx, (va, off, what) in sorted(WS_EVIDENCE.items()):
    c = ws_cols[idx]
    assert c.get("status") == "gap", (idx, c.get("status"))
    c["status"] = "confirmed"
    c["type"] = "str"
    c["memory_offset"] = off
    c["asm_va"] = va
    c["asm_reader"] = "sub_597F50"
    c["confidence"] = "○ASM确证"
    c["meaning"] = (
        f"reader 真读（`{va}` 取列；值当名字模板 → {what} @+{off}）；"
        f"原标 gap 系仿真静默截断（EMU-CUT）造成的假阴性"
    )
    c["display_name"] = f"派生名模板（csv{idx}→+{off}）"
    fixed.append(idx)
ws["column_count"] = 123  # = 已有 108 confirmed + 本次 15（reader 共读 123/148 列）
ws["columns_note"] = (
    "★2026-10-05 订正：csv " + "、".join(str(i) for i in fixed) + " 共 15 列原标 gap，"
    "经 `sub_597F50` 线性反汇编 + `sub_5976F0`（= 包 `sub_BBB920` 取列）核实为 reader 真读；"
    "为免 `-recreate` 丢 1648 行，**保留物理列名 colN**（GM 显示名已给出语义）"
)
save("WEAPON_SETTING", ws)
emit(f"[WEAPON_SETTING] gap→confirmed {len(fixed)} 列：{fixed}；column_count=123")

# ------------------------------------------------------- MISSION_COOP
mc = load("MISSION_COOP")
mc_cols = by_idx(mc)
# col5/6/7 的 asm_va 整体指向了下一列的位操作 -> 回正
VAFIX = {5: "0x59dce3", 6: "0x59dcf8", 7: "0x59dd10"}
for i, va in VAFIX.items():
    old = mc_cols[i].get("asm_va")
    mc_cols[i]["asm_va"] = va
    emit(f"[MISSION_COOP] col{i} {mc_cols[i]['db_column']} asm_va {old} → {va}")
c8 = mc_cols[8]
assert c8.get("status") == "gap", c8.get("status")
c8["status"] = "confirmed"
c8["type"] = "bool"
c8["db_column"] = "col8"
c8["name"] = "col8"
c8["memory_offset"] = 56
c8["asm_va"] = "0x59dd2d"
c8["asm_reader"] = "sub_59DC00"
c8["confidence"] = "○ASM确证"
c8["meaning"] = (
    "reader 真读（`push 8` @0x59dd0b → `call sub_BBB370` @0x59dd14）："
    "结果写入 **+56 的 bit2**（`add al,al`×2 → `and al,4` → `xor [esi+38h],al` @0x59dd2d）；"
    "与 col6=bit0(flag_ranked)、col7=bit1(flag_private) 同一位域；原标 gap 系仿真静默截断"
)
c8["display_name"] = "标志位2（csv8→+56 bit2）"
mc["column_count"] = 25  # = 原 24 + col8
mc["columns_note"] = (
    "★2026-10-05 订正：csv8 原标 gap，实为 reader 真读（+56 bit2）；"
    "并回正 col5/col6/col7 被整体错位一格的 asm_va"
)
save("MISSION_COOP", mc)
emit("[MISSION_COOP] col8 gap→confirmed（+56 bit2）；column_count=25")

emit()
emit("写入：" + "、".join(["QUEST.json", "WEAPON_SETTING.json", "MISSION_COOP.json"]))
open(os.path.join(HERE, "_out_fix_reader_gaps.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
