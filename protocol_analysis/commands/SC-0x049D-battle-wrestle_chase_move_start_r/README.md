# SC-0x049D-wrestle_chase_move_start_r

> 状态：`DONE`（2026-09-20，批次-2）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x049D` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `wrestle_chase_move_start_r` |
| 名字符串 | `)->_proto_battle_client::recv_wrestle_chase_move_start_r( ` @ `0xEE044C`，引用点 `0xB0D66B` |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0D48F` .. `0xB0D8AC`（块首 `0xB0D48F push 12Bh; call sub_B05DA0`，错误码 `0x12B`） |
| 关联命令 | 配对发送侧 `../CS-0x05CA-battle-wrestle_chase_move_start/`（容量 `0x26`）；同族 `../SC-0xED22-battle-wrestle_chase_move_end_r/`、`../CS-0x6007-battle-wrestle_chase_move_end/` |

## 2. 结论摘要

- **报文体总长：定长 `20` 字节**（`2 + 4 + 2 + 4 + 2 + 2 + 2 + 2`，无填充、非对齐）。
- 负载 = 8 个字段（1 个 u32 物品 ID + 1 个 u32 抓取 ID + 1 个 u16 实体 ID + 1 个 u16 方向 + 1 个 u16 目标实体 + 3 个 u16 目标坐标）。
- 长度校验：`0xB0D61E mov ebx,[esp+var_1B28]`（游标）、`0xB0D622 cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0D628 jz ok`（不等 ⇒ `push 12Bh` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 14h`（`0xB0D4AB`）= 20，**与线长相等** ✓。
- 是否分帧：否。
- 关键结论：8 个值一次性交 `vt[0x38C]`（`0xB0D855` 取虚表项 / `0xB0D878` 调用），实参顺序 = 线序（`ent_id, itemid, dir_h, wrestle_id, target_ent_id, target_pos_x, target_pos_y, target_pos_z`）。
- **与发送侧不对称**：C→S `0x05CA` 容量 `0x26`=38 与 S→C 20 不等，两侧**不是**同构镜像（详见 `notes.md` Q1，本批未展开 C→S 侧分析）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x049D` | `0xB0D66B`（名字串引用点） | 确证 |
| 1 | 0 | 2 | u16 | `ent_id` | 发起方实体 ID | 交 `vt[0x38C]`（第 1 实参）；日志 `ent_id=`（`0xB0D6C2`，十六进制打印 `sub_B032A0`） | - | `0xB0D4E6`（`sub_B02DF0`）；`0xB02E0B add [eax],2`；日志 `0xB0D6C2` | 确证 |
| 2 | 2 | 4 | u32 | `itemid` | 触发本次抓取/追击的物品（道具）ID | 交 `vt[0x38C]`（第 2 实参）；日志 `itemid=`（`0xB0D6EC`，十进制打印 `sub_B03580`） | - | `0xB0D526`（`sub_B02DD0`）；`0xB02DE9 add [eax],4`；日志 `0xB0D6EC` | 确证 |
| 3 | 6 | 2 | u16 | `dir_h` | 方向（水平角） | 交 `vt[0x38C]`（第 3 实参）；日志 `dir_h=`（`0xB0D717`，十六进制） | `?`（单位/量纲未定，见 `notes.md` Q2） | `0xB0D54A`（`sub_B02DF0`）；日志 `0xB0D717` | 类型确证 / 单位待定 |
| 4 | 8 | 4 | u32 | `wrestle_id` | 抓取（格斗/摔投）动作 ID | 交 `vt[0x38C]`（第 4 实参）；日志 `wrestle_id=`（`0xB0D741`，十进制） | - | `0xB0D56E`（`sub_B02DD0`）；日志 `0xB0D741` | 确证 |
| 5 | 12 | 2 | u16 | `target_ent_id` | 目标实体 ID | 交 `vt[0x38C]`（第 5 实参）；日志 `target_ent_id=`（`0xB0D76C`，十六进制） | - | `0xB0D596`（`sub_B02DF0`）；日志 `0xB0D76C` | 确证 |
| 6 | 14 | 2 | u16 | `target_pos_x` | 目标点 X | 交 `vt[0x38C]`（第 6 实参）；日志 `target_pos_x=`（`0xB0D797`） | `?`（定点/缩放未定） | `0xB0D5BE`（`sub_B02DF0`）；日志 `0xB0D797` | 类型确证 / 单位待定 |
| 7 | 16 | 2 | u16 | `target_pos_y` | 目标点 Y | 交 `vt[0x38C]`（第 7 实参）；日志 `target_pos_y=`（`0xB0D7C2`） | `?` | `0xB0D5E6`（`sub_B02DF0`）；日志 `0xB0D7C2` | 类型确证 / 单位待定 |
| 8 | 18 | 2 | u16 | `target_pos_z` | 目标点 Z | 交 `vt[0x38C]`（第 8 实参）；日志 `target_pos_z=`（`0xB0D7E8`） | `?` | `0xB0D60E`（`sub_B02DF0`）；日志 `0xB0D7E8` | 类型确证 / 单位待定 |
| — | 20 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0D622`（`cmp`）、`0xB0D628`（`jz`） | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE044C` 的引用点 `0xB0D66B` 落在 `sub_B0CC20` 的 case 块 `0xB0D48F..0xB0D8AC` 内。
2. 块首 `0xB0D48F push 12Bh; call sub_B05DA0` 与全部错误路径（`0xB0D4F9`、`0xB0D631`、`0xB0D6C9`）一致使用错误码 `0x12B`。
3. 8 次「`sub_B41470/sub_B413B0` 预留槽 + `sub_B02DD0/sub_B02DF0` 有界读取」成对出现；每次读取失败都跳回同一错误出口（`0xB0D4F2`）。
4. 日志区（`0xB0D6B5..0xB0D7FD`）按**同一顺序**打印 8 个值 ⇒ 字段名与线序一一对应。

### 4.2 长度闭合
- 读取器消费量累加：`2 + 4 + 2 + 4 + 2 + 2 + 2 + 2 = 20`；
- 闭合点 `0xB0D622` 要求「游标 == 末尾」；
- 声明容量 `0x14` = 20 ⇒ 三者一致 ✓。

### 4.3 存疑点
见 `notes.md`（坐标/方向量纲、与 C→S `0x05CA` 的字段对应关系）。

## 5. 质量门自检

- [x] G1 字段表总长（20）与 `0xB0D622` 的「游标 == 末尾」校验一致；容量 20 == 负载 20。
- [x] G2 全部线类型指回汇编 VA（u16：`0xB02E0B` 游标 +2；u32：`0xB02DE9` 游标 +4）；未使用伪代码类型。
- [x] G3 每个字段含义取自块内日志格式串（`ent_id=`/`itemid=`/`dir_h=`/`wrestle_id=`/`target_ent_id=`/`target_pos_x/y/z=`），用途追到 `vt[0x38C]`（`0xB0D878`）。
- [x] G4 不确定项（量纲/枚举）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对发送侧 `CS-0x05CA-battle-wrestle_chase_move_start` 已在 §1 链接（并记明两侧不对称）。
