# 归位复核批次 · pk

> 根对象无行键：判定对象自己的记录号（或确认只能 (world_id,pilot_id) 单行）

待判 **33** 项。裁决写回 `schema/homing/_overrides.json`，然后 `python tools/review_homing.py --check`。

| 对象 | 成员数 | 候选身份成员 | 折入线布局 |
|---|---|---|---|
| `bmgpack` | 7 | `shopitem_id` | bmgpack |
| `bonus_event` | 16 | - | bonus_event |
| `bracket` | 2 | - | bracket |
| `cinfo` | 25 | `clan_id`, `leader_id`, `npc_id` | cinfo |
| `dailycup_conf` | 14 | `extrule_id`, `tournament_id` | dailycup_conf, dailycup_conf_next |
| `dc_point` | 7 | - | dc_point, dcpoint_detail |
| `eq_bonus_modules_lot` | 3 | - | eq_bonus_modules_lot |
| `evflag3` | 1 | - | evflag3 |
| `ext_subrule` | 2 | - | ext_subrule |
| `fire_point` | 3 | - | fire_point |
| `funnel_snapshot_entry` | 3 | `ent_id` | funnel_snapshot_entry |
| `intro_info` | 4 | - | intro_info |
| `item_list` | 7 | `shopitem_id` | item_list |
| `mapgimmick_entry` | 23 | `ctrl_ent_id`, `ent_id`, `msma_id` | mapgimmick_entry |
| `order` | 5 | - | order, ranking_info |
| `parts_exec_entry` | 6 | `item_id` | parts_exec_entry |
| `pbadge` | 1 | - | pbadge |
| `phase_info` | 4 | - | phase_info |
| `pilot_detail` | 53 | `check_progress_quest_id`, `clan_id`, `cupteam_id`, `heroms_uniqid`, `monthly_bonus_holding_id`, `rokaku_space_uniq_msid`, `rokaku_uniq_msid` | pilot_detail |
| `precord` | 61 | - | precord |
| `rankself` | 6 | - | rankself, special_a_info |
| `recruit` | 7 | `channel_id`, `party_id` | recruit |
| `recruits` | 9 | `channel_id`, `party_id` | recruits |
| `rental_module` | 2 | `module_id` | rental_module |
| `respawn_post` | 9 | - | respawn_post |
| `respawn_post_entry` | 16 | `group_id`, `npc_ba_point_ent_id`, `post_chara_id` | respawn_post_entry |
| `result_detail` | 80 | `fight_ms_uniqid`, `itm_id`, `no_fight_ms_uniqid`, `use_buffitem_id` | result_detail |
| `result_wave` | 10 | - | result_wave |
| `season_rb_conf` | 10 | `mission_id`, `tournament_id` | season_rb_conf |
| `sort_info` | 12 | - | sort_info, sort_info_invite |
| `support_spot` | 11 | - | support_spot |
| `wbonus` | 3 | - | wbonus |
| `xwar_ext_rule` | 7 | - | extrarule_xwar_info, xwar_ext_rule |

裁决写法：`"pk": {"<对象>": ["<成员>"]}`；确认只能单行则写 `"pk": {"<对象>": []}` 并在 `note` 里说明。
