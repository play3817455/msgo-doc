# 字段归位 · 未决清单

> 由 `tools/derive_homing.py` 生成。**只列引擎判不了的**，供人工批次裁决；
> 每条都带推理依据，不做臆造。裁决结果写回 `homing/_overrides.json` 后重跑。

生成日期：2026-10-12

## 1. 未折入任何对象的复合体

（无：132 个复合体全部折入对象）

## 2. 无身份（PK）的根对象（仍未决）

根对象（有作用域列/有旧表锚点）却没有自己的行键：只能退回 `(world_id, pilot_id)` 单行，多条记录会互相 upsert 覆盖。

下面只列**没定**的；已裁决定性的两类见 §2b/§2c。

（无）

## 2b. 已裁决：单行（每个作用域一行）

裁决为「一个机师（或一个作用域）一行」。DDL 键形状**不变**，仍是 `(world_id, pilot_id)`；结论与依据记在 `_overrides.json.singleton`。

| 对象 | 依据 |
|---|---|
| `bracket` | 旧库 uq_game_bracket (world_id,pilot_id) 与生成 DDL 逐列一致 |
| `cinfo` | 旧库 uq_game_cinfo (world_id,pilot_id) 逐列一致；SC-0x5800/0x8E92 只读 |
| `dailycup_conf` | 旧库 uq_game_dailycup_conf (world_id,pilot_id) 逐列一致 |
| `dailycup_conf_next` | 旧库 uq_game_dailycup_conf_next (world_id,pilot_id) 逐列一致 |
| `dc_point` | 旧库 uq_game_dc_point (world_id,pilot_id) 逐列一致 |
| `eq_bonus_modules_lot` | 旧库 uq_game_eq_bonus_modules_lot (world_id,pilot_id) 逐列一致 |
| `evflag3` | 旧库 uq_game_pilot_evflag3 (world_id,pilot_id) 逐列一致；1 个 u64 位图成员，一个机师一份事件标志 |
| `exam_state` | 旧库 uq_game_exam_state (world_id,pilot_id) 逐列一致 |
| `ext_subrule` | 旧库 uq_game_ext_subrule (world_id,pilot_id) 逐列一致 |
| `intro_info` | 旧库 uq_game_intro_info (world_id,pilot_id) 逐列一致 |
| `lvjudge_hist` | 我方**等级判定履历**（369B，8 列：`lv_history[24]`/`lv_history_num`/`lv_history_max`/`term_old[25]`/`termstr_now`/`xwarwin_history[24]`/`xwarlose_history[24]`/`pilot_id`）：每个机师一份、随赛季推进更新（读方 `pilot_record_get_r`），键形状 `(world_id, pilot_id)` 正确，与 `precord`（战绩）、`pilot_detail`（我方详情）同类。本批**保留表**，只把它从 `no_writer` 挪到 `singleton`。 |
| `phase_info` | 旧库 uq_game_phase_info (world_id,pilot_id) 逐列一致 |
| `pilot_detail` | 旧库 uq_game_pilot_detail (world_id,pilot_id) 逐列一致；53 个成员全是一个机师的档案，手写面 store/pilot_money.go 也按 (world,pilot) 窄更新 |
| `precord` | 旧库 uq_game_precord (world_id,pilot_id) 逐列一致（61 个成员 = 一个机师的履历计数） |
| `ranking_info` | 旧库 uq_game_ranking_info (world_id,pilot_id) 逐列一致 |
| `rankself` | 旧库 uq_game_rankself (world_id,pilot_id) 逐列一致 |
| `season_rb_conf` | 旧库 uq_game_season_rb_conf (world_id,pilot_id) 逐列一致 |
| `sort_info` | 旧库 uq_game_sort_info (world_id,pilot_id) 逐列一致；两个写方 CS-0x2749/0x49D1 都是「GET 时顺带存下筛选条件」——12 个成员全是查询参数，一个机师一份 |
| `special_a_info` | 旧库 uq_game_special_a_info (world_id,pilot_id) 逐列一致 |
| `wbonus` | 旧库 uq_game_wbonus (world_id,pilot_id) 逐列一致 |
| `xwar_ext_rule` | 旧库 uq_game_xwar_ext_rule (world_id,pilot_id) 逐列一致 |

## 2c. 已裁决：暂无写入方（键待定）

在**写侧**（CS）没有任何写入方，只被 SC 读下发。没有写入方就不可能丢行，所以不阻塞；但接入写入方之前必须先定身份列，理由逐条记在 `_overrides.json.no_writer`。

（无）

## 3. 引用未解析（`X_id` 指不到唯一对象）

`X_id` 形式的成员已判为 `ref`，但对象名索引给不出**唯一**目标，且不属于下面 §3b/§3c 两类。多为「一族派生表都叫 clan」这类需要业务拍板的情况。

（无）

## 3b. 主数据引用（`cfg.*` 静态配置，**不是** `game.*` 外键）

这些 `X_id` 指向 `cfg` schema 的静态配置表（表在客户端/工具侧，服务器不写）。按 §4.E 口径，它们**不出 `relations.json` 的 `relations[]`**，单列在 `master_refs`。目标表有多候选的仍需人工点定。

