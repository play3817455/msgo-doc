# 分析笔记 —— CS-0xB235-lounge-season_rankerbattle_get_entitled_pilot_list

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x000E; call <reg>`（容量 `push` @ `0xBA7B56`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xBA7C65`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x258` @ `0xBA7C82`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 10(结构体) = 12 ≤ 容量 0xE = 14`（富余 2）
- 结构体/数组展开：`order` = `kind(u16) + term(u16) + filter(u16) + reason(u16) + troops(u16)` = **10B**（写入器 `sub_B42060` = 5×u16；打印器 `sub_B4F620` 成员名 `kind=`/`term=`/`filter=`/`reason=`/`troops=`）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0x9F9B-lounge-season_rankerbattle_get_entitled_pilot_list_r`（已 DONE）

## 未决 / 存疑

- 结构体线长必须进**写入器函数体**逐字段累加：`sub_B42060`（`0xB42060..0xB420D2`）= 5×u16 = 10B；成员名取自打印器 `sub_B4F620`。
- 容量 14 = `2 + 10 + 2`（富余 2）。
