# MSMA_MATERIAL ｜ `本地表，不下发`

- **用途**：机体素材（本地表）
- 表ID `18` ｜ 下载序 `18` ｜ 类名 `CMsmaMaterialTable` ｜ disposition `LOCAL`
- 逐列读取函数 `sub_594320` ｜ **列数 8**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `material_id` | u32 | +0 | 素材类型ID（主键） |
| 2 | `2` | `material_type` | enum `sub_594230` | +4 | 素材类别（enum col2 sub_594230：ARMOR/GENERATOR/… → +4） |
| 3 | `3` | `base_rate` | float | +8 | 开发成功率 base_rate（float col3 → +8） |
| 4 | `4` | `tier2_rate` | float | +12 | 开发成功率 tier2_rate（float col4 → +12） |
| 5 | `5` | `tier3_rate` | float | +16 | 开发成功率 tier3_rate（float col5 → +16） |
| 6 | `6` | `tier4_rate` | float | +20 | 开发成功率 tier4_rate（float col6 → +20） |
| 7 | `7` | `tier5_rate` | float | +24 | 开发成功率 tier5_rate（float col7 → +24） |
| 8 | `8` | `tier6_rate` | float | +28 | 开发成功率 tier6_rate（float col8 → +28） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `1`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
