# 分析笔记 —— CS-0x8DEB-lounge-msma_weapon_buildup_reset

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`（容量 `push` @ `0xb976e6`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8(u64) + 4 = 14 == 容量 0xE = 14`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x00F0-lounge-msma_weapon_buildup_reset_r`（已 DONE）构成请求/应答对。
- 与 `CS-0x5FAB-lounge-msma_weapon_buildup`、`CS-0x6199-lounge-msma_weapon_buildup_complete`（均已 DONE）同族。

## 未决 / 存疑

- 无未决项。
