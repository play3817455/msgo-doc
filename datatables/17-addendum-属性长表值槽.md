
---

# 附录 C｜第 3 批订正：两张「属性长表」的行宽（值槽模型）· WEAPON_BATTLE_DETAIL 3→9 · MSMA_BATTLE_DETAIL 3→16（2026-10-05）

> 本附录由 `datatables/17-addendum-属性长表值槽.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。
> 脚本：`datatables/_fix_battledetail_width.py`（改 schema）→ `merge_cfg_asm.py`（GM 侧）→
> `_widen_battledetail.py`（库 `ADD COLUMN` + 种子补宽）→ `cfgsync -export-only`（重拼 manifest）→
> `_normalize_battledetail_nulls.py`（本批新列 `NULL → ''` 归一，自带前后哈希自证）→
> `_verify_battledetail.py`（验收）。基线快照在 `datatables/_rollback/20261005-222848_battledetail/`。

## C.0 本批结论一览

| 表 | 症状（旧） | 订正 | 依据（VA 可复查） |
|---|---|---|---|
| `WEAPON_BATTLE_DETAIL` | `cfg` 4 列 / manifest 行宽 4（`POWER,1040101,150,`） | **3 → 9 列**（补 `attr_value_3..attr_value_7`），行数 9579 不变 | SHIELD 值列阅读器 `sub_595D60` 读 `csv2..csv8` |
| `MSMA_BATTLE_DETAIL` | `cfg` 3 列 / manifest 行宽 4 | **3 → 16 列**（补 `entry_value_2..entry_value_14`），行数 5270 不变 | BOOST_SPEED 值列阅读器 `sub_57B9F0` 读 `csv2..csv15` |
| `WEAPON_BATTLE_DETAIL` 列漂移 | 库残留 1 列 `attr_value_2`，`cfgsync` 每次 `WARN 列漂移` | **漂移 0**：`attr_value_2` 不再是"残留"，它就是 **csv3 的值槽** | 同上 |
| 对账口径 | 这两张表被 §2 静默排除（`emu_err` 一票否决） | `_sweep_verdict.py` 新增 **`STATIC-READSET`** 静态读集覆盖 ⇒ 判定 **`STATIC-OK`**，宽度按真值判 | `_out_sweep_verdict.txt` |

## C.1 为什么「列数 3」是错的：这两张表是**回调分派**式属性长表

旧注释（`column_count: 3`）来自对 `sub_A47BC0` 的常量传播失败：它自己**只读 col0**，
真正的值列由**子表对象**读。完整链路（两张表同构，`#36` 与 `#34` 共用同一个 `sub_A47BC0`）：

```
CSV 行 ──> sub_A47BC0(row, ctx)
             ├─ col0 属性名（sub_456D90 # 开头跳过 → sub_BBB4F0 取原串）
             ├─ ctx vtable[0](name)          ← 词表：名 → 子表编号 1..11/1..13
             └─ ctx vtable[1](row, 编号)
                  └─ 容器 sub_595B10/sub_57BB70 → this[4*idx-3] 取子表对象
                       └─ 子表 vtable[1] = AddRow   ← 只读 **col1**（键，sub_BBB4F0(idx=1)）
                            └─ 子表 vtable[0] = ★值列阅读器★  ← 读 **col2..colN**（N 随属性名而定）
```

- 11 张（`#36`）/ 13 张（`#34`）子表的 **AddRow 全部只取 col1**（逐函数扫 `sub_BBB4F0` 调用点得到
  唯一常量列号 `1`）⇒ 值列**只**由 `vtable[0]` 读。
- 仿真器不可能跑通这条链：`ctx` 是 C++ 对象，仿真里没有那两个 vtable ⇒
  `call [vtable[0]]` 落到 `eip=0x2` ⇒ `UC_ERR_EXCEPTION`（这正是 §6 里这两行的"崩点"）。
  **不是"读集未知"，是"仿真这条线结构上跑不通"** ⇒ 本批改用**静态反汇编**取真值。

## C.2 `WEAPON_BATTLE_DETAIL`（#36）：11 张子表的值列宽度 ⇒ 上限 **csv8**

