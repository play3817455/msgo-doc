# 未决问题 / 反例 / 关联 —— SC-0x1CF0-lounge-ranking_clan_get_r

## 1. 本命令要点

- 机器草案仅抽到 7 个字段即止步于 `sub_B41220`；**容量 `0x2BDC` 反推**暴露漏读 `order`/`rankself`/两组「计数+数组」/`term_str`(65)/`clan_kind`(1)。
- 两个数组的元素读取器同为 `sub_B46690`，槽步进同为 `sub_B41900` 的 `0x6C = 108`，循环步进亦 `0x6C` ⇒ **三方一致**。
- **元素线长 99**（不是 77）：`sub_B46690` 消费的 `4+4+31+1+4+4+25+1+1+1+1 = 77` 只是
  **打印器列出成员**那一段（`sub_B4FB00` 只打印 11 个成员），读取器在同一趟里还读尾部两个成员：
  `score`（u32 @+77，`0xB4678E`）+ `avatar`（18B @+81，`0xB467A8`）⇒ 77 + 4 + 18 = **99**。
  成员级取证见 `db_design/schema/composites/clan_ranking_entry.json`（13 成员 `asm_verified`、
  `total_bytes: 99` / `memory_claim: 108`）。2026-09-26 闭合，原「77」的记法见 §3。
- `ranking_num ≤ 100`、`topclans_num ≤ 3`、`term_str` 槽 65 —— 与容量反推**双向吻合**（按槽步进记账）。
- 数组元素前 11 个成员名取自打印器 `sub_B4FB00`（`rank`/`clan_id`/`clan_name[31]`/`troops`/`clan_lv`/`leader_pilot_id`/`leader_pilot_name[25]`/`leader_level`/`emb_base`/`emb_parts1`/`emb_parts2`），与 77B 线序逐一对应；尾部两个（`score`/`avatar`）无打印，由读取器 VA 取证。

## 2. 待补 / 存疑（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| 1 | `topclans_num` | 偏移/长度/类型存在不确定性 | 见 §1 要点与 SOP §10.5（必要时去 `unpacked\shell` dump 取证） |
| 2 | `topclans` | 偏移/长度/类型存在不确定性 | 见 §1 要点与 SOP §10.5（必要时去 `unpacked\shell` dump 取证） |
| 3 | `term_str` | 偏移/长度/类型存在不确定性 | 见 §1 要点与 SOP §10.5（必要时去 `unpacked\shell` dump 取证） |
| 4 | `clan_kind` | 偏移/长度/类型存在不确定性 | 见 §1 要点与 SOP §10.5（必要时去 `unpacked\shell` dump 取证） |

## 3. 关联

- 同批样本见 `_meta\自动化进度.md` 「批次记录」的 批次-6 行。
- 方法论：`00-规范-组包格式分析SOP.md` §4/§5/§6/§7；容量口径 `_meta\环境与工具约定.md` §7.5。
- 元素结构：`db_design/schema/composites/clan_ranking_entry.json`（99B 线 / 108B 槽，13 成员全 `asm_verified`）。
- 娘家与落点：`game.clan_ranking_entry`（见 `db_design/docs/05` §9.18「写它的是 `CS-0x050A` / `CS-0xF0FA`」）。

## 4. 已闭合的订正（原记错的记法）

| 项 | 原记 | 订正 | 订正依据 |
|---|---|---|---|
| `order` | 线长 8（4×u16） | **10**（5×u16） | `sub_B46420` 在 10 精确闭合、8 被拒（2026-09-24）；同族 `SC-0x9F9B` 同结构 |
| 数组元素 | 线上 **77B** | **99B**（槽步进 108） | `sub_B46690` 尾部还读 `score`（@+77，`0xB4678E`）与 `avatar`（18B @+81，`0xB467A8`）；`clan_ranking_entry.json` 13 成员逐成员 VA（2026-09-26） |
