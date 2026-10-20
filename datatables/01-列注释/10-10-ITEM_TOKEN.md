# ITEM_TOKEN ｜ `item/token_item.csv`

- **用途**：代币/票券类物品
- 表ID `10` ｜ 下载序 `10` ｜ 类名 `CTokenItemTable`
- 逐列读取函数 `sub_595960` ｜ **列数 4**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `token_item_id` | u32 | +0 | 主键；代币物品 ID |
| 2 | `2` | `token_type` | enum `sub_595870` | +4 | 代币类型：MSMA_STORAGE/MSMA_DECKCOST（sub_595870 @+4） |
| 3 | `3` | `token_value` | u32 | +8 | 代币面值/数量（u32 @+8） |
| 4 | `4` | `expire_rule` | u32 | +12 | 过期规则 ID（u32 @+12；0=不过期） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
