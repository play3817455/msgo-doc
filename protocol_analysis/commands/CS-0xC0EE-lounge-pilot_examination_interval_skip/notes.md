# 分析笔记 —— CS-0xC0EE-lounge-pilot_examination_interval_skip

> 状态：`DONE`（2026-09-20，批次-21）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x2; call <reg>`（@ `0xBA60A6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xBA6164`。
- 容量等式：零负载：`2 == 2`（容量 0x2 == 线长 2）。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- ★**零负载 C→S 命令**：容量 `0x2` == 线长 2，全块仅一条 `mov word ptr [edi],0C0EEh` 写 opcode，**无任何字段写入** ⇒ 报文体 0 字节（判据同批次-16/17/18/19/20）。

## 与其他命令的关联

## 服务端实现（2026-09-30，§㊻ 任务/收集/考试收尾族）

- 实现：`serverv/internal/lounge/quest.go` 的 `onPilotExaminationIntervalSkip`；落库
  `serverv/internal/store/quest_ops.go` 的 `SkipExaminationInterval`（两张表一个事务）；
  注册点 `registerQuestHandlers`（← `internal/lounge/handlers.go` 的
  `registerMatchHandlers`，该汇总函数由 `server.go` 的 `registerHandlers` 调用）。
- 落点（运营方裁决 `land_all`）：把该机师的考核 **间隔计数** `interval_cnt` 清零，
  **两张表都清** —— `game.pilot_detail__examination_state`（`pilot_detail.examination_state`
  内嵌复合体 → 1:1 子表，`pilot_select_r` 现在实际投影的那张）与 `game.exam_state`（同一复合体
  在旧模型里的独立表，本服两张都建了）。两表的 `interval_cnt` DDL 注释是**同一行**
  （`间隔计数 [u32] SC-0x063E-lounge-pilot_select_r@0xB423D9`）⇒ 它们承载同一个客户端字段；
  只清一张会让"读回的那张"与"被清的那张"不一致（玩家看到间隔没跳过）。
  `state`/`chances_*`/`playsec_*` 一律**不动**（清零是这一列唯一能被"跳过间隔"表达的动作）。
- 请求零负载 ⇒ "清谁的"由会话（`sess.PilotID`）决定。
- 回执 `SC-0x5B69{result}`：成功 ⇒ 0；两张表都命中 0 行 ⇒ `-10002` + 一条告警日志
  （"这个机师没有考核行"与本命令的语义不符，值得看出来）；DB 故障 ⇒ `-10053`。
- 验收：`internal/store/quest_ops_db_test.go` 的 `TestQuestOpsSkipExaminationInterval`
  （两表都清 + `state`/`chances_total` 不动 + 跨机师隔离 / 只剩 legacy / 两表都空，真库）；
  `internal/lounge/quest_test.go` 的 `TestQuestHandlersRegistered` + `TestQuestHandlersDropMalformed`。
- 留账：原服清零后是否还要写 `state`（例如把"冷却中"改成"可考"）**未取证** ⇒ 本批只清计数。

