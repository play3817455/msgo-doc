# 未决问题 / 反例 / 关联 —— SC-0x15B5-lounge-clan_npc_update_r

## 1. 存疑点（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| 1 | `npc_id` 来源表 | 名称确证（`npc_id=`），取值集合未交叉 | `datatables/` NPC 定义表 |
| 2 | `result` 枚举 | 只知为结果码 | 与 `0x143D`/`0x1600` 的 `result` 对照是否同一枚举 |
| 3 | `vt[0x444]` 业务定名 | 只知槽号，实参 2 个（result, npc_id） | 虚表填充点 |
| 4 | 「update 什么」 | 命令名为 `clan_npc_update_r`；报文只带 `npc_id`，被更新的具体数据（已在本会话别处下发）未验证 | 与 `0x143D`（创建）执行顺序的服务端日志 |

## 2. 反例 / 易错点

- `sub_B41470` 是 **u32 槽预留**（只 `add [ecx],4`），**不是字段**；字段只有 2 次 bounded 读。
- 实参序为 `(result, npc_id)`（cdecl：`push npc_id` 在前、`push result` 在后）。
- 机器草案与人工结论一致（2 字段 / 8 字节 / 容量 8 == 线长）。

## 3. 关联

- `../SC-0x143D-lounge-clan_create_r/`（`0x143D`）：氏族创建结果（`result` + `clan_kind`）。
- `../SC-0x1600-lounge-clan_leave_r/`（`0x1600`）：氏族退出结果（`result` + `clan_id` + `clan_kind` + `deckcost`）。
- 计数器 `[esi+0x5988]`（64 位）每收一条 +1。
