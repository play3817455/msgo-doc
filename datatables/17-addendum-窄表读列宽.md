
---

# 附录 D｜第 4 批订正：两张「奖励窄表」的行宽 · BEGINNER_CHALLENGE 6→16 · CHALLENGE_HIGHSCORE 10→28（2026-10-05）

> 本附录由 `datatables/17-addendum-窄表读列宽.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。
> 脚本：`datatables/_fix_narrow4.py`（改 schema）→ `merge_cfg_asm.py`（GM 侧）→
> `_apply_narrow4.py`（库 `RENAME COLUMN`/`ADD COLUMN` + 种子补宽）→
> `cfgsync -export-only`（重拼 manifest，**不加 `-bootstrap-csv`** ⇒ 不碰 `header_text`）→
> `_normalize_cfg_nulls.py`（**全库** `NULL → ''` 归一，自带前后哈希自证）→
> `_verify_narrow4.py`（验收）。基线快照在 `datatables/_rollback/20261005-224901_narrow4/`。

## D.0 本批结论一览

| 表 | 症状（旧） | 订正 | 依据（VA 可复查） |
|---|---|---|---|
| `BEGINNER_CHALLENGE` | schema 6 列 / 行宽 6，且列号**整套错位**（类型枚举记在 csv2） | **6 → 16 列**（`reward{1,2,3}_{type,param_a,param_b,param_c}`），行数 64 不变 | `sub_570420` @ `0x570420` 读 `csv0..csv15` |
| `CHALLENGE_HIGHSCORE` | schema 10 列 / 行宽 10，三条字符串错记在 csv2/3/4 | **10 → 28 列**（`csv2/3/4` = gap，3 串 → csv5/6/7，尾部 4×5 u32），行数 64 不变 | `sub_578630` @ `0x578630` 读 `csv0..csv27`（跳 2/3/4） |
| 全库 `NULL` 残留（附录 C.7 遗留） | 前两批 `ADD COLUMN` 的旧行是 `NULL`（cfg 其余列都是 `''`） | **125 列 / 901 格 `NULL → ''`**，下发件 **79 张表逐字节未变** | `_normalize_cfg_nulls.py` |
| §2 偏窄表计数 | 7 | **5**（剩 `AI_PARAM` / `MISSION_XWAR_BANPICK` / `COMMANDER_NPC` / `MODULE_BONUS` / `ITEM_PART`） | `_sweep_width_db.py` |

## D.1 `BEGINNER_CHALLENGE`（#77）：行结构 = 4 前导 u32 + **3 组 × {类型, 参数A, 参数B, 参数C}**

```c
// sub_570420  逐条反编译
sub_BBB370(0) → +0                       // u32 主键
sub_BBB370(1) → +4                       // u32
sub_BBB370(2) → +8                       // u32   ← 旧 schema 记成 reward_type（错）
sub_BBB370(3) → +12                      // u32
for (r = 0; r < 3; ++r) {                // 组步长 16B；组基址列号 = 4 + 4r
    v6[0] = sub_BBB370(r + 1);           //   → +0  参数 A
    v6[1] = sub_BBB370(r + 2);           //   → +4  参数 B
    v6[2] = sub_5703A0(sub_BBB4F0(r));   //   → +8  ★类型枚举（组基址那一列）
    v6[3] = sub_BBB370(r + 3);           //   → +12 参数 C
}
```

- ★**CSV 列序 ≠ 内存序**：CSV 是 `{type, A, B, C}`，结构体是 `{A, B, C` 前置…`type}` 在 `+8`。
- 内存落点：`challenge_id +0` / 3 前导 u32 `+4/+8/+12` /
  组 1 `A+16 B+20 type+24 C+28`、组 2 `A+32 B+36 type+40 C+44`、组 3 `A+48 B+52 type+56 C+60`。
- 旧 schema（6 列）与 reader 的真列号**整套错位**：`reward_type` 记在 csv2（真值 csv4）、
  `reward_quantity` 记在 csv4、`condition_param` 记在 csv5；csv6..csv15 未声明 ⇒ 被越界兜底吃成 0。

枚举 `sub_5703A0`（奖励类型，本批读出，旧的 0/1/2/3 标注作废）：

| CSV 字串 | 值 |
|---|---|
| `GP` | `0` |
| `ITEM` | `1` |
| `MSMA` | `998` |
| `BUILDUP_MSMA` | `-1` |
| 其它（含空） | `999` |

## D.2 `CHALLENGE_HIGHSCORE`（#57）：u32 主键 + u8 + **3 串** + **4 组 × 5 u32**

```c
// sub_578630  逐条反编译
a3[0] = sub_BBB370(0);   a3[1] = sub_BBB370(1);          // → +0（u32）/ +4（u8）
                                                          // ★ csv2 / csv3 / csv4 从不取用
