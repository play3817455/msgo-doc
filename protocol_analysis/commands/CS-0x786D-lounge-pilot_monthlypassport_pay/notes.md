# 分析笔记 —— CS-0x786D-lounge-pilot_monthlypassport_pay

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xb8f516`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 1 = 3 ≤ 容量 0x6 = 6`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x73F0-lounge-pilot_monthlypassport_pay_r` 构成请求/应答对。
- 与 `CS-0x7421-lounge-pilot_monthlypassport_get`（查询）配对。

## 未决 / 存疑

- 线上宽度 **1 字节**（`mov [eax],cl`）——不得按「path」语义直觉改成字符串/ u32。
- `period_path` 取值域 1..N（1 起的月卡期数下标：`sub_A06C50`@`0xA06C7A` 传 `a2[368] + 1` → `sub_AFEE80` → 装配器 `sub_B8F4D0`@`0xAFEE95`）（**不是** 0 基下标：写入点已 `+1`）。
- 容量富余 3（分配上限 6 = 2+4，实际用 1 字节负载）。
