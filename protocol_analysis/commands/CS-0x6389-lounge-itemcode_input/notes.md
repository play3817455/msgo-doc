# 分析笔记 —— CS-0x6389-lounge-itemcode_input

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x26; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 33(串槽) = 35 ≤ 容量 0x26=38（富余 3）`

## 与其他命令的关联

- 与 S→C `SC-0xC8AF-lounge-itemcode_input_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`code="`）与线序一致；日志名含开引号。
- 与 S→C `SC-0xC8AF-lounge-itemcode_input_r` 构成请求/应答对。
