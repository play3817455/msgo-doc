# SC-0x0825-weapon_state_update

> 状态：`DONE`（2026-09-20，批次-2）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0825` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `weapon_state_update` |
| 名字符串 | `)->_proto_battle_client::recv_weapon_state_update( ` @ `0xEE0320`，引用点 `0xB0E2D9` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0E1D1` .. `0xB0E407`（块首 `0xB0E1D1 push 73h; call sub_B05DA0`，错误码 `0x73`） |
| 关联命令 | 同族（武器状态）：`../SC-0x03CC-battle-weapon_fire__air_bomb_r/`、`../SC-0x1A13-battle-weapon_fire__hand_throw_r/`、`../SC-0x6D20-battle-weapon_fire__deploy_arms_r/`；本命令**无同名发送侧** |

## 2. 结论摘要

- **报文体总长：定长 `6` 字节** = `2+2+2`（三个 u16）。
- 负载 = 实体 ID + 武器状态 + 武器变更标志。
- 长度校验：`0xB0E292 mov ebx,[esp+var_1B28]`（游标）、`0xB0E296 cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0E29C jz ok`（不等 ⇒ `push 73h` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 6`（`0xB0E1EA`）= 6，**与线长相等** ✓。
- 是否分帧：否。
- 关键结论：3 个值交 `vt[0x1A0]`（`0xB0E3D6` 取虚表项 / `0xB0E3EB` 调用），实参顺序 `(ent_id, weapon_state, weapon_change_flag)`；三者均以 `movzx`（零扩展 u16）取值。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0825` | `0xB0E2D9`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 实体 ID | 交 `vt[0x1A0]`（第 1 实参）；日志 `ent_id=`（`0xB0E330`，十六进制打印 `sub_B032A0`） | - | `0xB0E225`（`sub_B02DF0`）；`0xB02E0B add [eax],2`；日志 `0xB0E330` | 确证 |
| 2 | 2 | 2 | u16 | `weapon_state` | 武器状态 | 交 `vt[0x1A0]`（第 2 实参）；日志 `weapon_state=`（`0xB0E35B`，十六进制） | `?`（枚举取值未定，见 `notes.md` Q1） | `0xB0E262`（`sub_B02DF0`）；日志 `0xB0E35B` | 类型确证 / 枚举待定 |
| 3 | 4 | 2 | u16 | `weapon_change_flag` | 武器切换标志 | 交 `vt[0x1A0]`（第 3 实参）；日志 `weapon_change_flag=`（`0xB0E381`，十六进制） | `?`（位义未定） | `0xB0E286`（`sub_B02DF0`）；日志 `0xB0E381` | 类型确证 / 位义待定 |
| — | 6 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0E296`（`cmp`）、`0xB0E29C`（`jz`） | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE0320` 的引用点 `0xB0E2D9` 落在 `sub_B0CC20` 的 case 块 `0xB0E1D1..0xB0E407` 内。
2. 块首 `0xB0E1D1 push 73h; call sub_B05DA0` 与全部错误路径（`0xB0E238`、`0xB0E2A5`）一致使用错误码 `0x73`。
3. 两次「预留槽 + 有界读取」成对出现（`0xB0E216`/`0xB0E225`、`0xB0E253`/`0xB0E262`、`0xB0E277`/`0xB0E286`），失败均跳回 `0xB0E231`。
4. 日志区顺序（`ent_id=` → `weapon_state=` → `weapon_change_flag=`）与线序一致。

### 4.2 长度闭合
- `2 + 2 + 2 = 6`；闭合点 `0xB0E296` 要求「游标 == 末尾」；声明容量 `6` ⇒ 一致 ✓。

### 4.3 存疑点
见 `notes.md`（`weapon_state`/`weapon_change_flag` 枚举与位义、`vt[0x1A0]` 去向）。

## 5. 质量门自检

- [x] G1 字段表总长（6）与 `0xB0E29C` 的「游标 == 末尾」校验一致；容量 6 == 负载 6。
- [x] G2 线类型指回汇编 VA（u16 `0xB0E225`/`0xB0E262`/`0xB0E286` + `0xB02E0B` 游标 +2）；未使用伪代码类型。
- [x] G3 字段含义取自块内日志串（`ent_id=`、`weapon_state=`、`weapon_change_flag=`），用途追到 `vt[0x1A0]`（`0xB0E3EB`）。
- [x] G4 不确定项（枚举/位义）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令无同名配对请求（已链接同族武器命令）。
