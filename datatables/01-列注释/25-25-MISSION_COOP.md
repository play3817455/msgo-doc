# MISSION_COOP ｜ `mission/mission_coop.csv`

- **用途**：协作战任务定义
- 表ID `25` ｜ 下载序 `25` ｜ 类名 `CMissionCoopTable`
- 逐列读取函数 `sub_59DC00` ｜ **列数 24**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `mission_id` | u32 | +4 | 主键；协作战任务 ID（与 AI 脚本 mission id 对应） |
| 2 | `1` | `map_id` | u32 | +8 | 地图 ID（u32 @+8；关联 map 资源） |
| 3 | `2` | `thumbnail_id` | u32 | +40 | 缩略图/图标 ID（u32 @+40） |
| 4 | `3` | `faction` | enum `sub_40CE20` | +80 | 势力限制：EFF/ZEON（sub_40CE20 @+80；空=不限） |
| 5 | `4` | `rule_param` | u32 | +84 | 规则参数 u32（@+84；col49=1 时强制写入 256） |
| 6 | `5` | `min_players` | u32 | +44 | 最少玩家数（u32 @+44） |
| 7 | `6` | `flag_ranked` | bool | +56 | 排位战标志（bool bit0 @+56） |
| 8 | `7` | `flag_private` | bool | +56 | 私人房间标志（bool bit1 @+56） |
| 9 | `9` | `coop_mode` | enum `sub_40CE20` | +48 | 协作模式：COOP_CORE_DESTROY/COOP_WAVE（enum @+48） |
| 10 | `10` | `coop_subtype` | enum `sub_40CE20` | +52 | 子模式：BASE_DEFENSE/TIME_ATTACK（enum @+52） |
| 11 | `11` | `script_bundle_id` | u32 | +200 | 脚本资源包 ID（u32 @+200；sub_744680 查关联） |
| 12 | `12` | `mission_name` | str | +88 | 任务名称（wstring @+88） |
| 13 | `13` | `recommended_rank` | u16 | +208 | 推荐等级/军衔（u16 @+208） |
| 14 | `14` | `min_rank` | u16 | +58 | 最低等级（u16 @+58） |
| 15 | `15` | `max_rank` | u16 | +60 | 最高等级（u16 @+60） |
| 16 | `16` | `time_limit_sec` | u32 | +68 | 时间限制秒（u32 @+68） |
| 17 | `19` | `respawn_limit` | u16 | +72 | 重生次数上限（u16 @+72） |
| 18 | `37` | `briefing_text` | str | +116 | 任务简报文本（wstring col37 @+116） |
| 19 | `38` | `objective_text` | str | +144 | 目标说明文本（wstring col38 @+144） |
| 20 | `39` | `result_text` | str | +172 | 结算说明文本（wstring col39 @+172） |
| 21 | `47` | `flag_tutorial` | bool | +204 | 教程任务标志（bool @+204） |
| 22 | `48` | `flag_event` | bool | +205 | 活动任务标志（bool @+205） |
| 23 | `49` | `flag_force_rule256` | bool | +206 | 强制规则 256 标志（bool @+206→col4=256） |
| 24 | `52` | `flag_allow_spectate` | bool | +210 | 允许观战标志（bool @+210；需 col47=1） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
