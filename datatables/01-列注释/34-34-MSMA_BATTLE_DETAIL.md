# MSMA_BATTLE_DETAIL ｜ `msma/msma_battle_detail.csv`

- **用途**：★**机体战斗明细的"属性 → 值"长表**★——一个容器装 **13 张子表**，CSV 靠 `col0` 的**属性名**选子表。
- 表ID `34` ｜ 下载序 `34` ｜ 类名 `CMSMABattleDetailTables` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_A47BC0`（容器，**只读 col0**）｜ **列数 16**
  —— ★2026-10-05 由 `3` 改正：`col2..col15` 是**按属性名定宽的值槽**，不是"一个值"（见 §0）

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `attribute_name` | str | — | 属性名（sub_456D90→sub_57BD40 词表分派 13 张子表） |
| 2 | `1` | `entry_key` | str | — | ★**条目键**（字符串）—— **必须与 `CHARA_PARAM` 对应槽串逐字节相等**（见 §1） |
| 3 | `2` | `entry_value` | mixed | — | **值槽 0**（每行必给，随属性名解释，见 §0.1） |
| 4 | `3` | `entry_value_2` | mixed | — | **值槽 1**：`RESPAWN_TIME`=int(+196)｜`ENERGY`=u32(+188)｜`BOOST_SPEED`=float(+264)｜`JUMP`=float(+320) |
| 5 | `4` | `entry_value_3` | mixed | — | **值槽 2**：`RESPAWN_TIME`=int(+200)｜`BOOST_SPEED`=u32(+268)｜`JUMP`=float(+324) |
| 6 | `5` | `entry_value_4` | mixed | — | **值槽 3**：`RESPAWN_TIME`=int(+204)｜`BOOST_SPEED`=float(+272)｜`JUMP`=float(+328) |
| 7 | `6` | `entry_value_5` | mixed | — | **值槽 4**：`RESPAWN_TIME`=int(+208)｜`BOOST_SPEED`=float(+276)｜`JUMP`=u32(+332) |
| 8 | `7` | `entry_value_6` | mixed | — | **值槽 5**：`RESPAWN_TIME`=int(+212)｜`BOOST_SPEED`=u32(+280)｜`JUMP`=float(+336) |
| 9 | `8` | `entry_value_7` | mixed | — | **值槽 6**：`RESPAWN_TIME`=int(+216)｜`BOOST_SPEED`=u32(+284，注入时取负)｜`JUMP`=u32(+340) |
| 10 | `9` | `entry_value_8` | mixed | — | **值槽 7**：`RESPAWN_TIME`=int(+220)｜`BOOST_SPEED`=float(+288)｜`JUMP`=u32(+344) |
| 11 | `10` | `entry_value_9` | mixed | — | **值槽 8**：`RESPAWN_TIME`=int(+224)｜`BOOST_SPEED`=float(+292)｜`JUMP`=u32(+348，注入时取负) |
| 12 | `11` | `entry_value_10` | mixed | — | **值槽 9**：`RESPAWN_TIME`=int(+228)｜`BOOST_SPEED`=float(+296)｜`JUMP`=u32(+352) |
| 13 | `12` | `entry_value_11` | mixed | — | **值槽 10**：`RESPAWN_TIME`=int(+232)｜`BOOST_SPEED`=float(+300)｜`JUMP`=float（57BAA0子表+40，581690注入CHARA_PARAM+360；不是+356） |
| 14 | `13` | `entry_value_12` | mixed | — | **值槽 11**：`BOOST_SPEED`=float(+304)｜`JUMP`=bool(+364) |
| 15 | `14` | `entry_value_13` | mixed | — | **值槽 12**：`BOOST_SPEED`=u32(+308) |
| 16 | `15` | `entry_value_14` | mixed | — | **值槽 13**：`BOOST_SPEED`=float(+312)；其余属性不用 |

## 0. ★值槽模型（2026-10-05 行宽 3 → 16）

**旧注释错在哪**：`sub_A47BC0` 自己**只读 col0**，旧扫描就按"读到 3 列"记了 `列数 3`。
真正的值列由**子表对象**读：容器 vtable[1] 分派到子表 → 子表 `AddRow` **只读 col1（键）**
→ 子表 **`vtable[0]` 读值列**（列号随属性名而定）。

| 属性名（col0） | 值列阅读器 | 读到的列 | 最大 |
|---|---|---|---|
| `RESPAWN_TIME` | `sub_57B940`（循环 11 次） | `2..12` | 12 |
| `WARP_TIME` / `COST` / `MAX_HP` / `BOOST_GAUGEMAX` | `sub_57B970` / `sub_595AF0` | `2` | 2 |
| `ENERGY` | `sub_57B990` | `2,3` | 3 |
| `MOVE` | `sub_57B9C0`（负值钳 0） | `2` | 2 |
| `BOOST_GAUGEHEAL` / `SHOT` / `LOCKON` / `RELOAD` | `sub_595AF0` | `2` | 2 |
| **`BOOST_SPEED`** | `sub_57B9F0` | **`2..15`** | **15** ← 上限 |
| `JUMP` | `sub_57BAA0` | `2..13` | 13 |

⇒ 行宽必须 **16**（`csv0..csv15`），否则 BOOST_SPEED 的 13 个高位值槽被越界兜底吃成 0。

**为什么仿真跑不通（所以本表不含在 §2 偏窄清单里）**：子表是 `std::map` 对象，仿真里没有那两个 vtable
⇒ `call [vtable[0]]` 落到 `eip=0x2` ⇒ `UC_ERR_EXCEPTION`。**不是"读集未知"，是"仿真这条线结构上跑不通"**
⇒ `_sweep_verdict.py` 对本表改判 **`STATIC-OK`**（静态读集 `csv 0..15` 覆盖），`_sweep_width_db.py` 不再用
`emu_err` 一票否决本表的宽度判定。订正与验收细节见 `17-addendum-属性长表值槽.md`（附录 C）。

### 0.1 `entry_value`（值槽 0）随属性名的解释

| 属性名 | 值槽 0 落点 |
|---|---|
| `RESPAWN_TIME` | int `+192` |
| `WARP_TIME` | int `+236` ｜ `COST` int `+240` ｜ `MAX_HP` int `+164` ｜ `BOOST_GAUGEMAX` int `+168` |
| `BOOST_GAUGEHEAL` | float `+176` ｜ `MOVE` float `+180` |
| `ENERGY` | u32 `+184`（★客户端注入端硬钳 `min(x,99)`，见 §2.1） |
| `BOOST_SPEED` | float `+260`（面板"最高速度"倍率，见 §2.2） |
| `JUMP` | float `+316` |

## 1. ★键语义 + 13 张子表 + 消费方（2026-09-28 定案）

**行解析**（`sub_A47BC0` → 容器 vtable）：
- col0 = 属性名 → 容器 vtable[0]（`sub_57BD40`，词表 `off_D7A298`）得**子表编号 1..10**；
- 容器 vtable[1]（`sub_57BB70`）按编号分派到子表对象，调其 vtable[1]（AddRow）；
- AddRow（如 `sub_A5BE20`）**读 col1 为字符串键**（`sub_BBB4F0(idx=1)`）、col2 为值，`vtable[2](key, value)` 插入
  —— 子表是 `std::map<std::string, T>`。

**子表清单**（ctor `sub_A725F0` 的 RTTI 实名；槽列指 `CHARA_PARAM` 对应窄串列）：
| 编号 | 子表类（RTTI） | 词表名（col0 原样写） | CHARA_PARAM 槽 | 消费后写入机体行 |
|---|---|---|---|---|
| 1 | `MSMA_DETAIL_RESPAWN_DATA` | `RESPAWN_TIME` | col56 | +192 块 |
| 2 | `MSMA_DETAIL_WARPTIME_DATA` | `WARP_TIME` | col58 | +236 |
| 3 | `MSMA_DETAIL_COST_DATA` | `COST` | col60 | +240 |
| 4 | `MSMA_DETAIL_MAX_HP_DATA` | `MAX_HP` | col62 | +164（面板装甲） |
| 5 | `MSMA_DETAIL_ENERGY_DATA` | `ENERGY` | col64 | +184/+188 |
| 6 | `MSMA_DETAIL_MOVE_DATA` | `MOVE` | col67 | +180（面板最高速度） |
| 7 | `MSMA_DETAIL_BOOST_GAUGEMAX_DATA` | `BOOST_GAUGEMAX` | col69 | +168（面板喷射容量） |
| 8 | `MSMA_DETAIL_BOOST_GAUGEHEAL_DATA` | `BOOST_GAUGEHEAL` | col71 | +176（面板喷射蓄力） |
| 9 | `MSMA_DETAIL_BOOST_MOVE_DATA` | `BOOST_SPEED` | col73 | +260..+312 |
| 10 | `MSMA_DETAIL_JUMP_DATA` | `JUMP` | col79 | +316..+364 |
| 11 | `MSMA_DETAIL_SHOT_DATA` | *（词表外）* | — | — |
| 12 | `MSMA_DETAIL_LOCKON_DATA` | *（词表外）* | — | — |
| 13 | `MSMA_DETAIL_RELOAD_DATA` | *（词表外）* | — | — |

**消费方 `sub_581690`**：对每台机体，用 `CHARA_PARAM` 的 10 个槽串分别查上表 1..10 号子表，
命中就把值写进机体行（上表右列），未命中按 0。⇒ **两边键必须同一口径**：本仓统一用**練度ID 十进制串**
（`gen_msma_machine.py` 同时写本表 col1 与 `CHARA_PARAM` 槽）。子表 11..13 无槽 ⇒ 不由该链注入。

> 词表 `off_D7A298` 只到 `JUMP`（10 名）⇒ `SHOT`/`LOCKON`/`RELOAD` 三表**无法按名寻址**（疑为残留/未启用）。

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。

## 2. ★本仓填写现状（2026-09-28，9 属性 × 576 台 = 5184 行）

生成器 `datatables/gen_msma_machine.py`；`col1` 与 `CHARA_PARAM`/`MSMA_RENTAL` 的槽串同口径（練度ID 十进制串）。

| 属性 | 行数 | 值来源 | 备注 |
|---|---|---|---|
| `RESPAWN_TIME` | 576 | codex/日服 ① ② ③ 三层 | 再出击时间（秒） |
| `MAX_HP` | 576 | 同上 | 面板「装甲」 |
| `MOVE` | 576 | 同上 | 面板「最高速度」的基值 |
| `BOOST_GAUGEMAX` | 576 | 同上 | 面板「喷射容量」 |
| `BOOST_GAUGEHEAL` | 576 | 同上 | 面板「喷射蓄力」 |
| `COST` | 576 | 同上 | 编成 COST / 商城购买补值 |
| `WARP_TIME` | 576 | 同上 | 面板「紧急返回」 |
| `ENERGY` | 576 | ★**常量 1000** | 见 §2.1 |
| `BOOST_SPEED` | 576 | ★**常量 col2 = 0.84** | 见 §2.2 |
| `JUMP` | 0 | ✗ 无来源 | 见 §2.3 |

> 另外 122 台（名册里有、codex/日服都查不到的机体）**一行都没有** ⇒ 面板全 0 —— 已知缺口，另批处理。

### 2.1 `ENERGY` —— 必须发，值取 1000

- **行解析** `sub_57B990`：`col2 → 结构[+0]`（u32）、`col3 → 结构[+4]`（u32）。
- **注入** `sub_581690`：查不到 ⇒ `row+184 = 0 / +188 = 0`；
  查到 ⇒ **`row+184 = min(col2, 99)`**（★客户端硬钳 99）、`row+188 = col3`。
- ⇒ **缺这一行 ⇒ 能量上限 0 ⇒ 编成界面判「由于能量耗尽 因此无法出击」✗**（P250 实证，见 `07-模块与能量攻关.md`）。
- 本仓只写 `col2 = 1000`（`col3` 留空 = 0）：1000 与协议侧 `msmaEnergyFull` / `energy_now` 对齐，
  客户端自己钳到 99 ⇒ **1000 与 99 在客户端等价**；"单列 1000"也正是 P250 验证过能出击的形态。
  `col3`（写 `row+188`）语义未取证 ⇒ 按「不猜」留 0。

### 2.2 `BOOST_SPEED` —— 必须发，`col2 = 0.84`

- **行解析** `sub_57B9F0`：**14 列**（`col2..col15`）→ 结构 `[+0..+52]`，**float/u32 混排**：

```
+0,col2 f ｜ +4,col3 f ｜ +8,col4 u ｜ +12,col5 f  ｜ +16,col6 f  ｜ +20,col7 u
+24,col8 u ｜ +28,col9 f ｜ +32,col10 f ｜ +36,col11 f ｜ +40,col12 f ｜ +44,col13 f
+48,col14 u ｜ +52,col15 f
```

- **注入** `sub_581690`：把这 14 个搬到机体行 **`+260..+312`**（⚠️ **`+284 = -col8`**，注入时取负）。
- **面板「最高速度」**（`sub_61C9A0` idx=1，逐字反编译）：

```
v = MOVE(row+180) × max(row+260, row+276)              // ← 就是 col2 / col6
v = v × flt_D90A04(0.0005952381) × flt_D6C124(200.0) × flt_D6874C(10.0)
面板值 = trunc(v) + 1
```

- 三个常量之积 = **1.1904762**（已用 IDA 读实数核对）⇒ 要「面板显示 == MOVE」就必须
  **`max(col2, col6) = 1 / 1.1904762 = 0.8399999… ⇒ 取 0.84`**。
- 历史生成器只写 `col2 = 0.840000`，高位槽留空，足以解释面板投影，不能证明控制配置完整。2026-10-08实际发布仅1101011/1132252的col6已按已有col2做兼容实验；不可全量运行旧生成器覆盖。
- ⛔ 缺这一行 ⇒ `+260/+276` 全 0 ⇒ 面板「最高速度」**恒显示 1** ✗。
- ⛔ 绝不能再写 1900 这类「载重量/机动值」：面板会把它当倍率相乘 ⇒ 显示成 2777619 ✗（用户实测截图 ✓）。

### 2.3 `JUMP` —— 本批不发（无面板绑定、无来源）

- **行解析** `sub_57BAA0`：**12 列**（`col2..col13`）→ 结构 `[+0..+44]`：

```
+0,col2 f ｜ +4,col3 f ｜ +8,col4 f ｜ +12,col5 f ｜ +16,col6 u ｜ +20,col7 f
+24,col8 u ｜ +28,col9 u ｜ +32,col10 u ｜ +36,col11 u ｜ +40,col12 f ｜ +44,col13 bool
```

- **注入** `sub_581690` → 机体行 **`+316..+364`**（⚠️ **`+348 = -col10`**、`+364` 是 `col13` 的布尔）。
- 它**没有任何面板绑定**，codex/日服也没有这套值 ⇒ 按仓库「不猜」铁律留空。
  缺行 ⇒ 注入字段为0。这是缺失输入的既有行为，不代表上升/辅助控制能正常工作；+360与+364之间有布局差异，不能简单按连续浮点块解释。
- 语义取证后另批补：列布局已写全，届时只需往 `gen_msma_machine.py` 的 `CONST_DETAILS` 加一条。

### 2026-10-08：目标v15运行消费者与单项实验

57B9F0/581690解析及注入后，501B70普通初始速度乘BOOST_SPEED col2；501D90读col3计时。503300/503060→502D70→502840→502470分别进入初始、过渡和持续阶段；过渡计时为col5，普通持续速度直接乘col6。4ED410的零时长在正delta下立即结束，不能称为永久等待。方向倍率501F90另用col9/10，当前空值仍是独立缺项。

BOOST_SPEED col8经581690取负进入+284，502470在相关空中分支通过虚表+636=4EC230写own+2616，属于请求向量的Y输入，不是直接写物理速度。col14/+308是580410要求为正的整数，也是501CE0→502290的资源计数输入；不能将它当成向上速度填写。col12/13另参与闪避推进1608的资格、速度和阶段时间；旧“Space资格”名称误把注册时相邻push当成当前配置名的编号，已由45E620完整函数纠正。

JUMP关联由CHARA_PARAM col79精确寻址。503670/503190辅助槽0初始Y输入为signed col8×float col4，col5是初始阶段时间、col7是过渡时间，col2控制槽0的一项寿命；502760辅助槽1使用取负col10。此前编队四台col79都空。新取证45E620注册jump=1602，4EA100→4E2770→4ED4B0→4FEDA0/4FFC20→5037B0槽0建立普通起跳链，当前保存配置Space绑定jump；完整现场输入未捕获。当前两台已关联R001_JUMP_V1_1101011/1132252实验定义，其余两台仍空。

前一轮只对1101011、1132252的BOOST_SPEED col6从空改为现有col2的0.840000，面板max(col2,col6)不变。这是可回滚控制兼容实验，非原服逐机体持续倍率；当轮未填阶段时间、JUMP或方向倍率。原始汇编42函数及11项隔离指令验证见serverv/tmp/r001-boost-stages-code-20261008.json、r001-boost-stages-instructions-20261008.json。最新用户确认此次冲刺可随鼠标转向，仅场景观察部分验收。后续新增两条JUMP实验定义，短起跳/下落仍待客户端验收；详见serverv/docs/R001-战斗启动数据契约.md第四轮，旧生成器不得全量覆盖。
