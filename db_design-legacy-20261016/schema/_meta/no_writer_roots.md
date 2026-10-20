# no_writer 根对象：0 个 CS 写方、无自身身份列（待定表去留）

由 `tools/report_no_writer.py` 生成，**不要手改**；改模型后重跑脚本。

`_overrides.json.no_writer` 共 **27** 个：**待裁决 0**（仍是 `PERSIST`、有表）+ **已裁决 25**（改判 `DERIVED`/`EVENT`/`CONFIG`/`TBD`，DDL 里没有表）+ **已并表退场 2**（对象已被 `fold` 折进别的对象）。

## 为什么这桶危险

它们都被 **SC 当顶层数组下发**（他人卡片 / 排行投影 / 战果附属 / 战斗期数组），
而建表口径只剩 `(world_id, pilot_id)`——数组元素按单行建表 = **静默压行**
（docs/05 §9.3）。0 个 CS 写方只是让问题**暂时**不发作：写方一落地就丢行。

裁决的三条出路（docs/05 §9.8 同口径）：

1. **孪生/子集** → `DERIVED`：行本来就在别的根表里（或能由它算出），退役副本表；
2. **战斗期数组** → `EVENT`：服务端每场重算，本就不该落库（`fire_point` 先例）；
3. **真有身份列** → 钉 `pk` 保留表（或 `inject_members` 补一列，同 `news` 的 `msg_id`）。

## 待裁决

| 对象 | 成员 | PK 类别 | 孪生根（非 no_writer） | 同批孪生 | 作为谁的成员 | 子集宿主 | 身份候选 | SC 读方 |
|---|---|---|---|---|---|---|---|---|

## 已裁决

