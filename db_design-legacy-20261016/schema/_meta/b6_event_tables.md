# 非 PERSIST 根对象：B6 入口（EVENT/TBD）+ 已裁决退场（DERIVED/CONFIG）

由 `tools/report_b6.py` 生成，**不要手改**；改模型后重跑脚本。

共 **51** 个根对象不建表，四个桶各自成因不同，处置也不同：

| 桶 | 条数 | 意思 | 开工时要做什么 |
|---|---|---|---|
| `EVENT` | 26 | 战斗/会话 ephemeral（一局一份，结算即弃） | 定身份列 + 定写入方（见下两节） |
| `TBD` | 1 | 分类未定（成员/线宽还有洞） | 先补模型，再判落 `PERSIST` 还是 `EVENT` |
| `DERIVED` | 21 | 行在别的根表里 / 可由别的表算出 | **不建表**（已裁决，理由逐条见末节） |
| `CONFIG` | 2 | 运营配置（主数据侧维护） | **不建表**（已裁决，理由逐条见末节） |

后两桶（`DERIVED`/`CONFIG`）是**批 19 起的裁决结果**，它们不是 B6 的输入，只是同在「非 PERSIST」这一层；列在末节是为了让「48 个」这个总数能对上账（此前只列 EVENT/TBD 两桶，表里 29 条、标题 48 条，读的人会以为漏了 19 个）。

它们不进 `0003_game_persist.up.sql`（P4 起由生成器的 `disposition == PERSIST` 过滤保证），模型里也没有幻影表（`derive_homing.py` 的幻影表门，`serverv/tools/verify_no_blob.py` 复核）。

**B6 开工时要做的两件事**（每个对象各自定，不能一刀切）：

1. **定身份列**：现在它们只有 `world_id, pilot_id` 兜底，多条记录会互相 upsert 覆盖。下表「身份候选」列是现成的命名候选（`ent_id`/`room_id`/`item_id`/`route_no`/`index`…），但要逐个判「是**自己的**记录号还是**指向别人的**引用」——`*_id` 多半是后者，当 PK 会把「一个实体一条」错钉成「一个引用目标一条」（`docs/05 §4.B`）。
2. **定写入方**：`CS 写方` 列为空的，说明服务端现在没有落库路径（战斗侧`battle/room.go` 的 `Room.Settle` 还是 no-op）；有了写入方才有「什么时候写、写哪一行」的问题，键也才有意义。

## EVENT（战斗/会话 ephemeral）

| 对象 | 域 | 线长 | 成员 | CS 写方 | SC 读方 | 身份候选 |
|---|---|---|---|---|---|---|
| `AI` | battle | 165 | 29 |  | `SC-0xB463-battle-msma_AI_install` | formation_id, group_id, hate_ent_id, param_id |
| `appear_info` | battle | 86 | 17 |  | `SC-0x057A-battle-entity_deploy_arms_appear` | arms_id, ent_id, index, item_id, msma_id, pilot_id, world_id |
| `bgm_desc` | battle | 14 | 5 |  | `SC-0x1365-battle-game_begin`, `SC-0xDC1E-battle-bgm_change` | ace_bgm_id, field_bgm_id, force_bgm_id |
| `buffitem` | battle | 6 | 3 |  | `SC-0x91C9-battle-battle_buffitem_list` | — |
| `buffitem_ex` | battle | 6 | 3 |  | `SC-0x91C9-battle-battle_buffitem_list` | — |
| `check_quest` | battle | 133 | 10 |  | `SC-0x6059-battle-check_progress_quest_r` | quest_id |
| `config` | battle | 34 | 10 |  | `SC-0x1365-battle-game_begin`, `SC-0xA5DA-battle-authenticate_r` | — |
| `examination_info_entry` | battle | 16 | 4 |  | `SC-0xFD8A-battle-examination_progress_r` | — |
| `fire_point` | battle | 6 | 3 | `CS-0xFBC1-battle-weapon_fire__funnel` | `SC-0xA78D-battle-weapon_fire__funnel_r` | — |
| `funnel_snapshot_entry` | battle | 10 | 3 | `CS-0x7916-battle-funnel_snapshot_self` | `SC-0x1B67-battle-funnel_snapshot_all` | ent_id |
| `funnelss` | battle | 10 | 3 |  | `SC-0x717D-battle-entity_msma_appear`, `SC-0x7621-battle-entity_msma_appear_self` | ent_id |
| `gimmick_progress_entry` | battle | 7 | 3 |  | `SC-0x1159-battle-game_mapgimmick_update` | access_ent_id |
| `hack_check` | battle | 79 | 30 | `CS-0x421B-battle-pos_move` |  | — |
| `mapgimmick_entry` | battle | 52 | 23 |  | `SC-0x1365-battle-game_begin` | ctrl_ent_id, ent_id, msma_id |
| `mprogress` | battle | 46 | 14 |  | `SC-0x3E23-battle-game_mission_progress_update` | — |
| `parts_exec_entry` | battle | 17 | 6 |  | `SC-0x16AA-battle-eqparts_execute` | item_id |
| `progress` | battle | 46 | 14 |  | `SC-0x1365-battle-game_begin`, `SC-0xA5DA-battle-authenticate_r`, `SC-0xC66B-battle-game_round_end`, `SC-0xD5E6-lounge-result_info` | — |
| `respawn_post` | battle | 25 | 9 |  | `SC-0xD1B3-battle-game_respawn_post_update` | — |
| `respawn_post_entry` | battle | 58 | 16 |  | `SC-0x1365-battle-game_begin` | group_id, npc_ba_point_ent_id, post_chara_id |
| `support_spot` | battle | 37 | 11 |  | `SC-0x5092-battle-commander_support_spot_notice` | — |
| `wave_res` | battle | 34 | 15 |  | `SC-0x6475-battle-game_coopwave_result` | — |
| `pointdmg` | lounge | 24 | 2 |  | `SC-0xD5E6-lounge-result_info` | — |
| `result_detail` | lounge | 555 | 80 |  | `SC-0xD5E6-lounge-result_info` | itm_id, use_buffitem_id |
| `result_wave` | lounge | 20 | 10 |  | `SC-0xD5E6-lounge-result_info` | — |
| `score_ranking` | lounge | 61 | 19 |  | `SC-0xD5E6-lounge-result_info` | pilot_id, world_id |
| `total_result_wave` | lounge | 19 | 7 |  | `SC-0xD5E6-lounge-result_info` | — |

