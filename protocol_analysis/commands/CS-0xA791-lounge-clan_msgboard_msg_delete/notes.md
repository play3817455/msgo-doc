# 分析笔记 —— CS-0xA791-lounge-clan_msgboard_msg_delete

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x000E; call <reg>`（容量 `push` @ `0xBA22C6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xBA2402`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x1D9` @ `0xBA241D`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 8(u64) + 1 = 11 ≤ 容量 0xE = 14`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xAD90-lounge-clan_msgboard_msg_delete_r`（已 DONE）

## 未决 / 存疑

- `clan_kind` 打印器 `sub_B0C1F0`（`movsx`）；线宽 1 字节记 `u8`。
