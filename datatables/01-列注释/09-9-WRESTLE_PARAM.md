# WRESTLE_PARAM ｜ `item/wrestle.csv`

- **用途**：格斗（近战）参数
- 表ID `9` ｜ 下载序 `9` ｜ 类名 `CAtkParamTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_56F5F0` ｜ **列数 31**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 0 | `0` | u32 | ★**格斗参数 ID** — 主键（sub_56F5F0 col0） |
| 4 | `4` | float | ★**打击伤害** — 基础打击伤害倍率（sub_56F5F0 col4 float） |
| 5 | `5` | u32 | ★**unknown_u32_5** — unknown_u32_5： sub_56F5F0 0x56f636 |
| 6 | `6` | u32 | ★**整型参数 col6** — 整型参数 col6（反转为 bool 存 +12） |
| 7 | `7` | enum | ★**命中类型**（`sub_56F4B0`）— NONE/HOMING/HACK_CHECK_EX（sub_56F4B0） |
| 8 | `8` | float | ★**攻击距离** — 有效攻击距离（sub_56F5F0 col8 float） |
| 9 | `9` | float | ★**判定宽度** — 命中判定宽度（sub_56F5F0 col9 float） |
| 10 | `10` | float | ★**判定高度** — 命中判定高度（sub_56F5F0 col10 float） |
| 11 | `11` | float | ★**起手时间** — 攻击起手秒数（sub_56F5F0 col11 float） |
| 12 | `12` | float | ★**生效时间** — 判定有效窗口（sub_56F5F0 col12 float） |
| 13 | `13` | float | ★**硬直时间** — 攻击后硬直（sub_56F5F0 col13 float） |
| 14 | `14` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 15 | `15` | float | ★**击退** — 击退力度（sub_56F5F0 col15 float） |
| 16 | `16` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 17 | `17` | enum | ★**攻击手**（`sub_56F3A0`）— L_HAND/R_HAND/ACTIVE_WEAPON（sub_56F3A0） |
| 18 | `18` | float | ★**连击缩放** — 连击段伤害缩放（sub_56F5F0 col18 float） |
| 19 | `19` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 20 | `20` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 21 | `21` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 22 | `22` | float | ★**盾伤** — 对盾伤害倍率（sub_56F5F0 col22 float） |
| 23 | `23` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 24 | `24` | bool | ★**开关位 col24** — 开关位 col24（!=0 ⇒ true） |
| 25 | `25` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 26 | `26` | float | ★**浮点参数** — 浮点参数（系数/倍率） |
| 27 | `27` | u32 | ★**unknown_u32_27** — unknown_u32_27： sub_56F5F0 0x56f7f4 |
| 29 | `29` | str | ★**枚举/类别 —— 写名称（见 `枚举表.md` `sub_402310`）** — 枚举/类别 —— 写名称（可选 0 个，见 `枚举表.md` `sub_402310`） |
| 30 | `30` | u32 | ★**unknown_u32_30** — unknown_u32_30： sub_56F5F0 0x56f890 |
| 32 | `32` | u32 | ★**unknown_u32_32** — unknown_u32_32： sub_56F5F0 0x56f89e |
| 35 | `35` | bool | ★**开关位 col35** — 开关位 col35（!=0 ⇒ true） |
| 36 | `36` | bool | ★**开关位 col36** — 开关位 col36（!=0 ⇒ true） |
| 37 | `37` | float | ★**眩晕值** — 眩晕/Down 累积（sub_56F5F0 col37 float） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
