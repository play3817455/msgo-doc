# db_design 形状定案（shapes）

> 本文件由 `serverv/tools/schema_design/gen_shapes.py` 生成，请勿手改。
> 机器可读版本：[shapes.json](shapes.json)，生成器只读 JSON。

证据源：`db_design/schema/composites/*.json`。判定规则与逐条覆盖见 `serverv/tools/schema_design/shapes.py`。

## 规则

| 条件 | shape | 落库形式 |
|---|---|---|
| `pad[N]` / 保留位 | `pad` | 不入库（编码补零） |
| 标量 | `scalar` | 单列 |
| `char[N]` / 文本语义的 `bytes[N]`/`u8[N]` | `text` | `TEXT` |
| `K×S` 文本槽 | `text_slots` | `TEXT[]` |
| 语义未定的定长块（≤64B） | `opaque` | `BYTEA`（须显式登记） |
| `T[N]` 标量数组 | `array_scalar` | PG 原生数组 |
| `E[N]` 复合体数组 | `array_struct` | 子表（`elem_index` 主键） |
| 内嵌复合体 ≤64B 且无数组 | `struct` | 前缀展开多列 |
| 内嵌复合体较大或含数组 | `subtree` | 1:1 子表 |

## 假设

- `u64` 线上为无符号，落库用 `BIGINT`：现有 ID/计数/位图实测未触及 2^63。
- `opaque` / `opaque_array` 仅允许由 `MEMBER_OVERRIDES` 显式登记，且单块 ≤ 64B；整包 `wire_blob` 永久禁止。
- 数组长度按 `count × 元素线长` 校验，元素线长取自复合体 `length`（内存 stride 不参与）。

## 逐成员定案

### AI（线长 165B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `type` | scalar | `u8` | 1B | `SMALLINT` | AI 类型 |
| `name` | text | `char[33]` | 33B | `TEXT` | 名称（定长 33 字节） |
| `param_id` | scalar | `u32` | 4B | `BIGINT` | 参数 ID |
| `action_type` | scalar | `u8` | 1B | `SMALLINT` | 行动类型 |
| `move_spd` | scalar | `u16` | 2B | `INTEGER` | 移动速度 |
| `stat` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 状态数组（10×u32） |
| `hate_ent_id` | array_scalar | `u16[10]` | 20B = 10×2B | `INTEGER[]` | 仇恨实体 ID（10×u16） |
| `hate_val` | array_scalar | `u16[10]` | 20B = 10×2B | `INTEGER[]` | 仇恨值（10×u16） |
| `pop_init_x` | scalar | `u16` | 2B | `INTEGER` | 出现初始 X |
| `pop_init_y` | scalar | `u16` | 2B | `INTEGER` | 出现初始 Y |
| `pop_init_z` | scalar | `u16` | 2B | `INTEGER` | 出现初始 Z |
| `pop_init_dir` | scalar | `u16` | 2B | `INTEGER` | 出现初始朝向 |
| `fire_start_x` | scalar | `u16` | 2B | `INTEGER` | 射击起点 X |
| `fire_start_y` | scalar | `u16` | 2B | `INTEGER` | 射击起点 Y |
| `fire_start_z` | scalar | `u16` | 2B | `INTEGER` | 射击起点 Z |
| `fire_end_x` | scalar | `u16` | 2B | `INTEGER` | 射击终点 X |
| `fire_end_y` | scalar | `u16` | 2B | `INTEGER` | 射击终点 Y |
| `fire_end_z` | scalar | `u16` | 2B | `INTEGER` | 射击终点 Z |
| `move_end_x` | scalar | `u16` | 2B | `INTEGER` | 移动终点 X |
| `move_end_y` | scalar | `u16` | 2B | `INTEGER` | 移动终点 Y |
| `move_end_z` | scalar | `u16` | 2B | `INTEGER` | 移动终点 Z |
| `order_kind` | scalar | `u16` | 2B | `INTEGER` | 指令种类 |
| `order_param` | scalar | `u32` | 4B | `BIGINT` | 指令参数 |
| `group_id` | scalar | `u32` | 4B | `BIGINT` | 编组 ID |
| `center_ms_entid` | scalar | `u16` | 2B | `INTEGER` | 中心机体实体 ID |
| `route_number` | scalar | `u16` | 2B | `INTEGER` | 路线编号 |
| `formation_id` | scalar | `u16` | 2B | `INTEGER` | 阵型 ID |
| `formation_number` | scalar | `u8` | 1B | `SMALLINT` | 阵型数量 |
| `stuck_escape` | scalar | `u8` | 1B | `SMALLINT` | 卡住脱困 |

### activity（线长 356B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 飞行员 ID |
| `pilot_name` | text | `char[25]` | 25B | `TEXT` | 飞行员名（NUL 结尾定长串） |
| `level` | scalar | `i8` | 1B | `SMALLINT` | 等级 |
| `is_admin` | scalar | `i8` | 1B | `SMALLINT` | 是否管理员 |
| `send_range` | scalar | `u32` | 4B | `BIGINT` | 发送范围 |
| `timestamp` | text | `char[24]` | 24B | `TEXT` | 时间戳文本（定长串） |
| `msg` | text | `char[241]` | 241B | `TEXT` | 公告正文（NUL 结尾定长串） |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称（NUL 结尾定长串） |
| `clan_emb_base` | scalar | `i8` | 1B | `SMALLINT` | 战队徽章底色 |
| `clan_emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 战队徽章部件2 |

### adop_get（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `db_index` | scalar | `u8` | 1B | `SMALLINT` | 数据库索引 |
| `equip_wid` | scalar | `u32` | 4B | `BIGINT` | 装备 wide ID |
| `adop_set` | array_scalar | `u16[4]` | 8B = 4×2B | `INTEGER[]` | 采纳集合（4×u16） |

### adop_list（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `db_index` | scalar | `u8` | 1B | `SMALLINT` | 数据库索引 |
| `equip_wid` | scalar | `u32` | 4B | `BIGINT` | 装备 wide ID |
| `adop_set` | array_scalar | `u16[4]` | 8B = 4×2B | `INTEGER[]` | 采纳集合（4×u16） |

### appear_info（线长 86B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `team` | scalar | `u8` | 1B | `SMALLINT` | 阵营/队伍 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 部队/兵种 |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 大区（世界）ID |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `ent_id` | scalar | `u32` | 4B | `BIGINT` | 实体 ID |
| `index` | scalar | `u32` | 4B | `BIGINT` | 序号/槽位 |
| `msma_id` | scalar | `u32` | 4B | `BIGINT` | 机体（msma）ID |
| `item_id` | scalar | `u32` | 4B | `BIGINT` | 物品/装备 ID |
| `type` | scalar | `u8` | 1B | `SMALLINT` | 类型 |
| `eff_range` | scalar | `u32` | 4B | `BIGINT` | 有效射程/范围 |
| `snapshot` | struct | `snapshot` | 39B → snapshot | `` | 实体状态快照（子结构 snapshot） |
| `arms_id` | scalar | `u32` | 4B | `BIGINT` | 武装（arms）ID |
| `state_bit` | scalar | `u16` | 2B | `INTEGER` | 状态位 |
| `is_gmk` | scalar | `u8` | 1B | `SMALLINT` | 是否 GMK |
| `is_using_ss` | scalar | `u8` | 1B | `SMALLINT` | 是否使用 SS |
| `remain_msec` | scalar | `u32` | 4B | `BIGINT` | 剩余时间（毫秒） |
| `buildup_eff_range` | scalar | `u32` | 4B | `BIGINT` | 强化后有效射程 |

### avatar（线长 18B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `avatar_id` | scalar | `u32` | 4B | `BIGINT` | 外观模板 ID |
| `gender` | scalar | `u8` | 1B | `SMALLINT` | 性别 |
| `face` | scalar | `u8` | 1B | `SMALLINT` | 脸型 |
| `skincolor` | scalar | `u8` | 1B | `SMALLINT` | 肤色 |
| `clothes` | scalar | `u16` | 2B | `INTEGER` | 服装 |
| `hair` | scalar | `u32` | 4B | `BIGINT` | 发型 |
| `accessory` | scalar | `u8` | 1B | `SMALLINT` | 饰品 |
| `frame` | scalar | `u8` | 1B | `SMALLINT` | 边框 |
| `voice` | scalar | `u8` | 1B | `SMALLINT` | 语音 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 口头禅（外观内嵌 byword 表 ID） |

### beginner_challenge_info（线长 454B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `begin_time` | scalar | `u32` | 4B | `BIGINT` | 开始时间 |
| `elapsed_days` | scalar | `u16` | 2B | `INTEGER` | 经过天数 |
| `archived` | array_scalar | `u16[32]` | 64B = 32×2B | `INTEGER[]` | 归档位图（32×u16） |
| `value` | array_scalar | `u32[96]` | 384B = 96×4B | `BIGINT[]` | 挑战数值（96×u32） |

### bgm_desc（线长 14B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `is_final_phase` | scalar | `i8` | 1B | `SMALLINT` | 是否最终阶段（打印器 movsx） |
| `field_bgm_id` | scalar | `u32` | 4B | `BIGINT` | 战场 BGM ID |
| `ace_bgm_id` | scalar | `u32` | 4B | `BIGINT` | 王牌（ace）BGM ID |
| `force_bgm_id` | scalar | `u32` | 4B | `BIGINT` | 强制播放 BGM ID |
| `is_one_shot` | scalar | `i8` | 1B | `SMALLINT` | 是否只播放一次（打印器 movsx） |

### block_detail（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### bmgpack（线长 23B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `shopitem_id` | scalar | `u32` | 4B | `BIGINT` | BGM 包商店道具 ID |
| `gp_x01` | scalar | `u32` | 4B | `BIGINT` | GP 单价（×01） |
| `gp_x10` | scalar | `u32` | 4B | `BIGINT` | GP 单价（×10） |
| `cp_x01` | scalar | `u32` | 4B | `BIGINT` | CP 单价（×01） |
| `cp_x10` | scalar | `u32` | 4B | `BIGINT` | CP 单价（×10） |
| `bit_eff` | scalar | `u8` | 1B | `SMALLINT` | 效果位标志 |
| `stock` | scalar | `u16` | 2B | `INTEGER` | 库存 |

### bonus_event（线长 64B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `main_rate` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 main_rate（16×u32 定长块，无线上 count） |
| `main_priority` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 main_priority（16×u32 定长块，无线上 count） |
| `gp_rate` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 gp_rate（16×u32 定长块，无线上 count） |
| `reward_rate` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 reward_rate（16×u32 定长块，无线上 count） |
| `raredrop_rate` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 raredrop_rate（16×u32 定长块，无线上 count） |
| `accump_rate` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 accump_rate（16×u32 定长块，无线上 count） |
| `over_custom_rate` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 over_custom_rate（16×u32 定长块，无线上 count） |
| `gp_offset` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 gp_offset（16×u32 定长块，无线上 count） |
| `reward_num` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 reward_num（16×u32 定长块，无线上 count） |
| `accump_offset` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 accump_offset（16×u32 定长块，无线上 count） |
| `over_custom_offset` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 over_custom_offset（16×u32 定长块，无线上 count） |
| `buildup_odds_offset` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 buildup_odds_offset（16×u32 定长块，无线上 count） |
| `bonus_target` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 bonus_target（16×u32 定长块，无线上 count） |
| `game_type` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 game_type（16×u32 定长块，无线上 count） |
| `begin_time` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 begin_time（16×u32 定长块，无线上 count） |
| `end_time` | scalar | `u32` | 4B | `BIGINT` | 加成活动参数 end_time（16×u32 定长块，无线上 count） |

### bonus_info（线长 29B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 奖励条目 ID |
| `battle_num` | scalar | `u32` | 4B | `BIGINT` | 所需战斗次数 |
| `begin_time` | scalar | `u32` | 4B | `BIGINT` | 开始时间 |
| `end_time` | scalar | `u32` | 4B | `BIGINT` | 结束时间 |
| `rwd_item_id` | scalar | `u32` | 4B | `BIGINT` | 奖励道具 ID |
| `rwd_item_num` | scalar | `u32` | 4B | `BIGINT` | 奖励道具数量 |
| `rwd_gp_amount` | scalar | `u32` | 4B | `BIGINT` | 奖励 GP 数额 |
| `is_completed` | scalar | `i8` | 1B | `SMALLINT` | 是否已完成 |

### bracket（线长 166B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `is_abort` | scalar | `u8` | 1B | `SMALLINT` | 是否中止 |
| `nodes` | array_struct | `bracket_node[15]` | 165B = 15×11B | `--` | 对阵节点（15×11B 线 / 14B 槽） |

### bracket_info（线长 46B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `phase` | scalar | `i8` | 1B | `SMALLINT` | 赛程阶段编号（打印器 movsx） |
| `round` | scalar | `u32` | 4B | `BIGINT` | 轮次 |
| `mission_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `bracket_id` | scalar | `u32` | 4B | `BIGINT` | 括号组 ID |
| `bracket_name` | text | `bytes` | 9B | `TEXT` | 对阵表名称（定长 9 字节，无 NUL 前缀） |
| `winners_bracket_id` | scalar | `u32` | 4B | `BIGINT` | 胜者组括号 ID |
| `losers_bracket_id` | scalar | `u32` | 4B | `BIGINT` | 败者组括号 ID |
| `open_time` | scalar | `u32` | 4B | `BIGINT` | 开放时间 |
| `close_time` | scalar | `u32` | 4B | `BIGINT` | 关闭时间 |
| `cupteam_id_a` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 A ID |
| `cupteam_id_b` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 B ID |

### bracket_node（线长 11B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `node_id` | scalar | `u16` | 2B | `INTEGER` | 节点 ID |
| `is_valid` | scalar | `u8` | 1B | `SMALLINT` | 节点是否有效 |
| `win_team_id` | scalar | `u16` | 2B | `INTEGER` | 获胜队伍 ID |
| `team_tr_a` | scalar | `u8` | 1B | `SMALLINT` | A 队阵营 |
| `team_id_a` | scalar | `u16` | 2B | `INTEGER` | A 队 ID |
| `team_tr_b` | scalar | `u8` | 1B | `SMALLINT` | B 队阵营 |
| `team_id_b` | scalar | `u16` | 2B | `INTEGER` | B 队 ID |

### buffitem（线长 6B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `itemid` | scalar | `u32` | 4B | `BIGINT` | 道具 ID |
| `is_used` | scalar | `u8` | 1B | `SMALLINT` | 是否已使用 |
| `is_usable` | scalar | `u8` | 1B | `SMALLINT` | 是否可用 |

### buffitem_ex（线长 6B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `itemid` | scalar | `u32` | 4B | `BIGINT` | 道具 ID |
| `is_used` | scalar | `u8` | 1B | `SMALLINT` | 是否已使用 |
| `is_usable` | scalar | `u8` | 1B | `SMALLINT` | 是否可用 |

### buildup_info（线长 42B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `build_num` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 各槽培育次数（7×u16；日志 build_num={…}） |
| `up_param` | array_scalar | `u32[7]` | 28B = 7×4B | `BIGINT[]` | 各槽强化参数（7×u32；日志 up_param={…}） |

### challenge_info（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 条目 ID |
| `val` | scalar | `u32` | 4B | `BIGINT` | 进度值 |
| `sub_val` | scalar | `u32` | 4B | `BIGINT` | 子进度值 |
| `is_clear` | scalar | `i8` | 1B | `SMALLINT` | 是否已通关（打印器 movsx） |

### channel（线长 54B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `channelid` | scalar | `u32` | 4B | `BIGINT` | 频道 ID |
| `name` | text | `char[37]` | 37B | `TEXT` | 频道名（NUL 结尾定长 37B） |
| `type` | scalar | `u8` | 1B | `SMALLINT` | 频道类型 |
| `pilotlv_min` | scalar | `u8` | 1B | `SMALLINT` | 可入最低驾驶员等级 |
| `pilotlv_max` | scalar | `u8` | 1B | `SMALLINT` | 可入最高驾驶员等级 |
| `user_num_eff` | scalar | `u16` | 2B | `INTEGER` | 联邦方人数 |
| `user_num_zeon` | scalar | `u16` | 2B | `INTEGER` | 吉翁方人数 |
| `user_max` | scalar | `u16` | 2B | `INTEGER` | 人数上限 |
| `user_conn` | scalar | `u16` | 2B | `INTEGER` | 当前连接数 |
| `user_comeback` | scalar | `u16` | 2B | `INTEGER` | 回归玩家数 |

### check_quest（线长 133B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `quest_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `title` | text | `bytes[97]` | 97B | `TEXT` | 任务标题（内联 97B；打印器 title=） |
| `achv_trig` | scalar | `u32` | 4B | `BIGINT` | 成就触发类型 |
| `achv_trigbit` | scalar | `u32` | 4B | `BIGINT` | 成就触发位掩码 |
| `achv_valA` | scalar | `u32` | 4B | `BIGINT` | 成就值 A |
| `achv_valB` | scalar | `u32` | 4B | `BIGINT` | 成就值 B |
| `achv_valC` | scalar | `u32` | 4B | `BIGINT` | 成就值 C |
| `denom_val` | scalar | `u32` | 4B | `BIGINT` | 分母值（进度分母） |
| `num_val` | scalar | `u32` | 4B | `BIGINT` | 分子值（当前进度） |
| `common_value` | scalar | `u32` | 4B | `BIGINT` | 通用附加值 |

