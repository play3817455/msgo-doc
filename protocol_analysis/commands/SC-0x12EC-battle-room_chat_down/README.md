# SC-0x12EC-battle-room_chat_down

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x12EC` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `room_chat_down` |
| 名字字符串 | `)->_proto_battle_client::recv_room_chat_down( `，引用点 `0xB0F96F`（`push offset aProtoBattleCli_17`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0F774` .. `0xB0FBDA` |
| 错误码 | `0x28`（`0xB0F774 push 28h` 守卫 / 读失败与闭合失败处 `0xB0F7DE`、`0xB0F93B`） |
| 关联命令 | 聊天同族：`../SC-0xC1F0-*/`？**见 `notes.md §3`**；本命令与大厅/战服共用的聊天下行链路同型（含「发送者+正文」两串）。**本命令无配对请求**（聊天是单向下行） |

## 2. 结论摘要

- **报文体总长：`10 + (L1+1) + (L2+1) + 3`**（L1 = `pilot_name` 串长 ≤ 24，L2 = `msg` 串长 ≤ 180）。
- 长度校验方式：读完最后一个 `u8` 后 `0xB0F928 mov ebx,[var_1B28]`（线游标）／`0xB0F92C cmp ebx,[var_1B24]`（vs 报文末尾）／`0xB0F932 jz ok` ⇒ 游标必须已在末尾。
- 声明容量：`0xDB`（`0xB0F78D push 0DBh`）＝ `1+1+4+4 + 25 + 181 + 1+1+1` = **219** ⇒ 容量 = **Σ各字段槽预算**（两个 NUL 串按槽位预算 25 / 181 记账，不含实际串长）。
- 变长字段：`pilot_name`（槽位预算 `0x19`＝25）、`msg`（槽位预算 `0xB5`＝181）；两者由 `sub_B02BA0(dst, cursor, maxlen)` 读入，**消费 = 串长 + 1（NUL）**，扫描上限 = `maxlen`。
- 是否分帧：否。
- 关键结论：9 个字段全部经 `vt[0xD4](team, troops, world_id, pilot_id, pilot_name, msg, is_all, is_party, is_audience)`（`0xB0FBBE`）交付；**9 个字段名全部由块内日志串一一对位确证**（`team=` `troops=` `world_id=` `pilot_id=` `pilot_name="` `msg="` `is_all=` `is_party=` `is_audience=`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x12EC` | `0xB0F96F` | 确证 |
| 1 | 0 | 1 | u8 | `team` | 发送者所属队伍 | 交 `vt[0xD4]` 第 1 实参（`movzx` 零扩展）；日志 `team=` | `?`（队伍枚举未交叉） | `0xB0F7CB`（`sub_B06230` 读）、`0xB0F9B9`/`0xB0F9C3`（日志名）、`0xB0FBB8`（去向） | 确证（宽度）/枚举待定 |
| 2 | 1 | 1 | u8 | `troops` | 发送者所属兵种/部队 | 交 `vt[0xD4]` 第 2 实参；日志 `troops=` | `?` | `0xB0F808`（读）、`0xB0F9E0`/`0xB0F9ED`（日志名）、`0xB0FBB0`（去向） | 确证 |
| 3 | 2 | 4 | u32 | `world_id` | 发送者所在世界（大区/场景）ID | 交 `vt[0xD4]` 第 3 实参；日志 `world_id=` | - | `0xB0F82C`（`sub_B02DD0` 读）、`0xB0FA0A`/`0xB0FA19`（日志名）、`0xB0FBA9`（去向） | 确证 |
| 4 | 6 | 4 | u32 | `pilot_id` | 发送者驾驶员 ID | 交 `vt[0xD4]` 第 4 实参；日志 `pilot_id=` | - | `0xB0F850`（读）、`0xB0FA34`/`0xB0FA43`（日志名）、`0xB0FBA4`（去向） | 确证 |
| 5 | 10 | L1+1 | bytes | `pilot_name` | 发送者驾驶员名（NUL 结尾串） | 串指针交 `vt[0xD4]` 第 5 实参；日志 `pilot_name="` | L1 ≤ 24（槽位预算 25） | `0xB0F875`（`sub_B02BA0`，maxlen `0x19`）、`0xB0FA70`（日志名）、`0xB0FBA1`（去向） | 确证 |
| 6 | 10+L1+1 | L2+1 | bytes | `msg` | 聊天正文（NUL 结尾串） | 串指针交 `vt[0xD4]` 第 6 实参；日志 `msg="` | L2 ≤ 180（槽位预算 181） | `0xB0F8A0`（`sub_B02BA0`，maxlen `0xB5`）、`0xB0FAA8`（日志名）、`0xB0FB9C`（去向） | 确证 |
| 7 | 10+L1+L2+2 | 1 | u8 | `is_all` | 是否对全体广播 | 交 `vt[0xD4]` 第 7 实参；日志 `is_all=` | `?`（0/1 未交叉） | `0xB0F8C8`（读）、`0xB0FADB`（日志名）、`0xB0FB91`（去向） | 确证 |
| 8 | 11+L1+L2+2 | 1 | u8 | `is_party` | 是否仅本小队可见 | 交 `vt[0xD4]` 第 8 实参；日志 `is_party=` | `?` | `0xB0F8F0`（读）、`0xB0FB05`（日志名）、`0xB0FB87`（去向） | 确证 |
| 9 | 12+L1+L2+2 | 1 | u8 | `is_audience` | 是否对观战者（audience）可见 | 交 `vt[0xD4]` 第 9 实参；日志 `is_audience=` | `?` | `0xB0F918`（读）、`0xB0FB2A`（日志名）、`0xB0FB7F`（去向） | 确证 |
| - | 13+L1+L2+2 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0xDB` = `1+1+4+4+25+181+1+1+1`（两串按槽预算） | - | `0xB0F92C`|`0xB0F932` | 确证 |

> 偏移列里的 `L1`/`L2` 为两个变长串的**实际串长**（各消耗 `L+1` 字节）；常量部分固定为 `1+1+4+4 = 10`，尾部固定为 `1+1+1 = 3`。

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0F96F` 落在 `sub_B0CC20` 的 case 块 `0xB0F774..0xB0FBDA`。
2. 入口 `call sub_B05DA0`（守卫）→ `push 0DBh; call [edx+78h]`（容量 219）→ `sub_ABB2F0` 初始化线游标。
3. 读取序列（**严格按线序**）：`sub_B05E30`+`sub_B06230`(u8) ×2 → `sub_B41470`+`sub_B02DD0`(u32) ×2 → `sub_B02BA0`(串1，maxlen 0x19) → `sub_B02BA0`(串2，maxlen 0xB5) → `sub_B05E30`+`sub_B06230`(u8) ×3。
4. 闭合：`0xB0F92C`/`0xB0F932`。
5. 去向：`0xB0FB74…0xB0FBBE`（9 次 push，cdecl 逆序）⇒ 声明序 `(team, troops, world_id, pilot_id, pilot_name, msg, is_all, is_party, is_audience)`。

### 4.2 长度闭合
- 常量部分 `1+1+4+4+1+1+1 = 13`，两串 `L1+1` 与 `L2+1` ⇒ 线长 `13 + L1 + L2 + 2`，与「总长」栏一致。
- 闭合点 `0xB0F92C`/`0xB0F932` 要求「游标 == 末尾」✓
- **容量核算**：`0xDB = 219 = 10 + 25 + 181 + 3`；串的 claim 是**槽位预算**（`pilot_name` 槽 25、`msg` 槽 181，即 `sub_B02BA0` 的 `maxlen` 实参），**不是串长** ⇒ 与批次-2/4 的容量口径一致。

### 4.3 存疑点
见 `notes.md`（`team`/`troops`/`is_*` 的枚举与有符号性；`vt[0xD4]` 业务定名）。

## 5. 质量门自检

- [x] G1 字段表总长 `13 + L1 + L2 + 2` 与 `0xB0F92C`/`0xB0F932` 闭合校验一致；容量 `0xDB` 已按「Σ槽预算」解释。
- [x] G2 每个字段类型都指回汇编（`sub_B06230` u8／`sub_B02DD0` u32／`sub_B02BA0` 变长串，串 maxlen 由 `push 19h`/`push 0B5h` 给出）；未使用伪代码类型。
- [x] G3 9 个字段含义全部来自块内日志串（一一对位）；用途指向 `vt[0xD4]`（`0xB0FBBE`，9 实参）。
- [x] G4 不确定项（枚举、`is_*` 有符号性、`vt[0xD4]` 定名）已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 聊天类命令的关联已在 `notes.md §3` 说明（本命令无配对请求）。
