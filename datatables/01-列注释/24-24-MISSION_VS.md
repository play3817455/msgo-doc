# MISSION_VS ｜ `mission/mission_vs.csv`

- **用途**：对战任务定义
- 表ID `24` ｜ 下载序 `24` ｜ 类名 `CMissionVsTable`
- 逐列读取函数 `sub_59FEE0` ｜ **CSV列位 75；当前 schema 建模34列，41列为有意留空/跳过**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `mission_id` | u32 | +4 | 主键；对战任务 ID（= AI 脚本 8 位 id，sub_629120 查表） |
| 2 | `1` | `map_id` | u32 | +8 | 地图 ID（u32 @+8） |
| 3 | `2` | `mode_param` | u32 | +40 | 模式参数 u32（@+40） |
| 4 | `3` | `mission_name` | str | +12 | 任务名称（wstring @+12） |
| 5 | `4` | `description` | str | +92 | 任务说明（wstring @+92） |
| 6 | `5` | `rule_param` | u32 | +44 | 规则参数 u32（@+44） |
| 7 | `13` | `flag_ranked` | bool | +56 | 地图环境地面标记：地图信息窗口 Ground on/off（bool bit0 @+56；旧物理名 flag_ranked 待迁移） |
| 8 | `14` | `flag_private` | bool | +56 | 地图环境水中标记：地图信息窗口 Underwater on/off（bool bit1 @+56；旧物理名 flag_private 待迁移） |
| 9 | `15` | `flag_clan` | bool | +56 | 地图环境宇宙标记：地图信息窗口 Space on/off（bool bit2 @+56；旧物理名 flag_clan 待迁移） |
| 10 | `16` | `vs_mode` | enum `sub_59FA70` | +48 | 对战模式（sub_59FA70 @+48：TD/DOM/CORE…） |
| 11 | `17` | `vs_submode` | enum `sub_59FB20` | +52 | 子模式（sub_59FB20 @+52：RPOST_DIFF/DOT_DMG…） |
| 12 | `18` | `faction` | enum `sub_40CE20` | +88 | 势力：EFF/ZEON（sub_40CE20 @+88） |
| 13 | `23` | `flag_spectate` | bool | +80 | 允许观战（bool @+80） |
| 14 | `26` | `flag_custom` | bool | +81 | 自定义房间（bool @+81） |
| 15 | `27` | `flag_event` | bool | +82 | 活动房（bool @+82） |
| 16 | `28` | `flag_tournament` | bool | +83 | 锦标赛（bool @+83） |
| 17 | `31` | `score_param_a` | u32 | +156 | 计分参数 A（u32 @+156） |
| 18 | `32` | `score_param_b` | u32 | +152 | 计分参数 B（u32 @+152） |
| 19 | `33` | `score_param_c` | u32 | +148 | 计分参数 C（u32 @+148） |
| 20 | `34` | `score_param_d` | u32 | +144 | 计分参数 D（u32 @+144） |
| 21 | `35` | `score_param_e` | u32 | +140 | 计分参数 E（u32 @+140） |
| 22 | `38` | `min_rank` | u16 | +58 | 最低等级（u16 @+58） |
| 23 | `39` | `max_rank` | u16 | +60 | 最高等级（u16 @+60） |
| 24 | `40` | `time_limit_sec` | u32 | +68 | 时间限制秒（u32 @+68） |
| 25 | `41` | `respawn_limit` | u16 | +72 | 重生上限（u16 @+72） |
| 26 | `44` | `team_size` | u16 | +128 | 队伍人数（u16 @+128） |
| 27 | `55` | `reward_gp` | u32 | +160 | GP 奖励基数（u32 @+160） |
| 28 | `56` | `reward_exp` | u32 | +164 | 经验奖励基数（u32 @+164） |
| 29 | `57` | `recommended_ms_cost` | u16 | +120 | 推荐机体 cost（u16 @+120） |
| 30 | `58` | `max_ms_cost` | u16 | +122 | 最大机体 cost（u16 @+122） |
| 31 | `59` | `banpick_rule_id` | u32 | +124 | BanPick 规则 ID（u32 @+124→MISSION_XWAR_BANPICK） |
| 32 | `60` | `sort_order` | u16 | +130 | 列表排序（u16 @+130） |
| 33 | `63` | `thumbnail_id` | u16 | +132 | 缩略图 ID（u16 @+132） |
| 34 | `74` | `script_flags` | u32 | +168 | 脚本标志 u32（@+168；30112300/30121320 时置 1） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 映射表只为34个已确认列命名；CSV列0..74 是客户端读取索引空间，不能因“34个已命名字段”而把第63/74列压缩到前34列。保留空位，避免错位 `thumbnail_id`、`script_flags` 等后段字段。
- 越界列 = 0；每个数据行至少 1 个单元格。
