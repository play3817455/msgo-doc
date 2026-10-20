# FORCEGAUGE_INFO ｜ `reward/forcegauge.csv`

- **用途**：战力槽（Force Gauge）定义：战斗内蓄力槽最大值/恢复/触发 Buff
- 表ID `62` ｜ 下载序 `70` ｜ 类名 `CForceGaugeTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_577560` ｜ **列数 14**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `gauge_id` | u32 | — | 战力槽 ID（主键；CForceGaugeTable） |
| 2 | `1` | `name_ref_id` | u32 | +4 | 战力槽名称引用 ID（u32 col1 → +4；UI 字符串索引） |
| 3 | `2` | `max_value` | u32 | +8 | 槽最大值（u32 col2 → +8） |
| 4 | `3` | `recover_rate` | u32 | +12 | 自然恢复速率（u32 col3 → +12） |
| 5 | `4` | `decay_rate` | u32 | +16 | 衰减速率（u32 col4 → +16） |
| 6 | `5` | `trigger_threshold` | u32 | +20 | 触发阈值（u32 col5 → +20） |
| 7 | `6` | `effect_id` | u32 | +24 | 关联效果 ID（u32 col6 → +24） |
| 8 | `7` | `display_order` | u32 | +28 | UI 排序（u32 col7 → +28） |
| 9 | `8` | `gauge_label` | str | +32 | 战力槽显示标签（wstring col8 → +32） |
| 10 | `9` | `icon_id` | u32 | +60 | 图标 ID（u32 col9 → +60） |
| 11 | `10` | `color_code` | u32 | +64 | UI 颜色编码（u32 col10 → +64） |
| 12 | `11` | `buff_id` | u32 | +68 | 满槽触发 Buff ID（u32 col11 → +68；→ BUFF） |
| 13 | `12` | `gauge_description` | str | +72 | 战力槽说明（wstring col12 → +72） |
| 14 | `13` | `extra_param` | u32 | +100 | 扩展参数（u32 col13 → +100） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
