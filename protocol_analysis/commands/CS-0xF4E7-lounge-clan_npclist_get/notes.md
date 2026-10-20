# 分析笔记 —— CS-0xF4E7-lounge-clan_npclist_get

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B9F6E6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B9F7A4`。
- 容量等式：`2（opcode）== 容量 0x2 = 2（零负载）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0xB514-lounge-clan_npclist_get_r`。

## 未决 / 存疑 / 备注

- **零负载命令**：仅 `mov word ptr [edi], 0F4E7h`（`0xB9F6F9`）写 opcode，容量 2 == 线长 2。
- **触发门与触发点（2026-09-25 当场复核）**：发送器 `sub_B9F6A0` 开头两道闸 ——
  `if (!*((_BYTE*)this + 520)) return 0;`（氏族窗口对象上的"氏族信息已到"标志）与
  `if (!(v2 = *((_DWORD*)this + 3))) return 0;`（**发送侧对象**，`vt[+0x78]` 申请 2 字节缓冲）；
  发完把 `this[5480]`/`this[5481]` 这对 64 位计数器加一（与 `0x4550` 的节流写法同族）。
  **唯一调用链**：军官面板入口 `sub_942870`（打开时把 `this[100]/[102]/[103]` 三个本地状态清零，
  再发这条、再 `sub_762800` 刷面板）← thunk `sub_63BBD0` ← `sub_B00460` ← 发送器（`xrefs_to` 各只有 1 条）。
  ⇒ **命令不带任何参数**（"发给谁"由会话决定），客户端收到应答后自己刷军官列表。
  ★ 这个入口就是 **`L07_ManageOfficer`「长官变更」**窗口（`layout.xml` 的 / `str_table` `82,7,70`），
  它的内容是**可翻页的名录**（详见配对的 `SC-0xB514` notes §名录 vs 名册）。
- ★**零负载的第二条独立佐证**：trace 模板串是 `")<-_proto_lounge_client::send_clan_npclist_get( "` +
  `" ) ["` + `"]byte"` —— **`( ` 与 ` )` 之间没有任何字段位**（这族命令的字段名正是从这条模板读出来的），
  所以"零负载"不只是容量 2 == opcode 2 的推论。
- **服务端落地（本仓库）**：`serverv/internal/lounge/clan_npc_list.go`（`CS-0xF4E7` ⇒ `SC-0xB514`）。
  应答**没有 `result` 字段** ⇒ 拒绝只能表达成空名录；本服只回"本族当下挂着的军官"
  （`game.clan.npc_id`，写侧是 `CS-0x0562`）。
  ⚠ **UI 已定性为"可选名录"**（`L07_ManageOfficer` 是翻页名录 + 确认框 `L07_OfficerChange`，
  见配对 notes）⇒ 只回 1 条会让界面里**只有 1 个候选**，够自洽但换不了人；名录数据仍是欠账。

## 与其他命令的关联

- SC-0xB514-lounge-clan_npclist_get_r（配对；展示侧语义见那边的 `notes.md`）
- CS-0x0562-lounge-clan_npc_update（`game.clan.npc_id` 的唯一写方；本条是它的读侧）
- CS-0xA5BC-lounge-clan_create（建族时写入 `npc_id`，即名录的第一条来源）
