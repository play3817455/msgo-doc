# ITEM_USE ｜ `item/use_item.csv`

- **用途**：消耗品使用效果
- 表ID `8` ｜ 下载序 `8` ｜ 类名 `CUseItemTable`
- 逐列读取函数 `sub_5959B0` ｜ **列数 3**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `use_item_id` | u32 | +0 | 主键；消耗品行 ID（= ITEM.linked_table_id） |
| 2 | `2` | `linked_item_id` | u32 | +32 | 关联 ITEM.item_id（u32 @+32） |
| 3 | `3` | `enabled_flag` | bool | +36 | 启用标志（u32 @+36；0=禁用该消耗品效果） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
