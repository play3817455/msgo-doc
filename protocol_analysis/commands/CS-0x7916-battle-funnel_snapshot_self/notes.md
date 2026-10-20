# 分析笔记 —— CS-0x7916-battle-funnel_snapshot_self

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`（容量 `push` @ `0xb3ab99`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 10(snapshot 结构) = 12 ≤ 容量 0xE = 14`（富余 2）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x568A-battle-entity_snapshot` / `SC-0x5EEA-battle-entity_snapshot_splitdelta`（均已 DONE）同属快照族。
- 与 `CS-0x7916` 的漏斗（funnel）对象族命令互证（`funnel_snapshot_self` 上报自身）。

## 未决 / 存疑

- 快照为**复合写入器** `sub_B06850`（`0xB06850..0xB068AD`）：u32 + u8 + u8[5] = **10 字节**，与容量 14 的差额 2（分配富余）。
- `move_info` 的 5 个字节成员未逐一命名（打印器 `sub_B0BF80` 整体打印 `move_info=`），标 `?`。
- `snapshot.wslot_idx` 为 **i8**：打印器用 `movsx`，且写线为单字节 `mov [ecx],dl`。
- **2026-09-30 折单行**：字段表由 3 行 `snapshot.*` 折成 1 行 `struct<funnel_snapshot_entry>`（长度 10）——
  原先前缀名 `snapshot` 让生成器撞上 39B 通用复合体 `snapshot`，生成的 `CS0x7916…Body` 与真包（10B）不符；
  折单行后令牌点名元素复合体 `funnel_snapshot_entry`（与 SC-0x1B67 数组元素同构），生成码变成
  `model.FunnelSnapshotEntry`（`FixedBodySize = 10`）。成员语义不丢，仍在复合体里。见 README §4.4。