### cinfo（线长 639B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `troops` | scalar | `i8` | 1B | `SMALLINT` | 阵营 |
| `npc_id` | scalar | `u32` | 4B | `BIGINT` | 战队 NPC ID |
| `npc_id2` | scalar | `u32` | 4B | `BIGINT` | 第二 NPC ID |
| `clan_name` | text | `bytes[31]` | 31B | `TEXT` | 战队名（定长 31B） |
| `level` | scalar | `i8` | 1B | `SMALLINT` | 战队等级 |
| `exp` | scalar | `u32` | 4B | `BIGINT` | 战队经验 |
| `emb_base` | scalar | `i8` | 1B | `SMALLINT` | 徽章底色 |
| `emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 2 |
| `member_num` | scalar | `u16` | 2B | `INTEGER` | 当前成员数 |
| `member_max` | scalar | `u16` | 2B | `INTEGER` | 成员上限 |
| `leader_id` | scalar | `u32` | 4B | `BIGINT` | 队长 pilot ID |
| `vs_win` | scalar | `u32` | 4B | `BIGINT` | 对战胜场 |
| `vs_lose` | scalar | `u32` | 4B | `BIGINT` | 对战败场 |
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `rank_score` | scalar | `u32` | 4B | `BIGINT` | 排名分数 |
| `rank_rate_vsl` | scalar | `u32` | 4B | `BIGINT` | 排名对战胜率 |
| `rate_vsl_score` | scalar | `u32` | 4B | `BIGINT` | 对战胜率分数 |
| `offer_is_active` | scalar | `i8` | 1B | `SMALLINT` | 招募/宣言是否激活 |
| `notice_body` | text | `bytes[433]` | 433B | `TEXT` | 战队公告正文（定长 433B；打印器 notice_body=） |
| `active_time_bits` | scalar | `u32` | 4B | `BIGINT` | 活跃时段位图 |
| `play_style` | scalar | `i8` | 1B | `SMALLINT` | 游戏风格 |
| `capture_unlock_num` | scalar | `u32` | 4B | `BIGINT` | 捕获解锁数量 |
| `feature_word` | text_slots | `bytes[112]` | 112B | `TEXT[]` | 特征文案块（4×28B；日志 feature_word={ + 3 段无单独日志名） |

### clan（线长 691B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 氏族 ID（服务端分配，身份列） |
| `clan_kind` | scalar | `u8` | 1B | `SMALLINT` | 氏族种类/所处阵营（leader_change 侧按 i8 读，同为 1 字节） |
| `clan_name` | text | `bytes[31]` | 31B | `TEXT` | 氏族名（命令侧 var(≤31) NUL 结尾；宽度取读侧定长 31B） |
| `npc_id` | scalar | `u32` | 4B | `BIGINT` | 建队 NPC ID |
| `is_active` | scalar | `u32` | 4B | `BIGINT` | 氏族是否激活（线宽 u32） |
| `emb_base` | scalar | `u8` | 1B | `SMALLINT` | 徽章底色 |
| `emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 徽章部件 2 |
| `offer_is_active` | scalar | `u32` | 4B | `BIGINT` | 招募宣言是否启用（命令侧字段名 is_active；cinfo 侧 offer_is_active） |
| `offer_subj` | text | `bytes[49]` | 49B | `TEXT` | 招募宣言标题（命令侧 var，读侧槽预算 0x31=49） |
| `offer_body` | text | `bytes[31]` | 31B | `TEXT` | 招募宣言正文（命令侧 var，读侧槽预算 0x1F=31） |
| `notice_body` | text | `bytes[433]` | 433B | `TEXT` | 氏族公告正文（命令侧 var，槽预算 0x1B1=433；cinfo 侧定长 433B） |
| `leader_pilot_id` | scalar | `u32` | 4B | `BIGINT` | 部队长机师 ID（命令侧 pilot_id_new；cinfo 侧 leader_id） |
| `lv` | scalar | `u8` | 1B | `SMALLINT` | 氏族等级（cinfo 侧名 level） |
| `exp` | scalar | `u32` | 4B | `BIGINT` | 氏族累计经验（升级进度的**权威值**：客户端拿它和 cfg.LVUP_CLAN 的累计需求做差算等级进度） |
| `deckcost` | scalar | `u32` | 4B | `BIGINT` | 氏族卡组编成费用上限（升级与退队响应里都带） |
| `active_time_bits` | scalar | `u8` | 1B | `SMALLINT` | 活跃时段位图（低 4 位 = 4 个时段复选框；写侧 u8、读侧 cinfo 槽宽 u32） |
| `play_style` | scalar | `u8` | 1B | `SMALLINT` | 游戏风格（下拉选中项序号；写侧 u8、读侧 cinfo 槽宽 i8） |
| `feature_word` | text_slots | `bytes[112]` | 112B | `TEXT[]` | 宣言短语（4×28B 文本槽：写侧 u8[112]、读侧 cinfo 同形） |

### clan_eff（线长 11B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 所属大区 ID |
| `emb_base` | scalar | `i8` | 1B | `SMALLINT` | 徽章底色 |
| `emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 2 |

### clan_member_card（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### clan_ranking_entry（线长 99B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rank` | scalar | `u32` | 4B | `BIGINT` | 名次 |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名 |
| `troops` | scalar | `i8` | 1B | `SMALLINT` | 势力 |
| `clan_lv` | scalar | `u32` | 4B | `BIGINT` | 战队等级 |
| `leader_pilot_id` | scalar | `u32` | 4B | `BIGINT` | 队长驾驶员 ID |
| `leader_pilot_name` | text | `char[25]` | 25B | `TEXT` | 队长名 |
| `leader_level` | scalar | `i8` | 1B | `SMALLINT` | 队长等级 |
| `emb_base` | scalar | `i8` | 1B | `SMALLINT` | 徽章底 |
| `emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 2 |
| `score` | scalar | `u32` | 4B | `BIGINT` | 战队分 |
| `avatar` | opaque | `avatar(18B)` | 18B | `BYTEA` | 战队徽章头像（18B 线 / 24B 槽） |

### clan_search_hit（线长 114B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `emb_base` | scalar | `u8` | 1B | `SMALLINT` | 队徽底 |
| `emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 队徽部件 1 |
| `emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 队徽部件 2 |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名（定长 31B） |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 战队等级 |
| `offer_body` | text | `char[31]` | 31B | `TEXT` | 招募正文（定长 31B） |
| `leader_name` | text | `char[25]` | 25B | `TEXT` | 队长名（定长 25B） |
| `member_num` | scalar | `u32` | 4B | `BIGINT` | 成员数 |
| `member_max` | scalar | `u32` | 4B | `BIGINT` | 成员上限 |
| `offer_is_active` | scalar | `u8` | 1B | `SMALLINT` | 招募是否有效 |
| `clan_kind` | scalar | `u8` | 1B | `SMALLINT` | 战队种类 |
| `active_time_bits` | scalar | `u32` | 4B | `BIGINT` | 活动时段位 |
| `play_style` | scalar | `u8` | 1B | `SMALLINT` | 游玩风格 |
| `capture_unlock_num` | scalar | `u32` | 4B | `BIGINT` | 占领解锁数 |

### clan_zeon（线长 11B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 所属大区 ID |
| `emb_base` | scalar | `i8` | 1B | `SMALLINT` | 徽章底色 |
| `emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 2 |

### comment（线长 267B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `msg_id` | scalar | `u64` | 8B | `BIGINT` | 留言 ID |
| `parent_msgid` | scalar | `u64` | 8B | `BIGINT` | 父留言 ID |
| `date` | scalar | `u32` | 4B | `BIGINT` | 留言时间 |
| `nice_count` | scalar | `u16` | 2B | `INTEGER` | 点赞数 |
| `is_niced` | scalar | `i8` | 1B | `SMALLINT` | 自己是否已点赞 |
| `body` | text | `char[193]` | 193B | `TEXT` | 留言正文（NUL 结尾定长串） |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 发言飞行员 ID |
| `npc_id` | scalar | `u32` | 4B | `BIGINT` | NPC ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 发言者名称 |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 发言者外观（18B 子结构） |

### config（线长 34B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `A_troops` | scalar | `u16` | 2B | `INTEGER` | A 军兵力 |
| `A_point_max` | scalar | `u32` | 4B | `BIGINT` | A 军点数上限 |
| `A_win_cnt` | scalar | `u32` | 4B | `BIGINT` | A 军胜利计数 |
| `B_troops` | scalar | `u16` | 2B | `INTEGER` | B 军兵力 |
| `B_point_max` | scalar | `u32` | 4B | `BIGINT` | B 军点数上限 |
| `B_win_cnt` | scalar | `u32` | 4B | `BIGINT` | B 军胜利计数 |
| `dotdmg_min` | scalar | `u32` | 4B | `BIGINT` | dot 伤害下限 |
| `atk_team` | scalar | `u16` | 2B | `INTEGER` | 当前进攻方队伍 |
| `round_now` | scalar | `u32` | 4B | `BIGINT` | 当前回合 |
| `round_max` | scalar | `u32` | 4B | `BIGINT` | 回合上限 |

