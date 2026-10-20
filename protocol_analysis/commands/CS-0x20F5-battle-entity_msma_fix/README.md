# CS-0x20F5-entity_msma_fix

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x20F5` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle` |
| 命令名 | `entity_msma_fix` |
| 名字符串 | `)<-_proto_battle::send_entity_msma_fix( ` @ `0xedc160` |
| 代码位置 | sub_B0C910 @ `0xb0c910`（`0xb0c910`..`0xb0cc13`） |
| opcode 写入/分发证据 | `0xb0c98c`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x1A`（26） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00B0CBA4`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | [SC-0x20F5-battle-entity_msma_fix](SC-0x20F5-battle-entity_msma_fix) |

## 2. 结论摘要

- 结论：6 字段 + opcode：机体位置/姿态纠偏（不经分发器的 battle 命令，双向同号 0x20F5）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x20F5` | `0xb0c98c` | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 实体 ID | 来源=入参 arg_0（`0xB0C998 mov si,word ptr [esp+arg_0]`），内联 `mov [eax],si` | - | `0xB0C99D` | 确证 |
| 2 | 2 | 2 | u16 | `pos_x` | 坐标 X | 来源=入参 arg_4（`0xB0C9AD mov cx,word ptr [esp+arg_4]`），内联 `mov [eax],cx` | - | `0xB0C9BA` | 确证 |
| 3 | 4 | 2 | u16 | `pos_y` | 坐标 Y | 来源=入参 arg_8（`0xB0C9BE lea eax,[esp+arg_8]`）经写 u16 原语 `sub_B02DA0` | - | `0xB0C9C3` | 确证 |
| 4 | 6 | 2 | u16 | `pos_z` | 坐标 Z | 来源=入参 arg_C（`0xB0C9D8 lea edx,[esp+arg_C]`）经 `sub_B02DA0` | - | `0xB0C9DD` | 确证 |
| 5 | 8 | 2 | u16 | `attach_parent_ent_id` | 挂接父实体 ID | 来源=入参 arg_10（`0xB0C9F2 lea ecx,[esp+arg_10]`）经 `sub_B02DA0` | - | `0xB0C9F7` | 确证 |
| 6 | 10 | 1 | u8 | `is_using_ss` | 是否使用 SS（特殊系统） | 来源=入参 arg_14（`0xB0CA0C lea eax,[esp+arg_14]`）经写 u8 原语 `sub_B061C0` | - | `0xB0CA11` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_entity_msma_fix` @ `0xB0C910`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0x1A; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- 容量 `0x1A`=26 ≥ 线长 11（2+10+1），符合「容量是预留上限，常有富余」。

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
