# -*- coding: utf-8 -*-
"""补 5 张「窄表」的 schema 列定义（客户端 reader 真读列号 → schema csv_index）。

依据（IDA 反编译 + Unicorn 仿真，见 datatables/17-读表真值全表对账.md）：
  PLAY_BONUS_REWARD  sub_58C440 读 push 0..7,9      → 需 csv9
  PLAYER_NAVI        sub_58C7C0 读到 push 18        → 需 csv17,18
  BUFF               sub_570750 循环 ebx=8..11      → 需 csv9,10,11
  MODULE_DEVELOP     sub_5A2B90 3 组配对循环        → 需 csv7..12（含 2 个 gap）
  MISSION_EXTRULE    sub_59E170 2×4 循环            → 需 csv6..13

原则：客户端 reader 的取列是**按绝对列号**的，缺列时 sub_456D90 返回 "" ⇒ atoi/atof = 0。
      所以补列 + 填 0 与「不补列」对客户端**行为等价**；补的意义是：
        1) 列位诚实（库/CSV 宽度 == reader 读列数，不再需要客户端越界兜底 0）；
        2) 将来拿到原版数值可直接落库生效（缺列时会被静默丢弃）。
      没有原版数据 ⇒ 一律占位 0/空（用户裁定："按照客户端行为补，没有原版只能我们自行处理"）。
"""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLES = os.path.join(ROOT, "db_design", "schema", "cfg", "tables")

PAD = "原版数据缺失 ⇒ 本服占位 0（缺列时客户端 sub_456D90 越界返回 \"\" ⇒ atoi 0，行为等价）"


def read_col(csv_index, name, type_, meaning, display_name, reader, off, va=None):
    return {
        "read_order": 0,
        "csv_index": csv_index,
        "db_column": name,
        "type": type_,
        "meaning": meaning,
        "confidence": "○ASM确证",
        "status": "confirmed",
        "name": name,
        "display_name": display_name,
        "asm_reader": reader,
        "asm_va": va,
        "memory_offset": off,
    }


def gap_col(csv_index, name, meaning, reader):
    return {
        "read_order": 0,
        "csv_index": csv_index,
        "db_column": name,
        "type": "u32",
        "meaning": meaning,
        "confidence": "○ASM确证",
        "status": "gap",
        "name": name,
        "display_name": meaning.split("（")[0],
        "asm_reader": reader,
        "asm_va": None,
        "memory_offset": None,
    }


# ---------------------------------------------------------------- 各表新增列
NEW = {}

NEW["PLAY_BONUS_REWARD"] = [
    read_col(
        9, "unknown_u32_9", "u32",
        "客户端 sub_58C440 取 csv9 → u32 @+28（push 9 @0x58c4a3 / call 0x58c4a9；Unicorn 仿真一致）；"
        "本函数取回后未再引用，语义未定。" + PAD,
        "u32 col9（语义未定，占位 0）", "sub_58C440", 28),
]
NEW["PLAY_BONUS_REWARD_NOTE"] = (
    "★2026-10-05 补列宽：旧 schema 只到 csv8（9 列），而 sub_58C440 读到 csv9（push 0..7,9，跳过 csv8）"
    "⇒ 追加 csv9 使 CSV 宽 10 列、库 10 列，与 reader 读列数一致。"
)

NEW["PLAYER_NAVI"] = [
    read_col(
        17, "unknown_u32_17", "u32",
        "客户端 sub_58C7C0 尾段取 csv17 → u32 @+136（v7=17 常量 push）；本函数取回后未再引用，语义未定。" + PAD,
        "u32 col17（语义未定，占位 0）", "sub_58C7C0", 136),
    read_col(
        18, "unknown_u32_18", "u32",
        "客户端 sub_58C7C0 尾段取 csv18 → u32 @+140（v7+1 常量 push）；本函数取回后未再引用，语义未定。" + PAD,
        "u32 col18（语义未定，占位 0）", "sub_58C7C0", 140),
]
NEW["PLAYER_NAVI_NOTE"] = (
    "★2026-10-05 补列宽：旧 schema 只到 csv16（17 列），而 sub_58C7C0 尾段还取 csv17/csv18"
    "（跳过 csv12）⇒ 追加 csv17/18 使 CSV 宽 19 列、库 19 列。"
)

