# 分析笔记 —— CS-0xD9AE-lounge-ranking_pilot_get

> 状态：`DONE`（2026-09-20，批次-21）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`（@ `0xBA3696`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xBA37A5`。
- 容量等式：`2+10 = 12 ≤ 容量 0xE = 14`（富余 2）。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- `order` 由复合写入器 `sub_B42060` 一次写入 **10 字节**（= 5×u16：`kind`/`term`/`filter`/`reason`/`troops`，见批次-17/20 固化的 `order` 结构定义）。
- 容量 `0xE` = 14 ≥ `2+10` = 12（富余 2）。

## 与其他命令的关联

- **配对命令**：S→C `0xB985-lounge-ranking_pilot_get_r`（`ranking_pilot_get_r`）。
- ★ 与 `CS-0x3FAF-lounge-ranking_pilot_get_page` **共用应答 `0xB985`**，两条的请求只差 4B：
  `0xD9AE` = `order`(10B)；`0x3FAF` = `order`(10B) + `page`(u32)。
- ★ **两条在客户端全库只有一个二选一分叉点**（`sub_648870` @ `0x6488C7`）：
  `page != 0 ⇒ sub_BA3820`（`0x3FAF`）、`page == 0 ⇒ sub_BA3650`（`0xD9AE`）。
  喂进那个分叉的页码一律 `sub_C08A80(...) + 1`（1 基，调用点 `0x957A1B` / `0x9FDEB8` 等）。
- ★ **唯一走 `0xD9AE` 的调用点**：`sub_8958E0`（@ `0x895A09`，登录/大厅横幅
  `L00/BridgeBanner…`），调用形如
  `sub_648870(dword_11EC978, 0, 0, 0, 0, 1, sub_894490, v3, -1)`
  ⇒ 传 `page = 0` 的意思是"**我没指定页**"，而 `order` 被拼成 `{kind:0, term:0, filter:0,
  reason:1, troops:-1}`（= 一份**默认条件**，`troops` 的 -1 在 u16 槽里是 `0xFFFF`）。
- 由此定下服务端口径：`0xD9AE` 是 `0x3FAF` 的"不带页码"变体，回**首屏（`page_now = 1`）**；
  两条的服务端处理是同一条（`internal/lounge/ranking.go` 的 `rankingPilotGetReply`）。
  终端落地记录见 `serverv/docs/01-进度-S0-S9.md`「机师排行榜第三条上行 `0xD9AE` 落地」。

