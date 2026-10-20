# SC-0xB080-lounge-mission_info_update_vs

> 状态：`DONE`（2026-09-20，批次-12）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xB080` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `mission_info_update_vs` |
| 处理块范围 | `0xb726bd`..`0xb72b17` |
| 名字串引用点 | `0xb728c9` |
| 声明容量（解码缓冲） | `0x40B`（`B726D3`） |
| 长度闭合点 | `B72886` |
| 报错码 | `0x5D`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0x13C]` @`B72ACF`（7 实参） |

## 2. 结论摘要

- **报文体线长**：`11 + 4·n₁ + 4·n₂`。
- 容量关系：容量 `0x40B` = 1035 = `4 + 128×4 + 4 + 128×4 + 3`（**精确相等**，上限 128 由 `cmp ebx,80h` 给出）。
- 长度闭合：块末 `B72886` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**7**（不含 opcode）；去向：`vt[0x13C]` @`B72ACF`（7 实参）。
- 类型：含 2 组「计数 + u32 数组」。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xB080` | `0xb728c9` | 确证 |
| 1 | 0 | 4 | u32 | `exvs_num` | exvs 任务 ID 数量（上限 128） | 驱动 mission_ids_exvs 数组循环（`cmp ebx,80h`） | 0..128 | B72706|B7272F | 确证 |
| 2 | 4 | 4·n₁ | array<u32,128> | `mission_ids_exvs` | 参加演习(VS)的任务 ID 列表（日志串 `mission_ids_exvs={...}`） | 经 `vt[0x13C]` 交业务（7 实参） | - | B72741|B7275E|B7276A | 确证 |
| 3 | var | 4 | u32 | `vslocal_num` | vslocal 任务 ID 数量（上限 128） | 驱动 mission_ids_vslocal 数组循环（`cmp ebx,80h`） | 0..128 | B7278F|B727A3 | 确证 |
| 4 | var | 4·n₂ | array<u32,128> | `mission_ids_vslocal` | 本地 VS 任务 ID 列表（日志串 `mission_ids_vslocal={...}`） | 经 `vt[0x13C]` 交业务 | - | B727B9|B727D6|B727E2 | 确证 |
| 5 | var | 1 | u8 | `is_mission_vs_force_entry` | 是否强制进入 VS 任务（日志串 `is_mission_vs_force_entry=`） | 经 `vt[0x13C]` 交业务 | 0/1 | B72815|B72AA1 | 确证 |
| 6 | var | 1 | u8 | `xwar_entry_is_freeze` | XWAR 入场是否冻结（日志串 `xwar_entry_is_freeze=`） | 经 `vt[0x13C]` 交业务 | 0/1 | B72852|B72AB1 | 确证 |
| 7 | var | 1 | u8 | `vswar_entry_is_freeze` | VS 战入场是否冻结（日志串 `vswar_entry_is_freeze=`） | 经 `vt[0x13C]` 交业务 | 0/1 | B72876|B72AB9 | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B72886` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb728c9` 落在处理块 `0xb726bd`..`0xb72b17` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B726D3` 确证为 `0x40B`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B72886`（SOP §5.3）。
5. 去向：`vt[0x13C]` @`B72ACF`（7 实参）。

### 4.2 长度闭合与容量口径
- 容量 `0x40B` = 1035 = `u32(exvs_num) + 128×4(mission_ids_exvs 槽) + u32(vslocal_num) + 128×4(mission_ids_vslocal 槽) + u8×3`；两处上限均为 `cmp ebx,80h`@`B7272F`/`B727A3`。
- 两组数组均为 `u32[]`（预留 `sub_B41850` 槽步进 4、读 `sub_B02DD0`）；线长 = `11 + 4·n₁ + 4·n₂`。

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
