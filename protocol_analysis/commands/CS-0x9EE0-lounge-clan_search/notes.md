# 分析笔记 —— CS-0x9EE0-lounge-clan_search

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x002A; call <reg>`（容量 `push` @ `0xBA1646`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xBA17EF`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x1CD` @ `0xBA180C`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 31(串槽) + 1 + 1 = 35 ≤ 容量 0x2A = 42`（富余 7）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xD467-lounge-clan_search_r`（已 DONE）
- 相关命令：C→S `CS-0x9EE0` 同族：`CS-0x2749-lounge-clan_search_sortfilter_get` / `CS-0xD77C-lounge-clan_search_random`

## 未决 / 存疑

- `clan_kind` 取值域 {0,1}（0=部隊 / 1=大会チーム；`sub_63CDA0` → `sub_B006F0(…,0,…)`@`0x63CE01`，`sub_697410` → `sub_B006F0(…,1,…)`@`0x697471`）（与 §73 的 `clan_kind` 族同口径）。
- `search_kind` 取值域 {0,1,2,3}（2 位掩码：`sub_93EE30` 里 v11 初值 0，左筛选框命中置 2@`0x93F0D4`，右筛选框命中则 v11 按位或上 1@`0x93F0ED`，再以 `sub_63CDA0(name,v11)`@`0x93F121` 出线）。
