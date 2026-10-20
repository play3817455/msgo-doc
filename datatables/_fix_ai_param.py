# -*- coding: utf-8 -*-
"""第 7 批（2026-10-05）：`AI_PARAM` 行宽 45 → 127，列语义按 **静态反汇编** 全量重订。

依据（IDA 逐字反汇编 + 共享子读函数逐个展开，可复查）：

* `sub_56EA00` @`0x56EA00`（`CAIParam::ParseRow`；类名/RTTI 由 `??_7CAIParam@@6B@`@`0xecf1b0`、
  ctor `sub_A5B8E0`@`0xA5B8E0` 交叉确证；vtable[5] = `sub_A564D0` = `atoi(a1,0)` ⇒ 键 = csv0）。
* 三个**同构带块**由 `sub_56E220` @`0x56E220` 读：每块 **25 列**
  = `{3 字节 atoi, 22 个 atof}`，`v42[0]` 由调用方或写 0；
  块内 23 个 float 随后被 `sub_56E450` **归一化（和 = 1）**。
* 列号游标 `v36` 由调用方持有并**按引用**传给子读函数（`&v36`），子函数每读一列 `(*a4)++`：

```c
csv0 → +0     atoi                     // 键
csv1 → +4     sub_56E570(窄串)          // enum 17 值
csv2 → +8     sub_56E610(窄串)          // enum  9 值
csv3 → +44    atoi != 0                // bool（u8）
csv4..9  → +12/+16/+20/+24/+28/+32  atof×π/180（csv4/csv7 取负）
csv10 → +36   100 * atoi
csv11 → +40   atof×π/180（<0 时写 FLT_MIN 1.17e-38）
csv12 → +520 bit0                     csv13 → +520 bit2     csv14 → +520 bit1
csv15 → +76   atof                     csv16 → +80  atof
v36 = 18;
csv17 → +520 bit3
sub_56E890(a3+84, a1, &v36)            // ★吃 5 列：csv18..22
csv23..47  sub_56E220(&v34, v42, a1, &v36)   // ★吃 25 列 → 带 A（NEAR）
csv48      v42[0] = atof（带 A 的 float[0]）
csv49..51  → +228 / +232 / +236（后两个 ×100）
csv52..76  sub_56E220(…)               // ★吃 25 列 → 带 B（MIDDLE），v42[0]=0
csv77..78  → +340 / +344（×100）
csv79..103 sub_56E220(…)               // ★吃 25 列 → 带 C（FAR），v42[0]=0
csv104..105 → +448 / +452（×100）
csv106..109 → +456/+460/+464/+468（4 值被 sub_56E510 归一化，和 = 1）
csv110..113 → +520 bit4 / bit7 / bit5 / bit6
csv114..118 → +472 / +476 / +480 / +484 / +488（+476/+480/+484 三者按和归一化）
csv119..121 → +492 / +496 / +500
csv122..125 sub_56E3F0(a3+504, a1, &v36)    // ★吃 4 列 → +504(u8)/+508/+512/+516
csv126     → +521 bit0
```

* ⇒ 读到 **csv126**，行宽 **127**，**无缝列**（仿真实测 csv0..csv126 连续全读）。
* 枚举表（本脚本从 IDA 逐字读出）：
  - csv1 `sub_56E570`（`0xD77428`/`0xD7742C`）：NORMAL=1 … DEBRIS=17（17 值）
  - csv2 `sub_56E610`（`0xD77558`/`0xD7755C`）：NORMAL=0 … BROADWAYONLY=8（9 值）
  - csv22 `sub_56E6B0`（`0xD775EC`/`0xD775F0`）：**NEAR=2 / MIDDLE=3 / FAR=4** ← 带名来源
* ★带 A/B/C 与 NEAR/MIDDLE/FAR 的对应是**推定**（csv22 枚举名 + 3 个同构块顺序）。
* 旧 schema 的 `col19` / `col22` 两处「gap」是**误判**：`sub_56E890` 连吃 csv18..22 共 5 列。

本脚本只改 schema；库/种子同步走 `_apply_batch7.py`。
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(os.path.dirname(HERE), "db_design", "schema", "cfg", "tables")
T = "AI_PARAM"
READER = "sub_56EA00"
WIDTH = 127

ARCHETYPE = ["NORMAL", "SHIELD", "UNDERWATER", "AMPHIBIAN", "SHOTGUN", "GATLINGGUN", "REPAIR",
             "SUPPORT", "CAMERAGUN", "CANNON", "SNIPER", "TANK", "AREA_AIRCRAFT", "AA_AIRCRAFT",
             "AAA", "BATTERY", "DEBRIS"]
MOBILITY = ["NORMAL", "LANDLUBBERLY", "UNDERWATER", "AMPHIBIAN", "TANK", "AIRCRAFT", "MINOVSKYCRAFT",
            "FIXED", "BROADWAYONLY"]
BAND = [("NEAR", 2), ("MIDDLE", 3), ("FAR", 4)]

NOTE7 = ("★2026-10-05 补列宽（第 7 批）：旧 schema 只声明 45 列（还误判 csv19/22 为 gap），"
         "`sub_56EA00` 实际为「固定头 csv0..17 + 距离带块 ×3（每块 25 列）+ 尾段」"
         "⇒ 声明到 **csv126（127 列）**，无缝列；列号/偏移逐条来自静态反汇编与共享子读函数展开。")


def col(idx: int, name: str, ctype: str, off, meaning: str, va: str, conf: str = "○ASM确证",
        extra: dict | None = None) -> dict:
    d = {
        "read_order": idx + 1, "csv_index": idx, "db_column": name, "name": name, "type": ctype,
        "memory_offset": off, "meaning": meaning, "display_name": name, "status": "confirmed",
        "confidence": conf, "asm_reader": READER, "asm_va": va,
    }
    if extra:
        d.update(extra)
    return d


cols: dict[int, dict] = {}

# ---- 固定头 0..17（沿用旧名，列位不变）
head = [
    ("ai_param_id", "u32", 0, "主键；AI 参数 ID（u32 @+0；★**本表索引键** = vtable[5] `sub_A564D0` 读 csv0）", "0x56ea45", "★确证", None),
    ("ai_archetype", "enum", 4, "NPC 战斗原型（@+4；`sub_56E570` 窄串→枚举，名表 `0xD77428`）", "0x56ea4e", "★确证",
     {"enum_converter": "sub_56E570", "enum_values": [{"name": n, "value": i + 1} for i, n in enumerate(ARCHETYPE)]}),
    ("mobility_class", "enum", 8, "地形/机动类别（@+8；`sub_56E610` 窄串→枚举，名表 `0xD77558`）", "0x56ea94", "★确证",
     {"enum_converter": "sub_56E610", "enum_values": [{"name": n, "value": i} for i, n in enumerate(MOBILITY)]}),
    ("custom_aim_cone", "bool", 44, "启用 CSV 照准角覆盖（csv3!=0→@+44；否则用机体默认锥）", "0x56eada", "★确证", None),
    ("aim_pitch_min_deg", "str_float", 12, "照准俯仰下限（CSV 度数×π/180 **取负** → @+12）", "0x56eaed", "★确证", None),
    ("aim_pitch_max_deg", "str_float", 16, "照准俯仰上限（度→弧度 @+16）", "0x56eafe", "★确证", None),
    ("aim_yaw_min_deg", "str_float", 20, "照准偏航下限（度→弧度 @+20）", "0x56eb0f", "★确证", None),
    ("aim_yaw_max_neg_deg", "str_float", 24, "照准偏航上限（度→弧度 **取负** @+24）", "0x56eb22", "★确证", None),
    ("aim_yaw_max_deg", "str_float", 28, "照准偏航上限（度→弧度 @+28）", "0x56eb33", "★确证", None),
    ("spread_timing_a", "float", 32, "集弾/散布计时系数 A（@+32）", "0x56eb44", "★确证", None),
    ("score_weight_x100", "u32", 36, "目标评分权重 ×100（csv10×100 → @+36）", "0x56eb55", None),
    ("warning_shot_range_deg", "str_float", 40, "警告射击阈值角（度→弧度 @+40；CSV <0 时写 `flt_D6D398`=FLT_MIN）",
     "0x56eb58", "★确证", None),
    ("use_default_spread", "bool", 520, "使用内置散布默认值（csv12→@+520 bit0）", "0x56eb98", None),
    ("move_wait_flag", "bool", 520, "移动-射击等待标志（csv13→@+520 bit2）", "0x56ebc1", None),
    ("burst_fire_flag", "bool", 520, "连射/点射行为标志（csv14→@+520 bit1）", "0x56ebe0", None),
    ("near_range_weight", "float", 76, "近距离段权重（atof → @+76）", "0x56ec0a", None),
    ("mid_range_weight", "float", 80, "中距离段权重（atof → @+80）", "0x56ec14", None),
    ("sniper_mode_flag", "bool", 520, "狙击/精密射击模式（csv17→@+520 bit3）", "0x56ec43", None),
]
for i, item in enumerate(head):
    name, ctype, off, mean, va, conf = item[:6]
    extra = item[6] if len(item) > 6 else None
    cols[i] = col(i, name, ctype, off, mean, va, conf or "○ASM确证", extra)

# ---- 距离带边界 + 选带枚举（sub_56E890 一次吃 5 列：csv18..22）
for i, va in enumerate(["0x56e8d3", "0x56e8e6", "0x56e8fa", "0x56e90e"]):
    cols[18 + i] = col(18 + i, f"band_edge_{i + 1}_x100", "u32", 84 + 4 * i,
                       f"距离带边界 {i + 1}（×100 存 @+{84 + 4 * i}；`sub_56E890` 另算 @+100/+104/+108/+112 = 各值平方，"
                       f"并按 csv22 选一对写 @+116(起)/@+120(止)/@+124(中点)）", va)
cols[22] = col(22, "band_select", "enum", 128,
               "选带枚举（@+128；`sub_56E6B0` 窄串→枚举，名表 `0xD775EC`）—— 决定 @+116/+120/+124 用哪一对边界",
               "0x56e92d", "★确证",
               {"enum_converter": "sub_56E6B0",
                "enum_values": [{"name": n, "value": v} for n, v in BAND]})

# ---- 三个同构距离带块；每块 = 25 列 = {3 u8, 22 float}，另加 1 个"块首 float"列（仅 NEAR 有）
#      NEAR: hdr csv23/24/25, pct[1..22] csv26..47, pct[0] csv48, extras csv49/50/51
#      MID : hdr csv52/53/54, pct[1..22] csv55..76,               extras csv77/78
#      FAR : hdr csv79/80/81, pct[1..22] csv82..103,              extras csv104/105
bands = [
    ("near", 23, 48, 51, "NEAR（推定）", 132, 136, 228, 3),
    ("mid", 52, None, 78, "MIDDLE（推定）", 240, 244, 340, 2),
    ("far", 79, None, 105, "FAR（推定）", 348, 352, 448, 2),
]
for tag, h0, lead, end, label, hoff, fbase, eoff, nextra in bands:
    for j in range(3):
        cols[h0 + j] = col(h0 + j, f"{tag}_hdr_{j + 1}", "u8", hoff + j,
                            f"{label} 带块 3 个字节参数之 {j + 1}（u8 @+{hoff + j}；"
                            f"`sub_56E220` 用 atoi 读、按字节存）", "0x56e22d")
    for j in range(1, 23):                       # 列序号
        idx = h0 + 3 + (j - 1)
        if idx == lead:                          # 插入 pct_01（NEAR 的 csv48）
            continue
        cols[idx] = col(idx, f"{tag}_pct_{j + 1:02d}", "float", fbase + 4 * j,
                        f"{label} 带权重数组下标 {j}（@+{fbase + 4 * j}；`sub_56E220` atof；"
                        f"整块 23 个 float 随后被 `sub_56E450` **归一化（和 = 1）**）", "0x56e273")
    if lead is not None:
        cols[lead] = col(lead, f"{tag}_pct_01", "float", fbase,
                         f"{label} 带权重数组下标 0（@+{fbase}；★**本列在块循环之外单独读**："
                         f"`v42[0] = atof(csv{lead})`；MIDDLE/FAR 两块此处是**常量 0，CSV 不读**）", "0x56ec7c")
    for j in range(nextra):
        idx = lead + 1 + j if lead is not None else end - nextra + 1 + j
        cols[idx] = col(idx, f"{tag}_extra_{j + 1}", "float", eoff + 4 * j,
                        f"{label} 带块尾随参数 {j + 1}（atof → @+{eoff + 4 * j}"
                        + ("；本项不乘 100" if j == 0 else "；×100") + "）", "0x56ecdc")

# ---- 尾段
tail = [
    (106, "weight4_1", "float", 456, "4 值权重组第 1 项（atof → @+456；`sub_56E510` 把 @+456..+468 **归一化，和 = 1**）"),
    (107, "weight4_2", "float", 460, "4 值权重组第 2 项（@+460）"),
    (108, "weight4_3", "float", 464, "4 值权重组第 3 项（@+464）"),
    (109, "weight4_4", "float", 468, "4 值权重组第 4 项（@+468）"),
    (110, "flag_bit4", "bool", 520, "开关位（csv110!=0 → @+520 bit4）"),
    (111, "flag_bit7", "bool", 520, "开关位（csv111!=0 → @+520 bit7）"),
    (112, "flag_bit5", "bool", 520, "开关位（csv112!=0 → @+520 bit5）"),
    (113, "flag_bit6", "bool", 520, "开关位（csv113!=0 → @+520 bit6）"),
    (114, "tail_f1", "float", 472, "尾段浮点 1（atof → @+472）"),
    (115, "tail_norm_1", "float", 476, "归一化三元组第 1 项（@+476；与 @+480、@+484 一起按三者和归一化）"),
    (116, "tail_norm_2", "float", 480, "归一化三元组第 2 项（@+480）"),
    (117, "tail_norm_3", "float", 484, "归一化三元组第 3 项（@+484）"),
    (118, "tail_f2", "float", 488, "尾段浮点 2（atof → @+488）"),
    (119, "tail_i1", "u32", 492, "尾段整数 1（atoi → @+492）"),
    (120, "tail_i2", "u32", 496, "尾段整数 2（atoi → @+496）"),
    (121, "tail_i3", "u32", 500, "尾段整数 3（atoi → @+500）"),
    (122, "tail_b1", "u8", 504, "尾段字节 1（`sub_56E3F0` atoi → 按 u8 存 @+504）"),
    (123, "tail_i4", "u32", 508, "尾段整数 4（`sub_56E3F0` atoi → @+508）"),
    (124, "tail_i5", "u32", 512, "尾段整数 5（`sub_56E3F0` atoi → @+512）"),
    (125, "tail_i6", "u32", 516, "尾段整数 6（`sub_56E3F0` atoi → @+516）"),
    (126, "tail_flag1", "bool", 521, "尾标志（csv126!=0 → @+521 bit0）"),
]
for idx, name, ctype, off, mean in tail:
    cols[idx] = col(idx, name, ctype, off, mean, "0x56f039" if idx == 126 else "0x56ee5b")

assert sorted(cols) == list(range(WIDTH)), sorted(cols)
columns = [cols[i] for i in range(WIDTH)]

path = os.path.join(TABLES, T + ".json")
d = json.load(open(path, encoding="utf-8"))
d["columns"] = columns
d["column_count"] = WIDTH
d["column_defined"] = WIDTH
d["column_confirmed"] = WIDTH
d["column_partial"] = 0
d["column_pending"] = 0
d["column_gap"] = 0
d["asm_status"] = "complete"
d["asm_reader"] = READER
d["reader_max_csv_index"] = 126
d["column_gap_note"] = "CSV 行含 col0..col126；无缝列（连续读；旧 schema 的 csv19/22 两个 gap 是误判）"
d["columns_note"] = NOTE7
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(path, "a", encoding="utf-8").write("\n")
print(f"{T}: {WIDTH} 列 全读（reader_max=csv126）")
print("  带块 NEAR csv23..48(+49..51) / MIDDLE csv52..76(+77..78) / FAR csv79..103(+104..105)")