| col0 属性名 | 子表类（RTTI） | 值列阅读器 | 读到的列 | 最大 |
|---|---|---|---|---|
| `POWER` | `WEAPON_DETAIL_POWER_DATA` | `sub_57B970` | 2 | 2 |
| `RANGE` | `WEAPON_DETAIL_RANGE_DATA` | `sub_595A10` | 2 | 2 |
| `STABILITY` | `WEAPON_DETAIL_STABILITY_DATA` | `sub_595A30` | **2,3,4,5,6** | 6 |
| `RAPIDDELAY` | `WEAPON_DETAIL_RAPIDDELAY_DATA` | `sub_595AF0` | 2 | 2 |
| `COOLTIME` | `WEAPON_DETAIL_COOLTIME_DATA` | `sub_595AF0` | 2 | 2 |
| `RELOAD` | `WEAPON_DETAIL_RELOAD_DATA` | `sub_595AF0` | 2 | 2 |
| `LOCKON_CAM` | `WEAPON_DETAIL_LOCKON_CAM_DATA` | `sub_595A10` | 2 | 2 |
| `RECOIL` | `WEAPON_DETAIL_RECOIL_DATA` | `sub_595AB0` | 2,3 | 3 |
| `SWITCHTIME` | `WEAPON_DETAIL_SWITCHTIME_DATA` | `sub_595AF0` | 2 | 2 |
| `SHIELD` | `WEAPON_DETAIL_SHIELD_DATA` | `sub_595D60` | **2,3,4,5,6,7,8** | **8** |
| `HIGH_LOCKON` | `WEAPON_DETAIL_HIGH_LOCKON_RANGE_DATA` | `sub_595A10` | 2 | 2 |

反编译原文（子表 `vtable[0]`，即 `CDetailDataTable<T>::vftable` 的第一个入口）：

```c
// sub_595A30  STABILITY —— 5 个 float，注意 f[1]←csv2、f[0]←csv3（顺序交换）且都 ×flt_D69A58
a2[1] = sub_BBB470(a1, 2u) * flt_D69A58;
*a2   = sub_BBB470(a1, 3u) * flt_D69A58;
a2[2] = sub_BBB470(a1, 4u);
a2[3] = sub_BBB470(a1, 5u);
a2[4] = sub_BBB470(a1, 6u);

// sub_595AB0  RECOIL —— 2 个 float（度 → 弧度）
*a2   = sub_BBB470(a1, 2u) * flt_D69A68;
a2[1] = sub_BBB470(a1, 3u) * flt_D69A68;

// sub_595D60  SHIELD —— 7 项，混排，csv5 是枚举名（逐字反编译，2026-10-05 复核）
*(_DWORD *)a2       = sub_BBB370((int)a1, 2u);     // csv2 int
*(float *)(a2 + 4)  = sub_BBB470(a1, 3u);          // csv3 float
*(float *)(a2 + 8)  = sub_BBB470(a1, 4u);          // csv4 float
sub_BBB4F0((int)v4, (int)a1, 5u);                  // csv5 枚举名
*(_DWORD *)(a2 + 12) = 命中"BEAM" ? 1 : (命中"BLAST" ? 3 : 2);   // ★非 0/1，是 1/3/2
*(float *)(a2 + 16) = sub_BBB470(a1, 6u);          // csv6 float
*(float *)(a2 + 20) = sub_BBB470(a1, 7u);          // csv7 float
*(_BYTE *)(a2 + 24) = sub_BBB370((int)a1, 8u) != 0; // csv8 int→bool
```

★**读时缩放常量**（本批顺带读出，取值是实数不是猜测）：

| 常量 | 值 | 作用 |
|---|---|---|
| `flt_D69A58` @`0xD69A58` | `0x42C80000` = **100.0f** | RANGE / LOCKON_CAM / HIGH_LOCKON / STABILITY 的值 ×100 |
| `flt_D69A68` @`0xD69A68` | `0x3C8EFA35` = **0.017453292f**（π/180） | RECOIL 的值：**度 → 弧度** |
| `flt_D91AF8` @`0xD91AF8` | `0x3F000000` = **0.5f** | 消费侧 STABILITY `f[2] <= 0` 时的缺省（与 `36-` §3 记的一致） |

