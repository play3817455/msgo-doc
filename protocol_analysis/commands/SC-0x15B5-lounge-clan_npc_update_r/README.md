# SC-0x15B5-lounge-clan_npc_update_r

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x15B5` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_npc_update_r` |
| 名字字符串 | `)->_proto_lounge_client::recv_clan_npc_update_r( `，引用点 `0xB561A0`（`push offset aProtoLoungeCli_25`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB560B0` .. `0xB56297` |
| 错误码 | `0x1C1`（`0xB560B0 push 1C1h` 守卫 / `0xB5611A`、`0xB56166` 读失败） |
| 关联命令 | 同族氏族命令：`../SC-0x143D-lounge-clan_create_r/`（`0x143D`）、`../SC-0x1600-lounge-clan_leave_r/`（`0x1600`）；氏族 NPC 相关：`0x15B5` 与 `0x143D` 共用 `result` 字段口径 |

## 2. 结论摘要

- **报文体总长：定长 `8` 字节**（2 个 u32）。
- 长度校验方式：`0xB56153 mov ebx,[var_2C44]` / `0xB56157 cmp ebx,[var_2C40]`（线游标 vs 报文末尾）＋ `0xB5615D jz ok` ⇒ 读完 2 个 u32 后游标必须已在末尾。
- 声明容量：`0x8`（`0xB560CC push 8`）⇒ 容量 `8` **精确等于**线长 `8`。
- 是否分帧：否。
- 关键结论：`result`（u32，`result=` `0xB561F6`）＋ `npc_id`（u32，`npc_id=` `0xB5621B`），经 `vt[0x444](result, npc_id)`（`0xB5627B`）交付（氏族 NPC 更新结果）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x15B5` | `0xB561A0` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 氏族 NPC 更新的处理结果码 | 交 `vt[0x444]` 第 1 实参；日志 `result=`（`sub_B03580`） | `?`（枚举未交叉） | `0xB56107`（`sub_B02DD0` 读）、`0xB561EA`/`0xB561F6`（日志名）、`0xB56269`/`0xB5627B`（去向） | 确证 |
| 2 | 4 | 4 | u32 | `npc_id` | 更新涉及的 NPC ID | 交 `vt[0x444]` 第 2 实参；日志 `npc_id=` | `?`（NPC 枚举/表未交叉） | `0xB56147`（`sub_B02DD0` 读）、`0xB56211`/`0xB5621B`（日志名）、`0xB5626F`（去向） | 确证 |
| - | 8 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0x8` == 线长 `8` | - | `0xB56153`|`0xB5615D` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB561A0` 落在 `sub_B51930` 的 case 块 `0xB560B0..0xB56297`（块首 `0xB560B0 push 1C1h`）。
2. 入口 `call sub_B41120`（守卫）→ `push 8; call [edx+78h]`（容量 8）→ `sub_ABB2F0` 初始化线游标。
3. 两处「`sub_B41470` 槽预留 + `sub_B02DD0` bounded 读」成对，各 4 字节。
4. 去向：`0xB56263 mov eax,[var_2C48]`（npc_id 槽）/ `0xB56269 mov eax,[var_2C38]`（result 槽）/ `0xB5626F mov edx,[edx+444h]` / `0xB5627B call edx`（实参序 `result, npc_id`）。

### 4.2 长度闭合
- 消费量 `4 + 4 = 8`；闭合点 `0xB56157`/`0xB5615D` 要求「游标 == 末尾」，与容量 `0x8` 精确相等 ✓

### 4.3 存疑点
见 `notes.md`（`npc_id` 来源表；`result` 枚举与 `0x143D`/`0x1600` 是否同一；`vt[0x444]` 业务定名）。

## 5. 质量门自检

- [x] G1 字段表总长（8）与 `0xB56157`/`0xB5615D` 闭合校验一致，且等于容量 `0x8`。
- [x] G2 两个 u32 均指回 `0xB56107`/`0xB56147`（`sub_B02DD0`，步进 +4）；未使用伪代码类型。
- [x] G3 含义来自日志串 `result=` / `npc_id=`；用途指向 `vt[0x444]`（`0xB5627B`，2 实参）。
- [x] G4 枚举未定项已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 同族 `0x143D`/`0x1600` 已在 §1 链接。
