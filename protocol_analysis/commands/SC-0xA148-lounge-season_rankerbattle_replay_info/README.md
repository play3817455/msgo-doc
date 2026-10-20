# SC-0xA148-lounge-season_rankerbattle_replay_info

> 状态：`DONE`（2026-09-20，批次-11）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xA148` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `season_rankerbattle_replay_info` |
| 处理块范围 | `0xb6f8fe`..`0xb6fae3` |
| 名字串引用点 | `0xb6f9ee` |
| 声明容量（解码缓冲） | `0x2C`（`B6F917`） |
| 长度闭合点 | `B6F9A5` |
| 报错码 | `0x268`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0x5D4]` @`B6FAC7`（2 实参） |

## 2. 结论摘要

- **报文体线长**：**42**（全定长）。
- 容量关系：容量 `0x2C` = 44 = `40`（结构体 claim `sub_B418C0`）+ `4`（`win_troops`）；线长 **38 + 4 = 42**。
- 长度闭合：块末 `B6F9A5` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**2**（不含 opcode）；去向：`vt[0x5D4]` @`B6FAC7`（2 实参）。
- 类型：定长（结构体 + 标量）。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xA148` | `0xb6f9ee` | 确证 |
| 1 | 0 | 38 | struct | `replay_info` | 录像信息结构体（日志串 `replay_info=`；claim 40 / 线长 38） | 经 `vt[0x5D4]` 交业务 | - | `B6F946`、`B6F955`、`B6FA42` | 确证 |
| 2 | 38 | 4 | u32 | `win_troops` | 胜利方部队（日志串 `win_troops=`） | 经 `vt[0x5D4]` 交业务 | - | `B6F995`、`B6FA69` | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B6F9A5` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb6f9ee` 落在处理块 `0xb6f8fe`..`0xb6fae3` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B6F917` 确证为 `0x2C`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B6F9A5`（SOP §5.3）。
5. 去向：`vt[0x5D4]` @`B6FAC7`（2 实参）。

### 4.2 长度闭合与容量口径
- 结构体 `replay_info` 的 claim = `sub_B418C0` 的 `add [ecx],28h` = **40**（结构体跨度）；其读取器 `sub_B47340` 实测消费 **38B** ⇒ claim ≠ 线长。
- 容量 `0x2C` = `40 + 4` = 44；线长 = `38 + 4` = **42**。

### 4.3 结构/数组说明
- `replay_info` 线序（`sub_B47340`）：`u64` + `u32` + `u32` + `u8` + `u8` + `u32×4` + `u32` = **38B**。
- 成员打印器 `sub_B513F0`：`id`、`missionId`、`time`、`troopsA`、`troopsB`、`endDate`、`top_pilot_id_troopsA`、`top_world_id_troopsA`、`top_pilot_id_troopsB`、`top_world_id_troopsB`。

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
