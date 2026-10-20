# SC-0xA5DA-battle-authenticate_r

> 状态：`DONE`（2026-09-20，批次-11）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xA5DA` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `battle_client` |
| 命令名 | `authenticate_r` |
| 处理块范围 | `0xb25a79`..`0xb262e9` |
| 名字串引用点 | `0xb25e4d` |
| 声明容量（解码缓冲） | `0x2DE`（`B25A8F`） |
| 长度闭合点 | `B25E0A` |
| 报错码 | `0x3`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0x70]` @`B262CD`（15 实参） |

## 2. 结论摘要

- **报文体线长**：**`635 + (L+1)`**（L = `room_name` 串长）。
- 容量关系：容量 `0x2DE` = 734 = `4+4+73+4+4+4+4+4+1+4+1+1+1+1+40+64+2+1+1+516`。
- 长度闭合：块末 `B25E0A` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**20**（不含 opcode）；去向：`vt[0x70]` @`B262CD`（15 实参）。
- 类型：定长 + 变长串 + 多结构体。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xA5DA` | `0xb25e4d` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 认证结果码（日志串 `result=`） | 经 `vt[0x70]` 交业务 | - | `B25AD6`、`B25EA6` | 确证 |
| 2 | 4 | 4 | u32 | `room_id` | 房间 ID（日志串 `room_id=`） | 经 `vt[0x70]` 交业务 | - | `B25B19`、`B25ED3` | 确证 |
| 3 | 8 | L+1 | string | `room_name` | 房间名（日志串 `room_name='...'`；NUL 结尾，槽预算 73） | 经 `vt[0x70]` 交业务 | - | `B25B41`、`B25F03` | 确证 |
| 4 | var | 4 | u32 | `mission_id` | 任务 ID（日志串 `mission_id=`） | 经 `vt[0x70]` 交业务 | - | `B25B7E`、`B25F38` | 确证 |
| 5 | var | 4 | u32 | `extrule_id` | 扩展规则 ID（日志串 `extrule_id=`） | 经 `vt[0x70]` 交业务 | - | `B25BA2`、`B25F62` | 确证 |
| 6 | var | 4 | u32 | `dc_node_id` | 数据中心节点 ID（日志串 `dc_node_id=`） | 经 `vt[0x70]` 交业务 | - | `B25BC6`、`B25F8C` | 确证 |
| 7 | var | 4 | u32 | `is_rankerbattle` | 是否排位战（日志串 `is_rankerbattle=`） | 经 `vt[0x70]` 交业务 | - | `B25BEE`、`B25FB6` | 确证 |
| 8 | var | 4 | u32 | `map_id` | 地图 ID（日志串 `map_id=`） | 经 `vt[0x70]` 交业务 | - | `B25C16`、`B25FE0` | 确证 |
| 9 | var | 1 | u8 | `is_vsclan` | 是否战队战（日志串 `is_vsclan=`，字节打印器） | 经 `vt[0x70]` 交业务 | - | `B25C3E`、`B26008` | 确证 |
| 10 | var | 4 | u32 | `comeback_stat` | 回归状态（日志串 `comeback_stat=`） | 经 `vt[0x70]` 交业务 | - | `B25C66`、`B26034` | 确证 |
| 11 | var | 1 | u8 | `is_playing` | 是否在游戏中（日志串 `is_playing=`） | 经 `vt[0x70]` 交业务 | - | `B25C8E`、`B2605C` | 确证 |
| 12 | var | 1 | u8 | `is_netcafe` | 是否网咖（日志串 `is_netcafe=`） | 经 `vt[0x70]` 交业务 | - | `B25CB6`、`B26086` | 确证 |
| 13 | var | 1 | u8 | `team` | 队伍（日志串 `team=`） | 经 `vt[0x70]` 交业务 | - | `B25CDE`、`B260B0` | 确证 |
| 14 | var | 1 | u8 | `is_practice` | 是否演习（日志串 `is_practice=`） | 经 `vt[0x70]` 交业务 | - | `B25D06`、`B260DA` | 确证 |
| 15 | var | 34 | struct | `config` | 战斗配置（日志串 `config=`；claim 40 / 线长 34） | 经 `vt[0x70]` 交业务 | - | `B25D1F`、`B25D2E`、`B26104` | 确证 |
| 16 | var | 46 | struct | `progress` | 战斗进程（日志串 `progress=`；claim 64 / 线长 46） | 经 `vt[0x70]` 交业务 | - | `B25D47`、`B25D56`、`B2612E` | 确证 |
| 17 | var | 2 | u16 | `expup_fgauge` | 经验加成槽（日志串 `expup_fgauge=`） | 经 `vt[0x70]` 交业务 | - | `B25D7E`、`B2615B` | 确证 |
| 18 | var | 1 | u8 | `is_ev_caravan` | 是否活动商队（日志串 `is_ev_caravan=`） | 经 `vt[0x70]` 交业务 | - | `B25DA6`、`B26183` | 确证 |
| 19 | var | 1 | u8 | `flag_wideuse` | 是否宽用标志（日志串 `flag_wideuse=`） | 经 `vt[0x70]` 交业务 | - | `B25DCE`、`B261AD` | 确证 |
| 20 | var | 514 | struct | `extrarule_xwar_info` | 跨服战扩展规则信息（日志串 `extrarule_xwar_info=`；claim 516 / 线长 514） | 经 `vt[0x70]` 交业务 | - | `B25DE7`、`B25DF6`、`B261D2` | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B25E0A` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb25e4d` 落在处理块 `0xb25a79`..`0xb262e9` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B25A8F` 确证为 `0x2DE`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B25E0A`（SOP §5.3）。
5. 去向：`vt[0x70]` @`B262CD`（15 实参）。

### 4.2 长度闭合与容量口径
- 容量 = Σ 各字段 claim：`result`4 + `room_id`4 + `room_name`串槽 **73**（`push 49h` @`B25B2B`）+ `mission_id`4 + `extrule_id`4 + `dc_node_id`4 + `is_rankerbattle`4 + `map_id`4 + `is_vsclan`1+ `comeback_stat`4 + `is_playing`1 + `is_netcafe`1 + `team`1 + `is_practice`1+ `config` claim **40**（`sub_B418C0`）+ `progress` claim **64**（`sub_B05ED0`）+ `expup_fgauge`2+ `is_ev_caravan`1 + `flag_wideuse`1 + `extrarule_xwar_info` claim **516**（`sub_B05EE0`）= **734** ✓。
- 线长 = 定长部分 **635** + `room_name` 的 `(L+1)`；其中 `config` 实测 34B、`progress` 46B、`extrarule_xwar_info` 514B（均 < 各自 claim）。

### 4.3 结构/数组说明
- `config`：claim 40（`sub_B418C0`）/ 线长 34（`sub_B077B0`：`u16+u32+u32+u16+u32+u32+u32+u16+u32+u32`）。
- `progress`：claim 64（`sub_B05ED0`）/ 线长 46（`sub_B07880`：`u32×4+u32+u16+u16+u8+u8+u32×5`）。
- `extrarule_xwar_info`：claim 516（`sub_B05EE0`）/ 线长 514（`sub_B08160`：`u16 + 128×u32`）；打印器 `sub_B0BEC0` 打印 `extra_rule=`/`param={...}`。

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
