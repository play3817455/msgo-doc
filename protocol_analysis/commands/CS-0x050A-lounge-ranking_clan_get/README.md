# CS-0x050A-ranking_clan_get

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x050A` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `ranking_clan_get` |
| 名字符串 | `)<-_proto_lounge_client::send_ranking_clan_get( ` @ `0xeece60` |
| 代码位置 | sub_BA3A30 @ `0xba3a30`（`0xba3a30`..`0xba3c37`） |
| opcode 写入/分发证据 | `0xba3ab1`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x12`（18） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00BA3BC3`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：战队排行榜查询：排序条件（复合体 `order`，5×u16）+ 战队类别。
- 字段数：**3**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 10(order 复合体) + 1 = 13 ≤ 容量 0x12 = 18`（富余 5）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x050A` | `0xba3ab1` | 确证 |
| 1 | 0 | 10 | struct | `order` | 排序条件结构（复合体 `order`，5×u16=10 字节） | 来源=入参 arg_0（`0xBA3AA7 mov edx,dword ptr [esp+arg_0]`，指向该 10B 结构）；复合写入器 `sub_B42060`（调用点 `0xBA3ABB call sub_B42060`，与 `CS-0x3FAF` @`0xBA38AB`、`CS-0x8BDF` @`0xBA77FB` 同一个）；服务端按该组条件排序 | 见 §3 结构体 | `0xBA3ABB (writer sub_B42060)` | 确证 |
| 2 | 10 | 1 | u8 | `clan_kind` | 战队类别 | 来源=入参 arg_4（`0xBA3ADC mov cl,[esp+arg_4]`），内联 `mov [eax],cl`；服务端据此过滤 | 取值域 {0,1}（0=部隊 1=大会チーム） | `0xBA3AE0` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_ranking_clan_get` @ `0xBA3A30`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0x12; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- `2 + 10(order 复合体) + 1 = 13 ≤ 容量 0x12 = 18`（富余 5）

### 4.3 复合体判定
- `order` 是复合写入器 `sub_B42060` 写出的 10 字节块（5×u16）。它不是"未知的 5 个 u16"：
  写这 10B 的 `sub_B42060`（调用点 `0xBA3ABB`）与 `CS-0x3FAF-lounge-ranking_pilot_get_page`
  （@ `0xBA38AB`）、`CS-0x8BDF-lounge-ranking_elite_pilot_get_page`（@ `0xBA77FB`）调的是
  **同一个函数**，三条上行这 10B 逐字段同序 ⇒ 就是复合体 `order`
  （`db_design/schema/composites/order.json`：成员 kind/term/filter/reason/troops，
  读者 `sub_B46420` @ `0xB46438`..`0xB4647D` 五处逐成员取证，`asm_verified: true`）。
  故本条线类型记 `struct`（与 `CS-0x3FAF` 同写法）。
- 写入器本体逐字段取证：`sub_B42060`（`0xB42060`）先按 `[ecx+0]/[ecx+2]/[ecx+4]/[ecx+6]`
  四次 `mov si,[ecx+k]; mov [edx],si; add dword ptr [eax],2` 内联写 4 个 u16，
  末槽 `add ecx,8; call sub_B02DA0`（u16），游标累计 +10 ⇒ 线长 10，
  与 `order.json` 的 `wire_layout: 5×2`、`memory_claim: 10` 一致。
- 同族互证：`CS-0x3FAF`（批次-17）、`CS-0x8BDF`（批次-19）已固化同一判定。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 无遗留 `?`（`order` 的复合体判定见 §4.3，已回写 `notes.md`）
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
