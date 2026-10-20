# CS-0x9527-lounge-msma_equipset_store

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x9527` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_equipset_store` |
| 名字符串 | `)<-_proto_lounge_client::send_msma_equipset_store(` @ `0xeebcb0` |
| 代码位置 | sub_B98E80 @ `0xb98e80`（`0xb98e80`..`0xb99093`） |
| opcode 写入证据 | `0xb98f02` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x86`（134） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x7172-lounge-msma_equipset_store_r`（已 DONE，equip_set claim 128/线长 121） |

## 2. 结论摘要

- 结论：保存机体装备套组（equipset）：机体 uniqid + 由复合写入器 `sub_B41C60` 写入的 121 字节装备套组结构。
- 字段数：**11**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 8(u64) + 121(equip_set 结构) = 131 ≤ 容量 0x86 = 134`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x9527` | `0xb98f02` | 确证 |
| 1 | 2 | 8 | u64 | `uniqid_ms` | 机体唯一 id | 来源=入参 arg_0/arg_4（低 32 位在前，两个内联 `mov [eax],ecx`/`mov [eax+4],ecx`）；服务端据此定位机体 | - | `0xB98F12, 0xB98F20` | 确证 |
| 2 | 10 | 8 | u64 | `equip_set.uniq_id` | 装备套组唯一 id | 来源=结构成员 `[src+0]`（写入器 `sub_B41C60`：`mov edx,[edi]; mov [ecx],edx` / `mov edx,[edi+4]; mov [ecx+4],edx`）；打印器 `sub_B4AA30` 名 `uniq_id` | - | `0xB41C73, 0xB41C7B` | 确证 |
| 3 | 18 | 2 | u16 | `equip_set.slot` | 套组槽位号 | 来源=结构成员 `[src+8]`（`mov dx,[edi+8]; mov [ecx],dx`）；打印器成员名 `slot` | - | `0xB41C92` | 确证 |
| 4 | 20 | 12 | u32[3] | `equip_set.eq_weapon` | 装备武器（3 项） | 来源=结构成员 `[src+0Ch..0x14]`（循环 3 次，`add edx,4`@0xB41CBD，`cmp ecx,3`@0xB41CC0）；打印器成员 `eq_weapon={` | 3×u32，**无线上计数** | `0xB41CA3 (loop @0xB41CA3..0xB41CC3)` | 确证 |
| 5 | 32 | 4 | u32 | `equip_set.eq_shield` | 装备盾 | 来源=结构成员 `[src+18h]`（`mov edx,[edi+18h]; mov [esi],edx`）；打印器成员 `eq_shield` | - | `0xB41CD1` | 确证 |
| 6 | 36 | 4 | u32 | `equip_set.eq_special` | 装备特殊装备 | 来源=结构成员 `[src+1Ch]`；打印器成员 `eq_special` | - | `0xB41CE7` | 确证 |
| 7 | 40 | 40 | u32[10] | `equip_set.eq_modules` | 装备模块（10 项） | 来源=结构成员 `[src+20h..0x44]`（循环 10 次，`cmp edx,0Ah`@0xB41D1B）；打印器成员 `eq_modules={` | 10×u32，**无线上计数** | `0xB41D00 (loop @0xB41D00..0xB41D1E)` | 确证 |
| 8 | 80 | 4 | u32 | `equip_set.eq_bonus_modules` | 奖励模块（1 项） | 来源=结构成员 `[src+48h]`（循环 1 次，`cmp edx,1`@0xB41D3C）；打印器成员 `eq_bonus_modules={` | 1×u32（固定 1 项数组） | `0xB41D25 (loop @0xB41D25..0xB41D3F)` | 确证 |
| 9 | 84 | 4 | u32 | `equip_set.eq_rental_modules` | 租赁模块（1 项） | 来源=结构成员 `[src+4Ch]`（循环 1 次，`cmp edx,1`@0xB41D5D）；打印器成员 `eq_rental_modules={` | 1×u32（固定 1 项数组） | `0xB41D46 (loop @0xB41D46..0xB41D60)` | 确证 |
| 10 | 88 | 43 | u8[43] | `equip_set.setname` | 套组名（43 字节定长字符数组） | 来源=结构成员 `[src+50h..0x7A]`（循环 `cmp ecx,2Bh`=43 次，逐字节 `mov dl,[ecx+edi+50h]`@0xB41D6E）；打印器成员 `setname` | 定长 43 字节，**无 NUL 保证**（按固定字节数读写） | `0xB41D64 (loop @0xB41D64..0xB41D7D)` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb98ec6`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb98f02`（`mov word ptr [...], 0x9527`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 8(u64) + 121(equip_set 结构) = 131 ≤ 容量 0x86 = 134`（富余 3）

### 4.3 存疑点
- `equip_set` 为**复合写入器** `sub_B41C60`（`0xB41C60..0xB41D92`）写入，共 **121 字节**（8+2+12+4+4+40+4+4+43），成员名取自打印器 `sub_B4AA30`（`0xb4aa30`）；与 S→C 侧 `SC-0x7172` 的 equip_set 线长 121 一致。
- `eq_weapon[3]` / `eq_modules[10]` / `eq_bonus_modules[1]` / `eq_rental_modules[1]` 均为**固定元素数、无线上计数**（循环上界为字面量）。
- `setname` 为 43 字节定长字符数组（无长度前缀、无 NUL 写入），打印器按 C 串处理 ⇒ 实际内容约定见服务端实现。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
