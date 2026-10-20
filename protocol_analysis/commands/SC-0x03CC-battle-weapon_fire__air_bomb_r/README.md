# SC-0x03CC-weapon_fire__air_bomb_r

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x03CC` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__air_bomb_r`（名字串里是双下划线 `__`） |
| 名字符串 | `)->_proto_battle_client::recv_weapon_fire__air_bomb_r(` @ `0xEE0508`，xref `0xB0CF10` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0CD3B` .. `0xB0D137`（块首 `0xB0CD3B call sub_B05DA0`；全部错误路径 `push 86h`，如 `0xB0CD9E`/`0xB0CED6` ⇒ 本 case 开关/错误码 `0x86`） |
| 关联命令 | 发出侧 `_proto_battle_client::send_weapon_fire__air_bomb`（C→S `0xC90D`，声明容量 `0x22`）→ `../CS-0xC90D-battle-weapon_fire__air_bomb/`；同族 `weapon_fire__air_bomb_intercepted`（C→S `0xE1C1`） |

## 2. 结论摘要

- **报文体总长：`20` 字节**（opcode `2` + 负载 `18`）。
- 负载 = **`u16 ent_id` + `u32 itemid` + `u32 airbomb_id` + 3×`u16`(target_x/y/z) + 2×`u8`**，
  即 `2 + 4 + 4 + 2 + 2 + 2 + 1 + 1 = 18`。
- 长度校验：`0xB0CEC3` 取读完后的游标，`0xB0CEC7 cmp ebx, [esp+1B3Ch+var_1B24]`（vs 报文末尾），`0xB0CECD jz ok`（不等 ⇒ `push 86h` 报错）。
- 声明容量 `push 12h`（`0xB0CD50`）= `18` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**空中炸弹（air bomb）发射广播**；发射者实体 + 武器物品 + 炸弹 ID + 目标坐标 + 弹道状态 + 特效开关，8 值一次性交 `vt[0x1C4]`（`0xB0D11B`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x03CC` | `0xB0CF10`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 发射者实体 ID | 交 `vt[0x1C4]` 第 1 实参；日志 `ent_id=`（`0xB0CF67`） | - | `0xB0CD8B`（`sub_B02DF0`）；本体 `0xB02E01`+`0xB02E0B`；日志 `0xB0CF5A`~`0xB0CF67` | 确证 |
| 2 | 2 | 4 | u32 | `itemid` | 武器（物品）ID | 交 `vt[0x1C4]` 第 2 实参；日志 `itemid=`（`0xB0CF91`） | - | `0xB0CDCB`（`sub_B02DD0`）；本体 `0xB02DE1`+`0xB02DE9`；日志 `0xB0CF82`~`0xB0CF91` | 确证 |
| 3 | 6 | 4 | u32 | `airbomb_id` | 空爆弹 ID（武器子类型/弹药 ID） | 交 `vt[0x1C4]` 第 3 实参；日志 `airbomb_id=`（`0xB0CFBB`） | - | `0xB0CDEF`（`sub_B02DD0`）；日志 `0xB0CFAC`~`0xB0CFBB` | 确证 |
| 4 | 10 | 2 | u16 | `target_x` | 目标点 X 坐标 | 交 `vt[0x1C4]` 第 4 实参；日志 `target_x=`（`0xB0CFE6`） | - | `0xB0CE13`（`sub_B02DF0`）；日志 `0xB0CFD6`~`0xB0CFE6` | 确证 |
| 5 | 12 | 2 | u16 | `target_y` | 目标点 Y 坐标 | 交 `vt[0x1C4]` 第 5 实参；日志 `target_y=`（`0xB0D011`） | - | `0xB0CE3B`（`sub_B02DF0`）；日志 `0xB0D001`~`0xB0D011` | 确证 |
| 6 | 14 | 2 | u16 | `target_z` | 目标点 Z 坐标 | 交 `vt[0x1C4]` 第 6 实参；日志 `target_z=`（`0xB0D03C`） | - | `0xB0CE63`（`sub_B02DF0`）；日志 `0xB0D02C`~`0xB0D03C` | 确证 |
| 7 | 16 | 1 | u8 | `shot0_drop1_impact2` | 炸弹阶段：`0`=发射(shot) / `1`=投下(drop) / `2`=命中(impact) | 交 `vt[0x1C4]` 第 7 实参；日志 `shot0_drop1_impact2=`（`0xB0D064`） | `0/1/2`（由字段名自解释；**未**在客户端找到枚举表 ⇒ 标 `推测`） | `0xB0CE8B`（`sub_B06230`）；本体 `0xB06241`+`0xB06249`；日志 `0xB0D057`~`0xB0D064` | 确证(类型) / 枚举 `推测` |
| 8 | 17 | 1 | u8 | `fx_opt` | 特效选项（客户端表现开关） | 交 `vt[0x1C4]` 第 8 实参；日志 `fx_opt=`（`0xB0D089`） | `?` | `0xB0CEB3`（`sub_B06230`）；日志 `0xB0D081`~`0xB0D089` | 确证(类型) / 含义 `推测` |
| — | 18 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB0CEC3`（`mov ebx,[esp+var_1B28]`）、`0xB0CEC7`（`cmp ebx,[esp+var_1B24]`）、`0xB0CECD`（`jz`） | 确证 |

**去向**（8 个值一次性交付）：`0xB0D0D3`..`0xB0D11B` —— `mov edx,[esi]; mov edx,[edx+1C4h]`；
按 `fx_opt`(u8) → `target_z`(u16) → `target_y`(u16) → `target_x`(u16) → `airbomb_id`(u32) → `itemid`(u32) → `ent_id`(u16)
（外加 `shot0_drop1_impact2` u8）依次压栈后 `call vt[0x1C4]`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE0508` 的引用点 `0xB0CF10` 落在 battle 分发器 `sub_B0CC20` 的 case 块 `0xB0CD3B..0xB0D137` 内。
2. 全部错误路径统一 `push 1; push 86h`（`0xB0CD9C`/`0xB0CD9E`、`0xB0CED4`/`0xB0CED6`）⇒ 本 case 开关/错误码 = `0x86`。

### 4.2 长度闭合
- 读取序列：`sub_B413B0`+`sub_B02DF0`(u16) → `sub_B41470`+`sub_B02DD0`(u32) → `sub_B41470`+`sub_B02DD0`(u32)
  → `sub_B413B0`+`sub_B02DF0`(u16) ×3 → `sub_B05E30`+`sub_B06230`(u8) ×2。
- 消费量 = `2+4+4+2+2+2+1+1` = **18** 字节；随即 `0xB0CEC7` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 12h`（`0xB0CD50`）= 18（旁证）。

### 4.3 存疑点
见 `notes.md`（`shot0_drop1_impact2` 枚举、`fx_opt` 取值、`vt[0x1C4]` 实现）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 18 字节；`游标 == 末尾` 校验在 `0xB0CEC7`/`0xB0CECD`。
- [x] G2 类型均指回汇编 VA（u16 `0xB02E0B`；u32 `0xB02DE9`；u8 `0xB06249`）；未使用伪代码类型。
- [x] G3 含义取自 8 条块内日志串；用途追到 `vt[0x1C4]`（`0xB0D11B`）；推测项已标 `推测`。
- [x] G4 不确定项标 `?`/`推测` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对命令（发出侧 `0xC90D weapon_fire__air_bomb`）已在 §1 链接。
