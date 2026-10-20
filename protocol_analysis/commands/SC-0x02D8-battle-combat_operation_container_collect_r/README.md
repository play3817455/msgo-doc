# SC-0x02D8-combat_operation_container_collect_r

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x02D8` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `combat_operation_container_collect_r` |
| 名字符串 | `)->_proto_battle_client::recv_combat_operation_container_collect_r(` @ `0xEE04C0`，xref `0xB0D227` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0D137` .. `0xB0D320`（块首 `0xB0D137 push 0F4h`，`0F4` 即本 case 开关/错误码） |
| 关联命令 | 发出侧 `_proto_battle_client::send_combat_operation_container_collect`（C→S `0x6FA1`，声明容量 `0x6`）→ `../CS-0x6FA1-battle-combat_operation_container_collect/` |

## 2. 结论摘要

- **报文体总长：`8` 字节**（opcode `2` + 负载 `6`）。
- 负载 = **`u16 ent_id` + `u32 result`**（`2 + 4 = 6`）。
- 长度校验：`0xB0D1DA` 取读完后的游标，`0xB0D1DE cmp ebx, [esp+1B3Ch+var_1B24]`（vs 报文末尾），`0xB0D1E4 jz ok`（不等 ⇒ `push 0F4h` 报错）。
- 声明容量 `push 6`（`0xB0D153`）= `6` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**战斗行动容器（combat operation container）交互应答**；`ent_id`＝实体 ID，`result` 是业务枚举尚未解的结果字段；两者交 `vt[0x2F4]`（`0xB0D304`）。消费端会清理待处理范围并刷新 UI/实体提示，但没有直接资源结算证据。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x02D8` | `0xB0D227`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 实体 ID | 交 `vt[0x2F4]` 第 1 实参；日志 `ent_id=`（`0xB0D27E`） | - | `0xB0D18E`（`call sub_B02DF0`）；本体 `0xB02E01`（`mov cx,[ecx]`）+ `0xB02E0B`（`add dword ptr [eax], 2`）；日志 `0xB0D271`~`0xB0D27E` | 确证 |
| 2 | 2 | 4 | u32 | `result` | 日志字段名为结果；业务枚举/资源结算语义未解 | 交 `vt[0x2F4]` 第 2 实参；日志 `result=`（`0xB0D2A3`） | 未知 | `0xB0D1CE`（`call sub_B02DD0`）；本体 `0xB02DE1` + `0xB02DE9`；日志 `0xB0D299`~`0xB0D2A3` | 确证（字段）/未解（枚举及结算语义） |
| — | 6 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB0D1DA`（`mov ebx,[esp+var_1B28]`）、`0xB0D1DE`（`cmp ebx,[esp+var_1B24]`）、`0xB0D1E4`（`jz`） | 确证 |

**去向**：`0xB0D2EB`..`0xB0D304` —— `mov eax,[esp+var_1B2C]`（u32 槽）→ `mov ecx,[eax]`；
`mov eax,[esp+var_1B20]`（u16 槽）→ `movzx ecx, word ptr [eax]` ⇒ `call vt[0x2F4](ent_id, result)`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE04C0` 的引用点 `0xB0D227` 落在 battle 分发器 `sub_B0CC20` 的 case 块 `0xB0D137..0xB0D320` 内。
2. 块首 `0xB0D137 push 0F4h` 与全部错误路径 `push 0F4h`（如 `0xB0D1A1`）一致。

### 4.2 长度闭合
- 读取序列：预留 u16 槽（`sub_B413B0`，非字段）→ `sub_B02DF0`(u16) → 预留 u32 槽（`sub_B41470`）→ `sub_B02DD0`(u32)。
- 消费量 = `2 + 4` = **6** 字节；随即 `0xB0D1DE` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 6`（`0xB0D153`）= 6（旁证）；发出侧容量同为 `0x6`，**双侧对称**（强交叉验证）。

### 4.3 存疑点
见 `notes.md`（`vt[0x2F4]` 实现、`result` 枚举未定）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 6 字节；`游标 == 末尾` 校验在 `0xB0D1DE`/`0xB0D1E4`。
- [x] G2 类型均指回汇编 VA（u16 `0xB02E01`/`0xB02E0B`；u32 `0xB02DE1`/`0xB02DE9`）；未使用伪代码类型。
- [x] G3 含义取自日志串 `ent_id=`/`result=`；用途追到 `vt[0x2F4]`（`0xB0D304`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对命令（发出侧 `0x6FA1`）已在 §1 链接。