## C.3 `MSMA_BATTLE_DETAIL`（#34）：13 张子表的值列宽度 ⇒ 上限 **csv15**

| col0 属性名 | 值列阅读器 | 读到的列 | 最大 |
|---|---|---|---|
| `RESPAWN_TIME` | `sub_57B940` | **2..12**（`for i<11: sub_BBB370(i+2)`） | 12 |
| `WARP_TIME` / `COST` / `MAX_HP` / `BOOST_GAUGEMAX` | `sub_57B970` | 2 | 2 |
| `ENERGY` | `sub_57B990` | 2,3 | 3 |
| `MOVE` | `sub_57B9C0` | 2（负值钳 0） | 2 |
| `BOOST_GAUGEHEAL` / `SHOT` / `LOCKON` / `RELOAD` | `sub_595AF0` | 2 | 2 |
| `BOOST_SPEED` | `sub_57B9F0` | **2..15** | **15** |
| `JUMP` | `sub_57BAA0` | **2..13** | 13 |

```c
// sub_57B9F0  BOOST_SPEED —— 14 项，float/u32 混排（f=sub_BBB470, u=sub_BBB370）
f(2) f(3) u(4) f(5) f(6) u(7) u(8) f(9) f(10) f(11) f(12) f(13) u(14) f(15)

// sub_57B940  RESPAWN_TIME —— 循环 11 列
for (i = 0; i < 11; ++i) *(_DWORD *)(a2 + 4 * i) = sub_BBB370(a1, i + 2);
```

## C.4 改法：补「值槽」列，而不是补 gap 列

新列名不是 `colN`，而是**值槽序号**（与既有 `attr_value` / `entry_value` 连贯，且**不重命名**已有列）：

| 表 | 值槽命名 | 列总数 |
|---|---|---|
| `WEAPON_BATTLE_DETAIL` | `attr_value`(csv2) · `attr_value_2`(csv3) · … · `attr_value_7`(csv8) | **9** |
| `MSMA_BATTLE_DETAIL` | `entry_value`(csv2) · `entry_value_2`(csv3) · … · `entry_value_14`(csv15) | **16** |

`column_count` = reader 真映射列数 = **9 / 16**（这两张表**没有 gap 列**：每一列都由某张子表读）。
`attr_value_2` **保留原名**（它在库里的语义本来就是 STABILITY 的第二个值 = csv3）⇒ 不再触发列漂移。

## C.5 四处同步（本批实际动作）

| 处 | 动作 | 命令 / 文件 |
|---|---|---|
| schema | 两张表 `columns` 重写到全宽 + `column_count`/`column_defined`/`columns_note`/`reader_max_csv_index` | `python datatables/_fix_battledetail_width.py` |
| GM schema | 重生 `cfg_schema.json` / `index.json`（`MSMA_BATTLE_DETAIL` 16 列、`WEAPON_BATTLE_DETAIL` 9 列，无 gap） | `python db_design/tools/merge_cfg_asm.py` |
| 库 | `ALTER TABLE ADD COLUMN`（**不加 `-recreate`，行不丢**）：`WEAPON_BATTLE_DETAIL` +5 列、`MSMA_BATTLE_DETAIL` +13 列 | `python datatables/_widen_battledetail.py` |
| 种子 | 两张表补宽到 10 / 17 段（`_widen_seed.py` 同款口径）+ 一行值槽映射注释；备份 `datatables/_backup_seeds/` | 同上 |
| 下发 | `cfgsync -export-only` 重拼 `raw_csv`（**不碰 `header_text`** ⇒ 无需 `_manifest_restore.py`） | `cd serverv && go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables -export-only` |
| 值归一 | `ADD COLUMN` 出来的新列在旧行里是 **`NULL`**（cfg 其余列都是 `''`）⇒ `_normalize_battledetail_nulls.py` 把本批 18 列 **`NULL → ''`**（`WEAPON_BATTLE_DETAIL` 改 47895 格、`MSMA_BATTLE_DETAIL` 改 68510 格），**下发件 sha256 逐字节未变**（`ExportTableRawCSV` 两者都导出成空字段） | 同上脚本自带前后哈希自证 |
| 工具 | `_sweep_verdict.py` 加 `STATIC_READSET` 覆盖；`_sweep_width_db.py` 不再用 `emu_err` 一票否决有静态背书的表 | 同上两个脚本 |

