# 分析笔记 —— CS-0xBCA5-battle-dynamic_taskforce_order_change_party

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x000A; call <reg>`（容量 `push` @ `0xB3F7C6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB3F8F6`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x0FA` @ `0xB3F911`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 1 + 4 = 7 ≤ 容量 0xA = 10`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：相关：S→C `SC-0x483F-battle-dynamic_taskforce_order_result`（已 DONE）
- 相关命令：C→S `CS-0x692B-battle-dynamic_taskforce_order_issue` / `SC-0x54C6-battle-dynamic_taskforce_info_update`

## 未决 / 存疑

- `order_kind` 取值域 {1..15}（战术指挥指令种类；取值点 `sub_62D010(a1,a2)` 的 `switch` 返回 15 个不同值 1..15，@`0x62D030`..`0x62D0F7`）（1..15，无 0；`sub_62D010` 即「界面动作 × 编成」→ 指令号的映射表）。
