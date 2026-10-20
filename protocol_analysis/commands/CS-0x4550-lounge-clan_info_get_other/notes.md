# 分析笔记 —— CS-0x4550-lounge-clan_info_get_other

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 1 = 7 ≤ 容量 0xA=10（富余 3）`

## 与其他命令的关联

- （见 INDEX 反向表交叉参照）

## 未决 / 存疑

- 日志名序（`clan_id=`→`clan_kind=`）与线序一致。
- `clan_kind` 打印器为 `sub_B0C1F0`（打印时按字节取值）。
