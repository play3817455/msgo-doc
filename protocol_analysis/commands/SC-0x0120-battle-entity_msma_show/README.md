# SC-0x0120-entity_msma_show

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0120` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `entity_msma_show` |
| 名字符串 | `)->_proto_battle_client::recv_entity_msma_show(` @ `0xEE0488`，xref `0xB0D3C7` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0D320` .. `0xB0D48F`（块首 `0xB0D320 push 5Dh; mov ecx,esi; call sub_B05DA0`，`5Dh` 即本 case 开关/错误码） |
| 关联命令 | 同族：`entity_msma_show_hp`(`0xE4DB`)、`entity_msma_hide`(`0x130A`)、`entity_msma_disappear`(`0x0943`)；找不到同名 `send_entity_msma_show`（C→S 无配对命令） |

## 2. 结论摘要

- **报文体总长：`4` 字节**（opcode `2` + 负载 `2`）。
- 负载 = **1 × `u16`**（`ent_id` @0）。
- 长度校验：`0xB0D399` 取读完后的游标，`0xB0D39D cmp ebx, [esp+1B3Ch+var_1B24]`（vs 报文末尾），`0xB0D3A1 jnz 错误`（不等 ⇒ `push 5Dh` 报错）。
- 声明容量 `push 2`（`0xB0D339`）= `2` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**战场上让指定实体（机体）显示**；`ent_id`＝实体 ID，交 `vt[0x174]`（`0xB0D473`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0120` | `0xB0D3C7`（名字串引用点，锚定 case 归属） | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 实体 ID（战场上的机体/单位） | 交 `vt[0x174]`（`0xB0D473`）；日志 `ent_id=`（`0xB0D419`） | - | `0xB0D374`（`call sub_B02DF0`，本体 `0xB02E01 mov cx,[ecx]`、`0xB02E0B add dword ptr [eax], 2`）；日志 `0xB0D411`~`0xB0D419` | 确证 |
| — | 2 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB0D399`（`mov ebx,[esp+var_1B28]`）、`0xB0D39D`（`cmp ebx,[esp+var_1B24]`）、`0xB0D3A1`（`jnz`） | 确证 |

**去向**：`0xB0D461`..`0xB0D473` —— `mov eax,[esp+var_1B2C]`（`sub_B413B0` 返回的 u16 槽）→
`movzx ecx, word ptr [eax]` → `mov edx,[esi]; mov edx,[edx+174h]` → `push ecx` ⇒ `call vt[0x174](ent_id)`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE0488` 的引用点 `0xB0D3C7` 落在 battle 分发器 `sub_B0CC20` 的 case 块 `0xB0D320..0xB0D48F` 内。
2. 块首 `0xB0D320 push 5Dh; call sub_B05DA0` 与全部错误路径 `push 5Dh`（如 `0xB0D389`）一致，确认 case 归属与错误码。

### 4.2 长度闭合
- 读取序列：预留 u16 槽（`sub_B413B0`，非字段）→ `sub_B02DF0` 读 u16。
- 消费量 = **2** 字节；随即 `0xB0D39D` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 2`（`0xB0D339`）= 2（旁证）。

### 4.3 存疑点
见 `notes.md`（`vt[0x174]` 实现未展开）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 2 字节；`游标 == 末尾` 校验在 `0xB0D39D`/`0xB0D3A1`。
- [x] G2 类型指回汇编 VA（`0xB02E01` 读 u16 + `0xB02E0B` 游标 +2）；未使用伪代码类型。
- [x] G3 含义取自日志串 `ent_id=`；用途追到 `vt[0x174]`（`0xB0D473`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 无配对 C→S 命令（已在 §1 说明，并列出同族命令）。
