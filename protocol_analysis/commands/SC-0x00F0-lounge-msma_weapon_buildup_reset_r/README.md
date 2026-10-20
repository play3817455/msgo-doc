# SC-0x00F0-msma_weapon_buildup_reset_r

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x00F0` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_buildup_reset_r` |
| 名字符串 | `)->_proto_lounge_client::recv_msma_weapon_buildup_reset_r(` @ `0xEEA19C`，xref `0xB51B65` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB51A58` .. `0xB51C95`（块首 `0xB51A58 call sub_B41120`；本 case 开关/错误码 `0x118`，见 `0xB51ABB`） |
| 关联命令 | 发出侧 `_proto_lounge_client::send_msma_weapon_buildup_reset`（C→S `0x8DEB`）→ `../CS-0x8DEB-lounge-msma_weapon_buildup_reset/` |

## 2. 结论摘要

- **报文体总长：`16` 字节**（opcode `2` + 负载 `14`）。
- 负载 = **2 × `u32` + 1 × `u64`**（`result` @0、`uniqid_ms` @4、`item_id` @12）。
- 长度校验：`0xB51B18` 取读完后的游标，`0xB51B1C cmp ebx, [esp+2C5Ch+var_2C40]`（vs 报文末尾），`0xB51B22 jz ok`（不等 ⇒ `push 118h` 报错）。
- 声明容量 `push 10h`（`0xB51A6D`）= `16` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**武器强化（buildup）重置应答**；`result`＝结果码，`uniqid_ms`＝机体唯一 ID，`item_id`＝被重置的物品 ID。三值一次性交 `vt[0x2D8]`（`0xB51C79`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x00F0` | `0xB51B65`（名字串引用点，锚定 case 归属） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 处理结果码 | 交 `vt[0x2D8]`（`0xB51C79`）第 1 实参；日志 `result=`（`0xB51BBB`） | - | `0xB51AA8`（`call sub_B02DD0`，本体 `0xB02DE9 add dword ptr [eax], 4`）；日志 `0xB51BAF`~`0xB51BBB` | 确证 |
| 2 | 4 | 8 | u64 | `uniqid_ms` | 机体唯一 ID | 交 `vt[0x2D8]` 第 2/3 实参（`0xB51C56`/`0xB51C69` 压 `[eax+4]`、`[eax]`）；日志 `uniqid_ms=`（`0xB51BE9`） | - | `0xB51AE8`（`call sub_B06200`，本体 `0xB06206 lea edx,[ecx+8]`、`0xB06220 add dword ptr [eax], 8`） | 确证 |
| 3 | 12 | 4 | u32 | `item_id` | 物品 ID（被重置的强化物品） | 交 `vt[0x2D8]` 第 4 实参（`0xB51C5A`/`0xB51C68` 压 `[eax]`）；日志 `item_id=`（`0xB51C0E`） | - | `0xB51B0C`（`call sub_B02DD0`）；日志 `0xB51C04`~`0xB51C0E` | 确证 |
| — | 16 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB51B18`（`mov ebx,[esp+var_2C44]`）、`0xB51B1C`（`cmp ebx,[esp+var_2C40]`）、`0xB51B22`（`jz`） | 确证 |

**去向**（3 个值一次性交付）：`0xB51C56`..`0xB51C79` ——
`mov eax,[var_2C24]`（item_id）→ `mov ecx,[eax]`；`mov eax,[var_2C10]`（u64 槽）→ `push [eax+4]; push [eax]`；
`mov ecx,[var_2C00]`（result）→ `push [ecx]` ⇒ `call vt[0x2D8]`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA19C` 的引用点 `0xB51B65` 落在 `sub_B51930`（lounge 分发器）的 case 块 `0xB51A58..0xB51C95` 内。
2. 全套错误路径统一 `push 1; push 118h`（`0xB51AB9`/`0xB51ABB`），与块首 case 开关号 `0x118` 一致。

### 4.2 长度闭合
- 读取序列：预留 u32 槽 → `sub_B02DD0`(u32) → 预留 u64 槽 → `sub_B06200`(u64) → 预留 u32 槽 → `sub_B02DD0`(u32)。
- 消费量 = `4 + 8 + 4` = **16** 字节；随即 `0xB51B1C` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 10h`（`0xB51A6D`）= 16（旁证）。

### 4.3 存疑点
见 `notes.md`（`vt[0x2D8]` 实现未展开；`result` 枚举未知）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 16 字节；`游标 == 末尾` 校验在 `0xB51B1C`/`0xB51B22`。
- [x] G2 类型均指回汇编 VA（u32 `0xB02DE9`；u64 `0xB06206`/`0xB06220`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串 `result=`/`uniqid_ms=`/`item_id=`；用途追到 `vt[0x2D8]`（`0xB51C79`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对命令（发出侧 `0x8DEB msma_weapon_buildup_reset`）已在 §1 链接。
