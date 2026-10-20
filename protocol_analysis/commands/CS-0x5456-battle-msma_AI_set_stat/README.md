# CS-0x5456-battle-msma_AI_set_stat

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x5456` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_set_stat` |
| 名字符串 | `)<-_proto_battle_client::send_msma_AI_set_stat(` @ `0xee1264` |
| 代码位置 | sub_B3CE60 @ `0xb3ce60`（`0xb3ce60`..`0xb3d203`） |
| opcode 写入证据 | `0xb3cee4` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x5E`（94） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：战斗内设置 AI 状态：AI 实体 id + 两组「计数 + u32 数组」。
- 字段数：**6**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 2 + 4 + 4×N1 + 4 + 4×N2（N1,N2 ≤ 10）≤ 2+2+4+40+4+40 = 92 ≤ 容量 0x5E=94（上限场景，富余 2）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 battle 协议类处理块（C→S 无 case 块） | 0x5456 | `0xB3CEE4` | 确证 |
| 1 | 2 | 2 | u16 | `AI_ent_id` | AI 实体 id | 来源=入参 arg_0 的低 16 位（@0xB3CEF6）；内联 `mov [eax],cx`；经 `vt[0x58]` 发送 | - | `0xB3CEFB` | 确证 |
| 2 | 4 | 4 | u32 | `idx_num` | idx 数组元素数（**上限校验 ≤ 10**） | 来源=入参 arg_8（@0xB3CEF8）；写线原语 `sub_B02D80`(u32)；上限 `cmp ebp,0Ah`@0xB3CEF3 | 0..10 | `0xB3CF12` | 确证 |
| 3 | 8 | var | array<u32,N> | `idx` | idx 数组（N = `idx_num`，N ≤ 10） | 来源=入参 arg_4 指向的 u32 数组（@0xB3CF3B `mov ebx,[arg_4]`→`[ebx+eax*4]`）；循环内联 `mov [ecx],ebx`；经 `vt[0x58]` 发送 | 元素 u32，逐个写入 | `0xB3CF42` | 确证 |
| 4 | var | 4 | u32 | `num_num` | num 数组元素数（**上限校验 ≤ 10**） | 来源=入参 arg_10（@0xB3CF55）；写线原语 `sub_B02D80`(u32)；上限 `cmp ebx,0Ah`@0xB3CF59 | 0..10 | `0xB3CF6C` | 确证 |
| 5 | var | var | array<u32,N> | `num` | num 数组（N = `num_num`，N ≤ 10） | 来源=入参 arg_C 指向的 u32 数组（@0xB3CF9A `mov esi,[arg_C]`→`[esi+eax*4]`）；循环内联 `mov [ecx],esi`；经 `vt[0x58]` 发送 | 元素 u32，逐个写入 | `0xB3CFA1` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 2 + 4 + 4×N1 + 4 + 4×N2（N1,N2 ≤ 10）≤ 2+2+4+40+4+40 = 92 ≤ 容量 0x5E=94（上限场景，富余 2）

### 4.3 存疑点
- 日志名序（`AI_ent_id=`→`idx={`→`num={`）与线序一致。
- 两个数组计数字段的日志**未单独打标签**（打印器 `sub_B032A0` 打印计数，数组名由 `idx={`/`num={` 给出）⇒ 计数字段名 `idx_num`/`num_num` 为**推定**，类型/长度已确证。
- 上限 10 由 `cmp ebp,0Ah`@0xB3CEF3 / `cmp ebx,0Ah`@0xB3CF59 判定；超限即跳错误出口 `loc_B3D1EE`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
