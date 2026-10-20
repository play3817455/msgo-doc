# 分析笔记 —— CS-0x77C0-battle-examination_progress

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x2; call <reg>`（容量 `push` @ `0xb400b6`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2(opcode) + 0 = 2 == 容量 0x2 = 2`（**零负载**）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xFD8A-battle-examination_progress_r` 构成请求/应答对。
- 与 `CS-0x4E88-lounge-xwar_forcegauge_get` 等零负载族同类。

## 未决 / 存疑

- **零负载 C→S 命令**：容量 2 == 线长 2，全块仅一条 opcode 写入（`mov word ptr [edi],77C0h`@0xB400C9），无任何字段写。
