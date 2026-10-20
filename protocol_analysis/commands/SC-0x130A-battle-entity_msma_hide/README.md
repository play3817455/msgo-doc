# SC-0x130A-battle-entity_msma_hide

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x130A` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `entity_msma_hide` |
| 名字字符串 | `)->_proto_battle_client::recv_entity_msma_hide( `，引用点 `0xB0F6AC`（`push offset aProtoBattleCli_16`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0F609` .. `0xB0F774` |
| 错误码 | `0x5C`（`0xB0F66E push 5Ch` 读失败；块首 `0xB0F609 call sub_B05DA0`（无立即数）） |
| 关联命令 | **成对**：`../SC-0x0120-battle-entity_msma_show/`（`0x0120`，同一 `ent_id` 出场的反向操作）；`../SC-0x0943-battle-entity_msma_disappear/`（`0x0943`，消失）；隐藏原因的对称命令见 `../SC-0x1165-battle-msma_AI_uninstall/`。**本命令无配对请求**（服务端主动通知） |

## 2. 结论摘要

- **报文体总长：定长 `2` 字节**（1 个字段）。
- 长度校验方式：`0xB0F682 mov ebx,[var_1B28]` / `0xB0F682 cmp ebx,[var_1B24]`（线游标 vs 报文末尾）＋ `0xB0F686 jnz 报错` ⇒ 读完唯一字段后游标必须已在末尾 ⇒ 负载 2 字节。
- 声明容量：`0x2`（`0xB0F61E push 2`）⇒ 容量 `2` **精确等于**线长 `2`。
- 是否分帧：否。
- 关键结论：唯一字段 `ent_id`（u16），经 `vt[0x170](ent_id)`（`0xB0F758`）交给 battle 业务层（隐藏该实体）；字段名由块内日志串 `ent_id=`（`0xB0F6FE`）确证。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x130A` | `0xB0F6AC` | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 要隐藏的实体 ID | 交 `vt[0x170]`（第 1 实参）；块内日志 `ent_id=` 回显 | - | `0xB0F659`（`sub_B02DF0` 读）、`0xB0F6FA`（`movzx word ptr`）、`0xB0F6FE`（日志名）、`0xB0F74F`/`0xB0F758`（去向） | 确证 |
| - | 2 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0x2` == 线长 `2` | - | `0xB0F682`|`0xB0F686` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0F6AC` 落在 `sub_B0CC20` 的 case 块 `0xB0F609..0xB0F774`。
2. 入口 `call sub_B05DA0`（守卫）→ `push 2; call [edx+78h]`（容量 2）→ `sub_ABB2F0` 初始化线游标。
3. 唯一读取：`sub_B413B0`（u16 槽预留，非字段）＋ `sub_B02DF0`（读 u16，`0xB0F659`）。
4. 去向：`0xB0F746 mov eax,[var_1B2C]` / `0xB0F74A movzx ecx,word ptr [eax]` / `0xB0F74F mov edx,[edx+170h]` / `0xB0F758 call edx`。

### 4.2 长度闭合
- 消费量 `2`；闭合点 `0xB0F682`/`0xB0F686` 要求「游标 == 末尾」，容量 `0x2` 与消费量精确相等 ✓

### 4.3 存疑点
见 `notes.md`（`vt[0x170]` 业务定名；`ent_id` 与「机体槽位」映射方式）。

## 5. 质量门自检

- [x] G1 字段表总长（2）与 `0xB0F682`/`0xB0F686` 闭合校验一致，且等于容量 `0x2`。
- [x] G2 类型 `u16` 指回 `0xB0F659`（`sub_B02DF0`，游标步进 +2）与 `0xB0F6FA`（`movzx word ptr`）；未使用伪代码类型。
- [x] G3 含义来自日志串 `ent_id=`（`0xB0F6FE`）；用途指向 `vt[0x170]`（`0xB0F758`）。
- [x] G4 不确定项（`vt[0x170]` 业务名、实体语义）已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 成对命令 `0x0120`（show）已在 §1 互相链接。
