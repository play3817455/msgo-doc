# SCORE_CONFIG_CATEGORY ｜ `mission/score_config_category.csv`

- **用途**：任务计分分类：将 score_config 计分项按类别分组
- 表ID `69` ｜ 下载序 `77` ｜ 类名 `CScoreConfigCategoryTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_58DDB0` ｜ **列数 2**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `category_name` | str | — | 计分分类名称（wstring col0；任务计分项归类标签） |
| 2 | `1` | `category_index` | enum `sub_5812E0` | — | 计分分类索引（enum col1 sub_5812E0 查 score_config 行 → 返回 +40 索引） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
