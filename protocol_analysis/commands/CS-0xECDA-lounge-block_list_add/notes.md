# 分析笔记 —— CS-0xECDA-lounge-block_list_add

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B9B4D6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B9B6AC`。
- 容量等式：`2 + 4 + 4 + 25(to_pilot_name 槽预算) + 4 = 39 ≤ 容量 0x2A = 42（富余 3）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x9B54-lounge-block_list_add_r`。

## 未决 / 存疑 / 备注

- `send_sysmes` 语义像布尔，但写线原语为 `sub_B02D80`（u32）、打印器为 `sub_B03580`（u32）⇒ 线型记 **u32**。
- `to_pilot_name` 之后的字段偏移浮动（记 `var`）。

## 与其他命令的关联

- SC-0x9B54-lounge-block_list_add_r
