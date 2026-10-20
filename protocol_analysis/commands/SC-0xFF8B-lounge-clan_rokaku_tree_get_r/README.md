# SC-0xFF8B-clan_rokaku_tree_get_r

> 状态：`DONE`
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xFF8B` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_rokaku_tree_get_r` |
| 名字符串 | `)->_proto_lounge_client::recv_clan_rokaku_tree_get_r( ` @ `0xee5490` |
| 代码位置 | sub_B51930 @ `0xb51930`　块 `0xb88c9d`..`0xb89116` |
| opcode 写入/分发证据 | `0xb88ebc`（命令名字符串引用点 = case 归属锚点）|
| 处理块范围 | `0xB88C9D`..`0xB89116` |
| 声明容量 | `0x574`（1396） |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：7 字段：`clan_id` + 「计数 + 变长数组」×2（page 上限 8 / node 上限 21）+ 两个点数。容量 1396 == 4+4+8×4+4+21×64+4+4 精确相等。
- 长度校验方式：处理块内「**游标 == 报文末尾**」闭合检查 @`0x00B88E7A`。
- 去向锚点：`vt[0x484]`（7 个实参）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0xFF8B` | `0xb88ebc` | 确证 |
| 1 | 0 | 4 | u32 | `clan_id` | 战队 ID | `sub_B02DD0`（`0xB88CF7`）读 u32；去向 `vt[0x484]` 第 7 实参（`0xB890D4 push eax`） | - | `0xB88CF7` | 确证 |
| 2 | 4 | 4 | u32 | `page_count` | 页码条目数（`cmp ebx,8; ja 出错` 上限 8） | `sub_B02DD0`（`0xB88D22`）读 u32；去向 `vt[0x484]` 第 5 实参（`0xB890D0 push ebx`） | ≤8 | `0xB88D22` | 确证 |
| 3 | 8 | page_count×4 | array<u32> | `page` | 页码列表（元素 u32，槽步进 4） | 阵列预留 `sub_B41850`（`0xB88D59`，按 count 申请，4B/槽）；循环 `sub_B02DD0`（步进 4）；去向 `vt[0x484]` 第 6 实参（`0xB890D1 push eax`） | 元素 4B / 槽 4B | `0xB88D59,0xB88D70` | 确证 |
| 4 | var | 4 | u32 | `node_count` | 节点条目数（`cmp [var_2C2C],15h; ja 出错` 上限 21） | `sub_B02DD0`（`0xB88DAE`）读 u32；去向 `vt[0x484]` 第 4 实参（`0xB890C3 push eax`） | ≤21 | `0xB88DAE` | 确证 |
| 5 | var | node_count×60 | array<elem60> | `node` | 节点列表（元素线长 60，槽步进 0x40=64） | 阵列预留 `sub_B41AC0`（`0xB88DD7`，按 count 申请，0x40/槽）；元素读取器 `sub_B46300`（`0xB46300`，线长 60 = 4×u32 + 7×u32 + u64），循环 count 次（步进 0x40）；去向 `vt[0x484]` 第 3 实参（`0xB890CB push ecx`） | 元素线长 60 / 槽步进 64 | `0xB88DD7,0xB88DFA` | 确证 |
| 6 | var | 4 | u32 | `point_use` | 已消耗点数 | `sub_B02DD0`（`0xB88E3E`）读 u32；去向 `vt[0x484]` 第 2 实参（`0xB890BE push ecx`） | - | `0xB88E3E` | 确证 |
| 7 | var | 4 | u32 | `point_pool` | 点数池 | `sub_B02DD0`（`0xB88E66`）读 u32；去向 `vt[0x484]` 第 1 实参（`0xB890B7 push ecx`） | - | `0xB88E66` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 处理块 `0xB88C9D..0xB89116`（lounge_client 分发器 `0xB51930`）；守卫 = `sub_B41120(lounge(0x1E0))`，收尾 = `sub_B41110`。
- 解码缓冲分配：`mov ecx,[esi+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push 0x574; call edx`（`0x574` 为**容量**，非线长）。

### 4.2 长度闭合
- 闭合点：`0x00B88E7A`（游标寄存器与报文末尾比较，`jz`/`jnz` 走成功分支）。
- 容量校验：`0x574`=1396 = 4 + 4 + 8×4(page claim) + 4 + 21×64(node claim) + 4 + 4 ✓ —— 两个数组的 claim 均按「槽步进 × 上限」记账，与代码里 `cmp ebx,8` / `cmp [var_2C2C],15h` 三方吻合。

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（游标==末尾 @`0x00B88E7A`）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