## TBD（分类未定）

| 对象 | 域 | 成员 | CS 写方 | SC 读方 | 身份候选 | 说明 |
|---|---|---|---|---|---|---|
| `rokaku_node_entry` | lounge | 14 |  | `SC-0xFF8B-lounge-clan_rokaku_tree_get_r` | — |  |

## 已裁决退场（DERIVED / CONFIG，不建表）

| 对象 | 域 | 裁决 | 理由（`no_table_reason` 首句；全文见对象页） |
|---|---|---|---|
| `activity` | lounge | CONFIG | 大厅公告条目（`SC-0x5A3D-lounge-activity_notice` 的顶层数组，成员与 356B `activity` 复合体逐成员对应：pilot_id/name(25B)/level/is_admin/send_range/timestamp_text(24B)/msg(241B) + avatar 10 列 + clan_id/clan_name/emb 3 列） |
| `bonus_event` | lounge | CONFIG | **运营配置**：`bonus_event_now_update` 下发当期加成活动日程（`game_type`/`begin_time`/`end_time`/`main_priority`/`accump_rate`/`gp_rate`/`moneyup_rate`/`raredrop_rate`/`reward_num`…），按世界（或全服）一份、由运营排期，不是玩家状态 |
| `extrarule_xwar_info` | battle | DERIVED | 大规模战扩展规则的**战斗侧副本**：7 个成员名与根对象 `xwar_ext_rule` 逐个相同（514B 同形），`battle-authenticate_r` 只是把开局参数回给客户端 |
| `bmgpack` | lounge | DERIVED | 商店在售商品的**读视图**（23B 元素，与 `item_list` 同一打印器 `sub_B4E110`、同一组列 `shopitem_id`+`gp_x01/gp_x10/cp_x01/cp_x10`+`bit_eff`+`stock`）：`pilot_list_get_r` 里下发的是「BGM 包在售清单」，主数据与价格/库存是运营态（`srv.shop_lineup` 一类），`bmgpack.shopitem_id`本来就被判为指向主数据的 `master` 引用 |
| `clan_member_card` | lounge | DERIVED | 氏族成员名片（孪生根，与 `lpcard` 逐字节同形 / 20 成员）：同判——成员关系在`pilot.clan_id`，卡片列 ⊂ `pilot` 并集，0 CS 写方 ⇒ 不建第二张成员表 |
| `coop_room` | lounge | DERIVED | 房间列表的读视图：15 个成员名与根对象 `roominfo` 逐个相同（= `roominfo` 的线形），`btlroom_coop_roomlist_get_r` 下发的是「协同房列表」 |
| `dailycup_team_pilot` | lounge | DERIVED | 每日杯队伍成员的**查询投影**：`SC-0x8669-dailycup_team_info_get_r` 的 `pilots[array<dailycup_team_pilot,N≤51>]`（48B 元素：`pilot_id`/`name`/`level`/`avatar`，成员名取自元素打印器 `sub_B50EC0`）——四列**全是机师列**，行=机师，「谁在这个杯赛队伍里」这件事属队伍一侧 |
| `dcpoint_detail` | lounge | DERIVED | 结算面板里的**差值投影**：5 个成员名与根对象 `dc_point` 逐个相同（`bef_dcpoint`/`aft_dcpoint`/`is_dc`/`reward_item_ids`/`reward_item_nums`），`result_info` 是那场结算的回执 |
| `favms_add` | lounge | DERIVED | **同一批行的结算增量形**：18 个成员名与元素复合体 `favms` 逐个相同，而行本身是`pilot_detail.favms_arr`（720 格，子表 `game.pilot_detail__favms_arr` 存 18 列）的元素 |
| `invite` | lounge | DERIVED | 「可邀请机师」的**分页查询结果**（`invite_count` + `page_now`/`page_max` + `sort_info`）：行=机师（`pilot_id`/`name`/`rank`/`mil_class`），`continued_login_days`/`is_bonus`/`vslocal_cnt`/`xwar_cnt`是筛选/加成用的**算出来的**值（连续登录天数、场次计数），`last_login`/`last_logout` 与 `pilot` 侧时间列同族（列名变体，留给 colname 批次） |
| `item_list` | lounge | DERIVED | 商店在售商品（23B 元素）：`shop_lineup_r` 下发「道具店在售清单」，与 `bmgpack` 同形同打印器、只是商店不同（`batch_02_fold` 说它们「布局全等但域不同」——对，两个货架） |
| `leaders` | lounge | DERIVED | 招募列表里的「队长条目」（7 成员）：行=机师（`pilot_id`/`name`/`level`/`avatar`/`rate_vslocal`），`is_leader`/`pstat` 是**队伍成员关系属性**，家在 `party_member`（本模型已有该表的同名成员） |
| `lpcard` | lounge | DERIVED | 氏族成员名片的**读视图**（113B / 20 成员，与 `friend_detail` 等同形）：20 列全是 `pilot` 并集的子集，而**成员关系可由 `pilot.clan_id` 推出**——「某氏族的成员」= 同 `clan_id` 的机师集合（`SC-0x…-clan_memberlist_get_r` 是查询，0 CS 写方）⇒ 行可派生，不建表 |
| `member` | lounge | DERIVED | 房间成员条目（7 成员，与 `leaders` 同形）：行=机师，`is_leader`/`pstat` 是成员关系属性（`party_member` 有同名成员） |
| `member_info` | lounge | DERIVED | 「我自己的名片」（`SC-0x…-clan_info_get_self_r` 里的 `member_info`，113B / 20 成员）：行就是**我**这一行，20 列 ⊂ `pilot` 并集 ⇒ 由 `game.pilot` 投影，不另建表（0 CS 写方） |
| `msdeck` | lounge | DERIVED | 机师战绩页里的**编成投影**（324B 固定元素，读取器 `sub_B43E00`）：`SC-0xDC47-pilot_record_get_r` 的 `msdeck[2]` 下发「该机师的两套机体编成暗牌」 |
| `rank_pilot` | lounge | DERIVED | 精英排行的查询投影（18 成员）：`ranking_elite_pilot_get_page_r` / 赛季命令 |
| `rank_pilot_light` | lounge | DERIVED | 精英排行轻量项（7 成员，`rank_pilot` 的子集）：同上，查询投影（含 `season_class_lv` 赛季态） |
| `ranking` | lounge | DERIVED | 排行项的**查询投影**（12 成员：`rank`/`score`/`pilot_id`/`clan_*`/`emb_*`/`avatar`/`level`/`troops`）：`ranking_pilot_get_r` 按分数排序取头部，名次与分数是查询时算出来的，不是机师的源数据列（`pilot`/`pilot_detail` 里没有 `score` 这一列） |
| `recruit` | lounge | DERIVED | **招募详情的读视图**（80B / 9 成员）：`SC-0x305D-party_recruit_detail_get_r` 的 `recruit` 与 `SC-0xB43F` 的列表项 `recruits` 是**同一读取器 `sub_B45400` 解出的同一个 80B 元素**（2026-09-25 复看 IDA：9 个字段的偏移、宽度、取值指令逐条相同，线 80B / 内存 84B；两张复合体只是同结构的两个用例：单发 vs 数组元素） |
| `recruits` | lounge | DERIVED | **招募列表项的读视图**（80B / 9 成员，与 `recruit` 同形同读取器 `sub_B45400`）：`SC-0xB43F-party_recruit_list_get_r` 的 `recruits[array<recruits,N≤200>]`，每项就是一条「正在招募的队伍」的预览，列同 `recruit`（8 列并进 `composites/party.json`，余 `party_id` 指 `game.party`） |
| `team_pilot` | lounge | DERIVED | 赛季队伍成员（5 成员：`pilot_id`/`name`/`level`/`avatar`/`world_id`）全是机师列，行=机师；队伍成员关系在 party 侧，0 CS 写方 ⇒ 查询投影 |
| `toppilots` | lounge | DERIVED | 排行项：与 `ranking` 成员名序完全相同（孪生根），同一条 `ranking_pilot_get_r` 的「榜首」窗口 |

## 备注

- 标 `TBD` 的对象先要补模型（成员/线宽），补完可能落进 `PERSIST` 或 `EVENT`；
  这一层没定之前不要给它建表。
- 「线长」取对象视图里的线体长度；`TBD` 行留空表示还没定形。
- 本清单与 `0003` 的对账口径：**非 PERSIST 对象不得出现在 DDL 里**，
  `verify_no_blob.py` 会在入库前拦一次。
- `DERIVED`/`CONFIG` 桶若将来出现写入方或新列，裁决要回到
  `_overrides.json.disposition` 改，并重跑本脚本（`--check` 会在 CI 拦过期）。
