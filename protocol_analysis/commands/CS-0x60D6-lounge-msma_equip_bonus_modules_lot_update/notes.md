# 分析笔记 —— CS-0x60D6-lounge-msma_equip_bonus_modules_lot_update

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 4 = 14 = 容量 0xE（精确相等）`

## 与其他命令的关联

- 与 S→C `SC-0xB5D6-lounge-msma_equip_bonus_modules_lot_draw_r` / `SC-0xA812-..._get_r` 同族互证。

## 未决 / 存疑

- 日志名序（`uniqid_ms=`→`eq_bonus_modules={`）与线序一致。
- ★ **整块定长数组形态（无线上 count）**：元数由字面量循环上界 1 给出。
- 与 S→C `SC-0xB5D6-lounge-msma_equip_bonus_modules_lot_draw_r` / `SC-0xA812-..._get_r` 同族互证。
