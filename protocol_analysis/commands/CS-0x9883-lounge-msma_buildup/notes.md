# 分析笔记 —— CS-0x9883-lounge-msma_buildup

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0016; call <reg>`（容量 `push` @ `0xB96306`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB964D4`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x106` @ `0xB964EF`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 8(u64) + 4 + 2 + 2 = 18 ≤ 容量 0x16 = 22`（富余 4）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xD8E2-lounge-msma_buildup_r`（已 DONE）
- 相关命令：C→S `CS-0x958A-lounge-msma_buildup_estimate`（同族，ticket_id u32 / usenum u16 / param_idx u16；线长 18 / 容量 22）

## 未决 / 存疑

- `usenum`/`param_idx` 均为 **u16**（写线原语 `sub_B02DA0`），与 `CS-0x958A` 互证一致。
