# 分析笔记 —— CS-0x5F28-lounge-speedhack_check_response

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 2 + 2 = 6 ≤ 容量 0xA=10（富余 4）`

## 与其他命令的关联

- 与 S→C `SC-0x0A78-lounge-speedhack_check_request` 构成**应答/请求对**（请求为 S→C、回执为 C→S）。

## 未决 / 存疑

- 日志名序（`debugger_found=`→`proc_ref_count=`）与线序一致。
- 两个字段打印器均为 `sub_B032A0`(u16)，与线宽一致。
- 与 S→C `SC-0x0A78-lounge-speedhack_check_request` 构成**应答/请求对**（请求为 S→C、回执为 C→S）。

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onSpeedhackCheckResponse`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatHandlersSendNothing` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。配对 `SC-0x0A78-lounge-speedhack_check_request`
  （出题那条只给一个 `sec`，**不带任何"期望值"**）⇒ 即便出了题这两格也没有可比对的基准
  （它报的是客户端环境的事实）；本服**不出题**（§㊹①）。
- ★`debugger_found` 取值按 field 表只有 `0/1`，但这里**不据此拒收/断线**：判定与执行都在
  "出题"那一半（§㊹①）。
