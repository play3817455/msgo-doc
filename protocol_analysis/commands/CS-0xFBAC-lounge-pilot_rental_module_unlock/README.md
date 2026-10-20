# CS-0xFBAC-lounge-pilot_rental_module_unlock

> 状态：`DONE`（2026-09-20，批次-23）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xFBAC` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_rental_module_unlock` |
| 名字符串 | `)<-_proto_lounge_client::send_pilot_rental_module_unlock( ` @ `0x00EEA710` |
| 代码位置 | `sub_B8C420` @ `0x00B8C420`（`0x00B8C420`..`0x00B8C603`） |
| opcode 写入证据 | `0x00B8C494` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xA`（10） |
| 容量申请证据 | `0x00B8C466`（分配器 `[obj+0Ch]` 的 `vt[0x78]`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0x00B8C594` |
| 提交 | `sub_B02FF0` @ `0x00B8C511` |
| 附加通知回调 | `[obj+79A8h]`（模块 id `0x39`） |
| 配对命令 | S→C `SC-0x7B30-lounge-pilot_rental_module_unlock_r` |

## 2. 结论摘要

- 字段数：**3**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 4 + 4 = 10 == 容量 0xA = 10`（**精确相等**）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | opcode | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xFBAC | `00B8C494` | 确证 |
| 1 | 0 | 4 | u32 | module_id | 要解锁的租赁用模块 ID | 来源=入参 `arg_0` → 内联写 `[eax],esi`(@`0xB8C4A9`) | - | `0xB8C4A9` | 确证 |
| 2 | 4 | 4 | u32 | count | 解锁（购买）数量 | 来源=入参 `arg_4` → 内联写 `[edx],ecx`(@`0xB8C4B5`) | - | `0xB8C4B5` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- opcode：`0x00B8C494`。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。

### 4.2 长度闭合
- `2 + 4 + 4 = 10 == 容量 0xA = 10`（**精确相等**）

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / `notes.md`）