| 对象 | 处置 | 理由 | 孪生根 |
|---|---|---|---|
| `bonus_event` | `CONFIG` | disposition=CONFIG（不建表）：**运营配置**：`bonus_event_now_update` 下发当期加成活动日程（`game_type`/`begin_time`/`end_time`/`main_priority`/`accump_rate`/`gp_rate`/`moneyup_rate`/`raredrop_rate`/`reward_num`…），按世界（或全服）一份、由运营排期，不是玩家状态。13 个费率/日程列在所有保留表里都没有娘家，也不该有——这属于 `srv.*` 运营态（本轮不建 `game.bonus_event`）。 | — |
| `bmgpack` | `DERIVED` | disposition=DERIVED（不建表）：商店在售商品的**读视图**（23B 元素，与 `item_list` 同一打印器 `sub_B4E110`、同一组列 `shopitem_id`+`gp_x01/gp_x10/cp_x01/cp_x10`+`bit_eff`+`stock`）：`pilot_list_get_r` 里下发的是「BGM 包在售清单」，主数据与价格/库存是运营态（`srv.shop_lineup` 一类），`bmgpack.shopitem_id`本来就被判为指向主数据的 `master` 引用。0 CS 写方 ⇒ 不成玩家维度表。 | `item_list` |
| `coop_room` | `DERIVED` | disposition=DERIVED（不建表）：房间列表的读视图：15 个成员名与根对象 `roominfo` 逐个相同（= `roominfo` 的线形），`btlroom_coop_roomlist_get_r` 下发的是「协同房列表」。房间本体的家在 `roominfo`，0 CS 写方 ⇒ 不成第二张房表。 | `roominfo` |
| `dcpoint_detail` | `DERIVED` | disposition=DERIVED（不建表）：结算面板里的**差值投影**：5 个成员名与根对象 `dc_point` 逐个相同（`bef_dcpoint`/`aft_dcpoint`/`is_dc`/`reward_item_ids`/`reward_item_nums`），`result_info` 是那场结算的回执。DC 点数的家是 `dc_point`（每个机师一行），0 CS 写方 ⇒ 不成第二张表。 | `dc_point` |
| `extrarule_xwar_info` | `DERIVED` | disposition=DERIVED（不建表）：大规模战扩展规则的**战斗侧副本**：7 个成员名与根对象 `xwar_ext_rule` 逐个相同（514B 同形），`battle-authenticate_r` 只是把开局参数回给客户端。真正的家在 `xwar_ext_rule`（机师预约选项，本批判单行保留）。 | `xwar_ext_rule` |
| `favms_add` | `DERIVED` | disposition=DERIVED（不建表）：**同一批行的结算增量形**：18 个成员名与元素复合体 `favms` 逐个相同，而行本身是`pilot_detail.favms_arr`（720 格，子表 `game.pilot_detail__favms_arr` 存 18 列）的元素。`result_info` 下发的是这一场加在哪几台机体上。行已有着落 ⇒ 不另建表。 | `favms` |
| `invite` | `DERIVED` | disposition=DERIVED（不建表）：「可邀请机师」的**分页查询结果**（`invite_count` + `page_now`/`page_max` + `sort_info`）：行=机师（`pilot_id`/`name`/`rank`/`mil_class`），`continued_login_days`/`is_bonus`/`vslocal_cnt`/`xwar_cnt`是筛选/加成用的**算出来的**值（连续登录天数、场次计数），`last_login`/`last_logout` 与 `pilot` 侧时间列同族（列名变体，留给 colname 批次）。0 CS 写方 ⇒ 不落库。 | — |
| `leaders` | `DERIVED` | disposition=DERIVED（不建表）：招募列表里的「队长条目」（7 成员）：行=机师（`pilot_id`/`name`/`level`/`avatar`/`rate_vslocal`），`is_leader`/`pstat` 是**队伍成员关系属性**，家在 `party_member`（本模型已有该表的同名成员）。0 CS 写方 ⇒ 不落库。 | — |
| `lpcard` | `DERIVED` | disposition=DERIVED（不建表）：氏族成员名片的**读视图**（113B / 20 成员，与 `friend_detail` 等同形）：20 列全是 `pilot` 并集的子集，而**成员关系可由 `pilot.clan_id` 推出**——「某氏族的成员」= 同 `clan_id` 的机师集合（`SC-0x…-clan_memberlist_get_r` 是查询，0 CS 写方）⇒ 行可派生，不建表。旧库把它按 `(world_id, 我, slot)` 存成每个请求者一份的副本（压行），批 18 起不再复刻。 | `block_detail`, `clan_member_card`, `friend_detail`, `friend_histories` |
| `member` | `DERIVED` | disposition=DERIVED（不建表）：房间成员条目（7 成员，与 `leaders` 同形）：行=机师，`is_leader`/`pstat` 是成员关系属性（`party_member` 有同名成员）。0 CS 写方 ⇒ 不落库。 | — |
| `member_info` | `DERIVED` | disposition=DERIVED（不建表）：「我自己的名片」（`SC-0x…-clan_info_get_self_r` 里的 `member_info`，113B / 20 成员）：行就是**我**这一行，20 列 ⊂ `pilot` 并集 ⇒ 由 `game.pilot` 投影，不另建表（0 CS 写方）。 | `block_detail`, `clan_member_card`, `friend_detail`, `friend_histories` |
| `rank_pilot` | `DERIVED` | disposition=DERIVED（不建表）：精英排行的查询投影（18 成员）：`ranking_elite_pilot_get_page_r` / 赛季命令。`is_regular`/`is_reserve`/`last_rank`/`last_score`/`season_class_lv`/`tm_upd` 是**赛季态**（`season_class_lv` 与 `pilot_detail.sc_lv_max` 同族；`msdeck` 是卡组引用，见 ref_stem 的 `msdeck` 一族），由赛季/排行服务按届算，不是机师行上的源列。0 CS 写方 ⇒ 不落库。 | — |
| `rank_pilot_light` | `DERIVED` | disposition=DERIVED（不建表）：精英排行轻量项（7 成员，`rank_pilot` 的子集）：同上，查询投影（含 `season_class_lv` 赛季态）。 | — |
| `ranking` | `DERIVED` | disposition=DERIVED（不建表）：排行项的**查询投影**（12 成员：`rank`/`score`/`pilot_id`/`clan_*`/`emb_*`/`avatar`/`level`/`troops`）：`ranking_pilot_get_r` 按分数排序取头部，名次与分数是查询时算出来的，不是机师的源数据列（`pilot`/`pilot_detail` 里没有 `score` 这一列）。0 CS 写方 ⇒ 不落库。 | — |
| `team_pilot` | `DERIVED` | disposition=DERIVED（不建表）：赛季队伍成员（5 成员：`pilot_id`/`name`/`level`/`avatar`/`world_id`）全是机师列，行=机师；队伍成员关系在 party 侧，0 CS 写方 ⇒ 查询投影。 | — |
| `toppilots` | `DERIVED` | disposition=DERIVED（不建表）：排行项：与 `ranking` 成员名序完全相同（孪生根），同一条 `ranking_pilot_get_r` 的「榜首」窗口。判同上。 | — |
| `funnel_snapshot_entry` | `EVENT` | disposition=EVENT（不建表）：战斗期快照元素（`ent_id`/`move_info`/`wslot_idx`）：孪生根 `funnelss` 已判 EVENT（同一场战斗的位置快照），0 CS 写方 ⇒ 不落库。 | `funnelss` |
| `mapgimmick_entry` | `EVENT` | disposition=EVENT（不建表）：战斗地图机关（`game_begin` 下发 23 列：`ent_id`/`ctrl_ent_id`/`gauge_max`/`msma_id*`/`param_*`/坐标）：服务端每场重算，0 CS 写方 ⇒ 不落库（同 `fire_point` 先例）。 | — |
| `parts_exec_entry` | `EVENT` | disposition=EVENT（不建表）：战斗部件效果执行（`eqparts_execute` 下发 6 列：`effect_catego`/`effect_msec`/`effect_param`/`effect_value*`/`item_id`）：一场内的执行记录，0 CS 写方 ⇒ 不落库。 | — |
| `respawn_post` | `EVENT` | disposition=EVENT（不建表）：战斗重生点进度（`game_respawn_post_update` 下发 9 列：`gauge_A/B`/`conquer_remain_sec`/`is_keep`/`is_visible`/`near_ms_num`/`team`…）：每场战斗的实时进度，0 CS 写方 ⇒ 不落库。 | — |
| `respawn_post_entry` | `EVENT` | disposition=EVENT（不建表）：战斗重生点初始形（`game_begin` 下发 16 列：坐标/`group_id`/`npc_ba_point_*`/`param1/2`）：与 `respawn_post` 同族的战斗期数组，0 CS 写方 ⇒ 不落库。 | — |
| `result_detail` | `EVENT` | disposition=EVENT（不建表）：战斗结算详情（`result_info` 下发 80 列：`badge_*`/`fight_ms_*`/`expup_*`/`moneyup_*`/`itm_*`/`cnt_*`…）：一场的战斗回执，属于 B6 的战斗持久化议题（docs/05 §4.C/§9），0 CS 写方 ⇒ 本轮不落库。 | — |
| `result_wave` | `EVENT` | disposition=EVENT（不建表）：波段结果元素（10 列）：`wave_res`（同族，已判 EVENT）的结算窗口，同属战斗回执，0 CS 写方 ⇒ 不落库。 | — |
| `score_ranking` | `EVENT` | disposition=EVENT（不建表）：战果排行项（`result_info` 下发 19 列：`kill_cnt`/`atk_point`/`con_point`/`spt_point`/`last_msma`/`last_weapon`…）：一场的得分榜，0 CS 写方 ⇒ 不落库。 | — |
| `support_spot` | `EVENT` | disposition=EVENT（不建表）：战斗支援地点（`commander_support_spot_notice` 下发 11 列：`route_no`/`pos_*`/`dir`/`team`/`stat`/`ai_priority`）：一场的指挥官指令目标，0 CS 写方 ⇒ 不落库。 | — |

## 已并表退场（`fold`：十个线形 → 一个对象）

| 对象 | 并入 | 依据 |
|---|---|---|
| `pcard` | `pilot` | 列不丢：成员并进宿主对象（`_overrides.json.fold` 逐条带理由） |
| `pilots_list` | `pilot` | 列不丢：成员并进宿主对象（`_overrides.json.fold` 逐条带理由） |

## 备注

- 「孪生根」= 成员名序**完全相同**的非 no_writer 对象：同一张线形被两个对象各建一张
  表，写方落到哪张另一张就是副本（`c4j` 的 `unlockw` 即此类，处置见 docs/05 §9.8）。
- 「子集宿主」= 成员集是别人真子集（或前 5 个成员同序）：同一批行的一个窗口。
- 「身份候选」只是命名候选：`*_id` 多半是**指向别人**的引用（`docs/05 §4.B`），
  钉成 PK 前先证明它是**自己的**记录号。
- 裁决写 `_overrides.json.disposition`（`DERIVED`/`EVENT`/`CONFIG`/`TRANSIENT` 之一）
  或 `pk`；引擎据此清掉 `table` 并落 `no_table_reason`（非 PERSIST 不建表，
  `verify_no_blob.py` 复核）。
