# -*- coding: utf-8 -*-
"""第 6 批（2026-10-05）：`MODULE_BONUS` 行宽 6 → 41，列语义/偏移按 **静态反汇编** 订正。

依据（IDA 逐字反编译，可复查）：

* `sub_5A29B0` @`0x5A29B0`（`CModuleBonusTable::ParseRow`，类名/RTTI 由
  `??_7CModuleBonusTable@@6B@`@`0xecef28` 与 ctor `sub_A5A910`@`0xA5A910` 交叉确证）：

```c
v3 = 2;
*a3 = sub_BBB370(a1, 1);        // ★ csv1 → +0   （csv0 全函数不读）
v4 = a3 + 2;  v5 = 8;
do {
    *(v4 - 1) = sub_BBB370(a1, v3);        // → +4  + 12k  「A」
    v7 = v3 + 2;
    *v4       = sub_BBB370(a1, v7++);      // → +8  + 12k  「B」
    v4[1]     = sub_BBB370(a1, v7);        // → +12 + 12k  「V」
    v3 = v7 + 2;                           // 列步长 5（组内 3 列 + 1 列缝 + 组间 1 列缝）
    v4 += 3;                               // 结构步长 3 dword = 12B
} while (--v5);                            // 8 次
```

* 组 k（1..8）列号 = `{5k-3, 5k-1, 5k}`，内存 = `{+4+12(k-1), +8+12(k-1), +12+12(k-1)}`；
  最大列号 = csv40 ⇒ **41 列**（csv0..csv40），其中 **16 列是缝**（csv0、`5k-2`、`5k+1`）。
* `sub_BBB370` → `sub_CC6876` → `sub_CC6865` → `sub_CC772B(_, 0, 10)` = **atoi（十进制整数）**
  ⇒ 本表**没有**浮点/enum 转换，全部 25 个取值列都是整数。
* 结构大小 = 26 dword = **104B**（+0 键 + 8×3）。
* ★**键列是 csv1 不是 csv0**：vtable[5] = `sub_5A2A10`（`return sub_BBB370(a1, 1)`）即 GetKey 读 csv1。
* 消费侧证据（语义旁证）：
  - `sub_5A2A30`：`v3[5] / v3[8] / … / v3[26] > 0` 逐个计数 ⇒ **「A」> 0 才是有效槽**（返回有效槽数）；
  - `sub_5A2AF0(table, group_id, slot)`：返回该槽的「A」（`v4[3*slot+5]`）；
  - `sub_7C09B0` / `sub_7BF480`：拿到「A」后到 `dword_11E3F08` 名表里取名字串 ⇒ 「A」是**定义 ID**；
  - 「B」「V」的消费点**未找到** ⇒ 只确证「会被读满」，语义沿用旧名（`stat_id_b` / `stat_value`，未取证）。

本脚本只改 schema；库/种子同步走 `_apply_module_bonus.py`。
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(os.path.dirname(HERE), "db_design", "schema", "cfg", "tables")
T = "MODULE_BONUS"
READER = "sub_5A29B0"

NOTE6 = ("★2026-10-05 补列宽（第 6 批）：旧 schema 只声明 4 个读到列（row 宽 6），"
         "`sub_5A29B0` 实为「1 键列 + 8 组 × {A,B,V}」固定块循环（列步长 5、结构步长 12B）"
         "⇒ 声明到 **csv40（41 列）**；列号/偏移逐条来自静态反汇编。")
KEY_NOTE = "★本表**索引键在 csv1**（vtable[5] `sub_5A2A10` = `sub_BBB370(a1,1)`）；csv0 全函数不读。"


def gap(idx: int) -> dict:
    return {
        "read_order": idx + 1,
        "csv_index": idx,
        "db_column": f"col{idx}",
        "name": f"col{idx}",
        "type": "u32",
        "memory_offset": None,
        "meaning": f"★gap：`{READER}` 全函数不读 csv{idx}（组内 1 列缝 / 组间 1 列缝）⇒ 纯占位列",
        "display_name": f"占位 col{idx}",
        "status": "gap",
        "confidence": "",
        "asm_reader": None,
        "asm_va": None,
    }


def read_col(idx: int, name: str, off: int, meaning: str, disp: str, va: str, conf: str) -> dict:
    return {
        "read_order": idx + 1,
        "csv_index": idx,
        "db_column": name,
        "name": name,
        "type": "u32",
        "memory_offset": off,
        "meaning": meaning,
        "display_name": disp,
        "status": "confirmed",
        "confidence": conf,
        "asm_reader": READER,
        "asm_va": va,
    }


cols: dict[int, dict] = {0: gap(0)}
cols[1] = read_col(
    1, "bonus_group", 0,
    "加成组 ID（u32 @+0；★**本表索引键** = vtable[5] `sub_5A2A10` 读的就是 csv1）",
    "加成组 ID", "0x5a29cc", "★确证")

for k in range(1, 9):
    base = 4 + 12 * (k - 1)
    cols[5 * k - 3] = read_col(
        5 * k - 3, f"group{k}_stat_id_a", base,
        f"组 {k} 定义 ID「A」（u32 @+{base}；★> 0 = 该槽有效 —— `sub_5A2A30` 以 A>0 计数、"
        f"`sub_5A2AF0` 返回 A、`sub_7C09B0` 拿 A 到 `dword_11E3F08` 名表取名）；"
        f"沿旧名 `stat_id_a`，语义细节未取证",
        f"组{k} 定义 A", "0x5a29d6", "○ASM确证")
    cols[5 * k - 2] = gap(5 * k - 2)          # 组内缝：A 与 B 之间
    cols[5 * k - 1] = read_col(
        5 * k - 1, f"group{k}_stat_id_b", base + 4,
        f"组 {k} 参数「B」（u32 @+{base + 4}；循环第 {k} 轮第 2 项；**语义未取证**，沿旧名 `stat_id_b`）",
        f"组{k} 参数 B", "0x5a29e3", "○ASM确证")
    cols[5 * k] = read_col(
        5 * k, f"group{k}_stat_value", base + 8,
        f"组 {k} 数值「V」（u32 @+{base + 8}；循环第 {k} 轮第 3 项；★atoi 读**整数**，不是 atof；"
        f"**语义未取证**，沿旧名 `stat_value`）",
        f"组{k} 数值 V", "0x5a29ef", "○ASM确证")
    # 组间缝：csv 5k+1（k=1..7）
    if 5 * k + 1 <= 40:
        cols[5 * k + 1] = gap(5 * k + 1)

assert sorted(cols) == list(range(41)), sorted(cols)
columns = [cols[i] for i in range(41)]
gap_idx = [c["csv_index"] for c in columns if c["status"] == "gap"]

path = os.path.join(TABLES, T + ".json")
d = json.load(open(path, encoding="utf-8"))
d["columns"] = columns
d["column_count"] = len(columns)
d["column_defined"] = len(columns)
d["column_confirmed"] = len(columns) - len(gap_idx)
d["column_partial"] = 0
d["column_pending"] = 0
d["column_gap"] = len(gap_idx)
d["asm_status"] = "complete"
d["asm_reader"] = READER
d["reader_max_csv_index"] = 40
d["column_gap_note"] = (f"CSV 行含 col0..col40；csv {', '.join(map(str, gap_idx))} reader 不读（占位）："
                        "csv0 + 每组内 1 缝（5k-2）+ 组间 1 缝（5k+1，最后一组无）")
d["columns_note"] = NOTE6 + " " + KEY_NOTE
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(path, "a", encoding="utf-8").write("\n")
print(f"{T}: {len(columns)} 列（读 {d['column_confirmed']} / 缝 {d['column_gap']}，reader_max=csv40）")
print("  缝列:", gap_idx)
print("  组偏移:", [f"g{k}=+{4 + 12 * (k - 1)}/+{8 + 12 * (k - 1)}/+{12 + 12 * (k - 1)}" for k in range(1, 9)])
