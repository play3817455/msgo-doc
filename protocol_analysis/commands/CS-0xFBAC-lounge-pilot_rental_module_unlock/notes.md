# 分析笔记 —— CS-0xFBAC-lounge-pilot_rental_module_unlock

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 4 + 4 = 10 == 容量 0xA = 10`（**精确相等**）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0x7B30-lounge-pilot_rental_module_unlock_r`。
- 与 S→C `SC-0x7B30-lounge-pilot_rental_module_unlock_r` 配对。

## 未决 / 存疑 / 备注

- 容量与线长**精确相等**（`2+4+4=10==0xA`）⇒ 全定长命令的强证据。
- `count` 为 **u32**（写线 `mov [edx],ecx`，打印器 `sub_B03580`）—— 不可因语义像小计数改窄。
- 附加通知 `[obj+79A8h]` 回调模块 id `0x39`。

## 与其他命令的关联

- SC-0x7B30-lounge-pilot_rental_module_unlock_r

## 服务端实现（本服，2026-09-29 落地）

实现：`serverv/internal/lounge/pilot_unlock.go` 的 `onPilotRentalModuleUnlock`（价目读
`store.LoadModuleRentalConfig`，落库 `store.UnlockPilotRentalModule`）；
验收：`serverv/internal/lounge/pilot_unlock_test.go`（`TestPilotRentalModuleUnlockChargesAccumulatesAndCaps` /
`TestPilotRentalModuleUnlockRejections` / `TestPilotRentalModuleUnlockZeroPriceDoesNotPush`）
+ `serverv/internal/store/pilot_unlock_db_test.go`。

- **落点 = 子表 `game.pilot_detail__hav_rental_modules`**（元素 `rental_module{module_id, count}`，
  128 槽，行键 `(world_id, pilot_id, elem_index)`）：与 `SC-0x063E.pilot_detail.hav_rental_modules`
  的 128×8B 数组是同一份真值。
- **价格来自配置、不来自请求**：请求里只有 `module_id` 与 `count`（没有金额），单价取
  `cfg."MODULE_RENTAL"` 的 `rental_cost_gp`，实扣 `rental_cost_gp × count`；该表里没有这件模块
  ⇒ **直接拒**（`-26002`），**不**兜底成免费。
- **上限 = `cfg."MODULE_RENTAL".max_rental_count`**，按同一 `module_id` 各行的 `count` **求和**
  判"总持有数"（脏库形下同 id 多行也拦得住）。
- **`SC-0x7B30.count` 回的是"成交后那一格的存量"**（复用既有行 ⇒ 原值 + `count`；新建行 ⇒ `count`），
  **不是**请求里的增量：这个量在库里与线上是同一个（`rental_module.count`），对应下行
  `SC-0xFCD2 pilot_rental_module_remain_info_notice` 的"剩余/持有"语义。
- **一个事务**：「锁机师行 → 锁子表全行 → 判上限 → 扣 GP（守卫写在 SQL 的 `WHERE` 里，
  并发不超扣）→ 写子表」；任何一步失败整笔回滚（不会出现"扣了 GP 没到货"）。
- **真扣了钱才推 `0x090C`**（新余额）；价目为 0 时不扣、不推。
- **结果码**（`SC-0x7B30.result`）：`0` / `-10002`（`module_id = 0`、`count = 0`、越权）/
  `-26002`（`cfg."MODULE_RENTAL"` 里没有这件模块、超 `max_rental_count`、子表 128 格满）/
  `-26007`（GP 不足）/ `-10053`（无 `pilot_detail` 行或真库错误）。
- ★**不发 `SC-0xFCD2` 剩余播报**：那张 1536B 包除 `hav_rental_modules`（有真值）还要
  `empty_rental_modules`（128 项"可租/空槽"），后者的口径没有取证 ⇒ 只回配对的 `0x7B30`，
  记在 `docs/01` 的缺口里（与 `msrokaku_deckslot.go`"零负载通知故意不发"同一取舍）。
