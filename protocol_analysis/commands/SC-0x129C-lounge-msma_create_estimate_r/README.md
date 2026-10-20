# SC-0x129C-lounge-msma_create_estimate_r

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x129C` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_create_estimate_r` |
| 名字字符串 | `)->_proto_lounge_client::recv_msma_create_estimate_r( `，引用点 `0xB5593C`（`push offset aProtoLoungeCli_21`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB55853` .. `0xB55A33` |
| 错误码 | `0x101`（`0xB558B6 push 101h`、`0xB55902`、`0xB55915`） |
| 关联命令 | 应答侧：`../CS-0x----`（机体创建估价请求，本批未定位）；同类货币/估价通知：`../SC-0x090C-lounge-pilot_money_update/`、商城 `../SC-0x2467-lounge-shop_buy_r/`（估价用于下单前预览） |

## 2. 结论摘要

- **报文体总长：定长 `8` 字节**（2 个 u32）。
- 长度校验方式：读完两个字段后 `0xB558F3 mov ebx,[var_2C44]` / `0xB558F7 cmp ebx,[var_2C40]`（线游标 vs 报文末尾）＋ `0xB558F9 jz ok`；不等 ⇒ 报错 ⇒ **负载恰为 8 字节**。
- 声明容量：`0x8`（`0xB55868 push 8` + `call [edx+78h]`）⇒ 容量 `8` **精确等于**线长 `8`。
- 是否分帧：否。
- 关键结论：字段 1 `result`（u32）、字段 2 `price`（u32），经 `vt[0x2A8](result, price)`（`0xB55A17`）交给 lounge 业务层（机体创建估价结果）；两个字段名均由块内日志串给出（`result=` `0xB55992`、`price=` `0xB559B7`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x129C` | `0xB5593C` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 估价结果码（能否创建 / 校验结果） | 交 `vt[0x2A8]` 第 1 实参；日志 `result=`（`sub_B03580` = 有符号十进制打印） | - | `0xB558A3`（`sub_B02DD0` 读）、`0xB55986`/`0xB55992`（日志名）、`0xB55A09`/`0xB55A17`（去向） | 确证 |
| 2 | 4 | 4 | u32 | `price` | 创建所需价格（货币量） | 交 `vt[0x2A8]` 第 2 实参；日志 `price=` | - | `0xB558E3`（`sub_B02DD0` 读）、`0xB559B1`/`0xB559B7`（日志名）、`0xB55A03`/`0xB55A11`（去向） | 确证 |
| - | 8 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0x8` == 线长 `8` | - | `0xB558F3`|`0xB558F9` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB5593C` 落在 `sub_B51930` 的 case 块 `0xB55853..0xB55A33`。
2. 入口 `sub_B41120`（case 守卫）→ `push 8; call [eax+78h]`（容量 8）→ `sub_ABB2F0` 初始化线游标。
3. 两处「槽预留 `sub_B41470` ＋ bounded 读 `sub_B02DD0`」成对，各消费 4 字节。
4. 去向：`0xB559FF mov eax,[var_2C48]`（price 槽）/ `0xB55A05 mov eax,[var_2C38]`（result 槽）/ `0xB55A0B mov edx,[edx+2A8h]` / `0xB55A17 call edx`（实参序：result, price）。

### 4.2 长度闭合
- 消费量 `4 + 4 = 8`，与容量 `0x8` 精确相等；闭合点 `0xB558F3`/`0xB558F9` 要求「游标 == 末尾」✓

### 4.3 存疑点
见 `notes.md`（`result` 的枚举取值表未交叉；`price` 是否为「单价」还是「总价」待与请求侧字段对照）。

## 5. 质量门自检

- [x] G1 字段表总长（8）与 `0xB558F3`/`0xB558F9` 闭合校验一致，且等于容量 `0x8`。
- [x] G2 两个字段类型均指回 `sub_B02DD0`（u32，游标步进 +4 @`0xB02DE9`）与内联 `mov`/`movzx` 使用点；未使用伪代码类型。
- [x] G3 含义来自日志串 `result=` / `price=`；用途指向 `vt[0x2A8]`（`0xB55A17`，2 实参）。
- [x] G4 不确定项（`result` 枚举、`price` 口径）已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求侧命令文件名为 `?`（未在本批 DRAFT 内），已在 §1 说明。
