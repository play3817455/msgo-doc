# MSMA_PLAN ｜ `item/msma_plan.csv`

- **用途**：机体图纸（开发计划；材料槽 qty/item_id 对；sub_5944D0 查 ITEM）
- 表ID `22` ｜ 下载序 `22` ｜ 类名 `CMsmaPlanTable` ｜ 逐列读取 `sub_594E20`
- 列数 32 ｜ 确证 32 ｜ 部分 0 ｜ gap 0

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `plan_id` | u32 | +0 | 图纸 ID（主键；col0→a3[0]；sub_594E20 @0x594e39） |
| 2 | `2` | `plan_group_key` | u32 | +20 | 图纸分组键（col2→a3[5]；sub_594D40 插入索引向量 @0x594e4a） |
| 3 | `5` | `plan_sort_order` | u32 | +4 | 图纸排序/列表序（col5→a3[1]；sub_594E20 @0x594e9d） |
| 4 | `7` | `plan_header_a` | u32 | +8 | 图纸头参数 A（col7→a3[2] @+8；sub_594E20 @0x594ebd） |
| 5 | `9` | `plan_header_b` | u32 | +12 | 图纸头参数 B（col9→a3[3] @+12；sub_594E20 @0x594ec8） |
| 6 | `11` | `plan_header_c` | u32 | +16 | 图纸头参数 C（col11→a3[4] @+16；sub_594E20 @0x594ed3） |
| 7 | `13` | `output_item_id` | u32 | +56 | 产出物品 ID（col13→a3[14] @+56；sub_5944D0 查 ITEM @0x594ed6） |
| 8 | `15` | `slot_0_qty` | u32 | +60 | 材料槽 0 数量（col15→+60；sub_594E20） |
| 9 | `16` | `slot_0_item_id` | u32 | +92 | 材料槽 0 物品ID（col16→+92；sub_5944D0 查 ITEM） |
| 10 | `18` | `slot_1_qty` | u32 | +96 | 材料槽 1 数量（col18→+96；sub_594E20） |
| 11 | `19` | `slot_1_item_id` | u32 | +128 | 材料槽 1 物品ID（col19→+128；sub_5944D0 查 ITEM） |
| 12 | `21` | `slot_2_qty` | u32 | +132 | 材料槽 2 数量（col21→+132；sub_594E20） |
| 13 | `22` | `slot_2_item_id` | u32 | +172 | 材料槽 2 物品ID（col22→+172；sub_5944D0 查 ITEM） |
| 14 | `24` | `slot_3_qty` | u32 | +168 | 材料槽 3 数量（col24→+168；sub_594E20） |
| 15 | `25` | `slot_3_item_id` | u32 | +208 | 材料槽 3 物品ID（col25→+208；sub_5944D0 查 ITEM） |
| 16 | `27` | `slot_4_qty` | u32 | +204 | 材料槽 4 数量（col27→+204；sub_594E20） |
| 17 | `28` | `slot_4_item_id` | u32 | +244 | 材料槽 4 物品ID（col28→+244；sub_5944D0 查 ITEM） |
| 18 | `30` | `slot_5_qty` | u32 | +240 | 材料槽 5 数量（col30→+240；sub_594E20） |
| 19 | `31` | `slot_5_item_id` | u32 | +280 | 材料槽 5 物品ID（col31→+280；sub_5944D0 查 ITEM） |
| 20 | `33` | `slot_6_qty` | u32 | +276 | 材料槽 6 数量（col33→+276；sub_594E20） |
| 21 | `34` | `slot_6_item_id` | u32 | +316 | 材料槽 6 物品ID（col34→+316；sub_5944D0 查 ITEM） |
| 22 | `36` | `slot_7_qty` | u32 | +312 | 材料槽 7 数量（col36→+312；sub_594E20） |
| 23 | `37` | `slot_7_item_id` | u32 | +352 | 材料槽 7 物品ID（col37→+352；sub_5944D0 查 ITEM） |
| 24 | `39` | `slot_8_qty` | u32 | +348 | 材料槽 8 数量（col39→+348；sub_594E20） |
| 25 | `40` | `slot_8_item_id` | u32 | +388 | 材料槽 8 物品ID（col40→+388；sub_5944D0 查 ITEM） |
| 26 | `42` | `slot_9_qty` | u32 | +384 | 材料槽 9 数量（col42→+384；sub_594E20） |
| 27 | `43` | `slot_9_item_id` | u32 | +424 | 材料槽 9 物品ID（col43→+424；sub_5944D0 查 ITEM） |
| 28 | `45` | `slot_10_qty` | u32 | +420 | 材料槽 10 数量（col45→+420；sub_594E20） |
| 29 | `46` | `slot_10_item_id` | u32 | +460 | 材料槽 10 物品ID（col46→+460；sub_5944D0 查 ITEM） |
| 30 | `48` | `slot_11_qty` | u32 | +456 | 材料槽 11 数量（col48→+456；sub_594E20） |
| 31 | `49` | `slot_11_item_id` | u32 | +496 | 材料槽 11 物品ID（col49→+496；sub_5944D0 查 ITEM） |
| 32 | `51` | `plan_footer_param` | u32 | +492 | 图纸尾参数（col51→a3[123] @+492；sub_594E20 @0x5951b5） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大有效列号。
