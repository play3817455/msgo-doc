# SEASON_RANKERBATTLE_REWARD ｜ `reward/season_rankerbattle_reward.csv`

- **用途**：赛季排名战奖励
- 表ID `66` ｜ 下载序 `75` ｜ 类名 `CSeasonRankerBattleRewardTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5921A0` ｜ **列数 8**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `reward_id` | u32 | — | 排名战奖励 ID（主键） |
| 2 | `1` | `season_id` | u32 | +4 | 赛季 ID（u32 col1） |
| 3 | `2` | `rank_min` | u32 | +8 | 适用排名下限（u32 col2） |
| 4 | `3` | `rank_max` | u32 | +12 | 适用排名上限（u32 col3） |
| 5 | `4` | `reward_gp` | u32 | +16 | 排名奖励 GP（u32 col4） |
| 6 | `5` | `reward_item_name` | str | +20 | 排名奖励物品名（narrow str col5 → +20；sub_CC711A 32 字节） |
| 7 | `6` | `reward_item_qty` | u32 | +84 | 奖励物品数量（u32 col6） |
| 8 | `7` | `bonus_title_name` | str | +88 | 奖励称号名（narrow str col7 → +88；sub_CC711A 32 字节） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
