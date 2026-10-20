# -*- coding: utf-8 -*-
"""第 5 批（2026-10-05）：`ITEM_PART`（`item/equip_parts.csv`, #7）行宽 21 → 50 列，按 **静态反汇编** 订正。

依据：`sub_5955A0` @`0x5955A0` 逐字反编译（IDA，可复查）：

```
*(a3+0)  = col0                       // u32 主键
*(a3+4)  = col2                       // u32   ★col1 全函数不读
*(a3+8)  = col3                       // u32
*(a3+12) = sub_5954A0(col4)           // 枚举字符串：MS=0 / WEAPON=1 / ARMOR=2 / 其他=3
*(a3+16..+32) = atof(col5..col9)      // 5 个 float
*(a3+36) = sub_5951D0(col10)          // 触发时机枚举（ANYTIME=1 …）
*(a3+40) = atof(col11)
*(a3+44) = sub_5951D0(col12)
*(a3+68) = atoi(col13) ; *(a3+48) = atof(col13)   // ★同一列读两遍（u32 与 float 各存一份）
*(a3+52) = atof(col14) ; *(a3+56) = atof(col15)

v6 = 16;  v5 = &(a3+80);
do {                                   // ★8 次
    *(v5-2) = sub_5952C0(col v6)       //   作用对象枚举（MS=1 / WEAPON_SLOT_MAIN=11 / … / OTHER=99）
    e = sub_5953B0(col v6+1)           //   参数名枚举（MS_ARMOR=100 … OTHER_CMDRSPT_RESPAWNTIME=2000）
    *(v5-1) = e
    if (e == 109 /* MS_BOOST_GAUGE_RECOV */) {
        *(v5) = atoi(col v6+2) + 64 * atoi(col v6+3)   // ★该组多占 1 列（2 列拼成 1 个值）
        v6 += 4
    } else {
        *(v5) = atof(col v6+2);  v6 += 3
    }
    v5 += 3;
} while (--8)
*(a3+60) = col v6 ; *(a3+64) = col v6+1     // 尾部 2 个 u32，**位置随上面前进量而变**
```

⇒ 行布局 = **16 前导列** + **8 组 ×（3 或 4）列** + **2 尾列**。
常态（组内参数名 ≠ `MS_BOOST_GAUGE_RECOV`）合计 = 16 + 8×3 + 2 = **42 列**；
最坏（8 组全为该参数名）合计 = 16 + 8×4 + 2 = **50 列** ⇒ schema 按 **50** 声明（固定宽度表必须覆盖最坏情况，
否则真实数据里这类行的最后几列会被静默截断；与第 3 批 `WEAPON_BATTLE_DETAIL` 按"属性名上限"定宽同一口径）。

本脚本只改 schema；库/种子同步走 `_apply_item_part.py`。
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(os.path.dirname(HERE), "db_design", "schema", "cfg", "tables")
PATH = os.path.join(TABLES, "ITEM_PART.json")

NOTE5 = ("★2026-10-05 第 5 批：旧 schema 21 列（把「8 组循环」当成了单组，并把尾列钉在 csv19/20）；"
         "按 `sub_5955A0` 的实际光标推进订正为 **50 列** = 16 前导 + 8 组×（3/4 列）+ 2 尾列（含 `MS_BOOST_GAUGE_RECOV` 多占列的余量）。"
         "col13 **同列双读**（`+48` float 与 `+68` u32）；尾部 2 个 u32 的 **CSV 位置随组内列数浮动** ⇒ 命名固定为常态布局。")

OLD = json.load(open(PATH, encoding="utf-8"))
ENUMS = {}
for c in OLD["columns"]:
    ec = c.get("enum_converter")
    if ec and c.get("enum_values"):
        ENUMS[ec] = c["enum_values"]
assert set(ENUMS) == {"sub_5954A0", "sub_5951D0", "sub_5952C0", "sub_5953B0"}, set(ENUMS)

TRIG = "触发时机枚举（`sub_5951D0`，见 `01-列注释/07-*`）"

# ---------------------------------------------------------------- 前导 16 列（csv0..15）
PRE = {
    0: ("item_part_id", "u32", 0, "主键；装备零件（部件）ID", "零件 ID", "★确证"),
    2: ("linked_item_id", "u32", 4, "关联 ITEM 行 ID（`sub_BBB370(2)` → +4）", "关联 ITEM ID", "★确证"),
    3: ("part_group_id", "u32", 8, "零件组 ID（→ +8）", "零件组 ID", "○ASM确证"),
    4: ("target_category", "enum", 12, "作用大类：MS=0 / WEAPON=1 / ARMOR=2 / 其他=3（`sub_5954A0` → +12）",
        "作用大类", "★确证"),
    5: ("trigger_threshold_a", "float", 16, "触发阈值 A（`atof` → +16；与 `trigger_type_primary` 配合）", "触发阈值 A", "○ASM确证"),
    6: ("trigger_threshold_b", "float", 20, "触发阈值 B（→ +20）", "触发阈值 B", "○ASM确证"),
    7: ("trigger_threshold_c", "float", 24, "触发阈值 C（→ +24）", "触发阈值 C", "○ASM确证"),
    8: ("trigger_threshold_d", "float", 28, "触发阈值 D（→ +28）", "触发阈值 D", "○ASM确证"),
    9: ("trigger_threshold_e", "float", 32, "触发阈值 E（→ +32）", "触发阈值 E", "○ASM确证"),
    10: ("trigger_type_primary", "enum", 36, "主触发时机（`sub_5951D0` → +36）", "主触发时机", "★确证"),
    11: ("effect_magnitude", "float", 40, "效果幅度（→ +40）", "效果幅度", "○ASM确证"),
    12: ("trigger_type_secondary", "enum", 44, "副触发时机（`sub_5951D0` → +44）", "副触发时机", "★确证"),
    13: ("param_mod_value", "float", 48, "★同一列双读：float → +48，**u32 另存 +68**（`sub_BBB370(col13)`）", "参数修改值", "★确证"),
    14: ("param_mod_value_b", "float", 52, "参数修改值 B（→ +52）", "参数修改值 B", "○ASM确证"),
    15: ("param_mod_value_c", "float", 56, "参数修改值 C（→ +56）", "参数修改值 C", "○ASM确证"),
}
ROLE = ("作用对象", "参数名", "参数值")

cols: list[dict] = []
for i in range(16):
    if i == 1:
        cols.append({
            "read_order": i + 1, "csv_index": i, "db_column": "col1", "name": "col1",
            "type": "u32", "memory_offset": None,
            "meaning": "★gap：`sub_5955A0` 全函数不读（`sub_BBB370(1)` 不存在）⇒ 纯占位列",
            "display_name": "占位 col1", "status": "gap", "confidence": "",
            "asm_reader": None, "asm_va": None,
        })
        continue
    name, typ, off, mean, disp, conf = PRE[i]
    c = {
        "read_order": i + 1, "csv_index": i, "db_column": name, "name": name,
        "type": typ, "memory_offset": off, "meaning": mean, "display_name": disp,
        "status": "confirmed", "confidence": conf,
        "asm_reader": "sub_5955A0", "asm_va": None,
    }
    if typ == "enum":
        c["enum_converter"] = "sub_5954A0" if i == 4 else "sub_5951D0"
        c["enum_values"] = ENUMS[c["enum_converter"]]
        c["enum_doc"] = "reverse-login-chain/formats/枚举表.md"
    cols.append(c)

ENUM_ROLE = {"作用对象": "sub_5952C0", "参数名": "sub_5953B0"}

# ---------------------------------------------------------------- 8 组 × 3 槽（csv16..39，常态布局）
for g in range(8):
    base = 72 + 12 * g
    for j, role in enumerate(ROLE):
        idx = 16 + g * 3 + j
        name = f"group{g + 1}_{('scope', 'stat', 'value')[j]}"
        if role == "参数值":
            mean = (f"第 {g + 1} 组参数值（`atof` → +{base + 8}）；"
                    f"★若本组参数名为 `MS_BOOST_GAUGE_RECOV`(109) 则值为 `atoi(A)+64*atoi(B)` 并多占 1 列")
        else:
            mean = (f"第 {g + 1} 组{role}（枚举 `{ENUM_ROLE[role]}` → +{base + 4 * j}）")
        c = {
            "read_order": idx + 1, "csv_index": idx, "db_column": name, "name": name,
            "type": "enum" if role != "参数值" else "float",
            "memory_offset": base + 4 * j,
            "meaning": mean + "。★8 组循环按「作用对象/参数名/参数值」顺序消费 CSV ⇒ 本列按**常态布局**（组组 3 列）命名；"
                              "若前行某组为 `MS_BOOST_GAUGE_RECOV` 则整体后移，含义随行变。",
            "display_name": f"第{g + 1}组{role}", "status": "confirmed",
            "confidence": "★确证" if role != "参数值" else "○ASM确证",
            "asm_reader": "sub_5955A0", "asm_va": None,
        }
        if role != "参数值":
            c["enum_converter"] = ENUM_ROLE[role]
            c["enum_values"] = ENUMS[ENUM_ROLE[role]]
            c["enum_doc"] = "reverse-login-chain/formats/枚举表.md"
        cols.append(c)

# ---------------------------------------------------------------- 尾部 2 列（csv40/41，常态布局）
for k, (idx, off) in enumerate(((40, 60), (41, 64))):
    name = f"tail_u32_{off}"
    cols.append({
        "read_order": idx + 1, "csv_index": idx, "db_column": name, "name": name,
        "type": "u32", "memory_offset": off,
        "meaning": f"尾部第 {k + 1} 个 u32（→ +{off}）；★CSV 位置 = 8 组消费完后的**光标处**"
                   f"（常态布局落在 csv{idx}；有 `MS_BOOST_GAUGE_RECOV` 组时随之后移）",
        "display_name": f"尾列 u32 @+{off}", "status": "confirmed", "confidence": "○ASM确证",
        "asm_reader": "sub_5955A0", "asm_va": None,
    })

# ---------------------------------------------------------------- 余量 8 列（csv42..49）
for idx in range(42, 50):
    name = f"overflow_slot_{idx}"
    cols.append({
        "read_order": idx + 1, "csv_index": idx, "db_column": name, "name": name,
        "type": "u32", "memory_offset": None,
        "meaning": "★余量槽位：8 组中每出现一次 `MS_BOOST_GAUGE_RECOV`(109) 组，该组就**多占 1 列**"
                   "（最多 8 列 / 可读到 csv49）⇒ 这 8 列只在**含该参数名的行**里被消费；"
                   "本表当前数据（64 行全空）走常态布局读不到，保留是为了承载真实数据的这类行、**避免静默截断**",
        "display_name": "余量槽位（109 组用）", "status": "confirmed", "confidence": "○ASM确证",
        "asm_reader": "sub_5955A0", "asm_va": None,
    })

assert len(cols) == 50 and [c["csv_index"] for c in cols] == list(range(50))

d = dict(OLD)
d["columns"] = cols
d["column_count"] = 50
d["column_defined"] = 50
d["column_confirmed"] = 49
d["column_partial"] = 0
d["column_pending"] = 0
d["column_gap"] = 1
d["column_gap_note"] = ("CSV 行常态 col0..col41（16 前导 + 8 组×3 + 2 尾），"
                        "含 `MS_BOOST_GAUGE_RECOV` 组的行可读到 col49 ⇒ schema 声明到 col49；"
                        "**csv1 reader 从不读（纯占位）**")
d["columns_note"] = NOTE5
d["reader_max_csv_index"] = 49
d["asm_status"] = "complete"
d["asm_reader"] = "sub_5955A0"
json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(PATH, "a", encoding="utf-8").write("\n")
print(f"ITEM_PART: 50 列（gap=1，reader_max=csv49）→ {os.path.relpath(PATH, os.path.dirname(HERE))}")
print("列名:", ", ".join(c["name"] for c in cols))
