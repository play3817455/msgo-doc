# SC-0x143D-lounge-clan_create_r

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x143D` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_create_r` |
| 名字字符串 | `)->_proto_lounge_client::recv_clan_create_r( `，引用点 `0xB55D0E`（`push offset aProtoLoungeCli_23`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB55C1E` .. `0xB55E21` |
| 错误码 | `0x1AF`（`0xB55C1E push 1AFh` 守卫 / `0xB55C88`、`0xB55CD4` 读失败） |
| 关联命令 | 同族氏族命令：`../SC-0x1600-lounge-clan_leave_r/`（`0x1600`，退出氏族，同 `result`+`clan_kind` 组）、`../SC-0x15B5-lounge-clan_npc_update_r/`（`0x15B5`）；应答侧创建请求 `../CS-0x----`（未在本批 DRAFT 内） |

## 2. 结论摘要

- **报文体总长：定长 `5` 字节**（2 个字段：u32 + u8）。
- 长度校验方式：`0xB55CC1 mov ebx,[var_2C44]` / `0xB55CC5 cmp ebx,[var_2C40]`（线游标 vs 报文末尾）＋ `0xB55CCB jz ok` ⇒ 读完 2 字段后游标必须已在末尾 ⇒ 负载 5 字节。
- 声明容量：`0x5`（`0xB55C3A push 5`）⇒ 容量 `5` **精确等于**线长 `5`（虽然字段 2 是 u8，容量仍按「槽位」记账 4+1）。
- 是否分帧：否。
- 关键结论：`result`（u32，`result=` `0xB55D64`）＋ `clan_kind`（u8，`clan_kind=` `0xB55D87`），经 `vt[0x420](result, clan_kind)`（`0xB55DEA`）交付；`clan_kind` 在派发时用 `movzx byte ptr`（`0xB55DD5`）零扩展 ⇒ 无符号。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x143D` | `0xB55D0E` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 创建氏族的处理结果码 | 交 `vt[0x420]` 第 1 实参；日志 `result=`（`sub_B03580`） | - | `0xB55C75`（`sub_B02DD0` 读）、`0xB55D58`/`0xB55D64`（日志名）、`0xB55DDC`/`0xB55DEA`（去向） | 确证 |
| 2 | 4 | 1 | u8 | `clan_kind` | 所创建氏族的种类/类别 | 交 `vt[0x420]` 第 2 实参（`movzx` 零扩展）；日志 `clan_kind=`（`sub_B0C1F0`） | `?`（氏族类别枚举未交叉） | `0xB55CB5`（`sub_B06230` 读）、`0xB55DD1`（`movzx byte ptr`）、`0xB55D87`（日志名）、`0xB55DE4`（去向） | 确证（宽度）/枚举待定 |
| - | 5 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0x5` == 线长 `5` | - | `0xB55CC1`|`0xB55CCB` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB55D0E` 落在 `sub_B51930` 的 case 块 `0xB55C1E..0xB55E21`（块首 `0xB55C1E push 1AFh` 即错误码）。
2. 入口 `call sub_B41120`（守卫）→ `push 5; call [eax+78h]`（容量 5）→ `sub_ABB2F0` 初始化线游标。
3. 读取：`sub_B41470`+`sub_B02DD0`（u32）→ `sub_B05E30`+`sub_B06230`（u8）。
4. 去向：`0xB55DD1 mov ecx,[var_2C48]` / `0xB55DD5 movzx edx,byte ptr [ecx]` / `0xB55DD8 mov ecx,[var_2C38]` / `0xB55DDE mov eax,[eax+420h]` / `0xB55DEA call eax`（实参序 `result, clan_kind`）。

### 4.2 长度闭合
- 消费量 `4 + 1 = 5`；闭合点 `0xB55CC1`/`0xB55CCB` 要求「游标 == 末尾」，与容量 `0x5` 精确相等 ✓

### 4.3 存疑点
见 `notes.md`（`clan_kind` 枚举取值；`vt[0x420]` 业务定名；`result` 与 `0x1600`/`0x15B5` 是否同一枚举）。

## 5. 质量门自检

- [x] G1 字段表总长（5）与 `0xB55CC1`/`0xB55CCB` 闭合校验一致，且等于容量 `0x5`。
- [x] G2 类型 `u32` 指回 `0xB55C75`（`sub_B02DD0`，步进 +4）、`u8` 指回 `0xB55CB5`（`sub_B06230`，步进 +1，复核 `0xB06249`）；未使用伪代码类型。
- [x] G3 含义来自日志串 `result=` / `clan_kind=`；用途指向 `vt[0x420]`（`0xB55DEA`，2 实参）。
- [x] G4 枚举未定项已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 同族 `0x1600`/`0x15B5` 已在 §1 链接。
