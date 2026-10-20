# 分析笔记 —— CS-0x9226-lounge-party_info_edit

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x4A; call <reg>`（容量 `push` @ `0xb92696`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 1 + 61(串槽) + 4 = 68 ≤ 容量 0x4A = 74`（富余 6）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x07E8-lounge-party_info_edit_notice`（已 DONE，容量 `0x19E`；元素线长 75/槽 96）构成请求/应答对。
- 与 `CS-0x645D-lounge-party_create`（已 DONE）共享 `is_recruiting` / `comment` / `party_type` 字段结构。

## 未决 / 存疑

- `is_recruiting` 线上 1 字节；`party_type` 取值域 {0,1}（布尔，比较结果直送）。
