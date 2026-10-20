# -*- coding: utf-8 -*-
"""第 7 批（2026-10-05）：`COMMANDER_NPC` 行宽 13 → 50，列语义/偏移按 **静态反汇编** 订正。

依据（IDA 逐字反汇编，可复查）：

* `sub_572EE0` @`0x572EE0`（`CCommanderNpcTable::ParseRow`，类名/RTTI 由
  `??_7CCommanderNpcTable@@6B@`@`0xecffe8` 与 ctor `sub_A77960`@`0xA77960`
  —— `*this = &TIndexTable<COMMANDERNPC_DATA>::vftable` —— 交叉确证）：

```c
*(_DWORD*)a3 = sub_BBB370(a1, 0);            // csv0  → +0   键（GetKey 同读 csv0）
*(_DWORD*)(a3+4)  = sub_BBB370(a1, 1);       // csv1  → +4
*(_DWORD*)(a3+8)  = sub_BBB370(a1, 2);       // csv2  → +8
sub_4029E0(a3+12, sub_456D90(a1, 3));        // csv3  → +12  wstring
sub_4029E0(a3+40, sub_456D90(a1, 4));        // csv4  → +40  wstring
*(_DWORD*)(a3+68) = sub_572C30(sub_BBB4F0(a1, 5));  // csv5 → +68  势力 enum
*(_DWORD*)(a3+72) = sub_BBB370(a1, 6);       // csv6  → +72
*(_WORD*)(a3+88)  = sub_BBB370(a1, 0xC);     // csv12 → +88  u16
v10 = 13; v11 = a3+92 (u16*); v30 = a3+220 (dword*); n = 3;
do {                                          // 组 k = 1..3
    *v11 = sub_BBB370(a1, v10);               // csv{5k+8}  → +88+2k   u16
    *v30 = sub_BBB370(a1, v10+1);             // csv{5k+9}  → +220+4k  u32
    v10 += 5; ++v11; ++v30;
} while (--n);                                // ⇒ 消耗 csv13/14, 17/18, 21/22
v15 = a3+304 (dword*); n = 12;
do {                                          // 支援槽 k = 1..12
    *(v15-12) = sub_BBB370(a1, v10);           // csv{2k+23} → +256+4(k-1)  u32 原始值
    *v15      = sub_572CD0(sub_BBB4F0(a1, v10+1)); // csv{2k+24} → +304+4(k-1) 枚举（名字串）
    v10 += 2; ++v15;
} while (--n);                                // ⇒ 消耗 csv25..48
*(_DWORD*)(a3+80) = sub_BBB370(a1, v10);     // csv49 → +80
// 之后 12 个枚举值按 switch(*result) 折成 31 位掩码写 +76（bit = 枚举值 0..30）
```

* 结构：**7 个前导列** + **4 槽消耗（u16）+ 3 槽冷却（u32）**（列步长 5，csv12/13/14、17/18、21/22）
  + **12 组 × {原始值 u32, 类型名（enum）}**（csv25..48，列步长 2）+ **1 尾列**（csv49）
  ⇒ 读到 **csv49**，行宽 **50**；其中 **11 列是缝**（csv 7,8,9,10,11 / 15,16 / 19,20 / 23,24）。
* `sub_BBB370` = **atoi**（整数）；`sub_456D90` = **wstring 取列**；`sub_BBB4F0` = **窄串取列**。
* 枚举表（本脚本从 IDA 逐字读出）：
  - csv5 势力（`sub_572C30` 查 `0xD78084` 名表 / `0xD78088` 值表）：`NEUTRAL=-1, EFF=0, ZEON=1`
  - csv26/28/…/48 支援类型（`sub_572CD0` 查 `0xD780B0`/`0xD780B4`）：31 个名字 → 0..30
* ★**索引键 = csv0**：vtable[5] = `sub_A564D0`（`return sub_BBB370(a1, 0)`）即 GetKey 读 csv0。
* 行回调 `sub_A74EF0`（TIndexTable 通用行处理）自证链路：
  `v6 = GetKey(row)` → `sub_A74970(rec)` 初始化 → `vtable[0](table, row, v6, rec)` 填行 → `vtable[3]` 插索引；
  且 `*v5 == '#'` 的行当注释跳过（csv0 以宽串比较首字符）。记录缓冲 **720B**。

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
T = "COMMANDER_NPC"
READER = "sub_572EE0"
GAPS = [7, 8, 9, 10, 11, 15, 16, 19, 20, 23, 24]
SUPPORT_ENUM = ["BOMB", "CARPET_BOMB", "TENDER", "SEARCH", "MINOVSKY", "SOLAR_RAY", "SUMMON_MA",
                "SUMMON_ACE", "BATTLE_SHIP", "ASSAULT_SHIP", "ORATION", "PATROL_AIRCRAFT", "AAG",
                "GUNTURRET", "EQPARTS_EXEC_A", "EQPARTS_EXEC_B", "EQPARTS_EXEC_C", "EQPARTS_EXEC_D",
                "EQPARTS_EXEC_E", "GRENADE_NET", "GRENADE_TUMBLE", "WALL", "DUMMY_BEACON",
                "TRANSPORT_SHIP", "STGARMS_OLD", "STGARMS1", "STGARMS2", "SUBFLIGHT",
                "ASSAULT_STGHOLD", "RIDE_ACE", "JAMMING"]
FACTION_ENUM = [("NEUTRAL", -1), ("EFF", 0), ("ZEON", 1)]

NOTE7 = ("★2026-10-05 补列宽（第 7 批）：旧 schema 只声明 13 列且 csv_index 与真读列不符，"
         "`sub_572EE0` 实为「7 前导 + 4 槽消耗 + 3 槽冷却 + 12 组 ×{原始值,类型名} + 1 尾列」"
         "（含 4 组空列缝）⇒ 声明到 **csv49（50 列）**；列号/偏移逐条来自静态反汇编。")


def gap(idx: int) -> dict:
    return {
        "read_order": idx + 1, "csv_index": idx, "db_column": f"col{idx}", "name": f"col{idx}",
        "type": "u32", "memory_offset": None,
        "meaning": f"★gap：`{READER}` 全函数不读 csv{idx}（槽组间 1 列缝 / 组内 1 列缝）⇒ 纯占位列",
        "display_name": f"占位 col{idx}", "status": "gap", "confidence": "",
        "asm_reader": None, "asm_va": None,
    }


def col(idx: int, name: str, ctype: str, off, meaning: str, disp: str, va: str,
        conf: str = "○ASM确证", extra: dict | None = None) -> dict:
    d = {
        "read_order": idx + 1, "csv_index": idx, "db_column": name, "name": name, "type": ctype,
        "memory_offset": off, "meaning": meaning, "display_name": disp, "status": "confirmed",
        "confidence": conf, "asm_reader": READER, "asm_va": va,
    }
    if extra:
        d.update(extra)
    return d


cols: dict[int, dict] = {}
cols[0] = col(0, "commander_id", "u32", 0,
              "主键；指挥官 ID（u32 @+0；★**本表索引键** = vtable[5] `sub_A564D0` 读的就是 csv0）",
              "指挥官 ID", "0x572f0e", "★确证")
cols[1] = col(1, "npc_model_id", "u32", 4, "NPC 模型 ID（u32 @+4；关联 chara 资源）",
              "NPC 模型 ID", "0x572f1c")
cols[2] = col(2, "portrait_id", "u32", 8, "头像/立绘 ID（u32 @+8）", "头像 ID", "0x572f27")
cols[3] = col(3, "commander_name", "str", 12, "指挥官名称（wstring @+12；`sub_456D90` 取列）",
              "指挥官名", "0x572f3b")
cols[4] = col(4, "description", "str", 40, "指挥官说明（wstring @+40；`sub_456D90` 取列）",
              "说明", "0x572f7c")
cols[5] = col(5, "faction", "enum", 68,
              "势力（@+68；`sub_572C30` 窄串→枚举，名表 `0xD78084`）",
              "势力", "0x572fb4", "★确证", {"enum_converter": "sub_572C30",
                                        "enum_values": [{"name": n, "value": v} for n, v in FACTION_ENUM]})
cols[6] = col(6, "voice_group_id", "u32", 72,
              "语音组 ID（u32 @+72；cutin_voice_*_commander.csv）", "语音组 ID", "0x572fe8")
for g in GAPS:
    cols[g] = gap(g)

cols[12] = col(12, "slot1_cost", "u16", 88, "支援槽 1 消耗（u16 @+88；列步长 5 的第 1 槽）",
               "槽1 消耗", "0x573000")
cols[13] = col(13, "slot2_cost", "u16", 92, "支援槽 2 消耗（u16 @+92）", "槽2 消耗", "0x573027")
cols[14] = col(14, "slot1_cooldown", "u32", 220, "支援槽 1 冷却（u32 @+220；循环第 1 轮第 2 项）",
               "槽1 冷却", "0x573034")
cols[17] = col(17, "slot3_cost", "u16", 94, "支援槽 3 消耗（u16 @+94）", "槽3 消耗", "0x573027")
cols[18] = col(18, "slot2_cooldown", "u32", 224, "支援槽 2 冷却（u32 @+224）", "槽2 冷却", "0x573034")
cols[21] = col(21, "slot4_cost", "u16", 96, "支援槽 4 消耗（u16 @+96；★只有 3 个冷却，本槽无冷却列）",
               "槽4 消耗", "0x573027")
cols[22] = col(22, "slot3_cooldown", "u32", 228, "支援槽 3 冷却（u32 @+228）", "槽3 冷却", "0x573034")

for k in range(1, 13):
    vcol, tcol = 2 * k + 23, 2 * k + 24          # csv25/26, 27/28, … 47/48
    cols[vcol] = col(vcol, f"support{k}_value", "u32", 256 + 4 * (k - 1),
                     f"支援槽 {k} 原始整数值（u32 @+{256 + 4 * (k - 1)}；`sub_BBB370` = atoi；语义未取证）",
                     f"槽{k} 值", "0x573066")
    cols[tcol] = col(tcol, f"support{k}_type", "enum", 304 + 4 * (k - 1),
                     f"支援槽 {k} 类型（@+{304 + 4 * (k - 1)}；`sub_572CD0` 窄串→枚举；"
                     f"12 个值随后按 switch 折成 31 位掩码写 @+76）",
                     f"槽{k} 类型", "0x573078", "★确证",
                     {"enum_converter": "sub_572CD0",
                      "enum_values": [{"name": n, "value": i} for i, n in enumerate(SUPPORT_ENUM)]})

cols[49] = col(49, "unlock_mission_id", "u32", 80,
               "解锁任务 ID（u32 @+80；12 组循环后紧接读取）", "解锁任务 ID", "0x5730dc")

assert sorted(cols) == list(range(50)), sorted(cols)
columns = [cols[i] for i in range(50)]
gap_idx = [c["csv_index"] for c in columns if c["status"] == "gap"]
assert gap_idx == GAPS, gap_idx

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
d["reader_max_csv_index"] = 49
d["column_gap_note"] = (f"CSV 行含 col0..col49；csv {', '.join(map(str, gap_idx))} reader 不读（占位）："
                        "前导 7 列后的 5 列、槽组间 1 列（15/16、19/20）、12 组前的 2 列（23/24）")
d["columns_note"] = NOTE7
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(path, "a", encoding="utf-8").write("\n")
print(f"{T}: {len(columns)} 列（读 {d['column_confirmed']} / 缝 {d['column_gap']}，reader_max=csv49）")
print("  缝列:", gap_idx)
print("  槽（cost 列 / cd 列）:", {1: (12, 14), 2: (13, 18), 3: (17, 22), 4: (21, None)})
