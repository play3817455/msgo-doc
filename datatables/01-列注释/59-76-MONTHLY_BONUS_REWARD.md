# MONTHLY_BONUS_REWARD ｜ `reward/monthly_bonus_reward.csv`

- **用途**：月度登录奖励：按年月+日序+渠道发放 GP/物品
- 表ID `76` ｜ 下载序 `59` ｜ 类名 `CMonthlyBonusRewardTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_57B0A0` ｜ **列数 8**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `reward_id` | u32 | — | 月度奖励 ID（主键） |
| 2 | `1` | `year_month` | u16 | +4 | 年月编码（u16 col1 → +4；YYYYMM 或序数） |
| 3 | `2` | `login_channel` | enum | +8 | 登录渠道（enum col2 比较链：LOGIN=0 / XWAR=1 / 其它=-1 → +8） |
| 4 | `3` | `day_of_month` | u16 | +12 | 月份内日序（u16 col3 → +12；第几天登录领取） |
| 5 | `4` | `reward_type` | enum `sub_5703A0` | +16 | 奖励物类型（enum col4 sub_5703A0：GP=999/ITEM=0/MSMA=1/BUILDUP_MSMA=998 → +16） |
| 6 | `5` | `reward_param_id` | u32 | +20 | 奖励物 ID（u32 col5） |
| 7 | `6` | `reward_quantity` | u32 | +24 | 奖励数量（u32 col6） |
| 8 | `7` | `bonus_flag` | u32 | +28 | 附加标志（u32 col7） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