| 对象 | 字段 | 候选目标 | 依据 | 证据 VA |
|---|---|---|---|---|
| `AI` | `formation_id` | `cfg.MSMA_FORMATION.formation_id` | 主数据 MSMA_FORMATION（cfg 主键列名命中） | `0xB074E9` |
| `AI` | `group_id` | `cfg.MISSION_GROUP.group_id` | 主数据 MISSION_GROUP（cfg 主键列名命中） | `0xB074AD` |
| `AI` | `param_id` | `cfg.AI_PARAM.ai_param_id` | 人工裁决·主数据：AI 对象的「参数 ID」= NPC AI 参数表 AI_PARAM（主键 ai_param_id）；对象 AI 是 battle 安装参数（EVENT，不落库），此处只把值域钉住 | `0xB07283` |
| `adop_get` | `equip_wid` | `cfg.ITEM.item_id` | 人工裁决·主数据：adop_list/adop_get 的 equip_wid「装备武器 id」= ITEM.item_id | `0xb43db9` |
| `adop_list` | `equip_wid` | `cfg.ITEM.item_id` | 人工裁决·主数据：adop_list/adop_get 的 equip_wid「装备武器 id」= ITEM.item_id | `0xb43db9` |
| `appear_info` | `item_id` | `cfg.ITEM.item_id` | 主数据/实例两解：cfg ['ITEM', 'OVER_CUSTOM_CUPSULE'] 与对象 item | `B07F65|B0B5E3` |
| `appear_info` | `msma_id` | `cfg.CHARA_PARAM.msma_id` | 主数据候选 ['CHARA_PARAM', 'MSMA_FLIGHT_SET', 'MSMA_MODULE', 'MSMA_RENTAL']（cfg 主键列名多命中，待定） | `B07F50|B0B5BC` |
| `bmgpack` | `shopitem_id` | `srv.shop_lineup.shopitem_id` | 人工裁决·主数据：商店商品 id = 服务端在售表 srv.shop_lineup.shopitem_id（item_list/bmgpack 都引用它；0018_srv_shop_lineup） | `0xb458b6` |
| `bonus_info` | `rwd_item_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：奖励物品 id = ITEM.item_id | `0xb4472c` |
| `bracket_info` | `mission_id` | `cfg.MISSION_COOP.mission_id` | 主数据候选 ['MISSION_COOP', 'MISSION_VS']（cfg 主键列名多命中，待定） | `B46DC5|B508AE` |
| `check_quest` | `quest_id` | `cfg.QUEST.quest_id` | 主数据/实例两解：cfg ['QUEST'] 与对象 quest_info | `B06C1A|B08FA6` |
| `coop_room` | `extrule_id` | `cfg.MISSION_EXTRULE.rule_id` | 人工裁决·主数据：扩展规则 id = 任务附加规则表 MISSION_EXTRULE（purpose 即「任务附加规则」，主键 rule_id）；coop_room/roominfo/dailycup_conf 用的都是这一张 | `0xB44928` |
| `coop_room` | `mission_id` | `cfg.MISSION_COOP.mission_id` | 主数据候选 ['MISSION_COOP', 'MISSION_VS']（cfg 主键列名多命中，待定） | `0xB44912` |
| `cshist_item` | `item_id` | `cfg.ITEM.item_id` | 主数据/实例两解：cfg ['ITEM', 'OVER_CUSTOM_CUPSULE'] 与对象 item | `0xB4240C` |
| `dailycup_conf` | `extrule_id` | `cfg.MISSION_EXTRULE.rule_id` | 人工裁决·主数据：扩展规则 id = 任务附加规则表 MISSION_EXTRULE（purpose 即「任务附加规则」，主键 rule_id）；coop_room/roominfo/dailycup_conf 用的都是这一张 | `B46F8F|B50C82` |
| `dailycup_conf_next` | `extrule_id` | `cfg.MISSION_EXTRULE.rule_id` | 人工裁决·主数据：扩展规则 id = 任务附加规则表 MISSION_EXTRULE（purpose 即「任务附加规则」，主键 rule_id）；coop_room/roominfo/dailycup_conf 用的都是这一张 | `B46F8F|B50C82` |
| `favms` | `favorite_ms_id` | `cfg.CHARA_PARAM.msma_id` | 人工裁决·主数据：favms/favms_add「收藏机体 ID」= CHARA_PARAM.msma_id | `` |
| `favms_add` | `favorite_ms_id` | `cfg.CHARA_PARAM.msma_id` | 人工裁决·主数据：favms/favms_add「收藏机体 ID」= CHARA_PARAM.msma_id | `` |
| `hack_check` | `weapon_itemid` | `cfg.ITEM.item_id` | 人工裁决·主数据：武器道具 id = ITEM.item_id（物品总表含武器） | `0xB06653|B0B9E0` |
| `item_list` | `shopitem_id` | `srv.shop_lineup.shopitem_id` | 人工裁决·主数据：商店商品 id = 服务端在售表 srv.shop_lineup.shopitem_id（item_list/bmgpack 都引用它；0018_srv_shop_lineup） | `0xb458b8` |
| `mail` | `attach_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：邮件附件 id = ITEM.item_id（attach_type 区分附件种类） | `0xb45881` |
| `mapgimmick_entry` | `msma_id` | `cfg.CHARA_PARAM.msma_id` | 主数据候选 ['CHARA_PARAM', 'MSMA_FLIGHT_SET', 'MSMA_MODULE', 'MSMA_RENTAL']（cfg 主键列名多命中，待定） | `0xB07C38` |
| `ms_rokaku` | `crew_msma_id` | `cfg.CHARA_PARAM.msma_id` | 人工裁决·主数据：ms_rokaku「乘员机体 ID」= 机体参数主表 CHARA_PARAM（主键 msma_id） | `0xb06dce` |
| `ms_rokaku` | `eqshield_itemid` | `cfg.ITEM.item_id` | 人工裁决·主数据：ms_rokaku「装备盾道具 ID」= ITEM.item_id | `0xb436ff` |
| `ms_rokaku` | `eqspecial_itemid` | `cfg.ITEM.item_id` | 人工裁决·主数据：ms_rokaku「装备特殊道具 ID」= ITEM.item_id | `0xb43715` |
| `ms_rokaku` | `eqweapon_itemid` | `cfg.ITEM.item_id` | 人工裁决·主数据：ms_rokaku「装备武器道具 ID（3 项）」= ITEM.item_id | `0xb436df` |
| `ms_rokaku` | `msma_id` | `cfg.CHARA_PARAM.msma_id` | 主数据候选 ['CHARA_PARAM', 'MSMA_FLIGHT_SET', 'MSMA_MODULE', 'MSMA_RENTAL']（cfg 主键列名多命中，待定） | `0xb06db8` |
| `ms_rokaku` | `sitem_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：ms_rokaku「副武器道具 ID」= ITEM.item_id | `0xb06f34` |
| `ms_rokaku` | `spitem_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：ms_rokaku「特殊道具 ID」= ITEM.item_id | `0xb06f49` |
| `ms_rokaku` | `witem_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：ms_rokaku「武器道具 ID（3 项）」= ITEM.item_id | `0xb06f14` |
| `msdeck_entry` | `msma_id` | `cfg.CHARA_PARAM.msma_id` | 主数据候选 ['CHARA_PARAM', 'MSMA_FLIGHT_SET', 'MSMA_MODULE', 'MSMA_RENTAL']（cfg 主键列名多命中，待定） | `0xB467D0` |
| `parts_exec_entry` | `item_id` | `cfg.ITEM.item_id` | 主数据/实例两解：cfg ['ITEM', 'OVER_CUSTOM_CUPSULE'] 与对象 item | `0xB06CF7` |
| `party_member_stat` | `mission_id` | `cfg.MISSION_COOP.mission_id` | 主数据候选 ['MISSION_COOP', 'MISSION_VS']（cfg 主键列名多命中，待定） | `0xb43329` |
| `pilot_detail` | `check_progress_quest_id` | `cfg.QUEST.quest_id` | 人工裁决·主数据：pilot_detail 的「进度检查任务 id」= 任务表 QUEST 主键 quest_id | `0xB42A3D` |
| `pilot_detail` | `monthly_bonus_holding_id` | `cfg.MONTHLY_BONUS_REWARD.reward_id` | 人工裁决·主数据：「月奖励持有 ID」= 月度登录奖励表 MONTHLY_BONUS_REWARD 主键 reward_id | `0xB42B34` |
| `quest_info` | `pay_byword_id` | `cfg.BYWORD.byword_id` | 人工裁决·主数据：quest_info 的报酬称号 id = 称号表 BYWORD 主键 byword_id（cfg 列名逐字命中） | `0xB46CA0` |
| `quest_info` | `pay_item_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：报酬物品 id = ITEM.item_id | `0xB46C64` |
| `quest_info` | `pay_msma_id` | `cfg.CHARA_PARAM.msma_id` | 人工裁决·主数据：quest_info「报酬机体 ID」= CHARA_PARAM.msma_id | `0xB46C8C` |
| `rental_module` | `module_id` | `cfg.MODULE.module_id` | 主数据 MODULE（cfg 主键列名命中） | `` |
| `replay_info` | `missionId` | `cfg.MISSION_COOP.mission_id` | 主数据候选 ['MISSION_COOP', 'MISSION_VS']（cfg 主键列名多命中，待定） | `0xB47378|B6FA42` |
| `respawn_post_entry` | `group_id` | `cfg.MISSION_GROUP.group_id` | 主数据 MISSION_GROUP（cfg 主键列名命中） | `0xB07A98` |
| `respawn_post_entry` | `post_chara_id` | `cfg.CHARA_PARAM.msma_id` | 人工裁决·主数据：v15客户端0x447310→0x4C17E0把post_chara_id作为CHARA定义表查询键；0x4C17E0参数a7进入0x581200查定义、创建后写inner+8，实例身份另由a15请求/自动分配。0x503B40后来把该字段值作为实例ID查对象管理器的键桥接疑点另见IDA证据，不改变此处客户端已证实的定义表值域。 | `0xB07A28` |
| `result_detail` | `itm_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：物品 id = 物品总表 ITEM 主键 item_id | `0xb44e84` |
| `result_detail` | `use_buffitem_id` | `cfg.ITEM.item_id` | 人工裁决·主数据：使用的 buff 道具 id = ITEM.item_id（战报里记的是道具模板 id，不是实例） | `0xb44e84` |
| `roominfo` | `extrule_id` | `cfg.MISSION_EXTRULE.rule_id` | 人工裁决·主数据：扩展规则 id = 任务附加规则表 MISSION_EXTRULE（purpose 即「任务附加规则」，主键 rule_id）；coop_room/roominfo/dailycup_conf 用的都是这一张 | `0xB44928` |
| `roominfo` | `mission_id` | `cfg.MISSION_COOP.mission_id` | 主数据候选 ['MISSION_COOP', 'MISSION_VS']（cfg 主键列名多命中，待定） | `0xB44912` |
| `season_rb_conf` | `mission_id` | `cfg.MISSION_COOP.mission_id` | 主数据候选 ['MISSION_COOP', 'MISSION_VS']（cfg 主键列名多命中，待定） | `0xB47258|B64D92` |
| `special_a_next` | `item_id` | `cfg.ITEM.item_id` | 主数据/实例两解：cfg ['ITEM', 'OVER_CUSTOM_CUPSULE'] 与对象 item | `0xb46cf9` |
| `unlockw` | `item_id` | `cfg.ITEM.item_id` | 主数据/实例两解：cfg ['ITEM', 'OVER_CUSTOM_CUPSULE'] 与对象 item | `0xb439eb` |

## 3c. 战斗期实体句柄（本场内存，不落库）

只在 battle 命令里出现的 `*ent_id`：指向本场战斗内存里的实体，**不落任何表**，故无所谓外键。

| 对象 | 字段 | 证据 VA |
|---|---|---|
| `AI` | `center_ms_entid` | `0xB074C1` |
| `AI` | `hate_ent_id` | `0xB072F9` |
| `appear_info` | `ent_id` | `B07F26|B0B56E` |
| `funnel_snapshot_entry` | `ent_id` | `0xB081C6` |
| `funnelss` | `ent_id` | `0xb081d7` |
| `gimmick_progress_entry` | `access_ent_id` | `0xB07DDE` |
| `mapgimmick_entry` | `ctrl_ent_id` | `0xB07CFB` |
| `mapgimmick_entry` | `ent_id` | `0xB07C07` |
| `respawn_post_entry` | `npc_ba_point_ent_id` | `0xB07AA9` |
| `snapshot` | `ent_id` | `0xb075be` |
| `snapshot` | `lockon_ent_id` | `0xb0771c` |
| `snapshot` | `rideon_ent_id` | `0xb0770b` |

## 3d. 已归类：引用目标不在本轮模型（保留普通列）

这些 `X_id` 已逐词干裁决（`_overrides.json.ref_stem`）：**目标不是一个可以指过去的表**，所以既不是 `game.*` 外键、也不是 cfg 主数据。它们照常落列（无 FK 约束），类别用来区分「模型缺对象」与「本来就不是引用」。类别：`world_entity` 跨机师共享实体（战队/杯赛队伍/锦标赛/队伍）、`local_table` 本地表资源（BGM 包/图标）、`value_object` 值对象内的编号（赛程节点/留言）、`master_candidate` 有候选 cfg 表但键名不符、`notref` 名字以 id 结尾而非引用。

| 对象 | 字段 | 类别 | 依据 | 证据 VA |
|---|---|---|---|---|
| `bgm_desc` | `ace_bgm_id` | `local_table` | BGM 包是本地表（BGMPACKAGE，主键 package_id）：ace_bgm_id 虽是表内同名列，但值是包内 bgm 编号、不是服务器主数据主键。 | `B07E36|B0B38F` |
| `bgm_desc` | `field_bgm_id` | `local_table` | 同上：field_bgm_id 是 BGMPACKAGE 内的 bgm 编号（同名列），不是主数据主键。 | `B07E24|B0B368` |
| `bgm_desc` | `force_bgm_id` | `local_table` | 同上：BGMPACKAGE 只暴露 force_bgm_enabled（没有 force_bgm_id 列），值域是包内 bgm 编号，不指主数据。 | `B07E48|B0B3B6` |
| `world_entry` | `icon_id` | `local_table` | world_entry.icon_id 是世界列表图标：80 张 cfg 表里没有 WORLD/ICON 主表（FORCEGAUGE_INFO/SEASON_CLASS_IMFORMATION 的 icon_id 是各自域内的），图标是客户端资源编号。 | `0xB02EB8` |
| `appear_info` | `arms_id` | `master_candidate` | appear_info「武装（arms）ID」候选是 cfg.MSMA_WEAPONSET.weapon_group_id（机体武器组），但该对象是战斗 EVENT 不落库，暂不指目标。 | `0xB07FAD` |
| `cinfo` | `npc_id` | `master_candidate` | clan 板 NPC 发帖人 id：80 张 cfg 里唯一 NPC 主表是 COMMANDER_NPC（主键 commander_id，另有 npc_model_id），键名与线名不符，未定 → 保留普通列。 | `0xB45985` |
| `clan` | `npc_id` | `master_candidate` | clan 板 NPC 发帖人 id：80 张 cfg 里唯一 NPC 主表是 COMMANDER_NPC（主键 commander_id，另有 npc_model_id），键名与线名不符，未定 → 保留普通列。 | `0xB9F8C6` |
| `news` | `npc_id` | `master_candidate` | clan 板 NPC 发帖人 id：80 张 cfg 里唯一 NPC 主表是 COMMANDER_NPC（主键 commander_id，另有 npc_model_id），键名与线名不符，未定 → 保留普通列。 | `0xB45DDE` |
| `news` | `parent_msgid` | `self_ref` | `parent_msgid` = 所属父条目号（`CS-0x45E3` 的 `parent_msgid=0` 即新话题），指向**同一张表** `game.news.msg_id` 的另一行。引擎把「目标=本对象」的 fk 一律判成身份列（`_stem_verdict` 自指分支，`news.msg_id` 正是靠这条），所以这里不指 FK：落普通列，自指关系留档（`0xB45E55`）。 | `0xb45e55` |
| `bracket_node` | `node_id` | `value_object` | bracket_node「节点 ID」是节点在括号内的编号；bracket_node 没有独立表（是 bracket_info 的子结构），节点身份由「父行 + 下标」给出，不另立 FK 目标。 | `0xB46FDA` |
| `dailycup_conf` | `tournament_id` | `world_entity` | 锦标赛 id 有 u32 载体（dailycup_conf.tournament_id / dailycup_conf_next.tournament_id / season_rb_conf.tournament_id，逐列带 VA），属性也在 conf 结构体里，但**0 个 CS 写方**：这一批回 IDA 把客户端发方**全枚举**过（345 个 `send_*` 名 ↔ 已建模 345 条 CS，**双向差集皆空**），赛事一族在 CS 侧只有 6 条 `_get` 查询，且**没有任何 CS 命令带 `tournament_id` 字段**；`tournament_id=` 的两处打印器只被 SC 分发器里的两条 config_update 分支调用（纯读侧）。客户端唯一沾边赛事的写命令是 `CS-0xC40D party_booking_ready`（只带 ready_ok + client_bogo_version，**不带 tournament_id**），已归位到 party。取证明细见 reviewed.batch_15_tournament_writer_hunt。且它自身的属性已由 dailycup_conf / dailycup_conf_next / season_rb_conf 三张表承载（三表就是「本机师视角的赛事配置」）。按 no_writer 同类的口径：没有写入方就不凭空建根表抢行键；等赛事调度写入方落地再建（届时按服务端运营态的口径进 srv.*，不是玩家维度的 game.*）。 | `B46EAF|B50A5F` |
| `dailycup_conf_next` | `tournament_id` | `world_entity` | 锦标赛 id 有 u32 载体（dailycup_conf.tournament_id / dailycup_conf_next.tournament_id / season_rb_conf.tournament_id，逐列带 VA），属性也在 conf 结构体里，但**0 个 CS 写方**：这一批回 IDA 把客户端发方**全枚举**过（345 个 `send_*` 名 ↔ 已建模 345 条 CS，**双向差集皆空**），赛事一族在 CS 侧只有 6 条 `_get` 查询，且**没有任何 CS 命令带 `tournament_id` 字段**；`tournament_id=` 的两处打印器只被 SC 分发器里的两条 config_update 分支调用（纯读侧）。客户端唯一沾边赛事的写命令是 `CS-0xC40D party_booking_ready`（只带 ready_ok + client_bogo_version，**不带 tournament_id**），已归位到 party。取证明细见 reviewed.batch_15_tournament_writer_hunt。且它自身的属性已由 dailycup_conf / dailycup_conf_next / season_rb_conf 三张表承载（三表就是「本机师视角的赛事配置」）。按 no_writer 同类的口径：没有写入方就不凭空建根表抢行键；等赛事调度写入方落地再建（届时按服务端运营态的口径进 srv.*，不是玩家维度的 game.*）。 | `B46EAF|B50A5F` |
| `season_rb_conf` | `tournament_id` | `world_entity` | 锦标赛 id 有 u32 载体（dailycup_conf.tournament_id / dailycup_conf_next.tournament_id / season_rb_conf.tournament_id，逐列带 VA），属性也在 conf 结构体里，但**0 个 CS 写方**：这一批回 IDA 把客户端发方**全枚举**过（345 个 `send_*` 名 ↔ 已建模 345 条 CS，**双向差集皆空**），赛事一族在 CS 侧只有 6 条 `_get` 查询，且**没有任何 CS 命令带 `tournament_id` 字段**；`tournament_id=` 的两处打印器只被 SC 分发器里的两条 config_update 分支调用（纯读侧）。客户端唯一沾边赛事的写命令是 `CS-0xC40D party_booking_ready`（只带 ready_ok + client_bogo_version，**不带 tournament_id**），已归位到 party。取证明细见 reviewed.batch_15_tournament_writer_hunt。且它自身的属性已由 dailycup_conf / dailycup_conf_next / season_rb_conf 三张表承载（三表就是「本机师视角的赛事配置」）。按 no_writer 同类的口径：没有写入方就不凭空建根表抢行键；等赛事调度写入方落地再建（届时按服务端运营态的口径进 srv.*，不是玩家维度的 game.*）。 | `0xB4720A|B64D92` |

## 4. 生命周期 TBD 的字段

| 对象 | 字段 | 线类型 | 线视图 |
|---|---|---|---|
| `examination_info_entry` | `val_00` | `u32` | examination_info_entry |
| `examination_info_entry` | `val_04` | `u32` | examination_info_entry |
| `examination_info_entry` | `val_08` | `u32` | examination_info_entry |
| `examination_info_entry` | `val_0c` | `u32` | examination_info_entry |
| `gimmick_progress_entry` | `access_ent_id` | `u16` | gimmick_progress_entry |
| `gimmick_progress_entry` | `gauge_now` | `u32` | gimmick_progress_entry |
| `gimmick_progress_entry` | `stat` | `i8` | gimmick_progress_entry |
| `mapgimmick_entry` | `param_1` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_2` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_3` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_4` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_5` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_6` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_7` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_8` | `u16` | mapgimmick_entry |
| `msdeck` | `grid_0` | `u32[10]` | msdeck |
| `msdeck` | `grid_1` | `u32[10]` | msdeck |
| `msdeck` | `grid_2` | `u32[10]` | msdeck |
| `msdeck` | `grid_3` | `u32[10]` | msdeck |
| `msdeck` | `row_0` | `u32[4]` | msdeck |
| `msdeck` | `row_1` | `u32[4]` | msdeck |
| `msdeck` | `row_2` | `u32[4]` | msdeck |
| `msdeck` | `row_3` | `u32[4]` | msdeck |
| `msdeck` | `row_4` | `u32[4]` | msdeck |
| `msdeck` | `row_5` | `u32[4]` | msdeck |
| `msdeck` | `row_6` | `u32[4]` | msdeck |
| `msdeck` | `row_7` | `u32[4]` | msdeck |
| `msdeck` | `tail_a` | `u32[4]` | msdeck |
| `msdeck` | `tail_b` | `u32[4]` | msdeck |
| `msdeck` | `tail_c` | `u8[4]` | msdeck |
| `quest_info` | `tail_1` | `u8` | quest_info |
| `rokaku_node_entry` | `val_00` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_04` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_08` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_0c` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_10` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_14` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_18` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_1c` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_20` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_24` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_28_u64` | `u64` | rokaku_node_entry |
| `rokaku_node_entry` | `val_30` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_34` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_38` | `u32` | rokaku_node_entry |

