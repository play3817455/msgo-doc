# COMBAT_OPERATION ｜ `command/combat_operation.csv`

- **用途**：战术/作战指令
- 表ID `30` ｜ 下载序 `30` ｜ 类名 `CCombatOperationTable`
- 逐列读取函数 `sub_572560` ｜ **列数 7**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `operation_id` | u32 | +0 | 主键；战术指令 ID（ATTACK/DEFENSE/MOVE/SPECIAL 族） |
| 2 | `7` | `title_text` | str | +4 | 指令标题（wstring @+4；UI 显示名） |
| 3 | `8` | `cast_time_sec` | float | +32 | 发动耗时秒（float @+32；sub_BBB470 col8） |
| 4 | `9` | `target_filter` | u32 | +36 | 目标筛选 ID（u32 @+36；battle-combat_operation_target_change） |
| 5 | `10` | `description` | str | +40 | 指令说明（wstring @+40） |
| 6 | `11` | `effect_duration_sec` | float | +68 | 效果持续秒（float @+68；sub_BBB470 col11） |
| 7 | `12` | `container_collect_id` | u32 | +72 | 容器收集 ID（u32 @+72；SC-0x6295 关联） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
