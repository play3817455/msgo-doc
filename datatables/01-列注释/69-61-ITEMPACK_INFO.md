# ITEMPACK_INFO ｜ `item/item_pack.csv`

- **用途**：物品包内容
- 表ID `61` ｜ 下载序 `69` ｜ 类名 `CItempackTable`
- 逐列读取函数 `sub_5933C0` ｜ **列数 4**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `itempack_id` | u32 | +0 | 主键；物品包 ID |
| 2 | `1` | `pack_item_id` | u32 | +4 | 包内物品 ITEM.item_id（u32 @+4） |
| 3 | `2` | `quantity` | u32 | +8 | 数量（u32 @+8） |
| 4 | `3` | `drop_weight` | u32 | +12 | 掉落权重（u32 @+12；加权随机时） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
