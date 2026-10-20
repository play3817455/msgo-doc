# 分析笔记 —— SC-0xFB85-channel_list_select_r

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自块内 trace 日志串 `result=` / `channel_id=` / `loungesv_host=\"` / `loungesv_port=` / `userid=` / `pilot_id=` / `otp=\"`（@`0xB8808F` 起）。
- ★ 容量校验：`0xBE`=190 = 4 + 4 + 129(串槽) + 4 + 4 + 4 + 41(串槽) ✓（串按**槽位预算**计）。
- ★ 该命令与 C→S `0x2830-lounge-channel_list_select` 成对（请求/应答），见 `INDEX`。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
