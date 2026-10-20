# 分析笔记 —— CS-0x7B73-lounge-quest_clienttrigger

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xb9d646`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 `CS-0x522B-lounge-update_check_progress_quest_id`、`CS-0x085F-lounge-check_progress_quest`（均已 DONE）同属任务进度族。

## 未决 / 存疑

- `trigger` 取值域 {1,2,3,4,5}（无 0）：1=登录/主界面 2=编成设定完成 3=教程步进 4=一览/榜打开 5=战斗结算。

## 服务端实现（2026-09-30，§㊻ 任务/收集/考试收尾族）

- 实现：`serverv/internal/lounge/quest.go` 的 `onQuestClientTrigger`；落库
  `serverv/internal/store/quest_ops.go` 的 `AdvanceQuestTrigger`（窄 UPDATE）；注册点
  `registerQuestHandlers`（← `internal/lounge/handlers.go`）。
- 处置：把**所有** `game.quest_info.achieve_trigger == trigger` 的行 `achieve_num` 推进 1，
  用 `LEAST(..., GREATEST(COALESCE(achieve_denom,0), 0))` **夹在目标数**上（`denom` 未配 ⇒ 压成
  0 ⇒ 数值不动："没配目标" ≠ 已完成）。请求里只有 `trigger`、**没有** `quest_id` ⇒ 服务端不替
  客户端挑一条；本条只改数、**不新建行**（否则会造出没有 `title`/`pay_*` 的空任务）。
- ★**无应答帧**（线上是单向通知，`gen/opcodes_lounge.go` 的 SC 段里没有同 opcode 的 `_r`）⇒
  一帧都不发；`trigger = 0` 与"命中 0 行"都只记日志（`QuestOpNoTrigger` 与"推了但没命中"分开记，
  便于运营看出是改包还是配置缺行）。
- ★**不推 `SC-0x9D5E quest_list_update`**（运营方裁决 `no_push`）：`0x9D5E` 是**12B 的单条进度
  更新**（`quest_id|achieve_denom|achieve_num`），而列表是另一条 `SC-0xC9BA quest_list_init`；
  本服**还没有任务列表的下发路径**（没有任何 CS/登录流程会发 `0xC9BA`）⇒ 客户端手里没有这份列表，
  为它不认识的 `quest_id` 推 12B 更新没有意义。进度只落库，客户端下次拉到列表时看到新值。
- 验收：`internal/store/quest_ops_db_test.go` 的 `TestQuestOpsAdvanceTrigger`（trigger=0 /
  命中 3 行 / 已满不冲过 denom / `denom` 为 NULL 行 / 跨行跨机师隔离 / 零命中，真库）；
  `internal/lounge/quest_test.go` 的 `TestQuestHandlersRegistered`（显式断言**零帧**）。
- 留账（补推 `0x9D5E` 需要什么证据）：① `SC-0xC9BA` 的**发送时机**（登录？进任务面板？哪个 CS
  触发？注意它是"服务端下发"、没有配对 CS，要找的是"原服在哪个流程里发它"）；② 列表条数上界 31 与
  "配给某机师的任务行可能超过 31"的取舍。

