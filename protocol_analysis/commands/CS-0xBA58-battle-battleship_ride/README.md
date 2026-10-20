# CS-0xBA58-battle-battleship_ride

> 状态：`DONE`（2026-09-20，批次-20）
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xBA58` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `battleship_ride` |
| 名字符串 | `)<-_proto_battle_client::send_battleship_ride(` @ `0xEE16D0` |
| 代码位置 | sub_B3F970 @ `0xB3F970`（`0xB3F970`..`0xB3FB1F`） |
| opcode 写入证据 | `0xB3F9E4` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x0006`（6） |
| 容量申请证据 | `0xB3F9B6`（`push 0x0006`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0xB3FAAD` |
| 附加通知 | `[obj+79A8h]` 回调，模块 id `0x0FC` @ `0xB3FAC8` |
| 配对命令 | S→C `SC-0xE014-battle-battleship_ride_r`（已 DONE） |

## 2. 结论摘要

- 结论：请求登上战舰。
- 字段数：**2**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 2 = 4 ≤ 容量 0x6 = 6`（富余 2）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xBA58 | `0xB3F9E4` | 确证 |
| 1 | 2 | 2 | u16 | `to_ent_id` | 目标战舰实体 id | 来源=入参 `arg_0`（`mov cx,word ptr [esp+40h+arg_0]` → 内联 `mov [eax],cx`） | - | `0xB3F9F5` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量申请 `push 0x0006` @ `0xB3F9B6`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xB3F9E4`（`mov     word ptr [ebp+0], 0BA58h`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 2 = 4 ≤ 容量 0x6 = 6`（富余 2）

### 4.3 存疑点
- 无。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / notes.md）
