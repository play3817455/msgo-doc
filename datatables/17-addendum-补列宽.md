
---

# 附录 A｜补列宽记录（缺 1~3 列的 5 张表，2026-10-05）

> 本附录由 `datatables/17-addendum-补列宽.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。

## A.1 原则（用户裁定）

**按客户端行为补；没有原版数据就自行占位。** 依据 `sub_456D90`（本次重新反编译复核）：

```c
v4 = this[28];                                            // 行字段数组（每字段 28 字节）
if (v4 && idx < (this[29] - v4) / 28) v5 = v4 + 28*idx;   // 界内 → 指向该列
else { sub_402AD0(&String, 0); v5 = &empty; }             // 越界 → 空串
*(dst + 20) = 0;                                          // 目标串长度 0
sub_4029E0(dst, v5, 0, -1);
```

⇒ **「越界列」与「存在但为空」的列对客户端完全等价**（两者都得到 `""` ⇒ `atoi`/`atof` = 0）。
所以补空列**不改变任何客户端行为**，换来三件事：

1. 列位诚实（库/CSV 宽度 == reader 读列数，不再依赖越界兜底）；
2. 库结构不再"少一截"（GM/审计不再报窄）；
3. 将来拿到原版数值可直接落库生效 —— **缺列时那些值是会被静默丢掉的**。

## A.2 逐表证据与新增列

| 表 | reader | reader 真读列（→内存偏移） | 本次新增列 | 判定依据（IDA 反编译） |
|---|---|---|---|---|
| `BUFF` | `sub_570750` | 0..11 | 9:`effect_param_1`→+48、10:`effect_param_2`→+52、11:`effect_param_3`→+56 | 循环 `mov ebx,8 … call sub_BBB370; [esi]=eax; esi+=4` 四次 ⇒ 数组 +44/+48/+52/+56 |
| `PLAY_BONUS_REWARD` | `sub_58C440` | 0..7, 9（跳 8） | 9:`unknown_u32_9`→+28 | `push 9 @0x58c4a3`（call @0x58c4a9）；取回存 +28，本函数未再引用 |
| `PLAYER_NAVI` | `sub_58C7C0` | 0..18（跳 12） | 17:`unknown_u32_17`→+136、18:`unknown_u32_18`→+140 | 尾段 `v7=17` ⇒ `push v7` / `push v7+1` |
| `MODULE_DEVELOP` | `sub_5A2B90` | 0,2,3,4,6,7,9,10,12（跳 1,5,8,11） | 7:`material2_item_id`→+12、8:`reserved_u32_8`(gap)、9:`material2_qty`→+16、10:`material3_item_id`→+20、11:`reserved_u32_11`(gap)、12:`material3_qty`→+24 | `do{ v3, v3+2; v3+=3 }×3` ⇒ **三组「材料ID/材料数量」配对**（(4,6)/(7,9)/(10,12)），组间空一列；结构体 9 字段 +0/+4/+8/+12/+16/+20/+24/+28/+32 |
| `MISSION_EXTRULE` | `sub_59E170` | 0, 2..13（跳 1） | 6..13:`unknown_u32_6..13` → +20/+24/+28/+32/+36/+40/+44/+48 | `v23=2 { v13=4 { push v11++ } }` ⇒ 固定 8 列 |

宽度变化：`BUFF` 9→12、`PLAY_BONUS_REWARD` 9→10、`PLAYER_NAVI` 17→19、`MODULE_DEVELOP` 7→13、
`MISSION_EXTRULE` 6→14（均含 gap 列；`reader_read_max` == 新宽度 ✓）。

## A.3 同批订正的既有列错误标注

| 表 | 列 | 原状 | 订正为 | 依据 |
|---|---|---|---|---|
| `MISSION_EXTRULE` | csv4 `param_b` / csv5 `param_value` | `param_value` 标 +12（整段早一格） | `param_b`→+12、`param_value`→+16 | `a3[2]=col3→+8`、`a3[3]=col4→+12`、`a3[4]=col5→+16` |
| `MISSION_EXTRULE` | csv1 `rule_label` | status=`confirmed`（声称已映射） | status=`gap`（客户端不读） | reader 只 push `0,2,3,4,5,6..13`，**从不取 col1**；它只是本服备注/GM 展示名（`gm/modules_spec.go` NameCols） |
| `BUFF` | csv3..csv6 `duration_sec`/`stack_limit`/`priority`/`icon_index` | "参与 +36 标志合成" | **读后丢弃**（值不落结构体） | `movzx edx,[esi+24h] … mov [esi+24h],dl`：四次取值都在 call 之后丢失，store 的是**原字节** ⇒ 改这 4 列对客户端无影响 |

## A.4 四处同步（本次实际动作）

| 处 | 动作 | 命令 / 文件 |
|---|---|---|
| schema | 加列（含 gap）+ `column_count/defined/confirmed/gap`、`column_gap_note`、`columns_note` 同步 | `datatables/_widen_patch.py` → `db_design/schema/cfg/tables/*.json` |
| GM schema | 重生成 GM 侧列语义（中文名/含义/枚举/证据 VA） | `python db_design/tools/merge_cfg_asm.py`（复核：80 张 JSON **零字节改动** = 幂等 ✓） |
| 种子 | 行宽补到 reader 列数 + 插入一行 reader 映射注释（沿用 #50 MODULE 种子写法） | `datatables/_widen_seed.py` → `server/datafiles/lounge/**`（原文件备份 `datatables/_backup_seeds/`） |
| 库 + 下发 | `ALTER TABLE cfg.{T} ADD COLUMN IF NOT EXISTS … TEXT` + 重拼 `meta.cfg_manifest.raw_csv` | `cd serverv && go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables` |

## A.5 验收（全部通过）

| 检查 | 结果 | 脚本 |
|---|---|---|
| 库物理列 == schema 列序（逐列同名同序） | 5/5 ✓ | `_widen_state.py` |
| `manifest` 每行字段数 == 库列数 == reader 读列数 | 10 / 19 / 12 / 13 / 14 ✓（每表每行字段数集合均为单值） | `_widen_verify.py` |
| 行数未变（无丢行、无灌行） | 64→64 × 5 ✓ | `_manifest_snapshot.py save`→`diff` |
| 其它 74 张表未被本次操作改动 | 数据行 0 变化；表头按快照逐字节复原 ✓ | `_manifest_audit.py` |
| 全表偏窄数 | **12 → 7** ✓ | `_sweep_width_db.py` |

## A.6 ⚠️ 操作要点：`cfgsync` 会覆盖注释表头（本次踩到并已复原）

- **不带 `-bootstrap-csv`**：`SyncAll` 里 `saveHeader(DefaultCSVHeader(spec))` 会**覆盖**
  `meta.cfg_manifest.header_text` ⇒ 76 张表的注释表头被换成兜底表头
  `# ===== <path> (<ID> / <DISP> / reader …) =====`。
- **带 `-bootstrap-csv`**：又会给 **6 张有意为空**的表触发 `importCSVFile`，凭空灌进 64 行占位行
  （`_sweep_width_db.py` §3 那 6 张）。
- ⇒ 正确姿势：跑完 cfgsync 后**必须**检查 `header_text`，必要时从种子注释块或备份复原并重拼 `raw_csv`；
  或走「只手写 DDL + `SyncTableManifest`」的路线。
- 本次复原结果：71 张无关表按快照**逐字节**还原；5 张目标表改用种子注释块（= 旧表头 + 一行补列宽说明）。

## A.7 遗留（未做）

- 剩余 7 张偏窄表（`AI_PARAM` 缺 82 列、`MISSION_XWAR_BANPICK` 39、`COMMANDER_NPC` 37、`MODULE_BONUS` 35、
  `ITEM_PART` 21、`CHALLENGE_HIGHSCORE` 18、`BEGINNER_CHALLENGE` 10）：列语义基本未知，
  需先按 reader 的「固定块循环」逆向出每组列的含义再补。
- ~~`WEAPON_BATTLE_DETAIL` 列漂移（库残留旧列 `attr_value_2`，cfgsync 每次 WARN）：需 `-recreate` + bootstrap
  重建（会丢行）或以 `DROP COLUMN` 清残留，见后续单独处理。~~
  ★**已结（2026-10-05 第三批，见附录 C）**：`attr_value_2` **不是残留**，它就是 `csv3` 的值槽 ——
  把行宽从 3 补到 **9**（`MSMA_BATTLE_DETAIL` 补到 **16**）后漂移自然归 0，
  用 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`（**没走 `-recreate`，9579/5270 行一行没丢**）。
- `LVUP_PILOT_CLASS`：`raw_csv` 宽 15 > 库列 14（历史遗留的"下发比库宽"），本次按现状保留。
