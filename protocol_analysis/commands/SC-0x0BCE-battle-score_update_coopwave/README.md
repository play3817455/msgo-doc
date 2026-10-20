# SC-0x0BCE-score_update_coopwave

> 状态：`DONE`（2026-09-20，批次-3）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0BCE` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `score_update_coopwave` |
| 名字符串 | `)->_proto_battle_client::recv_score_update_coopwave(` @ `0xEE0268`，引用点 `0xB0EA2D` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0E879` .. `0xB0EC1F`（块首 `0xB0E879 push 0ADh; call sub_B05DA0`，错误码 `0x0AD`） |
| 关联命令 | 相关 `SC-0x8D59 score_update`(DRAFT，普通计分)；本命令为**联合作战波次**计分，无配对 C→S |

## 2. 结论摘要

- **报文体总长：定长 22 字节**（4×u32 + 3×u16 交错）。
- 长度校验：`0xB0E9E0 mov ebx,[esp+var_1B28]`（游标）、`0xB0E9E4 cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0E9EA jz ok`（不等 ⇒ `push 0ADh` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 16h`（`0xB0E895`）= **22 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：7 个值交 `vt[0x228]`（`0xB0EBDA` 取虚表项 / `0xB0EC03` 调用），实参顺序
  `(reason, world_id, pilot_id, point_gain, point_total, n_cont_kill, bonus_cont_kill)`；块内日志同名。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x0BCE` | `0xB0EA2D`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `reason` | 计分原因（计分类别枚举） | 交 `vt[0x228]`（第 1 实参 `0xB0EC00 push ecx`）；日志 `reason=`（`0xB0EA83`，十进制） | `?`（与 `0x0943 reason` 是否同表未核） | `0xB0E8D0`（`sub_B02DD0`）；槽预留 `0xB0E8C1`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB0EA83` | 类型确证 / 枚举待定 |
| 2 | 4 | 4 | u32 | `world_id` | 大区（世界）ID | 交 `vt[0x228]`（第 2 实参 `0xB0EBFD push ecx`）；日志 `world_id=`（`0xB0EAAD`） | `?` | `0xB0E910`（`sub_B02DD0`）；槽预留 `0xB0E901`（`sub_B41470`）；日志 `0xB0EAAD` | 确证 |
| 3 | 8 | 4 | u32 | `pilot_id` | 驾驶员（角色）ID | 交 `vt[0x228]`（第 3 实参 `0xB0EBF6 push ecx`）；日志 `pilot_id=`（`0xB0EAD7`） | `-` | `0xB0E934`（`sub_B02DD0`）；槽预留 `0xB0E925`（`sub_B41470`）；日志 `0xB0EAD7` | 确证 |
| 4 | 12 | 2 | u16 | `point_gain` | 本次获得的积分 | 交 `vt[0x228]`（第 4 实参 `0xB0EBEF push ecx`，`movzx` `0xB0EBE8`）；日志 `point_gain=`（`0xB0EB02`，十六进制） | `-` | `0xB0E958`（`sub_B02DF0`）；槽预留 `0xB0E949`（`sub_B413B0`）；`0xB02E0B add [eax],2`；日志 `0xB0EB02` | 确证 |
| 5 | 14 | 4 | u32 | `point_total` | 累计总积分 | 交 `vt[0x228]`（第 5 实参 `0xB0EBE7 push ecx`）；日志 `point_total=`（`0xB0EB2C`，十进制） | `-` | `0xB0E980`（`sub_B02DD0`）；槽预留 `0xB0E971`（`sub_B41470`）；日志 `0xB0EB2C` | 确证 |
| 6 | 18 | 2 | u16 | `n_cont_kill` | 连续击杀数 | 交 `vt[0x228]`（第 6 实参 `0xB0EBE0 push ecx`）；日志 `n_cont_kill=`（`0xB0EB57`，十六进制） | `-` | `0xB0E9A8`（`sub_B02DF0`）；槽预留 `0xB0E999`（`sub_B413B0`）；日志 `0xB0EB57` | 确证 |
| 7 | 20 | 2 | u16 | `bonus_cont_kill` | 连续击杀奖励加成 | 交 `vt[0x228]`（第 7 实参 `0xB0EBD0 push ecx`）；日志 `bonus_cont_kill=`（`0xB0EB7D`，十六进制） | `-` | `0xB0E9D0`（`sub_B02DF0`）；槽预留 `0xB0E9C1`（`sub_B413B0`）；日志 `0xB0EB7D` | 确证 |
| — | 22 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0E9E4`（`cmp`）、`0xB0E9EA`（`jz`） | 确证 |

> 偏移核算：`4+4+4+2+4+2+2 = 22` ✓

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE0268` 的引用点 `0xB0EA2D` 落在 `sub_B0CC20` 的 case 块 `0xB0E879..0xB0EC1F` 内（全部错误路径 `0xB0E8E3`/`0xB0E9F3` 用错误码 `0x0AD`）。
2. 七个字段 = 七组「槽预留 + bounded 读取器」：u32 ×4（`sub_B41470`+`sub_B02DD0`）、u16 ×3（`sub_B413B0`+`sub_B02DF0`）。
3. 块内日志顺序（`reason=` → `world_id=` → `pilot_id=` → `point_gain=` → `point_total=` → `n_cont_kill=` → `bonus_cont_kill=`）与线序一致。
4. 去向：`0xB0EBDA mov edx,[edx+228h]` ⇒ `vt[0x228]`，实参 `(reason, world_id, pilot_id, point_gain, point_total, n_cont_kill, bonus_cont_kill)`（`0xB0EBFD`…`0xB0EC00` 入栈）。

### 4.2 长度闭合
- `4+4+4+2+4+2+2 = 22`；闭合点 `0xB0E9E4` 要求「游标 == 末尾」✓
- 容量 `0x16`=22 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`reason` 枚举、与 `0x8D59 score_update` 的字段差异）。

## 5. 质量门自检

- [x] G1 字段表总长（22）与 `0xB0E9E4`/`0xB0E9EA` 的「游标 == 末尾」校验一致；容量 22 == 线长。
- [x] G2 线类型指回汇编 VA（u32 `0xB02DE9`；u16 `0xB02E0B`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（7 个 `xxx=`），用途追到 `vt[0x228]`（`0xB0EC03`）。
- [x] G4 不确定项（`reason` 枚举、`world_id` 取值域）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令为战服 S→C 计分通知，无配对请求；已与 `SC-0x8D59 score_update` 互链。
