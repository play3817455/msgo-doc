# CS-0x9370-lounge-clan_rokaku_use_point

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x9370` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_rokaku_use_point` |
| 名字符串 | `)<-_proto_lounge_client::send_clan_rokaku_use_point(` @ `0xeeccb0` |
| 代码位置 | sub_BA2A80 @ `0xba2a80`（`0xba2a80`..`0xba2d40`） |
| opcode 写入证据 | `0xba2afc` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x16`（22） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x7300-lounge-clan_rokaku_use_point_r`（已 DONE） |

## 2. 结论摘要

- 结论：部队楼阁（rokaku）使用点数：树 id + 节点号 + 索引 + 消耗点数 + 是否补给。
- 字段数：**6**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4×4 + 1 = 19 ≤ 容量 0x16 = 22`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x9370` | `0xba2afc` | 确证 |
| 1 | 2 | 4 | u32 | `tree_id` | 楼阁树 id | 来源=入参 arg_0；内联 `mov [eax],ecx`；服务端据此定位楼阁 | - | `0xBA2B0C` | 确证 |
| 2 | 6 | 4 | u32 | `node_no` | 节点号 | 来源=入参 arg_4；内联 `mov [eax],ecx` | - | `0xBA2B27` | 确证 |
| 3 | 10 | 4 | u32 | `idx_no` | 条目索引 | 来源=入参 arg_8；写线原语 `sub_B02D80` | - | `0xBA2B2F` | 确证 |
| 4 | 14 | 4 | u32 | `point_use` | 消耗点数 | 来源=入参 arg_C；写线原语 `sub_B02D80` | - | `0xBA2B49` | 确证 |
| 5 | 18 | 1 | u8 | `is_supply` | 是否补给/补足消耗 | 来源=入参 arg_10；写线原语 `sub_B061C0`(u8) | 0/1 | `0xBA2B63` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xba2ac6`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xba2afc`（`mov word ptr [...], 0x9370`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 4×4 + 1 = 19 ≤ 容量 0x16 = 22`（富余 3）

### 4.3 存疑点
- `is_supply` 线上 1 字节（`sub_B061C0`）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
