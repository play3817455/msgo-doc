# SC-0x0943-entity_msma_disappear

> 状态：`DONE`（2026-09-20，批次-3）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0943` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `entity_msma_disappear` |
| 名字符串 | `)->_proto_battle_client::recv_entity_msma_disappear(` @ `0xEE0354`，引用点 `0xB0E0A5` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0DFA1` .. `0xB0E1D1`（块首 `call sub_B05DA0`，错误码 `0x57`） |
| 关联命令 | 相关：`SC-0x0120 entity_msma_show`(DONE)、`SC-0x130A entity_msma_hide`(DRAFT)、`SC-0x1EA5 entity_msma_reborn`(DRAFT)；无配对 C→S |

## 2. 结论摘要

- **报文体总长：定长 8 字节**（u16 + u32 + u16）。
- 长度校验：`0xB0E05E mov ebx,[esp+var_1B28]`（游标）、`0xB0E062 cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0E068 jz ok`（不等 ⇒ `push 57h` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 8`（`0xB0DFB6`）= **8 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：3 个值交 `vt[0x15C]`（`0xB0E1A1` 取虚表项 / `0xB0E1B5` 调用），实参顺序 `(ent_id, reason, not_use)`；块内日志 `ent_id=` / `reason=` / `not_use=`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0943` | `0xB0E0A5`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 实体 ID（消失的机体实体） | 交 `vt[0x15C]`（第 1 实参 `0xB0E1B2 push edx`）；日志 `ent_id=`（`0xB0E0FC`，十六进制打印器 `sub_B032A0`） | `-` | `0xB0DFF1`（`sub_B02DF0`）；槽预留 `0xB0DFE2`（`sub_B413B0`）；`0xB02E0B add [eax],2`；日志 `0xB0E0FC` | 确证 |
| 2 | 2 | 4 | u32 | `reason` | 消失原因（枚举） | 交 `vt[0x15C]`（第 2 实参 `0xB0E1AE push edx`）；日志 `reason=`（`0xB0E126`，十进制） | `?`（原因枚举未交叉） | `0xB0E02E`（`sub_B02DD0`）；槽预留 `0xB0E01F`（`sub_B41470`）；日志 `0xB0E126` | 类型确证 / 枚举待定 |
| 3 | 6 | 2 | u16 | `not_use` | 保留/未使用（原名字面） | 交 `vt[0x15C]`（第 3 实参 `0xB0E1A7 push edx`）；日志 `not_use=`（`0xB0E14C`） | `-` | `0xB0E052`（`sub_B02DF0`）；槽预留 `0xB0E043`（`sub_B413B0`）；日志 `0xB0E14C` | 确证 |
| — | 8 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0E062`（`cmp`）、`0xB0E068`（`jz`） | 确证 |

> 偏移核算：`2 + 4 + 2 = 8` ✓
> ⚠️ 注意 `ent_id` / `not_use` 的**零扩展取值**：交 `vt` 时用 `movzx edx, word ptr [...]`（`0xB0E1AF`、`0xB0E198`），字段本身仍是 u16。

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE0354` 的引用点 `0xB0E0A5` 落在 `sub_B0CC20` 的 case 块 `0xB0DFA1..0xB0E1D1` 内（全部错误路径 `0xB0E004`/`0xB0E071` 用错误码 `0x57`）。
2. 三个字段 = 三组「槽预留 + bounded 读取器」：`sub_B413B0`+`sub_B02DF0`（u16，`0xB0DFF1`）、`sub_B41470`+`sub_B02DD0`（u32，`0xB0E02E`）、`sub_B413B0`+`sub_B02DF0`（u16，`0xB0E052`）。
3. 块内日志顺序（`ent_id=` → `reason=` → `not_use=`）与线序一致。
4. 去向：`0xB0E1A1 mov eax,[eax+15Ch]` ⇒ `vt[0x15C]`，实参按 `(ent_id, reason, not_use)` 入栈（`0xB0E1A7`/`0xB0E1AE`/`0xB0E1B2`）。

### 4.2 长度闭合
- `2 + 4 + 2 = 8`；闭合点 `0xB0E062` 要求「游标 == 末尾」✓
- 容量 8 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`reason` 枚举、`not_use` 字段是否真「未使用」）。

## 5. 质量门自检

- [x] G1 字段表总长（8）与 `0xB0E062`/`0xB0E068` 的「游标 == 末尾」校验一致；容量 8 == 线长。
- [x] G2 线类型指回汇编 VA（u16 `0xB0DFF1`/`0xB0E052`；u32 `0xB0E02E`；游标步进 `0xB02E0B`/`0xB02DE9`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（`ent_id=`/`reason=`/`not_use=`），用途追到 `vt[0x15C]`（`0xB0E1B5`）。
- [x] G4 不确定项（`reason` 枚举、`not_use` 语义）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令为战服 S→C 通知，无配对请求；已与同族实体命令互链。
