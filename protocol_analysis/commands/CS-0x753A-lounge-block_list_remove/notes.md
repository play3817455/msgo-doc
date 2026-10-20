# 分析笔记 —— CS-0x753A-lounge-block_list_remove

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x2A; call <reg>`（容量 `push` @ `0xb9b766`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 25(串槽) + 4 = 39 ≤ 容量 0x2A = 42`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xDEE3-lounge-block_list_remove_r` 构成请求/应答对。
- 与 `CS-0x921B-lounge-block_list_get_idwlist`、`CS-0x9B54-lounge-block_list_add_r`（已 DONE）同属黑名单族。

## 未决 / 存疑

- `send_sysmes` 为 u32（写线原语 `sub_B02D80`），非 u8——按写线原语判定。
