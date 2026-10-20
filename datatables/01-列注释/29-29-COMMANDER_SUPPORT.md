# COMMANDER_SUPPORT ｜ `command/commander_support.csv`

- **用途**：指挥官支援（支援技能）
- 表ID `29` ｜ 下载序 `29` ｜ 类名 `CCommanderSupportTable`
- 逐列读取函数 `sub_574300` ｜ **列数 6**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `3` | `use_cost` | u16 | +292 | 发动消耗（u16 @+292；csv3） |
| 2 | `4` | `cooldown_sec` | u16 | +294 | 冷却时间秒（u16 @+294；csv4） |
| 3 | `7` | `effect_param_a` | u32 | +324 | 效果参数 A（u32 @+324；csv7） |
| 4 | `8` | `linked_commander_id` | u32 | +332 | 关联指挥官 ID（u32 @+332→查 COMMANDER_NPC 名称 @+296） |
| 5 | `11` | `effect_param_b` | u32 | +328 | 效果参数 B（u32 @+328；csv11） |
| 6 | `12` | `effect_radius` | float | +340 | 效果半径（float @+340 = csv12 × flt_D69A58） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
