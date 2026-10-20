# -*- coding: utf-8 -*-
"""生成 `datatables/01-列注释/42-42-AI_PARAM.md`（第 7 批 127 列版）。

列位/类型/内存偏移/语义**全部**取自 `db_design/schema/cfg/tables/AI_PARAM.json`（该文件由
`_fix_ai_param.py` 依据 `sub_56EA00` 静态反汇编生成），避免手工转录错位。
"""
from __future__ import annotations

import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCHEMA = os.path.join(ROOT, "db_design", "schema", "cfg", "tables", "AI_PARAM.json")
OUT = os.path.join(HERE, "01-列注释", "42-42-AI_PARAM.md")

d = json.load(open(SCHEMA, encoding="utf-8"))
cols = d["columns"]
assert len(cols) == 127, len(cols)

HEAD = """# AI_PARAM ｜ `npc/ai_param.csv`

- **用途**：NPC AI 参数
- 表ID `42` ｜ 下载序 `42` ｜ 类名 `CAIParam` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_56EA00` @`0x56EA00`（RTTI `??_7CAIParam@@6B@`@`0xecf1b0`、ctor `sub_A5B8E0`@`0xA5B8E0`）｜ **列数 127**
- ★2026-10-05 第 7 批订正：旧 schema 只声明 **45 列**，且把 `csv19` / `csv22` 误判成 gap
  （真正原因是列号游标 `v36` **按引用**传给共享子读函数 `sub_56E890`/`sub_56E220`/`sub_56E3F0`，
  静态扫主函数看不到子函数内部的 `(*a4)++`）⇒ 改为 **127 列**（`csv0..csv126`，**无缝列**）

## 1. 行布局（`sub_56EA00` + 共享子读函数逐个展开）

```c
csv0     → +0     atoi                      // 键
csv1     → +4     sub_56E570(窄串)           // enum 17 值
csv2     → +8     sub_56E610(窄串)           // enum  9 值
csv3     → +44    atoi != 0                 // bool（u8）
csv4..9  → +12/+16/+20/+24/+28/+32           // atof × π/180（csv4/csv7 取负）
csv10    → +36    100 * atoi
csv11    → +40    atof × π/180（< 0 时写 FLT_MIN）
csv12 → +520 bit0    csv13 → +520 bit2    csv14 → +520 bit1
csv15 → +76  atof    csv16 → +80  atof
v36 = 18;
csv17 → +520 bit3
sub_56E890(a3+84, a1, &v36)                  // ★吃 5 列：csv18..22
csv23..47  sub_56E220(&v34, v42, a1, &v36)   // ★吃 25 列 → 带 A（NEAR）
csv48      v42[0] = atof                     // ★带 A 独有的"块首 float"，不在子函数循环内
csv49..51  → +228 / +232 / +236              // 后两个 ×100
csv52..76  sub_56E220(…)                     // ★吃 25 列 → 带 B（MIDDLE），v42[0] = 0
csv77..78  → +340 / +344                     // ×100
csv79..103 sub_56E220(…)                     // ★吃 25 列 → 带 C（FAR），v42[0] = 0
csv104..105 → +448 / +452                    // ×100
csv106..109 → +456/+460/+464/+468            // `sub_56E510` 把 4 值归一化（和 = 1）
csv110..113 → +520 bit4 / bit7 / bit5 / bit6
csv114..118 → +472 / +476 / +480 / +484 / +488   // +476/+480/+484 三元组归一化
csv119..121 → +492 / +496 / +500
csv122..125 sub_56E3F0(a3+504, a1, &v36)     // ★吃 4 列 → +504(u8)/+508/+512/+516
csv126     → +521 bit0
```

- 三个**同构距离带块**由 `sub_56E220` 读，每块 **25 列** = `{3 个 u8（atoi）, 22 个 float（atof）}`；
  块内 23 个 float 随后被 `sub_56E450` **归一化（和 = 1）**。
- ★**带 A/B/C ↔ NEAR/MIDDLE/FAR 的对应是"推定"**：依据 `csv22` 的 `sub_56E6B0` 枚举名
  （`NEAR=2 / MIDDLE=3 / FAR=4`）与 3 个同构块的顺序（带 A 独有块首 float，Mid/Far 该处为常量 0）。
- 枚举表（从 IDA 逐字读出）：
  - `csv1` `sub_56E570`（名表 `0xD77428`）：`NORMAL=1` … `DEBRIS=17`（17 值）
  - `csv2` `sub_56E610`（名表 `0xD77558`）：`NORMAL=0` … `BROADWAYONLY=8`（9 值）
  - `csv22` `sub_56E6B0`（名表 `0xD775EC`）：`NEAR=2 / MIDDLE=3 / FAR=4`
- ★**本表索引键 = csv0**：vtable[5] = `sub_A564D0`（`return sub_BBB370(a1, 0)`）。

## 2. 列位总表（127 列；`sub_56EA00` 全读，无缝列）

| CSV# | 订案名 | 类型 | 内存 | 语义 |
|---|---|---|---|---|
"""

L = [HEAD.rstrip("\n")]
for c in cols:
    off = c.get("memory_offset")
    off = "" if off is None else (f"+{off}" if isinstance(off, int) else str(off))
    mean = (c.get("meaning") or "").replace("|", "\\|").replace("\n", " ")
    L.append(f'| `{c["csv_index"]}` | `{c["db_column"]}` | {c["type"]} | {off} | {mean} |')

L.append("""
## 3. 分段落速查

| 段 | CSV# | 内容 |
|---|---|---|
| 固定头 | `0`..`17` | 键 / 原型 / 机动类别 / 照准锥 / 散布 / 位标志（`@+520`、`@+521` 两组位图） |
| 带边界 + 选带 | `18`..`22` | 4 个边界（×100 存，另算平方与起/止/中点）+ `band_select` 枚举 |
| NEAR 带块（推定） | `23`..`51` | 3 个 u8 头 + 23 个归一化 float（下标 1..22 在循环内、下标 0 = `csv48`）+ 3 个尾随参数 |
| MIDDLE 带块（推定） | `52`..`78` | 同上但**无块首 float**（`v42[0]` 常量 0）；尾随参数 2 个 |
| FAR 带块（推定） | `79`..`105` | 同上；尾随参数 2 个 |
| 尾段 | `106`..`126` | 4 值归一化权重 / 4 个位标志 / 尾浮点与三元组归一化 / 6 个整数 / 1 位标志 |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 行宽 **127 段**（`csv0..csv126`），**无缝列**——每一格都有 reader 对应。
- 枚举列（`csv1` `csv2` `csv22`）写**名称字符串**；角度列（`csv4..8`、`csv11`）写**度数**（reader 内部转弧度）。
- 归一化数组（带块 23 float、`csv106..109`、`csv116..118`）**写相对权重即可**，reader 会自行归一到和为 1。
- 位标志列（`csv12..14/17/110..113/126`）写**非 0 = 置位**（`0` 或留空 = 不置位）。
""")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("wrote", os.path.relpath(OUT, ROOT), f"({len(cols)} 列)")
