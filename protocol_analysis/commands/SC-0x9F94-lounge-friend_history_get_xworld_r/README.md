# SC-0x9F94-lounge-friend_history_get_xworld_r

> 状态：`DONE`（2026-09-20，批次-11）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x9F94` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `friend_history_get_xworld_r` |
| 处理块范围 | `0xb6e8db`..`0xb6ec7c` |
| 名字串引用点 | `0xb6eab3` |
| 声明容量（解码缓冲） | `0x352C`（`B6E8ED`） |
| 长度闭合点 | `B6EA6A` |
| 报错码 | `0x159`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0x368]` @`B6EC60`（5 实参） |

## 2. 结论摘要

- **报文体线长**：**`12 + 113·N1 + 4·N2`**（N1/N2 ≤ 100）。
- 容量关系：容量 `0x352C` = 13612 = `4 + 4 + 100×132 + 4 + 100×4`（**上限场景线长**）。
- 长度闭合：块末 `B6EA6A` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**5**（不含 opcode）；去向：`vt[0x368]` @`B6EC60`（5 实参）。
- 类型：定长头 + 两组计数数组。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0x9F94` | `0xb6eab3` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 结果码（日志串 `result=`） | 经 `vt[0x368]` 交业务 | - | `B6E92E`、`B6EB09` | 确证 |
| 2 | 4 | 4 | u32 | `friend_histories_cnt` | 好友履历个数（上界 `cmp ebx,64h` @`B6E98C` ⇒ ≤100） | 驱动元素循环 | 0..100 | `B6E960` | 确证 |
| 3 | 8 | 113·N1 | array<struct,N1> | `friend_histories` | 好友履历列表（日志 `friend_histories={pilot_id,name,last_in,troops,...}`） | 经 `vt[0x368]` 交业务 | N1 ≤ 100 | `B6E99B`、`B6E9BA`、`B6EB24` | 确证 |
| 4 | var | 4 | u32 | `block_widlist_cnt` | 屏蔽世界 ID 个数（上界 `cmp …,64h` @`B6EA01` ⇒ ≤100） | 驱动元素循环 | 0..100 | `B6E9F1` | 确证 |
| 5 | var | 4·N2 | array<u32,N2> | `block_widlist` | 屏蔽世界 ID 列表（日志 `block_widlist={...}`） | 经 `vt[0x368]` 交业务 | N2 ≤ 100 | `B6EA1A`、`B6EA3A`、`B6EB9E` | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B6EA6A` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb6eab3` 落在处理块 `0xb6e8db`..`0xb6ec7c` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B6E8ED` 确证为 `0x352C`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B6EA6A`（SOP §5.3）。
5. 去向：`vt[0x368]` @`B6EC60`（5 实参）。

### 4.2 长度闭合与容量口径
- 容量 = `4`（`result`）+ `4`（`friend_histories_cnt`）+ `100`（`cmp ebx,64h` @`B6E98C`）× `132`（`sub_B415D0` 槽步进 `add [edx],84h` 及循环 `add …,84h` @`B6E9C6`）+ `4`（`block_widlist_cnt`）+ `100`（`cmp …,64h` @`B6EA01`）× `4`（`sub_B41850` 槽步进 4）= **13612** ✓。
- 元素（`friend_histories`）由 `sub_B43100` 读 = **113B**；`block_widlist` 元素为 `u32` = 4B。

### 4.3 结构/数组说明
- `friend_histories` 元素线序（`sub_B43100`，整函数 + 循环展开）：`u32` + `u8×25` + `u32` + `u8/u8/u8` + `u16` + `sub_B068B0`(18) + `u32` + `u8×31` + `u8/u8/u8` + `u32/u32` + `u8/u8` + `u32/u32` + `u8` = **113B**。
- 元素打印器 `sub_B49580` 成员名：`pilot_id`、`name`、`last_in`、`troops`、`level`、`mil_class`、`byword`、`avatar`、`clan_id`、`clan_name`、`clan_emb_base`、`clan_emb_parts1/2`、`clan_memb_exp`、`clan_memb_exp_use`、`channel_id`、`capture_bonus_state`、`capture_bonus_limit`、`rokaku_pt_use`、`state_bits`（部分成员与线序对齐，未逐一强制对位）。

### 4.4 存疑点
见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与客户端长度闭合一致（或已说明为何无法闭合）
- [x] G2 每个字段的线类型都能指回汇编证据 VA，未使用伪代码类型
- [x] G3 每个字段都有含义与用途（或明确标注仅回显/仅日志并给证据）
- [x] G4 不确定项全部显式标 `?` 且已记入 `notes.md`
- [x] G5 `README.md` / `fields.csv` / `asm.md` 三处一致
- [x] G6 INDEX 该行状态与文件夹内容一致（`DONE`）
- [x] G7 有配对请求/应答的命令已互相链接
