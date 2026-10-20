# 分析笔记 —— CS-0x60FC-lounge-msma_color_change

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 4 = 14 = 容量 0xE（精确相等）`

## 与其他命令的关联

- 与 S→C `SC-0xA003-lounge-msma_color_change_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`uniqid_ms=`→`color=`）与线序一致。
- 与 S→C `SC-0xA003-lounge-msma_color_change_r` 构成请求/应答对。