## 5. 对象边界待人工拍板

折叠链把以下对象合成了一个业务对象；若业务上应拆分，请在此登记。

| 对象 | 折入的线布局 | 线长 | 锚点 |
|---|---|---|---|
| `clan_search_hit` | clan_search_hit, srch_res | 114, 114 | `-` |
| `missionunit_set` | missionunit, missionunit_set | 12, 12 | `tbl_missionunit_set` |
| `ms_rokaku` | ms, ms_lounge, ms_rokaku | 244, 303, 401 | `tbl_ms_rokaku` |
| `news` | comment, news | 267, 244 | `-` |
| `pilot` | pcard, pilot, pilots_list | 398, 159, 398 | `-` |
| `ranking_info` | order, ranking_info | 10, 10 | `-` |
| `unlocked_navi` | navi_entry, unlocked_navi | 8, 8 | `tbl_unlocked_navi` |

## 6. 同名成员跨线形宽度差异（已定宽，非未决）

同一业务字段在不同 `wire_form` 里编码宽度可以不同。DDL 的列宽跟**落库线体**（`wire_body`，见 docs/05 §4.F）走，其余线形的宽度记在下面——**列宽必须装得下每一条线形**，所以这是核对清单而不是未决项：若某行的宽度大于列宽，`_survey_homing.py` 的「列宽装得下每条线形」不变量会报红。

