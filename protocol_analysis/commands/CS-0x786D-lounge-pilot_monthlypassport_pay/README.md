# CS-0x786D-lounge-pilot_monthlypassport_pay

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x786D` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_monthlypassport_pay` |
| 名字符串 | `)<-_proto_lounge_client::send_pilot_monthlypassport_pay(` @ `0xeead1c` |
| 代码位置 | sub_B8F4D0 @ `0xb8f4d0`（`0xb8f4d0`..`0xb8f67e`） |
| opcode 写入证据 | `0xb8f544` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x6`（6） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x73F0-lounge-pilot_monthlypassport_pay_r` |

## 2. 结论摘要

- 结论：购买（支付）月卡：只需一个 1 字节的「期段」索引。
- 字段数：**2**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 1 = 3 ≤ 容量 0x6 = 6`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x786D` | `0xb8f544` | 确证 |
| 1 | 2 | 1 | u8 | `period_path` | 期段索引（要购买第几期月卡） | 来源=入参 arg_0（`mov cl,[esp+40h+arg_0]; mov [eax],cl`@0xB8F54F/0xB8F553）；经 `vt[0x58]` 发送；服务端据此扣费并开通对应期段 | 取值域 1..N（1 起的月卡期数下标：`sub_A06C50`@`0xA06C7A` 传 `a2[368] + 1` → `sub_AFEE80` → 装配器 `sub_B8F4D0`@`0xAFEE95`） | `0xB8F553` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb8f516`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb8f544`（`mov word ptr [...], 0x786D`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 1 = 3 ≤ 容量 0x6 = 6`（富余 3）

### 4.3 存疑点
- 线上宽度 **1 字节**（`mov [eax],cl`）——不得按「path」语义直觉改成字符串/ u32。
- `period_path` 取值域 1..N（1 起的月卡期数下标：`sub_A06C50`@`0xA06C7A` 传 `a2[368] + 1` → `sub_AFEE80` → 装配器 `sub_B8F4D0`@`0xAFEE95`）（**不是** 0 基下标：写入点已 `+1`）。
- 容量富余 3（分配上限 6 = 2+4，实际用 1 字节负载）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
