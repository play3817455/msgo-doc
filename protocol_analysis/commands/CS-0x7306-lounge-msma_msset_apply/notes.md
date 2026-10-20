# 分析笔记 —— CS-0x7306-lounge-msma_msset_apply

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`（容量 `push` @ `0xb98cd6`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 2 + 2 = 6 ≤ 容量 0xA = 10`（富余 4）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x0DA1-lounge-msma_msset_apply_r` 构成请求/应答对。
- 与 `CS-0x9A9D-lounge-msma_msset_get` / `CS-0x5C1E-lounge-msma_get_buyback_list` 同属 msset 族。

## 未决 / 存疑

- 两字段均为 u16（写线为 `mov [eax],ax` / `mov [edx],ax`，目标操作数宽度 2）——不得按语义直觉记成 u32。
- `deck_type` 取值域 {0,1}（编成套别下标，实测小集合）；槽查找 `sub_6183B0` 布局 `800*deck_type + 80 + 80*slot` ⇒ 每套 10 槽。
