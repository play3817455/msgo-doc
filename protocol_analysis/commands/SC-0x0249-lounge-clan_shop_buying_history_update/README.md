# SC-0x0249-clan_shop_buying_history_update

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0249` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_shop_buying_history_update` |
| 名字符串 | `)->_proto_lounge_client::recv_clan_shop_buying_history_update(` @ `0xEEA0C0`，xref `0xB52432` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB52382` .. `0xB524F6`（块首 `0xB52382 push 1EDh`，`1ED` 即本 case 开关/错误码） |
| 关联命令 | INDEX 中无同名 C→S `send_clan_shop_buying_history_update`（无配对请求；本命令为服务端主动/异步通知） |

## 2. 结论摘要

- **报文体总长：`8` 字节**（opcode `2` + 负载 `6`）。
- 负载 = **`u32 item_id` + `u16 num`**，由**一个复合读取器 `sub_B46AB0` 一次性读入**（4 + 2 = 6 字节）。
- 长度校验：`0xB52401` 取读完后的游标，`0xB52405 cmp ebx, [esp+2C5Ch+var_2C40]`（vs 报文末尾），`0xB52409 jnz 错误`（不等 ⇒ `push 1EDh` 报错）。
- 声明容量 `push 8`（`0xB5239E`）**> 负载 6**：这是「按 8 字节槽（u64 预留）分配解码缓冲」的结果 —— 规范 §1 铁律 2 明确**容量 ≠ 线长**，线长以读取器实际消费量为准（见 `notes.md` Q1）。
- 是否分帧：否。
- 关键结论：**家族商店购买历史增量更新**；一项 `{item_id, num}` 作为一个整体交 `vt[0x4A4]`（`0xB524DA`，传**结构体指针**）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。
> 该结构体由 `sub_B46AB0` 一次读入 6 字节（`4 + 2`），本表按线序拆成两行登记。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0249` | `0xB52432`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `item_id` | 物品 ID | 组成 `cshist_item` 结构体交 `vt[0x4A4]`；格式串 `item_id=`（`0xB47AC0`，由 `sub_B47AA0` 打印） | - | `0xB523D9`（`call sub_B46AB0`）；reader 本体 `0xB46ABE`（`mov ecx,[ecx]` + `0xB46AC6 add dword ptr [eax], 4`） | 确证 |
| 2 | 4 | 2 | u16 | `num` | 购买数量 | 同上（结构体第 2 成员）；格式串 `num=`（`0xB47AE3`） | - | `0xB523D9`（`sub_B46AB0`）；reader 本体 `0xB46AD5`（`mov cx,[ecx]` + `0xB46ADC add dword ptr [eax], 2`） | 确证 |
| — | 6 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB52401`（`mov ebx,[esp+var_2C44]`）、`0xB52405`（`cmp ebx,[esp+var_2C40]`）、`0xB52409`（`jnz`） | 确证 |

**去向**：`0xB524CB`..`0xB524DA` —— `mov eax,[esp+2C5Ch+var_2C04]`（`sub_B41A10` 返回的槽地址）
→ `mov edx,[esi]; mov edx,[edx+4A4h]` → `push eax` ⇒ `call vt[0x4A4]`（**传槽指针**，非取值）。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA0C0` 的引用点 `0xB52432` 落在 `sub_B51930` 的 case 块 `0xB52382..0xB524F6` 内。
2. 块首 `0xB52382 push 1EDh` 与错误路径 `0xB523EE push 1EDh` 一致。

### 4.2 长度闭合
- 解码缓冲槽按 **8 字节**预留（`0xB523CA call sub_B41A10`：`0xB41A1A add dword ptr [ecx], 8`），但 `sub_B46AB0` **只消费 6 字节**（u32 + u16）。
- 读取完立即 `0xB52405` 校验「游标 == 末尾」⇒ 负载确为 **6** 字节 ✓；容量 8 只是槽位富余。

### 4.3 存疑点
见 `notes.md`（容量/线长差值、`vt[0x4A4]` 实现）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 6 字节；`游标 == 末尾` 校验在 `0xB52405`/`0xB52409`。
- [x] G2 类型均指回汇编 VA（`0xB46ABE` + `0xB46AC6` ⇒ u32；`0xB46AD5` + `0xB46ADC` ⇒ u16）；未使用伪代码类型。
- [x] G3 含义取自结构体打印器 `sub_B47AA0` 的格式串 `cshist_item={` / `item_id=` / `num=`；用途追到 `vt[0x4A4]`（`0xB524DA`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 无配对 C→S 命令（已在 §1 说明）。
