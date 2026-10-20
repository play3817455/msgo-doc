# 分析笔记 —— CS-0xEB98-lounge-msma_equip_all_change

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B992E6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B99441`。
- 容量等式：`2 + 8 + 121(equip_set) = 131 ≤ 容量 0x86 = 134（富余 3）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x548D-lounge-msma_equip_all_change_r`。

## 未决 / 存疑 / 备注

- `equip_set` 线长由**写入器函数体逐字段累加**确证（`sub_B41C60` @`0xB41C60`..`0xB41D92`）：`u64` + `u16` + `u32[3]` + `u32` + `u32` + `u32[10]` + `u32[1]` + `u32[1]` + `u8[43]` = **121**；与 S→C `SC-0x7172-lounge-msma_equipset_store_r` 的 equip_set **线长 121 跨方向精确互证**（批次-19 已固化）。
- 配套打印器 `sub_B4AA30`（@`0xB4AA30`）成员名（`uniq_id=`/`slot=`/`eq_weapon={`/`eq_shield=`/`eq_special=`/`eq_modules={`/`eq_bonus_modules={`/`eq_rental_modules={`/`setname=`）与写入器偏移逐一对位。

## 与其他命令的关联

- SC-0x548D-lounge-msma_equip_all_change_r