## C.6 验收（全部通过）

| 检查 | 结果 | 脚本 |
|---|---|---|
| 全库列漂移 | **1 → 0**（`WEAPON_BATTLE_DETAIL` 的 `attr_value_2` 归位） | `_verify_battledetail.py` |
| 列序 == schema `csv_index` 序 | 9/9 ✓、16/16 ✓ | `_verify_battledetail.py` |
| manifest 行宽 == reader 最大列号 + 1 | 9 == 8+1 ✓、16 == 15+1 ✓ | `_verify_battledetail.py` / `_sweep_width_db.py` |
| 原列取值**逐行未变** | `WEAPON_BATTLE_DETAIL` 38316 个值差异 **0**；`MSMA_BATTLE_DETAIL` 15810 个值差异 **0** | `_verify_battledetail.py` |
| 行数 | 9579 → 9579、5270 → 5270（**未丢行**） | 同上 |
| 新列取值口径 | 18 个新列 **0 个 NULL 残留**（全 `''`，与 cfg 其余列同口径；`_probe_battledetail_nulls.py`） | `_normalize_battledetail_nulls.py` |
| 其余表逐字节未变 | manifest 79 行：added `[]`、removed `[]`、**changed 只 2 张** | `_manifest_snapshot.py diff` |
| 读集判定 | 两张表 `EMU-PARTIAL` → **`STATIC-OK`**；§2 偏窄表仍为 7 张（未增） | `_sweep_verdict.txt` |
| GM 侧 | `cfg_schema.json` 两张表列名与 `csv_index` 一一对应 | 本批脚本复核 |

## C.7 遗留（本批未做）

- **列名语义**：`attr_value_N` / `entry_value_N` 只是"第 N 个值槽"；**槽里到底是什么**取决于同行 col0
  的属性名（已逐条写进 schema 的 `meaning`，但列名本身不带语义）。
- **`RANGE/LOCKON_CAM/HIGH_LOCKON/STABILITY` 的 ×100 与 `RECOIL` 的 π/180**：本批只把常量读出并记录；
  `36-` §6 现在写的是「射程 **原样**（世界单位）」，与读表侧的 ×100 **口径不一致** ——
  需核消费侧是否再除 100（`36-` §3 记的 `sub_42A6B0` 反编译里只有 `flt_D7A47C`/`flt_D675B4`，
  后者是 `0x4F000000`≈2^31，**不是 0.01 级缩放常数**，疑为该文出处有误）⇒ **下一批专项核对**。
- `46-` 遗留的 **RAW_CSV vs FB 口径**：`cfg_schema.json` 是「库列名」口径，客户端是「CSV 列号」口径；
  两张表列数仍不同名（如 `attr_value_3` ↔ csv4），查表时以 `csv_index` 为准。
- §2 剩余 7 张偏窄表（`AI_PARAM` 82 缺 / `MISSION_XWAR_BANPICK` 39 / `COMMANDER_NPC` 37 /
  `MODULE_BONUS` 35 / `ITEM_PART` 21 / `CHALLENGE_HIGHSCORE` 18 / `BEGINNER_CHALLENGE` 10）
  仍是"固定块循环"，需先逆向每组列含义（与本批的"值槽"模型不同）。
- **`ADD COLUMN` 出来的列在旧行里是 `NULL` 而非 `''`** —— 本批两张表已归一，但**前两批补的列仍有残留**
  （`PLAY_BONUS_REWARD.reserved_u32_8` 起 1 列、`PLAYER_NAVI` 2 列、`BUFF` 3 列、`MODULE_DEVELOP` 6 列、
  `MISSION_EXTRULE` 8 列，`_probe_battledetail_nulls.py` 实测）：目前**无读侧受影响**（这些列没被任何 Go
  查询引用，且 `ExportTableRawCSV` 对 `NULL`/`''` 都导出空字段），但下次补列时**顺手归一**更省事
  （`_normalize_battledetail_nulls.py` 改 `NEW_COLS` 即可复用）。
