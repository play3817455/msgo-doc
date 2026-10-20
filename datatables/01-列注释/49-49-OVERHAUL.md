# OVERHAUL ｜ `item/overhaul.csv`

- **用途**：大修 / 翻新
- 表ID `49` ｜ 下载序 `49` ｜ 类名 `COverHaulTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_587780` ｜ **列数 16**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `overhaul_id` | u32 | +0 | 大修方案 ID（主键；COverHaulTable） |
| 2 | `1` | `overhaul_name` | str | +4 | 大修方案名称（wstring col1） |
| 3 | `2` | `msma_id` | u32 | +32 | 目标机体 ID（u32 col2 → +32；→ CHARA_PARAM） |
| 4 | `3` | `rank_requirement` | u32 | +36 | 机体稀有度/等级需求（u32 col3 → +36） |
| 5 | `4` | `gp_cost` | u32 | +40 | GP 翻新费用（u32 col4 → +40） |
| 6 | `6` | `base_param` | u32 | +44 | 基础参数/成功率权重（u32 col6 → +44） |
| 7 | `7` | `material_id_1` | u32 | +48 | 素材 1 物品 ID（u32 col7 → +48） |
| 8 | `8` | `material_sub_id_1` | u32 | +52 | 素材 1 子类型/参数（u32 col8 → +52） |
| 9 | `9` | `material_name_1` | str | +76 | 素材 1 名称（wstring col9 → +76） |
| 10 | `10` | `material_qty_1` | u32 | +64 | 素材 1 数量（u32 col10 → +64） |
| 11 | `11` | `material_id_2` | u32 | +56 | 素材 2 物品 ID（u32 col11 → +56） |
| 12 | `12` | `material_name_2` | str | +104 | 素材 2 名称（wstring col12 → +104） |
| 13 | `13` | `material_qty_2` | u32 | +68 | 素材 2 数量（u32 col13 → +68） |
| 14 | `14` | `material_id_3` | u32 | +60 | 素材 3 物品 ID（u32 col14 → +60） |
| 15 | `15` | `material_name_3` | str | +132 | 素材 3 名称（wstring col15 → +132） |
| 16 | `16` | `material_qty_3` | u32 | +72 | 素材 3 数量（u32 col16 → +72） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `5`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
