# MISSION_GROUP ｜ `mission/mission_group.csv`

- **用途**：任务分组
- 表ID `26` ｜ 下载序 `26` ｜ 类名 `CMissionGroupTable`
- 逐列读取函数 `sub_59E8A0` ｜ **列数 4**

| 读序 | CSV# | 逻辑字段（数据库兼容列名） | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `group_id` | u32 | +0 | 主键；CMissionGroupTable 索引键（sub_59E830 按 group_id 查行） |
| 2 | `1` | `group_name` | str | +4 | 分组显示名（wstring @+4；任务列表 UI 归类标签） |
| 3 | `2` | `mission_id`（DB旧列名 `sort_order`） | u32 | +8 | 引用的任务ID；`sub_59E8A0` 用此值查 `MISSION_VS`，找到后置任务行 `+100=1`，再把任务ID加入当前组成员集合。 |
| 4 | `3` | `entry_name`（DB旧列名 `group_tag`） | str | +12 | 该组内单个任务项的副名/显示名；不是分组tag。 |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 数据库兼容列名仍为 `sort_order` / `group_tag`；它们的实际业务内容分别是任务ID和条目副名。不要据旧列名写入排序权重或分组tag。
- 越界列 = 0；每个数据行至少 1 个单元格。
