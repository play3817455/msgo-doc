# SC-0x1365-battle-game_begin

> 状态：`DONE`（2026-09-20，批次-5）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x1365` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `game_begin` |
| 名字字符串 | `)->_proto_battle_client::recv_game_begin( `，引用点 `0xB100B2`（`push offset aProtoBattleCli_18`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0FBDA` .. `0xB10671`（本批最大块，覆盖 `0xB0FBDA..0xB10671`，末尾接 `0x10643` 起的比较链） |
| 错误码 | `0x32`（`0xB0FBDA push 32h` 守卫 / 全部读失败与闭合失败处均 `push 32h`） |
| 关联命令 | **引导链**：`../SC-0x0C5F-battle-commander_candidacy_start/`（`0x0C5F`）、`../SC-0x1159-battle-game_mapgimmick_update/`（`0x1159`，`mapgimmicks` 的增量更新版）；地图切换 `../SC-0x243B-battle-game_btlfield_change/`（`0x243B`）；脚本 `../SC-0x1113-battle-game_script_play/`（`0x1113`） |

## 2. 结论摘要

- **报文体总长：`156 + 58·N1 + 52·N2 + 4·N3`**（N1 = `respawn_posts_num` ≤ 50、N2 = `mapgimmicks_num` ≤ 32、N3 = `missionunit_num` ≤ 11）——**23 个顶层字段位**（13 个定长标量 + 2 个结构体 + 3 组「计数 + 数组」+ 1 个结构体 + 1 个标量）。
- 长度校验方式：`0xB1006F mov ecx,[var_1B28]`（线游标）／`0xB1006F cmp ecx,[var_1B24]`（vs 报文末尾）／`0xB10075 jz ok` ⇒ **最后一个字段是 `mission_phase`（u32，`0xB1005B`）**，其后即闭合。
- 声明容量：`0x2806`（`0xB0FBF3 push 2806h`）＝ **10246**：
  `46 (字段 1~13) + 0x28(40, config 结构 claim) + 0x40(64, progress 结构 claim) + 4 (N1) + 50×0x50(4000) + 4 (N2) + 32×0xBC(6016) + 0x14(20, bgm_desc claim) + 4 (N3) + 11×4(44) + 4 (mission_phase)` **精确等于 `0x2806`** ⇒ 容量 = 上限场景线长（结构/元素按**缓冲槽步进**记账）。
- 是否分帧：否。
- 关键结论：全部 23 个实参经 `vt[0xEC](...)`（`0xB10627`）一次性交付 battle 业务层（开局初始化）；**23 个字段名全部由块内日志串一一对位确证**；三个数组/两个结构体的成员名由对应打印器（`sub_B0A670`/`sub_B0A820`/`sub_B0AA70`/`sub_B0AEA0`/`sub_B0B320`）确证，见 §3.1~§3.5。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择子 | `0x1365` | `0xB100B2` | 确证 |
| 1 | 0 | 4 | u32 | `snapshot_int_msec` | 快照发送间隔（毫秒） | 交 `vt[0xEC]` 第 1 实参；日志 `snapshot_int_msec=` | - | `0xB0FC37`、`0xB1010B`（日志名）、`0xB10624`（去向） | 确证 |
| 2 | 4 | 4 | u32 | `snapshot_res_msec` | 快照重发/保留间隔（毫秒） | 第 2 实参；日志 `snapshot_res_msec=` | - | `0xB0FC7A`、`0xB10138`、`0xB10621` | 确证 |
| 3 | 8 | 4 | u32 | `pos_factor` | 坐标换算系数 | 第 3 实参；日志 `pos_factor=` | - | `0xB0FC9E`、`0xB10162`、`0xB10617` | 确证 |
| 4 | 12 | 4 | u32 | `map_id` | 地图 ID | 第 4 实参；日志 `map_id=` | - | `0xB0FCC2`、`0xB1018C`、`0xB1060D` | 确证 |
| 5 | 16 | 4 | u32 | `btlfield` | 战场/战域 ID | 第 5 实参；日志 `btlfield=` | - | `0xB0FCEA`、`0xB101B6`、`0xB10603` | 确证 |
| 6 | 20 | 4 | u32 | `clear_remain_msec` | 关卡剩余时间（毫秒） | 第 6 实参；日志 `clear_remain_msec=` | - | `0xB0FD12`、`0xB101E0`、`0xB105F9` | 确证 |
| 7 | 24 | 1 | u8 | `is_disable_conq_sp` | 是否禁用征服/据点 SP | 第 7 实参（`movzx` 零扩展）；日志 `is_disable_conq_sp=` | `?`（0/1） | `0xB0FD3A`、`0xB10208`（日志名）、`0xB105D2`/`0xB105E9`（去向） | 确证（宽度）/枚举待定 |
| 8 | 25 | 1 | u8 | `is_room_suspend` | 房间是否处于暂停（suspend）状态 | 第 8 实参（`movzx`）；日志 `is_room_suspend=` | `?`（0/1） | `0xB0FD62`、`0xB10232`、`0xB105D2`/`0xB105DC` | 确证 |
| 9 | 26 | 4 | u32 | `mission_id` | 任务（关卡）ID | 第 9 实参；日志 `mission_id=` | - | `0xB0FD8A`、`0xB1025E`、`0xB105D1` | 确证 |
| 10 | 30 | 4 | u32 | `sudden_type` | 突发事件类型 | 第 10 实参；日志 `sudden_type=` | `?`（类型枚举未交叉） | `0xB0FDB2`、`0xB10288`、`0xB105C7` | 确证（宽度）/枚举待定 |
| 11 | 34 | 4 | u32 | `sudden_bonus_target` | 突发事件奖励目标 | 第 11 实参；日志 `sudden_bonus_target=` | - | `0xB0FDDA`、`0xB102B2`、`0xB105BD` | 确证 |
| 12 | 38 | 4 | u32 | `exp_min` | 本局经验下限 | 第 12 实参；日志 `exp_min=` | - | `0xB0FE02`、`0xB102DC`、`0xB105B6` | 确证 |
| 13 | 42 | 4 | u32 | `exp_max` | 本局经验上限 | 第 13 实参；日志 `exp_max=` | - | `0xB0FE2A`、`0xB10306`、`0xB105AF` | 确证 |
| 14 | 46 | 34 | struct `config` | 对战配置（A/B 两军兵力与点数、回合、dotdamage 等） | 结构指针交第 14 实参；日志 `config=`（打印器 `sub_B0A670`） | 成员见 §3.1；**claim 0x28 = 40（结构体跨度）≠ 线长 34** | `0xB0FE43`（`sub_B418C0` 预留 0x28）、`0xB0FE52`（`sub_B077B0` 读）、`0xB1032E`/`0xB10346`（日志） | 确证 |
| 15 | 80 | 46 | struct `progress` | 战况进度（据点、量表、规则计时、dot 伤害等） | 结构指针交第 15 实参；日志 `progress=`（打印器 `sub_B0A820`） | 成员见 §3.2；**claim 0x40 = 64 ≠ 线长 46** | `0xB0FE6B`（`sub_B05ED0` 预留 0x40）、`0xB0FE7A`（`sub_B07880` 读）、`0xB10358`/`0xB10370`（日志） | 确证 |
| 16 | 126 | 4 | u32 | `respawn_posts_num` | 重生点条目数 N1 | 上限 `cmp 32h`；驱动数组循环与打印循环；交第 17 实参（`vt[0xEC]` 第 17 个实参） | `0..50` | `0xB0FE94`（`sub_B02DD0` 读）、`0xB0FEBD`/`0xB0FEC0`（上限）、`0xB1059D`（去向） | 确证 |
| 17 | 130 | 58·N1 | `array<elem 58>` | `respawn_posts` | 重生点列表（每元素 58 字节；缓冲槽步进 `0x50 = 80`） | 数组基址交第 16 实参；日志 `respawn_posts={...}`（打印器 `sub_B0AA70`） | 成员见 §3.3 | `0xB0FECF`（`sub_B05F20` 预留 0x50/槽）、`0xB0FEEF`（`sub_B079A0` 读元素）、`0xB0FEFB`（循环步进 0x50）、`0xB10390`（打印器） | 确证 |
| 18 | 130+58N1 | 4 | u32 | `mapgimmicks_num` | 地图机关条目数 N2 | 上限 `cmp 20h`；驱动数组循环与打印循环；交第 19 实参 | `0..32` | `0xB0FF20`（读）、`0xB0FF30`/`0xB0FF35`（上限）、`0xB10589`（去向） | 确证 |
| 19 | 134+58N1 | 52·N2 | `array<elem 52>` | `mapgimmicks` | 地图机关列表（每元素 52 字节；缓冲槽步进 `0xBC = 188`） | 数组基址交第 18 实参；日志 `mapgimmicks={...}`（打印器 `sub_B0AEA0`） | 成员见 §3.4 | `0xB0FF4C`（`sub_B05F50` 预留 0xBC/槽）、`0xB0FF6E`（`sub_B07BD0` 读元素）、`0xB0FF7A`（循环步进 0xBC）、`0xB1040A`（打印器） | 确证 |
| 20 | 134+58N1+52N2 | 14 | struct `bgm_desc` | 背景音乐描述（终局/王牌/强制 BGM、是否单次） | 结构指针交第 20 实参；日志 `bgm_desc=`（打印器 `sub_B0B320`） | 成员见 §3.5；**claim 0x14 = 20 ≠ 线长 14** | `0xB0FFA3`（`sub_B41740` 预留 0x14）、`0xB0FFB2`（`sub_B07E00` 读）、`0xB1047B`/`0xB10493`（日志） | 确证 |
| 21 | 148+58N1+52N2 | 4 | u32 | `missionunit_num` | 任务机体编成条目数 N3 | 上限 `cmp 0Bh`；驱动数组循环与打印循环；交第 22 实参 | `0..11` | `0xB0FFCC`（读）、`0xB0FFDC`/`0xB0FFE1`（上限）、`0xB10577`（去向） | 确证 |
| 22 | 152+58N1+52N2 | 4·N3 | `array<u32, N3>` | `missionunit_set` | 任务机体（mission unit）ID 集合 | 数组基址交第 21 实参；日志 `missionunit_set={...}`（逐个 `sub_B03580` 打印） | 每元素 4 字节（槽步进 4） | `0xB0FFF8`（`sub_B41850` 预留 4/槽）、`0xB1001A`（`sub_B02DD0` 读元素）、`0xB10026`（循环步进 4）、`0xB104B9`/`0xB104EB`（日志） | 确证 |
| 23 | 156+58N1+52N2+4N3 | 4 | u32 | `mission_phase` | 任务阶段（phase） | 交第 23 实参；日志 `mission_phase=` | - | `0xB1005B`（读）、`0xB1051C`（日志名）、`0xB10572`（去向） | 确证 |
| - | 156+58N1+52N2+4N3 | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 容量 `0x2806` == `46+40+64+4+50×80+4+32×188+20+4+11×4+4` | - | `0xB1006F`|`0xB10075` | 确证 |

### 3.1 `config` 成员（`sub_B077B0` 读取 / `sub_B0A670` 打印；线长 34、槽 0x28=40）

| # | 元素偏移 | 长度 | 线类型 | 成员名 | 含义 | 证据(VA) |
|---|---|---|---|---|---|---|
| 14.1 | +0 | 2 | u16 | `A_troops` | A 军兵力 | `0xB077C3`/`0xB0A685`/`0xB0A691` |
| 14.2 | +4 | 4 | u32 | `A_point_max` | A 军点数上限 | `0xB077DF`/`0xB0A6AC`/`0xB0A6B8` |
| 14.3 | +8 | 4 | u32 | `A_win_cnt` | A 军胜利计数 | `0xB077F1`/`0xB0A6D3`/`0xB0A6DF` |
| 14.4 | +0xC | 2 | u16 | `B_troops` | B 军兵力 | `0xB07803`/`0xB0A6FA`/`0xB0A707` |
| 14.5 | +0x10 | 4 | u32 | `B_point_max` | B 军点数上限 | `0xB07812`/`0xB0A722`/`0xB0A72E` |
| 14.6 | +0x14 | 4 | u32 | `B_win_cnt` | B 军胜利计数 | `0xB07823`/`0xB0A749`/`0xB0A755` |
| 14.7 | +0x18 | 4 | u32 | `dotdmg_min` | dot 伤害下限 | `0xB07834`/`0xB0A77C` |
| 14.8 | +0x1C | 2 | u16 | `atk_team` | 当前进攻方队伍 | `0xB07845`/`0xB0A797`/`0xB0A7A4` |
| 14.9 | +0x20 | 4 | u32 | `round_now` | 当前回合 | `0xB07856`/`0xB0A7CB` |
| 14.10 | +0x24 | 4 | u32 | `round_max` | 回合上限 | `0xB07870`/`0xB0A7ED` |

### 3.2 `progress` 成员（`sub_B07880` 读取 / `sub_B0A820` 打印；线长 46、槽 0x40=64）

| # | 元素偏移 | 长度 | 线类型 | 成员名 | 含义 | 证据(VA) |
|---|---|---|---|---|---|---|
| 15.1 | +0 | 4 | u32 | `remain_msec` | 本局剩余时间（毫秒） | `0xB07893`/`0xB0A840` |
| 15.2 | +4 | 4 | u32 | `coop_step` | 协力（coop）阶段步号 | `0xB078AD`/`0xB0A867` |
| 15.3 | +8 | 4 | u32 | `A_point_now` | A 军当前点数 | `0xB078C3`/`0xB0A88E` |
| 15.4 | +0xC | 4 | u32 | `B_point_now` | B 军当前点数 | `0xB078D9`/`0xB0A8B5` |
| 15.5 | +0x10 | 2 | u16 | `A_gauge_dmg_scale` | A 军量表伤害比例 | `0xB078E6`/`0xB0A8D0`/`0xB0A8DD` |
| 15.6 | +0x12 | 2 | u16 | `B_gauge_dmg_scale` | B 军量表伤害比例 | `0xB078FB`/`0xB0A8F8`/`0xB0A905` |
| 15.7 | +0x14 | 1 | i8 | `coop_dead_remain` | 协力死亡剩余计数（打印器 `movsx`） | `0xB0790C`/`0xB0A928` |
| 15.8 | +0x15 | 1 | i8 | `is_prestart` | 是否处于开局前阶段（打印器 `movsx`） | `0xB0791D`/`0xB0A948` |
| 15.9 | +0x18 | 4 | u32 | `rule_status` | 规则状态 | `0xB0792E`/`0xB0A97C` |
| 15.10 | +0x1C | 4 | u32 | `rule_timer_msec` | 规则计时（毫秒） | `0xB0793F`/`0xB0A9A3` |
| 15.11 | +0x20 | 4 | u32 | `rule_param1` | 规则参数 1 | `0xB07950`/`0xB0A9CA` |
| 15.12 | +0x24 | 4 | u32 | `rule_param2` | 规则参数 2 | `0xB07961`/`0xB0A9F1` |
| 15.13 | +0x28 | 4 | u32 | `A_dot_dmg` | A 军 dot 伤害值 | `0xB07972`/`0xB0AA18` |
| 15.14 | +0x2C | 4 | u32 | `B_dot_dmg` | B 军 dot 伤害值 | `0xB0798C`/`0xB0AA3A` |

### 3.3 `respawn_posts` 元素成员（`sub_B079A0` 读取 / `sub_B0AA70` 打印；元素线长 58、槽 0x50=80）

| # | 元素偏移 | 长度 | 线类型 | 成员名 | 含义 | 证据(VA) |
|---|---|---|---|---|---|---|
| 17.1 | +0 | 4 | u32 | `type` | 重生点类型 | `0xB079B3`/`0xB0AA90` |
| 17.2 | +4 | 2 | u16 | `ini_team` | 初始所属队伍 | `0xB079CD`/`0xB0AAB8` |
| 17.3 | +6 | 2 | u16 | `ini_troops` | 初始所属兵种 | `0xB079E5`/`0xB0AAE0` |
| 17.4 | +8 | 13 | bytes | `name` | 重生点名称（定长 13 字节，**无 NUL 前缀**） | `0xB079F1`（13 次 u8 循环）/`0xB0AB07` |
| 17.5 | +0x18 | 4 | u32 | `gauge_max` | 量表上限 | `0xB07A1E`/`0xB0AB30` |
| 17.6 | +0x1C | 4 | u32 | `post_chara_id` | 驻守角色（chara）ID | `0xB07A34`/`0xB0AB57` |
| 17.7 | +0x20 | 2 | u16 | `pos_x` | X 坐标 | `0xB07A4A`/`0xB0AB7F` |
| 17.8 | +0x22 | 2 | u16 | `pos_y` | Y 坐标 | `0xB07A5C`/`0xB0ABA7` |
| 17.9 | +0x24 | 2 | u16 | `pos_z` | Z 坐标 | `0xB07A65`/`0xB0ABCF` |
| 17.10 | +0x26 | 2 | u16 | `dir` | 朝向 | `0xB07A76`/`0xB0ABF7` |
| 17.11 | +0x28 | 1 | i8 | `cmdr_sptype` | 指挥官支援类型（打印器 `movsx`） | `0xB07A8C`/`0xB0AC1F` |
| 17.12 | +0x2C | 4 | u32 | `group_id` | 编组 ID | `0xB07A9D`/`0xB0AC46` |
| 17.13 | +0x30 | 4 | u32 | `npc_ba_point_ent_id` | 关联 NPC 据点实体 ID | `0xB07AAE`/`0xB0AC6D` |
| 17.14 | +0x34 | 4 | u32 | `npc_ba_point_move_range_abs_x` | 关联 NPC 据点移动范围（绝对 X） | `0xB07ABF`/`0xB0AC94` |
| 17.15 | +0x38 | 4 | u32 | `param1` | 参数 1 | `0xB07AD0`/`0xB0ACBB` |
| 17.16 | +0x3C | 4 | u32 | `param2` | 参数 2 | `0xB07AEA`/`0xB0ACDD` |

### 3.4 `mapgimmicks` 元素成员（`sub_B07BD0` 读取 / `sub_B0AEA0` 打印；元素线长 52、槽 0xBC=188）

| # | 元素偏移 | 长度 | 线类型 | 成员名 | 含义 | 证据(VA) |
|---|---|---|---|---|---|---|
| 19.1 | +0 | 1 | i8 | `type` | 机关类型（打印器 `movsx`） | `0xB07BE3`/`0xB0AEC1` |
| 19.2 | +1 | 1 | i8 | `stat` | 机关状态（打印器 `movsx`） | `0xB07BFD`/`0xB0AEE9` |
| 19.3 | +2 | 2 | u16 | `ent_id` | 机关实体 ID | `0xB07C13`/`0xB0AF11` |
| 19.4 | +4 | 4 | u32 | `gauge_max` | 量表上限 | `0xB07C2B`/`0xB0AF38` |
| 19.5 | +8 | 4 | u32 | `msma_id` | 关联机体 ID | `0xB07C38`/`0xB0AF5F` |
| 19.6 | +0xC | 4 | u32 | `msma_id2` | 关联机体 ID（副） | `0xB07C4D`/`0xB0AF86` |
| 19.7 | +0x10 | 2 | u16 | `pos_x` | X 坐标 | `0xB07C5E`/`0xB0AFAE` |
| 19.8 | +0x12 | 2 | u16 | `pos_y` | Y 坐标 | `0xB07C6F`/`0xB0AFD6` |
| 19.9 | +0x14 | 2 | u16 | `pos_z` | Z 坐标 | `0xB07C80`/`0xB0AFFE` |
| 19.10 | +0x16 | 2 | u16 | `dir` | 朝向 | `0xB07C91`/`0xB0B026` |
| 19.11 | +0x18 | 2 | u16 | `pos2_x` | 第二坐标 X | `0xB07CA2`/`0xB0B04E` |
| 19.12 | +0x1A | 2 | u16 | `pos2_y` | 第二坐标 Y | `0xB07CB3`/`0xB0B076` |
| 19.13 | +0x1C | 2 | u16 | `pos2_z` | 第二坐标 Z | `0xB07CC4`/`0xB0B09E` |
| 19.14 | +0x1E | 2 | u16 | `ctrl_ent_id[0]` | 控制实体 ID 组（打印器 `ctrl_ent_id={`） | `0xB07CE2`（2 次循环）/`0xB0B0C1` |
| 19.15 | +0x20 | 2 | u16 | `ctrl_ent_id[1]` | 同上第 2 个 | `0xB07CF5`/`0xB0B0DB` |
| 19.16 | +0x22 | 2 | u16 | `ctrl_count` | 控制实体数 | `0xB07D02`/`0xB0B116` |
| 19.17 | +0x24 | 2 | u16 | `route_number` | 路线编号 | `0xB07D13`/`0xB0B13E` |
| 19.18 | +0x26 | 2 | u16 | `route_initial_index` | 路线起始索引 | `0xB07D24`/`0xB0B166` |
| 19.19 | +0x28 | 2 | u16 | `move_speed` | 移动速度 | `0xB07D35`/`0xB0B18E` |
| 19.20 | +0x2A | 2 | u16 | `rot_speed` | 旋转速度 | `0xB07D46`/`0xB0B1B6` |
| 19.21 | +0x2C | 2 | u16 | `door_auto_sensor_height` | 门自动感应器高度 | `0xB07D57`/`0xB0B1DE` |
| 19.22 | +0x2E | 2 | u16 | `door_auto_sensor_radius` | 门自动感应器半径 | `0xB07D68`/`0xB0B206` |
| 19.23 | +0x30 | 2 | u16 | `attach_barrier_npc_ent_id` | 关联屏障 NPC 实体 ID | `0xB07D79`/`0xB0B22E` |
| 19.24 | +0x32 | 2 | u16 | `local_ctrl_id` | 本地控制 ID | `0xB07D91`/`0xB0B251` |

### 3.5 `bgm_desc` 成员（`sub_B07E00` 读取 / `sub_B0B320` 打印；线长 14、槽 0x14=20）

| # | 元素偏移 | 长度 | 线类型 | 成员名 | 含义 | 证据(VA) |
|---|---|---|---|---|---|---|
| 20.1 | +0 | 1 | i8 | `is_final_phase` | 是否最终阶段（打印器 `movsx`） | `0xB07E0E`/`0xB0B341` |
| 20.2 | +4 | 4 | u32 | `field_bgm_id` | 战场 BGM ID | `0xB07E24`/`0xB0B368` |
| 20.3 | +8 | 4 | u32 | `ace_bgm_id` | 王牌（ace）BGM ID | `0xB07E36`/`0xB0B38F` |
| 20.4 | +0xC | 4 | u32 | `force_bgm_id` | 强制播放 BGM ID | `0xB07E48`/`0xB0B3B6` |
| 20.5 | +0x10 | 1 | i8 | `is_one_shot` | 是否只播放一次（打印器 `movsx`） | `0xB07E55`/`0xB0B3D9` |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB100B2` 落在 `sub_B0CC20` 的 case 块 `0xB0FBDA..0xB10671`（块首 `0xB0FBDA push 32h`）。
2. 入口 `call sub_B05DA0`（守卫）→ `push 2806h; call [edx+78h]`（容量 10246）→ `sub_ABB2F0` 初始化线游标。
3. 读取序列（严格线序，见 `asm.md` E2~E9）：13 个定长标量 → `sub_B418C0`+`sub_B077B0`(config) → `sub_B05ED0`+`sub_B07880`(progress) → u32(N1)+`sub_B05F20`+循环 `sub_B079A0` → u32(N2)+`sub_B05F50`+循环 `sub_B07BD0` → `sub_B41740`+`sub_B07E00`(bgm_desc) → u32(N3)+`sub_B41850`+循环 `sub_B02DD0` → `sub_B41470`+`sub_B02DD0`(mission_phase)。
4. 闭合：`0xB1006F`/`0xB10075`（在 `mission_phase` 之后）。
5. 去向：`0xB10572..0xB10625`（23 次 push，cdecl 逆序），`0xB10627 call edx`（`edx = [edx+0ECh]`）。

### 4.2 长度闭合（含容量反推）
- 常量部分 `46 + 34 + 46 + 4 + 4 + 14 + 4 + 4 = 156`；变量部分 `58·N1 + 52·N2 + 4·N3`。
- **容量精确核对**：`0x2806 = 10246 = 46 + 40 + 64 + 4 + (50×80=4000) + 4 + (32×188=6016) + 20 + 4 + (11×4=44) + 4` ✓
  - 结构 claim 用**结构体跨度/槽步进**（config 40、progress 64、respawn 80/元素、mapgimmick 188/元素、bgm_desc 20），**不是元素线长**（34/46/58/52/14）。
  - 三个数组上限 50 / 32 / 11 由块内 `cmp` 直接给出（`0xB0FEC0`、`0xB0FF35`、`0xB0FFE1`），与容量反推**完全一致** ⇒ 三方互证。
- 闭合点 `0xB1006F`/`0xB10075` 要求「游标 == 末尾」✓

### 4.3 存疑点
见 `notes.md`（`vt[0xEC]` 业务定名；若干枚举；`snapshot_res_msec` 语义）。

## 5. 质量门自检

- [x] G1 字段表总长 `156 + 58·N1 + 52·N2 + 4·N3` 与 `0xB1006F`/`0xB10075` 闭合校验一致；三个计数上限与容量 `0x2806` 反推精确吻合。
- [x] G2 每个字段类型都指回汇编（`sub_B02DD0` u32／`sub_B06230` u8／`sub_B02DF0` u16／`sub_B077B0`/`sub_B07880`/`sub_B079A0`/`sub_B07BD0`/`sub_B07E00` 复合读取器整函数扫描）；未使用伪代码类型。
- [x] G3 23 个顶层字段含义全部来自块内日志串；结构/元素成员来自打印器 `sub_B0A670`/`sub_B0A820`/`sub_B0AA70`/`sub_B0AEA0`/`sub_B0B320` 的成员名；用途指向 `vt[0xEC]`（`0xB10627`，23 实参，实参序已逐条记录）。
- [x] G4 不确定项（枚举取值、`vt[0xEC]` 定名、`snapshot_res_msec` 语义）已标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致（成员以 §3.1~§3.5 为准，`fields.csv` 以结构字段一行 + 指针示意）。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 引导链与同型命令（`0x0C5F`/`0x1159`/`0x243B`/`0x1113`）已在 §1 链接。
