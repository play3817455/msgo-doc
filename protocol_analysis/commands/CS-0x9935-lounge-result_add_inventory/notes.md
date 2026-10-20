# 分析笔记 —— CS-0x9935-lounge-result_add_inventory

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0002; call <reg>`（容量 `push` @ `0xB9F006`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB9F0C4`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x1A3` @ `0xB9F106`（发送成功后的统计/日志钩子）。
- 容量等式：`2 == 容量 0x2 = 2`（**零负载**：无任何字段写线）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xCFD2-lounge-result_add_inventory`（已 DONE）

## 未决 / 存疑

- **零负载命令**：容量 `0x2` == 线长 2，全块仅一条 `mov word ptr [edi], 9935h` 写 opcode，写线窗口内无任何其它写入。

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/result_item.go` 的 `onResultAddInventory`（落库在
`serverv/internal/store/result_item.go` 的 `AddResultItemsToInventory`）；
验收：`serverv/internal/lounge/result_item_test.go`（`TestResultItemsCommitMovesListIntoBag` /
`TestResultItemsCommitStacksOntoExistingSlot` / `TestResultItemsCommitStopsWhenBoxFull` /
`TestResultItemsCommitDropsZeroAmountRows` / `TestResultItemsCommitEmptyListIsOKAndIdempotent` /
`TestResultAddInventoryFrameRepliesAndPushes` / `TestResultAddInventoryRejectsForeignAccount`）。

- **语义 = 把结算列表搬进道具主栏**。线名（`result_add_inventory`）+ 回执格（`remain_count`）
  合起来只有一个读法：逐条 `grantItemMainBox`（`item_grant.go`，发货的**唯一写入口**），
  **搬走即删行**（同一事务）；`remain_count` = 收工后**还留在列表里**的条数（直接
  `COUNT(*)`，不是 `Total - len(granted)`）。
- **可续 / 部分成功**：主栏满时**就地收工**（已搬走的不回滚），剩下的留在列表里，
  回 `-18006 道具仓库剩余槽不足` + `remain_count > 0`，客户端清包后再发一发从断点接着搬
  —— 这是"批处理 + 剩余计数"这个字段形状存在的理由（做成整笔全或无，那一格就恒为
  `0` 或 `len(列表)`，没有信息量）。
- **`FOR UPDATE` 锁整列**：两个端同时点"全部入库"，不锁会让同一行被搬两次（道具翻倍）。
- **不凭空造道具**：`amount ≤ 0` 的行直接删掉（留着会让 `remain_count` 永不归零 ⇒ 客户端
  无限重发）。`itemid` 超出 u32 值域（`game.item_info.itemid` 是 BIGINT）⇒ 整笔不成，
  **不夹住**（夹住等于发一件别的道具）。
- **回执不含道具列表**（`0xCFD2` 只有 `result + remain_count`，没有 `uniqid`）
  ⇒ 成功的每一件**再推** `0xF72A item_add`（新格）/ `0xD563 item_stack_update`（叠到已有格），
  否则玩家看到"点了入库，背包没变"（同 `onItemcodeInput` 的 ★）。
- **结果码**（`SC-0xCFD2.result`）：`0` / `-18006`（主栏满，`remain_count > 0`）/
  `-10002`（其它拒绝）/ `-10053`（基础设施故障）。会话/归属不过时 `remain_count` 回 0
  （服务端此时无权去数列表）。
- **缺表不当空列表**：`game.item_info` 不存在（迁移 0003 未跑）⇒ 报错，不静默成功。
- ★**顺带确立的语义**（2026-09-29 补 D 批开箱缺口时定，见 `serverv/docs/01-进度-S0-S9.md` ㊷/㊸）：
  列表里 **`is_itmbox != 0` 的行是物品箱**，而这条命令**不认识它们**（线契约就是"把列表整个
  搬走"）⇒ 未开的箱子也会被搬进背包。
- ★**口径已定：不动它**（`0x9935` 一行不改）。这条命令仍是"把列表整个搬走"，`remain_count` /
  `Reason` 的推导不碰；"箱子进背包"从此**不再是死局** —— 背包里的箱子用
  `CS-0x457B item_use_uniqid_in_lobby` 就能开（掉落直接进背包，判据
  `cfg."ITEM".item_type = 'ITEMPACK'` ∪ `srv.itembox_drop` 有条目，见同目录 `CS-0x457B` 的
  「服务端实现」与 `serverv/internal/store/itembox.go`）。
  ⇒ 当初记账的"进包之后再也开不了"这个洞**已闭合**，本命令无须承担任何开箱口径
  （改了反倒要让 `-18006` 去分辨"剩下的是箱子"，属于动已验收的代码）。
