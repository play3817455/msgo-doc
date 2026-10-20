# SEASON_CLASS_IMFORMATION ｜ `season_class/season_class_information.csv`

- **用途**：赛季阶级信息
- 表ID `67` ｜ 下载序 `73` ｜ 类名 `CSeasonClassInformationTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5900A0` ｜ **列数 12**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `class_id` | u32 | — | 赛季阶级 ID（主键） |
| 2 | `1` | `class_name` | str | — | 阶级名称（wstring col1 sub_402310 → +4） |
| 3 | `2` | `rank_min` | u16 | +32 | 适用排名下限（u16 col2 → +32） |
| 4 | `3` | `rank_max` | u16 | +34 | 适用排名上限（u16 col3 → +34） |
| 5 | `4` | `point_threshold` | u16 | +36 | 阶级点数阈值（u16 col4 → +36） |
| 6 | `5` | `promotion_wins` | u16 | +38 | 升阶所需胜场（u16 col5 → +38） |
| 7 | `6` | `demotion_losses` | u16 | +40 | 降阶败场阈值（u16 col6 → +40） |
| 8 | `7` | `season_bonus` | u16 | +44 | 赛季加成系数（u16 col7 → +44） |
| 9 | `8` | `icon_id` | u16 | +46 | 阶级图标 ID（u16 col8 → +46） |
| 10 | `9` | `display_color` | u16 | +48 | UI 显示颜色（u16 col9 → +48） |
| 11 | `10` | `tier_min` | u16 | +50 | 阶级段下限（u16 col10） |
| 12 | `11` | `tier_max` | u16 | +52 | 阶级段上限（u16 col11） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