### coop_room（线长 135B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `room_id` | scalar | `u32` | 4B | `BIGINT` | 房间 ID |
| `room_name` | text | `bytes[73]` | 73B | `TEXT` | 房间名（定长 73B） |
| `room_type` | scalar | `u32` | 4B | `BIGINT` | 房间类型 |
| `room_stat` | scalar | `i8` | 1B | `SMALLINT` | 房间状态 |
| `play_elapsed` | scalar | `u32` | 4B | `BIGINT` | 已进行时间（秒） |
| `mission_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `extrule_id` | scalar | `u32` | 4B | `BIGINT` | 扩展规则 ID |
| `is_lock` | scalar | `i8` | 1B | `SMALLINT` | 是否上锁 |
| `is_vsclan` | scalar | `i8` | 1B | `SMALLINT` | 是否部队对战房间 |
| `count_eff` | scalar | `u16` | 2B | `INTEGER` | 联邦侧人数 |
| `count_zeon` | scalar | `u16` | 2B | `INTEGER` | 吉翁侧人数 |
| `count_max` | scalar | `u16` | 2B | `INTEGER` | 房间人数上限 |
| `master_pilotid` | scalar | `u32` | 4B | `BIGINT` | 房主 pilot ID |
| `master_worldid` | scalar | `u32` | 4B | `BIGINT` | 房主 world ID |
| `master_name` | text | `bytes[25]` | 25B | `TEXT` | 房主名称（定长 25B） |

### cshist_item（线长 6B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `item_id` | scalar | `u32` | 4B | `BIGINT` | 物品/条目 ID |
| `num` | scalar | `u16` | 2B | `INTEGER` | 数量 |

### cupteam（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `cupteam_id` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 ID（服务端分配，身份列；dailycup_team_info_get_r 里叫 team_id） |
| `cupteam_rate` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍积分率 |

### dailycup_conf（线长 73B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `state` | scalar | `u32` | 4B | `BIGINT` | 杯赛状态 |
| `tournament_id` | scalar | `u32` | 4B | `BIGINT` | 锦标赛 ID |
| `mode` | scalar | `u32` | 4B | `BIGINT` | 模式 |
| `open_date` | scalar | `u32` | 4B | `BIGINT` | 开放日期 |
| `team_num` | scalar | `u32` | 4B | `BIGINT` | 队伍数量 |
| `bracket_num` | scalar | `u16` | 2B | `INTEGER` | 对阵表数量 |
| `bracket_max` | scalar | `u16` | 2B | `INTEGER` | 对阵表上限 |
| `booking_start` | scalar | `u32` | 4B | `BIGINT` | 预约开始时间 |
| `booking_end` | scalar | `u32` | 4B | `BIGINT` | 预约结束时间 |
| `mission_id_st` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 单淘任务 ID 列表（4×u32） |
| `mission_id_dt` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 双淘任务 ID 列表（4×u32） |
| `matching_extrule` | scalar | `u32` | 4B | `BIGINT` | 匹配扩展规则 |
| `extrule_id` | scalar | `u32` | 4B | `BIGINT` | 扩展规则 ID |
| `isTDM` | scalar | `u8` | 1B | `SMALLINT` | 是否 TDM 模式 |

### dailycup_conf_next（线长 73B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `state` | scalar | `u32` | 4B | `BIGINT` | 杯赛状态 |
| `tournament_id` | scalar | `u32` | 4B | `BIGINT` | 锦标赛 ID |
| `mode` | scalar | `u32` | 4B | `BIGINT` | 模式 |
| `open_date` | scalar | `u32` | 4B | `BIGINT` | 开放日期 |
| `team_num` | scalar | `u32` | 4B | `BIGINT` | 队伍数量 |
| `bracket_num` | scalar | `u16` | 2B | `INTEGER` | 对阵表数量 |
| `bracket_max` | scalar | `u16` | 2B | `INTEGER` | 对阵表上限 |
| `booking_start` | scalar | `u32` | 4B | `BIGINT` | 预约开始时间 |
| `booking_end` | scalar | `u32` | 4B | `BIGINT` | 预约结束时间 |
| `mission_id_st` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 单淘任务 ID 列表（4×u32） |
| `mission_id_dt` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 双淘任务 ID 列表（4×u32） |
| `matching_extrule` | scalar | `u32` | 4B | `BIGINT` | 匹配扩展规则 |
| `extrule_id` | scalar | `u32` | 4B | `BIGINT` | 扩展规则 ID |
| `isTDM` | scalar | `u8` | 1B | `SMALLINT` | 是否 TDM 模式 |

### dailycup_team_pilot（线长 48B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 驾驶员名 |
| `level` | scalar | `i8` | 1B | `SMALLINT` | 等级 |
| `avatar` | opaque | `avatar(18B)` | 18B | `BYTEA` | 头像（18B 线 / 24B 槽） |

### dc_point（线长 65B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `is_dc` | scalar | `i8` | 1B | `SMALLINT` | 本次是否掉线（DC） |
| `bef_dcpoint` | scalar | `u32` | 4B | `BIGINT` | 掉线前积分 |
| `aft_dcpoint` | scalar | `u32` | 4B | `BIGINT` | 掉线后积分 |
| `reward_item_ids` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 奖励道具 ID 列表（固定 4 项） |
| `reward_item_nums` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 奖励道具数量列表（固定 4 项） |
| `bef_next` | struct | `u32[3]` | 12B → special_a_next | `` | 下阶段奖励预览（掉线前）｜Oracle 实测：线上 3×u32（写记录流 3 次 4 字节写），并非仅内存成员 |
| `aft_next` | struct | `u32[3]` | 12B → special_a_next | `` | 下阶段奖励预览（掉线后）｜Oracle 实测：线上 3×u32（写记录流 3 次 4 字节写），并非仅内存成员 |

### dcpoint_detail（线长 65B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `is_dc` | scalar | `i8` | 1B | `SMALLINT` | 本次是否掉线（DC） |
| `bef_dcpoint` | scalar | `u32` | 4B | `BIGINT` | 掉线前积分 |
| `aft_dcpoint` | scalar | `u32` | 4B | `BIGINT` | 掉线后积分 |
| `reward_item_ids` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 奖励道具 ID 列表（固定 4 项） |
| `reward_item_nums` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 奖励道具数量列表（固定 4 项） |
| `bef_next` | struct | `u32[3]` | 12B → special_a_next | `` | 下阶段奖励预览（掉线前）｜Oracle 实测：线上 3×u32（写记录流 3 次 4 字节写），并非仅内存成员 |
| `aft_next` | struct | `u32[3]` | 12B → special_a_next | `` | 下阶段奖励预览（掉线后）｜Oracle 实测：线上 3×u32（写记录流 3 次 4 字节写），并非仅内存成员 |

### eq_bonus_modules_lot（线长 12B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `mod_0` | scalar | `u32` | 4B | `BIGINT` | 抽选模块 ID 0 |
| `mod_1` | scalar | `u32` | 4B | `BIGINT` | 抽选模块 ID 1 |
| `mod_2` | scalar | `u32` | 4B | `BIGINT` | 抽选模块 ID 2 |

### equip_set（线长 121B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `uniq_id` | scalar | `u64` | 8B | `BIGINT` | 装备套组唯一 id |
| `slot` | scalar | `u16` | 2B | `INTEGER` | 套组槽位号 |
| `eq_weapon` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 装备武器（3 项） |
| `eq_shield` | scalar | `u32` | 4B | `BIGINT` | 装备盾 |
| `eq_special` | scalar | `u32` | 4B | `BIGINT` | 装备特殊装备 |
| `eq_modules` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 装备模块（10 项） |
| `eq_bonus_modules` | scalar | `u32` | 4B | `BIGINT` | 奖励模块（1 项） |
| `eq_rental_modules` | scalar | `u32` | 4B | `BIGINT` | 租赁模块（1 项） |
| `setname` | text | `u8[43]` | 43B | `TEXT` | 套组名（43 字节定长） |

### evflag3（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `evflag3` | scalar | `u64` | 8B | `BIGINT` | 活动标志位组 3（位掩码；日志串 `evflag3=`） |

### exam_state（线长 68B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `state` | scalar | `u32` | 4B | `BIGINT` | 考核状态 |
| `chances_used` | scalar | `u32` | 4B | `BIGINT` | 已用机会数 |
| `chances_total` | scalar | `u32` | 4B | `BIGINT` | 总机会数 |
| `playsec_total` | scalar | `u32` | 4B | `BIGINT` | 总游玩秒数 |
| `playsec_elapsed` | scalar | `u32` | 4B | `BIGINT` | 已进行秒数 |
| `playscore_sum` | scalar | `u32` | 4B | `BIGINT` | 游玩分数合计 |
| `examination_list` | array_struct | `examination_item[5]` | 40B = 5×8B | `--` | 考核结果列表（固定 5 元 examination_item，元素 8B={id,gain_val}） |
| `interval_cnt` | scalar | `u32` | 4B | `BIGINT` | 间隔计数 |

### examination_info_entry（线长 16B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `val_00` | scalar | `u32` | 4B | `BIGINT` | 线序成员 1（打印器未命名） |
| `val_04` | scalar | `u32` | 4B | `BIGINT` | 线序成员 2（打印器未命名） |
| `val_08` | scalar | `u32` | 4B | `BIGINT` | 线序成员 3（打印器未命名） |
| `val_0c` | scalar | `u32` | 4B | `BIGINT` | 线序成员 4（打印器未命名） |

### examination_item（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 考核项 ID |
| `gain_val` | scalar | `u32` | 4B | `BIGINT` | 获得的考核值 |

### examination_state（线长 68B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `state` | scalar | `u32` | 4B | `BIGINT` | 考核状态 |
| `chances_used` | scalar | `u32` | 4B | `BIGINT` | 已用机会数 |
| `chances_total` | scalar | `u32` | 4B | `BIGINT` | 总机会数 |
| `playsec_total` | scalar | `u32` | 4B | `BIGINT` | 总游玩秒数 |
| `playsec_elapsed` | scalar | `u32` | 4B | `BIGINT` | 已进行秒数 |
| `playscore_sum` | scalar | `u32` | 4B | `BIGINT` | 游玩分数合计 |
| `examination_list` | array_struct | `examination_item[5]` | 40B = 5×8B | `--` | 考核结果列表（固定 5 元 examination_item，元素 8B={id,gain_val}） |
| `interval_cnt` | scalar | `u32` | 4B | `BIGINT` | 间隔计数 |

### ext_subrule（线长 20B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `subrule_type` | array_scalar | `u16[2]` | 4B = 2×2B | `INTEGER[]` | 子规则类型（2×u16） |
| `param` | array_scalar | `u16[8]` | 16B = 8×2B | `INTEGER[]` | 子规则参数（8×u16） |

### extrarule_xwar_info（线长 514B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `extra_rule` | scalar | `u16` | 2B | `INTEGER` | 扩展规则 ID |
| `param` | scalar | `u32` | 4B | `BIGINT` | 主参数（行 0 槽首 u32） |
| `row0` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 0（31×u32） |
| `row1` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 1（31×u32） |
| `row2` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 2（31×u32） |
| `row3` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 3（31×u32） |
| `w502_bytes` | opaque | `bytes[12]` | 12B | `BYTEA` | 12B 定长字段（原登记为 padding，reader 实测写入 3 次；粒度不判定） |

### favms（线长 66B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `favorite_ms_id` | scalar | `u32` | 4B | `BIGINT` | 收藏机体 ID |
| `battle_rule` | scalar | `u8` | 1B | `SMALLINT` | 战斗规则 |
| `favorite_exp_sum` | scalar | `u32` | 4B | `BIGINT` | 收藏经验合计 |
| `kill_cnt` | scalar | `u32` | 4B | `BIGINT` | 击坠数 |
| `kill_assist_cnt` | scalar | `u32` | 4B | `BIGINT` | 助攻数 |
| `resurrect_cnt` | scalar | `u32` | 4B | `BIGINT` | 复活数 |
| `stghold_damage` | scalar | `u32` | 4B | `BIGINT` | 据点伤害 |
| `battle_cnt` | scalar | `u32` | 4B | `BIGINT` | 战斗次数 |
| `score_max_atk` | scalar | `u32` | 4B | `BIGINT` | 攻击最高得分 |
| `score_max_spt` | scalar | `u32` | 4B | `BIGINT` | 支援最高得分 |
| `score_max_con` | scalar | `u32` | 4B | `BIGINT` | 控制最高得分 |
| `score_sum_atk` | scalar | `u32` | 4B | `BIGINT` | 攻击得分合计 |
| `score_sum_spt` | scalar | `u32` | 4B | `BIGINT` | 支援得分合计 |
| `score_sum_con` | scalar | `u32` | 4B | `BIGINT` | 控制得分合计 |
| `score_sum_sum` | scalar | `u32` | 4B | `BIGINT` | 总得分合计 |
| `last_update` | scalar | `u32` | 4B | `BIGINT` | 最后更新时间 |
| `dirty_flag` | scalar | `u8` | 1B | `SMALLINT` | 脏标记 |

### favms_add（线长 66B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `favorite_ms_id` | scalar | `u32` | 4B | `BIGINT` | 收藏机体 ID |
| `battle_rule` | scalar | `u8` | 1B | `SMALLINT` | 战斗规则 |
| `favorite_exp_sum` | scalar | `u32` | 4B | `BIGINT` | 机体经验累计 |
| `kill_cnt` | scalar | `u32` | 4B | `BIGINT` | 击坠数 |
| `kill_assist_cnt` | scalar | `u32` | 4B | `BIGINT` | 助攻数 |
| `resurrect_cnt` | scalar | `u32` | 4B | `BIGINT` | 复归数 |
| `stghold_damage` | scalar | `u32` | 4B | `BIGINT` | 据点伤害 |
| `battle_cnt` | scalar | `u32` | 4B | `BIGINT` | 出击次数 |
| `score_max_atk` | scalar | `u32` | 4B | `BIGINT` | 攻击分最高 |
| `score_max_spt` | scalar | `u32` | 4B | `BIGINT` | 支援分最高 |
| `score_max_con` | scalar | `u32` | 4B | `BIGINT` | 压制分最高 |
| `score_sum_atk` | scalar | `u32` | 4B | `BIGINT` | 攻击分累计 |
| `score_sum_spt` | scalar | `u32` | 4B | `BIGINT` | 支援分累计 |
| `score_sum_con` | scalar | `u32` | 4B | `BIGINT` | 压制分累计 |
| `score_sum_sum` | scalar | `u32` | 4B | `BIGINT` | 总分累计 |
| `last_update` | scalar | `u32` | 4B | `BIGINT` | 最后更新时间 |
| `dirty_flag` | scalar | `u8` | 1B | `SMALLINT` | 脏标志 |

### fire_point（线长 6B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `x` | scalar | `u16` | 2B | `INTEGER` | X 坐标 |
| `y` | scalar | `u16` | 2B | `INTEGER` | Y 坐标 |
| `z` | scalar | `u16` | 2B | `INTEGER` | Z 坐标 |

### friend_detail（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### friend_histories（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### funnel_snapshot_entry（线长 10B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `ent_id` | scalar | `u32` | 4B | `BIGINT` | 实体 ID |
| `wslot_idx` | scalar | `i8` | 1B | `SMALLINT` | 武器槽序号 |
| `move_info` | opaque | `u8[5]` | 5B | `BYTEA` | 移动信息（5 元字节） |

### funnelss（线长 10B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `ent_id` | scalar | `u32` | 4B | `BIGINT` | 实体 ID |
| `wslot_idx` | scalar | `i8` | 1B | `SMALLINT` | 武器槽索引 |
| `move_info` | opaque | `u8[5]` | 5B | `BYTEA` | 移动/姿态信息（5B 定长） |

### gacha_lineup（线长 6B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `gacha_id` | scalar | `u32` | 4B | `BIGINT` | 扭蛋 ID |
| `stock` | scalar | `u16` | 2B | `INTEGER` | 库存/剩余数 |

### gimmick_progress_entry（线长 7B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `gauge_now` | scalar | `u32` | 4B | `BIGINT` | 当前计量 |
| `stat` | scalar | `i8` | 1B | `SMALLINT` | 机关状态 |
| `access_ent_id` | scalar | `u16` | 2B | `INTEGER` | 接入实体 ID |

### hack_check（线长 79B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `move_spd` | scalar | `u16` | 2B | `INTEGER` | 移动速度 |
| `boost_gauge` | scalar | `u16` | 2B | `INTEGER` | 推进剂槽 |
| `boost_recov` | scalar | `u16` | 2B | `INTEGER` | 推进恢复 |
| `boost_consume` | scalar | `u16` | 2B | `INTEGER` | 推进消耗 |
| `clcheck_result` | scalar | `i8` | 1B | `SMALLINT` | 客户端校验结果 |
| `weapon_itemid` | scalar | `u32` | 4B | `BIGINT` | 武器道具 ID |
| `weapon_cooltime` | scalar | `u32` | 4B | `BIGINT` | 武器冷却 |
| `weapon_rapidtime` | scalar | `u32` | 4B | `BIGINT` | 武器连射时间 |
| `weapon_reload` | scalar | `u32` | 4B | `BIGINT` | 武器装填 |
| `debugger_found` | scalar | `u8` | 1B | `SMALLINT` | 检测到调试器 |
| `proc_ref_count` | scalar | `u8` | 1B | `SMALLINT` | 进程引用计数 |
| `reserved1` | scalar | `u8` | 1B | `SMALLINT` | 保留字节 1 |
| `reserved2` | scalar | `u8` | 1B | `SMALLINT` | 保留字节 2 |
| `weapon_bullet_speed` | scalar | `f32` | 4B | `REAL` | 弹速 |
| `weapon_range` | scalar | `u16` | 2B | `INTEGER` | 射程 |
| `weapon_charge_time` | scalar | `u16` | 2B | `INTEGER` | 蓄力时间 |
| `weapon_bullet_mgz` | scalar | `u16` | 2B | `INTEGER` | 弹匣容量 |
| `weapon_bullet_all` | scalar | `u16` | 2B | `INTEGER` | 总弹药 |
| `weapon_batch_fire` | scalar | `u16` | 2B | `INTEGER` | 连射批次 |
| `weapon_fired` | scalar | `f32` | 4B | `REAL` | 已发射弹量 |
| `wrestle_size` | scalar | `u16` | 2B | `INTEGER` | 格斗尺寸 |
| `wrestle_hack_check_ex` | scalar | `u8` | 1B | `SMALLINT` | 格斗反作弊扩展 |
| `fps` | scalar | `f32` | 4B | `REAL` | 帧率 |
| `ai_num` | scalar | `u8` | 1B | `SMALLINT` | AI 数量 |
| `perf_pre_chara` | scalar | `f32` | 4B | `REAL` | 性能：角色前 |
| `perf_chara` | scalar | `f32` | 4B | `REAL` | 性能：角色 |
| `perf_ai` | scalar | `f32` | 4B | `REAL` | 性能：AI |
| `perf_last` | scalar | `f32` | 4B | `REAL` | 性能：末段 |
| `perf_if` | scalar | `f32` | 4B | `REAL` | 性能：接口 |
| `perf_rdr` | scalar | `f32` | 4B | `REAL` | 性能：渲染 |

### intro_info（线长 547B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `active_time_bits` | scalar | `u8` | 1B | `SMALLINT` | 活跃时段位图 |
| `play_style` | scalar | `u8` | 1B | `SMALLINT` | 游戏风格 |
| `feature_word` | text_slots | `u8[112]` | 112B | `TEXT[]` | 特色词（4×28 字节） |
| `notice_body` | text | `u8[433]` | 433B | `TEXT` | 公告正文 |

### invite（线长 55B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 飞行员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 飞行员名（NUL 结尾定长串） |
| `mil_class` | scalar | `i8` | 1B | `SMALLINT` | 军衔等级 |
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `xwar_cnt` | scalar | `u32` | 4B | `BIGINT` | 跨服战次数 |
| `vslocal_cnt` | scalar | `u32` | 4B | `BIGINT` | 本地对战次数 |
| `last_login` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `last_logout` | scalar | `u32` | 4B | `BIGINT` | 最后登出时间 |
| `continued_login_days` | scalar | `u32` | 4B | `BIGINT` | 连续登录天数 |
| `is_bonus` | scalar | `i8` | 1B | `SMALLINT` | 是否有奖励加成 |

### item（线长 22B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `uniqid` | scalar | `u64` | 8B | `BIGINT` | 该物品实例的唯一 ID |
| `item_id` | scalar | `u32` | 4B | `BIGINT` | 物品模板 ID |
| `tm_sec` | scalar | `u32` | 4B | `BIGINT` | 获得/更新时刻（秒） |
| `tm_usec` | scalar | `u32` | 4B | `BIGINT` | 获得/更新时刻（微秒） |
| `stack` | scalar | `u16` | 2B | `INTEGER` | 堆叠数量 |

### item_info（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id_type` | scalar | `i8` | 1B | `SMALLINT` | 物品 ID 类型 |
| `itemid` | scalar | `u32` | 4B | `BIGINT` | 物品 ID |
| `is_itmbox` | scalar | `i8` | 1B | `SMALLINT` | 是否物品箱 |
| `amount` | scalar | `u16` | 2B | `INTEGER` | 数量 |

### item_list（线长 23B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `shopitem_id` | scalar | `u32` | 4B | `BIGINT` | 商店商品 ID |
| `gp_x01` | scalar | `u32` | 4B | `BIGINT` | GP 单价（×1） |
| `gp_x10` | scalar | `u32` | 4B | `BIGINT` | GP 单价（×10） |
| `cp_x01` | scalar | `u32` | 4B | `BIGINT` | CP 单价（×1） |
| `cp_x10` | scalar | `u32` | 4B | `BIGINT` | CP 单价（×10） |
| `bit_eff` | scalar | `u8` | 1B | `SMALLINT` | 位效果标志 |
| `stock` | scalar | `u16` | 2B | `INTEGER` | 库存 |

### leaders（线长 52B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称（定长 25 字节） |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 对本地胜率 |
| `is_leader` | scalar | `u8` | 1B | `SMALLINT` | 是否队长 |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `pstat` | scalar | `u8` | 1B | `SMALLINT` | 机师状态 |

### lpcard（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### lvjudge_hist（线长 369B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `lv_history` | array_scalar | `u32[24]` | 96B = 24×4B | `BIGINT[]` | 等级历史（24 档） |
| `lv_history_num` | scalar | `u32` | 4B | `BIGINT` | 等级历史有效条数 |
| `lv_history_max` | scalar | `u32` | 4B | `BIGINT` | 等级历史最大条数 |
| `xwarwin_history` | array_scalar | `u16[24]` | 48B = 24×2B | `INTEGER[]` | 大规模战胜场历史 |
| `xwarlose_history` | array_scalar | `u16[24]` | 48B = 24×2B | `INTEGER[]` | 大规模战败场历史 |
| `termstr_now` | text | `u8[65]` | 65B | `TEXT` | 当前赛季串（C 串） |
| `term_old` | array_scalar | `u32[25]` | 100B = 25×4B | `BIGINT[]` | 历史赛季 ID（25 个） |

### mail（线长 130B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `mailid` | scalar | `u64` | 8B | `BIGINT` | 邮件 ID |
| `kind` | scalar | `u32` | 4B | `BIGINT` | 邮件种类 |
| `state` | scalar | `u32` | 4B | `BIGINT` | 邮件状态（未读/已读等） |
| `pilot_name` | text | `char[25]` | 25B | `TEXT` | 发件飞行员名（NUL 结尾定长串） |
| `subject` | text | `char[73]` | 73B | `TEXT` | 邮件标题（NUL 结尾定长串） |
| `date` | scalar | `u32` | 4B | `BIGINT` | 邮件日期 |
| `accept_term` | scalar | `u32` | 4B | `BIGINT` | 附件领取期限 |
| `attach_type` | scalar | `u32` | 4B | `BIGINT` | 附件类型 |
| `attach_id` | scalar | `u32` | 4B | `BIGINT` | 附件 ID |

### mapgimmick_entry（线长 52B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `type` | scalar | `i8` | 1B | `SMALLINT` | 机关类型 |
| `stat` | scalar | `i8` | 1B | `SMALLINT` | 状态 |
| `ent_id` | scalar | `u16` | 2B | `INTEGER` | 实体 ID |
| `gauge_max` | scalar | `u32` | 4B | `BIGINT` | 计量上限 |
| `msma_id` | scalar | `u32` | 4B | `BIGINT` | 机体 ID |
| `msma_id2` | scalar | `u32` | 4B | `BIGINT` | 机体 ID 2 |
| `pos_x` | scalar | `u16` | 2B | `INTEGER` | X 坐标 |
| `pos_y` | scalar | `u16` | 2B | `INTEGER` | Y 坐标 |
| `pos_z` | scalar | `u16` | 2B | `INTEGER` | Z 坐标 |
| `dir` | scalar | `u16` | 2B | `INTEGER` | 朝向 |
| `pos2_x` | scalar | `u16` | 2B | `INTEGER` | 坐标 2 X |
| `pos2_y` | scalar | `u16` | 2B | `INTEGER` | 坐标 2 Y |
| `pos2_z` | scalar | `u16` | 2B | `INTEGER` | 坐标 2 Z |
| `ctrl_ent_id` | array_scalar | `u16[2]` | 4B = 2×2B | `INTEGER[]` | 控制实体 ID（2 元定长，`cmp ebx,2`） |
| `param_1` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_2` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_3` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_4` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_5` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_6` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_7` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `param_8` | scalar | `u16` | 2B | `INTEGER` | 打印器只打 ctrl_count，未命名 |
| `tail_1` | scalar | `u16` | 2B | `INTEGER` | 线尾 u16（打印器未命名） |

### member（线长 52B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称（定长 25 字节） |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 对本地胜率 |
| `is_leader` | scalar | `u8` | 1B | `SMALLINT` | 是否队长 |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `pstat` | scalar | `u8` | 1B | `SMALLINT` | 机师状态 |

