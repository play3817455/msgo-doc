# SC-0x1159-battle-game_mapgimmick_update

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x1159` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `game_mapgimmick_update` |
| 名字字符串 | `)->_proto_battle_client::recv_game_mapgimmick_update( `，引用点 `0xB0F00A`（`push offset aProtoBattleCli_12`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0EF02` .. `0xB0F127`（case 起始前导 `0xB0EEFE push 42h`） |
| 错误码 | `0x42`（`0xB0EF5A push 42h` → `vt[0x64](1, 0x42)`） |
| 关联命令 | **无配对请求**（服务端推送地图机关状态）；同类数组样本 `../SC-0x0E85-battle-commander_list_get_r/`（本批） |

## 2. 结论摘要

- **报文体总长：变长 = `4 + 7N`**（u32 `count` + `gimmick_progress[count]`，元素线长 **7**；`N ≤ 32`）。
- 长度校验：`0xB0EFC3 mov ecx,[esp+var_1B28]`（线游标）、`0xB0EFC7 cmp ecx,[esp+var_1B24]`（vs 报文末尾）、`0xB0EFCD jz loc_B0EFE6`（不等 ⇒ 报错）⇒ **整包精确消费完**。
- 声明容量 `push 404h`（`0xB0EF17`）= **1028 = 4 + 32×32** —— 即 `count` 取上限 32、且数组按**结构体跨度 32**记账时的 claim；
  实际线长 `4 + 7N ≤ 228`。⇒ 「结构体数组：容量 claim 用结构体跨度 ≠ 元素线长」的又一例（`_meta\长期记忆.md` §3）。
- 元素读取器 `sub_B07DB0`（整函数 `0xB07DB0..0xB07DFB`）消费 `u32(4) + u8(1) + u16(2) = 7`；缓冲步进 `0x20 = 32`（`sub_B05FC0` 的 `add [edx],20h`，`0xB0EFA8 add [var_1B2C],20h`）。
- 是否分帧：否。
- 关键结论：`count` + 数组交 `vt[0x11C]`（`0xB0F101` 取虚表项 / `0xB0F10B` 调用），实参顺序 `(gimmick_progress 数组, count)`；块内日志 `gimmick_progress={...}`（元素经 `sub_B0B280` 打印）。
- 元素成员名/偏移（取自元素打印器 `sub_B0B280`，与线序一致）：`gauge_now` u32 @ `[0]`、`stat` **i8** @ `[4]`（打印器 `movsx`）、`access_ent_id` u16 @ `[6]`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x1159` | `0xB0F00A`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `count` | 地图机关（gimmick）进度条目数 | 上限检查 `cmp ebx,20h / ja 报错`（`0xB0EF70`）；交 `vt[0x11C]` 第 2 实参（`0xB0F107 push ebx`）；驱动数组循环 | `0..32` | `0xB0EF47`（`sub_B02DD0`）；`0xB0EF70`（`cmp`）/`0xB0EF73`（`ja`） | 确证 |
| 2 | 4 | `7N` | array\<elem,N\> | `gimmick_progress` | 地图机关进度列表 | 交 `vt[0x11C]` 第 1 实参 = 数组基址（`0xB0F108 push eax`）；日志 `gimmick_progress={...}` | 元素线长 7 / 缓冲步进 32 | 数组预留 `0xB0EF7F`（`sub_B05FC0`，步进 `0x20`）；元素读取 `0xB0EF9C`（`sub_B07DB0`）；循环步进 `0xB0EFA8 add [var_1B2C],20h`；上界 `0xB0EFB0 cmp edi,ebx` | 确证 |
| 2.1 | +0 | 4 | u32 | `gimmick_progress.gauge_now` | 机关当前计量值（槽值） | 交 `vt[0x11C]` 的数组元素 `[elem+0]`；日志 `gauge_now=`（`sub_B0B280`） | `-` | 读取 `0xB07DBE`/`0xB07DC4`；打印 `0xB0B295`/`0xB0B2A0` | 确证 |
| 2.2 | +4 | 1 | i8 | `gimmick_progress.stat` | 机关状态 | 数组元素 `[elem+4]`；日志 `stat=`（`sub_B0B280`，`movsx` 符号扩展） | `?`（状态枚举未交叉） | 读取 `0xB07DD4`（`mov cl,[ecx]`，1 字节）；打印 `0xB0B2BB movsx` | 类型确证（符号由打印器判定）/ 枚举待定 |
| 2.3 | +6 | 2 | u16 | `gimmick_progress.access_ent_id` | 触发/访问该机关的实体 ID | 数组元素 `[elem+6]`；日志 `access_ent_id=`（`sub_B0B280`） | `-` | 读取 `0xB07DE6`（`mov cx,[ecx]`，2 字节）/`0xB07DE9`；打印 `0xB0B2E3`/`0xB0B2EB` | 确证 |
| — | `4+7N` | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0EFC7`（`cmp`）、`0xB0EFCD`（`jz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0F00A` 落在 `sub_B0CC20` 的 case 块 `0xB0EF02..0xB0F127` 内（错误码 `0x42`）。
2. `0xB0EF47` 读 u32 → `0xB0EF70 cmp ebx,20h / ja` ⇒ **计数**（上限 32）。
3. `push ebx; lea eax,[var_1B14]; push eax; lea ecx,[var_1B08]; call sub_B05FC0` ⇒ 预留 `ebx × 32` 字节数组（`sub_B05FC0` 内 `add [edx],20h` 循环）。
4. 循环内 `sub_B07DB0(元素地址, &线游标)`，元素地址 `+= 0x20` ⇒ 结构体步进 32。
5. **元素读取器整函数扫描**（`sub_B07DB0`，`0xB07DB0..0xB07DFB`）：消费 `4 + 1 + 2 = 7` ⇒ **元素线长 7 ≠ 缓冲步进 32**。
6. 元素成员名取自元素打印器 `sub_B0B280`（`gauge_now=`/`stat=`/`access_ent_id=`，内存偏移 `[0]`/`[4]`/`[6]`，与线序一致）。
7. 去向 `vt[0x11C](数组, count)`。

### 4.2 长度闭合
- `4 + 7N`；闭合点 `0xB0EFC7`/`0xB0EFCD` 要求「游标 == 末尾」✓
- 容量校验：`1028 = 4 + 32 × 32`（`count` 上限 × 结构体跨度）⇒ **容量 ≠ 线长**；若按元素线长 7 记则只能得到 `4 + 7×32 = 228`，与 1028 不符 —— 反证「数组 claim 用结构体跨度」这一口径。
- 三方对齐（元素线长）：① 元素读取器消费 7（② 缓冲步进 32、③ 数组预留步进 32 是**结构体**步进，不是线长）。

### 4.3 存疑点
见 `notes.md`（`vt[0x11C]` 业务定名、`stat` 枚举、`count == 0` 的语义）。

## 5. 质量门自检

- [x] G1 字段表总长（`4+7N`）与 `0xB0EFC7`/`0xB0EFCD` 的「游标 == 末尾」校验一致；容量 1028 已解释为「上限场景 × 结构体跨度」。
- [x] G2 线类型指回汇编 VA（`0xB0EF47`+`0xB02DE9`；`0xB07DBE`/`0xB07DD4`/`0xB07DE6`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串 + 元素打印器成员名，用途追到 `vt[0x11C]`（`0xB0F10B`）。
- [x] G4 不确定项（`stat` 枚举、`vt[0x11C]` 定名）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令无配对请求；同类样本已在 §1 链接。
