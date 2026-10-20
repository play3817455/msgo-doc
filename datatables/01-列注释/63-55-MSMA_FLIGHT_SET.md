# MSMA_FLIGHT_SET ｜ `msma/msma_flight_settings.csv`

- **用途**：机体飞行/浮游/推进/浮游炮物理参数（按 msma_id 索引；sub_57D670 查表后 sub_4DC510/sub_4DFC70 载入推进控制器）
- 表ID `55` ｜ 下载序 `63` ｜ 类名 `CCharaFlightTable` ｜ 逐列读取 `sub_57D4A0`
- 列数 31 ｜ 确证 28 ｜ 部分 0 ｜ gap 3

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `msma_id` | u32 | +0 | 机体ID（主键；col0 → +0） |
| 2 | `4` | `flight_flags_a` | u32 | +44 | u32 飞行/浮游模式标志位组 A（sub_4DC510/sub_4DFC70 载入推进控制器 +4940/+4736；col4→+44） |
| 3 | `5` | `flight_flags_b` | u32 | +48 | u32 飞行/浮游模式标志位组 B（sub_4DC510/sub_4DE4B0 载入推进控制器 +4944/+4948；col5→+48） |
| 4 | `6` | `hover_thrust_base` | float | +4 | float 悬停/浮游基础推力（×flt_D69A68 缩放；sub_4DC510/+4892、sub_4DFC70/+4696；col6→+4） |
| 5 | `7` | `hover_param_height` | float | +56 | float 悬停高度副参数（与 col8 同时>0 启用悬停模式；sub_4DC510/+4896；col7→+56） |
| 6 | `8` | `hover_param_damp` | float | +60 | float 悬停阻尼副参数（与 col7 同时>0 启用悬停并设 +4872；sub_4DC510/+4900；col8→+60） |
| 7 | `9` | `boost_accel` | float | +8 | float 推进/Boost 加速度（sub_4DC510/+4904；无悬停时亦作当前推进速度 +4860；col9→+8） |
| 8 | `10` | `boost_speed_max` | float | +12 | float 推进最高速度上限（sub_4DC510/+4908、+4864；sub_4DFC70/+4704；col10→+12） |
| 9 | `11` | `boost_drain_rate` | float | +16 | float 推进槽消耗速率（sub_4DC510/+4912；sub_4DFC70/+4708；col11→+16） |
| 10 | `12` | `gravity_scale` | float | +20 | float 重力影响缩放系数（sub_4DC510/+4916；sub_4DFC70/+4712；col12→+20） |
| 11 | `13` | `pitch_rate` | float | +32 | float 机体俯仰旋转角速度（sub_4DC510/+4928；sub_4DFC70/+4724；col13→+32） |
| 12 | `14` | `yaw_rate` | float | +36 | float 机体偏航旋转角速度（sub_4DC510/+4932；sub_4DFC70/+4728；col14→+36） |
| 13 | `15` | `roll_rate` | float | +40 | float 机体滚转旋转角速度（sub_4DC510/+4936；sub_4DFC70/+4732；col15→+40） |
| 14 | `16` | `float_height` | float | +24 | float 浮游/悬停目标高度（sub_4DC510/+4920；sub_4DFC70/+4716；col16→+24） |
| 15 | `17` | `float_damp` | float | +28 | float 浮游高度回归阻尼（sub_4DC510/+4924；sub_4DFC70/+4720；col17→+28） |
| 16 | `18` | `transform_time` | float | +64 | float MS 变形/切换飞行模式过渡时间（sub_4DC510/+4948；sub_4DFC70/+4740；col18→+64） |
| 17 | `19` | `landing_speed` | float | +68 | float 着陆判定速度阈值（sub_4C2D20 设 entity+0x163 bit2；sub_4DC510/+4952；col19→+68） |
| 18 | `20` | `takeoff_speed` | float | +72 | float 起飞/离地速度阈值（sub_4DC510/+4956；sub_4DFC70/+4748；col20→+72） |
| 19 | `21` | `air_brake` | float | +76 | float 空中刹车/减速系数（sub_4DC510/+4960；sub_4DFC70/+4752；col21→+76） |
| 20 | `22` | `stall_threshold` | float | +80 | float 失速速度阈值（Minovsky 机体 sub_4D7930 取 +80×flt_D6EED0→+1152；col22→+80） |
| 21 | `23` | `flight_speed_limit` | float | +84 | float 额外飞行速度上限/修正（sub_4DC510/+4968；sub_4DFC70/+4760；col23→+84） |
| 22 | `24` | `funnel_mode_id` | u32 | +108 | u32 浮游炮/Fin Funnel 模式索引（sub_4DC510/+4976；sub_4DFC70/+4764；col24→+108） |
| 23 | `25` | `hover_height_offset` | u32 | +52 | u32 悬停高度偏移量（sub_475680×flt_D6AE54→entity+384；sub_4DC510 触发；col25→+52） |
| 24 | `26` | `funnel_speed_hover` | float | +88 | float 悬停/变形态浮游炮速度倍率（entity+353 bit4 时 sub_479040→+380；col26→+88） |
| 25 | `27` | `funnel_speed_default` | float | +92 | float 默认态浮游炮速度倍率（sub_479040→entity+380；col27→+92） |
| 26 | `28` | `transform_bgm_speed` | float | +96 | float 变形时 BGM/镜头速度倍率（entity+353 bit4 时 sub_67E360→sub_666DD0；col28→+96） |
| 27 | `29` | `transform_bgm_speed_alt` | float | +100 | float 变形 BGM/镜头备用速度倍率（sub_67E360 非 bit4 路径；col29→+100） |
| 28 | `30` | `flight_feature_enable` | u32 | +104 | u32 飞行附加特性启用标志（sub_4DC510→bool +4980/+4984；col30→+104） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大有效列号。
