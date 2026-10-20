
---

# 附录 G｜第 7 批订正：最后 3 张偏窄表 · `COMMANDER_NPC` 13→50 · `MISSION_XWAR_BANPICK` 4→43 · `AI_PARAM` 45→127（2026-10-05）

> 本附录由 `datatables/17-addendum-第7批缝列与带块.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。
> 脚本：`_fix_commander_npc.py` / `_fix_mission_xwar_banpick.py` / `_fix_ai_param.py`（改 schema）
> → `merge_cfg_asm.py`（GM 侧）→ `_apply_batch7.py`（库 `RENAME COLUMN`/`ADD COLUMN` + 物理列重排 + 种子补宽）
> → `cfgsync -export-only`（重拼 manifest，**不加 `-bootstrap-csv`** ⇒ 不碰 `header_text`）
> → `_verify_batch7.py`（验收）。
> 基线快照在 `datatables/_rollback/20261005-233942_commander_npc/`、
> `..._mission_xwar_banpick/`、`..._ai_param/`（三个目录各含 `.json` / `.db.csv` / `.manifest.txt` / `.seed.csv`）。

## G.0 结论一览

| 表 | 旧行宽 | 订正 | reader 读集 | 缝列 | 依据 |
|---|---|---|---|---|---|
| `COMMANDER_NPC` | schema 13 / 库 13 / 种子 13 | **50**（`csv0..csv49`） | `0..6, 12,13,14, 17,18, 21,22, 25..49`（**39 列**） | **11**：`7..11, 15,16, 19,20, 23,24` | `sub_572EE0` @`0x572EE0` |
| `MISSION_XWAR_BANPICK` | schema 4 / 库 4 / 种子 4 | **43**（`csv0..csv42`） | `0..42`（**43 列**，连续；**实际读几列由 `csv2` 决定**） | 0 | `sub_5A0300` @`0x5A0300` |
| `AI_PARAM` | schema 45（declared 43）/ 库 45 / 种子 45 | **127**（`csv0..csv126`） | `0..126`（**127 列**，连续） | 0 | `sub_56EA00` @`0x56EA00` |

- 三张表**修完全库偏窄清单归零**：`_out_sweep_width_db.json` 的 narrow 集合 **3 → 0**。
- 对账等级：`MISSION_XWAR_BANPICK` = **OK**（写偏移多重集 + 配对一致）；另两张 = **READSET-OK**
  （读集一致，写点仅高置信部分可比 —— 因为 reader 会把值经转换函数写入枚举/浮点字段）。

## G.1 三张表是同一种错法：「把循环的某一轮 / 某一段当成整张表」

| 表 | 旧声明怎么来的 | 为什么"看着自洽" |
|---|---|---|
| `COMMANDER_NPC` | 旧注释把 reader 的**内部列号**（`csv12/13/14` 这类）当成 **CSV 列位**，只保留了前 7 列 + 5 个"像是槽位"的列 | 13 段行宽刚好能被 parser 接受，且 `csv0` 是键 ⇒ 表面正常 |
| `MISSION_XWAR_BANPICK` | 只声明了 `rule_id + mode + count + 1 个机体 ID`（把**可变长列表**当成"1 列默认机体"） | 种子只填 `csv2` 一个数 ⇒ 客户端 `3 + min(csv2,40)` = 3 列，**读取失败不会报错**（越界读作 0） |
| `AI_PARAM` | 声明到 `csv44` 就停了，并把 `csv19` / `csv22` 标成 gap | 那两处 gap 是**静态扫描的假象**（见 G.4） |

> 共同点：**客户端读到行外一律返回空串 ⇒ `atoi`/`atof` = 0**（`sub_456D90` 的
> `if (col < n) 取列 else 空串`）。所以"行宽偏窄"在运行时**永远不会报错**，只会静默变成 0 —— 这也是前六批
> 一共修掉 10 张表、却直到本批才把清单清零的原因。

## G.2 `COMMANDER_NPC`：7 前导 + 4 槽消耗 + 3 槽冷却 + 12 组×{值,类型名} + 1 尾列

```c
// sub_572EE0 逐条反编译（v10 = CSV 列游标）
csv0..6  → +0/+4/+8/+12(wstring)/+40(wstring)/+68(势力 enum)/+72     // 7 前导
csv12    → +88 (u16)                                                 // 槽 1 消耗
v10=13; do { *u16++ = atoi(csv v10); *u32++ = atoi(csv v10+1); v10+=5; } ×3
//   ⇒ 消耗 csv13/17/21（+92/+94/+96），冷却 csv14/18/22（+220/+224/+228）
v10=25; do { *u32++ = atoi(csv v10); *u32++ = enum(csv v10+1); v10+=2; } ×12
//   ⇒ 12 组 {supportK_value → +256+4(k-1), supportK_type → +304+4(k-1)}，吃 csv25..48
csv49    → +80                                                        // 尾列：解锁任务 ID
// 12 个类型枚举随后按 switch 折成 31 位掩码写 +76
```

- **列步长 5** 是缝列的来源：槽组 3 轮报的是 `{消耗, 冷却}` 两列，但步长 5 ⇒ 中间夹 3 列缝
  （`csv15/16` 在槽 1 与槽 3 之间、`csv19/20` 在槽 3 与槽 4 之间；`csv7..11` 是前导后的第一段缝、`csv23/24` 是 12 组前的缝）。
- ★**槽 4 只有消耗没有冷却**：reader 只读 **3 个**冷却（`csv14/18/22`），`slot4_cost`（`csv21`）之后直接进 12 组循环
  ⇒ 旧注释把 `support_type_1` 摆在 `+224` 是**错位**的（那是 `slot2_cooldown`）。
- 枚举（`sub_572C30` 势力 3 值；`sub_572CD0` 支援类型 **31 值**）见 `01-列注释/28-28-COMMANDER_NPC.md`。
- ★**索引键 = `csv0`**（vtable[5] `sub_A564D0` = `atoi(a1,0)`），旧注释这里是对的。

## G.3 `MISSION_XWAR_BANPICK`：**行宽依赖数据**的一张表（全库唯一）

```c
// sub_5A0300
*a3 = atoi(csv0); a3[1] = atoi(csv1); a3[2] = atoi(csv2);
if (a3[2] > 40) a3[2] = 40;                      // ★硬上限 40
for (v4 = 0; v4 < a3[2]; ++v4) a3[3+v4] = atoi(csv v4+3);
```

- ⇒ 真读列数 = `3 + min(csv2, 40)`：**`csv2` 空 ⇒ 只读 3 列**（40 个机体槽全 0）。
- 我们把 schema/库/种子统一声明为**上界 43 列**，保证 CSV 行宽稳定；写数据时**必须同时写 `csv2`**
  （只填机体槽而不写 `csv2`，客户端一个槽都不读）。这条已写进列注释与种子注记。
- 旧名 `pick_count` → `ban_ms_count`（它是**条数**，不是"可选机体数"）；`ban_ms_id` → `ban_ms_id_1`
  （原位改名，位置保持）。库侧走 `RENAME COLUMN` ⇒ 数据不搬。

## G.4 `AI_PARAM`：两个"假 gap"与三个"同构带块"

旧 schema 在 `csv19` / `csv22` 标了 gap，真实原因是 **列号游标 `v36` 按引用传给共享子读函数**：

```c
v36 = 18;
csv17 → +520 bit3
sub_56E890(a3+84, a1, &v36)                  // ★内部 (*a4)++ 5 次 ⇒ 吃 csv18..22
csv23..47  sub_56E220(&v34, v42, a1, &v36)   // ★内部吃 25 列 → 带 A（NEAR）
csv48      v42[0] = atof(csv48)              // ★带 A 独有的"块首 float"，不在子函数循环里
csv52..76  sub_56E220(…)                     // 带 B（MIDDLE），v42[0] = 0（不读 CSV）
csv79..103 sub_56E220(…)                     // 带 C（FAR），v42[0] = 0
csv122..125 sub_56E3F0(a3+504, a1, &v36)     // ★吃 4 列 → +504(u8)/+508/+512/+516
cssv126 → +521 bit0
```

- ⇒ 主函数里只看得到 `sub_56E890(&v36)` 这一句，**看不到游标前进**，于是静态扫描把 `csv19`/`csv22`
  误判成"没被读"。**仿真读集**（`_out_emu_readers.json`）给出的是连续的 `0..126` ⇒ 旧 gap 是假象。
- 三个带块**同构**：每块 25 列 = `{3 个 u8（atoi）, 22 个 float（atof）}`，块内 23 个 float 随后被
  `sub_56E450` **归一化（和 = 1）**。
- ★带 A/B/C ↔ `NEAR/MIDDLE/FAR` 的对应是**推定**：依据 `csv22` 枚举名（`sub_56E6B0`：`NEAR=2/MIDDLE=3/FAR=4`）
  与"带 A 独有块首 float、Mid/Far 该处为常量 0"的差异。**该推定已写入 schema 的 `columns_note`，属未取证项。**
- 旧注释里 `col18`/`col20`/`col21`/`col23`/`col24` 等"近/中距权重"的列位**全部错位**（把子函数内部偏移当列位），
  本批按展开后的游标逐列重排；`col42/43/44` 三个"整型/开关"也很靠后（真实位置在 `csv119..121/126`）。

## G.5 库侧动作（三表统一走「`_row_id` 保持的整表重建」）

本次**没有**用 `ADD COLUMN` 追加（那会把新列排在物理末尾、与 schema 的 `csv_index` 序不一致，
而 `ExportTableRawCSV` 是**按 `information_schema` 物理列序**重拼 CSV 的 —— 见 `internal/cfg/audit.go` 的说明）。
做法：`BEGIN` → `CREATE TABLE cfg."T__b7" (LIKE 目标 ... )` 按 schema 序建列 → `INSERT ... SELECT`（旧同名/改名列按名搬迁、
新列填 `''`、`_row_id` 原值带入）→ 断言新表 0 `NULL`、丢弃的旧列**逐格全空** → `DROP` 旧表 / `RENAME` 新表 /
`ALTER SEQUENCE ... OWNED BY` → `COMMIT`。

| 表 | 旧→新列 | 跨名搬迁 | 丢弃旧列（已断言全空） | 种子 |
|---|---|---|---|---|
| `COMMANDER_NPC` | 13 → 50 | `support_type_1` → `support1_type` | 无 | `command/commander_npc.csv` 行宽 → 50 段（64 行）+ 布局注记 |
| `MISSION_XWAR_BANPICK` | 4 → 43 | `pick_count`→`ban_ms_count`、`ban_ms_id`→`ban_ms_id_1` | 无 | `mission/mission_xwar_banpick_rule.csv` → 43 段（64 行）+ 布局注记 |
| `AI_PARAM` | 45 → 127 | 无 | **27 列**（`near_band_param`、`col19`、`near_weight_a/b`、`col22`、`mid_weight_a/b`、`field_25..29`、`far_weight_a/b`、`fire_mode_weight_a/b/c`、`field_35..38`、`linked_weapon_param_a/b`、`melee_subtype`、`unknown_u32_42/43`、`flag_44`） | `npc/ai_param.csv` → 127 段（64 行）+ 布局注记 |

> `AI_PARAM` 丢弃的 27 列在基线上**全是空串**（`_apply_batch7.py` 判前先断言），所以"逐格未变"这条红线成立：
> 它们的语义已按新列名原样落在新表的对应位置（不是删数据，而是**重新分配列位**）。

## G.6 验收（`_verify_batch7.py`，全绿）

| 检查 | 结果 |
|---|---|
| 全库列漂移（物理列序 == schema `csv_index` 序，80 张） | **0** |
| 三表：库列 == schema 宽度 == manifest 段数 | 50/43/127 ✓ |
| `reader_max_csv_index` + 1 ≤ 宽度 | 49/42/126 ✓ |
| 行数 / `NULL` 行 / 邻表行数变化 | 64→64 ✓ / **0** ✓ / **0** ✓ |
| 老列取值**按列名**逐格比对（改名走映射表） | 三表各 **64 非空格，差异 0** ✓ |
| 被物理丢弃的旧列逐格为空 | `AI_PARAM` 27 列 **0 非空格** ✓ |
| manifest 数据格 == 库格（导出链无错位） | 三表 **差异行 0** ✓ |
| 对账等级 | `MISSION_XWAR_BANPICK` **OK**；另两张 **READSET-OK** ✓ |
| §2 偏窄清单 | **3 → 0** ✓ |

## G.7 GM 侧声明同步（`internal/gm/modules_spec.go`）

改列名会让 GM 玩法模块的**列声明静默失效**，`TestModulesMatchDB` 正是拦这个的红灯（本次重跑直接报红）：
它点名了 3 张本批表 + 3 张前几批表的**旧列名**。本批一并归位（改名 → 新名；旧名指向的点位已不存在的，改指真读列）：

| 模块 / 实体 | 旧声明 | 新声明（与 schema 一致） |
|---|---|---|
| `ms/module_bonus` | `stat_id_a` / `stat_value` | `group1_stat_id_a` / `group1_stat_value`（并加注：键在 `bonus_group`） |
| `item/item` → ITEM_PART | `stat_name` / `priority` | `group1_stat` / `group2_scope` |
| `item/item_part` | `stat_name` / `priority` | `group1_stat` / `group2_scope` |
| `mission/mission_xwar_banpick` | `pick_count` / `ban_ms_id` | `ban_ms_count` / `ban_ms_id_1`、`ban_ms_id_2`（并加注"读列数随 `ban_ms_count` 变化"） |
| `mission/challenge_beginner` | `reward_param_id`（第 4 批已归位为占位列 `unknown_u32_3`，客户端不读） | `reward1_type` / `reward1_param_*`（改指真读的奖励列） |
| `mission/challenge_highscore` | `rank_title` / `reward_title`（同上，已成占位列） | `ui_label` / `reward_desc` / `footer_text` / `score_threshold` / `reward_gp` |

> `TestModulesMatchDB` 的口径值得记住：**改 schema 列名必须同步 `modules_spec.go`**，
> 否则 GM 页面会"静默少一栏"。本次 `go test ./...` 全绿（`internal/gm` 9.2s）。

## G.8 遗留（本批**只记不裁**）

- `AI_PARAM` 带 A/B/C ↔ `NEAR/MIDDLE/FAR` 仍是**推定**；`near/mid/far_extra_*`、`tail_*` 多列的**业务语义未取证**
  （只到"哪个内存偏移、什么类型、是否归一化"这一层）。取证入口：`sub_56E450`/`sub_56E510` 的调用方（AI 决策/评分）。
- `COMMANDER_NPC` 的 `supportK_value`（`csv25/27/…/47`）与 `unlock_mission_id` 的**消费点未找到**。
- `MISSION_XWAR_BANPICK` 的 `banpick_mode` 取值域（旧注释写"0=标准 1=快速"）**无 ASM 证据**，
  本批保留旧描述但不再作为确证。
- 全库仍有许多表的**取值**为空（"结构已对齐、数值待填"）—— 这是下一步的工作面，与列宽问题已解耦。
