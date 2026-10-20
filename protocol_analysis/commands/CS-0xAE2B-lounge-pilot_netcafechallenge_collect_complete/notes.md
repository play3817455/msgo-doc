# 分析笔记 —— CS-0xAE2B-lounge-pilot_netcafechallenge_collect_complete

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0002; call <reg>`（容量 `push` @ `0xB8EBB6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB8EC74`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x073` @ `0xB8ECB6`（发送成功后的统计/日志钩子）。
- 容量等式：`2 == 容量 0x2 = 2`（**零负载**：无任何字段写线）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xB3D4-lounge-pilot_netcafechallenge_collect_complete_r`（已 DONE）

## 未决 / 存疑

- **零负载命令**：容量 `0x2` == 线长 2，仅写 opcode。

## 服务端实现（2026-09-30，§㊻ 任务/收集/考试收尾族）

- 实现：`serverv/internal/lounge/quest.go` 的 `onPilotNetcafeChallengeCollectComplete`；注册点
  `registerQuestHandlers`（← `internal/lounge/handlers.go`）。
- 处置（运营方裁决 `cfg_existing`，与 `CS-0x2EE8` **完全同形**）：回
  `SC-0xB3D4{result=0, cnt_completed=0, item_id=0, item_cnt=0, money_gp=0}` —— 逐字节全 0。
- ★与 `0x2EE8` 的差别：这张 **有**奖励源（`cfg."NETCAFE_CHALLENGE"` 有
  `challenge_id`(主键) + `reward_gp`/`reward_item_id`/`reward_qty`，三列都有确认过的读表 VA），
  本批**仍然**不发 —— 缺的不是奖励表而是"**发哪一条**"的判据：
  (a) 请求体**零负载** ⇒ 客户端没说这次收哪一条挑战（`challenge_id` 只能来自请求，或来自一条
  "这机师刚通关了哪一条"的记录）；
  (b) 承载"该机师挑战进度"的是 `game.challenge_info`（`0xFA18` 读它）/ `game.netcafe_challenge_info`
  （战斗侧 `SC-0x7626` 读它）——**两张都零写方**，且都只有 `id`/`val`/`sub_val`/`is_clear` 四列、
  **没有"已领"标记**；
  (c) 归位模型里 `netcafe_challenge_info` 的 `views[].commands` 只有战斗侧的 `SC-0x7626`，
  与本条（大厅侧）不是同一条链 ⇒ "哪张表 + 哪一行"两处都无证据。
- ⇒ **不**按 `cfg` 的任一列现发一份：那需要替客户端挑一个 `challenge_id`（做法只能是"挑第一行"
  或"按 cnt 推一行"），两者都是编造，且都没有防重领的列。
- 验收：`internal/lounge/quest_test.go` 的 `TestQuestCollectCompleteRepliesEmpty`（逐字节全 0）、
  `TestQuestHandlersRegistered`、`TestQuestHandlersDropMalformed`。
- 留账（补它需要什么证据）：① "该机师网咖挑战进度"落在 `challenge_info` 还是
  `netcafe_challenge_info`（两表同形、都零写方）；② 这两张表由谁写、`is_clear` 何时置位；
  ③ `0xAE2B` 与原服"通关"事件的因果关系（是先有进度行再收，还是本命令**就是**置位的那一下）
  —— 三样齐了才能接。

