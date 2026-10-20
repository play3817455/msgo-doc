# 未决问题 / 反例 / 关联 —— SC-0x244E-lounge-btlroom_info_one

## 1. 本命令要点

- 机器草案只抽到 1 个 u8 就止步于 `sub_B41440`（144B 单槽预留），漏掉 `roominfo`/`clan_eff`/`clan_zeon`。
- 三处都是「**线长 ≠ 槽宽**」：`roominfo` 线上 **135** / 槽 **144**；`clan_eff`、`clan_zeon` 各线上 **11** / 槽 **12**。
- 容量 `0xA9 = 169 = 1 + 144 + 12 + 12`（**槽口径**）⇒ 线上限 `1 + 135 + 11 + 11 = 158 ≤ 169`。

## 2. 已定案（原「95B 短形 / 第 12 字节未定名」的收口）

| # | 项 | 结论 | 证据 |
|---|---|---|---|
| 1 | `roominfo` 线长 | **135**（不是早期 README 记的 95） | 读取器 `sub_B44880` 整函数消费 135B；`probe_reader` 在 135 闭合、134 拒绝。旧记 95 = 成员表只列到 `is_lock`（漏列后 7 个成员：`is_vsclan`/`count_eff`/`count_zeon`/`count_max`/`master_pilotid`/`master_worldid`/`master_name`），同族的 `SC-0x6B15` 早已写 `struct<roominfo>`+135 ⇒ 是**单向漏列**，不是第二个线形；幽灵复合体 `roominfo_short` 已删除 |
| 2 | `roominfo` 槽宽 | **144**（0x90）= 内存跨度 **141**（`master_name` 结束于 116+25=141）+ 3B 尾部余量 | `sub_B41440` 的 `add [ecx],90h`；打印器 `sub_B4C0D0` 按内存偏移寻址，`room_name`（73B）后 `room_type`（u32）对齐到 `[+50h]` ⇒ 槽内 **3B 对齐填充**（77→80） |
| 3 | `clan_eff`/`clan_zeon` 线长 | 各 **11** | 读取器 `sub_B45F30` 实测 11 闭合、10 拒绝（`probe_reader`） |
| 4 | **第 12 字节** | 命名为 `clan_*.slot_pad`：**仅内存对齐余量，不在线上** | 槽步进 `sub_B41460` = `0x0C`（12B），而读取器 `sub_B45F30` 消费 11B 即停；11 不是 4/8 的倍数 ⇒ 槽 12 = 11 + 1B 尾部对齐。打印器 `sub_B4EC50` 只列 11B 成员（`clan_id`/`world_id`/`emb_base`/`emb_parts1`/`emb_parts2`），无第 12 个打印点 ⇒ 该字节无线上语义 |
| 5 | 容量口径 | `0xA9 = 169` 按槽记（`1 + 144 + 12 + 12`）；线长 `158` 更小，不矛盾 | `0xB58B72 push 0A9h` |

> 判据写法（本库口径）：**线长 = 读取器消费量**；`slot_pad` 只描述槽内剩余字节，**不进字段表长度求和**。`fields.csv` 里 `clan_*.slot_pad` 与其余 `clan_*.*` 成员行在导入期由 `_overrides/SC-0x244E-lounge-btlroom_info_one.json` 的 `drop: ["clan_*.*"]` 剔除（成员清单由 `composites/clan_eff.json` 承载），故模型线长仍是 `1 + 135 + 11 + 11`。

## 3. 待补 / 存疑（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| 1 | `clan_*.emb_base`/`emb_parts1`/`emb_parts2` 的取值域 | 类型/偏移已确证，取值集合未穷举 | 徽章拼装 UI 消费点（不阻塞组包） |

## 4. 关联

- 同族：`SC-0x6B15-lounge-btlroom_member_detail_get_r`（同用 `struct<roominfo>` / `clan_*` 成员口径）。
- 同批样本见 `_meta\自动化进度.md` 「批次记录」的 批次-6 行。
- 方法论：`00-规范-组包格式分析SOP.md` §4/§5/§6/§7；容量口径 `_meta\环境与工具约定.md` §7.5。
