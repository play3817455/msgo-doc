# SC-0x0E85-battle-commander_list_get_r

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0E85` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `commander_list_get_r` |
| 名字字符串 | `)->_proto_battle_client::recv_commander_list_get_r( `，引用点 `0xB0ED77`（`push offset aProtoBattleCli_11`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0EC1F` .. `0xB0EF02`（块首即 `push 0D2h`，错误码 `0xD2`） |
| 错误码 | `0xD2`（`0xB0EC89 push 0D2h` → `vt[0x64](1, 0xD2)`） |
| 关联命令 | 配对请求 `../CS-0xDAE0-battle-commander_list_get/`（`0xDAE0`，容量 `0xA`） |

## 2. 结论摘要

- **报文体总长：变长 = `8 + 4N`**（`result` u32 + `count` u32 + `commander_id[count]` u32；`N ≤ 4`）。
- 长度校验：`0xB0ED2A mov ecx,[esp+var_1B28]`（线游标）、`0xB0ED2E cmp ecx,[esp+var_1B24]`（vs 报文末尾）、`0xB0ED34 jz loc_B0ED50`（不等 ⇒ 报错）⇒ **整包精确消费完**。
- 声明容量 `push 18h`（`0xB0EC3B`）= **24 == 上限场景线长** `8 + 4×4`（`count` 上限 4，见 `0xB0ECD4 cmp ebx,4`）⇒ **容量 ≠ 实际线长**，只是上限。
- 是否分帧：否。
- 关键结论：`result` + `count` + 列表交 `vt[0x290]`（`0xB0EE94` 取虚表项 / `0xB0EEA1` 调用），**实参顺序 `(result, commander_id 数组, count)`**；块内日志 `result=`、`commander_id={ ... }`（元素逗号分隔）。
- 机器草案把「数组预留 `sub_B41850`」误记成一个字段（草案 #3），并漏读了循环内的元素读取器（草案 #4 与 #3 实为同一处）；**本文件已更正**。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0E85` | `0xB0ED77`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 指挥官列表查询结果码 | 交 `vt[0x290]` 第 1 实参（`0xB0EE9E push eax`）；日志 `result=`（`0xB0EDCD`） | `?`（结果码枚举未交叉） | `0xB0EC76`（`sub_B02DD0`）；槽预留 `0xB0EC67`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB0EDCD` | 类型确证 / 枚举待定 |
| 2 | 4 | 4 | u32 | `count` | 指挥官 ID 列表元素个数 | 上限检查 `cmp ebx,4 / ja 报错`（`0xB0ECD4`）；交 `vt[0x290]` 第 3 实参（`0xB0EE9A push ebx`）；驱动数组填充循环 | `0..4` | `0xB0ECA8`（`sub_B02DD0`）；`0xB0ECD4`（`cmp`）/`0xB0ECD7`（`ja`） | 确证 |
| 3 | 8 | `4N` | array\<u32,N\> | `commander_id` | 可选指挥官 ID 列表 | 交 `vt[0x290]` 第 2 实参（`0xB0EE9B push eax` = 数组基址）；日志以 `commander_id={` 起、元素逗号分隔、`}` 收尾 | `-` | 数组预留 `0xB0ECE3`（`sub_B41850`，4B/槽）；元素读取 `0xB0ED00`（`sub_B02DD0`）；循环步进 `0xB0ED0C add [var_1B2C],4`；循环上界 `0xB0ED14 cmp edi,ebx` | 确证 |
| — | `8+4N` | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0ED2E`（`cmp`）、`0xB0ED34`（`jz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0ED77` 落在 `sub_B0CC20` 的 case 块 `0xB0EC1F..0xB0EF02` 内（错误码 `0xD2`）。
2. 前两个字段 = 两组「槽预留 + bounded 读取器」；第 2 个读完后立即 `cmp ebx,4 / ja` ⇒ 它是列表**计数**（上限 4）。
3. `push ebx; lea eax,[var_1B14]; push eax; lea ecx,[var_1B08]; call sub_B41850` ⇒ 预留 `ebx × 4` 字节数组，基址入 `var_1B08`。
4. 循环 `edi = 0..ebx-1`：`sub_B02DD0(槽, &线游标)`，槽地址每次 `+= 4` ⇒ 元素线长 **4**（与 4B 槽步进、循环步进三方一致）。
5. 含义取自块内日志 `result=` / `commander_id={`；去向 `vt[0x290]`。

### 4.2 长度闭合
- `4 + 4 + 4N = 8 + 4N`；闭合点 `0xB0ED2E`/`0xB0ED34` 要求「游标 == 末尾」✓
- 容量 `0x18 = 24` 恰为 `N = 4` 时的线长 ⇒ 与「容量 = 上限场景线长」判别法一致，同时确证元素线长 4 与上限 4。
- 若 `count == 0`，无循环、无数组字节（`sub_B41850` 对 `N = 0` 不推进游标）。

### 4.3 存疑点
见 `notes.md`（`result` 枚举、`commander_id` 的 ID 空间、与 C→S `0xDAE0` 的字段对应）。

## 5. 质量门自检

- [x] G1 字段表总长（`8+4N`）与 `0xB0ED2E`/`0xB0ED34` 的「游标 == 末尾」校验一致；容量 24 == 上限场景线长。
- [x] G2 线类型指回汇编 VA（`0xB0EC76`/`0xB0ECA8`/`0xB0ED00` + `0xB02DE9`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串，用途追到 `vt[0x290]`（`0xB0EEA1`）。
- [x] G4 不确定项（`result` 枚举）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `CS-0xDAE0-battle-commander_list_get` 已在 §1 链接。
