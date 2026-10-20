# MSMA_ADOP ｜ `item/advanced_option.csv`

- **用途**：机体采纳/领养（advanced option）
- 表ID `64` ｜ 下载序 `72` ｜ 类名 `CMsmaAdopTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_57B3D0` ｜ **列数 3**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `adop_id` | u16 | +0 | 高级选项ID（主键 u16；col0 → +0） |
| 2 | `1` | `msma_id` | u32 | +4 | 关联机体 ID（u32 col1 → +4） |
| 3 | `3` | `adop_param` | u32 | +8 | 高级选项参数（u32 col3 → +8） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
