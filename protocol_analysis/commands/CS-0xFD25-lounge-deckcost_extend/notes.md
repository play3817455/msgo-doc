# 分析笔记 —— CS-0xFD25-lounge-deckcost_extend

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 4 + 4 = 10 == 容量 0xA = 10`（**精确相等**）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0x5A2C-lounge-deckcost_extend_r`。
- 与 S→C `SC-0x5A2C-lounge-deckcost_extend_r` 配对（同族 `deckcost_*`）。

## 未决 / 存疑 / 备注

- ★ `use_bc` **语义像布尔，但写线为 u32**（`mov [eax],esi` 取 4 字节入参、打印器 `sub_B03580` 为 u32）⇒ 记 **u32**（与批次-22 `0xE591.use_bc` 同口径）。
- 容量与线长**精确相等**（`2+4+4=10==0xA`）。
- 附加通知 `[obj+79A8h]` 回调模块 id `0x1FC`。

## 与其他命令的关联

- SC-0x5A2C-lounge-deckcost_extend_r

## 字段语义取证（2026-09-24）

- `use_bc` / `token_id` 是**支付方式二选一**，由客户端**自动判定**，不是玩家手填：
  `sub_809420`（延长窗口的支付判定）先用 `sub_60D950`（走 `sub_60D180`）取当前持有
  的「延长券」数量，与需要的份数比较：

```asm
00809420  ...                          ; 取持有券数
0080945C  cmp eax, <需要数>            ; 持有 >= 需要 ?
0080945E  jl  short use_bc_path        ; 不够 → 走 BC
          ; 够 → use_bc=0, token_id=<全局券槽>
use_bc_path:
          ; use_bc=1, token_id=0
```

  ⇒ 服务端收 `use_bc==0` 时才该查 `token_id`；`use_bc!=0` 时 `token_id` 必须为 0
  （客户端自己就是这么发的）。
- 定价来源（BC 路线）：`srv.chargepoint_price`，列 `deckcost`（见 `0012_srv_config.up.sql`
  已给默认值 500）。
- 券的定义来源：`cfg.ITEM_TOKEN`（`token_type` / `token_value` / `expire_rule`）——
  **当前该表在数据侧是空的**（`server\datafiles\lounge\item\token_item.csv` 只有主键 1..64，
  其余列为空），属「数据欠账」；见 `serverv\docs\01-进度-S0-S9.md` 的扩容族小节。
- 本命令**不携带**「涨多少 `deckcost`」的信息（客户端在线长上没有这个字段）⇒ 增量是
  **服务端策略**，得由 `srv.*` 配置决定；`SC-0x5A2C.deckcost` 回的是**新上限的绝对值**
  （判据见 `SC-0x5A2C` 的 `notes.md` §2.1）。