NEW["BUFF"] = [
    read_col(
        9, "effect_param_1", "u32",
        "类别相关效果参数第 2 项（sub_570750 循环 ebx=8..11 → +44/+48/+52/+56；本列落 +48）；"
        "值入结构体但本函数未再引用，语义未定。" + PAD,
        "效果参数1", "sub_570750", 48),
    read_col(
        10, "effect_param_2", "u32",
        "类别相关效果参数第 3 项（sub_570750 同一循环 → +52）；本函数未再引用，语义未定。" + PAD,
        "效果参数2", "sub_570750", 52),
    read_col(
        11, "effect_param_3", "u32",
        "类别相关效果参数第 4 项（sub_570750 同一循环 → +56；数组收尾）；本函数未再引用，语义未定。" + PAD,
        "效果参数3", "sub_570750", 56),
]
NEW["BUFF_NOTE"] = (
    "★2026-10-05 补列宽：旧 schema 只到 csv8（9 列），而 sub_570750 的效果参数是 "
    "ebx=8..11 的 4 项循环（+44/+48/+52/+56）⇒ 追加 effect_param_1..3 使 CSV 宽 12 列、库 12 列。"
    "另据反汇编订正：csv3..csv6 的取值被**读后丢弃**（+36 字节写回原值，值不落结构体），"
    "改这 4 列对客户端无影响（详见各列 meaning）。"
)

NEW["MODULE_DEVELOP"] = [
    read_col(
        7, "material2_item_id", "u32",
        "材料第 2 组 ITEM ID（u32 @+12；sub_5A2B90 配对循环第 2 组，与第 1 组 material_item_id/material_qty 同构）。" + PAD,
        "材料2 ITEM ID", "sub_5A2B90", 12),
    gap_col(
        8, "reserved_u32_8",
        "CSV col8 预留（sub_5A2B90 三组配对循环只取 (4,6)/(7,9)/(10,12)，本列不读；保持 CSV 列位对齐；默认 0）",
        "sub_5A2B90"),
    read_col(
        9, "material2_qty", "u32",
        "材料第 2 组数量（u32 @+16；sub_5A2B90 第 2 组配对收尾）。" + PAD,
        "材料2 数量", "sub_5A2B90", 16),
    read_col(
        10, "material3_item_id", "u32",
        "材料第 3 组 ITEM ID（u32 @+20；sub_5A2B90 配对循环第 3 组）。" + PAD,
        "材料3 ITEM ID", "sub_5A2B90", 20),
    gap_col(
        11, "reserved_u32_11",
        "CSV col11 预留（sub_5A2B90 不读本列；保持 CSV 列位对齐；默认 0）",
        "sub_5A2B90"),
    read_col(
        12, "material3_qty", "u32",
        "材料第 3 组数量（u32 @+24；sub_5A2B90 第 3 组配对收尾，也是全表最大列号）。" + PAD,
        "材料3 数量", "sub_5A2B90", 24),
]
NEW["MODULE_DEVELOP_NOTE"] = (
    "★2026-10-05 补列宽：反编译 sub_5A2B90 得固定列号 0,2,3,4,6,7,9,10,12（do{v3,v3+2; v3+=3}×3 三组"
    "「材料ID/材料数量」配对，组间空一列），旧 schema 只到 csv6 ⇒ 追加 csv7..csv12（含 gap csv8/csv11）"
    "使 CSV 宽 13 列、库 13 列。结构体 9 字段偏移：+0/+4/+8/+12/+16/+20/+24/+28/+32。"
)

NEW["MISSION_EXTRULE"] = [
    read_col(6, "unknown_u32_6", "u32",
             "客户端 sub_59E170 外层 2×内层 4 循环取 csv6 → u32 @+20（结构体 a3[5]）；本函数未再引用，语义未定。" + PAD,
             "u32 col6（语义未定，占位 0）", "sub_59E170", 20),
    read_col(7, "unknown_u32_7", "u32",
             "同一循环取 csv7 → u32 @+24（a3[6]）；未再引用，语义未定。" + PAD,
             "u32 col7（语义未定，占位 0）", "sub_59E170", 24),
    read_col(8, "unknown_u32_8", "u32",
             "同一循环取 csv8 → u32 @+28（a3[7]）；未再引用，语义未定。" + PAD,
             "u32 col8（语义未定，占位 0）", "sub_59E170", 28),
    read_col(9, "unknown_u32_9", "u32",
             "同一循环取 csv9 → u32 @+32（a3[8]，第 1 组收尾）；未再引用，语义未定。" + PAD,
             "u32 col9（语义未定，占位 0）", "sub_59E170", 32),
    read_col(10, "unknown_u32_10", "u32",
             "同一循环取 csv10 → u32 @+36（a3[9]，第 2 组起始）；未再引用，语义未定。" + PAD,
             "u32 col10（语义未定，占位 0）", "sub_59E170", 36),
    read_col(11, "unknown_u32_11", "u32",
             "同一循环取 csv11 → u32 @+40（a3[10]）；未再引用，语义未定。" + PAD,
             "u32 col11（语义未定，占位 0）", "sub_59E170", 40),
    read_col(12, "unknown_u32_12", "u32",
             "同一循环取 csv12 → u32 @+44（a3[11]）；未再引用，语义未定。" + PAD,
             "u32 col12（语义未定，占位 0）", "sub_59E170", 44),
    read_col(13, "unknown_u32_13", "u32",
             "同一循环取 csv13 → u32 @+48（a3[12]，全表最大列号）；未再引用，语义未定。" + PAD,
             "u32 col13（语义未定，占位 0）", "sub_59E170", 48),
]
NEW["MISSION_EXTRULE_NOTE"] = (
    "★2026-10-05 补列宽：反编译 sub_59E170 得固定列号 0,2,3,4,5,6..13（csv1 跳过；尾部为"
    "外层2×内层4 共 8 个 u32 循环），旧 schema 只到 csv5 ⇒ 追加 csv6..csv13 使 CSV 宽 14 列、库 14 列。"
    "同时订正：csv4(param_b) 落 +12、csv5(param_value) 落 +16（旧 schema 把 param_value 标成 +12，整段早一格）；"
    "csv1(rule_label) 客户端根本不读 ⇒ 状态由 confirmed 改 gap（仅作本服备注/GM 展示名，见 gm/modules_spec.go NameCols）。"
)