sub_456D90(+8 , 5);  sub_456D90(+36, 6);  sub_456D90(+64, 7);   // 3 条 wstring，每条占 28B
v7 = &(+92);
do { 5 次 *(v7++) = sub_BBB370(k++); } while (4 轮);      // csv8..csv27 → +92..+168（组步长 20B）
```

- 三串在 `+8 / +36 / +64`（间距 28B，与附录 A.1 里 `sub_456D90` 的「每字段 28 字节」一致）。
- 旧 schema 把三串记在 **csv2/3/4**（reader 根本不读这三列），并在 csv9 截断 ⇒ 缺 18 列。
- `csv8`/`csv9` 沿用旧名 `score_threshold` / `reward_gp`（在循环第 1 组内），**语义未取证** ⇒
  schema 里标注为「沿旧名，语义未取证」，不据旧名做任何业务推断。

## D.3 库侧动作：**`RENAME COLUMN` 保位置** + `ADD COLUMN` 补宽

- 旧库列名与读者真列号不对应时，**不 `DROP`/`ADD`**，而是
  `ALTER TABLE cfg."T" RENAME COLUMN old TO new` ⇒ **物理序号不变、数据不搬**；
  新增列用 `ALTER TABLE cfg."T" ADD COLUMN IF NOT EXISTS … TEXT`。
- 实测映射（`BEGINNER_CHALLENGE`）：`sort_order→unknown_u32_1`、`reward_type→unknown_u32_2`、
  `reward_param_id→unknown_u32_3`、`reward_quantity→reward1_type`、`condition_param→reward1_param_a` + 9 新列。
- 实测映射（`CHALLENGE_HIGHSCORE`）：`rank_title→col2`、`rank_description→col3`、`reward_title→col4`，
  `reward_desc`/`ui_label`/`footer_text`/`score_threshold`/`reward_gp` **原位同名保留** + 18 新列。
- 种子 `server/datafiles/lounge/**` 同步补宽（16 / 28 段），原文件备份 `datatables/_backup_seeds/`。

## D.4 全库 `NULL → ''` 归一（顺带清掉附录 C.7 的遗留）

`ADD COLUMN` 出来的列在**旧行**里是 `NULL`，而 cfg 其余列都是 `''`
（`ExportTableRawCSV` 两者都导出空字段，故此前无可见影响，但口径不一致）。本批一次扫全库：

| 表 | 列数 | 格数 | 来源 |
|---|---|---|---|
| `WEAPON_SETTING` | 108 | 648 | 早批补宽 |
| `MISSION_EXTRULE` | 8 | 512 | 第 1 批 |
| `MODULE_DEVELOP` | 6 | 384 | 第 1 批 |
| `BUFF` | 3 | 192 | 第 1 批 |
| `PLAYER_NAVI` | 2 | 128 | 第 1 批 |
| `PLAY_BONUS_REWARD` | 1 | 64 | 第 1 批 |
| `ITEM` | 3 | 9 | —— |
| **合计** | **125** | **901** | —— |

自证：改前/改后对 **全部 79 张** `meta.cfg_manifest.raw_csv` 取 sha256 ⇒ **逐字节未变 ✓**。

## D.5 四处同步（本批实际动作）

| 处 | 动作 | 命令 / 文件 |
|---|---|---|
| schema | 两张表 `columns` 重写到全宽 + `column_count/defined/confirmed/gap`、`column_gap_note`、`reader_max_csv_index`、`columns_note` | `python datatables/_fix_narrow4.py` |
| GM schema | 重生 `cfg_schema.json` / `gm_data_boundaries.json`（80 张） | `python db_design/tools/merge_cfg_asm.py` |
| 库 | `RENAME COLUMN`（保位置）+ `ADD COLUMN IF NOT EXISTS`（**不加 `-recreate`，64 行一行没丢**） | `python datatables/_apply_narrow4.py` |
| 种子 | 补宽到 16 / 28 段 + 备份 | 同上 |
| 下发 | `cfgsync -export-only` 重拼 `raw_csv`（**不碰 `header_text`** ⇒ 无需 `_manifest_restore.py`） | `cd serverv && go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables -export-only` |
| 归一 | 全库 `NULL → ''`（125 列 / 901 格） | `python datatables/_normalize_cfg_nulls.py` |

## D.6 验收（全部通过）

| 检查 | 结果 | 脚本 |
|---|---|---|
| 全库列漂移 | **0** | `_verify_narrow4.py` |
| 列序 == schema 列序（逐列同名同序） | 16/16 ✓、28/28 ✓ | 同上 |
| `reader_max_csv_index` == 列数 − 1 | 15 ✓、27 ✓ | 同上 |
| manifest 每行字段数 == 库列数 | `{16}` ✓、`{28}` ✓（均为单值） | 同上 |
| **原列取值逐格未变**（按位置比对 ⇒ 覆盖改名前**全部**物理列：7 列 / 11 列） | 448 格差异 **0** ✓、704 格差异 **0** ✓ | 同上 |
| 行数 | 64 → 64 × 2（**未丢行**） | 同上 |
| 新列取值口径 | 两表 **0 个 NULL**（全 `''`） | 同上 |
| 其余 77 张表未被本次操作改动 | manifest 79 行：added `[]`、removed `[]`、**changed 只 2 张** | `_manifest_snapshot.py diff` |
| 全库 NULL 残留 | **901 → 0**，下发件 sha256 未变 | `_normalize_cfg_nulls.py` |

## D.7 遗留（本批未做）

- **列语义**：`CHALLENGE_HIGHSCORE` 的 4 组 × 5 u32（csv8..csv27）与 `BEGINNER_CHALLENGE` 的
  `param_a/b/c` **含义未定**（reader 取回即存，未见消费侧引用）—— 只确证了「客户端会读满这些列」。
  `score_threshold` / `reward_gp` 两名沿用旧注释，**未取证**。
- §2 剩余 **5** 张偏窄表（缺列数）：`AI_PARAM` 82、`MISSION_XWAR_BANPICK` 39、`COMMANDER_NPC` 37、
  `MODULE_BONUS` 35、`ITEM_PART` 21 —— 与第 1 批同型（**固定块循环**），
  逐表按 `reader` 的循环层数/步长反推出组结构后再补（`ITEM_PART` 已开工：`sub_5955A0`）。
