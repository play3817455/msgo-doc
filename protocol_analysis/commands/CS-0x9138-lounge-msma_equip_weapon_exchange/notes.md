# 分析笔记 —— CS-0x9138-lounge-msma_equip_weapon_exchange

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12; call <reg>`（容量 `push` @ `0xb93646`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8(u64) + 2 + 2 = 14 ≤ 容量 0x12 = 18`（富余 4）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x2064-lounge-msma_equip_weapon_exchange_r`（已 DONE）构成请求/应答对。
- 与 `CS-0x3FFF-lounge-msma_sp_parts_change`、`CS-0x60FC-lounge-msma_color_change`（均已 DONE）同属装备变更族。

## 未决 / 存疑

- 两个槽位均为 u16（`mov [edx],ax` / `sub_B02DA0`）——不得按语义直觉记成 u32。
