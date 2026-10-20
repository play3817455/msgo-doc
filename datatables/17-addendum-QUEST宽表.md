
---

# 附录 B｜第 2 批订正：QUEST 行宽 5→25 · WEAPON_SETTING 15 列确证 · MISSION_COOP col8（2026-10-05）

> 本附录由 `datatables/17-addendum-QUEST宽表.md` 提供，`_sweep_report.py` 生成正文时自动附加（重跑不丢）。
> 脚本：`datatables/_fix_reader_gaps.py`（改 schema）→ `merge_cfg_asm.py`（GM 侧）→ `_widen_seed.py` 同款补宽 → `cfgsync`（库+manifest）→ `_manifest_restore.py`（复原注释表头）。

## B.0 本批结论一览

| 表 | 症状（旧） | 订正 | 依据（VA 可复查） |
|---|---|---|---|
| `QUEST` | `raw_csv`/`cfg.QUEST` 只有 **5** 列（`1,,,,`），reader 读到 **25** 列 | `reward_table_id` `csv_index` **4 → 24**；补 `csv4..csv23` 占位列 ⇒ 行宽 **5 → 25** | `sub_58DCA0`：`push 0/1/2/3` 后 `push 18h`(=**24**) → `mov [edi+40h],eax` @`0x58dd85` |
| `WEAPON_SETTING` | 15 列被标 `gap`（"客户端不读"） | 15 列 `gap → confirmed`（35/37/39/42/44/46/48/50/52/54/58/60/61/62/63） | `sub_597F50` 线性反汇编：`sub_5978A0`/`sub_597D00` 三项块；`sub_5976F0` 内部即 `sub_BBB920` 取列 |
| `MISSION_COOP` | `col8` 标 `gap`；`col5/6/7` 的 `asm_va` **整体后移一格** | `col8 → confirmed`（+56 bit2）；`col5/6/7` VA 回正 | `push 8` @`0x59dd0b` → `sub_BBB370` @`0x59dd14` → `and al,4` / `xor [esi+38h],al` @`0x59dd2d` |

## B.1 `QUEST`：reader 真读 `csv24`，不是 `csv4`（行宽 5 → 25）

**症状**：`cfg.QUEST` 与 manifest `raw_csv` 只有 5 列、64 行（种子行 `1,,,,`），
而 `sub_58DCA0` 的**绝对列号**要到 24。缺的 20 列被 §0.3 的越界兜底吃掉 ⇒ `reward_table_id` 恒为 0
（奖励表行 ID 失效，是**真实数值缺失**，不是"结构合法空表"）。

**根因**：旧 schema 把 asm 里的 `push 18h` 记成了 `csv_index = 4`（`0x18` = 24 被当成 4），
于是 `reward_table_id` 被排在第 5 列，后续 20 个占位列整体不存在。

**订正**：

| 项 | 旧 | 新 |
|---|---|---|
| `reward_table_id.csv_index` / `read_order` | 4 / 5 | **24 / 25** |
| `cfg.QUEST` 物理列数 · manifest 行宽 | 5 · 5 | **25 · 25** |
| 新增列 | — | `col4..col23`（`status: gap`，reader 不读、内存不映射、默认 0） |
| `column_count` / `column_defined` | 5 / 5 | 5 / **25**（`column_count` = reader 映射列数 0,1,2,3,24） |
| 行数 | 64 | 64（**未丢行**） |

**为什么 §2 从来没列过它**：§2 的筛选带了 `not r["emu_err"]`，而 `QUEST` 的仿真**必然失败**
（`UC_ERR_MAP @0xcd2e17`：reader 需要一个可写目标 buffer）⇒ 它被静默排除在"偏窄"清单之外。
⚠️ **这是本次发现的口径漏洞**：EMU-PARTIAL 表的行宽必须另走
`raw_fields < schema_defined`（或静态反汇编）这条线核对，否则漏判。

## B.2 `WEAPON_SETTING`：15 列是"仿真截断假阴性"，不是空列

`sub_597F50` 单函数仿真只走到 `EMU-CUT(limit) eip=0x48303d`（崩前仅取 2 列），
但同一 reader 的三项名字模板块沿线性代码继续读下列列，且 `sub_5976F0` **本身就是** `sub_BBB920` 取列的包装：

| 列 | VA | →内存偏移 | 语义 |
|---|---|---|---|
| 35 | `0x598448` | +112 | `sub_5978A0` 三项名字模板块 |
| 37 | `0x5984a2` | +284 | wstring 原样 |
| 39 | `0x5984f6` | +316 | `sub_BBB920`→`sub_56F550`（条件追加 fx 后缀） |
| 42 / 44 / 46 / 48 / 50 / 52 / 54 | `0x5985ea` … `0x598857` | +376 … +1156 | `sub_5978A0` 三项名字模板块 |
| 58 / 60 / 61 / 62 / 63 | `0x5989b6` … `0x598afb` | +1300 … +1808 | `sub_597D00` 三项派生块（后两项后缀 +10） |

**处理方式（刻意的保守选择）**：只把 `status` 由 `gap` 改为 `confirmed` 并补 `asm_va`/`memory_offset`/语义，
**保留物理列名 `col35`…`col63`**。理由：改名会让 `cfgsync` 判定为"列漂移"从而触发 `-recreate`，
而该表已有 **1648** 行真数据 —— 为改正"标注"去冒丢数据的风险不值得（GM 侧显示名已带语义，见 `column_display_name`）。
`column_count` 108 → **123**（= reader 真读列数；总列 148 不变，仍是 148 列 1648 行）。

## B.3 `MISSION_COOP`：`col8` 真读（+56 bit2）+ `col5/6/7` VA 回正一格

