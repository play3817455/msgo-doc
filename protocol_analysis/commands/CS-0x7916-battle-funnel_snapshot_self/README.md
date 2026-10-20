# CS-0x7916-battle-funnel_snapshot_self

> 状态：`DONE`（2026-09-20，批次-19；2026-09-30 折单行 `struct<funnel_snapshot_entry>` 对齐生成码）
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x7916` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `funnel_snapshot_self` |
| 名字符串 | `)<-_proto_battle_client::send_funnel_snapshot_self(` @ `0xee1048` |
| 代码位置 | sub_B3AB30 @ `0xb3ab30`（`0xb3ab30`..`0xb3ad27`） |
| opcode 写入证据 | `0xb3abd4` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xE`（14） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | 无同名 S→C 应答；与 `CS-0x7916` 同族的快照下发见 `SC-0x568A-battle-entity_snapshot`（已 DONE） |

## 2. 结论摘要

- 结论：本机上报「漏斗（funnel）快照」：报文体就是**一个** `funnel_snapshot_entry` 元素 —— 由复合写入器 `sub_B06850` 写入的 10 字节快照结构（ent_id + 武器槽 + 移动信息 5 字节）。
- 字段数：**2**（含 opcode 第 0 项；第 1 项是单个具名复合体 `struct<funnel_snapshot_entry>`，成员在 db_design 侧展开）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 10(snapshot 结构) = 12 ≤ 容量 0xE = 14`（富余 2）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x7916` | `0xb3abd4` | 确证 |
| 1 | 2 | 10 | struct\<funnel_snapshot_entry\> | `snapshot` | 漏斗快照：**一个元素**（线长 10 / 落地槽 12） | 来源=复合写入器 `sub_B06850(src, cursor)`（`0xB06850..0xB068AD`）；成员 `ent_id` u32（快照实体 id，`mov edx,[edi]; mov [ecx],edx`@0xB41C63）/`wslot_idx` i8（武器槽序号，`mov dl,[edi+4]`@0xB41C74，打印器 `sub_B0BF80` 用 `movsx` ⇒ 有符号）/`move_info` u8[5]（5 字节定长块，`[src+5..9]` 循环写 @0xB41C89..0xB41C9A） | 复合体 `funnel_snapshot_entry`（线长 10 = u32+i8+u8[5]；元素读取器 `sub_B081C0`、打印器 `sub_B0BF80`），与 SC-0x1B67 的数组元素同构 | `0xB06850` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb3ab99`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb3abd4`（`mov word ptr [...], 0x7916`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 10(snapshot 结构) = 12 ≤ 容量 0xE = 14`（富余 2）

### 4.3 存疑点
- 快照为**复合写入器** `sub_B06850`（`0xB06850..0xB068AD`）：u32 + u8 + u8[5] = **10 字节**，与容量 14 的差额 2（分配富余）。
- `move_info` 的 5 个字节成员未逐一命名（打印器 `sub_B0BF80` 整体打印 `move_info=`），标 `?`。
- `snapshot.wslot_idx` 为 **i8**：打印器用 `movsx`，且写线为单字节 `mov [ecx],dl`。

### 4.4 生成码侧对齐（2026-09-30）

字段表原先按打印器日志名逐格列出 `snapshot.ent_id` / `snapshot.wslot_idx` / `snapshot.move_info`；
生成器 `codecgen` 只把**长度 10** 的块与 `db_design` 复合体做匹配，前缀名 `snapshot` 先撞上
通用 39B 复合体 `snapshot`（`model.Snapshot`）⇒ 生成的 `CS0x7916…Body` 是 39B，与真包 10B 不符。

现改为**单行** `struct<funnel_snapshot_entry>`（长度 10）：线类型令牌点名元素复合体
`funnel_snapshot_entry`（与 SC-0x1B67 数组元素同构，`db_design/schema/composites/funnel_snapshot_entry.json`
`length: 10`），`composite_index.resolve` 走「令牌点名 + 线长一致」⇒ `ok`。生成码因此变成
`Snapshot model.FunnelSnapshotEntry`（`FixedBodySize = 10`），成员语义仍在复合体里，无需在命令层重复。
`serverv/internal/battle/relay.go` 的 `0x7916 → 0x1B67` 中转相应改回**生成码解码**（撤掉元素解码器绕行）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