# --------------------------------------------- 既有列的 meaning/offset 订正
FIX = {
    "BUFF": {
        3: dict(meaning="效果持续秒数（sub_570750 push 3）——★反汇编订正：取值被**读后丢弃**"
                      "（0x5707eb 起为 movzx/mov [esi+24h]，写回 +36 原值），值不落结构体 ⇒ 本服改此列对客户端无影响",
                memory_offset=None),
        4: dict(meaning="堆叠上限（sub_570750 push 4）——★读后丢弃（同上，+36 写回原值），改此列无客户端影响",
                memory_offset=None),
        5: dict(meaning="优先级（sub_570750 push 5）——★读后丢弃（同上，+36 写回原值），改此列无客户端影响",
                memory_offset=None),
        6: dict(meaning="UI 图标索引（sub_570750 push 6）——★读后丢弃（同上，+36 写回原值），改此列无客户端影响",
                memory_offset=None),
    },
    "MISSION_EXTRULE": {
        4: dict(memory_offset=12),
        5: dict(memory_offset=16),
        1: dict(status="gap", confidence="○ASM确证", memory_offset=None, asm_va=None,
                meaning="CSV col1：客户端 reader（sub_59E170）跳过、不落内存 ⇒ 仅本服备注/标签列"
                        "（gm/modules_spec.go 用它作 NameCols 展示名；改它不影响客户端）"),
    },
}

log = []


def emit(s=""):
    print(s)
    log.append(s)


for table, cols in NEW.items():
    if table.endswith("_NOTE"):
        continue
    path = os.path.join(TABLES, table + ".json")
    d = json.load(open(path, encoding="utf-8"))
    note = NEW.get(table + "_NOTE")

    for old, patch in (FIX.get(table) or {}).items():
        c = next(c for c in d["columns"] if c["csv_index"] == old)
        before = {k: c.get(k) for k in patch}
        c.update(patch)
        emit(f"[{table}] 订正 csv{old}（{c['db_column']}）：{before} → {patch}")

    have = {c["csv_index"] for c in d["columns"]}
    added = [c for c in cols if c["csv_index"] not in have]
    if not added and not note:
        emit(f"[{table}] 无需改动")
        continue
    d["columns"] = sorted(d["columns"] + added, key=lambda c: c["csv_index"])
    for i, c in enumerate(d["columns"], 1):
        c["read_order"] = i
    max_idx = max(c["csv_index"] for c in d["columns"])
    conf = sum(1 for c in d["columns"] if c["status"] == "confirmed")
    gap = sum(1 for c in d["columns"] if c["status"] == "gap")
    d["column_count"] = conf
    d["column_defined"] = len(d["columns"])
    d["column_confirmed"] = conf
    d["column_partial"] = sum(1 for c in d["columns"] if c["status"] == "partial")
    d["column_pending"] = sum(1 for c in d["columns"] if c["status"] not in ("confirmed", "partial", "gap"))
    d["column_gap"] = gap
    d["asm_status"] = "complete" if d["column_pending"] == 0 else "partial"
    d["column_gap_note"] = f"CSV 行含 col0..col{max_idx}，读表跳过未映射列见 gap 标记"
    if note:
        d["columns_note"] = note
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    emit(f"[{table}] 新增 {len(added)} 列 csv{sorted(c['csv_index'] for c in added)} "
         f"⇒ 定义 {len(d['columns'])} 列（confirmed {conf} / gap {gap}），列号 0..{max_idx}")

open(os.path.join(HERE, "_out_widen_patch.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
