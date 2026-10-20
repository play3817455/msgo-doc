# SC-0xFCD2-pilot_rental_module_remain_info_notice

> 状态：`DONE`
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xFCD2` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_rental_module_remain_info_notice` |
| 名字符串 | `)->_proto_lounge_client::recv_pilot_rental_module_remain_info_notice( ` @ `0xee55a0` |
| 代码位置 | sub_B51930 @ `0xb51930`　块 `0xb88255`..`0xb884cd` |
| opcode 写入/分发证据 | `0xb8835d`（命令名字符串引用点 = case 归属锚点）|
| 处理块范围 | `0xB88255`..`0xB884CD` |
| 声明容量 | `0x600`（1536） |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：2 字段，均为**固定 128 元数组、无线上 count**：`hav_rental_modules`（元素 8B，读取器 2×u32）与 `empty_rental_modules`（u32）。容量 1536 == 1024 + 512 精确相等。
- 长度校验方式：处理块内「**游标 == 报文末尾**」闭合检查 @`0x00B8831A`。
- 去向锚点：`vt[0xEC]`（2 个实参）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0xFCD2` | `0xb8835d` | 确证 |
| 1 | 0 | 1024 | array<2×u32,128> | `hav_rental_modules` | 已持有租用模块 ID 列表（128 项） | 整块预留 `sub_B412A0`（`0xB412A0`：`add edx,400h` 一次推进 1024）；元素读取器 `sub_B434B0`（`0xB434B0`，2×u32 = 8B）循环 128 次（`cmp edi,80h`，步进 8）；去向 `vt[0xEC]` 第 1 实参（`0xB884AE push ecx`） | 元素 8B / 槽 8B / 上限 128 | `0xB88299,0xB882AA` | 确证 |
| 2 | 1024 | 512 | array<u32,128> | `empty_rental_modules` | 可租用（空槽）模块 ID 列表（128 项） | `sub_B02DD0` 循环 128 次（`0xB882ED`，步进 4，`cmp edi,80h`）；去向 `vt[0xEC]` 第 2 实参（`0xB884AD push eax`） | 元素 4B / 上限 128 | `0xB882ED` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 处理块 `0xB88255..0xB884CD`（lounge_client 分发器 `0xB51930`）；守卫 = `sub_B41120(lounge(0x3B))`，收尾 = `sub_B41110`。
- 解码缓冲分配：`mov ecx,[esi+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push 0x600; call edx`（`0x600` 为**容量**，非线长）。

### 4.2 长度闭合
- 闭合点：`0x00B8831A`（游标寄存器与报文末尾比较，`jz`/`jnz` 走成功分支）。
- 容量校验：`0x600`=1536 = 128×8 + 128×4 ✓（两个数组**均无线上 count**，上限为字面量 128）。

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（游标==末尾 @`0x00B8831A`）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
