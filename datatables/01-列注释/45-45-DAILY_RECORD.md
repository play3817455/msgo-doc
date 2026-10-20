# DAILY_RECORD ｜ `pilot/daily_record.csv`

- **用途**：机师每日战绩统计定义：46 项战斗统计 + 铜/银/金绶带阈值（与 badge_config 同源）
- 表ID `45` ｜ 下载序 `45` ｜ 类名 `CDailyRecordTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_575840` ｜ **列数 13**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `record_id` | u32 | +0 | 战绩统计行 ID（主键；与 badge_config リボンID 一一对应） |
| 2 | `1` | `display_group` | u8 | +4 | UI 显示分组/排序（u8 col1） |
| 3 | `4` | `stat_type` | enum `sub_592DB0` | +8 | 战绩统计项（enum sub_592DB0，46 项：VERSUS/WIN/KILL/SCORE_* 等；与客户端「战斗记录」页签及 badge_config リボンタイプ 同源） |
| 4 | `5` | `unit_type` | u32 | +12 | 统计单位类型/辅助参数（u32 col5 → +12；badge_config「单位」列同源） |
| 5 | `8` | `display_order` | u32 | +16 | 列表排序权重（u32 col8） |
| 6 | `10` | `badge_tier_ref` | enum `sub_587540` | +20 | 绶带等级参照（enum col10 sub_587540：BRONZE/SILVER/GOLD） |
| 7 | `11` | `bronze_threshold` | u32 | +24 | 铜绶带获得条件值（u32 col11 ↔ badge_config 銅リボン） |
| 8 | `12` | `silver_threshold` | u32 | +28 | 银绶带获得条件值（u32 col12 ↔ badge_config 銀リボン） |
| 9 | `14` | `bronze_icon_id` | u32 | +32 | 铜绶带图标 ID（u32 col14 ↔ badge_config 銅アイコン） |
| 10 | `15` | `silver_icon_id` | u32 | +36 | 银绶带图标 ID（u32 col15） |
| 11 | `17` | `gold_icon_id` | u32 | +40 | 金绶带图标 ID（u32 col17） |
| 12 | `18` | `stat_title` | str | +44 | 统计项显示标题（wstring col18） |
| 13 | `19` | `stat_description` | str | +72 | 统计项说明（wstring col19；badge_config 説明文同源） |

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
