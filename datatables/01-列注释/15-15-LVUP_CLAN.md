# LVUP_CLAN ｜ `growth/lvup_clan.csv`

- **用途**：部队（Clan）等级成长
- 表ID `15` ｜ 下载序 `15` ｜ 类名 `CLvupClanTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_579960` ｜ **列数 12**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `clan_level` | u8 | +8 | 部队等级（u8 col0 主键） |
| 2 | `1` | `member_cap` | u32 | +0 | 成员上限（u32 col1 → +0） |
| 3 | `3` | `mechanic_level` | enum `sub_578C50` | +24 | 部队机械师等级档（enum col3；MECHANIC_LV0..LV10） |
| 4 | `4` | `exp_base` | u32 | +12 | 升级经验基数（u32 col4 → +12） |
| 5 | `5` | `exp_increment` | u32 | +16 | 升级经验增量（u32 col5 → +16；与 col4 合成总需求） |
| 6 | `6` | `rokaku_level` | enum `sub_578EE0` | +28 | 着陆平台等级档（enum col6 sub_578EE0：ROKAKU_LV0..5 → +28） |
| 7 | `7` | `gp_bonus` | u32 | +32 | 部队 GP 加成（u32 col7 → +32） |
| 8 | `8` | `shop_level` | enum `sub_5790B0` | +36 | 部队商店等级（enum col8 sub_5790B0：SHOP_LV0..21 → +36） |
| 9 | `9` | `deck_cost_level` | enum `sub_579500` | +40 | 卡组 COST 上限档（enum col9 sub_579500：DECKCOST_LV0..5 → +40） |
| 10 | `10` | `bonus_gp` | u32 | +44 | 等级奖励 GP 数（u32 col10 → +44） |
| 11 | `11` | `discount_level` | enum `sub_5796D0` | +48 | 商店折扣档（enum col11 sub_5796D0：DISCOUNT_LV0..10 → +48） |
| 12 | `12` | `extra_param` | u32 | +52 | 扩展参数（u32 col12 → +52） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**本服填写现状（2026-09-24）**：等级 **1..50** 连续填实，生成器 `datatables/gen_lvup_clan.py`
（改曲线改脚本 → 重生成 → `cfgsync` 导库）。曲线 `need(L) = 10×L×(L+10)`，累计满级 **556,750**；
★ 占位口径、非客户端真值。`col3/col4/col5` 等档位列**留空 = 0**（未取证）。

**列填充盘点（2026-10-05 体检，`_probe_batch_n2.py`）**：13 列里**只有 2 列有值**：

| 有值 | col0 `clan_level`（1..50，50 个唯一值）、col1（`10×L×(L+10)`，50 个唯一值，公式命中 100%） |
|---|---|
| **全空 11 列** | col2 `reserved_u32_2`、col3 `mechanic_level`、col4 `exp_base`、col5 `exp_increment`、col6 `rokaku_level`、col7 `gp_bonus`、col8 `shop_level`、col9 `deck_cost_level`、col10 `bonus_gp`、col11 `discount_level`、col12 `extra_param` |

其中 **col3 / col6 / col8 / col9 / col11 是客户端枚举档位**（`sub_578C50`/`sub_578EE0`/`sub_5790B0`/
`sub_579500`/`sub_5796D0`）⇒ 全 0 = **恒最低档**（机制师等级、着陆平台、部队商店、卡组 COST、折扣）。
这是「结构合法但内容缺失」，不是崩溃点；要填实必须有档位来源，**不能猜**。

⚠️ **`member_cap` 是历史误名：它其实是「本级所需经验」**（`sub_579960` 读进 `+0`，
`sub_579B40` 逐级累加成累计需求；`sub_63D060` 用它算进度 `progress = row[+0] + exp − 累计`）。
真正的成员上限是本服常量 `store.ClanMemberCap`（= 50，客户端解码上限）。

**★ 客户端崩点（填表与发等级都必须守）**：`sub_63D060` 是
`sub_619C90(表 = dword_11EBA90, key = *(char *)(a2 + 47))`（@`0x63d08f`）查这一行的，
**查不到返回 0 后立刻 `*v4` 解引用**（@`0x63d130`）⇒
① 等级必须**连续覆盖**服务端会发出的每一级（本表从 1 起，没有 0 级那一行）；
② `clan_level` 客户端按**有符号 i8** 读 ⇒ **不得 > 127**。
两条已钉成门禁：`internal/store/clan_exp_test.go · TestClanLevelTableContentIsUsable`。

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
