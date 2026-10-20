# 分析笔记 —— SC-0xFE46-msma_get_buyback_list_r

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自块内 trace 日志串 `ms_list={`（@`0xB88721`）；计数字段日志**未打标签**，命名为推定（记 `?`）。
- ★ 容量校验：`0x79E4`=31204 = 4 + 100×312 ✓（**容量 = 上限场景线长**，由容量反推计数上限 100，与代码里 `cmp ebx,64h` 三方吻合）。
- `ms_list` 元素结构 = `ms_lounge`（303B，见 `db_design/schema/composites/ms_lounge.json`）。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 字段名取自块内 trace 日志串 `ms_list={`（@`0xB88721`）；计数字段日志**未打标签**，命名为推定（记 `?`）。
- `ms_list` 元素结构 = `ms_lounge`（303B，见 `db_design/schema/composites/ms_lounge.json`）。
