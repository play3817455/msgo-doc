# CS-0xB235-lounge-season_rankerbattle_get_entitled_pilot_list

> 状态：`DONE`（2026-09-20，批次-20）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xB235` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `season_rankerbattle_get_entitled_pilot_list` |
| 名字符串 | `)<-_proto_lounge_client::send_season_rankerbattle_get_entitled_pilot_list(` @ `0xEED548` |
| 代码位置 | sub_BA7B10 @ `0xBA7B10`（`0xBA7B10`..`0xBA7CD9`） |
| opcode 写入证据 | `0xBA7B91` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x000E`（14） |
| 容量申请证据 | `0xBA7B56`（`push 0x000E`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0xBA7C65` |
| 附加通知 | `[obj+79A8h]` 回调，模块 id `0x258` @ `0xBA7C82` |
| 配对命令 | S→C `SC-0x9F9B-lounge-season_rankerbattle_get_entitled_pilot_list_r`（已 DONE） |

## 2. 结论摘要

- 结论：请求获取赛季排位赛「有资格驾驶员」名单（带 5 字段排序/筛选条件）。
- 字段数：**6**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 10(结构体) = 12 ≤ 容量 0xE = 14`（富余 2）
- 结构体/数组展开：`order` = `kind(u16) + term(u16) + filter(u16) + reason(u16) + troops(u16)` = **10B**（写入器 `sub_B42060` = 5×u16；打印器 `sub_B4F620` 成员名 `kind=`/`term=`/`filter=`/`reason=`/`troops=`）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xB235 | `0xBA7B91` | 确证 |
| 1 | 2 | 2 | u16 | `order.kind` | 排序/筛选种类 | 复合写入器 `sub_B42060` 第 1 个 `mov [edx],si`（源 `[src+0]`；`sub_B42060` 前 4 个 u16 内联写、第 5 个走 `sub_B02DA0`） | - | `0xB42073` | 确证 |
| 2 | 4 | 2 | u16 | `order.term` | 统计期间 | 复合写入器 `sub_B42060` 第 2 个 u16（源 `[src+2]`） | - | `0xB42086` | 确证 |
| 3 | 6 | 2 | u16 | `order.filter` | 筛选条件 | 复合写入器 `sub_B42060` 第 3 个 u16（源 `[src+4]`） | - | `0xB4209A` | 确证 |
| 4 | 8 | 2 | u16 | `order.reason` | 原因/依据 | 复合写入器 `sub_B42060` 第 4 个 u16（源 `[src+6]`） | - | `0xB420AE` | 确证 |
| 5 | 10 | 2 | u16 | `order.troops` | 势力/阵营 | 复合写入器 `sub_B42060` 第 5 个 u16（源 `[src+8]`，走写线原语 `sub_B02DA0`） | - | `0xB420BD` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量申请 `push 0x000E` @ `0xBA7B56`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xBA7B91`（`mov     word ptr [edi], 0B235h`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 10(结构体) = 12 ≤ 容量 0xE = 14`（富余 2）

### 4.3 存疑点
- 结构体线长必须进**写入器函数体**逐字段累加：`sub_B42060`（`0xB42060..0xB420D2`）= 5×u16 = 10B；成员名取自打印器 `sub_B4F620`。
- 容量 14 = `2 + 10 + 2`（富余 2）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / notes.md）
