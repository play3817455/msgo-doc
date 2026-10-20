# 分析笔记 —— CS-0x6B74-lounge-bugtrace_report

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x1816; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 3073 + 4 + 3073 = 6160 ≤ 容量 0x1816=6166（富余 6，上限场景）`

## 与其他命令的关联

- 与 S→C `SC-0x6B74-lounge-bugtrace_report_r`（若存在）构成请求/应答对；INDEX 反向表见交叉参照。

## 未决 / 存疑

- 日志名序（`occured_time=`→`pc=`→`stack=`→`excode=`→`exinfo=`）与线序一致。
- 两个串槽预算均为 3073（`push 0xC01`）⇒ 容量按串槽计。
- ★ 与本项目 `topics\20-客户端崩溃取证SOP.md` 的崩溃链一致：`0x6B74` 即客户端崩溃上报（`go_srv.err 0x6B74` 的线上对应命令）。
- 与 S→C `SC-0x6B74-lounge-bugtrace_report_r`（若存在）构成请求/应答对；INDEX 反向表见交叉参照。

## 服务端实现（2026-09-30，§㊺ 杂项收尾族）

- 实现：`serverv/internal/lounge/misc.go` 的 `onBugtraceReport`；注册点
  `registerMiscHandlers`（← `internal/lounge/server.go` 的 `registerHandlers`）。
- 处置：**无同 opcode 的 `_r`**（逐条核过 `gen/opcodes_lounge.go` 的 SC 段 ⇒ "若存在"的
  那条**不存在**）⇒ 解码 + 留证、**零回包**、不落库（同 docs/01 §㊹ 的反外挂上报形状）。
- 日志纪律：两个 3073 串槽走 §㊹ 的 `strBrief(s, 256)`（前 256B + 截断标记，`%q` 转义），
  整段打进日志会把日志冲垮，而"栈有多长"正是留证要看的。
- 验收：`internal/lounge/misc_test.go` 的 `TestMiscSilentHandlersSendNothing`（好包帧数 **0**，
  两个串槽塞满时也 0）、`TestMiscHandlersTolerateBadBody`（7B 半截体 ⇒ 零帧不崩）。
- 配对：无（单向上报）。
- 留账：要不要把崩溃上报变成**可查询的崩溃库**不是本批议题（那要一张**新的**运维表，
  读方不在游戏链路里，正是 `report_batches.py` 拦的"只有自己读"的形状）。
