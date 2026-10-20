# 分析笔记 —— CS-0xA53B-lounge-result_item_fullopen

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0002; call <reg>`（容量 `push` @ `0xB9ECE6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB9EDA4`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x19D` @ `0xB9EDE6`（发送成功后的统计/日志钩子）。
- 容量等式：`2 == 容量 0x2 = 2`（**零负载**：无任何字段写线）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0x9193-lounge-result_item_fullopen_r`（已 DONE）

## 未决 / 存疑

- **零负载命令**：容量 `0x2` == 线长 2，仅写 opcode。

## 服务端实现（本服，2026-09-29 落地；同日补齐抽取算法）

实现：`serverv/internal/lounge/result_item.go` 的 `onResultItemFullopen`（开箱走
`serverv/internal/store/itembox.go` 的 `OpenResultBoxes`，`MaxOpen = 15`）；
验收：`serverv/internal/lounge/result_item_test.go`（`TestResultItemFullopenOpensAllAndPadsTo15` /
`TestResultItemFullopenSkipsBoxesWithoutDrops`）、
`serverv/internal/store/itembox_test.go`、`serverv/internal/store/itembox_db_test.go`。

**语义**：把结算列表 `game.item_info` 里**每个箱子格**（`is_itmbox != 0`）各开一次，按箱子
`itemid` 升序，每箱按权重抽 1 件（抽取口径见配对上行 `CS-0x2D19` 的笔记），产出写回列表、
由已落地的 `0x9935` 搬进包。

- **箱子数 > 15 ⇒ 只开前 15 个**，其余留到下一次（日志报 `skipped`/`remain`）。★15 是**线格式
  的安全边界**（`SC-0x9193` 是定长 15 格，`gen` 编码器写死这个数，少一格直接编码失败），
  不是策略值 ⇒ 客户端读得下的量就是上限。
- **非箱子的行跳过、不消费**；**没配可掉落行（含权重全 0）的箱子也跳过且不消费**
  （白吃一个箱子不可恢复），跳过数与"收工后还剩几个箱子格"进日志。
- 回执 **15 格零填**：前 n 格 = 开出的东西（按箱子 `itemid` 升序），其余全 0。
- **一件都没开**（列表里没箱子 / 箱子全没配内容）⇒ 15 格全 0。外观与旧行为（拒答）一致，
  但这次是**真值**：库确实一个字节没动（只有"数量 ≤ 0"的脏行会被清账）。
- 应答**没有 `result` 格** ⇒ 拒绝原因只进服务端日志（`store.ItemOpReason.String()`），
  运营据此修配置。**必须回包**（客户端靠回执清界面状态），解不出请求体时才一个字节不回。
- 这一条现在**真的要读库写库**（旧实现零读零写）⇒ 批量账本里从"最小合法包"升到"字段级"。

口径与取舍的完整推导（为什么算法与掉落表是本服的、两阶段消费/发放、并发下只靠 `FOR UPDATE`
会吞产出）：见 `serverv/docs/01-进度-S0-S9.md` ㊷（㊶④ 那份"补它需要什么证据"的清单已因
运营方定调"算法自定"而作废）。
