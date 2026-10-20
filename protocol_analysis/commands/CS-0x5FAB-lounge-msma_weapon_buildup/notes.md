# 分析笔记 —— CS-0x5FAB-lounge-msma_weapon_buildup

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x1A; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 4 + 4 + 2 + 2 = 22 ≤ 容量 0x1A=26（富余 4）`

## 与其他命令的关联

- 与 `CS-0x6199-lounge-msma_weapon_buildup_complete`（同 opcode 家族的「完成」侧）字段结构完全一致（22 字节同构）。

## 未决 / 存疑

- ★ 类型以写线原语宽度为准：`ticket_id` 是 **u32**（`sub_B02D80`）、`usenum`/`param_target` 是 **u16**（`sub_B02DA0`）。
- 日志名序（`uniqid_ms=`→`item_id=`→`ticket_id=`→`usenum=`→`param_target=`）与线序一致。
- 与 `CS-0x6199-lounge-msma_weapon_buildup_complete`（同 opcode 家族的「完成」侧）字段结构完全一致（22 字节同构）。
