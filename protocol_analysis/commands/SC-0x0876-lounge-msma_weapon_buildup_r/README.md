# SC-0x0876-msma_weapon_buildup_r

> 状态：`DONE`（2026-09-20，批次-3）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0876` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_buildup_r` |
| 名字符串 | `)->_proto_lounge_client::recv_msma_weapon_buildup_r(` @ `0xEE9EC4`，引用点 `0xB54507` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB542C3` .. `0xB547B0`（错误码 `0x112`） |
| 关联命令 | 配对请求 `../CS-0x5FAB-lounge-msma_weapon_buildup/`（`sub_B96E30`，容量 `0x1A`） |

## 2. 结论摘要

- **报文体总长：定长 36 字节**（10 个字段全定长）。
- 负载 = 3×u32 + 1×u64 + 2×u32 + 2×u16 + 2×u32 + 2×u16，全部由 bounded 读取器消费。
- 长度校验：`0xB544BA mov eax,[esp+var_2C44]`（游标）、`0xB544BE cmp eax,[esp+var_2C40]`（vs 报文末尾）、`0xB544C4 jz ok`（不等 ⇒ `push 112h` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 24h`（`0xB542DF`）= **36 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：10 个值交 `vt[0x2CC]`（`0xB5474D` 取虚表项 / `0xB5477C` 调用），实参顺序
  `(result, uniqid_ms(64位), item_id, ticket_id, usenum, param_target, workres, buildup_cnt, up_param, mech_npcpict)`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0876` | `0xB54507`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 强化请求结果码 | 交 `vt[0x2CC]`（第 1 实参 `0xB54779 push ecx`）；日志 `result=`（`0xB5455D`，十进制） | `?`（结果码枚举未交叉） | `0xB5431A`（`sub_B02DD0`）；`0xB02DE9 add [eax],4`；日志 `0xB5455D` | 类型确证 / 枚举待定 |
| 2 | 4 | 8 | u64 | `uniqid_ms` | 机体唯一编号（64 位） | 交 `vt[0x2CC]`（`0xB5476E`/`0xB54776` 压高低 32 位）；日志 `uniqid_ms=`（`0xB54587`，64 位打印器 `sub_B08500`） | `-` | `0xB5435A`（`sub_B06200`）；槽预留 `0xB5434B`（`sub_B41A10`）；日志 `0xB54587` | 确证 |
| 3 | 12 | 4 | u32 | `item_id` | 强化所用道具 ID | 交 `vt[0x2CC]`（`0xB5476B push ecx`）；日志 `item_id=`（`0xB545B1`） | `-` | `0xB5439A`（`sub_B02DD0`）；日志 `0xB545B1` | 确证 |
| 4 | 16 | 4 | u32 | `ticket_id` | 强化所用票券 ID | 交 `vt[0x2CC]`（`0xB54765 push ecx`）；日志 `ticket_id=`（`0xB545DB`） | `-` | `0xB543BE`（`sub_B02DD0`）；日志 `0xB545DB` | 确证 |
| 5 | 20 | 2 | u16 | `usenum` | 道具使用次数/数量 | 交 `vt[0x2CC]`（`0xB5475B push ecx`）；日志 `usenum=`（`0xB54606`，十六进制打印器 `sub_B032A0`） | `-` | `0xB543E2`（`sub_B02DF0`）；`0xB02E0B add [eax],2`；日志 `0xB54606` | 确证 |
| 6 | 22 | 2 | u16 | `param_target` | 强化参数对象（目标槽/部位） | 交 `vt[0x2CC]`（`0xB54753 push ecx`）；日志 `param_target=`（`0xB54631`） | `?`（枚举未交叉） | `0xB5440A`（`sub_B02DF0`）；日志 `0xB54631` | 类型确证 / 枚举待定 |
| 7 | 24 | 4 | u32 | `workres` | 强化产出物 ID | 交 `vt[0x2CC]`（`0xB54743 push ecx`）；日志 `workres=`（`0xB5465B`） | `-` | `0xB54432`（`sub_B02DD0`）；日志 `0xB5465B` | 确证 |
| 8 | 28 | 2 | u16 | `buildup_cnt` | 累计强化次数 | 交 `vt[0x2CC]`（`0xB5473C push ecx`）；日志 `buildup_cnt=`（`0xB54686`） | `-` | `0xB5445A`（`sub_B02DF0`）；日志 `0xB54686` | 确证 |
| 9 | 30 | 2 | u16 | `up_param` | 强化提升参数 | 交 `vt[0x2CC]`（`0xB54734 push ecx`）；日志 `up_param=`（`0xB546B1`） | `?` | `0xB54482`（`sub_B02DF0`）；日志 `0xB546B1` | 类型确证 / 枚举待定 |
| 10 | 32 | 4 | u32 | `mech_npcpict` | 机体 NPC 立绘/外观编号 | 交 `vt[0x2CC]`（`0xB5472C push ecx`）；日志 `mech_npcpict=`（`0xB546D6`） | `-` | `0xB544AA`（`sub_B02DD0`）；日志 `0xB546D6` | 确证 |
| — | 36 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB544BE`（`cmp`）、`0xB544C4`（`jz`） | 确证 |

> 偏移核算：`4+8+4+4+2+2+4+2+2+4 = 36` ✓

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE9EC4` 的引用点 `0xB54507` 落在 `sub_B51930` 的 case 块 `0xB542C3..0xB547B0` 内（错误码 `0x112`）。
2. 逐字段读法（槽预留 + bounded 读取器成对，只计一次字段）：`sub_B41470`+`sub_B02DD0` 读 u32；`sub_B41A10`+`sub_B06200` 读 **u64**（`0xB5435A`）；`sub_B413B0`+`sub_B02DF0` 读 u16。
3. 日志顺序（`result=` → `uniqid_ms=` → `item_id=` → `ticket_id=` → `usenum=` → `param_target=` → `workres=` → `buildup_cnt=` → `up_param=` → `mech_npcpict=`）与线序完全一致。

### 4.2 长度闭合
- `4+8+4+4+2+2+4+2+2+4 = 36`；闭合点 `0xB544BE` 要求「游标 == 末尾」✓
- 容量 `0x24`=36 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`result`/`param_target`/`up_param` 枚举；与 C→S `0x5FAB` 的字段对应）。

## 5. 质量门自检

- [x] G1 字段表总长（36）与 `0xB544BE`/`0xB544C4` 的「游标 == 末尾」校验一致；容量 36 == 线长。
- [x] G2 线类型指回汇编 VA（u32 `0xB02DE9`；u64 `0xB5435A`；u16 `0xB02E09`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（10 个 `xxx=` 格式串），用途追到 `vt[0x2CC]`（`0xB5477C`）。
- [x] G4 不确定项（`result`/`param_target`/`up_param` 枚举）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `CS-0x5FAB-lounge-msma_weapon_buildup` 已在 §1 链接。
