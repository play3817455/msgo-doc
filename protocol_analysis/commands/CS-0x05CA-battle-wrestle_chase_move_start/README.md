# CS-0x05CA-wrestle_chase_move_start

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x05CA` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `wrestle_chase_move_start` |
| 名字符串 | `)<-_proto_battle_client::send_wrestle_chase_move_start( ` @ `0xee18e0` |
| 代码位置 | sub_B40B50 @ `0xb40b50`（`0xb40b50`..`0xb40f16`） |
| opcode 写入/分发证据 | `0xb40bcc`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x26`（38） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00B40EA4`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：9 字段 + opcode：格斗追身移动开始（帧号/方向/招式/时长/目标实体与坐标/AI 实体号）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x05CA` | `0xb40bcc` | 确证 |
| 1 | 0 | 4 | u32 | `frame_count` | 起始帧号（同步基准） | 来源=入参 arg_0（`0xB40BD8 mov esi,[esp+arg_0]`），内联 `mov [ecx],esi`；服务端用于回放同步 | - | `0xB40BDC` | 确证 |
| 2 | 4 | 2 | u16 | `dir_h` | 朝向（水平角，定点） | 来源=入参 arg_4（`0xB40BE9 mov ax,word ptr [esp+arg_4]`），内联 `mov [edx],ax` | - | `0xB40BF6` | 确证 |
| 3 | 6 | 4 | u32 | `wrestle_id` | 格斗（追身）动作 ID | 来源=入参 arg_8（`0xB40BFA lea edx,[esp+arg_8]`）经写 u32 原语 `sub_B02D80` | - | `0xB40BFF` | 确证 |
| 4 | 10 | 4 | u32 | `chase_time_msec` | 追身持续时间（毫秒） | 来源=入参 arg_C（`0xB40C14 lea ecx,[esp+arg_C]`）经 `sub_B02D80` | - | `0xB40C19` | 确证 |
| 5 | 14 | 2 | u16 | `target_ent_id` | 目标实体 ID | 来源=入参 arg_10（`0xB40C2E lea eax,[esp+arg_10]`）经写 u16 原语 `sub_B02DA0` | - | `0xB40C33` | 确证 |
| 6 | 16 | 2 | u16 | `target_pos_x` | 目标坐标 X | 来源=入参 arg_14（`0xB40C48 lea edx,[esp+arg_14]`）经 `sub_B02DA0` | - | `0xB40C4D` | 确证 |
| 7 | 18 | 2 | u16 | `target_pos_y` | 目标坐标 Y | 来源=入参 arg_18（`0xB40C62 lea ecx,[esp+arg_18]`）经 `sub_B02DA0` | - | `0xB40C67` | 确证 |
| 8 | 20 | 2 | u16 | `target_pos_z` | 目标坐标 Z | 来源=入参 arg_1C（`0xB40C7C lea eax,[esp+arg_1C]`）经 `sub_B02DA0` | - | `0xB40C81` | 确证 |
| 9 | 22 | 2 | u16 | `AI_ent_id` | AI 实体 ID | 来源=入参 arg_20（`0xB40C96 lea edx,[esp+arg_20]`）经 `sub_B02DA0` | - | `0xB40C9B` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_wrestle_chase_move_start` @ `0xB40B50`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0x26; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- 容量 `0x26`=38 ≥ 线长 26 ✓。

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 <= 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
