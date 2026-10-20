# 分析笔记 —— CS-0x48F2-lounge-pilot_record_get

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 1 = 11 ≤ 容量 0xE=14（富余 3）`

## 与其他命令的关联

- （见 INDEX 反向表交叉参照）

## 未决 / 存疑

- 日志名序（`pilot_id=`→`world_id=`→`is_checkmedal=`）与线序一致。
- `is_checkmedal` 打印器 `sub_B0C1F0`。
