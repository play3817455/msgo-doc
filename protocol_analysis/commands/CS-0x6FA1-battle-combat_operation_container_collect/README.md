# CS-0x6FA1-battle-combat_operation_container_collect

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x6FA1` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `combat_operation_container_collect` |
| 名字符串 | `)<-_proto_battle_client::send_combat_operation_container_collect(` @ `0xee15c0` |
| 代码位置 | sub_B3F000 @ `0xb3f000`（`0xb3f000`..`0xb3f1ad`） |
| opcode 写入证据 | `0xb3f074` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x6`（6） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x02D8-battle-combat_operation_container_collect_r` |

## 2. 结论摘要

- 结论：战场近距离对象扫描发出交互类别请求；`destination=2` 已证实来自 `CHARA_PARAM.combat_role=EX_TENDER` 对象分支，类别 0/1 的对象条件和三类的资源结算仍未解。
- 字段数：**2**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2(opcode) + 4 = 6 == 容量 0x6 = 6`（精确相等）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x6FA1` | `0xb3f074` | 确证 |
| 1 | 2 | 4 | u32 | `destination` | 客户端近距离对象交互类别；值2由 `combat_role=EX_TENDER` 分支产生，0/1对象条件未解 | 来源=入参 arg_0；调用链 `sub_68D580 → sub_B01760 → sub_B3F000`；经 `vt[0x58]` 发送 | 0/1/2；2的筛选角色已证实为 `EX_TENDER`，不等于资源结算类型 | `0xB3F084`；分支谓词 `sub_474BC0 @ 0x474BC0`；`CHARA_PARAM` CSV7 | 确证（分支筛选字段和值来源）/未解（0/1及结算语义） |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb3f046`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb3f074`（`mov word ptr [...], 0x6FA1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2(opcode) + 4 = 6 == 容量 0x6 = 6`（精确相等）

### 4.3 存疑点
- `destination` 的三个类别各自对应的容器/物资与资源增量未解；响应 `result` 枚举及客户端响应消费端的实际库存变化也未闭合。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
