# 分析笔记 —— CS-0x83B2-lounge-msma_equip_rental_modules_update_requip

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12C6; call <reg>`（容量 `push` @ `0xb947fa`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 600×8 = 4806 == 容量 0x12C6 = 4806`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x1E8D-lounge-msma_equip_rental_modules_update_requip_r` 构成请求/应答对。
- 与 `CS-0x5D04-lounge-msma_equip_rental_modules_update`（已 DONE，`eq_modules`=`u32[10]`/`eq_rental_modules`=`u32[1]`）同族（租赁模块）。

## 未决 / 存疑

- **「整块定长数组（无线上 count）」形态**：循环上界为**字面量 `cmp eax,258h`=600**，元素步进 8（u64），无计数写入 ⇒ `u64[600]`，线长 4800；容量等式精确：`2 + 4 + 4800 = 4806`。
- 元素为 u64（低 32 位在前写入）；打印器 `sub_B08500` 按 u64 打印。
- 本命令为**全批最大线长**（4806B）；单帧上限 16366B，无需分帧。
