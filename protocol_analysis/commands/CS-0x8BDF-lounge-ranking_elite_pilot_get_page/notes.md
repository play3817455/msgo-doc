# 分析笔记 —— CS-0x8BDF-lounge-ranking_elite_pilot_get_page

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12; call <reg>`（容量 `push` @ `0xba77b6`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 10(order 复合体) + 4 = 16 ≤ 容量 0x12 = 18`（富余 2）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xC5A9-lounge-ranking_elite_pilot_get_page_r`（已 DONE，容量 `0x4E8B`）构成请求/应答对；轻量版 `SC-0xC664`（已 DONE）。
- `order` 结构与 `CS-0x3FAF-lounge-ranking_pilot_get_page`（已 DONE）共享同一写入器 `sub_B42060`（10B = 5×u16）。

## 复合体判定（2026-09-25 闭合，原「未决 / 存疑」）

- 原存疑：`order` 为 `sub_B42060` 写出的 10 字节（5×u16），"成员语义未逐一取证，标 `?`"。
- 取证：`0x8BDF` @ `0xBA77FB` 与 `CS-0x3FAF-lounge-ranking_pilot_get_page` @ `0xBA38AB`
  调的是**同一个函数** `sub_B42060`，摊平同一个入参（arg_0）⇒ 这 10B 逐字段同序，
  就是复合体 `order`。`db_design/schema/composites/order.json` 已有五处成员级取证
  （读者 `sub_B46420` @ `0xB46438`/`0xB4644D`/`0xB46461`/`0xB46475`/`0xB4647D`，
  `asm_verified: true`，线长 = claim = 10）⇒ 不再是"无名位置形"。
- 动作：`fields.csv` 第 2 行线类型 `u16[5]` → `struct`（与 `CS-0x3FAF` 同写法）、
  取值列写「见 §3 结构体」，README §3 同步；本命令登记进 `composites/order.json` 的
  `evidence.commands`（第 6 条线体证据；`protocol_paths` 只留给有**成员级** `wire_sources`
  的那两条，本条没有，故不加）；`_legacy_tables/tbl_order.json` 是冻结的旧库证据，不动。
- 收尾：codecgen 生成码由 `[]uint16` 变 `model.Order` ⇒ 服务端**删掉按位置映射的
  `rankingOrderOfU16`**，`onRankingElitePilotGetPage` 直接用 `req.Order`
  （`internal/lounge/ranking.go`），测试侧的喂参同步改。

## 服务端落地（2026-09-25）

服务端已按本命令接线（`internal/lounge/ranking.go` 的 `onRankingElitePilotGetPage`
⇒ `SC-0xC5A9`，页容量 20、`rankself` 8B u64、一次查询同时取本页与总数）。