```c
sub_59DC00:
  push 8  @0x59dd0b
  call sub_BBB370  @0x59dd14        // 取 csv8
  add al, al        ×2              // <<2  ⇒ bit2
  and al, 4
  xor [esi+38h], al  @0x59dd2d      // +56 的 bit2
```

- `col8`：`gap → confirmed`，`type: bool`、`memory_offset: 56`、`asm_va: 0x59dd2d`；
  与 `col6`=bit0(`flag_ranked`)、`col7`=bit1(`flag_private`) **同一位域**（+56）⇒ 三列是一组标志位。
- `col5/6/7` 的 `asm_va` 原值各指向**后一列**的位操作（`0x59dcf8`/`0x59dd10`/`0x59dd2d`），回正为
  `0x59dce3`/`0x59dcf8`/`0x59dd10`。列名、偏移、行数**均未变**。
- `column_count` 24 → **25**；物理列 53、行 64 不变。

## B.4 四处同步（本批实际动作）

| 处 | 动作 | 命令 / 文件 |
|---|---|---|
| schema | `csv_index`/`status`/`asm_va`/`memory_offset`/`column_count`/`columns_note` 同步 | `python datatables/_fix_reader_gaps.py` → `db_design/schema/cfg/tables/{QUEST,WEAPON_SETTING,MISSION_COOP}.json` |
| GM schema | 重生 `cfg_schema.json` / `index.json` | `python db_design/tools/merge_cfg_asm.py` |
| 种子 | `QUEST` 补到 25 列（`quest/quest.csv`，64 行）+ 一行 reader 映射注释 | `server/datafiles/lounge/quest/quest.csv`（备份 `datatables/_backup_seeds/`） |
| 库 + 下发 | `-recreate QUEST` 重建 `cfg.QUEST`（25 列序与 `csv_index` 一一对应 + 64 行），其余表只重拼 `raw_csv` | `cd serverv && go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables -recreate QUEST` |
| 表头复原 | `cfgsync` 会覆盖非 bootstrap 表的 `header_text` ⇒ 跑完必须复原 | `python datatables/_manifest_restore.py`（本次：`QUEST` 换种子注释块，其余 **75 张逐字节**复原） |
| 来源文档 | `QUEST` 的 `source_md` 补到 25 列口径（绝对字段号 `0,1,2,3,24` + 跳过 `4..23`）+ 订正节 | `datatables/01-列注释/44-44-QUEST.md` |
| 站点页 | 按新 schema 重生成（`QUEST.html` 含 `col4..col23`/`reward_table_id`） | `python db_design/tools/build_cfg_site.py`（80 页） |
| 对账报告 | §1/§2/§4/§5/§6/§8 按本轮仿真重算 + 本附录 | `python datatables/_sweep_report.py` |

## B.5 验收（全部通过）

| 检查 | 结果 | 脚本 |
|---|---|---|
| `cfg.QUEST` 列序 == schema `csv_index` 序（逐列同名同序） | 25/25 ✓ `… col4 … col23, reward_table_id` | `_probe_three.py` |
| `cfg.QUEST` / manifest 行宽 == reader 最大绝对列号+1 | 25 == 25 ✓；行 64 == 64 ✓ | `_probe_three.py` / `_sweep_width_db.py` |
| `WEAPON_SETTING` 未被本次操作改动 | 148 列 / **1648 行**不变（仅 JSON 标注变） | `_probe_three.py` |
| `MISSION_COOP` 未被本次操作改动 | 53 列 / 64 行不变（仅 JSON 标注变） | `_probe_three.py` |
| 其它表逐字节未变 | manifest 79 行：added `[]`、removed `[]`、**changed 只 1 张**（`QUEST`：937B → 2670B，sha `02d50042` → `4d77e44f`） | `_manifest_snapshot.py diff` |
| §2 偏窄表数 | 7 → **7**（未新增）；`QUEST` 已从"仿真失败漏判"回到列宽达标 | `_sweep_width_db.py` |
| `MISSION_COOP` 读集差异 | 旧 `仿真有schema无=[8]` → **消失**（schema 已含 8） | `_sweep_verdict.py` |
| `QUEST` 仿真 | 仍 `EMU-PARTIAL`（`UC_ERR_MAP`）⇒ 行宽结论**来自静态反汇编**，非仿真 | `_sweep_verdict.py` |
| GM 侧 `serverv/static/cfg_schema.json` | `QUEST` 25 列（`reward_table_id` = `csv_index` **24**，末列）/ `WEAPON_SETTING` 15 列 `confirmed` / `MISSION_COOP` `col8 confirmed` | 本批脚本复核（读 GM schema 断言 `csv_index` 集合 == 0..24） |
| 来源文档 | `01-列注释/44-44-QUEST.md` 与 schema 一致（绝对字段号 + 跳过列说明） | 文档里的 asm 片段对照 `tables_spec.json` 的 `cols[4].col="24"` |
| 站点页 | `db_design/site/cfg/QUEST.html` 含 `col4…col23` + `reward_table_id` | `build_cfg_site.py` |

## B.6 遗留（本批未做）

- §2 剩余 7 张偏窄表列语义未知（见 A.7），需先逆向"固定块循环"每组列含义。
- `WEAPON_SETTING` 物理列名仍是 `col35`…（语义只在 GM 显示名）：
  若日后要改名，必须走「`ALTER TABLE … RENAME COLUMN`」而非 `-recreate`，以免丢 1648 行。
- `WEAPON_SETTING` 仿真截断（`EMU-CUT`）本身未修：需给 `sub_597F50` 提高指令上限 / 补桩，
  才能让 123 列的读集由仿真而非静态反汇编背书。