### member_info（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### missionunit（线长 12B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `deck_type` | scalar | `u16` | 2B | `INTEGER` | 编成卡组类型 |
| `deck_set` | scalar | `u16` | 2B | `INTEGER` | 编成卡组套编号 |
| `missionunit_id` | scalar | `u64` | 8B | `BIGINT` | 任务单元唯一 ID（线上 2×u32 内联读/写；打印器分低/高 32 位） |

### missionunit_set（线长 12B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `deck_type` | scalar | `u16` | 2B | `INTEGER` | 编成卡组类型 |
| `deck_set` | scalar | `u16` | 2B | `INTEGER` | 编成卡组套编号 |
| `missionunit_id` | scalar | `u64` | 8B | `BIGINT` | 任务单元唯一 ID（线上 2×u32 内联读/写；打印器分低/高 32 位） |

### mprogress（线长 46B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `remain_msec` | scalar | `u32` | 4B | `BIGINT` | 本局剩余时间（毫秒） |
| `coop_step` | scalar | `u32` | 4B | `BIGINT` | 协力（coop）阶段步号 |
| `A_point_now` | scalar | `u32` | 4B | `BIGINT` | A 军当前点数 |
| `B_point_now` | scalar | `u32` | 4B | `BIGINT` | B 军当前点数 |
| `A_gauge_dmg_scale` | scalar | `u16` | 2B | `INTEGER` | A 军量表伤害比例 |
| `B_gauge_dmg_scale` | scalar | `u16` | 2B | `INTEGER` | B 军量表伤害比例 |
| `coop_dead_remain` | scalar | `i8` | 1B | `SMALLINT` | 协力死亡剩余计数（打印器 movsx） |
| `is_prestart` | scalar | `i8` | 1B | `SMALLINT` | 是否处于开局前阶段（打印器 movsx） |
| `rule_status` | scalar | `u32` | 4B | `BIGINT` | 规则状态 |
| `rule_timer_msec` | scalar | `u32` | 4B | `BIGINT` | 规则计时（毫秒） |
| `rule_param1` | scalar | `u32` | 4B | `BIGINT` | 规则参数 1 |
| `rule_param2` | scalar | `u32` | 4B | `BIGINT` | 规则参数 2 |
| `A_dot_dmg` | scalar | `u32` | 4B | `BIGINT` | A 军 dot 伤害值 |
| `B_dot_dmg` | scalar | `u32` | 4B | `BIGINT` | B 军 dot 伤害值 |

### ms（线长 244B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `uniqid` | scalar | `u64` | 8B | `BIGINT` | 机体唯一 ID |
| `msma_id` | scalar | `u32` | 4B | `BIGINT` | 机体模板 ID |
| `crew_msma_id` | scalar | `u32` | 4B | `BIGINT` | 乘员机体 ID |
| `decal` | scalar | `u32` | 4B | `BIGINT` | 贴纸/标识 |
| `color` | scalar | `u8` | 1B | `SMALLINT` | 配色 |
| `deck_index` | scalar | `u8` | 1B | `SMALLINT` | 卡组索引 |
| `cost` | scalar | `u32` | 4B | `BIGINT` | 机体 COST 值 |
| `is_costover` | scalar | `u8` | 1B | `SMALLINT` | 是否超 COST |
| `energy_now` | scalar | `u32` | 4B | `BIGINT` | 当前 EN |
| `weight_balance` | scalar | `u16` | 2B | `INTEGER` | 重量平衡 |
| `shield_weight` | scalar | `u16` | 2B | `INTEGER` | 盾重 |
| `sp_parts` | scalar | `u32` | 4B | `BIGINT` | 特殊部件 |
| `armor_up` | scalar | `u16` | 2B | `INTEGER` | 装甲强化 |
| `warp_up` | scalar | `u16` | 2B | `INTEGER` | 传送强化 |
| `boost_offset` | scalar | `u16` | 2B | `INTEGER` | 推进偏移 |
| `boost_offset_ns` | scalar | `u16` | 2B | `INTEGER` | 推进偏移（无盾） |
| `over_custom_armor` | scalar | `u16` | 2B | `INTEGER` | 超限自定义装甲 |
| `over_custom_warp` | scalar | `u16` | 2B | `INTEGER` | 超限自定义传送 |
| `over_custom_level` | scalar | `u16` | 2B | `INTEGER` | 超限自定义等级 |
| `witem_id` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 武器道具 ID（3） |
| `sitem_id` | scalar | `u32` | 4B | `BIGINT` | 副武器道具 ID |
| `spitem_id` | scalar | `u32` | 4B | `BIGINT` | 特殊道具 ID |
| `wbu_power` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 威力（3） |
| `wbu_stability` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 稳定性（3） |
| `wbu_rapid` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 连射（3） |
| `wbu_shot_range` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 射程（3） |
| `wbu_shield_hp` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 盾 HP（3） |
| `wbu_eff_time` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 有效时间（3） |
| `wbu_eff_range` | array_scalar | `u16[3]` | 6B = 3×2B | `INTEGER[]` | 武器 BU 有效范围（3） |
| `eq_modules` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 装备模块（10） |
| `eq_bonus_modules` | scalar | `u32` | 4B | `BIGINT` | 装备奖励模块 |
| `eq_rental_modules` | scalar | `u32` | 4B | `BIGINT` | 装备租用模块 |
| `adop_items_ms` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 采纳项 MS（4） |
| `adop_items_eq` | array_scalar | `u32[12]` | 48B = 12×4B | `BIGINT[]` | 采纳项装备（12） |
| `is_exdeck` | scalar | `u8` | 1B | `SMALLINT` | 是否扩展 deck |
| `is_rokaku` | scalar | `u8` | 1B | `SMALLINT` | 是否络格 |
| `rokakums_limit_use` | scalar | `u32` | 4B | `BIGINT` | 络格机体限制使用 |
| `respawn_wait_sec` | scalar | `u16` | 2B | `INTEGER` | 重生等待秒数 |
| `respawn_wait_max` | scalar | `u16` | 2B | `INTEGER` | 重生等待上限 |
| `is_reduce_respawn_wait` | scalar | `u8` | 1B | `SMALLINT` | 是否缩短重生等待 |
| `is_extrule_invalid` | scalar | `u8` | 1B | `SMALLINT` | 扩展规则无效标志 |
| `is_heroms` | scalar | `u8` | 1B | `SMALLINT` | 是否英雄机体 |
| `level_gauge_now_level` | scalar | `u32` | 4B | `BIGINT` | 等级 gauge 当前等级 |

### ms_lounge（线长 303B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `uniqid` | scalar | `u64` | 8B | `BIGINT` | 机体唯一 ID |
| `msma_id` | scalar | `u32` | 4B | `BIGINT` | 机体模板 ID |
| `tm_sec` | scalar | `u32` | 4B | `BIGINT` | 取得时间（秒） |
| `tm_usec` | scalar | `u32` | 4B | `BIGINT` | 取得时间（微秒） |
| `rental_time_limit` | scalar | `u32` | 4B | `BIGINT` | 租赁时限 |
| `nickname` | text | `char[61]` | 61B | `TEXT` | 机体昵称（NUL 结尾定长串） |
| `energy_now` | scalar | `u32` | 4B | `BIGINT` | 当前 EN |
| `decal` | scalar | `u32` | 4B | `BIGINT` | 贴纸/标识 |
| `color` | scalar | `u8` | 1B | `SMALLINT` | 配色 |
| `deckslot` | text | `char[2]` | 2B | `TEXT` | 卡组槽位小串（2B 定长，打印器按串打印） |
| `is_costover` | text | `char[2]` | 2B | `TEXT` | 是否超 COST（2B 定长小串，打印器按串打印） |
| `cost` | scalar | `u32` | 4B | `BIGINT` | 机体 COST 值 |
| `mission_cost` | scalar | `u32` | 4B | `BIGINT` | 任务 COST 值 |
| `eqweapon_itemid` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 装备武器道具 ID（3 项） |
| `eqshield_itemid` | scalar | `u32` | 4B | `BIGINT` | 装备盾道具 ID |
| `eqspecial_itemid` | scalar | `u32` | 4B | `BIGINT` | 装备特殊道具 ID |
| `eq_modules` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 装备模块（10 项） |
| `eq_bonus_modules` | scalar | `u32` | 4B | `BIGINT` | 奖励模块（1 项） |
| `eq_bonus_modules_lot` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 抽选奖励模块（3 项） |
| `eq_rental_modules` | scalar | `u32` | 4B | `BIGINT` | 租赁模块（1 项） |
| `sp_parts` | scalar | `u32` | 4B | `BIGINT` | 特殊部件 |
| `sp_parts_exp` | scalar | `u32` | 4B | `BIGINT` | 特殊部件经验 |
| `buildup_cnt` | scalar | `u16` | 2B | `INTEGER` | 强化次数 |
| `up_param` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 强化参数（7 项） |
| `up_param_develop` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 开发强化参数（7 项） |
| `weapon_buildup_extra_cnt` | scalar | `u16` | 2B | `INTEGER` | 武器强化追加次数 |
| `over_custom_exp` | scalar | `u32` | 4B | `BIGINT` | 超限自定义经验 |
| `over_custom_level` | scalar | `u32` | 4B | `BIGINT` | 超限自定义等级 |
| `over_custom_buildup_cnt` | scalar | `u32` | 4B | `BIGINT` | 超限自定义强化次数 |
| `over_custom_param` | array_scalar | `u32[7]` | 28B = 7×4B | `BIGINT[]` | 超限自定义参数（7 项） |
| `over_custom_count` | array_scalar | `u32[7]` | 28B = 7×4B | `BIGINT[]` | 超限自定义计数（7 项） |
| `msbits` | scalar | `u16` | 2B | `INTEGER` | 机体位标志 |
| `unlocked_colors` | scalar | `u32` | 4B | `BIGINT` | 已解锁配色 |
| `spticket_success_ms` | scalar | `u8` | 1B | `SMALLINT` | 补给券保底机体 |
| `spticket_greatest_ms` | scalar | `u8` | 1B | `SMALLINT` | 补给券最高机体 |
| `is_favorite` | scalar | `u8` | 1B | `SMALLINT` | 是否收藏 |

### ms_rokaku（线长 401B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `uniqid` | scalar | `u64` | 8B | `BIGINT` | 机体唯一 ID |
| `msma_id` | scalar | `u32` | 4B | `BIGINT` | 机体模板 ID |
| `tm_sec` | scalar | `u32` | 4B | `BIGINT` | 取得时间（秒） |
| `tm_usec` | scalar | `u32` | 4B | `BIGINT` | 取得时间（微秒） |
| `rental_time_limit` | scalar | `u32` | 4B | `BIGINT` | 租赁时限 |
| `nickname` | text | `char[61]` | 61B | `TEXT` | 机体昵称（NUL 结尾定长串） |
| `energy_now` | scalar | `u32` | 4B | `BIGINT` | 当前 EN |
| `decal` | scalar | `u32` | 4B | `BIGINT` | 贴纸/标识 |
| `color` | scalar | `u8` | 1B | `SMALLINT` | 配色 |
| `deckslot` | text | `char[2]` | 2B | `TEXT` | 卡组槽位小串（2B 定长，打印器按串打印） |
| `is_costover` | text | `char[2]` | 2B | `TEXT` | 是否超 COST（2B 定长小串，打印器按串打印） |
| `cost` | scalar | `u32` | 4B | `BIGINT` | 机体 COST 值 |
| `mission_cost` | scalar | `u32` | 4B | `BIGINT` | 任务 COST 值 |
| `eqweapon_itemid` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 装备武器道具 ID（3 项） |
| `eqshield_itemid` | scalar | `u32` | 4B | `BIGINT` | 装备盾道具 ID |
| `eqspecial_itemid` | scalar | `u32` | 4B | `BIGINT` | 装备特殊道具 ID |
| `eq_modules` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 装备模块（10 项） |
| `eq_bonus_modules` | scalar | `u32` | 4B | `BIGINT` | 奖励模块（1 项） |
| `eq_bonus_modules_lot` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 抽选奖励模块（3 项） |
| `eq_rental_modules` | scalar | `u32` | 4B | `BIGINT` | 租赁模块（1 项） |
| `sp_parts` | scalar | `u32` | 4B | `BIGINT` | 特殊部件 |
| `sp_parts_exp` | scalar | `u32` | 4B | `BIGINT` | 特殊部件经验 |
| `buildup_cnt` | scalar | `u16` | 2B | `INTEGER` | 强化次数 |
| `up_param` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 强化参数（7 项） |
| `up_param_develop` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 开发强化参数（7 项） |
| `weapon_buildup_extra_cnt` | scalar | `u16` | 2B | `INTEGER` | 武器强化追加次数 |
| `over_custom_exp` | scalar | `u32` | 4B | `BIGINT` | 超限自定义经验 |
| `over_custom_level` | scalar | `u32` | 4B | `BIGINT` | 超限自定义等级 |
| `over_custom_buildup_cnt` | scalar | `u32` | 4B | `BIGINT` | 超限自定义强化次数 |
| `over_custom_param` | array_scalar | `u32[7]` | 28B = 7×4B | `BIGINT[]` | 超限自定义参数（7 项） |
| `over_custom_count` | array_scalar | `u32[7]` | 28B = 7×4B | `BIGINT[]` | 超限自定义计数（7 项） |
| `msbits` | scalar | `u16` | 2B | `INTEGER` | 机体位标志 |
| `unlocked_colors` | scalar | `u32` | 4B | `BIGINT` | 已解锁配色 |
| `spticket_success_ms` | scalar | `u8` | 1B | `SMALLINT` | 补给券保底机体 |
| `spticket_greatest_ms` | scalar | `u8` | 1B | `SMALLINT` | 补给券最高机体 |
| `is_favorite` | scalar | `u8` | 1B | `SMALLINT` | 是否收藏 |
| `weapons` | array_struct | `unlockw[3]` | 90B = 3×30B | `--` | 络格武器列表（3 项，元素 = unlockw） |
| `limit_use` | scalar | `u32` | 4B | `BIGINT` | 络格限制使用 |
| `limit_coolup` | scalar | `u32` | 4B | `BIGINT` | 络格限制冷却 |

### ms_set（线长 95B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `uniq_id` | scalar | `u64` | 8B | `BIGINT` | 套装记录唯一 id |
| `deck_type` | scalar | `u16` | 2B | `INTEGER` | 卡组类型 |
| `deck_slot` | scalar | `u16` | 2B | `INTEGER` | 套装槽位 |
| `setname` | text | `u8[43]` | 43B | `TEXT` | 套装名（定长 43 字节） |
| `msma_uniq_ids` | array_scalar | `u64[4]` | 32B = 4×8B | `BIGINT[]` | 四个机体的唯一 id |
| `equip_set_slots` | array_scalar | `u16[4]` | 8B = 4×2B | `INTEGER[]` | 四个装备槽位 |

### msdeck（线长 324B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `row_0` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 0 |
| `row_1` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 1 |
| `row_2` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 2 |
| `row_3` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 3 |
| `row_4` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 4 |
| `row_5` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 5 |
| `row_6` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 6 |
| `row_7` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成行 7 |
| `grid_0` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 暗牌格 0 行 |
| `grid_1` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 暗牌格 1 行 |
| `grid_2` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 暗牌格 2 行 |
| `grid_3` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 暗牌格 3 行 |
| `tail_a` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 尾 A（+0x120） |
| `tail_b` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 尾 B（+0x130） |
| `tail_c` | opaque | `u8[4]` | 4B | `BYTEA` | 尾 C（+0x140，4×u8） |

### msdeck_entry（线长 36B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `msma_id` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成槽机体模板 ID（4 槽） |
| `color` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 编成槽配色（4 槽） |
| `is_heroms` | opaque | `u8[4]` | 4B | `BYTEA` | 编成槽是否英雄机（4 槽；打印器只打第 1 槽 `is_heroms=`） |

### mshipbid_card（线长 113B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_memb_exp_use` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验使用量 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 络格点数使用 |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |

### navi_entry（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `navi_id` | scalar | `u32` | 4B | `BIGINT` | 导航 ID |
| `status` | scalar | `u32` | 4B | `BIGINT` | 导航解锁/进度状态（枚举待交叉） |

### netcafe_challenge_info（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 条目 ID |
| `val` | scalar | `u32` | 4B | `BIGINT` | 进度值 |
| `sub_val` | scalar | `u32` | 4B | `BIGINT` | 子进度值 |
| `is_clear` | scalar | `i8` | 1B | `SMALLINT` | 是否已通关（打印器 movsx） |

### news（线长 244B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `msg_id` | scalar | `u64` | 8B | `BIGINT` | 新闻（留言）ID |
| `date` | scalar | `u32` | 4B | `BIGINT` | 新闻发布时间 |
| `kind` | scalar | `u16` | 2B | `INTEGER` | 新闻类别（打印器 `kind=` 按 u16 输出；枚举值待补） |
| `nice_count` | scalar | `u16` | 2B | `INTEGER` | 点赞数 |
| `child_count` | scalar | `u16` | 2B | `INTEGER` | 子条目（回复）条数 |
| `body` | text | `char[193]` | 193B | `TEXT` | 新闻正文（NUL 结尾定长串，逐字节循环 0xC1 次） |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 发布飞行员 ID（0 = 非玩家发布） |
| `npc_id` | scalar | `u32` | 4B | `BIGINT` | 发布 NPC ID（0 = 非 NPC 发布） |
| `name` | text | `char[25]` | 25B | `TEXT` | 发布者名称（NUL 结尾定长串，逐字节循环 0x19 次） |

