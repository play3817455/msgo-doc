# SC-0x1165-battle-msma_AI_uninstall

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x1165` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_uninstall` |
| 名字字符串 | `)->_proto_battle_client::recv_msma_AI_uninstall( `，引用点 `0xB0F529`（`push offset aProtoBattleCli_15`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0F479` .. `0xB0F609` |
| 错误码 | `0xB6`（`0xB0F479 push 0B6h` 守卫 / `0xB0F4E5 push 0B6h` 读失败） |
| 关联命令 | 同族机体通知：`../SC-0x130A-battle-entity_msma_hide/`（`0x130A`，同为「单 ID + 虚表派发」）；显示侧 `../SC-0x0120-battle-entity_msma_show/`。**本命令无配对请求**（服务端主动通知） |

## 2. 结论摘要

- **报文体总长：定长 `2` 字节**（1 个字段）。
- 长度校验方式：处理块末尾 `0xB0F4FC cmp ebx,[esp+var_1B24]`（线游标 vs 报文末尾）＋ `0xB0F500 jnz 报错`；读完第 1 个字段后游标必须已在末尾 ⇒ 负载恰为 2 字节，块内**无其它读取器**。
- 声明容量：`0x2`（`0xB0F495 push 2` + `0xB0F497 call [edx+78h]`）⇒ 容量 `2` **精确等于**线长 `2`（S→C 定长强相等）。
- 是否分帧：否。
- 关键结论：唯一字段 `AI_ent_id`（u16）经 `vt[0x244](AI_ent_id)`（`0xB0F5D5`）交给 battle 业务层，语义为「解除某实体的 AI 安装」；块内日志串 `AI_ent_id=`（`0xB0F57B`，`0xB0F577 movzx ecx,word ptr [eax]`）给出字段名。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x1165` | `0xB0F529`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `AI_ent_id` | 要解除 AI 的实体 ID | 交 `vt[0x244]`（第 1 实参）；块内日志 `AI_ent_id=` 回显 | - | `0xB0F4D0`（`sub_B02DF0` 读）、`0xB0F577`（`movzx word ptr`）、`0xB0F57B`（日志名）、`0xB0F5C3`/`0xB0F5D5`（去向） | 确证 |
| - | 2 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0x2` == 线长 `2` | - | `0xB0F4FC`|`0xB0F500` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0F529` 落在 `sub_B0CC20` 的 case 块 `0xB0F479..0xB0F609`（块首 `0xB0F479 push 0B6h` 即错误码）。
2. 入口先 `call sub_B05DA0`（case 起始守卫，**不读线**）→ `push 2; call [edx+78h]`（解码缓冲容量 2）→ `sub_ABB2F0` 初始化线游标。
3. 唯一读取：`sub_B413B0`（u16 槽预留，**非字段**）＋ `sub_B02DF0`（读 u16，`0xB0F4D0`）。
4. 去向：`0xB0F5C3 mov eax,[var_1B2C]` / `0xB0F5C7 movzx ecx,word ptr [eax]` / `0xB0F5CC mov edx,[edx+244h]` / `0xB0F5D5 call edx`。

### 4.2 长度闭合
- 消费量 `2`（仅 1 次 `sub_B02DF0`，游标步进 +2）。
- 闭合点 `0xB0F4FC`/`0xB0F500` 要求「游标 == 末尾」；容量 `0x2` 与消费量精确相等 ⇒ 双向印证 ✓

### 4.3 存疑点
见 `notes.md`（`vt[0x244]` 的业务定名；`AI_ent_id` 指向「AI 机体实体」还是「机体的 AI 槽」未交叉）。

## 5. 质量门自检

- [x] G1 字段表总长（2）与 `0xB0F4FC`/`0xB0F500` 的「游标 == 末尾」校验一致，且等于容量 `0x2`。
- [x] G2 类型 `u16` 指回 `0xB0F4D0`（`sub_B02DF0`，游标步进 +2 @`0xB02E0B`）与 `0xB0F577`（`movzx word ptr`）；未使用伪代码类型。
- [x] G3 字段含义来自日志串 `AI_ent_id=`（`0xB0F57B`）；用途指向 `vt[0x244]`（`0xB0F5D5`）。
- [x] G4 不确定项（`vt[0x244]` 业务名、实体语义）已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 同族命令已在 §1 链接（本命令无配对请求）。
