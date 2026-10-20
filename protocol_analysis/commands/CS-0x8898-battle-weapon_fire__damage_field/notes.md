# 分析笔记 —— CS-0x8898-battle-weapon_fire__damage_field

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x4A; call <reg>`（容量 `push` @ `0xb3ad7b`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 2×11 + 1×2 + 4×2 + 1 + 2 = 41 ≤ 容量 0x4A = 74`（富余 33）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xA9E7-battle-weapon_fire__damage_field_r`（已 DONE）构成请求/应答对。
- 与 `CS-0x7C0C-battle-weapon_fire__hand_throw`（含 `impact_grenade_id`）、`CS-0x7CA0-battle-weapon_fire__shot_single` 同族。

## 未决 / 存疑

- 坐标/目标点均为 u16（写线原语 `sub_B02DA0`）。
- 容量 0x4A=74 远大于 Σ 线长 41（富余 33，分配上限）。
- ★`fx_opt` 取值域 {0,1}（布尔：写侧调用点 @`0x510E30` 先调 `sub_515690`（包围盒/条件判定，只返回 0/1）再把它作为包装 `sub_B026D0` 第 7 实参送入装配器） ⇒ **不是位掩码**（旧记「位掩码（取值表未取证）」作废）。
