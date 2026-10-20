# 分析笔记 —— CS-0xE41F-lounge-pilot_module_unlock

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B8C106`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B8C1FB`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6（精确相等）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x58FF-lounge-pilot_module_unlock_r`。

## 未决 / 存疑 / 备注

- 无（全部字段 `确证`）。

## 与其他命令的关联

- SC-0x58FF-lounge-pilot_module_unlock_r

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/pilot_unlock.go` 的 `onPilotModuleUnlock`（落库在
`serverv/internal/store/pilot_unlock.go` 的 `UnlockPilotModule`）；
验收：`serverv/internal/lounge/pilot_unlock_test.go`（`TestPilotModuleUnlockAppendsAndIsIdempotent` /
`TestPilotModuleUnlockRejections`）+ `serverv/internal/store/pilot_unlock_db_test.go`。

- **落点 = `game.pilot_detail.hav_modules`**（`BIGINT[]`，线上 `u32[128]`）。`db_design` 对这条是
  `db_effects: []`（"无既有实体/表证据"），本簇落地时按**线形逐位对齐**复核后补上映射 ——
  全协议里"往机师身上加一个模块"的写方只有这一条，而 `SC-0x063E.pilot_detail` 里就是同一个
  128 槽数组。
- **不收费**：全库没有模块的货币价目（`cfg."MODULE"` 全是定义列、`cfg."MODULE_DEVELOP"` 是素材
  配方）⇒ 与配对估价 `0xD969` 恒报 `0/0` 同源。
- **幂等**：已在表里的 id 重发 ⇒ 回 `result = 0`、库里一个字节不动（连点/重发不产生第二格）；
  满表时**已有**的 id 仍幂等成功，新 id 才拒。
- **结果码**（`SC-0x58FF.result`）：`0` / `-10002`（`module_id = 0`、越权、无会话）/ `-26002`
  （128 槽满）/ `-10053`（无 `pilot_detail` 行或真库错误）。应答回显 `module_id`（原样）。
