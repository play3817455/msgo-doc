# 分析笔记 —— CS-0x9527-lounge-msma_equipset_store

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x86; call <reg>`（容量 `push` @ `0xb98ec6`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8(u64) + 121(equip_set 结构) = 131 ≤ 容量 0x86 = 134`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x7172-lounge-msma_equipset_store_r`（已 DONE；其 `equip_set` claim **128**（`sub_B411D0`）/ 线长 **121**）**精确互证**（本命令的 equip_set 线长同为 121）。
- 与 `CS-0x9A9D-lounge-msma_msset_get`、`CS-0x7306-lounge-msma_msset_apply`（本批）同属编成/套组族。

## 未决 / 存疑

- `equip_set` 为**复合写入器** `sub_B41C60`（`0xB41C60..0xB41D92`）写入，共 **121 字节**（8+2+12+4+4+40+4+4+43），成员名取自打印器 `sub_B4AA30`（`0xb4aa30`）；与 S→C 侧 `SC-0x7172` 的 equip_set 线长 121 一致。
- `eq_weapon[3]` / `eq_modules[10]` / `eq_bonus_modules[1]` / `eq_rental_modules[1]` 均为**固定元素数、无线上计数**（循环上界为字面量）。
- `setname` 为 43 字节定长字符数组（无长度前缀、无 NUL 写入），打印器按 C 串处理 ⇒ 实际内容约定见服务端实现。
