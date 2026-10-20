# 分析笔记 —— CS-0x457B-lounge-item_use_uniqid_in_lobby

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 2 = 12 ≤ 容量 0xE=14（富余 2）`

## 与其他命令的关联

- （见 INDEX 反向表交叉参照）

## 未决 / 存疑

- u64 写线形态：`mov [eax],esi`（低 32 位）+ `mov [eax+4],esi`（高 32 位），低 32 位在前。
- 日志名序（`uniqid=`→`num=`）与线序一致。

## 服务端实现（本服，2026-09-29 落地；同日补效果层）

实现：`serverv/internal/lounge/item_chain.go` 的 `onItemUseUniqidInLobby`（回执 `SC-0xA3BE`
形状**不变**，只有 `result`；落库在 `serverv/internal/store/item_ops.go` 的
`ConsumeItemByUniqid`，箱子分支进 `serverv/internal/store/itembox.go` 的 `openBagBox`）；
验收：`serverv/internal/lounge/item_chain_test.go`（`TestItemBoxBagOpenFrameSequence` /
`TestItemBoxBagOpenPartialSuccessFrame` / `TestItemBoxBagOpenBoxFullFrame`）、
`serverv/internal/store/itembox_test.go`、`serverv/internal/store/itembox_db_test.go`。

- **语义 = 用掉背包里的一格**。普通道具仍是**纯扣账**（无效果层，口径一字未改）；
  箱子（物品包）**有效果层**：掉落**直接进背包**（`game.item`，复用发货唯一写入口
  `grantItemMainBox`，与 `0x2D19`/`0xA53B` 的"写回结算列表"不同 —— 这里点的是背包，
  没有结算画面可看）。
- **判据（背包这一格是不是箱子）**：取两条的**并集**（`store.isBagItemBox`）——
  ① `cfg."ITEM".item_type = 'ITEMPACK'`（客户端自己的判据：`db_design/schema/cfg/tables/
  ITEM.json` 的枚举 + 真库 8 行 `道具包·01..08`，`item_id` 如 `9010501`）；
  ② `srv.itembox_drop` 里有 `box_itemid = 该 id` 的**任意**一行。★②**故意不带
  `weight > 0`**：`weight = 0` 是"停用而不删行"（0035 口径），只认 `weight > 0` 会让一个
  被停用的箱子掉出判据、被当普通消耗品**白吃**（不可恢复）；开不开得出来由开箱那步的
  `weight > 0` 判（`ItemOpNoDrop`，同 `0x2D19`）。两条查询各自容忍缺表（`isUndefinedTable`）。
- **一次请求开 `n` 个**，`num` 由那一格的 `stack` 夹住（`itemBoxUseCount` = `min(num, stack)`）：
  多报的按"把有的都开掉"处理（每开一个有确定产出，与普通道具"整笔拒"的
  `ItemOpShortStack` 不同）。每个箱子各掷一次加权点（口径同 `0x2D19`：权重 `uint64` 累加，
  按 `drop_itemid` 升序扫累计和）。
- **顺序是"先发货、后扣箱"**（`openBagBox`），两条不变量由此成立：
  1. **背包满 ⇒ 这一个箱子不消费**（`grantItemMainBox` 回 `errItemBoxFull` 时还没扣）
     —— 与"没配掉落就不消费箱子"同一条取舍：宁可少开，不可白吃。
  2. **箱子掉自己**自然正确：先发货叠到**同一格**（`uniqid` 不变），再从那格扣 1
     ⇒ 净变化 0；"先扣后发"会在 `stack = 1` 时先删行再新建，玩家会看到一个**新的 uniqid**。
- **部分是成功**（开了 k 个之后背包满）：回 `ItemOpOK`（库里真改了、产出照推），
  已开的照给，缺的个数只进日志。`SC-0xA3BE` 只有一个 `result` 格，线上表达不了"还剩几个"
  ⇒ 若这里回 `-18006`，调用方会当整笔失败而**不推**已经开出来的箱子格与产出
  （库里却真改了）⇒ 背包与服务端永久不一致。**一个都没开成**才回 `ItemOpBoxFull`（整笔回滚）。
- **推送**（回执已发出且库真改了之后）：
  箱子格 `pushItemOutcome`（`0xD563` 叠格 / `0x8CB2` 删格，`stack = 1` 时是删）
  ＋ 每个掉落 `pushGrantedItem`（`0xF72A` 新格 / `0xD563` 叠格）。失败只记日志
  （`push_common.go` 既定口径）。
- **结果码**（`SC-0xA3BE.result`）：`0` / `-10002`（通用拒绝，含没配可掉落行）/
  `-18006`（`ItemOpBoxFull`，"道具仓库剩余槽不足"—— 大厅用箱子、背包满是玩家唯一能自救的
  情形，比通用码有信息量；这一支**只可能**由箱子路径产生，不改变其它三条命令）。
- **事务形状**：`lockItemByUniqid` 的 `FOR UPDATE` + 唯一发货写入口，拒答一律 `defer tx.Rollback`
  ⇒ "拒答 = 库一个字节没动"（箱子还在背包里）。
