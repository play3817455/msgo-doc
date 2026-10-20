# GACHA ｜ `gacha/gacha.csv`

- **用途**：扭蛋（抽卡）奖池
- 表ID `32` ｜ 下载序 `31` ｜ 类名 `CGachaTable`
- 逐列读取函数 `sub_578220` ｜ **列数 34**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `gacha_id` | u32 | — | 主键；扭蛋池 ID |
| 2 | `1` | `display_order` | u32 | — | UI 排序（u32 @+4） |
| 3 | `2` | `gacha_name` | str | — | 扭蛋池名称（wstring @+8） |
| 4 | `3` | `description` | str | — | 扭蛋池说明（wstring @+36） |
| 5 | `4` | `currency_type` | enum `sub_578090` | — | 消耗货币：GP/CP/CP_EX/CN_LOCAL…（sub_578090 @+64） |
| 6 | `5` | `draw_mode` | enum `sub_578130` | — | 抽取模式：NORMAL/SINGLE/SINGLE_NORESET（sub_578130 @+68） |
| 7 | `6` | `flag_visible` | bool | — | 开关位 flag_visible（!=0⇒true） |
| 8 | `7` | `flag_limited` | bool | — | 开关位 flag_limited（!=0⇒true） |
| 9 | `8` | `flag_new` | bool | — | 开关位 flag_new（!=0⇒true） |
| 10 | `9` | `single_cost` | u32 | — | 单抽价格（u32 col9） |
| 11 | `10` | `ten_cost` | u32 | — | 十连价格（u32 col10） |
| 12 | `11` | `ticket_item_id` | u32 | — | 所需票券 ITEM ID（u32 col11） |
| 13 | `12` | `start_time` | u32 | — | 开始时间戳（u32 col12） |
| 14 | `13` | `end_time` | u32 | — | 结束时间戳（u32 col13） |
| 15 | `14` | `banner_id` | u32 | — | 横幅 ID（u32 col14） |
| 16 | `15` | `pity_counter` | u32 | — | 保底计数（u32 col15） |
| 17 | `16` | `pity_rare_id` | u32 | — | 保底稀有 ID（u32 col16） |
| 18 | `17` | `daily_limit` | u32 | — | 每日上限（u32 col17） |
| 19 | `18` | `total_limit` | u32 | — | 总次数上限（u32 col18） |
| 20 | `19` | `flag_recommend` | bool | — | 开关位 flag_recommend（!=0⇒true） |
| 21 | `20` | `flag_hidden` | bool | — | 开关位 flag_hidden（!=0⇒true） |
| 22 | `22` | `pool_group` | u32 | — | 池分组 ID（u32 col22） |
| 23 | `24` | `ui_layout_id` | u32 | — | UI 布局 ID（u32 col24） |
| 24 | `26` | `bonus_item_id` | u32 | — | 附赠物品 ID（u32 col26） |
| 25 | `30` | `rate_pair_30a` | u32 | — | 概率对 A（col30；与 col31 成对） |
| 26 | `31` | `rate_rarity_30b` | enum `sub_577FF0` | — | 稀有度/捆绑类型（col31；sub_577FF0：FREE_PLAY_BUNDLE 等） |
| 27 | `32` | `rate_pair_32a` | u32 | — | 概率对 A（col32；与 col33 成对） |
| 28 | `33` | `rate_rarity_32b` | enum `sub_577FF0` | — | 稀有度/捆绑类型（col33；sub_577FF0：FREE_PLAY_BUNDLE 等） |
| 29 | `34` | `rate_pair_34a` | u32 | — | 概率对 A（col34；与 col35 成对） |
| 30 | `35` | `rate_rarity_34b` | enum `sub_577FF0` | — | 稀有度/捆绑类型（col35；sub_577FF0：FREE_PLAY_BUNDLE 等） |
| 31 | `38` | `bundle_type` | enum `sub_577F50` | — | 捆绑类型（sub_577F50：PLAY_BUNDLE_BC_ONLY 等） |
| 32 | `39` | `season_id` | u32 | — | 赛季 ID（u32 col39） |
| 33 | `40` | `play_bundle_type` | enum `sub_577FF0` | — | 游玩捆绑类型（sub_577FF0 col40：FREE_PLAY_BUNDLE） |
| 34 | `41` | `related_gacha_id` | u32 | — | 关联池 ID（u32 col41） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
