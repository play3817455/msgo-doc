# -*- coding: utf-8 -*-
"""第 7 批（2026-10-05）：`MISSION_XWAR_BANPICK` 行宽 4 → 43，列语义按 **静态反汇编** 订正。

依据（IDA 逐字反汇编，可复查）：

* `sub_5A0300` @`0x5A0300`（`CMissionXwarBanPickTable::ParseRow`，类名/RTTI 由
  `??_7CMissionXwarBanPickTable@@6B@`@`0xecf274` 与 vtable[5] = `sub_A564D0` 交叉确证）：

```c
*a3      = sub_BBB370(a1, 0);        // csv0 → +0
a3[1]    = sub_BBB370(a1, 1);        // csv1 → +4
a3[2]    = sub_BBB370(a1, 2);        // csv2 → +8   ← ★条数
if (a3[2] > 40) a3[2] = 40;          // ★硬上限 40
for (v4 = 0; v4 < a3[2]; ++v4)
    a3[3 + v4] = sub_BBB370(a1, v4 + 3);   // csv{3..} → +12 + 4k
```

* ★**本表读列数随数据变化**：真读 `3 + min(csv2, 40)` 列 ⇒ **最大列号 csv42**（43 列）。
  仿真（Unicorn，种子 csv2 ≥ 40）实测读到 **csv0..csv42 连续 43 列，无缝列**。
* 结构 = `rule_id` + `mode` + `count`(≤40) + **40 个机体 ID 槽**（内存密集 dword 数组 @+12）。
* `sub_BBB370` = **atoi**（整数）。
* ★**索引键 = csv0**：vtable[5] = `sub_A564D0`（`return sub_BBB370(a1, 0)`）。
* 旧 schema 名 `pick_count`（csv2）/ `ban_ms_id`（csv3）保留语义但订正列位：
  csv2 是**条数**（不是"可选机体数"），csv3 起是 **40 槽机体 ID 列表**。

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
T = "MISSION_XWAR_BANPICK"
READER = "sub_5A0300"
SLOTS = 40

NOTE7 = ("★2026-10-05 补列宽（第 7 批）：旧 schema 只声明 4 列，`sub_5A0300` 为"
         "「3 前导 + csv2 条数个 ID 槽（硬上限 40）」的可变长循环 ⇒ 声明到 **csv42（43 列）**；"
         "★注意**本表真读列数随 csv2 取值变化**（3 + min(csv2,40)），43 列是上限。")


def col(idx: int, name: str, ctype: str, off, meaning: str, disp: str, va: str,
        conf: str = "○ASM确证") -> dict:
    return {
        "read_order": idx + 1, "csv_index": idx, "db_column": name, "name": name, "type": ctype,
        "memory_offset": off, "meaning": meaning, "display_name": disp, "status": "confirmed",
        "confidence": conf, "asm_reader": READER, "asm_va": va,
    }


cols = [
    col(0, "rule_id", "u32", 0,
        "主键；XWAR Ban/Pick 规则 ID（u32 @+0；★**本表索引键** = vtable[5] `sub_A564D0` 读 csv0）",
        "规则 ID", "0x5a030a", "★确证"),
    col(1, "banpick_mode", "u32", 4, "Ban/Pick 模式（u32 @+4）", "模式", "0x5a0318"),
    col(2, "ban_ms_count", "u32", 8,
        "★机体 ID 条数（u32 @+8；**硬上限 40** —— 超过则按 40 截断，循环次数即此值）",
        "条数", "0x5a0323", "★确证"),
]
for k in range(1, SLOTS + 1):
    cols.append(col(2 + k, f"ban_ms_id_{k}", "u32", 12 + 4 * (k - 1),
                    f"Ban 机体 ID 槽 {k}（u32 @+{12 + 4 * (k - 1)}；仅当 csv2 ≥ {k} 时才被读取，"
                    f"否则 +{12 + 4 * (k - 1)} 保持 0）",
                    f"Ban 机体{k}", "0x5a034a"))

assert len(cols) == 43, len(cols)
path = os.path.join(TABLES, T + ".json")
d = json.load(open(path, encoding="utf-8"))
d["columns"] = cols
d["column_count"] = len(cols)
d["column_defined"] = len(cols)
d["column_confirmed"] = len(cols)
d["column_partial"] = 0
d["column_pending"] = 0
d["column_gap"] = 0
d["asm_status"] = "complete"
d["asm_reader"] = READER
d["reader_max_csv_index"] = 42
d["column_gap_note"] = "CSV 行含 col0..col42；无缝列（连续读），但**实际读几列由 csv2 决定**（≤40）"
d["columns_note"] = NOTE7
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(path, "a", encoding="utf-8").write("\n")
print(f"{T}: {len(cols)} 列 全读（reader_max=csv42，条数上限 40）")
