# 分析笔记 —— CS-0x93EC-lounge-clan_rokaku_ms_deck_check

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x2; call <reg>`（容量 `push` @ `0xba2f86`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2(opcode) + 0 = 2 == 容量 0x2 = 2`（**零负载**）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x89EF-lounge-clan_rokaku_ms_deck_check_r`（已 DONE）构成请求/应答对。

## 未决 / 存疑

- **零负载 C→S 命令**：容量 2 == 线长 2，全块仅一条 opcode 写入（`mov word ptr [edi],93ECh`@0xBA2F99）。