| 对象 | 字段 | 落库线体 | 列宽（已定） | 其它线形 |
|---|---|---|---|---|
| `ms_rokaku` | `is_costover` | `ms_rokaku` | char[2]（2B） | `ms` u8(1B) |
| `ms_rokaku` | `over_custom_level` | `ms_rokaku` | u32（4B） | `ms` u16(2B) |
| `pilot` | `avatar` | `pcard` | avatar（18B） | `pilot` avatar(18B)(18B) |
| `pilot` | `clan_emb_base` | `pcard` | u8（1B） | `pilot` i8(1B) |
| `pilot` | `clan_emb_parts1` | `pcard` | u8（1B） | `pilot` i8(1B) |
| `pilot` | `clan_emb_parts2` | `pcard` | u8（1B） | `pilot` i8(1B) |
| `pilot` | `level` | `pcard` | u8（1B） | `pilot` i8(1B) |
| `pilot` | `mil_class` | `pcard` | u8（1B） | `pilot` i8(1B) |
| `pilot` | `troops` | `pcard` | u8（1B） | `pilot` i8(1B) |

## 7. 值对象（无独立行键，由父行定位）

以下对象没有自己的行键、也没有作用域列——它们是嵌在别的对象里的值对象，**不单独建表**，列内联到父表。

