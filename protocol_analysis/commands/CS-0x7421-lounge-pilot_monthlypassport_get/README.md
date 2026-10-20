# CS-0x7421-lounge-pilot_monthlypassport_get

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x7421` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_monthlypassport_get` |
| 名字符串 | `)<-_proto_lounge_client::send_pilot_monthlypassport_get(` @ `0xeeace0` |
| 代码位置 | sub_B8F340 @ `0xb8f340`（`0xb8f340`..`0xb8f4c6`） |
| opcode 写入证据 | `0xb8f399` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x2`（2） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x3C66-lounge-pilot_monthlypassport_get_r` |

## 2. 结论摘要

- 结论：请求月卡（monthly passport）信息——**零负载命令**（无线体字段）。
- 字段数：**1**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2(opcode) + 0 = 2 == 容量 0x2 = 2`（**零负载**）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x7421` | `0xb8f399` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb8f386`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb8f399`（`mov word ptr [...], 0x7421`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2(opcode) + 0 = 2 == 容量 0x2 = 2`（**零负载**）

### 4.3 存疑点
- **零负载 C→S 命令**：容量 2 == 线长 2，全块仅一条 opcode 写入（`mov word ptr [edi],7421h`@0xB8F399），无任何字段写。判据同批次-16/17/18。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
