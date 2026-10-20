# SC-0x1600-lounge-clan_leave_r

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x1600` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_leave_r` |
| 名字字符串 | `)->_proto_lounge_client::recv_clan_leave_r( `，引用点 `0xB55F56`（`push offset aProtoLoungeCli_24`） |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB55E21` .. `0xB560B0` |
| 错误码 | `0x1B1`（`0xB55E84 push 1B1h`、`0xB55F1C`；块首 `0xB55E21 call sub_B41120`（无立即数）） |
| 关联命令 | 同族氏族命令：`../SC-0x143D-lounge-clan_create_r/`（`0x143D`，创建）、`../SC-0x15B5-lounge-clan_npc_update_r/`（`0x15B5`）；编成相关：`deckcost` 与机库编成（`character_msdeck`）同口径 |

## 2. 结论摘要

- **报文体总长：定长 `13` 字节**（4 个字段：u32 + u32 + u8 + u32）。
- 长度校验方式：`0xB55F09 mov ebx,[var_2C44]` / `0xB55F0D cmp ebx,[var_2C40]`（线游标 vs 报文末尾）＋ `0xB55F13 jz ok` ⇒ 读完 4 个字段后游标必须已在末尾。
- 声明容量：`0xD`（`0xB55E36 push 0Dh`）⇒ 容量 `13` **精确等于**线长 `4+4+1+4 = 13`。
- 是否分帧：否。
- 关键结论：字段 `result`（u32）、`clan_id`（u32）、`clan_kind`（u8）、`deckcost`（u32），经 `vt[0x424](result, clan_id, clan_kind, deckcost)`（`0xB56094`）交付（退出氏族结果 + 编成费用）。四个字段名全部由块内日志串确证（`result=`/`clan_id=`/`clan_kind=`/`deckcost=`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x1600` | `0xB55F56` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 退出氏族的处理结果码 | 交 `vt[0x424]` 第 1 实参；日志 `result=` | `?`（枚举未交叉） | `0xB55E71`（`sub_B02DD0` 读）、`0xB55FA0`/`0xB55FAC`（日志名）、`0xB5608A`/`0xB56094`（去向） | 确证 |
| 2 | 4 | 4 | u32 | `clan_id` | 所退出的氏族 ID | 交 `vt[0x424]` 第 2 实参；日志 `clan_id=` | `?`（氏族表未交叉） | `0xB55EB1`（`sub_B02DD0` 读）、`0xB55FC7`/`0xB55FD6`（日志名）、`0xB56083`（去向） | 确证 |
| 3 | 8 | 1 | u8 | `clan_kind` | 氏族种类/类别 | 交 `vt[0x424]` 第 3 实参（`movzx` 零扩展）；日志 `clan_kind=`（`sub_B0C1F0`） | `?`（氏族类别枚举未交叉） | `0xB55ED5`（`sub_B06230` 读）、`0xB5606D`/`0xB56080`（`movzx byte ptr` + 去向）、`0xB55FFE`（日志名） | 确证（宽度）/枚举待定 |
| 4 | 9 | 4 | u32 | `deckcost` | 退出后编成费用（机库编成消耗） | 交 `vt[0x424]` 第 4 实参；日志 `deckcost=` | `?`（单位/口径未交叉） | `0xB55EF9`（`sub_B02DD0` 读）、`0xB56015`/`0xB56025`（日志名）、`0xB56077`（去向） | 确证 |
| - | 13 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0xD` == 线长 `4+4+1+4 = 13` | - | `0xB55F09`|`0xB55F13` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB55F56` 落在 `sub_B51930` 的 case 块 `0xB55E21..0xB560B0`。
2. 入口 `call sub_B41120`（守卫）→ `push 0Dh; call [eax+78h]`（容量 13）→ `sub_ABB2F0` 初始化线游标。
3. 读取序列：`sub_B41470`+`sub_B02DD0`(u32) → `sub_B41470`+`sub_B02DD0`(u32) → `sub_B05E30`+`sub_B06230`(u8) → `sub_B41470`+`sub_B02DD0`(u32)。
4. 去向：`0xB5606D`…`0xB56092` 依 cdecl 逆序 push，`0xB56094 call edx`（`edx = [esi]+0x424`），实参序 `(result, clan_id, clan_kind, deckcost)`。

### 4.2 长度闭合
- 消费量 `4 + 4 + 1 + 4 = 13`；闭合点 `0xB55F0D`/`0xB55F13` 要求「游标 == 末尾」，与容量 `0xD` **精确相等** ✓

### 4.3 存疑点
见 `notes.md`（`clan_kind` 枚举；`deckcost` 口径；`vt[0x424]` 业务定名）。

## 5. 质量门自检

- [x] G1 字段表总长（13）与 `0xB55F0D`/`0xB55F13` 闭合校验一致，且等于容量 `0xD`。
- [x] G2 三个 u32 指回 `sub_B02DD0`（步进 +4 @`0xB02DE9`）；u8 指回 `sub_B06230`（步进 +1 @`0xB06249`）；未使用伪代码类型。
- [x] G3 四个字段含义全部来自块内日志串（`result=`/`clan_id=`/`clan_kind=`/`deckcost=`）；用途指向 `vt[0x424]`（`0xB56094`，4 实参）。
- [x] G4 枚举/口径未定项已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 同族 `0x143D`/`0x15B5` 已在 §1 链接。
