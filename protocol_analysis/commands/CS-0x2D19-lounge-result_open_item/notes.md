# 分析笔记 —— CS-0x2D19-lounge-result_open_item

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0x6`；分配器指纹 @ `0xB9EB36`。
- 去向槽：`vt[0x58]`（发送）@ `0xB9EC2B`。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

## 服务端实现（本服，2026-09-29 落地；同日补齐抽取算法）

实现：`serverv/internal/lounge/result_item.go` 的 `onResultOpenItem`（回显读
`serverv/internal/store/result_item.go` 的 `ResultItemAt`；开箱走
`serverv/internal/store/itembox.go` 的 `OpenResultBoxes`）；
验收：`serverv/internal/lounge/result_item_test.go`（`TestResultOpenItemDrawsLoot` /
`TestResultOpenItemIsRefusedAndEchoesSlot`）、
`serverv/internal/store/itembox_test.go`、`serverv/internal/store/itembox_db_test.go`。

**抽取口径 = 本服自定，掉落由 GM 配**（`srv.itembox_drop`，迁移 0035）：

- **认定箱子**：`game.item_info.is_itmbox != 0`（线格式自带这一格，无需查配置）。这一行的
  `itemid` 就是 `srv.itembox_drop.box_itemid`。`is_itmbox = 0` 的行被要求开箱 ⇒ 拒。
- **一次开一格，按 `weight` 加权抽 1 件**：权重和按 `uint64` 累加，掷点 `r ∈ [0, sum)`，
  按 `drop_itemid` 升序扫累计和取第一个 `acc + w > r` 的行（次序是**契约**：同权重不同次序
  会给出不同分布）。`weight = 0` = **永不掉落**（= 停用开关，读取侧 `WHERE weight > 0` 滤掉）。
- **`acc_index` 是 `SC-0xC4CF` 数组的下标** ⇒ 先按下标选目标、**再**清 0 数量的脏行。
- **产出写回结算列表 `game.item_info`**（同 `itemid` 合并 `amount`），不是直接进背包；
  玩家随后用已落地的 `0x9935` 搬进包（断线不丢货，也不给 `game.item` 开第二条写入口）。
- **没有可掉落行（含权重全 0）⇒ 拒答且不消费箱子**：白吃一个箱子不可恢复。
- **★语义翻转**：回执 `SC-0xC452` 只有一件、**连数量格都没有** ⇒ 数量只能落在它新写回的那一
  行里，所以 `id_type`/`itemid` 这一格必须报**抽中的那一件**（不是"你点的那一格"，那是旧行为）。

**拒答**（失败仍回 `-10002` + 回显请求格，库一个字节没动）：

| 情形 | 领域原因 | 线上码 |
|---|---|---|
| `acc_index` 越界 / 列表已空（客户端列表过期） | `no_item` | `-10002` |
| 那一格 `is_itmbox = 0` | `not_a_box` | `-10002` |
| 箱子没配可掉落行 / 权重全 0 | `no_drop` | `-10002` |
| 掉落物的落点是**没被本次消费的箱子格** | `box_conflict` | `-10002` |
| 合并后 `amount` 超出 u16 | `amount_overflow` | `-10002` |

失败时回显 = 列表第 `acc_index` 项（序 = `itemid` 升序 = `SC-0xC4CF` 下发的序），免得客户端
拿回执对不上它点的那行；越界 ⇒ 两格回 0 + 日志记下越界访问。拒答也**必须回包**（客户端靠
应答回执走回调/清界面状态，不回 = 按钮永久点不动）；只有解不出请求体时一个字节不回。

两条开箱命令都**不推背包**（东西还没进包）；回执本身就是"开完了"的通知。

口径与取舍的完整推导（为什么不用 `cfg."ITEMPACK_INFO"`、两阶段消费/发放、`FOR UPDATE` 之外的
咨询锁、`0x9935` 能搬走未开箱子那个记账的洞）：见 `serverv/docs/01-进度-S0-S9.md` ㊷
（㊶④ 那份"补它需要什么证据"的清单已因运营方定调"算法自定"而作废）。
