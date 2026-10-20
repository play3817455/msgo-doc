# MODULE_BONUS_LOT ｜ `module/module_bonus_lot.csv`

- **用途**：模块加成抽取
- 表ID `70` ｜ 下载序 `53` ｜ 类名 `CModuleBonusLotTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5A26F0` ｜ **列数 8**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `lot_key` | str | — | 抽取键（str col0；如 ASSAULT_A×RANK1 组合键，原样存储） |
| 2 | `1` | `lot_category` | enum `sub_5804F0` | — | 战斗角色类别（str enum col1；sub_5804F0 词表：ASSAULT_A/SNIPE/CANNON/SUPPORT 等） |
| 3 | `2` | `weight` | u32 | — | 抽取权重（u32 col2） |
| 4 | `5` | `bonus_group_id` | u32 | — | 目标 MODULE_BONUS.bonus_group（u32 col5） |
| 5 | `6` | `reward_type` | str | — | 奖励类型（str col6；原样字符串，读表无独立转换函数） |
| 6 | `7` | `reward_param_a` | u32 | — | 奖励参数 A（u32 col7） |
| 7 | `8` | `reward_param_b` | u32 | — | 奖励参数 B（u32 col8） |
| 8 | `9` | `reward_param_c` | u32 | — | 奖励参数 C（u32 col9） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `3`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `4`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
