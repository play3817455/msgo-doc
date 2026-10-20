# 分析笔记 —— CS-0x6CF9-lounge-clan_memb_exp_use

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 = 6 = 容量 0x6（精确相等）`

## 与其他命令的关联

- 与 S→C `SC-0x4E3E-lounge-clan_memb_exp_use_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`exp=`）与线序一致。
- 与 S→C `SC-0x4E3E-lounge-clan_memb_exp_use_r` 构成请求/应答对。
