# 分析笔记 —— CS-0x6199-lounge-msma_weapon_buildup_complete

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x1A; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 4 + 4 + 2 + 2 = 22 ≤ 容量 0x1A=26（富余 4）`

## 与其他命令的关联

- ★ **同族互证**：与 `CS-0x5FAB-lounge-msma_weapon_buildup` **字段结构、宽度、顺序完全一致**（同为 22 字节线长、同 26 字节容量），互为交叉验证。

## 未决 / 存疑

- 日志名序（`uniqid_ms=`→`item_id=`→`ticket_id=`→`usenum=`→`param_target=`）与线序一致。
- ★ **同族互证**：与 `CS-0x5FAB-lounge-msma_weapon_buildup` **字段结构、宽度、顺序完全一致**（同为 22 字节线长、同 26 字节容量），互为交叉验证。
