# NETCAFE_CHALLENGE ｜ `pilot/netcafe_challenge.csv`

- **用途**：网吧挑战：网吧登录用户的专属战绩挑战
- 表ID `48` ｜ 下载序 `48` ｜ 类名 `CNetcafeChallengeTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5875E0` ｜ **列数 13**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `challenge_id` | u32 | +0 | 网吧挑战 ID（主键） |
| 2 | `1` | `display_group` | u8 | +4 | UI 显示分组（u8 col1） |
| 3 | `4` | `stat_type` | enum `sub_5874A0` | +8 | 网吧挑战统计项（enum sub_5874A0，46 项 + NETCAFE；与 DAILY_RECORD 同一套战绩体系） |
| 4 | `5` | `target_value` | u32 | +12 | 网吧累计目标值（u32 col5 → +12） |
| 5 | `8` | `display_order` | u32 | +16 | 列表排序权重（u32 col8 → +16） |
| 6 | `10` | `badge_tier_ref` | enum `sub_587540` | +20 | 绶带等级参照（enum col10 sub_587540：BRONZE/SILVER/GOLD） |
| 7 | `11` | `reward_gp` | u32 | +24 | 达成奖励 GP（u32 col11 → +24） |
| 8 | `12` | `reward_item_id` | u32 | +28 | 达成奖励物品 ID（u32 col12 → +28） |
| 9 | `14` | `reward_qty` | u32 | +32 | 奖励物品数量（u32 col14 → +32） |
| 10 | `15` | `bonus_point` | u32 | +36 | 附加点数/积分（u32 col15 → +36） |
| 11 | `17` | `bonus_param` | u32 | +40 | 附加奖励参数（u32 col17 → +40） |
| 12 | `18` | `challenge_title` | str | +44 | 挑战标题（wstring col18 → +44） |
| 13 | `19` | `challenge_desc` | str | +72 | 挑战说明（wstring col19 → +72） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `3`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `6`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `7`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `9`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `13`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `16`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
