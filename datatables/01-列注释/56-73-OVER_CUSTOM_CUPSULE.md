# OVER_CUSTOM_CUPSULE ｜ `item/item_over_custom_point.csv`

- **用途**：超改胶囊
- 表ID `73` ｜ 下载序 `56` ｜ 类名 `CItemOverCustomPointTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_593250` ｜ **列数 3**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `item_id` | u32 | +0 | 超改点数胶囊物品 ID（主键；→ ITEM 表） |
| 2 | `1` | `point_value` | u32 | +4 | 使用后获得超改点数（col1 u32） |
| 3 | `3` | `bonus_rate` | u32 | +8 | 点数倍率/附加参数（u32 col3 → +8；跳过 col2 默认 0） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
