# 分析笔记 —— CS-0x522B-lounge-update_check_progress_quest_id

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 = 6 = 容量 0x6（精确相等）`

## 与其他命令的关联

- （见 INDEX 反向表交叉参照）

## 未决 / 存疑

- 日志名序（`quest_id=`）与线序一致。

## 服务端实现（2026-09-30，§㊻ 任务/收集/考试收尾族）

- 实现：`serverv/internal/lounge/quest.go` 的 `onUpdateCheckProgressQuestID`；落库
  `serverv/internal/store/quest_ops.go` 的 `SetCheckProgressQuestID`（窄 UPDATE）；注册点
  `registerQuestHandlers`（← `internal/lounge/handlers.go` 的 `registerHandlers`）。
- 落点：`game.pilot_detail.check_progress_quest_id`（DDL 注释点名
  `进度检查任务 ID [u32] SC-0x063E-lounge-pilot_select_r@0xB42A3D`）。★交叉证据：`SC-0xC9BA
  quest_list_init` 的末字段 `progress_id` 与本列同名同义，而 `0xC9BA` 正是 `game.quest_info`
  全 13 列的读回通道 ⇒ "客户端上报的任务 id 存在这一格"有两处独立指向。
- 处置：写入上报值；**不做存在性校验**（`quest_id` 在 `quest_info` 里没有行也照记——这一格是
  "客户端正在追踪哪一条"，0 是合法值；原服是否校验未取证，见 §㊻ 留账）。
  回执 `SC-0x7470{result, quest_id}`：**只在成功时回显**请求值，失败回 0（与 `0x0C41` 同口径，
  否则客户端会以为服务端收下了）。
- 错误码：没有 `pilot_detail` 行 ⇒ `QuestOpNoWallet` → 通用可发码 `-10002`。
- 验收：`internal/store/quest_ops_db_test.go` 的 `TestQuestOpsSetCheckProgressQuestID`
  （记 7 / 记 0 / 无钱包三条，真库）；`internal/lounge/quest_test.go` 的
  `TestQuestHandlersRegistered` + `TestQuestHandlersDropMalformed`（配对与畸形包）。
- 留账：原服对"未发过的 quest_id"是否拒**未取证**；本条按"客户端自述的追踪目标"照记。

