# 分析笔记 —— CS-0xA76E-lounge-msma_msset_store

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0062; call <reg>`（容量 `push` @ `0xB98916`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB98A25`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x129` @ `0xB98A42`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 95(结构体) = 97 ≤ 容量 0x62 = 98`（富余 1）
- 结构体/数组展开：`ms_set` = `uniq_id(u64) + deck_type(u16) + deck_slot(u16) + setname(u8[43]) + msma_uniq_ids(u64[4]) + equip_set_slots(u16[4])` = 8+2+2+43+32+8 = **95B**
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xB8BB-lounge-msma_msset_store_r`（已 DONE，`ms_set` 95B / 槽 96 —— **与本次 C→S 写入器独立算出同值**）

## 未决 / 存疑

- 本命令**无顶层逐字段写线**：唯一字段 `ms_set` 由复合写入器 `sub_B41B10`（`0xB41B10..0xB41BE5`）整块写出，结构体线长必须进函数体逐字段累加（8+2+2+43+32+8 = 95）。
- 字段名取自 `ms_set` 打印器 `sub_B4A7E0` 的成员名（`uniq_id=`/`deck_type=`/`deck_slot=`/`setname=`/`msma_uniq_ids={`/`equip_set_slots={`）。
- 与 S→C `SC-0xB8BB-msma_msset_store_r` 的 `ms_set` **线长 95 跨方向精确互证**。
- 容量 98 = 2 + 95 + 1（富余 1）。
