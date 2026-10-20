# 分析笔记 —— CS-0x7CA0-battle-weapon_fire__shot_single

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x26; call <reg>`（容量 `push` @ `0xb36526`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 2×5 + 1 + 2 + 1 = 20 ≤ 容量 0x26 = 38`（富余 18）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x4E9F-battle-weapon_fire__shot_single_special_r`（已 DONE）同族。
- 与 `CS-0x7C0C-battle-weapon_fire__hand_throw`、`CS-0x8898-battle-weapon_fire__damage_field` 同族。

## 未决 / 存疑

- 坐标点为 u16（写线原语 `sub_B02DA0`）。容量 0x26 富余 18。
