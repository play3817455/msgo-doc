# CS-0x8BDF-lounge-ranking_elite_pilot_get_page

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x8BDF` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `ranking_elite_pilot_get_page` |
| 名字符串 | `)<-_proto_lounge_client::send_ranking_elite_pilot_get_page(` @ `0xeed4cc` |
| 代码位置 | sub_BA7770 @ `0xba7770`（`0xba7770`..`0xba7973`） |
| opcode 写入证据 | `0xba77f1` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x12`（18） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0xC5A9-lounge-ranking_elite_pilot_get_page_r`（轻量版 `SC-0xC664-..._light_r`） |

## 2. 结论摘要

- 结论：分页请求精英驾驶员排行榜：排序条件（复合体 `order`，5×u16）+ 页码。
- 字段数：**3**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 10(order 复合体) + 4 = 16 ≤ 容量 0x12 = 18`（富余 2）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x8BDF` | `0xba77f1` | 确证 |
| 1 | 2 | 10 | struct | `order` | 排序条件结构（复合体 `order`，5×u16=10 字节） | 来源=入参 arg_0；复合写入器 `sub_B42060`（`0xB42060`，逐字段 5×u16，与 `CS-0x3FAF` @ `0xBA38AB` 同一个）；服务端据此排序 | 见 §3 结构体 | `0xBA77FB (writer sub_B42060)` | 确证 |
| 2 | 12 | 4 | u32 | `page` | 页码 | 来源=入参 arg_4；内联 `mov [eax],ecx`；服务端据此返回对应页 | - | `0xBA7820` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xba77b6`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xba77f1`（`mov word ptr [...], 0x8BDF`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 10(order 复合体) + 4 = 16 ≤ 容量 0x12 = 18`（富余 2）

### 4.3 复合体判定
- `order` 是复合写入器 `sub_B42060` 写出的 10 字节块（5×u16）。它不是"未知的 5 个 u16"：
  写这 10B 的 `sub_B42060`（@ `0xBA77FB`）与 `CS-0x3FAF-lounge-ranking_pilot_get_page`
  写同一块的 `sub_B42060`（@ `0xBA38AB`）**是同一个函数**，两条上行这 10B 逐字段同序
  ⇒ 就是复合体 `order`（`db_design/schema/composites/order.json`：成员
  kind/term/filter/reason/troops，读者 `sub_B46420` @ `0xB46438`..`0xB4647D` 五处逐成员取证，
  `asm_verified: true`）。故本条线类型记 `struct`（与 `CS-0x3FAF` 同写法）。
- 同族互证：`CS-0x3FAF-lounge-ranking_pilot_get_page` 亦用 `sub_B42060`（批次-17 已固化）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 无遗留 `?`（`order` 的复合体判定见 §4.3，已回写 `notes.md`）
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
