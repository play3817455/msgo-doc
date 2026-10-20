# 分析笔记 —— CS-0x4E94-lounge-pilot_avatar_parts_unlock

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 = 10 = 容量 0xA（精确相等）`

## 与其他命令的关联

- 与 `CS-0x2C17-lounge-msma_sort_list` 等属同族 lounge 小命令（同 4B×2 形态）。

## 未决 / 存疑

- 日志名序（`kind=`→`custom_id=`）与线序一致。
- 与 `CS-0x2C17-lounge-msma_sort_list` 等属同族 lounge 小命令（同 4B×2 形态）。
