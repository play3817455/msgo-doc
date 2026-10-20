# 分析笔记 —— SC-0xFD8A-examination_progress_r

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自块内 trace 日志串 `examination_info={` / `examination_playscore=` / `examination_playsec_remain_msec=`（@`0xB30DDE` 起），3 个日志名与 3 个字段线序一一对应。
- ★ 容量校验：`0x58`=88 = 5×16 + 4 + 4 ✓（元素 claim 16 == 元素线长 16）。
- `examination_info` 元素 4 个 u32 成员的语义未逐一命名，已记 `?`。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- `examination_info` 元素 4 个 u32 成员的语义未逐一命名，已记 `?`。
