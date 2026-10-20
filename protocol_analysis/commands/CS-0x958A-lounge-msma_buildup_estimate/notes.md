# 分析笔记 —— CS-0x958A-lounge-msma_buildup_estimate

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x16; call <reg>`（容量 `push` @ `0xb96596`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8(u64) + 4 + 2 + 2 = 18 ≤ 容量 0x16 = 22`（富余 4）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xFEF1-lounge-msma_buildup_estimate_r`（已 DONE，容量 `0x8=4+4`）构成请求/应答对。
- 与 `CS-0x5FAB-lounge-msma_weapon_buildup`（已 DONE，`ticket_id` u32 / `usenum` u16 / `param_target` u16；线长 22 / 容量 26）**同构互证**。

## 未决 / 存疑

- `usenum` / `param_idx` 均为 **u16**（写线原语 `sub_B02DA0`），不得按批次-17 的 `0x5FAB` 直觉套用（该条同为 u16，互证一致）。
