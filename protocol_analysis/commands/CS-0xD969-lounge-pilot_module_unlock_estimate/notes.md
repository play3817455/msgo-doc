# 分析笔记 —— CS-0xD969-lounge-pilot_module_unlock_estimate

> 状态：`DONE`（2026-09-20，批次-21）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（@ `0xB8C2B6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB8C3AB`。
- 容量等式：`2+4 = 6` **== 容量 0x6 = 6**（精确相等）。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- 容量 `0x6` = 6 = `2+4`（精确相等）。

## 与其他命令的关联

- 配对：S→C `SC-0xC334-lounge-pilot_module_unlock_estimate_r`；本体：`CS-0xE41F-lounge-pilot_module_unlock`

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/pilot_unlock.go` 的 `onPilotModuleUnlockEstimate`；
验收：`serverv/internal/lounge/pilot_unlock_test.go` 的 `TestPilotModuleUnlockEstimateQuotesZero`。

- **报价恒 `price_gp = price_cp = 0`**，而**不是**"没实现"：全库没有模块的货币价目
  （`cfg."MODULE"` 的列全是定义列 `linked_item_id`/`slot_index`/`param_a/b`/`module_category`/
  `unlock_level`；`cfg."MODULE_DEVELOP"` 是 `module_id` + `develop_time_sec` + `material_item_id`
  + `material_qty` 的**素材配方**），且本体 `0xE41F` 也确实一分钱不收 ⇒ 两条同源。
  同一口径见 `msma_estimate.go`（机体强化/武器强化/机体生产三条也恒 0）。
- **纯报价：不读也不写任何表**（两格只表达"本服这一项不额外收货币"）。
- 唯一拒因 `module_id = 0`（脏包/改包）⇒ `-10002`，但仍**回包**（客户端靠这一帧清界面状态）。
- 不查 `cfg."MODULE"` 里有没有这件模块：那张表是客户端 datafile 的同源副本，查它只会把
  "配置没播种"变成"玩家买不了"（与 `msma_estimate.go` 只查能自证非法的字段同一取舍）。

