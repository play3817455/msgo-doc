# 未决问题 / 反例 / 关联 —— SC-0x1600-lounge-clan_leave_r

## 1. 存疑点（已标 `?`）

| # | 项 | 现状 | 待补证据 |
|---|---|---|---|
| 1 | `clan_kind` 枚举 | 名称确证；取值表未交叉 | 与 `0x143D.clan_kind` 对照（同族应同枚举） |
| 2 | `deckcost` 口径 | 名称确证（`deckcost=`）；是「退出后的编成费」还是「本次退出补偿」未定 | 服务端业务实现 / UI 显示点 |
| 3 | `result` 枚举 | 只知结果码 | 与 `0x143D`/`0x15B5` 的 `result` 对照 |
| 4 | `vt[0x424]` 业务定名 | 只知槽号，实参 4 个 | 虚表填充点 |
| 5 | 块首守卫无错误码 | 入口直接 `call sub_B41120`，未 `push` 立即数；错误码只出现在读失败处 | `sub_B41120` 调用约定复核 |

## 2. 反例 / 易错点

- 容量 `0xD` 与 `4+4+1+4` 精确相等 ⇒ 该命令是**全定长强相等**样本；任何把 `clan_kind` 记成 u32 的做法都会多算 3 字节，并被闭合校验否掉。
- `sub_B41470` / `sub_B05E30` 均为**槽预留**，不是字段。
- 去向的 push 顺序为 `deckcost → clan_kind → clan_id → result`（cdecl 逆序）⇒ 声明序 `(result, clan_id, clan_kind, deckcost)`。
- 机器草案与人工结论一致（4 字段 / 13 字节 / 容量 13 == 线长）。

## 3. 关联

- `../SC-0x143D-lounge-clan_create_r/`（`0x143D`）：氏族创建结果（`result` + `clan_kind`）。
- `../SC-0x15B5-lounge-clan_npc_update_r/`（`0x15B5`）：氏族 NPC 更新结果（`result` + `npc_id`）。
- 计数器 `[esi+0x5688]`（64 位）每收一条 +1。
