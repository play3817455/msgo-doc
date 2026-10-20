# 分析笔记 —— CS-0x770D-battle-weapon_hit_to

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x14E; call <reg>`（容量 `push` @ `0xb3b7ea`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 4×3 + 8×(4(计数) + 16×2(上限元素)) + 1 + 2 + 2 + 4 + 1 + 1 = 321 ≤ 容量 0x14E = 334`（上限场景，富余 13）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xDDF7-battle-weapon_hit_to_r` 构成请求/应答对。
- 与 `CS-0x8898-battle-weapon_fire__damage_field`、`CS-0x7C0C-battle-weapon_fire__hand_throw`、`CS-0x7CA0-battle-weapon_fire__shot_single` 同属开火/命中上报族（字段命名风格一致：frame_count/msec/charge_lv/AI_ent_id）。

## 未决 / 存疑

- 8 组「计数 + u16 数组」的计数均为 u32 且上限 **16**（`cmp <reg>,10h; ja 出错`），元素线长 **2**；偏移在首个数组之后为变长 ⇒ `fields.csv` 偏移列记 `var`（不编造偏移）。
- `hit_distance` / `body_distance` 的元素打印器为 `sub_B03420`，其余数组为 `sub_B032A0` —— **仅打印格式不同，线上宽度同为 u16**（写线原语均为 `sub_B02DA0`）。
- 容量 0x14E 为上限场景（8 组数组各取 16 元素），Σ 线长 321 ≤ 334。
