# -*- coding: utf-8 -*-
"""第 4 批（2026-10-05）：两张窄表的行宽与列语义按 **静态反汇编** 订正。

依据（IDA 逐字反编译，可复查）：

* `BEGINNER_CHALLENGE` `sub_570420` @`0x570420`
    - 先取 4 个 u32：`*a3 = col0`，然后 `v3=1` 起循环 3 次写 `a3[1..3]` ⇒ **csv0..csv3**；
    - 再循环 3 次（`v6 = a3+4`，步长 4 dword = 16B）：
      `v6[2] = sub_5703A0(字符串 col v3)`、`v6[0] = col(v3+1)`、`v6[1] = col(v3+2)`、`v6[3] = col(v3+3)`，
      `v3 += 4` ⇒ 三组 `{+0=col(4k+5), +4=col(4k+6), +8=枚举 col(4k+4), +12=col(4k+7)}`，**csv4..csv15**。
    - 结构 = 16 dword = 64B ⇒ **16 列**（当前 6 列 ⇒ csv6..csv15 被越界兜底吃成 0）。
    - 枚举 `sub_5703A0`：不含 `GP` ⇒ **999**；`GP`=**0**、`ITEM`=**1**、`MSMA`=**998**、
      `BUILDUP_MSMA`=**-1**（旧 schema 记的 0/1/2/3 **是错的**）。
* `CHALLENGE_HIGHSCORE` `sub_578630` @`0x578630`
    - `a3[0]=col0`(u32)、`a3[1]=col1`(u8)、`a3+8/+36/+64 = wstring col5/col6/col7`；
    - **csv2/csv3/csv4 全函数不读**（旧 schema 把三串字符串错记在这三列）；
    - 再循环 4 次、每次 5 个 u32（`v7 = a3+100` 起，步长 5 dword=20B）⇒ **csv8..csv27**。
    - 结构 100+4×20 = 180B ⇒ **28 列**（当前 10 列 ⇒ csv10..csv27 吃成 0）。

本脚本只改 schema；库/种子同步走 `_apply_narrow4.py`。
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(os.path.dirname(HERE), "db_design", "schema", "cfg", "tables")

NOTE4 = ("★2026-10-05 补列宽（第 4 批）：旧 schema 行宽不足，reader 高位列被越界兜底吃成 0；"
         "列号/偏移逐条来自静态反汇编。")

# ---------------------------------------------------------------- BEGINNER_CHALLENGE
# (csv_index, name, type, memory_offset, meaning, display_name)
B = [("challenge_id", "u32", 0, "新手挑战 ID（主键）", "挑战 ID")]
B += [(f"unknown_u32_{i}", "u32", 4 * i, f"u32 col{i}（语义未取证；reader 取回后未见引用）",
       f"u32 col{i}（语义未定）") for i in (1, 2, 3)]
# 三组奖励：csv(4+4k)=枚举类型 @+24+16k，csv(4+4k+1/2/3)=三个 u32 @+16/+20/+28+16k
for k, (a, b, c, t) in enumerate(((5, 6, 7, 4), (9, 10, 11, 8), (13, 14, 15, 12)), start=1):
    base = 16 + 16 * (k - 1)
    B.append((f"reward{k}_param_a", "u32", base + 0,
              f"奖励 {k} 第 1 个 u32（循环第 {k} 次 → +{base}）", f"奖励{k} 参数A"))
    B.append((f"reward{k}_param_b", "u32", base + 4,
              f"奖励 {k} 第 2 个 u32（→ +{base + 4}）", f"奖励{k} 参数B"))
    B.append((f"reward{k}_type", "enum", base + 8,
              f"★奖励 {k} 类型（`sub_5703A0` 把字符串 col{t} 转成枚举：GP=0 / ITEM=1 / "
              f"MSMA=998 / BUILDUP_MSMA=-1 / 其他=999）", f"奖励{k} 类型"))
    B.append((f"reward{k}_param_c", "u32", base + 12,
              f"奖励 {k} 第 3 个 u32（→ +{base + 12}）", f"奖励{k} 参数C"))

# csv 顺序 != 结构顺序（每组"类型"列在 csv 上是该组第 1 列）⇒ 显式给出 csv 顺序
B_CSV_ORDER = [
    "challenge_id", "unknown_u32_1", "unknown_u32_2", "unknown_u32_3",
    "reward1_type", "reward1_param_a", "reward1_param_b", "reward1_param_c",
    "reward2_type", "reward2_param_a", "reward2_param_b", "reward2_param_c",
    "reward3_type", "reward3_param_a", "reward3_param_b", "reward3_param_c",
]
B_BY_NAME = {n: (t, o, m, d) for n, t, o, m, d in B}
assert sorted(B_CSV_ORDER) == sorted(B_BY_NAME), (set(B_CSV_ORDER) ^ set(B_BY_NAME))

ENUM_B = [
    {"name": "GP", "value": 0},
    {"name": "ITEM", "value": 1},
    {"name": "MSMA", "value": 998},
    {"name": "BUILDUP_MSMA", "value": -1},
    {"name": "(其他)", "value": 999},
]


def col_beginner(idx: int) -> dict:
    name = B_CSV_ORDER[idx]
    typ, off, mean, disp = B_BY_NAME[name]
    c = {
        "read_order": idx + 1,
        "csv_index": idx,
        "db_column": name,
        "name": name,
        "type": typ,
        "memory_offset": off,
        "meaning": mean,
        "display_name": disp,
        "status": "confirmed",
        "confidence": "★确证" if idx == 0 else "○ASM确证",
        "asm_reader": "sub_570420",
        "asm_va": None,
    }
    if typ == "enum":
        c["enum_converter"] = "sub_5703A0"
        c["enum_values"] = ENUM_B
        c["enum_doc"] = "reverse-login-chain/formats/枚举表.md"
    return c


# ---------------------------------------------------------------- CHALLENGE_HIGHSCORE
H_NAMES = {
    0: ("highscore_id", "u32", 0, "协作挑战排行 ID（主键）", "排行 ID", "★确证"),
    1: ("mission_id", "u8", 4, "关联协作战任务 ID（col1 只取低字节 → MISSION_COOP）", "任务 ID", "○ASM确证"),
    2: ("col2", "gap", None, "★reader 不读（`sub_578630` 全函数无 col2）⇒ 占位列", "占位 col2", ""),
    3: ("col3", "gap", None, "★reader 不读 ⇒ 占位列", "占位 col3", ""),
    4: ("col4", "gap", None, "★reader 不读 ⇒ 占位列", "占位 col4", ""),
    5: ("reward_desc", "wstr", 8, "宽字符串 @+8（★位置确证；文本角色沿旧名，未取证）", "文本 col5", "★确证"),
    6: ("ui_label", "wstr", 36, "宽字符串 @+36（★位置确证；文本角色沿旧名，未取证）", "文本 col6", "★确证"),
    7: ("footer_text", "wstr", 64, "宽字符串 @+64（★位置确证；文本角色沿旧名，未取证）", "文本 col7", "★确证"),
}
for g in range(4):
    for j in range(5):
        idx = 8 + g * 5 + j
        off = 92 + g * 20 + j * 4
        if idx == 8:
            H_NAMES[idx] = ("score_threshold", "u32", off,
                            f"u32 循环第 1 组第 1 个 → +{off}（沿旧名 `score_threshold`，语义未取证）",
                            "分数阈值", "○ASM确证")
        elif idx == 9:
            H_NAMES[idx] = ("reward_gp", "u32", off,
                            f"u32 循环第 1 组第 2 个 → +{off}（沿旧名 `reward_gp`，语义未取证）",
                            "奖励 GP", "○ASM确证")
        else:
            H_NAMES[idx] = (f"unknown_u32_{idx}", "u32", off,
                            f"u32 col{idx}（循环第 {g + 1} 组第 {j + 1} 个 → +{off}；"
                            f"reader 取回后未见引用，语义未定）",
                            f"u32 col{idx}（语义未定）", "○ASM确证")


def col_highscore(idx: int) -> dict:
    name, typ, off, mean, disp, conf = H_NAMES[idx]
    gap = typ == "gap"
    return {
        "read_order": idx + 1,
        "csv_index": idx,
        "db_column": name,
        "name": name,
        "type": "u32" if gap else typ,
        "memory_offset": off,
        "meaning": mean,
        "display_name": disp,
        "status": "gap" if gap else "confirmed",
        "confidence": conf,
        "asm_reader": None if gap else "sub_578630",
        "asm_va": None,
    }


# ---------------------------------------------------------------- 写入
def apply(table: str, cols: list, reader_max: int, gap: int, note: str):
    path = os.path.join(TABLES, table + ".json")
    d = json.load(open(path, encoding="utf-8"))
    d["columns"] = cols
    d["column_count"] = len(cols) - gap
    d["column_defined"] = len(cols)
    d["column_confirmed"] = len(cols) - gap
    d["column_partial"] = 0
    d["column_pending"] = 0
    d["column_gap"] = gap
    d["asm_status"] = "complete"
    d["asm_reader"] = cols[0]["asm_reader"] or d.get("asm_reader")
    d["reader_max_csv_index"] = reader_max
    d["column_gap_note"] = (
        f"CSV 行含 col0..col{reader_max}；"
        + (f"csv {', '.join(str(c['csv_index']) for c in cols if c['status'] == 'gap')} reader 不读（占位）"
           if gap else "全部列都由 reader 映射（无 gap 列）")
    )
    d["columns_note"] = note
    json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(path, "a", encoding="utf-8").write("\n")
    print(f"{table}: {len(cols)} 列（column_count={d['column_count']}，gap={gap}，"
          f"reader_max=csv{reader_max}）")


apply(
    "BEGINNER_CHALLENGE",
    [col_beginner(i) for i in range(16)],
    15, 0,
    NOTE4 + " 结构 = 4 个 u32（csv0..csv3）+ **3 组**{u32,u32,枚举,u32}（每组 16B，"
    "组内 csv 序 = 类型,参数A,参数B,参数C，结构偏移序 = 参数A,参数B,类型,参数C）⇒ 16 列。"
    "旧 schema 把 `reward_type` 记在 csv2、`reward_quantity` 记在 csv4（实际 csv4 才是类型枚举，"
    "且枚举值应为 GP=0/ITEM=1/MSMA=998/BUILDUP_MSMA=-1/其他=999）⇒ 本批一并订正。",
)

apply(
    "CHALLENGE_HIGHSCORE",
    [col_highscore(i) for i in range(28)],
    27, 3,
    NOTE4 + " 布局 = u32(csv0) + u8(csv1) + **csv2/3/4 空占位（reader 不读）** + 3 个 wstring"
    "（csv5/6/7 → +8/+36/+64）+ **4 组 × 5 个 u32**（csv8..csv27 → +92..+168，步长 20B）⇒ 28 列。"
    "旧 schema 把三串字符串错记在 csv2/3/4，并把 csv8/csv9 当成循环外单列 ⇒ 本批订正。",
)
