# PLAYER_NAVI ｜ `player_navi/player_navi.csv`

- **用途**：新手引导（Navi）步骤链：UI 锚点 + 触发条件 + 链式 next_id
- 表ID `63` ｜ 下载序 `71` ｜ 类名 `CPlayerNaviTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_58C7C0` ｜ **列数 16**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `navi_id` | u32 | +0 | 引导步骤 ID（主键；对应 0xF0C4 player_navi_get_list） |
| 2 | `1` | `step_title` | str | +4 | 引导步骤标题（wstring col1） |
| 3 | `2` | `step_body` | str | +32 | 引导正文（wstring col2） |
| 4 | `3` | `trigger_condition` | bool | +60 | 触发条件标志（bool col3>0 → +60） |
| 5 | `4` | `ui_target` | str | +64 | UI 锚点/目标控件名（wstring col4） |
| 6 | `5` | `show_when_not_first` | bool | +92 | 非首次显示标志（bool col5!=1 → +92） |
| 7 | `6` | `repeat_flag` | u32 | +96 | 可重复显示标志（u32 col6） |
| 8 | `7` | `next_navi_id` | u32 | +100 | 下一步引导 ID（u32 col7；链式教程） |
| 9 | `8` | `screen_id` | u32 | +104 | 触发界面 ID（u32 col8） |
| 10 | `9` | `min_level` | bool | +108 | 最低机师等级门槛启用（bool col9>0 → +108） |
| 11 | `10` | `max_level` | u32 | +112 | 最高机师等级（u32 col10；0=不限） |
| 12 | `11` | `mission_id` | u32 | +116 | 关联任务 ID（u32 col11） |
| 13 | `13` | `dialog_style` | u32 | +120 | 对话框样式（u32 col13 → +120；读表跳过 col12） |
| 14 | `14` | `voice_id` | u32 | +124 | 语音 ID（u32 col14 → +124） |
| 15 | `15` | `image_id` | u32 | +128 | 插图资源 ID（u32 col15 → +128） |
| 16 | `16` | `skip_allowed` | u32 | +132 | 允许跳过标志（u32 col16 → +132；16 列 CSV 可省略） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `12`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
