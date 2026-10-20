# 分析笔记 —— SC-0xFE50-roomlobby_pick_vote_deck

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自块内 trace 日志串 `state=` / `msma_id={` / `enemy_msma_id={`（@`0xB3161D` 起）。
- ★ 容量校验：`0x24`=36 = 4 + 4×4 + 4×4 ✓（两数组均**无线上 count**，上限为字面量 4）。
- 与 C→S `0xFE50` 侧的投票命令族（`0x97EC-roomlobby_pick_vote_r` / `0x7D59-..._result`）配套。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
