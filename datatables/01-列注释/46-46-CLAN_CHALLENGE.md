# CLAN_CHALLENGE ｜ `clan/clan_challenge.csv`

- **用途**：部队（Clan）挑战：部队全员累计 46 项战绩达成目标后发放奖励
- 表ID `46` ｜ 下载序 `46` ｜ 类名 `CClanChallengeTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_571DA0` ｜ **列数 11**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `challenge_id` | u32 | +0 | 部队挑战 ID（主键） |
| 2 | `1` | `display_group` | u8 | +4 | UI 显示分组（u8 col1） |
| 3 | `4` | `stat_type` | enum `sub_571D00` | +8 | 部队挑战统计项（enum sub_571D00，46 项 + PERFECT；与 DAILY_RECORD 同一套战绩体系，换到部队维度） |
| 4 | `5` | `target_value` | u32 | +12 | 部队累计目标值（u32 col5 → +12） |
| 5 | `11` | `reward_gp` | u32 | +16 | 达成奖励 GP（u32 col11 → +16） |
| 6 | `12` | `reward_item_id` | u32 | +20 | 达成奖励物品 ID（u32 col12 → +20） |
| 7 | `14` | `reward_qty` | u32 | +24 | 奖励物品数量（u32 col14 → +24） |
| 8 | `15` | `bonus_point` | u32 | +28 | 附加点数/积分（u32 col15 → +28） |
| 9 | `17` | `bonus_param` | u32 | +32 | 附加奖励参数（u32 col17 → +32） |
| 10 | `18` | `challenge_title` | str | +36 | 挑战标题（wstring col18 → +36） |
| 11 | `19` | `challenge_desc` | str | +64 | 挑战说明（wstring col19 → +64） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `3`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `6`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `7`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `8`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `9`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `10`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `13`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `16`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
