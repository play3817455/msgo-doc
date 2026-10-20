# QUEST ｜ `quest/quest.csv`

- **用途**：任务/委托
- 表ID `44` ｜ 下载序 `44` ｜ 类名 `CQuestTable`
- 逐列读取函数 `sub_58DCA0` ｜ **列数 5**（★2026-10-05 订正：reader 读 **5** 列，但**绝对列号到 24** ⇒ 行宽必须 ≥ 25；旧文档把 `push 18h` 记成 CSV# 4）

> ★★ 本表**读取列号不连续**（`0,1,2,3` + `24`）：CSV# 是**绝对字段号**，不是读序。见文末「订正节」。

| 读序 | CSV 字段号 | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `quest_id` | u32 | `+0` | 主键；委托/任务 ID（`0x58dccd`） |
| 2 | `1` | `quest_type` | u32 | `+4` | 任务类型（区分日常/成就/活动，`0x58dcdb`） |
| 3 | `2` | `title` | str | `+8` | 任务标题（wstring，`0x58dcef`） |
| 4 | `3` | `description` | str | `+36` | 任务说明（wstring，`0x58dd3a`） |
| 5 | **`24`** | `reward_table_id` | u32 | `+64` | 奖励表行 ID（**`push 18h`=24** → `mov [edi+40h],eax`，`0x58dd85`） |

- 客户端**跳过**的字段：**`4`…`23`**（共 20 列，`sub_58DCA0` 从不读；填什么都无害，但**必须留位**）。
- 越界列 = 0（`sub_456D90` 兜底）：**若行宽 < 25，`reward_table_id` 恒为 0 ⇒ 任务奖励失效**。

**行格式**（写到字段 24，保留尾逗号）：

`<quest_id>,<quest_type>,<title>,<description>,,,,,,,,,,,,,,,,,,,,<reward_table_id>,`

（`description` 之后连续 20 个空字段 = CSV# 4..23）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。

---

## 订正节（2026-10-05，第 2 批）

### 1. 病：把 `0x18` 当成了 CSV# 4 ⇒ 行宽只有 5，`reward_table_id` 恒为 0

旧文档（本文件旧版 + 由此生成的 `db_design/schema/cfg/tables/QUEST.json`）给出：

| 来源 | 声称的读列 | 行宽 |
|---|---|---|
| 本文件旧版 | `0,1,2,3` + `reward_table_id`@**4** | 5 |
| **ASM 实测** | `0,1,2,3` + `reward_table_id`@**24** | **25** |

`0x18` = 24（不是 4）。旧表把 `reward_table_id` 排在第 5 列 ⇒ 种子/库/manifest 只有 5 列（`1,,,,`），
读字段 24 时越界 ⇒ 空串 ⇒ `atoi` = 0。

### 2. 证据

```asm
sub_58DCA0:
  push 0        ; → mov [edi+0],  eax      0x58dccd
  push 1        ; → mov [edi+4],  eax      0x58dcdb
  push 2        ; → wstring [edi+8]        0x58dcef
  push 3        ; → wstring [edi+24h]      0x58dd3a
  push 18h      ; ★ 24 = 0x18 → mov [edi+40h], eax   0x58dd85
```

静态交叉验证：`reverse-login-chain/formats/tables_spec.json` 的 QUEST 条目
`cols[4].col = "24"`（**原始抽取本来就是 24**）⇒ 本次订正是把 schema 回正到抽取真值，
`colCount = 5` 只是"读了几列"，不是"最大列号"。

### 3. 后果与修复

| 项 | 订正前 | 订正后 |
|---|---|---|
| 行宽（种子 / `cfg.QUEST` / `manifest.raw_csv`） | 5 | **25** |
| `reward_table_id` 读到的值 | 恒 `0`（越界空串） | 取 CSV# 24 |
| 行数 | 64 | 64（未丢行） |

同步文件：`db_design/schema/cfg/tables/QUEST.json`（`csv_index` 4→24、补 `csv4..csv23` gap 列）、
`server/datafiles/lounge/quest/quest.csv`（补到 25 列）、`serverv/static/cfg_schema.json`（GM）、
库表 `cfg.QUEST`（`cfgsync -recreate QUEST`）。验收见 `datatables/17-读表真值全表对账.md` 附录 B。
