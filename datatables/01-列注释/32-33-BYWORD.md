# BYWORD ｜ `pilot/byword.csv`

- **用途**：称号（byword）
- 表ID `33` ｜ 下载序 `32` ｜ 类名 `CBywordTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_570FC0` ｜ **列数 7**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `byword_id` | u32 | — | 称号 ID（主键；机师记录 byword u16 字段引用） |
| 2 | `1` | `display_order` | u32 | — | 显示排序（u32 col1） |
| 3 | `2` | `prefix_text` | str | — | 称号前缀文本（wstring col2） |
| 4 | `3` | `suffix_text` | str | — | 称号后缀文本（wstring col3） |
| 5 | `4` | `title_text` | str | — | 称号主文本（wstring col4） |
| 6 | `5` | `description` | str | — | 称号说明（wstring col5） |
| 7 | `6` | `byword_type` | enum `sub_570E80` | — | 称号类型（enum col6 sub_570E80；决定显示槽位/颜色） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
