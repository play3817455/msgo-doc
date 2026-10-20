# 分析笔记 —— CS-0x72F1-lounge-msma_decal_change

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x16; call <reg>`（容量 `push` @ `0xb94a56`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8(u64) + 4 + 8(u64) = 22 == 容量 0x16 = 22`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x69C9-lounge-msma_decal_change_r` 构成请求/应答对。
- 与 `CS-0x60FC-lounge-msma_color_change`（已 DONE）同族（机体外观变更）。

## 未决 / 存疑

- `uniqid_ms`/`uniqid_decal` 为 u64，线上连续 8 字节（低 32 位在前）。
