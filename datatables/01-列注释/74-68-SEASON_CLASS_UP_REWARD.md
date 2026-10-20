# SEASON_CLASS_UP_REWARD ｜ `season_class/season_class_up_reward.csv`

- **用途**：赛季阶级升级奖励
- 表ID `68` ｜ 下载序 `74` ｜ 类名 `CSeasonClassUpRewardTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_590ED0` ｜ **列数 10**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `class_id` | u32 | — | 赛季阶级 ID（主键；→ SEASON_CLASS_IMFORMATION） |
| 2 | `1` | `reward_param` | u32 | — | 奖励参数 A（u32 col1 → +4；ASM 直读 u32） |
| 3 | `2` | `reward_title` | str | — | 奖励标题（wstring col2 sub_402310 → +8） |
| 4 | `3` | `primary_reward_value` | u32 | +36 | 主奖励数值（u32 col3 → +36；GP 或物品 ID 依配置） |
| 5 | `4` | `reward_item_id` | u32 | +40 | 奖励物品 ID（u32 col4 → ITEM；首槽） |
| 6 | `5` | `reward_item_qty` | u32 | +44 | 奖励物品数量（u32 col5；首槽） |
| 7 | `6` | `reward_item_name` | str | — | 奖励物品名称（wstring col6；首槽说明） |
| 8 | `7` | `bonus_item_id` | u32 | +112 | 附加物品 ID（u32 col7；二槽） |
| 9 | `8` | `bonus_item_qty` | u32 | +116 | 附加物品数量（u32 col8；二槽） |
| 10 | `9` | `bonus_item_name` | str | — | 附加物品名称（wstring col9；二槽说明） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
