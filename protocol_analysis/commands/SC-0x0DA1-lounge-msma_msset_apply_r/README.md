# SC-0x0DA1-lounge-msma_msset_apply_r

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0DA1` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_msset_apply_r` |
| 名字字符串 | `)->_proto_lounge_client::recv_msma_msset_apply_r( `，引用点 `0xB55341`（`push offset aProtoLoungeCli_19`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB55234` .. `0xB5546D`（case 起始前导 `0xB5522D push 12Eh`） |
| 错误码 | `0x12E`（`0xB55297 push 12Eh` → `vt[0x64](1, 0x12E)`） |
| 关联命令 | 配对请求 `../CS-0x7306-lounge-msma_msset_apply/`（`0x7306`，容量 `0xA`） |

## 2. 结论摘要

- **报文体总长：定长 8 字节**（u32 + u16 + u16）。
- 长度校验：`0xB552F4 mov ebx,[esp+var_2C44]`（线游标）、`0xB552F8 cmp ebx,[esp+var_2C40]`（vs 报文末尾）、`0xB552FE jz loc_B5531A`（不等 ⇒ `push 12Eh` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 8`（`0xB55249`）= **8 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：三个值交 `vt[0x308]`（`0xB5543D` 取虚表项 / `0xB55451` 调用），**实参顺序 `(result, deck_type, slot)`**（`0xB55443 push edx`=slot、`0xB5544B push edx`=deck_type、`0xB5544E push edx`=result，cdecl 右→左 ⇒ 第 1 实参 = `result`）；块内日志 `result=` / `deck_type=` / `slot=`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0DA1` | `0xB55341`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 机体套组（msset）应用结果码 | 交 `vt[0x308]` 第 1 实参（`0xB5544E push edx`）；日志 `result=`（`0xB55397`） | `?`（结果码枚举未交叉） | `0xB55284`（`sub_B02DD0`）；槽预留 `0xB55275`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB55397` | 类型确证 / 枚举待定 |
| 2 | 4 | 2 | u16 | `deck_type` | 卡组（deck）类型 | 交 `vt[0x308]` 第 2 实参（`0xB5544B push edx`）；日志 `deck_type=`（`0xB553C2`，`sub_B032A0` 十进制） | `?`（类型枚举未交叉） | `0xB552C4`（`sub_B02DF0`）；槽预留 `0xB552B5`（`sub_B413B0`）；`0xB02E0B add [eax],2`；日志 `0xB553C2` | 确证 |
| 3 | 6 | 2 | u16 | `slot` | 应用到的卡组槽位号 | 交 `vt[0x308]` 第 3 实参（`0xB55443 push edx`）；日志 `slot=`（`0xB553E8`，`sub_B032A0` 十进制） | `-` | `0xB552E8`（`sub_B02DF0`）；槽预留 `0xB552D9`（`sub_B413B0`）；日志 `0xB553E8` | 确证 |
| — | 8 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB552F8`（`cmp`）、`0xB552FE`（`jz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB55341` 落在 `sub_B51930` 的 case 块 `0xB55234..0xB5546D` 内（错误码 `0x12E`）。
2. 三个字段 = 三组「槽预留（`sub_B41470` u32 / `sub_B413B0` u16）+ bounded 读取器（`sub_B02DD0` / `sub_B02DF0`）」，槽分别在 `var_2C30` / `var_2C34` / `var_2C38`。
3. 含义取自块内日志顺序 `result=` → `deck_type=` → `slot=`，与线序**完全一致**。
4. 去向：`0xB55430..0xB55451` 逐个取槽 → 三次 `push`（`slot`,`deck_type`,`result`）→ `call vt[0x308]`。

### 4.2 长度闭合
- `4 + 2 + 2 = 8`；闭合点 `0xB552F8`/`0xB552FE` 要求「游标 == 末尾」✓
- 容量 8 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`result` 结果码枚举、`deck_type` 枚举、与 C→S `0x7306` 的字段对应）。

## 5. 质量门自检

- [x] G1 字段表总长（8）与 `0xB552F8`/`0xB552FE` 的「游标 == 末尾」校验一致；容量 8 == 线长。
- [x] G2 线类型指回汇编 VA（`0xB55284`/`0xB552C4`/`0xB552E8` + `0xB02DE9`/`0xB02E0B`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（`result=`/`deck_type=`/`slot=`），用途追到 `vt[0x308]`（`0xB55451`）。
- [x] G4 不确定项（`result`/`deck_type` 枚举）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `CS-0x7306-lounge-msma_msset_apply` 已在 §1 链接。