| 对象 | 成员数 | 出处线布局 |
|---|---|---|
| `avatar` | 10 | avatar |
| `beginner_challenge_info` | 4 | beginner_challenge_info |
| `bracket_node` | 7 | bracket_node |
| `cshist_item` | 2 | cshist_item |
| `examination_item` | 2 | examination_item |
| `examination_state` | 8 | examination_state |
| `favms` | 18 | favms |
| `msdeck_entry` | 3 | msdeck_entry |
| `rental_module` | 2 | rental_module |
| `snapshot` | 21 | snapshot |
| `special_a_next` | 3 | special_a_next |

## 8. 同形线布局（折叠候选）

逐字节同形（线长 + 成员名序列完全一致）却分属不同对象的复合体。引擎不擅自合并（`layout_same_as` 只说明布局相同、不说明是同一业务对象；P2 复核批次 `batch_02_fold` 的裁决是保守不折叠），请人工判定，裁决写进 `_overrides.json.twin_verdicts`（`fold` / `keep` + 理由），守卫 18 会校验裁决与引擎状态一致。

### 8.1 未裁决（0 组）

（无）

### 8.2 已裁决·不折（18 组）

同形只说明元素字段相同；下面每组都有「折了会丢行/丢列/改行主」或「都不建表、折叠不改 DDL」的具体理由。

