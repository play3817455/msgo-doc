# SC-0x10B1-lounge-msma_over_custom_exp_notice

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x10B1` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_over_custom_exp_notice` |
| 名字字符串 | `)->_proto_lounge_client::recv_msma_over_custom_exp_notice( `，引用点 `0xB55B23`（`push offset aProtoLoungeCli_22`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB55A33` .. `0xB55C1E`（块首即 `push 265h`，错误码 `0x265`） |
| 错误码 | `0x265`（`0xB55A9D push 265h` → `vt[0x64](1, 0x265)`） |
| 关联命令 | **无配对请求**（服务端通知）；同族通知 `../SC-0x0C41-lounge-exchange_play_bonus_r/`、`../SC-0x10B1` 所属的「机体经验/改装」族（`../SC-0x0876-lounge-msma_weapon_buildup_r/` 等） |

## 2. 结论摘要

- **报文体总长：定长 12 字节**（u64 + u32）。
- 长度校验：`0xB55AD6 mov eax,[esp+var_2C44]`（线游标）、`0xB55ADA cmp eax,[esp+var_2C40]`（vs 报文末尾）、`0xB55AE0 jz loc_B55AFC`（不等 ⇒ 报错）⇒ **整包精确消费完**。
- 声明容量 `push 0Ch`（`0xB55A4F`）= **12 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：`uniq_msid`（**u64 唯一机体 ID**）+ `exp` 交 `vt[0x5C8]`（`0xB55BF5` 取虚表项 / `0xB55C02` 调用），**实参顺序 `(uniq_msid 低 32 位, uniq_msid 高 32 位, exp)`** —— u64 在 cdecl 下拆成两个 32 位实参（`0xB55BFF push ecx`=低、`0xB55BFE push eax`=高）。
- u64 读原语：`sub_B41A10`（预留槽步进 8）+ `sub_B06200`（`0xB06220 add [..],8`）；日志用 64 位打印器 `sub_B08500`，取值 `mov eax,[ebx+4]; mov ecx,[ebx]`（高/低分开传）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x10B1` | `0xB55B23`（名字串引用点） | 确证 |
| 1 | 0 | 8 | u64 | `uniq_msid` | 唯一机体 ID（64 位） | 交 `vt[0x5C8]` 第 1/2 实参（`0xB55BFF`=低、`0xB55BFE`=高）；日志 `uniq_msid=`（`0xB55B79`，64 位打印器 `sub_B08500`） | `-` | `0xB55A8A`（`sub_B06200`）；槽预留 `0xB55A7B`（`sub_B41A10`，步进 8）；`0xB06220 add [..],8`；日志 `0xB55B6D`/`0xB55B70` | 确证 |
| 2 | 8 | 4 | u32 | `exp` | 改装/自定义经验值 | 交 `vt[0x5C8]` 第 3 实参（`0xB55BFB push ecx`）；日志 `exp=`（`0xB55B9E`，十进制打印器 `sub_B03580`） | `-` | `0xB55ACA`（`sub_B02DD0`）；槽预留 `0xB55ABB`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB55B9E` | 确证 |
| — | 12 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB55ADA`（`cmp`）、`0xB55AE0`（`jz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB55B23` 落在 `sub_B51930` 的 case 块 `0xB55A33..0xB55C1E` 内（错误码 `0x265`）。
2. 字段 1 = 「`sub_B41A10`（u64 槽预留）+ `sub_B06200`（读 8 字节）」；字段 2 = 「`sub_B41470` + `sub_B02DD0`（读 4 字节）」。
3. 含义取自块内日志 `uniq_msid=` / `exp=`（顺序与线序一致）。
4. 去向：`0xB55BEA..0xB55C02` 取 `uniq_msid` 的高/低 32 位与 `exp`，三次 `push` → `call vt[0x5C8]`。

### 4.2 长度闭合
- `8 + 4 = 12`；闭合点 `0xB55ADA`/`0xB55AE0` 要求「游标 == 末尾」✓
- 容量 12 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`vt[0x5C8]` 业务定名、`uniq_msid` 是否即 msma 的 `uniqid_ms`、`exp` 的量纲）。

## 5. 质量门自检

- [x] G1 字段表总长（12）与 `0xB55ADA`/`0xB55AE0` 的「游标 == 末尾」校验一致；容量 12 == 线长。
- [x] G2 线类型指回汇编 VA（`0xB55A8A`+`0xB06220` u64、`0xB55ACA`+`0xB02DE9` u32）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（`uniq_msid=`/`exp=`），用途追到 `vt[0x5C8]`（`0xB55C02`）。
- [x] G4 不确定项（`vt[0x5C8]` 定名、`uniq_msid` 与 msma `uniqid_ms` 的关系）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令无配对请求；同族通知已在 §1 链接。
