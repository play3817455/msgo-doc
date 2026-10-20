# 分析笔记 —— CS-0x6142-lounge-pilot_delete

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 4 + 1 = 15 ≤ 容量 0x12=18（富余 3）`

## 与其他命令的关联

- ★ 与 `CS-0x498B-lounge-pilot_rename` 为**同族结构**（troops/slot/pilot_id 头三字段同构同宽）。

## 未决 / 存疑

- 日志名序（`troops=`→`slot=`→`pilot_id=`→`del_kind=`）与线序一致。
- `del_kind` 打印器 `sub_B0C1F0`（按字节取值）。
- ★ 与 `CS-0x498B-lounge-pilot_rename` 为**同族结构**（troops/slot/pilot_id 头三字段同构同宽）。
