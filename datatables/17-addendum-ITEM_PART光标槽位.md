
---

# 附录 E｜第 5 批订正：`ITEM_PART` 的「光标式」行宽 · 21 → 50 列（2026-10-05）

> 本附录由 `datatables/17-addendum-ITEM_PART光标槽位.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。
> 脚本：`datatables/_fix_item_part.py`（改 schema）→ `merge_cfg_asm.py`（GM 侧）→
> `_apply_item_part.py`（库 `RENAME COLUMN`/`ADD COLUMN` + 种子补宽）→
> `cfgsync -export-only`（重拼 manifest，**不加 `-bootstrap-csv`** ⇒ 不碰 `header_text`）→
> `_verify_item_part.py`（验收）。基线快照在 `datatables/_rollback/20261005-230106_item_part/`。

## E.0 结论一览

| 项 | 旧 | 订正 | 依据 |
|---|---|---|---|
| 行宽 | 21 列（注释记 23；把「8 组循环」当成**单组**，尾列钉在 csv19/20） | **50 列** = 16 前导 + 8 组×3 + 2 尾（常态 42）+ **8 余量**（109 组才用） | `sub_5955A0` @`0x5955A0` |
| 列名 | `effect_scope/stat_name/loop_param_value/priority/stack_rule` 钉在 csv16..20 | 前 3 个 → `group1_scope/group1_stat/group1_value`；后 2 个 → `group2_scope/group2_stat`（**位置不变**）+ 27 个新列 | 同上 |
| 库/种子 | 21 列 / 21 段 | 50 列 / 50 段（64 行未丢） | `_apply_item_part.py` |
| §2 偏窄清单 | 5 张 | **4 张**（`AI_PARAM` / `MISSION_XWAR_BANPICK` / `COMMANDER_NPC` / `MODULE_BONUS`） | `_sweep_width_db.py` |

## E.1 为什么旧注释"看着对、其实错"：这张表是**光标式**，不是**定长式**

旧注释的 21 列里，csv0..csv15 **逐个都对**（4 条枚举换算函数 `sub_5954A0` / `sub_5951D0` /
`sub_5952C0` / `sub_5953B0` 也都认对了），错的是**结构**：它把 `sub_5955A0` 的

```c
v6 = 16;  do 8 次 { 作用对象=col(v6); 参数名=col(v6+1); 值=col(v6+2); v6 += 3; }
```

当成了"只读一组"（csv16/17/18），于是把 8 组压成 1 组、再把尾部 2 个 u32 钉在 csv19/20。
真实情况是 **8 组顺序消费 CSV**，且**每组的列数可变**：

```c
e = sub_5953B0(col v6+1);                       // 参数名
if (e == 109 /* MS_BOOST_GAUGE_RECOV */) {      // ★该组多占 1 列
    v6 += 4; 值 = atoi(col v6+2) + 64 * atoi(col v6+3);
} else {
    v6 += 3; 值 = atof(col v6+2);
}
```

旧注释其实**瞥见过**这个分支（它把 csv18/csv19 记成 `key_action_a/b`、"numeric str →
`sub_CC6CA8`/strtol"）—— 只是没把它理解成「同一个组的第 3、4 列」。

## E.2 宽度该定多少：**50**（最坏情况），不是 42

| 布局 | 宽度 | 谁会走 |
|---|---|---|
| 常态（无 109 组） | 16 + 8×3 + 2 = **42** | 本表当前 64 行（全空）；旧 21 列注释也对应这个形态的"截断版" |
| 最坏（8 组全 109） | 16 + 8×4 + 2 = **50** | 真实数据里出现 `MS_BOOST_GAUGE_RECOV` 的行 |

库是**固定宽度**表 ⇒ 按 42 声明会让"真实数据里的 109 行"最后几列被**静默截断**。
这与第 3 批 `WEAPON_BATTLE_DETAIL` 的口径一致（那张表也按"属性名可读到的**上限**"定 9 列，
而不是按单行的实际列数定）⇒ 本批同样定 **50**，并把 8 个只可能被 109 行用到的列命名成
`overflow_slot_42..49`（**不是 gap**：reader 会读，只是要看数据）。

## E.3 尾部 2 列的位置是**浮动**的

```c
*(a3+60) = sub_BBB370(a1, v6);        // 8 组消费完之后的**光标处**
*(a3+64) = sub_BBB370(a1, v6+1);
```

⇒ `tail_u32_60` / `tail_u32_64` 这两个**结构偏移**是固定的，但它们在 CSV 里的**列号**
随前面 8 组的列数浮动（常态落在 csv40/41）。旧注释把它们钉在 csv19/20 并命名
`priority`/`stack_rule`；本批按**结构偏移**命名（`tail_u32_60`/`tail_u32_64`），
列名不再暗示"第 19/20 列"。

## E.4 库侧动作

| 处 | 动作 |
|---|---|
| 库 | `RENAME COLUMN`：`effect_scope→group1_scope`、`stat_name→group1_stat`、`loop_param_value→group1_value`、`priority→group2_scope`、`stack_rule→group2_stat`（**位置不变、数据不搬**）；`ADD COLUMN IF NOT EXISTS` 追加 29 列（`group2_value` … `group8_value`、`tail_u32_60/64`、`overflow_slot_42..49`，新列 1856 格 `NULL → ''`） |
| 种子 | `server/datafiles/lounge/item/equip_parts.csv` 行宽 21 → **50 段**（64 行）+ 一行映射注释；原文件备份 `datatables/_backup_seeds/` |
| 下发 | `cfgsync -export-only` ⇒ `meta.cfg_manifest.raw_csv` 1970 → 3826 字节 |

## E.5 验收（全绿）

| 检查 | 结果 |
|---|---|
| 全库列漂移 | **0** |
| 列序 == schema 列序 / `reader_max_csv_index` == 列数−1 | 50/50 ✓ / 49 ✓ |
| manifest 每行字段数 == 库列数 | 段数分布 **`[50]`**（单值）✓ |
| 原列取值**按位置**逐格比对（改前全部 **22** 个物理列 × 64 行） | 1408 格差异 **0** ✓ |
| 行数 | 64 → 64（**一行没丢**） |
| 新列取值口径 | **0 个 NULL** |
| 其余 78 张表 | manifest `added [] / removed [] / changed 只 3 张`（含第 4 批两张）✓ |
| §2 偏窄清单 | **5 → 4** |

## E.6 遗留

- `groupN_*` / `tail_*` 的**列名只在"前面没有 109 组"时成立**；含 109 组的行整体后移，
  此时那些列的含义随行变（客户端只按顺序消费，写行时按光标顺序排布即可，末尾补空无害）。
- §2 剩余 **4** 张偏窄表：`AI_PARAM`（缺 82）/ `MISSION_XWAR_BANPICK`（39）/ `COMMANDER_NPC`（37）/
  `MODULE_BONUS`（35）—— 与第 1 批同型（固定块循环），逐表按 reader 的循环层数/步长反推组结构后再补。
