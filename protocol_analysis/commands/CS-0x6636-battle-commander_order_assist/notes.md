# 分析笔记 —— CS-0x6636-battle-commander_order_assist

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 1 = 3 ≤ 容量 0x6=6（富余 3）`

## 与其他命令的关联

- 与 S→C `SC-0x58FC-battle-commander_order_assist_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`type=`）与线序一致。
- 1 字节字段打印器 `sub_B0C1F0`。
- 与 S→C `SC-0x58FC-battle-commander_order_assist_r` 构成请求/应答对。