| 同形组 | 裁决 | 理由 |
|---|---|---|
| `adop_get`, `adop_list` | keep | 元素同形（13B：db_index/equip_wid/adop_set）但**行键不同**：`adop_get` 的行是「按槽的采纳结果」（pk w,p,db_index），`adop_list` 的行是「某台机体上的采纳列表」（pk w,p,uniqid_ms,db_index，`uniqid_ms` 来自 `SC-0xA832-msma_add` 的兄弟字段）。旧库两张表都在（`game.adop_get` / `game.adop_list`，UNIQUE 各不同）。折了会丢 `uniqid_ms`、把两个聚合的行混成一张。 |
| `block_detail`, `clan_member_card`, `friend_detail`, `friend_histories`, `lpcard`, `member_info`, `mshipbid_card` | keep | 批 18 已裁决（reviewed.batch_18_list_family_correction）：113B 是「他人名片」，行主是「读方 + 目标机师」——同一个人会同时出现在屏蔽/好友/履历/竞标四张表里，四张表的行集不重合（各有自己的目标身份列 `*_pilot_id`），且 `block_detail`/`friend_detail` 有真实 CS 写方（`CS-0xECDA`/`CS-0x753A`/`CS-0xBA4E`/`CS-0xA30C`）；`lpcard`/`clan_member_card`/`member_info` 维持 DERIVED（成员关系可由 `pilot.clan_id` 推出）。折叠会把四张列表压成一条线形、并且让「谁在我的列表里」无处可存。 |
| `bmgpack`, `item_list` | keep | 两者都已判 DERIVED（不建表）：`item_list` 是商店在售线up（`SC-0x99A0`/`SC-0xAB7B`），`bmgpack` 出现在机师列表响应里（`SC-0xE13A`）。同形只说明元素字段相同；是否同一批行（同一张 srv.shop_lineup）未取证（两族读命令不同）。都不落库 ⇒ 折叠不改 DDL，不折以免把一个未取证的假设写进模型。 |
| `buffitem`, `buffitem_ex` | keep | 同一命令（`SC-0x91C9-battle-battle_buffitem_list`）下发两个数组，但旧表声明把两者各建一件（`buffitem` / `buffitem_ex` 都在 `declared_but_not_live` 里），说明前一版分析已按「两组同类道具」分别建模。两者都 EVENT（战斗期，不落库）⇒ 折叠不改 DDL。 |
| `challenge_info`, `netcafe_challenge_info`, `pdaily`, `trchallenge_info` | keep | 四个**不同进度族**复用同一 `(id,val,sub_val,is_clear)` 13B 形状：部队挑战通关（`SC-0x51B7`）、网咖挑战（`SC-0x7626`）、每日记录（`SC-0x81F1`）、部队挑战（`SC-0x271C`）。各族 `id` 的命名空间不同、行集由各自命令下发；旧库把 `challenge_info` 与 `trchallenge_info` 建成两张表（`netcafe_challenge_info` 声明为 EVENT、旧库从未建成）。折了会把四族的行混成一张、`id` 命名空间互撞。 |
| `clan_eff`, `clan_zeon` | keep | 同一命令（`SC-0x244E-btlroom_info_one`）下发**两军各一份**战队编成，元素里`clan_id`/`world_id`/`emb_*` **没有侧别列**：折进一张表后，若同一个 clan 同时出现在两侧（pk 同为 w,p,clan_id）就会撞行、丢掉一侧。旧库也是两张表（`game.clan_eff` / `game.clan_zeon`，列集逐字相同）。 |
| `coop_room`, `roominfo` | keep | `coop_room` 是**房间列表**投影（`SC-0xDBDB-btlroom_coop_roomlist_get_r` 下发别人的房间），`roominfo` 是持久房间行；且模型里 `coop_room.room_id` 已经是指向 `roominfo.room_id` 的外键（`ref_stem.room`）——折了会把这个外键变成自指、并把「我查过的房间列表」写成「我的房间」（行主同 113B 卡片族）。两者一个建表一个 DERIVED，折叠不改 DDL。 |
| `dailycup_conf`, `dailycup_conf_next` | keep | 同一命令（`SC-0x44C1-dailycup_config_update`）下发**本届/次届两份**配置，两者行键相同（`(world_id,pilot_id)` 单行）。折进同一 pk 后，后写的次届参数会把本届覆盖掉（每作用域只剩一行）。旧库两张表都在（`game.dailycup_conf` / `game.dailycup_conf_next`）。 |
| `dc_point`, `dcpoint_detail` | keep | `dc_point` 是**结算后的当前累计行**（`SC-0x2AAF-dailycup_get_point_r`），`dcpoint_detail` 是**战斗回执里的本场前后值快照**（`SC-0xD5E6-result_info`，与 `result_detail` 同族的「本场变化」）。两者行键同为 `(world_id,pilot_id)` 单行，折了会把当前值覆盖成本场变化。旧库 `game.dc_point` 存在、`dcpoint_detail` 从未建成。 |
| `exam_state`, `examination_state` | keep | 行主不同：`exam_state` 是**我方**考核态根行（`SC-0xA204-pilot_examination_state`，表 `game.exam_state`），`examination_state` 是 `pilot_detail` 的 **1:1 嵌套成员**、行在 `game.pilot_detail__examination_state`（旧库同名子表存在）——`pilot_detail` 也可用于别人的卡（`SC-0xB4B6-pilotcard_get_r`），所以那一份是「我看过的详情里的状态」快照（同 113B 卡片族的行主）。两者 pk 都是 (world,pilot)，折了会互相覆盖。 |
| `extrarule_xwar_info`, `xwar_ext_rule` | keep | `extrarule_xwar_info` 是**战斗鉴权回执**里下发的本场规则快照（`SC-0xA5DA-battle-authenticate_r`），`xwar_ext_rule` 是机师持久行（`SC-0xCCDF-xwar_booking_option_get_r`，旧库 `game.xwar_ext_rule` 存在）。战斗用的规则由房间/匹配决定，不必然等于我预约时的设置 ⇒ 一行建表、一行不建，折叠会把两个语义合到一个对象页里（且不改 DDL）。 |
| `favms`, `favms_add` | keep | `favms` 是持久行（旧库 `game.pilot_detail__favms_arr`，数组子表，键 w,p,elem_index），`favms_add` 是**结算回执里的本场增量**（`SC-0xD5E6-result_info` 带 `dirty_flag`/`last_update`）。一份是累计值、一份是本场变化，行键同族 ⇒ 折了会把增量覆盖进累计行。 |
| `funnel_snapshot_entry`, `funnelss` | keep | 两者都判 EVENT（战斗期临时数组，不落库）。`funnel_snapshot_entry` 有 CS 写方（`CS-0x7916-battle-funnel_snapshot_self`，自机上报），`funnelss` 只有读方（`SC-0x717D`/`SC-0x7621` 实体出现广播）——同形但来源与去向不同；折叠不改 DDL（两张都不建表）。 |
| `leaders`, `member`, `party_member` | keep | 同形（52B / 7 成员：`pilot_id`/`name`/`level`/`rate_vslocal`/`is_leader`/`avatar`/`pstat`）但**三个不同的成员花名册**：`leaders` 是队伍招募列表里的成员（`SC-0xB43F-party_recruit_list_get_r`），`member` 是对战房间成员详情（`SC-0x6B15-btlroom_member_detail_get_r`），`party_member` 是招募详情里的成员（`SC-0x305D-party_recruit_detail_get_r` 的 `party_members[]`）。三者都 0 写方、都 DERIVED（不建表）⇒ 折叠不改 DDL，保留三个对象以维持各命令的语义边界。**键的来历**：组键是「线长 + 成员名序」的签名，`party_member` 定稿为这一形状后签名变成三件，而原裁决只覆盖两件 ⇒ 守卫 18 报「判 keep 但已不在孪生清单里」。这不是裁决错了，是**裁决没跟上新的分组边界**，故补上第三个 id 而不是删条目。 |
| `mprogress`, `progress` | keep | 两者都判 EVENT（不落库）。`progress` 是**整场任务进度全量**（`SC-0x1365-game_begin` / `SC-0xA5DA-authenticate_r` / `SC-0xC66B-game_round_end` / `SC-0xD5E6-result_info` 都下发），`mprogress` 是 `SC-0x3E23-game_mission_progress_update` 的**增量更新**——同一结构两种用途，折叠不改 DDL。 |
| `ranking`, `toppilots` | keep | 同一命令（`SC-0xB985-ranking_pilot_get_r`）下发两个数组（`ranking[]` 检索结果页 / `toppilots[]` 榜首列表），**行集不同**；两者都 0 写方、都 DERIVED（不建表）⇒ 折叠不改 DDL，保留两形以维持「结果页 ≠ 榜首」的区别。 |
| `rankself`, `special_a_info` | keep | 两者都是**每机师一行**的同 pk 结构（`(world_id,pilot_id)`，6 成员 rank/score_now/entry_until/highscores/entry_until_es/eventscores），但读命令不同（`SC-0xB985-ranking_pilot_get_r` vs `SC-0x8D4F-get_special_a_info_r`）、旧库两张表都在（`game.rankself` / `game.special_a_info`）：折了同一 pk 只能留一行，`highscores`/`eventscores` 两族历史分互相覆盖。 |
| `recruit`, `recruits` | keep | ★ 本组是 2026-09-25 合并 `recruit` 尾字段占位名（`w74_u16`→`remain_minutes`、`w76_u32`→`party_type`）**之后**才出现的：两者先前签名不同（占位名对不上），定名后签名全等（80B / 9 名）。裁决 `keep`：这两形确实是**同一元素**（同一读取器 `sub_B45400`、9 个字段逐偏移逐指令相同），但它们是**两条命令的语义边界**——`SC-0x305D-party_recruit_detail_get_r` 的单发详情 vs `SC-0xB43F-party_recruit_list_get_r` 的数组项（上限 200），与 `ranking+toppilots`（同命令两数组）、`leaders+member+party_member`（三个名册）同族：两者都判 `DERIVED`（不建表）⇒ **折叠不改 DDL**，保留两形以维持「详情 ≠ 列表项」的对象页与命令归属（详情对象的列证据来自 305D，列表项的来自 B43F）。 |

