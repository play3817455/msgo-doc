# 分析笔记 —— CS-0x5D04-lounge-msma_equip_rental_modules_update

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x36; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 40 + 4 = 54 = 容量 0x36=54（精确相等）`

## 与其他命令的关联

- 与 S→C `SC-0xEE0F-lounge-msma_equip_rental_modules_update_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`uniqid_ms=`→`eq_modules={`→`eq_rental_modules={`）与线序一致。
- ★ **整块定长数组形态（无线上 count）**：数组元数由**字面量循环上界**给出（10 / 1），非线上计数字段；判据 = 循环 `cmp <reg>,<字面量>` + 无 `sub_B02D80` 计数写入。
- ★ **本块没有 `call sub_B02FF0` 提交调用**（本批 50 条中唯一一条）：写线结束后直接进入日志块与发送；闭合由发送侧的 `sub edi, esi; push edi; push esi; call vt[0x58]`（长度 = 游标 − 缓冲首址）完成。⇒ 「提交 = `sub_B02FF0`」**不是绝对判据**，须以「写线事件结束 + 发送长度按游标差计算」为准。
- 与 S→C `SC-0xEE0F-lounge-msma_equip_rental_modules_update_r` 构成请求/应答对。
