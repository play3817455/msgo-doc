# SC-0x0D24-lounge-pilot_bot_checkcode_request

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0D24` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_bot_checkcode_request` |
| 名字字符串 | `)->_proto_lounge_client::recv_pilot_bot_checkcode_request( `，引用点 `0xB55150`（`push offset aProtoLoungeCli_18`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB550B7` .. `0xB55234`（块首即 `push 3Ch`，错误码 `0x3C`） |
| 错误码 | `0x3C`（`0xB55112 push 3Ch` → `vt[0x64](1, 0x3C)`） |
| 关联命令 | 配对请求 `../CS-0x93EE-lounge-pilot_bot_checkcode_request_r/`（`0x93EE`，容量 `0x12`）；后续应答 `../SC-0xCA2C-lounge-pilot_bot_checkcode_result/`（`0xCA2C`） |

## 2. 结论摘要

- **报文体总长：变长 = `L + 1`**（单个 NUL 结尾字符串，`L = strlen(code) ≤ 12`）。
- 长度校验：`0xB55122 mov ebx,[esp+var_2C44]`（线游标）、`0xB55126 cmp ebx,[esp+var_2C40]`（vs 报文末尾）、`0xB5512A jnz loc_B5510B`（不等 ⇒ 报错）⇒ **整包精确消费完** ⇒ 只有这一个字段。
- 声明容量 `push 0Dh`（`0xB550D0`）= **13 == 该串的槽位预算**（`sub_B02BA0` 的第 3 实参也是 `0xD`）⇒ 串长上限 `L ≤ 12`；容量口径与「串 claim == 槽位预算」一致。
- 是否分帧：否。
- 关键结论：唯一的 `code` 以 **NUL 结尾串**上线，交 `vt[0xF0]`（`0xB551FD` 取虚表项 / `0xB55206` 调用），唯一实参 = 串首地址；块内日志 `code="`（`0xB551A4`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0D24` | `0xB55150`（名字串引用点） | 确证 |
| 1 | 0 | `L+1` | bytes（NUL 串） | `code` | 机器人（Bot）验证码字符串 | 交 `vt[0xF0]`（唯一实参 = 串首地址 `0xB55204 push eax`）；日志 `code="`（`0xB551A4`） | `L = strlen ≤ 12` | `0xB550FD`（`sub_B02BA0`，预算 `0xB550EA push 0Dh`）；`0xB02BEE mov [edi],esi`（游标 += 串长+1）；`0xB551A4`（日志）；`0xB551FD`（去向） | 确证 |
| — | `L+1` | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB55126`（`cmp`）、`0xB5512A`（`jnz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB55150` 落在 `sub_B51930` 的 case 块 `0xB550B7..0xB55234` 内（错误码 `0x3C`）。
2. 字段 = 「`vt[0x78](0xD)` 申请 13B 解码缓冲」+「`push 0xD; call sub_B02BA0`」的变长串读取（`sub_B02BA0(dst, &cursor, maxlen)`）。
3. 读取后立即做「游标 == 末尾」校验，说明**后面没有别的字段**。
4. 含义取自日志串 `code="`（`0xB551A4`，注意其前后拼的引号串 `0xEDAD54` = `"`）。
5. 去向：`0xB551F7 mov edx,[esi]` / `0xB551FD mov edx,[edx+0F0h]` / `0xB55203 push eax`（`eax = [var_2C3C]` = 缓冲首址）/ `0xB55206 call edx` ⇒ `vt[0xF0](code)`。

### 4.2 长度闭合
- `L+1`；闭合点 `0xB55126`/`0xB5512A` 要求「游标 == 末尾」✓（只有一个字段）。
- 容量 13 == 槽位预算（串 claim）；实际线长 `L+1 ≤ 13`。

### 4.3 存疑点
见 `notes.md`（`vt[0xF0]` 业务定名、`code` 的字符集/长度是否还有更严的语义约束）。

## 5. 质量门自检

- [x] G1 字段表总长（`L+1`）与 `0xB55126`/`0xB5512A` 的「游标 == 末尾」校验一致；容量 13 == 串槽预算。
- [x] G2 线类型指回汇编 VA（`0xB550FD` + `0xB02BEE`，NUL 串族）；未使用伪代码类型。
- [x] G3 含义取自块内日志串 `code="`，用途追到 `vt[0xF0]`（`0xB55206`）。
- [x] G4 不确定项（`vt[0xF0]` 业务定名）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `0x93EE`、后续应答 `0xCA2C` 已在 §1 链接。
