# 分析笔记 —— CS-0x9765-lounge-quest_clear

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0006; call <reg>`（容量 `push` @ `0xB9D7F6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB9D8EB`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x186` @ `0xB9D906`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0x817D-lounge-quest_clear_r`（已 DONE）

## 未决 / 存疑

- 无。

## 服务端实现（2026-09-30，§㊻ 任务/收集/考试收尾族）

- 实现：`serverv/internal/lounge/quest.go` 的 `onQuestClear`；落库
  `serverv/internal/store/quest_ops.go` 的 `ClaimQuestClear`（一个事务）；注册点
  `registerQuestHandlers`（← `internal/lounge/handlers.go`）。
- 口径（运营方裁决 `row_pay`）：**按 `game.quest_info` 那一行发奖，发完删行**，全在一个事务里：
  `pay_gp → game.pilot_detail.money`、`pay_exp → game.pilot_detail.exp`（两列**同一个** UPDATE，
  见 `creditQuestPay`）、`pay_item_id`/`pay_item_num` → 主栏发货（复用 `grantItemMainBox`，
  即 `0xF72A` 那一套）⇒ 成功才 `DELETE` 那一行。
  ★`pay_msma_id` / `pay_byword_id` **不发**（发机体是另一条链、台词本服没有素材表），
  但会**记进 `pay_comment` 并标 `(未发)`**，运营据此能看出这一行还配了什么（不悄悄吞掉）。
- 为什么必须同事务：分两步做会留下"奖发了任务还在"（可再领 = 复制奖励）或"任务没了奖没发"
  （资产凭空消失）；`-18006`（主栏满）与"没有钱包"都**整笔回滚**，任务行留着让玩家清包再来。
- 回执 `SC-0x817D{result, quest_id, pay_comment}`：`pay_comment` 是**唯一的奖励明细通道**
  （`0x817D` 没有逐项奖励字段），由 `questPayComment` 装配（`gp=`/`exp=`/`item=IDxN`，
  上限 `questPayCommentCap` 截断防越出 cstr 槽 1537）；**失败时不发文案**（避免被改包客户端当成
  "没领也拿到了什么"的证据面）。`result`：没有这一行 ⇒ `-10002`；没有钱包 ⇒ `-10002`；
  主栏满 ⇒ `-18006`；DB 故障 ⇒ `-10053`（与"配置拒"分开，避免让玩家以为任务坏了去反复点）。
- 回执之后的因果推送（只在库真改了**且**回执已发出之后，失败只记日志）：GP > 0 ⇒
  `0x090C pilot_money_update`；发了道具 ⇒ `0xF72A item_add` / `0xD563 item_stack_update`
  （`pushGrantedItem`）。
- 验收：`internal/store/quest_ops_db_test.go` 的 `TestQuestOpsClaimQuestClearHappyPath`
  （钱/经验/道具/删行/二次领取）、`…StacksExisting`（叠加）、`…NoPay`（含"除行键外全 NULL"
  的行）、`…BoxFullRollsBack`（★已入账的 GP 必须随满包一起回滚）、`…NoWallet`（拒且不删行）；
  `internal/lounge/quest_test.go` 的 `TestQuestHandlersRegistered`。
- 留账：`pay_exp` 落到 `exp` 后**没有**对应的窄推送 —— 带经验的推送只有 `SC-0xE3B4
  pilot_level_update`，它要 `lv_new`/`lv_old`/`lv_point`/`deckcost`，把累计经验折成等级要读
  `cfg."LVUP_PILOT"`（**本仓库还没有机师的这条折算**，氏族那条有 `store.ClanLevelForExp`），
  `reason`/`is_penalty` 的取值也没有证据 ⇒ 不凭空组一条会让客户端显示编出来的等级的包。