### 8.3 已裁决·折叠（2 组）

折成一个对象（表只留一张，另一张在 `retire_tables` 登记退场）。

| 同形组 | 折成 | 理由 |
|---|---|---|
| `navi_entry`, `unlocked_navi` | `unlocked_navi` | 同一批行两张表：`navi_entry` 是全量列表（`SC-0x0906-player_navi_get_list_r` 的 `navi_list[]`），`unlocked_navi` 是刚解锁的那一条（`SC-0xA0BB-player_navi_unlock_r` 的单8B 元素）。线长 8B、成员名/线宽逐字相同，行键同为 `(world_id,pilot_id,navi_id)`（旧库 `uq_game_unlocked_navi` 唯一键 = `navi_id`）⇒ 折到 `unlocked_navi`、退 `game.navi_entry`（登记见 retire_tables）。 |
| `order`, `ranking_info` | `ranking_info` | 同一批行两张表：`SC-0x9F9B` 的字段名是 `ranking_info`、日志串是 `order=`（`0xB6EF5A`），CS 写方发的是同一 `order` 结构（`sub_B42060`）⇒ 同一份「上次排行检索条件」。行键同为 `(world_id,pilot_id)` 单行、成员名/线宽逐字相同 ⇒ 折到 `ranking_info`、退 `game.order`（登记见 retire_tables）；3 个 CS 写方随折叠落到 `ranking_info`。 |

## 9. 有定位但无地址级 VA 的成员

这些成员有 `命令 + 子程序 + README 章节` 但没记到地址级 `evidence_va`。证据在，不阻塞归位，但**不满足 §8「指回 VA」的严格口径**——要么补 VA（走 IDA 批次），要么接受按 `evidence_ref` 追溯。

| 对象 | 无 VA 成员数 | 示例字段 |
|---|---|---|
| `favms` | 18 | `battle_cnt`, `battle_rule`, `dirty_flag`, `favorite_exp_sum` |
| `favms_add` | 18 | `battle_cnt`, `battle_rule`, `dirty_flag`, `favorite_exp_sum` |
| `bonus_event` | 16 | `accump_offset`, `accump_rate`, `begin_time`, `bonus_target` |
| `result_wave` | 10 | `cleartime_rank`, `cleartime_sec`, `container_max`, `container_num` |
| `examination_item` | 2 | `gain_val`, `id` |
| `rental_module` | 2 | `count`, `module_id` |
