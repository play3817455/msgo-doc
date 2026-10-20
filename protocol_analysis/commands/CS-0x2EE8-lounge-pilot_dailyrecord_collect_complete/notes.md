# 分析笔记 —— CS-0x2EE8-lounge-pilot_dailyrecord_collect_complete

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0x2`；分配器指纹 @ `0xB8E896`。
- 去向槽：`vt[0x58]`（发送）@ `0xB8E954`。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

## 服务端实现（2026-09-30，§㊻ 任务/收集/考试收尾族）

- 实现：`serverv/internal/lounge/quest.go` 的 `onPilotDailyrecordCollectComplete`；注册点
  `registerQuestHandlers`（← `internal/lounge/handlers.go`）。
- 处置（运营方裁决 `cfg_existing`，即"没有落点列就不编"）：一律回
  `SC-0xDFC2{result=0, cnt_completed=0, item_id=0, item_cnt=0, money_gp=0}` —— 逐字节全 0。
- 为什么**不发奖也不写库**（证据逐条，不是"没做完"）：
  (a) 归位模型里 `game.pdaily`（`schemas/homing/objects/`）的 `writes`/`db_effects` 都是 `[]`，
  `reads` 只有读数那条 `SC-0x81F1` ⇒ **本条没有落点列**；
  (b) 请求体**零负载**（容量 `0x2` == 线长 2）⇒ 客户端没说"收第几条"，而 `game.pdaily` 的行键
  `pdaily_id` 是运营配的条目 ID；
  (c) 表里只有 `id`/`val`/`sub_val`/`is_clear` 四列，**没有"已领/已收"标记** ⇒ 没有任何列能做
  "同一行只发一次"的守卫（双开会双花）；
  (d) `cfg."DAILY_RECORD"` 的 13 列里**没有奖励列** ⇒ 连"该发什么"都指不出来。
- 为什么回"成功 + 全 0"而不是拒答：与同簇的 `SC-0x81F1`/`0xFA18` 既有口径一致 —— 那两条读命令的
  `cnt_completed` 本来就是**恒 0**（"不拿数组现算，那是编造"，见 `pilot_challenge_daily.go` 文件头），
  客户端在这个前提下收到的是"没有新的可收项"，不会显示成错误。
- 验收：`internal/lounge/quest_test.go` 的 `TestQuestCollectCompleteRepliesEmpty`（**逐字节全 0**
  的 18B，不是"解出来像空的"）、`TestQuestHandlersRegistered`（体长 18）、
  `TestQuestHandlersDropMalformed`（零负载仍校验"一个字节都不多"）。
- 留账（补它需要什么证据）：① `game.pdaily` 该由谁写、`is_clear` 由什么事件置位（目前**零写方**
  ⇒ 表永远为空）；② 原服"收"的动作是否需要请求侧带条目 ID（若本条的体在原服不止 0B，本仓库的
  `fields.csv` 会先错，那时要先修线体再谈落点）；③ 每日战绩的奖励表（`cfg."DAILY_RECORD"` 没有
  奖励列 ⇒ 要么有第四张表没被识别，要么奖励挂在别处）。

