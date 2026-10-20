# 分析笔记 —— CS-0xF0FA-lounge-ranking_clan_get_page

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00BA3C86`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00BA3E1D`。
- 容量等式：`2 + 10(order) + 4 + 1 = 17 ≤ 容量 0x16 = 22（富余 5）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- `order` 线长由写入器 `sub_B42060`（@`0xB42060`..`0xB420D3`，5×u16 = **10B**）确证；配套打印器 `sub_B4F620`（@`0xB4F620`）成员名 `kind=`/`term=`/`filter=`/`reason=`/`troops=`（均 `movzx word` ⇒ u16）。
- `clan_kind` 取值域 {0,1}（0=部隊 1=大会チーム）。
- INDEX 中无同名 `ranking_clan_get_page_r`（S→C）；相近的有 `SC-0x1CF0-lounge-ranking_clan_get_r`（不同命令）。

## 与其他命令的关联

- （无同名 S→C 应答命令）
