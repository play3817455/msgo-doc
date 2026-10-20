# 分析笔记 —— CS-0xC4A2-lounge-item_use_uniqid_in_battle

> 状态：`DONE`（2026-09-20，批次-21）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`（@ `0xB9A366`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB9A467`。
- 容量等式：`2+8 = 10` **== 容量 0xA = 10**（精确相等）。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- **u64**（低 @`0xB9A3A8` / 高 @`0xB9A3AA`）；容量 `0xA` = 10 = `2+8`（精确相等）。

## 与其他命令的关联

- 同一物品格、同一扣账入口（`store.ConsumeItemByUniqid`），与 `CS-0x457B` 只差"在大厅还是在战斗"：
  `0xC4A2` 传 `OpenBox: false`。

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/item_chain.go` 的 `onItemUseUniqidInBattle`（回 `SC-0xACF7`，
结果码走 `itemOpDeniedCode`；落库在 `serverv/internal/store/item_ops.go` 的
`ConsumeItemByUniqid`）；
验收：`serverv/internal/lounge/item_chain_test.go`（`0xC4A2` 遇箱子的拒答帧用例）、
`serverv/internal/store/itembox_db_test.go`（`OpenBox=false` 遇箱子 ⇒ `ItemOpBoxInBattle`）。

- **语义 = 用掉战斗中那一格**。普通道具仍是**纯扣账**（无效果层，口径一字未改）。
- ★**箱子（物品包）一律拒答且不消费**：判据同 `0x457B`（`store.isBagItemBox` 的并集）。
  战斗里用箱子会命中新增的领域原因 **`ItemOpBoxInBattle`** ⇒ 回**通用码 `-10002`**、
  **零推送**、那格**原样不动**（`defer tx.Rollback`）。
- 为什么拒而不是开：战斗里"掉落怎么推"没有证据（`SC-0xACF7` 只有结果码，战斗链的推送面
  也不同），而白吃一个箱子是**不可恢复**的资产损失 ⇒ 宁可拒。玩家回大厅用 `0x457B` 开。
- 这一条**只影响箱子**：非箱子的战斗使用行为（`Stack < num` 判据、`applyItemConsume`、
  事务形状）与落地前**完全一致**。