### order（线长 10B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `kind` | scalar | `u16` | 2B | `INTEGER` | 排序/筛选种类 |
| `term` | scalar | `u16` | 2B | `INTEGER` | 统计期间 |
| `filter` | scalar | `u16` | 2B | `INTEGER` | 筛选条件 |
| `reason` | scalar | `u16` | 2B | `INTEGER` | 原因/依据 |
| `troops` | scalar | `u16` | 2B | `INTEGER` | 势力/阵营 |

### parts_exec_entry（线长 17B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `item_id` | scalar | `u32` | 4B | `BIGINT` | 部件物品 ID |
| `effect_msec` | scalar | `u32` | 4B | `BIGINT` | 效果生效毫秒 |
| `effect_catego` | scalar | `i8` | 1B | `SMALLINT` | 效果类别 |
| `effect_param` | scalar | `u16` | 2B | `INTEGER` | 效果参数 |
| `effect_value` | scalar | `u32` | 4B | `BIGINT` | 效果值 |
| `effect_value2` | scalar | `u16` | 2B | `INTEGER` | 效果值 2 |

### party（线长 81B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `party_id` | scalar | `u32` | 4B | `BIGINT` | 队伍 ID（服务端分配，身份列） |
| `is_recruiting` | scalar | `u8` | 1B | `SMALLINT` | 是否招募中 |
| `comment` | text | `bytes[61]` | 61B | `TEXT` | 队伍留言（命令侧 var，NUL 结尾；宽度取读侧定长槽 0x3D=61） |
| `party_type` | scalar | `u32` | 4B | `BIGINT` | 队伍类型 |
| `remain_minutes` | scalar | `u16` | 2B | `INTEGER` | 队伍剩余有效时间（分钟） |
| `channel_id` | scalar | `u32` | 4B | `BIGINT` | 队伍所在频道 ID（队伍建在创建者会话当时的频道里；读侧把 channel_id 与 party_id 并列回给客户端，招募列表/详情也逐条带它） |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 队伍势力（0 个 CS 写方**直接**送它：创建命令只送 is_recruiting/comment/party_type ⇒ 创建时按队长机师的势力落列，之后不再变） |
| `member_count` | scalar | `u16` | 2B | `INTEGER` | 队伍人数（=party_member 行数，含队长）——缓存列；两条读路径均现算（列表 count(*)，详情取数组长） |
| `pstat` | scalar | `u8` | 1B | `SMALLINT` | 队伍状态（招募视图独有的 1B 列）——★ 语义未定、无写方：四条队伍级命令都不下发它，旧库两处注释互相矛盾（「机师状态」/「队伍状态」）⇒ 本批按 0 写入，见 batch_28 |
| `is_lock` | scalar | `u8` | 1B | `SMALLINT` | 是否上锁（招募视图独有的 1B 列）——★ 无写方，本批按 0 写入；与 is_recruiting 不是同一字节（后者在 comment 之前、由创建/编辑命令写） |

### party_member（线长 52B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 成员名 |
| `level` | scalar | `i8` | 1B | `SMALLINT` | 等级 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 本地胜率 |
| `is_leader` | scalar | `i8` | 1B | `SMALLINT` | 是否队长 |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 成员外观（嵌套 avatar，线 18B / 槽 24B；读址是 `sub_B454D0` 里那次 `sub_B068B0(a1+36, a2)` 调用——18B 由该嵌套 reader 消费） |
| `pstat` | scalar | `i8` | 1B | `SMALLINT` | 成员状态（线上 +33→+51 之间隔着 18B avatar；内存 +60 与线上 +51 的差是业务侧填充造成的空洞） |

### party_member_stat（线长 31B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `lv` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 对本地胜率 |
| `stat` | scalar | `u8` | 1B | `SMALLINT` | 状态 |
| `is_booking` | scalar | `u8` | 1B | `SMALLINT` | 是否预约中 |
| `mission_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |

### pbadge（线长 152B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `hav_count` | array_scalar | `u32[38]` | 152B = 38×4B | `BIGINT[]` | 徽章计数数组（38 元 u32，逐元打 `hav_count=`） |

### pcard（线长 398B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `cmdr_fame` | scalar | `u32` | 4B | `BIGINT` | 指挥官声望 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 本地对战胜率 |
| `rate_vslocal_4ev` | scalar | `u16` | 2B | `INTEGER` | 活动对战胜率 |
| `rate_vslocal_clan` | scalar | `u16` | 2B | `INTEGER` | 战队对战胜率 |
| `rec_vs` | scalar | `u32` | 4B | `BIGINT` | 对战场次 |
| `rec_vs_win` | scalar | `u32` | 4B | `BIGINT` | 对战胜场 |
| `rec_vs_lose` | scalar | `u32` | 4B | `BIGINT` | 对战败场 |
| `rec_vsl_td` | scalar | `u32` | 4B | `BIGINT` | 对战塔防场次 |
| `rec_vsl_td_win` | scalar | `u32` | 4B | `BIGINT` | 对战塔防胜场 |
| `rec_vsl_td_lose` | scalar | `u32` | 4B | `BIGINT` | 对战塔防败场 |
| `rec_xwar` | scalar | `u32` | 4B | `BIGINT` | 大规模战场次 |
| `rec_xwar_win` | scalar | `u32` | 4B | `BIGINT` | 大规模战胜场 |
| `rec_xwar_lose` | scalar | `u32` | 4B | `BIGINT` | 大规模战败场 |
| `rec_xwar_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场大规模战场次 |
| `rec_xwar_win_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场大规模战胜场 |
| `rec_xwar_lose_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场大规模战败场 |
| `rec_xwar_win_term` | scalar | `u32` | 4B | `BIGINT` | 本届大规模战胜场 |
| `rec_xwar_win_term_last1` | scalar | `u32` | 4B | `BIGINT` | 上届大规模战胜场 |
| `rec_cmd` | scalar | `u32` | 4B | `BIGINT` | 指挥战场次 |
| `rec_cmd_win` | scalar | `u32` | 4B | `BIGINT` | 指挥战胜场 |
| `rec_cmd_lose` | scalar | `u32` | 4B | `BIGINT` | 指挥战败场 |
| `rec_cmd_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场指挥战场次 |
| `rec_cmd_win_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场指挥战胜场 |
| `rec_cmd_lose_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场指挥战败场 |
| `rec_dc` | scalar | `u32` | 4B | `BIGINT` | 断线战场次 |
| `rec_dc_win` | scalar | `u32` | 4B | `BIGINT` | 断线战胜场 |
| `rec_dc_lose` | scalar | `u32` | 4B | `BIGINT` | 断线战败场 |
| `score_assault_a` | scalar | `u32` | 4B | `BIGINT` | 评分·强袭 A |
| `score_assault_b` | scalar | `u32` | 4B | `BIGINT` | 评分·强袭 B |
| `score_snipe` | scalar | `u32` | 4B | `BIGINT` | 评分·狙击 |
| `score_cannon` | scalar | `u32` | 4B | `BIGINT` | 评分·炮击 |
| `score_support` | scalar | `u32` | 4B | `BIGINT` | 评分·支援 |
| `comment` | text | `char[116]` | 116B | `TEXT` | 自我介绍/评论 |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `cupteam_id` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 ID |
| `cupteam_name` | text | `char[31]` | 31B | `TEXT` | 杯赛队伍名称 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |
| `accum_point` | scalar | `u32` | 4B | `BIGINT` | 累计点数 |
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `base_accump` | scalar | `u32` | 4B | `BIGINT` | 基础累计点 |
| `req_accump` | scalar | `u32` | 4B | `BIGINT` | 需求累计点 |
| `level_point` | scalar | `u32` | 4B | `BIGINT` | 等级点 |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |

### pclanchlg（线长 9B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 记录 ID |
| `val` | scalar | `u32` | 4B | `BIGINT` | 记录值 |
| `is_clear` | scalar | `i8` | 1B | `SMALLINT` | 是否已通关 |

### pdaily（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 条目 ID |
| `val` | scalar | `u32` | 4B | `BIGINT` | 进度值 |
| `sub_val` | scalar | `u32` | 4B | `BIGINT` | 子进度值 |
| `is_clear` | scalar | `i8` | 1B | `SMALLINT` | 是否已通关（打印器 movsx） |

### phase_info（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `phase` | scalar | `i8` | 1B | `SMALLINT` | 赛程阶段编号（打印器 movsx） |
| `round` | scalar | `u32` | 4B | `BIGINT` | 轮次 |
| `open_time` | scalar | `u32` | 4B | `BIGINT` | 开放时间 |
| `close_time` | scalar | `u32` | 4B | `BIGINT` | 关闭时间 |

### pilot（线长 159B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 驾驶员名（NUL 结尾，定长 25 槽） |
| `troops` | scalar | `i8` | 1B | `SMALLINT` | 所属阵营（0=秩序 / 1=抵抗） |
| `level` | scalar | `i8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `i8` | 1B | `SMALLINT` | 军衔阶级 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 口头禅（byword 表 ID） |
| `cmdr_fame` | scalar | `u32` | 4B | `BIGINT` | 指挥官功勋 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 对本服胜率 |
| `rate_vslocal_4ev` | scalar | `u16` | 2B | `INTEGER` | 对本服胜率（4 人战） |
| `rate_vslocal_clan` | scalar | `u16` | 2B | `INTEGER` | 对本服胜率（部队战） |
| `level_point` | scalar | `u32` | 4B | `BIGINT` | 等级点数 |
| `avatar` | struct | `avatar(18B)` | 18B → avatar | `` | 外观（18B 子结构） |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 所属部队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 部队名（NUL 结尾，定长 31 槽） |
| `clan_emb_base` | scalar | `i8` | 1B | `SMALLINT` | 部队徽章底图 |
| `clan_emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 部队徽章部件 1 |
| `clan_emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 部队徽章部件 2 |
| `cupteam_id` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 ID |
| `cupteam_name` | text | `char[31]` | 31B | `TEXT` | 杯赛队伍名（NUL 结尾，定长 31 槽） |
| `accum_point` | scalar | `u32` | 4B | `BIGINT` | 累计点数 |
| `rank` | scalar | `u32` | 4B | `BIGINT` | 名次/顺位 |
| `base_accump` | scalar | `u32` | 4B | `BIGINT` | 基础累计点 |
| `req_accump` | scalar | `u32` | 4B | `BIGINT` | 所需累计点 |
| `penalty` | scalar | `u32` | 4B | `BIGINT` | 惩罚值 |

### pilot_detail（线长 51672B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `exp` | scalar | `u32` | 4B | `BIGINT` | 经验值 |
| `money` | scalar | `u32` | 4B | `BIGINT` | 游戏内货币 |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 所属战队 ID |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `clan_forbidden` | scalar | `u32` | 4B | `BIGINT` | 战队禁入/禁言标志 |
| `cupteam_id` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 ID |
| `deckcost` | scalar | `u16` | 2B | `INTEGER` | 卡组/编成费用 |
| `last_battle` | scalar | `u32` | 4B | `BIGINT` | 上次战斗 |
| `cw_chscore` | scalar | `u32` | 4B | `BIGINT` | 连战/冠军积分 |
| `score_special_a` | scalar | `u32` | 4B | `BIGINT` | 特殊积分 A |
| `last_play_bonus` | scalar | `u32` | 4B | `BIGINT` | 上次游玩奖励 |
| `last_play_bonus_vsl` | scalar | `u32` | 4B | `BIGINT` | 上次 VS 联赛奖励 |
| `last_play_bonus_vsl_cnt` | scalar | `u16` | 2B | `INTEGER` | 上次 VS 联赛奖励次数 |
| `last_dormant_ret_cc` | scalar | `u32` | 4B | `BIGINT` | 上次休眠回归奖励 |
| `capture_bonus_state` | scalar | `u32` | 4B | `BIGINT` | 占领奖励状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占领奖励上限 |
| `clan_rokaku_btime_limit` | scalar | `u32` | 4B | `BIGINT` | 战队楼阁建设时间上限 |
| `comment` | text | `bytes[115]` | 115B | `TEXT` | 个人留言（定长 115B） |
| `hav_medal` | array_scalar | `u64[16]` | 128B = 16×8B | `BIGINT[]` | 已获得勋章（16×u64） |
| `hav_emblem` | array_scalar | `u64[8]` | 64B = 8×8B | `BIGINT[]` | 已获得徽章（8×u64） |
| `hav_avatar` | array_scalar | `u64[160]` | 1280B = 160×8B | `BIGINT[]` | 已获得头像（160×u64） |
| `hav_voice` | array_scalar | `u64[8]` | 64B = 8×8B | `BIGINT[]` | 已获得语音（8×u64） |
| `hav_modules` | array_scalar | `u32[128]` | 512B = 128×4B | `BIGINT[]` | 已获得模块（128×u32） |
| `examination_state` | subtree | `struct` | 68B → examination_state | `` | 考验/考核状态 |
| `rokaku_uniq_msid` | scalar | `u64` | 8B | `BIGINT` | 楼阁机体唯一 ID |
| `rokaku_space_uniq_msid` | scalar | `u64` | 8B | `BIGINT` | 楼阁空间机体唯一 ID |
| `rokaku_pt` | scalar | `u32` | 4B | `BIGINT` | 楼阁点数 |
| `rokaku_pt_use` | scalar | `u32` | 4B | `BIGINT` | 已用楼阁点数 |
| `cshist` | array_struct | `cshist_item[32]` | 192B = 32×6B | `--` | CS 战绩历史（32×6B） |
| `second_chance_free` | scalar | `u8` | 1B | `SMALLINT` | 复归机会（免费）次数 |
| `second_chance_free_upd` | scalar | `u32` | 4B | `BIGINT` | 复归机会更新时间 |
| `hav_rental_modules` | array_struct | `rental_module[128]` | 1024B = 128×8B | `--` | 租用模块（128×8B） |
| `dc_point` | scalar | `u32` | 4B | `BIGINT` | DC 点数 |
| `favms_arr` | array_struct | `favms[720]` | 47520B = 720×66B | `--` | 收藏机体战绩（720×66B） |
| `heroms_grants` | array_scalar | `u32[10]` | 40B = 10×4B | `BIGINT[]` | 英雄授予列表（10×u32） |
| `heroms_uniqid` | scalar | `u64` | 8B | `BIGINT` | 英雄唯一 ID |
| `last_period_bonus` | scalar | `u32` | 4B | `BIGINT` | 上次周期奖励 |
| `daily_battle_bonus_flg` | scalar | `u32` | 4B | `BIGINT` | 每日战斗奖励标志 |
| `last_daily_battle_bonus` | scalar | `u32` | 4B | `BIGINT` | 上次每日战斗奖励 |
| `check_progress_quest_id` | scalar | `u32` | 4B | `BIGINT` | 进度检查任务 ID |
| `lvjudge_hist` | array_scalar | `u16[1]` | 2B = 1×2B | `INTEGER[]` | 等级判定历史（1 项） |
| `pilot_made_timestamp` | scalar | `u32` | 4B | `BIGINT` | 驾驶员创建时间戳 |
| `newpilot_challenge_nextindex` | scalar | `u16` | 2B | `INTEGER` | 新兵挑战下一序号 |
| `newpilot_challenge_last` | scalar | `u32` | 4B | `BIGINT` | 新兵挑战上次值 |
| `sc_lv_up_reward_get` | array_scalar | `u16[19]` | 38B = 19×2B | `INTEGER[]` | 等级提升奖励获取位图（19 项） |
| `sc_lv_max_pre` | array_scalar | `u16[12]` | 24B = 12×2B | `INTEGER[]` | 等级上限预览（12 项） |
| `sc_lv_max` | scalar | `u16` | 2B | `INTEGER` | 当前等级上限 |
| `last_pilot_channel_in` | scalar | `u32` | 4B | `BIGINT` | 上次进入频道 |
| `monthly_bonus_holding_id` | scalar | `u16` | 2B | `INTEGER` | 月奖励持有 ID |
| `monthly_bonus_logincnt` | scalar | `u16` | 2B | `INTEGER` | 月奖励登录计数 |
| `monthly_bonus_xwarcnt` | scalar | `u16` | 2B | `INTEGER` | 月奖励对战计数 |
| `periodpath_end` | scalar | `u32` | 4B | `BIGINT` | 周期路径终点 |
| `beginner_challenge_info` | subtree | `struct` | 454B → beginner_challenge_info | `` | 新兵挑战信息 |

