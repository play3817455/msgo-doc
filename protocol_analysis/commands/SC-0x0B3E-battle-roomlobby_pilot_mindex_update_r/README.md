# SC-0x0B3E-roomlobby_pilot_mindex_update_r

> 状态：`DONE`（2026-09-20，批次-3）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0B3E` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pilot_mindex_update_r` |
| 名字符串 | `)->_proto_battle_client::recv_roomlobby_pilot_mindex_update_r(` @ `0xEE02E0`，引用点 `0xB0E55F` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0E407` .. `0xB0E708`（块首 `0xB0E407 push 0Bh; call sub_B05DA0`，错误码 `0x0B`） |
| 关联命令 | 配对请求 `../CS-0x9B19-battle-roomlobby_pilot_mindex_update/`（`sub_B31E20`，容量 `0x6`） |

## 2. 结论摘要

- **报文体总长：定长 14 字节**（3×u32 + 2×u8）。
- 长度校验：`0xB0E518 mov ebx,[esp+var_1B28]`（游标）、`0xB0E51C cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0E522 jz ok`（不等 ⇒ `push 0Bh` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 0Eh`（`0xB0E420`）= **14 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：5 个值交 `vt[0x8C]`（`0xB0E6AD` 取虚表项 / `0xB0E6CF` 调用），实参顺序 `(result, world_id, pilot_id, member_index, is_commander)`；块内日志 `result=` / `world_id=` / `pilot_id=` / `member_index=` / `is_commander=`。命令名 `mindex` = `member_index`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0B3E` | `0xB0E55F`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 更新结果码 | 交 `vt[0x8C]`（第 1 实参 `0xB0E6CC push ecx`）；日志 `result=`（`0xB0E5B5`，十进制） | `?` | `0xB0E45B`（`sub_B02DD0`）；槽预留 `0xB0E44C`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB0E5B5` | 类型确证 / 枚举待定 |
| 2 | 4 | 4 | u32 | `world_id` | 大区（世界）ID | 交 `vt[0x8C]`（第 2 实参 `0xB0E6C9 push ecx`）；日志 `world_id=`（`0xB0E5DF`） | `?`（`authsv.csv` 大区表） | `0xB0E498`（`sub_B02DD0`）；槽预留 `0xB0E489`（`sub_B41470`）；日志 `0xB0E5DF` | 确证 |
| 3 | 8 | 4 | u32 | `pilot_id` | 驾驶员（角色）ID | 交 `vt[0x8C]`（第 3 实参 `0xB0E6C2 push ecx`）；日志 `pilot_id=`（`0xB0E609`） | `-` | `0xB0E4BC`（`sub_B02DD0`）；槽预留 `0xB0E4AD`（`sub_B41470`）；日志 `0xB0E609` | 确证 |
| 4 | 12 | 1 | u8 | `member_index` | 房间内成员槽位序号（`mindex`） | 交 `vt[0x8C]`（第 4 实参 `0xB0E6BB push ecx`，`movzx` 零扩展 `0xB0E6B4`）；日志 `member_index=`（`0xB0E631`，单字节打印器 `sub_B0C1F0`） | `?`（0..N 槽位） | `0xB0E4E0`（`sub_B06230`）；槽预留 `0xB0E4D1`（`sub_B05E30`）；`0xB06249 add [eax],1`；日志 `0xB0E631` | 确证 |
| 5 | 13 | 1 | u8 | `is_commander` | 该成员是否指挥官 | 交 `vt[0x8C]`（第 5 实参 `0xB0E6B3 push ecx`，`movzx` 零扩展 `0xB0E6A4`）；日志 `is_commander=`（`0xB0E656`） | `?`（0/1 语义未确证） | `0xB0E508`（`sub_B06230`）；槽预留 `0xB0E4F9`（`sub_B05E30`）；日志 `0xB0E656` | 类型确证 / 枚举待定 |
| — | 14 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0E51C`（`cmp`）、`0xB0E522`（`jz`） | 确证 |

> 偏移核算：`4+4+4+1+1 = 14` ✓

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE02E0` 的引用点 `0xB0E55F` 落在 `sub_B0CC20` 的 case 块 `0xB0E407..0xB0E708` 内（错误路径 `0xB0E46E`/`0xB0E52B` 用错误码 `0x0B`）。
2. 五个字段 = 五组「槽预留 + bounded 读取器」：u32 用 `sub_B41470`+`sub_B02DD0`×3；u8 用 `sub_B05E30`+`sub_B06230`（`0xB06249 add [eax],1`）×2。
3. 块内日志顺序（`result=` → `world_id=` → `pilot_id=` → `member_index=` → `is_commander=`）与线序一致。
4. 去向：`0xB0E6AD mov edx,[edx+8Ch]` ⇒ `vt[0x8C]`，实参 `(result, world_id, pilot_id, member_index, is_commander)`；两个 u8 实参在入栈前零扩展（`0xB0E6A4`/`0xB0E6B4`）。

### 4.2 长度闭合
- `4+4+4+1+1 = 14`；闭合点 `0xB0E51C` 要求「游标 == 末尾」✓
- 容量 `0xE`=14 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`member_index` 取值范围、`is_commander` 是否布尔）。

## 5. 质量门自检

- [x] G1 字段表总长（14）与 `0xB0E51C`/`0xB0E522` 的「游标 == 末尾」校验一致；容量 14 == 线长。
- [x] G2 线类型指回汇编 VA（u32 `0xB0E45B`/`0xB0E498`/`0xB0E4BC` + `0xB02DE9`；u8 `0xB0E4E0`/`0xB0E508` + `0xB06249`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（5 个 `xxx=`），用途追到 `vt[0x8C]`（`0xB0E6CF`）。
- [x] G4 不确定项（`result`/`member_index`/`is_commander` 取值域）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `CS-0x9B19-battle-roomlobby_pilot_mindex_update` 已在 §1 链接。
