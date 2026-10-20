# CS-0x4BDF-lounge-msma_over_custom_use_capsule

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x4BDF` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_over_custom_use_capsule` |
| 名字符串 | `)<-_proto_lounge_client::send_msma_over_custom_use_capsule(` @ `0xeed60c` |
| 代码位置 | sub_BA80F0 @ `0xba80f0`（`0xba80f0`..`0xba82e2`） |
| opcode 写入证据 | `0xba8164` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xE`（14） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：机体改造使用胶囊：机体唯一 id + 道具 id。
- 字段数：**3**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 8 + 4 = 14 = 容量 0xE（精确相等）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 lounge 协议类处理块（C→S 无 case 块） | 0x4BDF | `0xBA8164` | 确证 |
| 1 | 2 | 8 | u64 | `uniq_msid` | 机体唯一 id | 来源=入参 arg_0（低 32 位 @0xBA8170）+ arg_4（高 32 位 @0xBA8176）；内联两次 `mov`（低 32 位在前）；经 `vt[0x58]` 发送 | - | `0xBA8174` | 确证 |
| 2 | 10 | 4 | u32 | `item_id` | 胶囊道具 id | 来源=入参 arg_8（@0xBA8188）；内联 `mov [edx],ecx`；经 `vt[0x58]` 发送 | - | `0xBA818C` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 8 + 4 = 14 = 容量 0xE（精确相等）

### 4.3 存疑点
- 日志名序（`uniq_msid=`→`item_id=`）与线序一致。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
