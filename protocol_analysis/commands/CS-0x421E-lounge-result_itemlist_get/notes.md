# 分析笔记 —— CS-0x421E-lounge-result_itemlist_get

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0x2`；分配器指纹 @ `0xB9EE76`。
- 去向槽：`vt[0x58]`（发送）@ `0xB9EF34`。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/result_item.go` 的 `onResultItemlistGet`（读库在
`serverv/internal/store/result_item.go` 的 `ListResultItems`）；
验收：`serverv/internal/lounge/result_item_test.go`（`TestResultItemWire` /
`TestListResultItemsOrdersAndCaps` / `TestResultItemlistGetFrame`）。

- **落点 = `game.item_info`**（`db_design` 对这条是 `db_effects: []` + "待批次复核补映射"）。
  判据是**逐列对齐**：DDL（迁移 0003）里 `game.item_info` 的四个列注释全部指向
  `SC-0xC4CF-lounge-result_itemlist_get_r`（`itemid`@`0xB4536C` / `id_type`@`0xB45356` /
  `is_itmbox`@`0xB4537E` / `amount`@`0xB45390`，正是该报文的元素读取器 `sub_B45350`
  的四个成员），表注释写"结算物品元素 item_info（8B 线 / 20B 槽）"——线上线长、字段顺序、
  字段名逐项对齐；这张表在本批之前**零读零写**。
- **次序 = `itemid` 升序**（行键是 `uq_game_item_info_world_pilot_itemid`）。下发的 `ritem`
  是**有序数组**、`0x2D19` 的 `acc_index` 是**下标**，两边必须约定同一个序；本服定
  `ORDER BY itemid`（生成的 `ListItemInfoRows` 与锁行查询同序）。
- **上界 23 条**：`SC-0xC4CF` 的客户端读取器循环上界是 `cmp ebx,17h`@`B7829A`（≤ 23），
  解码缓冲 `0x1D0 = 4 + 23×20` 也是这个数 ⇒ 超出的**截断并告警**（线格式的安全边界，
  不是策略值）。落在 `store.ResultItemSlots`。
- **没有行是常态**（新号 / 这一局没掉东西）⇒ 回空列表 + 成功。
- **失败无从回码**（体只有 `ritem_num + ritem`，没有 `result`）⇒ 读库失败回空列表 + 日志，
  与 `0x02EE item_init_get_r` 同一处置。
- ★**顺带确立的语义**（2026-09-29 补 D 批开箱缺口时定，见 `serverv/docs/01-进度-S0-S9.md` ㊷）：
  这一行里的 **`is_itmbox != 0` 就是"这是物品箱"**（线格式自带的判据，不必查任何配置），
  `0x2D19` 单开 / `0xA53B` 全开都只作用于这种行；开箱的产出也写回这张表（新行 `is_itmbox = 0`），
  再由 `0x9935` 搬进背包。本表因此是**进包之前的暂存区**：既是开箱的作用面，也是开箱结果
  的落点。抽取口径与掉落表（`srv.itembox_drop`）见 ㊷。
