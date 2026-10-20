# 分析笔记 —— CS-0x7AE0-lounge-party_member_kick

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xb924e6`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x5885-lounge-party_member_kick_r` 构成请求/应答对。
- 与 `CS-0x48F2`… 无；与 `CS-0x5F80-lounge-party_leave`、`CS-0x645D-lounge-party_create`（均已 DONE）同族。

## 未决 / 存疑

- 无未决项。
