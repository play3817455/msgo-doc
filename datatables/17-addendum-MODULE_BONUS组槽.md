
---

# 附录 F｜第 6 批订正：`MODULE_BONUS` 的「8 组 × {A,B,V}」行宽 · 6 → 41 列（2026-10-05）

> 本附录由 `datatables/17-addendum-MODULE_BONUS组槽.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。
> 脚本：`datatables/_fix_module_bonus.py`（改 schema）→ `merge_cfg_asm.py`（GM 侧）→
> `_apply_module_bonus.py`（库 `RENAME COLUMN`/`ADD COLUMN` + 种子补宽）→
> `cfgsync -export-only`（重拼 manifest，**不加 `-bootstrap-csv`** ⇒ 不碰 `header_text`）→
> `_normalize_cfg_nulls.py`（全库 `NULL → ''` 复核，本批 0 列）→
> `_verify_module_bonus.py`（验收）。基线快照在 `datatables/_rollback/20261005-231713_module_bonus/`。

## F.0 结论一览

| 项 | 旧 | 订正 | 依据 |
|---|---|---|---|
| 行宽 | schema 6 段 / 注释 4 列（**只声明了循环第 1 组**） | **41 列** = 1 键列 + **8 组 × {A,B,V}**（列步长 5，16 个缝列） | `sub_5A29B0` @`0x5A29B0` |
| 列名 | `stat_id_a` / `stat_id_b` / `stat_value`（钉在 csv2/4/5，像是"整表只有一组"） | `stat_id_a/b/value` → **原位**改名 `group1_stat_id_a/b/value`，组 2..8 同构命名 + 16 个 `colN` 缝列 | 同上 |
| 类型 | 记 u32（对） | u32（对，但补上证据：`sub_BBB370` = **atoi**，本表无 atof/enum） | `sub_CC6865`/`sub_CC772B(_,0,10)` |
| ★键列 | 注释把「加成组 ID」记在 csv1（**对**），但种子的行号写在 **csv0**（reader 不读） | 文档明确：**键在 csv1**，写行时组 ID 必须落在 csv1 | vtable[5] = `sub_5A2A10`（`sub_BBB370(a1,1)`） |
| 库/种子 | 6 列 / 2 段 | **41 列 / 41 段**（64 行未丢） | `_apply_module_bonus.py` |
| §2 偏窄清单 | 4 张 | **3 张**（`AI_PARAM` / `MISSION_XWAR_BANPICK` / `COMMANDER_NPC`） | `_sweep_width_db.py` |

## F.1 旧注释为什么只对了 4 列：它把「循环体」当成了「表结构」

```c
// sub_5A29B0  逐条反编译
*a3 = sub_BBB370(a1, 1);            // csv1 → +0   （csv0 全函数不读）
v4 = a3 + 2;  v5 = 8;
do {
    *(v4 - 1) = sub_BBB370(a1, v3);      // csv(v3)     → +4  + 12k
    v7 = v3 + 2;
    *v4       = sub_BBB370(a1, v7++);    // csv(v3+2)   → +8  + 12k
    v4[1]     = sub_BBB370(a1, v7);      // csv(v3+3)   → +12 + 12k
    v3 = v7 + 2;                         // ← 列步长 5（组内多一个缝 + 组间一个缝）
    v4 += 3;  --v5;
} while (v5);
```

- 旧注释在这张表上**只采了循环的第 1 轮**（csv2/4/5），于是 6 段 schema 就"看着自洽"了 ——
  但客户端每行**稳定读 25 列**（`_out_sweep_verdict` 的仿真读集就是
  `1, 2, 4, 5, 7, 9, 10, 12, 14, 15, 17, 19, 20, 22, 24, 25, …, 37, 39, 40`，
  正好 8 轮 × {5k-3, 5k-1, 5k}），旧下发行宽 6 段 ⇒ **csv6..csv40 恒为 0**。
- 与第 4/5 批同型（`BEGINNER_CHALLENGE` / `CHALLENGE_HIGHSCORE` / `ITEM_PART`）：**固定块循环**。
  本次 8 轮**列步长恒定 5**（不像 `ITEM_PART` 会随参数名变宽）⇒ 宽度是**定值 41**，不存在"最坏情况"余量问题。

## F.2 三项槽（A / B / V）的语义证据链 —— 只到 "A" 这一层

| 项 | 语义（证据） |
|---|---|
| **A** | ★**定义 ID，且 `A > 0` 才算该槽有效**：<br>1) `sub_5A2A30(table, group_id)` 把 `v3[5]/v3[8]/…/v3[26]` 逐个与 0 比较并计数（返回"有效槽数"）；<br>2) `sub_5A2AF0(table, group_id, slot)` 返回 `v4[3*slot+5]`（即该槽的 A）；<br>3) `sub_7C09B0` / `sub_7BF480` 拿到 A 后到 `dword_11E3F08` 名表里查**名字串**再拼显示文本。 |
| **B** | ⚠️ **未取证**：只确证 `reader` 会读满（`sub_BBB370(a1, v7)` 在结构 +8+12k）——**消费点未找到**。命名沿旧名 `stat_id_b`。 |
| **V** | ⚠️ **未取证**（沿旧名 `stat_value`）；但已确证读法是 **atoi 整数**（不是 `atof`）⇒ 写整数。 |

> ★这张表**没有**枚举转换函数（不像 `ITEM_PART` 组内用 `sub_5952C0`/`sub_5953B0` 两张 32/129 值枚举表），
> 三项都是纯 `atoi` ⇒ **不要求写枚举名**，写十进制整数即可。

## F.3 ★一个比行宽更要紧的发现：**索引键在 csv1，不在 csv0**

- `CModuleBonusTable` vtable[5] = `sub_5A2A10`，函数体就是 `return sub_BBB370(a1, 1);` ⇒ **GetKey 读 csv1**；
- `sub_5A2AF0` 的树查找条件是 `v4[4] == a2`，而 `v4` 是树节点、`v4[4]` 正好是行的 `+0` dword（=csv1）⇒ 键一致；
- 我们的 `module_bonus.csv` 种子沿用「字段 0 = 行号」的占位约定（`1,`…`64,`），
  这些行号**落在 csv0** ⇒ 客户端按 csv1 取键时拿到的是**空键(=0)**。
- 本批**不动数据**（保持"取值逐格未变"这条验收红线），只在**注释/种子头部注记**里写清：
  以后填真实数据时，**组 ID 写 csv1**。
- 影响面：占位行全空 + 键恒 0 ⇒ 客户端 `sub_5A2A30` 计到的有效槽数为 0，行为上等价于"空表"（与其余占位表一致），
  **不是**本批引入的偏差。

## F.4 库侧动作

| 处 | 动作 |
|---|---|
| 库 | `RENAME COLUMN` 3 个：`stat_id_a→group1_stat_id_a`、`stat_id_b→group1_stat_id_b`、`stat_value→group1_stat_value`（**位置不变、数据不搬**）；`ADD COLUMN IF NOT EXISTS` 追加 35 列（`group2_*`…`group8_*` + 16 个 `colN` 缝列），新列 **2240 格 `NULL → ''`**（= 35 列 × 64 行）；**未走 `-recreate`** |
| 种子 | `server/datafiles/lounge/module/module_bonus.csv` 行宽 6 → **41 段**（64 行）+ 一行布局/键列注记；原文件备份 `datatables/_backup_seeds/` |
| 下发 | `cfgsync -export-only` ⇒ `meta.cfg_manifest.raw_csv` 1016 → **3256 字节**（`header_text` 未动，无需 `_manifest_restore.py`） |
| GM / 站点 | `merge_cfg_asm.py`（80 张）+ `build_cfg_site.py`（80 页）重生 |

## F.5 验收（`_verify_module_bonus.py`，全绿）

| 检查 | 结果 |
|---|---|
| 全库列漂移（A 类） | **0** |
| 列序 == schema 列序 / `reader_max_csv_index` == 列数−1 | 41/41 ✓ / 40 ✓ |
| 缝列集合 == ASM 推定 | **16 个全等** ✓（`0,3,6,8,11,13,16,18,21,23,26,28,31,33,36,38`） |
| 结构断言（csv↔物理位置↔内存 `+4+12k/+8+12k/+12+12k`） | **0 违例** ✓ |
| manifest 每行字段数 == 库列数 | 段数分布 **`[41]`**（单值）✓ |
| 原列取值**按位置**逐格比对（改前全部 **7** 个物理列 × 64 行） | **448 格差异 0** ✓ |
| 行数 / 新列 NULL | 64 → 64 ✓ / **0** ✓ |
| 其余表 | `_manifest_snapshot.py diff`：`added [] / removed []`，`changed` 的 4 张 = 第 4 批 2 张 + 第 5 批 1 张 + 本表 ✓ |
| §2 偏窄清单 | **4 → 3** |

## F.6 遗留

- `groupN_stat_id_b` / `groupN_stat_value` 的**业务语义仍未取证**（A 已到"定义 ID + >0 有效"这一层）。
  取证入口：`sub_7C09B0` 的上层（模块 UI 显示）与 `dword_11E3F08` 名表的定义方。
- 种子的**行号占位在 csv0**（客户端不读）—— 是否改成"把组 ID 写到 csv1"属于**数据口径决策**，
  本批只记不裁（见 F.3）。
- §2 剩余 **3** 张偏窄表：`AI_PARAM`（缺 82）/ `MISSION_XWAR_BANPICK`（39）/ `COMMANDER_NPC`（37）
  —— 均为**固定块循环**型，逐表按 reader 的循环层数/步长反推出组结构后再补。
