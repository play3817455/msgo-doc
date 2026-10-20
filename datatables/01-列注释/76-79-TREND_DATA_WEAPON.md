# TREND_DATA_WEAPON ｜ `trend/trend_data_weapon.csv`

- **用途**：武器流行趋势数据：使用率/胜率/选取率统计（推荐配装参考）
- 表ID `79` ｜ 下载序 `76` ｜ 类名 `CTrendDataWeaponTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5928E0` ｜ **列数 11**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `weapon_trend_id` | u32 | — | 武器趋势行 ID（主键） |
| 2 | `1` | `weapon_id` | u32 | +4 | 武器 ID（→ WEAPON_SETTING）（u32 col1 → +4） |
| 3 | `2` | `usage_rate` | u32 | +8 | 使用率/流行度（百分比×100 或权重）（u32 col2 → +8） |
| 4 | `3` | `win_rate` | u32 | +12 | 胜率统计（u32 col3 → +12） |
| 5 | `4` | `pick_rate` | u32 | +16 | 选取率（u32 col4 → +16） |
| 6 | `5` | `trend_rank` | u32 | +20 | 趋势排名（u32 col5 → +20） |
| 7 | `6` | `msma_id` | u32 | +24 | 关联机体 ID（配装推荐机体）（u32 col6 → +24） |
| 8 | `7` | `period_id` | u32 | +28 | 统计周期 ID（u32 col7 → +28） |
| 9 | `8` | `sample_count` | u32 | +32 | 样本数量（u32 col8 → +32） |
| 10 | `9` | `recommend_score` | u32 | +36 | 推荐分数（u32 col9 → +36） |
| 11 | `10` | `display_flag` | u32 | +40 | 大厅显示标志（u32 col10 → +40） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
