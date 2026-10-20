# 分析笔记 —— CS-0x692B-battle-dynamic_taskforce_order_issue

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x5E; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 1 + 4 + 4 + 51×1 + 4 + 12×2 = 90 ≤ 容量 0x5E=94（上限场景，富余 4）`

## 与其他命令的关联

- 与 S→C `SC-0x483F-battle-dynamic_taskforce_order_result` 构成请求/结果对。

## 未决 / 存疑

- 日志名序（`order_kind=`→`order_param=`→`select_members={`→`select_npcs={`）与线序一致。
- 两个数组计数字段的日志**未单独打标签** ⇒ 字段名 `select_members_num`/`select_npcs_num` 为**推定**（类型/长度/上限已确证）。
- ★ 两数组元素宽度**不同**：成员 u8、NPC u16——须分别按各自写线原语（`sub_B061C0` / `sub_B02DA0`）判宽。
- 与 S→C `SC-0x483F-battle-dynamic_taskforce_order_result` 构成请求/结果对。
