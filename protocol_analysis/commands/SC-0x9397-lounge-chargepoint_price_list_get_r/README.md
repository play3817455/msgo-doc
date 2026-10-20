# SC-0x9397-lounge-chargepoint_price_list_get_r

> 状态：`DONE`（2026-09-20，批次-11）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x9397` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `chargepoint_price_list_get_r` |
| 处理块范围 | `0xb6d145`..`0xb6d749` |
| 名字串引用点 | `0xb6d3f5` |
| 声明容量（解码缓冲） | `0x25`（`B6D15B`） |
| 长度闭合点 | `B6D3B2` |
| 报错码 | `0x42`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0xFC]` @`B6D712`（13 实参） |

## 2. 结论摘要

- **报文体线长**：**37**（全定长）。
- 容量关系：容量 `0x25` = 37 == 线长 ✓。
- 长度闭合：块末 `B6D3B2` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**13**（不含 opcode）；去向：`vt[0xFC]` @`B6D712`（13 实参）。
- 类型：固定。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0x9397` | `0xb6d3f5` | 确证 |
| 1 | 0 | 4 | u32 | `strg_msma` | 储值-机体价（日志串 `strg_msma=`） | 经 `vt[0xFC]` 交业务 | - | `B6D19F`、`B6D44E` | 确证 |
| 2 | 4 | 4 | u32 | `strg_item` | 储值-道具价（日志串 `strg_item=`） | 经 `vt[0xFC]` 交业务 | - | `B6D1E2`、`B6D47B` | 确证 |
| 3 | 8 | 4 | u32 | `clan_emblem` | 战队徽章价（日志串 `clan_emblem=`） | 经 `vt[0xFC]` 交业务 | - | `B6D20C`、`B6D4A8` | 确证 |
| 4 | 12 | 4 | u32 | `clan_npc` | 战队 NPC 价（日志串 `clan_npc=`） | 经 `vt[0xFC]` 交业务 | - | `B6D236`、`B6D4D5` | 确证 |
| 5 | 16 | 4 | u32 | `msma_energy` | 机体能量价（日志串 `msma_energy=`） | 经 `vt[0xFC]` 交业务 | - | `B6D25E`、`B6D4FF` | 确证 |
| 6 | 20 | 4 | u32 | `deckcost` | 编成费价（日志串 `deckcost=`） | 经 `vt[0xFC]` 交业务 | - | `B6D286`、`B6D529` | 确证 |
| 7 | 24 | 4 | u32 | `avatar_reset` | 头像重置价（日志串 `avatar_reset=`） | 经 `vt[0xFC]` 交业务 | - | `B6D2AE`、`B6D553` | 确证 |
| 8 | 28 | 2 | u16 | `periodpath_ticket_0_bc` | 周期通行证 0 价（日志串 `periodpath_ticket_0_bc=`） | 经 `vt[0xFC]` 交业务 | - | `B6D2D6`、`B6D57E` | 确证 |
| 9 | 30 | 2 | u16 | `periodpath_ticket_1_bc` | 周期通行证 1 价（日志串 `periodpath_ticket_1_bc=`） | 经 `vt[0xFC]` 交业务 | - | `B6D2FE`、`B6D5A9` | 确证 |
| 10 | 32 | 2 | u16 | `periodpath_ticket_2_bc` | 周期通行证 2 价（日志串 `periodpath_ticket_2_bc=`） | 经 `vt[0xFC]` 交业务 | - | `B6D326`、`B6D5D4` | 确证 |
| 11 | 34 | 1 | u8 | `periodpath_ticket_0_days` | 周期通行证 0 天数（日志串 `periodpath_ticket_0_days=`） | 经 `vt[0xFC]` 交业务 | - | `B6D34E`、`B6D5FC` | 确证 |
| 12 | 35 | 1 | u8 | `periodpath_ticket_1_days` | 周期通行证 1 天数（日志串 `periodpath_ticket_1_days=`） | 经 `vt[0xFC]` 交业务 | - | `B6D376`、`B6D626` | 确证 |
| 13 | 36 | 1 | u8 | `periodpath_ticket_2_days` | 周期通行证 2 天数（日志串 `periodpath_ticket_2_days=`） | 经 `vt[0xFC]` 交业务 | - | `B6D39E`、`B6D64B` | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B6D3B2` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb6d3f5` 落在处理块 `0xb6d145`..`0xb6d749` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B6D15B` 确证为 `0x25`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B6D3B2`（SOP §5.3）。
5. 去向：`vt[0xFC]` @`B6D712`（13 实参）。

### 4.2 长度闭合与容量口径
- 容量 = `7×4 + 3×2 + 3×1` = **37** == 线长 ✓。

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
