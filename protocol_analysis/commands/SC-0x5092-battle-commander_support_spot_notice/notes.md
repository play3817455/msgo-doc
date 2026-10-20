# 未决问题 / 反例 / 关联 —— SC-0x5092-battle-commander_support_spot_notice

## 1. 本命令要点

- 报文体线长：`4 + 37N`（N = support_spot_count ≤ 30）；容量 `0x784`。
- 元素读取器 `sub_B08220` 消费 37 = `2×u16 + 2×u32 + u8 + 6×u32`。
- **元素槽（64B，行步进 `0x40`）成员名（打印器 `sub_B0C020` 逐字段取证）**：`+0x00 team`(u16)、`+0x02 troops`(u16)、`+0x04 type`(u32)、`+0x08 stat`(u32)、`+0x0C is_lock`(u8)、`+0x10/14/18 pos_x/y/z`(u32)、`+0x1C dir`(u32)、`+0x20 route_no`(u32)、`+0x3C ai_priority`(u32)。
- **去向业务 = `sub_44BB40(容器 app+115364, rows, count)`**（`vt[0x2AC]`@`0xB16F1B`→`BAA530`→`AFC6E0`）。该函数**先整表清空**（`432DC0(容器,_Myfirst,_Mylast)`）再按行追加 **40B/元素**：`+0x00`=循环序号（覆盖线 `team`）、`+0x02`=troops、`+0x04`=type（`==8` 且场景标记 `v9&0x200` → 改 9）、`+0x08/0C/10`=pos×`app+115248`(PosFactor) 过 `AB2C60`、`+0x14`=dir、`+0x18`=0、`+0x1C`=stat、`+0x20`=route_no、`+0x24`=is_lock。⇒ **每个 0x5092 是全量替换，不是增量**；配套点锁见 `SC-0x8D1F`（`vt[0x2B0]`→`440A50` 写元素 `+0x24`）。

## 2. 待补 / 存疑（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| - | - | 本命令无未决项 | - |

## 3. 关联

- **客户端消费链（已取证）**：`SC-0x5092` → `44BB40` 全量填 `app+115364`（40B/元素）；支援窗 `CCommanderSupportWindow`(`8DFBB0`) 按选中 `support_type` 遍历该表、过滤 `element+0x04`，摆 kind-32 `CSupportSpotIcon` 图标；点图标 → `CS-0x6486`（`spt_spot_index` = 表内下标）。
- **点锁**：`SC-0x8D1F`（`vt[0x2B0]`→`440A50`）写同表元素 `+0x24 is_lock`。
- 详见 `serverv/docs/05-战斗客户端状态机.md` §3.6 / §3.7。
- 同批样本见 `_meta\自动化进度.md`「批次记录」的 批次-8 行。
- 方法论：`00-规范-组包格式分析SOP.md` §4/§5/§6/§7；容量口径 `_meta\环境与工具约定.md` §7.5。
- 跨批口径：`_meta\长期记忆.md`（零负载判据 / 槽步进 vs 元素线长 / 分配器指纹 / 守卫与收尾）。
