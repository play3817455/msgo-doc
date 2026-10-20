# SC-0x056D-battleship_cooltime_notice

> 状态：`DONE`（2026-09-20，批次-2）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x056D` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `battleship_cooltime_notice` |
| 名字符串 | `)->_proto_battle_client::recv_battleship_cooltime_notice( ` @ `0xEE03D4`，引用点 `0xB0DB03` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0DA13` .. `0xB0DBFC`（块首 `0xB0DA13 push 102h; call sub_B05DA0`，错误码 `0x102`） |
| 关联命令 | 同族（战舰）：`../CS-0xBA58-battle-battleship_ride/`、`../SC-0xE014-battle-battleship_ride_r/`、`../SC-0x5B98-battle-battleship_limittime_notice/`、`../CS-0xF4B9-battle-battleship_get_down/`、`../SC-0x1EC7-battle-battleship_get_down_r/`；本命令**无同名发送侧** |

## 2. 结论摘要

- **报文体总长：定长 `6` 字节** = `2`(to_ent_id) + `4`(remain_msec)。
- 负载 = 1 个 u16 目标实体 ID + 1 个 u32 剩余毫秒。
- 长度校验：`0xB0DAB6 mov ebx,[esp+var_1B28]`（游标）、`0xB0DABA cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0DAC0 jz ok`（不等 ⇒ `push 102h` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 6`（`0xB0DA2F`）= 6，**与线长相等** ✓。
- 是否分帧：否。
- 关键结论：2 个值交 `vt[0x310]`（`0xB0DBD3` 取虚表项 / `0xB0DBE0` 调用），实参顺序 `(to_ent_id, remain_msec)`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x056D` | `0xB0DB03`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `to_ent_id` | 冷却提示目标实体 ID（谁的战舰进入冷却） | 交 `vt[0x310]`（第 1 实参）；日志 `to_ent_id=`（`0xB0DB5A`，十六进制打印 `sub_B032A0`） | - | `0xB0DA6A`（`sub_B02DF0`）；`0xB02E0B add [eax],2`；日志 `0xB0DB5A` | 确证 |
| 2 | 2 | 4 | u32 | `remain_msec` | 剩余冷却时间（毫秒） | 交 `vt[0x310]`（第 2 实参）；日志 `remain_msec=`（`0xB0DB7F`，十进制） | `?`（单位按名称为 ms，块内无换算） | `0xB0DAAA`（`sub_B02DD0`）；`0xB02DE9 add [eax],4`；日志 `0xB0DB7F` | 类型确证 / 单位按名称 |
| — | 6 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0DABA`（`cmp`）、`0xB0DAC0`（`jz`） | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE03D4` 的引用点 `0xB0DB03` 落在 `sub_B0CC20` 的 case 块 `0xB0DA13..0xB0DBFC` 内。
2. 块首 `0xB0DA13 push 102h; call sub_B05DA0` 与全部错误路径（`0xB0DA7D`、`0xB0DAC9`）一致使用错误码 `0x102`。
3. 2 次「预留槽 + 有界读取」成对出现（`0xB0DA5B`/`0xB0DA6A`、`0xB0DA9B`/`0xB0DAAA`），失败均跳回 `0xB0DA76`。
4. 日志区顺序（`to_ent_id=` → `remain_msec=`）与线序一致。

### 4.2 长度闭合
- `2 + 4 = 6`；闭合点 `0xB0DABA` 要求「游标 == 末尾」；声明容量 `6` ⇒ 一致 ✓。

### 4.3 存疑点
见 `notes.md`（`vt[0x310]` 去向、`remain_msec` 单位与客户端是否自行倒计时）。

## 5. 质量门自检

- [x] G1 字段表总长（6）与 `0xB0DAC0` 的「游标 == 末尾」校验一致；容量 6 == 负载 6。
- [x] G2 线类型指回汇编 VA（u16 `0xB02E0B`；u32 `0xB02DE9`）；未使用伪代码类型。
- [x] G3 字段含义取自块内日志串（`to_ent_id=`、`remain_msec=`），用途追到 `vt[0x310]`（`0xB0DBE0`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令无同名配对请求（已链接同族战舰命令）。