### pilots_list（线长 398B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称 |
| `last_in` | scalar | `u32` | 4B | `BIGINT` | 最后登录时间 |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `mil_class` | scalar | `u8` | 1B | `SMALLINT` | 军衔 |
| `byword` | scalar | `u16` | 2B | `INTEGER` | 座右铭 ID |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |
| `cmdr_fame` | scalar | `u32` | 4B | `BIGINT` | 指挥官声望 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 本地对战胜率 |
| `rate_vslocal_4ev` | scalar | `u16` | 2B | `INTEGER` | 活动对战胜率 |
| `rate_vslocal_clan` | scalar | `u16` | 2B | `INTEGER` | 战队对战胜率 |
| `rec_vs` | scalar | `u32` | 4B | `BIGINT` | 对战场次 |
| `rec_vs_win` | scalar | `u32` | 4B | `BIGINT` | 对战胜场 |
| `rec_vs_lose` | scalar | `u32` | 4B | `BIGINT` | 对战败场 |
| `rec_vsl_td` | scalar | `u32` | 4B | `BIGINT` | 对战塔防场次 |
| `rec_vsl_td_win` | scalar | `u32` | 4B | `BIGINT` | 对战塔防胜场 |
| `rec_vsl_td_lose` | scalar | `u32` | 4B | `BIGINT` | 对战塔防败场 |
| `rec_xwar` | scalar | `u32` | 4B | `BIGINT` | 大规模战场次 |
| `rec_xwar_win` | scalar | `u32` | 4B | `BIGINT` | 大规模战胜场 |
| `rec_xwar_lose` | scalar | `u32` | 4B | `BIGINT` | 大规模战败场 |
| `rec_xwar_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场大规模战场次 |
| `rec_xwar_win_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场大规模战胜场 |
| `rec_xwar_lose_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场大规模战败场 |
| `rec_xwar_win_term` | scalar | `u32` | 4B | `BIGINT` | 本届大规模战胜场 |
| `rec_xwar_win_term_last1` | scalar | `u32` | 4B | `BIGINT` | 上届大规模战胜场 |
| `rec_cmd` | scalar | `u32` | 4B | `BIGINT` | 指挥战场次 |
| `rec_cmd_win` | scalar | `u32` | 4B | `BIGINT` | 指挥战胜场 |
| `rec_cmd_lose` | scalar | `u32` | 4B | `BIGINT` | 指挥战败场 |
| `rec_cmd_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场指挥战场次 |
| `rec_cmd_win_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场指挥战胜场 |
| `rec_cmd_lose_last1` | scalar | `u32` | 4B | `BIGINT` | 上一场指挥战败场 |
| `rec_dc` | scalar | `u32` | 4B | `BIGINT` | 断线战场次 |
| `rec_dc_win` | scalar | `u32` | 4B | `BIGINT` | 断线战胜场 |
| `rec_dc_lose` | scalar | `u32` | 4B | `BIGINT` | 断线战败场 |
| `score_assault_a` | scalar | `u32` | 4B | `BIGINT` | 评分·强袭 A |
| `score_assault_b` | scalar | `u32` | 4B | `BIGINT` | 评分·强袭 B |
| `score_snipe` | scalar | `u32` | 4B | `BIGINT` | 评分·狙击 |
| `score_cannon` | scalar | `u32` | 4B | `BIGINT` | 评分·炮击 |
| `score_support` | scalar | `u32` | 4B | `BIGINT` | 评分·支援 |
| `comment` | text | `char[116]` | 116B | `TEXT` | 自我介绍/评论 |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 战队 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名称 |
| `clan_emb_base` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章底 |
| `clan_emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件1 |
| `clan_emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 战队徽章部件2 |
| `clan_memb_exp` | scalar | `u32` | 4B | `BIGINT` | 战队成员经验 |
| `cupteam_id` | scalar | `u32` | 4B | `BIGINT` | 杯赛队伍 ID |
| `cupteam_name` | text | `char[31]` | 31B | `TEXT` | 杯赛队伍名称 |
| `channel_id` | scalar | `u8` | 1B | `SMALLINT` | 频道 ID |
| `state_bits` | scalar | `u8` | 1B | `SMALLINT` | 状态位 |
| `accum_point` | scalar | `u32` | 4B | `BIGINT` | 累计点数 |
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `base_accump` | scalar | `u32` | 4B | `BIGINT` | 基础累计点 |
| `req_accump` | scalar | `u32` | 4B | `BIGINT` | 需求累计点 |
| `level_point` | scalar | `u32` | 4B | `BIGINT` | 等级点 |
| `capture_bonus_state` | scalar | `u8` | 1B | `SMALLINT` | 占点加成状态 |
| `capture_bonus_limit` | scalar | `u32` | 4B | `BIGINT` | 占点加成上限 |

### pointdmg（线长 24B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `gaugedmg` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 量表伤害（3 点） |
| `w12_u323` | array_scalar | `u32[3]` | 12B = 3×4B | `BIGINT[]` | 量表伤害第 2 组（3×u32，线上 +12 / 内存 +12）——**宽度位置已实证、语义名待定**：与 `gaugedmg` 同处 `sub_B45760` 那一个双循环，第二趟（`v2=3`）用**同一条**存储指令写入；打印器只给整块一个 `gaugedmg={` 标签，没给这一组单独命名，故保留位置占位名。 |

### precord（线长 242B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rec_point` | scalar | `u32` | 4B | `BIGINT` | 记录点/总积分 |
| `kill_cnt` | scalar | `u32` | 4B | `BIGINT` | 击杀数 |
| `kill_wrestle_cnt` | scalar | `u32` | 4B | `BIGINT` | 格斗击杀数 |
| `kill_shot_cnt` | scalar | `u32` | 4B | `BIGINT` | 射击击杀数 |
| `kill_cannon_cnt` | scalar | `u32` | 4B | `BIGINT` | 炮击击杀数 |
| `kill_throw_cnt` | scalar | `u32` | 4B | `BIGINT` | 投掷击杀数 |
| `kill_deparms_cnt` | scalar | `u32` | 4B | `BIGINT` | 缴械击杀数 |
| `kill_assist_cnt` | scalar | `u32` | 4B | `BIGINT` | 助攻数 |
| `mapobj_killcnt` | scalar | `u32` | 4B | `BIGINT` | 地图目标破坏数 |
| `battery_killcnt` | scalar | `u32` | 4B | `BIGINT` | 炮台击破数 |
| `stronghold_killcnt` | scalar | `u32` | 4B | `BIGINT` | 据点压制数 |
| `death_cnt` | scalar | `u32` | 4B | `BIGINT` | 死亡数 |
| `search_cnt` | scalar | `u32` | 4B | `BIGINT` | 索敌数 |
| `resurrect_cnt` | scalar | `u32` | 4B | `BIGINT` | 复活数 |
| `respawn_defeat_cnt` | scalar | `u32` | 4B | `BIGINT` | 再出击(败)数 |
| `respawn_conquer_cnt` | scalar | `u32` | 4B | `BIGINT` | 再出击(胜)数 |
| `container_cnt` | scalar | `u32` | 4B | `BIGINT` | 集装箱数 |
| `protect_cnt` | scalar | `u32` | 4B | `BIGINT` | 护卫数 |
| `stgarms_set_cnt` | scalar | `u32` | 4B | `BIGINT` | 据点兵器设置数 |
| `odrcomp_pl_cnt` | scalar | `u32` | 4B | `BIGINT` | 指令完成数 |
| `move_length` | scalar | `u32` | 4B | `BIGINT` | 移动距离 |
| `stgarms_move_length` | scalar | `u32` | 4B | `BIGINT` | 据点兵器移动距离 |
| `repair_armor` | scalar | `u32` | 4B | `BIGINT` | 修理装甲量 |
| `stghold_damage` | scalar | `u32` | 4B | `BIGINT` | 据点守备伤害 |
| `btlship_damage` | scalar | `u32` | 4B | `BIGINT` | 战舰伤害 |
| `tender_damage` | scalar | `u32` | 4B | `BIGINT` | 补给舰伤害 |
| `ace_damage` | scalar | `u32` | 4B | `BIGINT` | 王牌伤害 |
| `result_gold` | scalar | `u32` | 4B | `BIGINT` | 黄金奖牌数 |
| `result_gold_score` | scalar | `u32` | 4B | `BIGINT` | 黄金奖牌分 |
| `result_gold_rank` | scalar | `u32` | 4B | `BIGINT` | 黄金奖牌排名 |
| `result_gold_dss` | scalar | `u32` | 4B | `BIGINT` | 黄金奖牌 DSS |
| `result_gold_conquer` | scalar | `u32` | 4B | `BIGINT` | 黄金奖牌征服 |
| `score_atk` | scalar | `u32` | 4B | `BIGINT` | 评分·攻击 |
| `score_spt` | scalar | `u32` | 4B | `BIGINT` | 评分·支援 |
| `score_con` | scalar | `u32` | 4B | `BIGINT` | 评分·指挥 |
| `score_total` | scalar | `u32` | 4B | `BIGINT` | 评分·合计 |
| `score_atk_max` | scalar | `u32` | 4B | `BIGINT` | 最高分·攻击 |
| `score_spt_max` | scalar | `u32` | 4B | `BIGINT` | 最高分·支援 |
| `score_con_max` | scalar | `u32` | 4B | `BIGINT` | 最高分·指挥 |
| `vsl_kill_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战击杀数 |
| `vsl_kill_wrestle_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战格斗击杀 |
| `vsl_kill_shot_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战射击击杀 |
| `vsl_kill_cannon_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战炮击击杀 |
| `vsl_kill_throw_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战投掷击杀 |
| `vsl_kill_deparms_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战缴械击杀 |
| `vsl_kill_assist_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战助攻数 |
| `vsl_death_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战死亡数 |
| `vsl_search_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战索敌数 |
| `vsl_repair_armor` | scalar | `u32` | 4B | `BIGINT` | 对战修理量 |
| `vsl_resurrect_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战复活数 |
| `vsl_td_kill_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战塔防击杀 |
| `vsl_td_death_cnt` | scalar | `u32` | 4B | `BIGINT` | 对战塔防死亡 |
| `vsl_td_score_best` | scalar | `u16` | 2B | `INTEGER` | 对战塔防最高分 |
| `vsl_td_score_total` | scalar | `u32` | 4B | `BIGINT` | 对战塔防总分 |
| `dc_victory` | scalar | `u32` | 4B | `BIGINT` | 断线胜利数 |
| `dc_kill_cnt` | scalar | `u32` | 4B | `BIGINT` | 断线击杀数 |
| `dc_death_cnt` | scalar | `u32` | 4B | `BIGINT` | 断线死亡数 |
| `ms_develop_cnt` | scalar | `u32` | 4B | `BIGINT` | 机体开发数 |
| `ms_buildup_cnt` | scalar | `u32` | 4B | `BIGINT` | 机体强化数 |
| `weapon_unlock_cnt` | scalar | `u32` | 4B | `BIGINT` | 武器解锁数 |
| `weapon_buildup_cnt` | scalar | `u32` | 4B | `BIGINT` | 武器强化数 |

### prize（线长 21B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `prize_id` | scalar | `u32` | 4B | `BIGINT` | 奖品 ID |
| `id_type` | scalar | `u32` | 4B | `BIGINT` | ID 类型 |
| `stack` | scalar | `u16` | 2B | `INTEGER` | 堆叠/数量 |
| `rare_type` | scalar | `i8` | 1B | `SMALLINT` | 稀有度类型 |
| `odds` | scalar | `u32` | 4B | `BIGINT` | 中奖概率 |
| `odds_max` | scalar | `u32` | 4B | `BIGINT` | 中奖概率上限 |
| `csv_index` | scalar | `u16` | 2B | `INTEGER` | CSV 索引 |

### progress（线长 46B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `remain_msec` | scalar | `u32` | 4B | `BIGINT` | 本局剩余时间（毫秒） |
| `coop_step` | scalar | `u32` | 4B | `BIGINT` | 协力（coop）阶段步号 |
| `A_point_now` | scalar | `u32` | 4B | `BIGINT` | A 军当前点数 |
| `B_point_now` | scalar | `u32` | 4B | `BIGINT` | B 军当前点数 |
| `A_gauge_dmg_scale` | scalar | `u16` | 2B | `INTEGER` | A 军量表伤害比例 |
| `B_gauge_dmg_scale` | scalar | `u16` | 2B | `INTEGER` | B 军量表伤害比例 |
| `coop_dead_remain` | scalar | `i8` | 1B | `SMALLINT` | 协力死亡剩余计数（打印器 movsx） |
| `is_prestart` | scalar | `i8` | 1B | `SMALLINT` | 是否处于开局前阶段（打印器 movsx） |
| `rule_status` | scalar | `u32` | 4B | `BIGINT` | 规则状态 |
| `rule_timer_msec` | scalar | `u32` | 4B | `BIGINT` | 规则计时（毫秒） |
| `rule_param1` | scalar | `u32` | 4B | `BIGINT` | 规则参数 1 |
| `rule_param2` | scalar | `u32` | 4B | `BIGINT` | 规则参数 2 |
| `A_dot_dmg` | scalar | `u32` | 4B | `BIGINT` | A 军 dot 伤害值 |
| `B_dot_dmg` | scalar | `u32` | 4B | `BIGINT` | B 军 dot 伤害值 |

### quest_info（线长 138B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `quest_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `title` | text | `char[97]` | 97B | `TEXT` | 任务标题 |
| `is_event` | scalar | `i8` | 1B | `SMALLINT` | 是否活动任务 |
| `is_known` | scalar | `i8` | 1B | `SMALLINT` | 是否已知 |
| `achieve_trigger` | scalar | `u16` | 2B | `INTEGER` | 达成触发条件 |
| `achieve_denom` | scalar | `u32` | 4B | `BIGINT` | 达成分母 |
| `achieve_num` | scalar | `u32` | 4B | `BIGINT` | 达成分子 |
| `pay_gp` | scalar | `u32` | 4B | `BIGINT` | 报酬 GP |
| `pay_exp` | scalar | `u32` | 4B | `BIGINT` | 报酬 EXP |
| `pay_item_id` | scalar | `u32` | 4B | `BIGINT` | 报酬物品 ID |
| `pay_item_num` | scalar | `u32` | 4B | `BIGINT` | 报酬物品数量 |
| `pay_msma_id` | scalar | `u32` | 4B | `BIGINT` | 报酬机体 ID |
| `pay_byword_id` | scalar | `u32` | 4B | `BIGINT` | 报酬称号 ID |
| `tail_1` | scalar | `u8` | 1B | `SMALLINT` | 线尾 1B（打印器未命名，按线序记账） |

### rank_pilot（线长 188B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rank` | scalar | `u32` | 4B | `BIGINT` | 名次 |
| `score` | scalar | `u32` | 4B | `BIGINT` | 分数 |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 驾驶员名（定长 25B） |
| `troops` | scalar | `i8` | 1B | `SMALLINT` | 势力/阵营 |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 世界 ID |
| `season_class_lv` | scalar | `u32` | 4B | `BIGINT` | 赛季阶级等级 |
| `tm_upd` | scalar | `f64` | 8B | `DOUBLE PRECISION` | 更新时间（f64 时间戳） |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构，元素 = avatar） |
| `last_score` | scalar | `u32` | 4B | `BIGINT` | 上次分数 |
| `msdeck` | array_struct | `msdeck_entry[2]` | 72B = 2×36B | `--` | 编成机体槽（2 项，元素 = msdeck_entry；打印器 `msdeck={` 后跟分隔再一份） |
| `last_rank` | scalar | `u32` | 4B | `BIGINT` | 上次名次 |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名（定长 31B） |
| `emb_base` | scalar | `i8` | 1B | `SMALLINT` | 徽章底图 |
| `emb_parts1` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `i8` | 1B | `SMALLINT` | 徽章部件 2 |
| `is_regular` | scalar | `i8` | 1B | `SMALLINT` | 是否正规（打印器标签 `is_regular=`；语义待业务核） |
| `is_reserve` | scalar | `i8` | 1B | `SMALLINT` | 是否预备（打印器标签 `is_reserve=`；语义待业务核） |

### rank_pilot_light（线长 73B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `score` | scalar | `u32` | 4B | `BIGINT` | 分数 |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 驾驶员名（定长 25B） |
| `troops` | scalar | `i8` | 1B | `SMALLINT` | 势力/阵营 |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 世界 ID |
| `season_class_lv` | scalar | `u32` | 4B | `BIGINT` | 赛季阶级等级 |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 战队名（定长 31B） |

### ranking（线长 95B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称（定长 25 字节） |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 公会 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 公会名称（定长 31 字节） |
| `emb_base` | scalar | `u8` | 1B | `SMALLINT` | 徽章底图 |
| `emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 徽章部件 2 |
| `score` | scalar | `u32` | 4B | `BIGINT` | 分数 |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |

### ranking_info（线长 10B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `kind` | scalar | `u16` | 2B | `INTEGER` | 排序/筛选种类 |
| `term` | scalar | `u16` | 2B | `INTEGER` | 统计期间 |
| `filter` | scalar | `u16` | 2B | `INTEGER` | 筛选条件 |
| `reason` | scalar | `u16` | 2B | `INTEGER` | 原因/依据 |
| `troops` | scalar | `u16` | 2B | `INTEGER` | 势力/阵营 |

### rankself（线长 40B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `score_now` | scalar | `u32` | 4B | `BIGINT` | 当前分数 |
| `entry_until` | scalar | `u16` | 2B | `INTEGER` | 报名截止期 |
| `highscores` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 历史高分（7×u16） |
| `entry_until_es` | scalar | `u16` | 2B | `INTEGER` | 报名截止期（ES） |
| `eventscores` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 活动分数（7×u16） |

### recruit（线长 80B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `channel_id` | scalar | `u32` | 4B | `BIGINT` | 频道 ID |
| `party_id` | scalar | `u32` | 4B | `BIGINT` | 队伍 ID |
| `troops` | scalar | `i8` | 1B | `SMALLINT` | 势力 |
| `member_count` | scalar | `u16` | 2B | `INTEGER` | 队伍人数 |
| `comment` | text | `bytes[61]` | 61B | `TEXT` | 招募留言（定长 61B） |
| `pstat` | scalar | `i8` | 1B | `SMALLINT` | 队伍状态 |
| `is_lock` | scalar | `i8` | 1B | `SMALLINT` | 是否上锁 |
| `remain_minutes` | scalar | `u16` | 2B | `INTEGER` | 剩余分钟数（线上 +74 / 内存 +76）——★ 2026-09-25 定名（原名 `w74_u16` 是位置占位符）。三条独立证据把语义取死：① **同一读取器**：IDA 复看 `sub_B45400`，本字段的取值就是 `0xB454A3 push eax(edi+4Ch); 0xB454A4 call sub_B02DF0`，而列表项 `recruits` 用的是**同一个函数同一个取值点**（`reader: sub_B45400`，VA 亦为 `0xB454A4`），`recruits` 在该偏移已命名为 `remain_minutes`；② **旧库列注释**：live `game.recruits.remain_minutes` 的注释逐字为「剩余分钟数 [u16] SC-0xB43F-lounge-party_recruit_list_get_r@0xB454A4」——与 ① 的 VA 相同；③ **第三条命令同形**：`SC-0x1E49-party_enter_r` 的队伍体在 comment 之后同样是 u16 → u32 的尾对，`composites/party.json` 已把 u16 命名为 `remain_minutes`。⇒ 把占位名改成与 `recruits`/`party` 同名（同一字段三个命令口径一致）。 |
| `party_type` | scalar | `u32` | 4B | `BIGINT` | 队伍类型（线上 +76 / 内存 +80）——★ 2026-09-25 定名（原名 `w76_u32` 是位置占位符），判据同 `remain_minutes`：① IDA `sub_B45400` 在此处 `push edi+50h; call sub_B02DD0`（u32 原语）；② live `game.recruits.party_type` 的注释是「队伍类型 [u32] SC-0xB43F@0xB454BE」，而同一读取器里 u32 的 call 点就是 `0xB454BE`（本复合体原先记的 `0xB454C9` 是 call 之后的 `setnz al`，属**记错一位**，本次一并改正）；③ `CS-0x645D-party_create` / `CS-0x9226-party_info_edit` 都送 `party_type`，`CS-0x0A73-party_recruit_list_get` 还按它过滤列表 ⇒ 它是队伍自身的属性。 |

### recruits（线长 80B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `channel_id` | scalar | `u32` | 4B | `BIGINT` | 频道 ID |
| `party_id` | scalar | `u32` | 4B | `BIGINT` | 队伍 ID |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 部队/阵营 |
| `member_count` | scalar | `u16` | 2B | `INTEGER` | 成员数量 |
| `comment` | text | `char[61]` | 61B | `TEXT` | 招募说明（定长 61 字节） |
| `pstat` | scalar | `u8` | 1B | `SMALLINT` | 机师状态 |
| `is_lock` | scalar | `u8` | 1B | `SMALLINT` | 是否锁定 |
| `remain_minutes` | scalar | `u16` | 2B | `INTEGER` | 剩余分钟数 |
| `party_type` | scalar | `u32` | 4B | `BIGINT` | 队伍类型 |

### rental_module（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `module_id` | scalar | `u32` | 4B | `BIGINT` | 模块 ID |
| `count` | scalar | `u32` | 4B | `BIGINT` | 数量 |

### replay_info（线长 38B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u64` | 8B | `BIGINT` | 录像 ID |
| `missionId` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `time` | scalar | `u32` | 4B | `BIGINT` | 时间戳 |
| `troopsA` | scalar | `u8` | 1B | `SMALLINT` | A 方势力 |
| `troopsB` | scalar | `u8` | 1B | `SMALLINT` | B 方势力 |
| `endDate` | scalar | `u32` | 4B | `BIGINT` | 结束日期 |
| `top_pilot_id_troopsA` | scalar | `u32` | 4B | `BIGINT` | A 方最高分机师 ID |
| `top_world_id_troopsA` | scalar | `u32` | 4B | `BIGINT` | A 方最高分世界 ID |
| `top_pilot_id_troopsB` | scalar | `u32` | 4B | `BIGINT` | B 方最高分机师 ID |
| `top_world_id_troopsB` | scalar | `u32` | 4B | `BIGINT` | B 方最高分世界 ID |

### respawn_post（线长 25B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `team` | scalar | `u16` | 2B | `INTEGER` | 势力 |
| `troops` | scalar | `u16` | 2B | `INTEGER` | 兵力 |
| `gauge_A` | scalar | `u32` | 4B | `BIGINT` | A 计量 |
| `gauge_B` | scalar | `u32` | 4B | `BIGINT` | B 计量 |
| `is_visible` | scalar | `i8` | 1B | `SMALLINT` | 是否可见 |
| `is_lock` | scalar | `i8` | 1B | `SMALLINT` | 是否锁定 |
| `is_keep` | scalar | `i8` | 1B | `SMALLINT` | 是否保持 |
| `near_ms_num` | opaque | `u8[2]` | 2B | `BYTEA` | 附近机体数（2 元） |
| `conquer_remain_sec` | scalar | `f64` | 8B | `DOUBLE PRECISION` | 占领剩余秒 |

### respawn_post_entry（线长 58B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `type` | scalar | `u32` | 4B | `BIGINT` | 重生点类型 |
| `ini_team` | scalar | `u16` | 2B | `INTEGER` | 初始势力 |
| `ini_troops` | scalar | `u16` | 2B | `INTEGER` | 初始兵力 |
| `name` | text | `char[13]` | 13B | `TEXT` | 重生点名 |
| `gauge_max` | scalar | `u32` | 4B | `BIGINT` | 计量上限 |
| `post_chara_id` | scalar | `u32` | 4B | `BIGINT` | 开局本地创建路径使用的 CHARA_PARAM 定义表键；本地实例身份另行分配 |
| `pos_x` | scalar | `u16` | 2B | `INTEGER` | X 坐标 |
| `pos_y` | scalar | `u16` | 2B | `INTEGER` | Y 坐标 |
| `pos_z` | scalar | `u16` | 2B | `INTEGER` | Z 坐标 |
| `dir` | scalar | `u16` | 2B | `INTEGER` | 朝向 |
| `cmdr_sptype` | scalar | `i8` | 1B | `SMALLINT` | 指挥官支援类型 |
| `group_id` | scalar | `u32` | 4B | `BIGINT` | 组 ID |
| `npc_ba_point_ent_id` | scalar | `u32` | 4B | `BIGINT` | NPC 据点实体 ID |
| `npc_ba_point_move_range_abs_x` | scalar | `u32` | 4B | `BIGINT` | NPC 据点移动范围 |
| `param1` | scalar | `u32` | 4B | `BIGINT` | 参数 1 |
| `param2` | scalar | `u32` | 4B | `BIGINT` | 参数 2 |

### result_detail（线长 555B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `teamside` | scalar | `u8` | 1B | `SMALLINT` | 所属阵营（内存按 u32 打印） |
| `exp` | scalar | `u32` | 4B | `BIGINT` | 获得经验 |
| `money` | scalar | `u32` | 4B | `BIGINT` | 获得金钱 |
| `tp` | scalar | `u32` | 4B | `BIGINT` | 获得 TP |
| `cmdr_fame` | scalar | `u32` | 4B | `BIGINT` | 司令功勋 |
| `victory_fame` | scalar | `u32` | 4B | `BIGINT` | 胜利功勋 |
| `victory_score` | scalar | `u32` | 4B | `BIGINT` | 胜利分数 |
| `alloy_chip` | scalar | `u32` | 4B | `BIGINT` | 合金碎片 |
| `rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 本地对战加成率 |
| `rate_vslocal_4ev` | scalar | `u16` | 2B | `INTEGER` | 本地对战加成率（4ev） |
| `lv_point_self` | scalar | `u16` | 2B | `INTEGER` | 自身等级点 |
| `lv_point_team` | scalar | `u16` | 2B | `INTEGER` | 队伍等级点 |
| `over_custom_exp` | scalar | `u16` | 2B | `INTEGER` | 超限自定义经验 |
| `rate_vslocal_clan` | scalar | `u16` | 2B | `INTEGER` | 战队本地对战加成率 |
| `rate_vslocal_clan_total` | scalar | `u16` | 2B | `INTEGER` | 战队本地对战加成率（累计） |
| `cnt_kill` | scalar | `u8` | 1B | `SMALLINT` | 击杀数 |
| `cnt_death` | scalar | `u8` | 1B | `SMALLINT` | 阵亡数 |
| `cnt_assist` | scalar | `u8` | 1B | `SMALLINT` | 助攻数 |
| `cnt_resurrect` | scalar | `u8` | 1B | `SMALLINT` | 复活数 |
| `cnt_search` | scalar | `u16` | 2B | `INTEGER` | 搜索次数 |
| `cnt_repair` | scalar | `u32` | 4B | `BIGINT` | 修理次数 |
| `openable_num_win_bonus` | scalar | `u8` | 1B | `SMALLINT` | 可开启宝箱数（胜利加成） |
| `openable_num_member_bonus` | scalar | `u8` | 1B | `SMALLINT` | 可开启宝箱数（成员加成） |
| `openable_num_bc_bonus` | scalar | `u8` | 1B | `SMALLINT` | 可开启宝箱数（BC 加成） |
| `openable_num_event_bonus` | scalar | `u8` | 1B | `SMALLINT` | 可开启宝箱数（活动加成） |
| `expup_campaign` | scalar | `u16` | 2B | `INTEGER` | 经验加成（活动） |
| `expup_bc` | scalar | `u16` | 2B | `INTEGER` | 经验加成（BC） |
| `expup_fgauge` | scalar | `u16` | 2B | `INTEGER` | 经验加成（FGauge） |
| `moneyup_campaign` | scalar | `u16` | 2B | `INTEGER` | 金钱加成（活动） |
| `moneyup_bc` | scalar | `u16` | 2B | `INTEGER` | 金钱加成（BC） |
| `moneyup_event` | scalar | `u16` | 2B | `INTEGER` | 金钱加成（事件） |
| `moneyup_win` | scalar | `u16` | 2B | `INTEGER` | 金钱加成（胜利） |
| `accumpup_event` | scalar | `u16` | 2B | `INTEGER` | 累积加成（事件） |
| `buffnum` | scalar | `u8` | 1B | `SMALLINT` | BUFF 数量 |
| `result_spbits` | scalar | `u8` | 1B | `SMALLINT` | 结算特殊位 |
| `enemy_avg_lv` | scalar | `u8` | 1B | `SMALLINT` | 敌方平均等级 |
| `enemy_avg_rate` | scalar | `u16` | 2B | `INTEGER` | 敌方平均加成率 |
| `avg_lv_diff` | scalar | `u32` | 4B | `BIGINT` | 平均等级差 |
| `overplay_rate` | scalar | `u8` | 1B | `SMALLINT` | 过量游玩率 |
| `itm_id` | array_scalar | `u32[8]` | 32B = 8×4B | `BIGINT[]` | 获得道具 ID（8 项） |
| `itm_num` | scalar | `u8` | 1B | `SMALLINT` | 获得道具数量 |
| `use_buffitem_id` | array_scalar | `u32[14]` | 56B = 14×4B | `BIGINT[]` | 使用 BUFF 道具 ID（14 项） |
| `use_buffitem_num` | scalar | `u8` | 1B | `SMALLINT` | 使用 BUFF 道具数量 |
| `fight_ms_uniqid` | array_scalar | `u64[5]` | 40B = 5×8B | `BIGINT[]` | 参战机体唯一 ID（5 项） |
| `fight_ms_score` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体分数（5 项） |
| `fight_ms_score_atk` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体攻击分（5 项） |
| `fight_ms_score_spt` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体支援分（5 项） |
| `fight_ms_score_con` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体贡献分（5 项） |
| `fight_ms_kill_cnt` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体击杀数（5 项） |
| `fight_ms_assist_cnt` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体助攻数（5 项） |
| `fight_ms_resurrect_cnt` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体复活数（5 项） |
| `fight_ms_stghold_damage` | array_scalar | `u32[5]` | 20B = 5×4B | `BIGINT[]` | 参战机体据点伤害（5 项） |
| `fight_ms_num` | scalar | `u8` | 1B | `SMALLINT` | 参战机体数 |
| `no_fight_ms_uniqid` | array_scalar | `u64[5]` | 40B = 5×8B | `BIGINT[]` | 未参战机体唯一 ID（5 项） |
| `no_fight_ms_num` | scalar | `u8` | 1B | `SMALLINT` | 未参战机体数 |
| `badge_bits` | array_scalar | `u64[3]` | 24B = 3×8B | `BIGINT[]` | 徽章位（3 项） |
| `badge_score` | scalar | `u8` | 1B | `SMALLINT` | 徽章分数 |
| `badge_result` | scalar | `u8` | 1B | `SMALLINT` | 徽章结果 |
| `badge_rankmember` | scalar | `u8` | 1B | `SMALLINT` | 徽章排行成员 |
| `badge_deadcnt` | scalar | `u8` | 1B | `SMALLINT` | 徽章阵亡计数 |
| `badge_cleartime` | scalar | `u8` | 1B | `SMALLINT` | 徽章通关时间 |
| `badge_cmdr` | scalar | `u8` | 1B | `SMALLINT` | 徽章司令 |
| `badge_cmdr2` | scalar | `u8` | 1B | `SMALLINT` | 徽章司令2 |
| `team_pilot_rate_adjusted_level` | scalar | `u32` | 4B | `BIGINT` | 队伍飞行员等级修正率 |
| `contribute_rank` | scalar | `u32` | 4B | `BIGINT` | 贡献排名 |
| `dtf_score_rate` | scalar | `u8` | 1B | `SMALLINT` | DTF 分数率 |
| `conquer_rate` | scalar | `u8` | 1B | `SMALLINT` | 占领率 |
| `elapsed_sec` | scalar | `u32` | 4B | `BIGINT` | 耗时（秒） |
| `accump_inc` | scalar | `u32` | 4B | `BIGINT` | 累积增量 |
| `spc_bonus_item_ids` | array_scalar | `u32[8]` | 32B = 8×4B | `BIGINT[]` | 特殊奖励道具 ID（8 项） |
| `spc_bonus_item_nums` | array_scalar | `u32[8]` | 32B = 8×4B | `BIGINT[]` | 特殊奖励道具数量（8 项） |
| `bef_cupteam_rate` | scalar | `u16` | 2B | `INTEGER` | 变更前 CupTeam 加成率 |
| `cupteam_rate_delta` | scalar | `u16` | 2B | `INTEGER` | CupTeam 加成率增量 |
| `enemy_cupteam_rate` | scalar | `u16` | 2B | `INTEGER` | 敌方 CupTeam 加成率 |
| `rokaku_pt` | scalar | `u32` | 4B | `BIGINT` | 络格点数 |
| `rokaku_pt_reason` | scalar | `u32` | 4B | `BIGINT` | 络格点数原因 |
| `examination_playsec_elapsed` | scalar | `u32` | 4B | `BIGINT` | 考核游玩耗时 |
| `examination_playscore` | scalar | `u32` | 4B | `BIGINT` | 考核游玩分数 |
| `special_contributed_point` | scalar | `u32` | 4B | `BIGINT` | 特殊贡献点 |
| `is_periodpath` | scalar | `u8` | 1B | `SMALLINT` | 是否周期路线 |

### result_wave（线长 20B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `wave_rank` | scalar | `u8` | 1B | `SMALLINT` | 波段评价 |
| `cleartime_sec` | scalar | `u32` | 4B | `BIGINT` | 通关用时（秒） |
| `cleartime_rank` | scalar | `u8` | 1B | `SMALLINT` | 通关用时评价 |
| `container_num` | scalar | `u16` | 2B | `INTEGER` | 集装箱取得数 |
| `container_max` | scalar | `u16` | 2B | `INTEGER` | 集装箱总数 |
| `container_rank` | scalar | `u8` | 1B | `SMALLINT` | 集装箱评价 |
| `enemybase_num` | scalar | `u16` | 2B | `INTEGER` | 敌方据点破坏数 |
| `enemybase_max` | scalar | `u16` | 2B | `INTEGER` | 敌方据点总数 |
| `enemybase_rank` | scalar | `u8` | 1B | `SMALLINT` | 敌方据点评价 |
| `total_score` | scalar | `u32` | 4B | `BIGINT` | 波段总得分 |

### rokaku_node_entry（线长 60B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `val_00` | scalar | `u32` | 4B | `BIGINT` | 线序成员 1（打印器未命名） |
| `val_04` | scalar | `u32` | 4B | `BIGINT` | 线序成员 2（打印器未命名） |
| `val_08` | scalar | `u32` | 4B | `BIGINT` | 线序成员 3（打印器未命名） |
| `val_0c` | scalar | `u32` | 4B | `BIGINT` | 线序成员 4（打印器未命名） |
| `val_10` | scalar | `u32` | 4B | `BIGINT` | 线序成员 5（打印器未命名） |
| `val_14` | scalar | `u32` | 4B | `BIGINT` | 线序成员 6（打印器未命名） |
| `val_18` | scalar | `u32` | 4B | `BIGINT` | 线序成员 7（打印器未命名） |
| `val_1c` | scalar | `u32` | 4B | `BIGINT` | 线序成员 8（打印器未命名） |
| `val_20` | scalar | `u32` | 4B | `BIGINT` | 线序成员 9（打印器未命名） |
| `val_24` | scalar | `u32` | 4B | `BIGINT` | 线序成员 10（打印器未命名） |
| `val_28_u64` | scalar | `u64` | 8B | `BIGINT` | 线序成员 11（u64，打印器未命名） |
| `val_30` | scalar | `u32` | 4B | `BIGINT` | 线序成员 12（打印器未命名） |
| `val_34` | scalar | `u32` | 4B | `BIGINT` | 线序成员 13（打印器未命名） |
| `val_38` | scalar | `u32` | 4B | `BIGINT` | 线序成员 14（打印器未命名） |

### roominfo（线长 135B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `room_id` | scalar | `u32` | 4B | `BIGINT` | 房间 ID |
| `room_name` | text | `bytes[73]` | 73B | `TEXT` | 房间名（定长 73B） |
| `room_type` | scalar | `u32` | 4B | `BIGINT` | 房间类型 |
| `room_stat` | scalar | `i8` | 1B | `SMALLINT` | 房间状态 |
| `play_elapsed` | scalar | `u32` | 4B | `BIGINT` | 已进行时间（秒） |
| `mission_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `extrule_id` | scalar | `u32` | 4B | `BIGINT` | 扩展规则 ID |
| `is_lock` | scalar | `i8` | 1B | `SMALLINT` | 是否上锁 |
| `is_vsclan` | scalar | `i8` | 1B | `SMALLINT` | 是否部队对战房间 |
| `count_eff` | scalar | `u16` | 2B | `INTEGER` | 联邦侧人数 |
| `count_zeon` | scalar | `u16` | 2B | `INTEGER` | 吉翁侧人数 |
| `count_max` | scalar | `u16` | 2B | `INTEGER` | 房间人数上限 |
| `master_pilotid` | scalar | `u32` | 4B | `BIGINT` | 房主 pilot ID |
| `master_worldid` | scalar | `u32` | 4B | `BIGINT` | 房主 world ID |
| `master_name` | text | `bytes[25]` | 25B | `TEXT` | 房主名称（定长 25B） |

### score_ranking（线长 61B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 世界 ID |
| `is_cmdr` | scalar | `i8` | 1B | `SMALLINT` | 是否指挥官 |
| `is_xbnpc` | scalar | `i8` | 1B | `SMALLINT` | 是否 XB NPC |
| `rank` | scalar | `u16` | 2B | `INTEGER` | 名次 |
| `totalpoint` | scalar | `u32` | 4B | `BIGINT` | 总分 |
| `stghold_dmg` | scalar | `u32` | 4B | `BIGINT` | 据点伤害 |
| `kill_cnt` | scalar | `u16` | 2B | `INTEGER` | 击破数 |
| `atk_point` | scalar | `u32` | 4B | `BIGINT` | 攻击分 |
| `spt_point` | scalar | `u32` | 4B | `BIGINT` | 支援分 |
| `con_point` | scalar | `u32` | 4B | `BIGINT` | 贡献分 |
| `victory_score` | scalar | `u32` | 4B | `BIGINT` | 胜利分 |
| `ranking_point` | scalar | `u32` | 4B | `BIGINT` | 排行分 |
| `last_msma` | scalar | `u32` | 4B | `BIGINT` | 最后机体 ID |
| `last_weapon` | scalar | `u32` | 4B | `BIGINT` | 最后武器 ID |
| `last_shield` | scalar | `u32` | 4B | `BIGINT` | 最后护盾 ID |
| `last_decal` | scalar | `u32` | 4B | `BIGINT` | 最后涂装 ID |
| `last_mscolor` | scalar | `i8` | 1B | `SMALLINT` | 最后机体配色 |
| `add_rate_vslocal` | scalar | `u16` | 2B | `INTEGER` | 本地加成率 |

### season_rb_conf（线长 52B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `state` | scalar | `u32` | 4B | `BIGINT` | 赛季状态 |
| `tournament_id` | scalar | `u32` | 4B | `BIGINT` | 锦标赛 ID |
| `mode` | scalar | `u32` | 4B | `BIGINT` | 模式 |
| `open_date` | scalar | `u32` | 4B | `BIGINT` | 开放日期 |
| `booking_start` | scalar | `u32` | 4B | `BIGINT` | 预约开始 |
| `booking_end` | scalar | `u32` | 4B | `BIGINT` | 预约结束 |
| `mission_id` | scalar | `u32` | 4B | `BIGINT` | 任务 ID |
| `mission_id_dm` | array_scalar | `u32[4]` | 16B = 4×4B | `BIGINT[]` | 死亡竞赛任务 ID（4 元） |
| `is_end` | scalar | `u32` | 4B | `BIGINT` | 是否已结束 |
| `is_debug` | scalar | `u32` | 4B | `BIGINT` | 调试标志 |

### snapshot（线长 39B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `ent_id` | scalar | `u16` | 2B | `INTEGER` | 实体 ID |
| `pos_x` | scalar | `u16` | 2B | `INTEGER` | 位置 X |
| `pos_y` | scalar | `u16` | 2B | `INTEGER` | 位置 Y |
| `pos_z` | scalar | `u16` | 2B | `INTEGER` | 位置 Z |
| `dir` | scalar | `u16` | 2B | `INTEGER` | 朝向 |
| `target_x` | scalar | `u16` | 2B | `INTEGER` | 目标 X |
| `target_y` | scalar | `u16` | 2B | `INTEGER` | 目标 Y |
| `target_z` | scalar | `u16` | 2B | `INTEGER` | 目标 Z |
| `score1` | scalar | `u16` | 2B | `INTEGER` | 得分 1 |
| `score2` | scalar | `u16` | 2B | `INTEGER` | 得分 2 |
| `score3` | scalar | `u16` | 2B | `INTEGER` | 得分 3 |
| `hp_percent` | scalar | `u8` | 1B | `SMALLINT` | HP 百分比 |
| `hp_percent_shield` | scalar | `u8` | 1B | `SMALLINT` | 盾 HP 百分比 |
| `down_power` | scalar | `u16` | 2B | `INTEGER` | DOWN 力量 |
| `equip_index` | scalar | `u8` | 1B | `SMALLINT` | 装备索引 |
| `water_index` | scalar | `u8` | 1B | `SMALLINT` | 水域索引 |
| `layer_index` | scalar | `u8` | 1B | `SMALLINT` | 层索引 |
| `rideon_ent_id` | scalar | `u16` | 2B | `INTEGER` | 搭乘实体 ID |
| `lockon_ent_id` | scalar | `u16` | 2B | `INTEGER` | 锁定实体 ID |
| `special_bits` | scalar | `u32` | 4B | `BIGINT` | 特殊状态位 |
| `special_bits2` | scalar | `u16` | 2B | `INTEGER` | 特殊状态位 2 |

### sort_info（线长 18B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `filter_type` | scalar | `u16` | 2B | `INTEGER` | 筛选类型 |
| `lv_under` | scalar | `u8` | 1B | `SMALLINT` | 等级下限 |
| `lv_upper` | scalar | `u8` | 1B | `SMALLINT` | 等级上限 |
| `member_under` | scalar | `u8` | 1B | `SMALLINT` | 成员数下限 |
| `member_upper` | scalar | `u8` | 1B | `SMALLINT` | 成员数上限 |
| `rokaku_under` | scalar | `u8` | 1B | `SMALLINT` | 落格下限 |
| `rokaku_upper` | scalar | `u8` | 1B | `SMALLINT` | 落格上限 |
| `ranking_under` | scalar | `u16` | 2B | `INTEGER` | 排名下限 |
| `ranking_upper` | scalar | `u16` | 2B | `INTEGER` | 排名上限 |
| `recruit_value` | scalar | `u8` | 1B | `SMALLINT` | 招募条件值 |
| `time_value` | scalar | `u32` | 4B | `BIGINT` | 时间条件值 |
| `style_value` | scalar | `u8` | 1B | `SMALLINT` | 风格条件值 |

### sort_info_invite（线长 9B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `filter_type` | scalar | `u8` | 1B | `SMALLINT` | 筛选类型（本形为 u8；18B 形为 u16） |
| `lv_under` | scalar | `u8` | 1B | `SMALLINT` | 等级下限 |
| `lv_upper` | scalar | `u8` | 1B | `SMALLINT` | 等级上限 |
| `member_under` | scalar | `u8` | 1B | `SMALLINT` | 成员数下限 |
| `member_upper` | scalar | `u8` | 1B | `SMALLINT` | 成员数上限 |
| `rokaku_under` | scalar | `u8` | 1B | `SMALLINT` | 落格下限 |
| `rokaku_upper` | scalar | `u8` | 1B | `SMALLINT` | 落格上限 |
| `recruit_value` | scalar | `u8` | 1B | `SMALLINT` | 招募条件值 |
| `style_value` | scalar | `u8` | 1B | `SMALLINT` | 风格条件值 |

### special_a_info（线长 40B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `score_now` | scalar | `u32` | 4B | `BIGINT` | 当前分数 |
| `entry_until` | scalar | `u16` | 2B | `INTEGER` | 报名截止期 |
| `highscores` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 历史高分（7×u16） |
| `entry_until_es` | scalar | `u16` | 2B | `INTEGER` | 报名截止期（ES） |
| `eventscores` | array_scalar | `u16[7]` | 14B = 7×2B | `INTEGER[]` | 活动分数（7×u16） |

### special_a_next（线长 12B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `point` | scalar | `u32` | 4B | `BIGINT` | 积分/点数 |
| `item_id` | scalar | `u32` | 4B | `BIGINT` | 道具 ID |
| `item_num` | scalar | `u32` | 4B | `BIGINT` | 道具数量 |

### srch_res（线长 114B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w00_u32 |
| `emb_base` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w04_u8 |
| `emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w05_u8 |
| `emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w06_u8 |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w07_char31 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w38_u8 |
| `offer_body` | text | `char[31]` | 31B | `TEXT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w39_char31 |
| `leader_name` | text | `char[25]` | 25B | `TEXT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w70_char25 |
| `member_num` | scalar | `u32` | 4B | `BIGINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w95_u32 |
| `member_max` | scalar | `u32` | 4B | `BIGINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w99_u32 |
| `offer_is_active` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w103_u8 |
| `clan_kind` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w104_u8 |
| `active_time_bits` | scalar | `u32` | 4B | `BIGINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w105_u32 |
| `play_style` | scalar | `u8` | 1B | `SMALLINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w109_u8 |
| `capture_unlock_num` | scalar | `u32` | 4B | `BIGINT` | 同 `clan_search_hit`（同读取器 sub_B45BA0 同一偏移）；原名 w110_u32 |

### support_spot（线长 37B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `team` | scalar | `u16` | 2B | `INTEGER` | 所属队伍 |
| `troops` | scalar | `u16` | 2B | `INTEGER` | 兵力 |
| `type` | scalar | `u32` | 4B | `BIGINT` | 地点类型 |
| `stat` | scalar | `u32` | 4B | `BIGINT` | 状态 |
| `is_lock` | scalar | `i8` | 1B | `SMALLINT` | 是否锁定 |
| `pos_x` | scalar | `u32` | 4B | `BIGINT` | X 坐标 |
| `pos_y` | scalar | `u32` | 4B | `BIGINT` | Y 坐标 |
| `pos_z` | scalar | `u32` | 4B | `BIGINT` | Z 坐标 |
| `dir` | scalar | `u32` | 4B | `BIGINT` | 朝向 |
| `route_no` | scalar | `u32` | 4B | `BIGINT` | 路线编号 |
| `ai_priority` | scalar | `u32` | 4B | `BIGINT` | AI 优先级 |

### team_pilot（线长 55B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 驾驶员 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 驾驶员名 |
| `level` | scalar | `u32` | 4B | `BIGINT` | 等级 |
| `world_id` | scalar | `u32` | 4B | `BIGINT` | 世界 ID |
| `avatar` | opaque | `avatar(18B)` | 18B | `BYTEA` | 头像（18B 线 / 24B 槽） |

### toppilots（线长 95B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `rank` | scalar | `u32` | 4B | `BIGINT` | 排名 |
| `pilot_id` | scalar | `u32` | 4B | `BIGINT` | 机师 ID |
| `name` | text | `char[25]` | 25B | `TEXT` | 名称（定长 25 字节） |
| `troops` | scalar | `u8` | 1B | `SMALLINT` | 势力/阵营 |
| `level` | scalar | `u8` | 1B | `SMALLINT` | 等级 |
| `clan_id` | scalar | `u32` | 4B | `BIGINT` | 公会 ID |
| `clan_name` | text | `char[31]` | 31B | `TEXT` | 公会名称（定长 31 字节） |
| `emb_base` | scalar | `u8` | 1B | `SMALLINT` | 徽章底图 |
| `emb_parts1` | scalar | `u8` | 1B | `SMALLINT` | 徽章部件 1 |
| `emb_parts2` | scalar | `u8` | 1B | `SMALLINT` | 徽章部件 2 |
| `score` | scalar | `u32` | 4B | `BIGINT` | 分数 |
| `avatar` | struct | `avatar` | 18B → avatar | `` | 外观（18B 子结构） |

### total_result_wave（线长 19B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `end_wave` | scalar | `u8` | 1B | `SMALLINT` | 结束波次 |
| `result_coop` | scalar | `u8` | 1B | `SMALLINT` | 协作结果 |
| `rank` | scalar | `u8` | 1B | `SMALLINT` | 排名 |
| `rank_score` | scalar | `u32` | 4B | `BIGINT` | 排名分 |
| `container_comp` | scalar | `u32` | 4B | `BIGINT` | 集装箱完成 |
| `enemyobj_comp` | scalar | `u32` | 4B | `BIGINT` | 敌方目标完成 |
| `total_score` | scalar | `u32` | 4B | `BIGINT` | 总分 |

### trchallenge_info（线长 13B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `id` | scalar | `u32` | 4B | `BIGINT` | 条目 ID |
| `val` | scalar | `u32` | 4B | `BIGINT` | 进度值 |
| `sub_val` | scalar | `u32` | 4B | `BIGINT` | 子进度值 |
| `is_clear` | scalar | `i8` | 1B | `SMALLINT` | 是否已通关（打印器 movsx） |

### unlocked_navi（线长 8B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `navi_id` | scalar | `u32` | 4B | `BIGINT` | 导航 ID |
| `status` | scalar | `u32` | 4B | `BIGINT` | 解锁状态 |

### unlockw（线长 30B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `item_id` | scalar | `u32` | 4B | `BIGINT` | 道具/武器 ID |
| `db_index` | scalar | `u16` | 2B | `INTEGER` | 数据库索引 |
| `buildup_cnt` | scalar | `u16` | 2B | `INTEGER` | 强化次数 |
| `buildup_val` | array_scalar | `u16[10]` | 20B = 10×2B | `INTEGER[]` | 强化值（10×u16） |
| `spticket_success_wp` | scalar | `u8` | 1B | `SMALLINT` | 特殊票成功武器点 |
| `spticket_greatest_wp` | scalar | `u8` | 1B | `SMALLINT` | 特殊票最大武器点 |

### wave_res（线长 34B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `wave` | scalar | `u8` | 1B | `SMALLINT` | 波次编号 |
| `wave_rank` | scalar | `u8` | 1B | `SMALLINT` | 波次评级 |
| `result_coop` | scalar | `u8` | 1B | `SMALLINT` | 协同结果码 |
| `cleartime_sec` | scalar | `u32` | 4B | `BIGINT` | 通关用时（秒） |
| `cleartime_rank` | scalar | `u8` | 1B | `SMALLINT` | 通关时间评级 |
| `cleartime_score` | scalar | `u32` | 4B | `BIGINT` | 通关时间得分 |
| `container_num` | scalar | `u16` | 2B | `INTEGER` | 容器达成数 |
| `container_max` | scalar | `u16` | 2B | `INTEGER` | 容器目标数 |
| `container_rank` | scalar | `u8` | 1B | `SMALLINT` | 容器任务评级 |
| `container_score` | scalar | `u32` | 4B | `BIGINT` | 容器任务得分 |
| `enemybase_num` | scalar | `u16` | 2B | `INTEGER` | 敌基地击破数 |
| `enemybase_max` | scalar | `u16` | 2B | `INTEGER` | 敌基地目标数 |
| `enemybase_rank` | scalar | `u8` | 1B | `SMALLINT` | 敌基地任务评级 |
| `enemybase_score` | scalar | `u32` | 4B | `BIGINT` | 敌基地任务得分 |
| `total_score` | scalar | `u32` | 4B | `BIGINT` | 总得分 |

### wbonus（线长 4B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `lv` | scalar | `i8` | 1B | `SMALLINT` | 等级加成 |
| `openbox` | scalar | `i8` | 1B | `SMALLINT` | 开箱加成 |
| `gp_rate` | scalar | `u16` | 2B | `INTEGER` | GP 倍率 |

### world_entry（线长 309B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `worldid` | scalar | `u32` | 4B | `BIGINT` | 世界 ID |
| `name` | text | `char[49]` | 49B | `TEXT` | 世界名 |
| `name_en` | text | `char[49]` | 49B | `TEXT` | 世界名（英文） |
| `desc` | text | `char[193]` | 193B | `TEXT` | 世界说明 |
| `stat` | scalar | `u32` | 4B | `BIGINT` | 世界状态 |
| `icon_id` | scalar | `u16` | 2B | `INTEGER` | 图标 ID |
| `client_now` | scalar | `u32` | 4B | `BIGINT` | 客户端当前值 |
| `client_max` | scalar | `u32` | 4B | `BIGINT` | 客户端上限 |

### xwar_ext_rule（线长 514B）

| 成员 | shape | 线型 | 长 | 落库 | 说明 |
|---|---|---|---|---|---|
| `extra_rule` | scalar | `u16` | 2B | `INTEGER` | 扩展规则 ID |
| `param` | scalar | `u32` | 4B | `BIGINT` | 主参数（行 0 槽首 u32） |
| `row0` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 0（31×u32） |
| `row1` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 1（31×u32） |
| `row2` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 2（31×u32） |
| `row3` | array_scalar | `u32[31]` | 124B = 31×4B | `BIGINT[]` | 参数行 3（31×u32） |
| `w502_bytes` | opaque | `bytes[12]` | 12B | `BYTEA` | 12B 定长字段（原登记为 padding，reader 实测写入 3 次；粒度不判定） |
