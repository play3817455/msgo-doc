# 分析笔记 —— CS-0x6921-lounge-msma_create_estimate

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 2 = 12 ≤ 容量 0xE=14（富余 2）`

## 与其他命令的关联

- 与 S→C `SC-0x129C-lounge-msma_create_estimate_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`ms_plan_id=`→`ticket_id=`→`usenum=`）与线序一致。
- `usenum` 打印器 `sub_B032A0`(u16)。
- 与 S→C `SC-0x129C-lounge-msma_create_estimate_r` 构成请求/应答对。
