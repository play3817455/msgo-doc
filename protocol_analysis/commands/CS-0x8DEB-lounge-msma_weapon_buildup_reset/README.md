# CS-0x8DEB-lounge-msma_weapon_buildup_reset

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x8DEB` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_buildup_reset` |
| 名字符串 | `)<-_proto_lounge_client::send_msma_weapon_buildup_reset(` @ `0xeeba64` |
| 代码位置 | sub_B976A0 @ `0xb976a0`（`0xb976a0`..`0xb97892`） |
| opcode 写入证据 | `0xb97714` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xE`（14） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x00F0-lounge-msma_weapon_buildup_reset_r`（已 DONE） |

## 2. 结论摘要

- 结论：重置机体武器强化：机体 uniqid + 道具 id。
- 字段数：**3**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 8(u64) + 4 = 14 == 容量 0xE = 14`（精确相等）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x8DEB` | `0xb97714` | 确证 |
| 1 | 2 | 8 | u64 | `uniqid_ms` | 机体唯一 id | 来源=入参 arg_0/arg_4（低 32 位在前，两个内联 `mov [eax],ecx`/`mov [eax+4],ecx`）；服务端据此定位机体 | - | `0xB97724, 0xB9772F` | 确证 |
| 2 | 10 | 4 | u32 | `item_id` | 武器道具 id | 来源=入参 arg_8；内联 `mov [edx],ecx`；服务端据此重置该武器的强化 | - | `0xB9773C` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb976e6`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb97714`（`mov word ptr [...], 0x8DEB`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 8(u64) + 4 = 14 == 容量 0xE = 14`（精确相等）

### 4.3 存疑点
- 无未决项。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
