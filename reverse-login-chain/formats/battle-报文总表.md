# 战服（battle）报文总表 —— `_proto_battle_client`

> 自动提取：`reverse-login-chain/tools/dump_battle_protocol.py`（IDA，2026-09-15）。
> 机读版：`battle_protocol_raw.json`。字段**顺序**来自客户端自动生成的 dump 拼接（可靠）；
> `类型` 是 dump 助手给出的**线索**（i32/i16/u8/i64/var），**体长与精确类型需逐条反编译 parse 段确认**。
> ★**体长**见 `battle-体长线索.md`：**143/205** 条已三重验证为定长（可直接造包），其余 62 条（含变长串/数组/复合）待人工。

## 0. 概览

| 项 | 值 |
|---|---|
| 收包分发器 | `sub_B0CC20`（0xb0cc20..0xb317df）|
| S→C（recv） | **205** 条（有 ID 205） |
| C→S（send） | **92** 条（有 ID 92） |
| 其它类 `_proto_battle` | 2 条（entity_msma_fix 收发）|
| ID 区间 | recv 0x0120..0xFEBB ／ send 0x0372..0xFBC1 |

## 1. ★ 战服 MVP 必做的报文（按流程）

**握手**
- `proto_version_check_r` **0xDE24** 闸门=1 字段: version:i32 | crc:? | gentime:i32
- `authenticate_r` **0xA5DA** 闸门=3 字段: result:i32 | room_id:i32 | room_name:? | mission_id:i32 | extrule_id:i32 | dc_node_id:i32 | is_rankerbattle:i32 | map_id:i32 | is_vsclan:u8/bool | comeback_stat:i32 | is_playing:u8/bool | is_netcafe:u8/bool | team:u8/bool | is_practice:u8/bool | config:? | progress:? | expup_fgauge:i16/u16 | is_ev_caravan:u8/bool | flag_wideuse:u8/bool | extrarule_xwar_info:i32
- `cpf_authenticate` **0xBA73** 闸门=283 字段: data[]:i32
- `cpf_authenticate_error` **0x2C60** 闸门=285 字段: result:i32

**大厅/房间**
- `roomlobby_pilot_add` **0xBDD6** 闸门=4 字段: team:u8/bool | troops:u8/bool | world_id:i32 | pilot:? | stat:i32 | is_commander:u8/bool | is_audience:u8/bool | member_index:u8/bool | dtaskf_order_number:u8/bool | kill_count:i32 | death_count:i32
- `roomlobby_pilot_del` **0xC64E** 闸门=6 字段: world_id:i32 | pilot_id:i32
- `roomlobby_pilot_mindex_update_r` **0x0B3E** 闸门=11 字段: result:i32 | world_id:i32 | pilot_id:i32 | member_index:u8/bool | is_commander:u8/bool
- `roomlobby_game_ready_r` **0x339C** 闸门=19 字段: result:i32 | world_id:i32 | pilot_id:i32 | stat:i32
- `roomlobby_game_start_r` **0x7206** 闸门=21 字段: result:i32 | elapsed_sec:i32 | limit_sec:i32 | kill_count:i32 | death_count:i32
- `roomlobby_exit_r` **0x14C5** 闸门=23 字段: -
- `room_chat_down` **0x12EC** 闸门=40 字段: team:u8/bool | troops:u8/bool | world_id:i32 | pilot_id:i32 | pilot_name:? | msg:? | is_all:u8/bool | is_party:u8/bool | is_audience:u8/bool
- `room_kick_vote_r` **0x27F3** 闸门=47 字段: result:i32

**开局/生成**
- `game_begin` **0x1365** 闸门=50 字段: snapshot_int_msec:i32 | snapshot_res_msec:i32 | pos_factor:i32 | map_id:i32 | btlfield:i32 | clear_remain_msec:i32 | is_disable_conq_sp:u8/bool | is_room_suspend:u8/bool | mission_id:i32 | sudden_type:i32 | sudden_bonus_target:i32 | exp_min:i32 | exp_max:i32 | config:? | progress:? | respawn_posts[]:? | mapgimmicks[]:? | bgm_desc:? | missionunit_set[]:i32 | mission_phase:i32
- `msma_spawn_list_get_r_begin` **0x9951** 闸门=71 字段: spawn1st_post:i32 | is_1st:i32
- `msma_spawn_list_get_r_end` **0xAB6F** 闸门=73 字段: -
- `msma_spawn_select_r` **0x86B2** 闸门=76 字段: result:i32 | ms_index:i32 | post_index:i32 | spt_spot_index:i32 | respawn_ent_id:i16/u16 | script_ini:i32
- `msma_spawn_warp_start_r` **0xFEBB** 闸门=79 字段: result:i32 | is_cancel:i32 | ent_id:i16/u16 | countdown_msec:i32
- `msma_spawn_wait_update` **0x8DE4** 闸门=74 字段: deck_index:u8/bool | respawn_wait_sec:i16/u16 | respawn_wait_max:i16/u16
- `entity_deploy_arms_appear` **0x057A** 闸门=85 字段: appear_info:i32

**移动/状态同步**
- `entity_snapshot` **0x568A** 闸门=97 字段: frame_count:i32 | remain_msec:i32 | snapshots[]:i32
- `entity_snapshot_splitdelta_compress` **0xBAE4** 闸门=99 字段: frame_count:i32 | remain_msec:i32 | zbuff[]:i32
- `pos_warp_force` **0xC327** 闸门=106 字段: ent_id:i16/u16 | pos_x:i16/u16 | pos_y:i16/u16 | pos_z:i16/u16 | dir:i16/u16 | reason:i16/u16
- `entity_msma_reborn` **0x1EA5** 闸门=89 字段: ent_id:i16/u16 | hp_percent:i16/u16
- `entity_msma_hide` **0x130A** 闸门=92 字段: ent_id:i16/u16
- `entity_msma_disappear` **0x0943** 闸门=87 字段: ent_id:i16/u16 | reason:i32 | not_use:i16/u16
- `weapon_state_update` **0x0825** 闸门=115 字段: ent_id:i16/u16 | weapon_state:i16/u16 | weapon_change_flag:i16/u16
- `active_weapon_change_r` **0xB334** 闸门=112 字段: ent_id:i16/u16 | result:i32 | equip_index:u8/bool | equip_itemid:i32 | is_force:u8/bool
- `eqparts_toggle` **0xCE08** 闸门=164 字段: ent_id:i16/u16 | group_id:i32 | toggle:i16/u16 | reason:i32

**命中/伤害/死亡**
- `weapon_hit_from` **0x49C6** 闸门=158 字段: ent_id:i16/u16 | from_ent_id:i16/u16 | weapon_itemid:i32 | charge_lv:u8/bool | hp_now:i32 | hp_max:i32 | damage:i32 | spbits:i32 | hit_pos_x:i16/u16 | hit_pos_y:i16/u16 | hit_pos_z:i16/u16 | hit_dir:i16/u16 | body_region:i16/u16 | optbits:i32 | shield_hp_now:i32
- `weapon_hit_from_with_stumble` **0xE332** 闸门=160 字段: ent_id:i16/u16 | hit_dir:i16/u16 | spbits:i32 | optbits:i32 | stumble_power:i16/u16 | stumble_msec:i16/u16
- `weapon_hit_from_with_tumble` **0xA8F2** 闸门=159 字段: ent_id:i16/u16 | hit_dir:i16/u16 | spbits:i32 | optbits:i32 | down_power:i16/u16 | down_msec:i16/u16
- `weapon_hit_from_with_module` **0x8EFD** 闸门=162 字段: ent_id:i16/u16 | module_hp:i32 | is_force:u8/bool
- `weapon_hit_to_r` **0xDDF7** 闸门=156 字段: weapon_itemid:i32 | ent_id:i16/u16 | optbit:i32 | hit_pos_x:i16/u16 | hit_pos_y:i16/u16 | hit_pos_z:i16/u16
- `shield_any_damage` **0xF4D7** 闸门=296 字段: ent_id:i16/u16 | damage:i32
- `entity_msma_show_hp` **0xE4DB** 闸门=95 字段: ent_id[]:i16/u16 | hp_max[]:i32 | gauge_max:i32
- `entity_msma_dead` **0x9105** 闸门=88 字段: ent_id_dead:i16/u16 | world_id_kill:i32 | pilot_id_kill:i32 | decal_kill:i32 | weapon_itemid:i32 | repair_wait_sec:i16/u16 | kill_streak_count:i16/u16 | spbits:i32 | is_resurrect:u8/bool | is_extend_style_change_limit:u8/bool
- `module_toggle_point` **0xE2DE** 闸门=293 字段: ent_id:i16/u16 | point:i16/u16 | point_max:i16/u16
- `module_toggle_level` **0xDDE9** 闸门=295 字段: ent_id:i16/u16 | level_up_flag:i32 | next_level_max:i32
- `module_toggle_time` **0xD8B9** 闸门=294 字段: ent_id:i16/u16 | msec:i32 | rate:i16/u16
- `system_message` **0xB313** 闸门=286 字段: msg:? | color:i32

**得分/进度**
- `score_update` **0x8D59** 闸门=172 字段: reason:i32 | point_gain:i16/u16 | point_total:i32 | is_taskforce_aux:i16/u16 | point_atk:i32 | point_spt:i32 | point_con:i32 | kill_streak_chain_num:i32
- `score_update_coopwave` **0x0BCE** 闸门=173 字段: reason:i32 | world_id:i32 | pilot_id:i32 | point_gain:i16/u16 | point_total:i32 | n_cont_kill:i16/u16 | bonus_cont_kill:i16/u16
- `kill_count_update` **0x844B** 闸门=171 字段: reason:i32 | ent_id_dead:i16/u16 | world_id_kill:i32 | pilot_id_kill:i32 | kill_streak:i32 | weapon_itemid:i32 | is_extend_style_change_limit:u8/bool
- `mission_goal_text` **0xEAB3** 闸门=268 字段: text:i32
- `game_mission_progress_update` **0x3E23** 闸门=64 字段: mprogress:i32
- `game_round_end` **0xC66B** 闸门=54 字段: win_team:u8/bool | win_troops:u8/bool | progress:i32
- `battle_contribute_rank` **0xEB53** 闸门=175 字段: rank:i32
- `game_score_ranker_notice` **0xCDE6** 闸门=68 字段: -

## 2. S→C 全表（服务端必须能发）

| # | ID | 报文名 | 闸门 | 字段（序） |
|---|---|---|---|---|
| 1 | `0x0120` | entity_msma_show | 93 | ent_id:i16/u16 |
| 2 | `0x02D8` | combat_operation_container_collect_r | 244 | ent_id:i16/u16 | result:i32 |
| 3 | `0x03CC` | weapon_fire__air_bomb_r | 134 | ent_id:i16/u16 | itemid:i32 | airbomb_id:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | shot0_drop1_impact2:u8/bool | fx_opt:u8/bool |
| 4 | `0x049D` | wrestle_chase_move_start_r | 299 | ent_id:i16/u16 | itemid:i32 | dir_h:i16/u16 | wrestle_id:i32 | target_ent_id:i16/u16 | target_pos_x:i16/u16 | target_pos_y:i16/u16 | target_pos_z:i16/u16 |
| 5 | `0x056D` | battleship_cooltime_notice | 258 | to_ent_id:i16/u16 | remain_msec:i32 |
| 6 | `0x057A` | entity_deploy_arms_appear | 85 | appear_info:i32 |
| 7 | `0x07E9` | room_kick_vote_get_enable_pilots_r | 49 | enable_worlds[]:i32 | enable_pilots[]:i32 | result:i32 |
| 8 | `0x0825` | weapon_state_update | 115 | ent_id:i16/u16 | weapon_state:i16/u16 | weapon_change_flag:i16/u16 |
| 9 | `0x0943` | entity_msma_disappear | 87 | ent_id:i16/u16 | reason:i32 | not_use:i16/u16 |
| 10 | `0x0B3E` | roomlobby_pilot_mindex_update_r | 11 | result:i32 | world_id:i32 | pilot_id:i32 | member_index:u8/bool | is_commander:u8/bool |
| 11 | `0x0BCE` | score_update_coopwave | 173 | reason:i32 | world_id:i32 | pilot_id:i32 | point_gain:i16/u16 | point_total:i32 | n_cont_kill:i16/u16 | bonus_cont_kill:i16/u16 |
| 12 | `0x0C5F` | commander_candidacy_start | 214 | remain_sec:i16/u16 |
| 13 | `0x0E85` | commander_list_get_r | 210 | result:i32 | commander_id[]:i32 |
| 14 | `0x0EC5` | room_kick_to | 45 | - |
| 15 | `0x1113` | game_script_play | 61 | src:? | is_with_resume:u8/bool | script_thread:u8/bool |
| 16 | `0x1159` | game_mapgimmick_update | 66 | gimmick_progress[]:i32 |
| 17 | `0x1165` | msma_AI_uninstall | 182 | AI_ent_id:i16/u16 |
| 18 | `0x12EC` | room_chat_down | 40 | team:u8/bool | troops:u8/bool | world_id:i32 | pilot_id:i32 | pilot_name:? | msg:? | is_all:u8/bool | is_party:u8/bool | is_audience:u8/bool |
| 19 | `0x130A` | entity_msma_hide | 92 | ent_id:i16/u16 |
| 20 | `0x1365` | game_begin | 50 | snapshot_int_msec:i32 | snapshot_res_msec:i32 | pos_factor:i32 | map_id:i32 | btlfield:i32 | clear_remain_msec:i32 | is_disable_conq_sp:u8/bool | is_room_suspend:u8/bool | mission_id:i32 | sudden_type:i32 | sudden_bonus_target:i32 | exp_min:i32 | exp_max:i32 | config:? | progress:? | respawn_posts[]:? | mapgimmicks[]:? | bgm_desc:? | missionunit_set[]:i32 | mission_phase:i32 |
| 21 | `0x14C5` | roomlobby_exit_r | 23 | - |
| 22 | `0x16AA` | eqparts_execute | 163 | ent_id:i16/u16 | parts_exec[]:i32 |
| 23 | `0x1A13` | weapon_fire__hand_throw_r | 126 | ent_id:i16/u16 | itemid:i32 | grenade_id:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | shot0_impact1:u8/bool | fx_opt:u8/bool | charge_lv:u8/bool |
| 24 | `0x1B32` | rideable_msma_ride | 259 | result:i32 | access_type:i16/u16 | from_world_id:i32 | from_pilot_id:i32 | from_ent_id:i16/u16 | to_ent_id:i16/u16 | hp_now:i32 | hp_max:i32 |
| 25 | `0x1B67` | funnel_snapshot_all | 150 | snapshot_arr[]:i32 |
| 26 | `0x1BB4` | commander_support_countdown | 230 | ent_id:i16/u16 | support_type:i32 | team:u8/bool | troops:u8/bool | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | count:i16/u16 | is_hit_send:u8/bool |
| 27 | `0x1E0F` | preset_voice_down | 101 | ent_id:i16/u16 | voice_id:i32 | voice_volume:u8/bool | is_cutin:u8/bool | is_party:u8/bool | is_use_textmsg:u8/bool | textmsg:i32 |
| 28 | `0x1E2F` | msma_spawn_list_get_r_one | 72 | index:i32 | ms:i32 |
| 29 | `0x1EA5` | entity_msma_reborn | 89 | ent_id:i16/u16 | hp_percent:i16/u16 |
| 30 | `0x1EC7` | battleship_get_down_r | 255 | result:i32 | to_ent_id:i16/u16 |
| 31 | `0x1ED8` | roomlobby_ban_vote_cancel_r | 27 | result:i32 |
| 32 | `0x214C` | commander_support_rendition_end | 229 | team:u8/bool | troops:u8/bool | support_type:i32 | spt_spot_index:u8/bool |
| 33 | `0x243B` | game_btlfield_change | 51 | btlfield:i32 |
| 34 | `0x26E9` | commander_select_tell | 213 | team:u8/bool | troops:u8/bool | commander_id:i32 |
| 35 | `0x26F8` | xwar_commander_subcmdr_lot_r | 236 | is_lot:u8/bool |
| 36 | `0x27F3` | room_kick_vote_r | 47 | result:i32 |
| 37 | `0x2B4D` | setmsparam | 289 | ent_id:i32 | val:i32 | type:i32 |
| 38 | `0x2C60` | cpf_authenticate_error | 285 | result:i32 |
| 39 | `0x2D27` | area_over_penalty_countdown | 302 | ent_id:i16/u16 | limit_msec:i32 | elapsed_msec:i32 |
| 40 | `0x30A9` | roomlobby_ban_vote_result | 32 | state:i32 | vote_count[]:i32 | ban_msma_id[]:i32 | member_count:i32 |
| 41 | `0x315C` | roomlobby_xwar_commander_lot_r | 15 | result:i32 | is_lot:u8/bool | lot_count:i16/u16 |
| 42 | `0x3298` | msma_spawn_force_warp_start | 80 | ent_id:i16/u16 | countdown_msec:i32 |
| 43 | `0x339C` | roomlobby_game_ready_r | 19 | result:i32 | world_id:i32 | pilot_id:i32 | stat:i32 |
| 44 | `0x3638` | msma_AI_move_stuckescape_r | 198 | AI_ent_id:i16/u16 | to_x:i16/u16 | to_y:i16/u16 | to_z:i16/u16 | msec:i16/u16 |
| 45 | `0x377D` | bullet_supply | 201 | percent_val:i16/u16 | equip_idx:i16/u16 |
| 46 | `0x37C1` | weapon_fire__for_myself_r | 144 | ent_id:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | begin1_end0:u8/bool |
| 47 | `0x39B3` | msma_AI_update_move_end | 191 | AI_ent_id:i16/u16 | end_x:i16/u16 | end_y:i16/u16 | end_z:i16/u16 |
| 48 | `0x3BBE` | room_chat_editing_r | 42 | world_id:i32 | pilot_id:i32 | is_editing:u8/bool |
| 49 | `0x3C70` | mission_safety_area_return_to_area | 303 | ent_id:i16/u16 |
| 50 | `0x3E07` | commander_subcmdr_candidacy_end | 239 | - |
| 51 | `0x3E23` | game_mission_progress_update | 64 | mprogress:i32 |
| 52 | `0x412B` | cutin_down | 104 | ent_id:i16/u16 | cutin_category_id:i32 |
| 53 | `0x45FC` | weapon_hit_from_with_staggery | 161 | ent_id:i16/u16 | hit_dir:i16/u16 | spbits:i32 | optbits:i32 | staggery_power:i16/u16 | staggery_msec:i16/u16 |
| 54 | `0x47C2` | conquer_spoint_change | 265 | conquer:i32 |
| 55 | `0x483F` | dynamic_taskforce_order_result | 251 | result:i32 | order_index:u8/bool | order_number:u8/bool | order_kind:u8/bool | order_param:i32 |
| 56 | `0x49C6` | weapon_hit_from | 158 | ent_id:i16/u16 | from_ent_id:i16/u16 | weapon_itemid:i32 | charge_lv:u8/bool | hp_now:i32 | hp_max:i32 | damage:i32 | spbits:i32 | hit_pos_x:i16/u16 | hit_pos_y:i16/u16 | hit_pos_z:i16/u16 | hit_dir:i16/u16 | body_region:i16/u16 | optbits:i32 | shield_hp_now:i32 |
| 57 | `0x4C36` | rideable_msma_get_down_r | 261 | result:i32 | access_type:i16/u16 | from_ent_id:i16/u16 | to_world_id:i32 | to_pilot_id:i32 | to_ent_id:i16/u16 | hp_now:i32 | hp_max:i32 |
| 58 | `0x4C7D` | entity_msma_unattended_state | 96 | ent_id:i16/u16 | state_bit:i16/u16 |
| 59 | `0x4D96` | game_client_signal_r | 60 | sigval:i32 |
| 60 | `0x4E9F` | weapon_fire__shot_single_special_r | 119 | ent_id:i16/u16 | itemid:i32 |
| 61 | `0x4FCE` | msma_AI_move_stuckescape_end | 199 | AI_ent_id:i16/u16 |
| 62 | `0x501D` | commander_support_debug_cooltime_end | 234 | - |
| 63 | `0x5080` | msma_AI_suspend | 184 | AI_ent_id:i16/u16 |
| 64 | `0x5092` | commander_support_spot_notice | 221 | support_spots[]:i32 |
| 65 | `0x5157` | access_state | 206 | to_ent_id:i16/u16 | from_ent_id:i16/u16 | remain_msec:i32 |
| 66 | `0x54C6` | dynamic_taskforce_info_update | 247 | order_all_number[]:u8/bool | order_all_kind[]:u8/bool | order_all_param[]:i32 | members_order_idx[]:u8/bool | npc_entid[]:i16/u16 | npc_order_index[]:u8/bool | party_worldid:i32 | party_pilotid:i32 |
| 67 | `0x54DD` | msma_AI_set_fire_area | 194 | AI_ent_id:i16/u16 | fire_sx:i16/u16 | fire_sy:i16/u16 | fire_sz:i16/u16 | fire_ex:i16/u16 | fire_ey:i16/u16 | fire_ez:i16/u16 | end_x:i16/u16 | end_y:i16/u16 | end_z:i16/u16 |
| 68 | `0x553F` | commander_support_gauge_update | 223 | gauge_val:i32 | no_complement:u8/bool |
| 69 | `0x568A` | entity_snapshot | 97 | frame_count:i32 | remain_msec:i32 | snapshots[]:i32 |
| 70 | `0x56CF` | commander_support_hit_from | 232 | support_type:i32 | ent_id:i16/u16 | hp_now:i32 | hp_max:i32 | spbits:i32 | hit_dir:i16/u16 |
| 71 | `0x58FC` | commander_order_assist_r | 220 | type:u8/bool |
| 72 | `0x5913` | roomlobby_roommaster_notice | 12 | world_id:i32 | pilot_id:i32 |
| 73 | `0x5B98` | battleship_limittime_notice | 257 | to_ent_id:i16/u16 | limit_msec:i32 |
| 74 | `0x5C4F` | entity_msma_detach | 91 | ent_id:i16/u16 |
| 75 | `0x5D2A` | roomlobby_clan_notice | 16 | team:u8/bool | troops:u8/bool | clan_id:i32 | clan_name:? | clan_emb_base:u8/bool | clan_emb_parts1:u8/bool | clan_emb_parts2:u8/bool |
| 76 | `0x5EEA` | entity_snapshot_splitdelta | 98 | frame_count:i32 | remain_msec:i32 | ent_id[]:i16/u16 | dirty_bits[]:i16(2B) | pos_real_x[]:i16/u16 | pos_real_y[]:i16/u16 | pos_real_z[]:i16/u16 | pos_diff_x[]:u8/bool | pos_diff_y[]:u8/bool | pos_diff_z[]:u8/bool | dir[]:? | target_real_x[]:i16/u16 | target_real_y[]:i16/u16 | target_real_z[]:i16/u16 | target_diff_x[]:i16/u16 | target_diff_y[]:i16/u16 | target_diff_z[]:i16/u16 | spbit_ll[]:? | spbit_l[]:? | spbit_h[]:? | spbit_hh[]:? | spbit2[]:i16(2B) | hp_percent[]:u8/bool | hp_percent_shield[]:u8/bool | down_power[]:i16/u16 | equip_index[]:u8/bool | score1[]:i16/u16 | water_index[]:u8/bool | score2[]:i16/u16 | layer_index[]:u8/bool | score3[]:i16/u16 | rideon_ent_id[]:i16/u16 | lockon_ent_id[]:i16/u16 |
| 77 | `0x5F32` | bullet_supply_per_weapon_slot | 203 | supplyer_end_id:i16/u16 | supply_amount_per_weapon_slot[]:i16/u16 |
| 78 | `0x6059` | check_progress_quest_r | 277 | check_quest:i32 |
| 79 | `0x611B` | game_script_play_also_replay | 62 | src:? | script_thread:u8/bool |
| 80 | `0x6295` | combat_operation_start | 241 | team:u8/bool | troops:u8/bool | support_type:i32 | remain_msec:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | use_worldid:i32 | use_pilotid:i32 |
| 81 | `0x640D` | msma_spawn_info_prestart | 77 | remain_sec:i32 | mstype[]:u8/bool | post_index[]:i16/u16 | spt_spot_index[]:i16/u16 | stghold_entid[]:i16/u16 |
| 82 | `0x6411` | gm_camera_change_r | 282 | type:u8/bool | args:i16/u16 |
| 83 | `0x645D` | module_val_update | 292 | ent_id:i16/u16 | val:i16/u16 | val2:i16/u16 |
| 84 | `0x6475` | game_coopwave_result | 53 | wave_res:i32 |
| 85 | `0x6735` | deliver_oration | 263 | voice_id:i32 | elap_msec:i32 |
| 86 | `0x6A0F` | roomlobby_vote_get_comeback | 38 | state:i32 | msma_id[]:i32 |
| 87 | `0x6A38` | roomlobby_pilot_level_update | 9 | world_id:i32 | pilot_id:i32 | lv_old:i16/u16 | lv_new:i16/u16 |
| 88 | `0x6A8D` | roomlobby_xwar_countdown | 13 | sec:i32 |
| 89 | `0x6B2C` | roomlobby_cupteam_notice | 17 | team:u8/bool | cupteam_id:i32 | cupteam_rate:i32 | tournament_vs_type:i32 |
| 90 | `0x6B71` | roomlobby_vote_state | 37 | state:i32 | sec:i32 |
| 91 | `0x6D20` | weapon_fire__deploy_arms_r | 132 | ent_id:i16/u16 | itemid:i32 | arms_id:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | target_ent_id:i16/u16 | state:u8/bool | fx_opt:u8/bool | judge_worldid:i32 | judge_pilotid:i32 |
| 92 | `0x6D4B` | commander_subcmdr_notice | 240 | worldids[]:i32 | pilotids[]:i32 |
| 93 | `0x6D8F` | commander_support_debug_end | 228 | team:u8/bool | troops:u8/bool | support_type:i32 | ent_id:i16/u16 | spt_ms_index:i16/u16 | spt_spot_index:u8/bool |
| 94 | `0x7155` | roomlobby_pilot_add_npc | 5 | team:u8/bool | troops:u8/bool | pilot_id:i32 | level:i16/u16 | cutin_id:i32 | name:? | gender:u8/bool | platoon:u8/bool | platoon_slot:u8/bool | is_platoon_leader:u8/bool | dtaskf_order_number:u8/bool | is_disable_scoreboard:u8/bool |
| 95 | `0x717D` | entity_msma_appear | 84 | team:u8/bool | troops:i32 | world_id:i32 | pilot_id:i32 | ms:? | snapshot:? | funnelss:? | unattended_state_bit:i16/u16 | weapon_state_bits:i16/u16 | target_icon:u8/bool | is_respawn:u8/bool | is_using_ss:u8/bool | stghold_number:u8/bool | xweapon_fired:u8/bool |
| 96 | `0x7206` | roomlobby_game_start_r | 21 | result:i32 | elapsed_sec:i32 | limit_sec:i32 | kill_count:i32 | death_count:i32 |
| 97 | `0x731C` | weapon_fire__start_homing_r | 130 | grenade_id:i32 | pos_x:i16/u16 | pos_y:i16/u16 | pos_z:i16/u16 | target_ent_id:i16/u16 |
| 98 | `0x73CE` | entity_msma_attach | 90 | ent_id:i16/u16 | attach_parent_ent_id:i16/u16 | attach_socket:? | attach_pos_x:i16/u16 | attach_pos_y:i16/u16 | attach_pos_z:i16/u16 |
| 99 | `0x747B` | weapon_fire__chain_mine | 146 | from_ent_id:i16/u16 | to_ent_id:i16/u16 | weapon_itemid:i32 | fire_id:i32 |
| 100 | `0x759C` | deliver_assault_stghold_ace_status | 264 | team:u8/bool | troops:u8/bool | ent_id:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | spt_spot_index:u8/bool | spt_spot_dir:i16/u16 | remain_msec:i32 |
| 101 | `0x7621` | entity_msma_appear_self | 83 | team:u8/bool | troops:u8/bool | ms:? | snapshot:? | funnelss:? | hp_now:i32 | hp_max:i32 | shield_hp_now:i32 | shield_hp_max:i32 | weapon_state_bits:i16/u16 |
| 102 | `0x7626` | netcafe_challenge_progress_r | 275 | netcafe_challenge_info[]:i32 |
| 103 | `0x7C83` | map_event_fog_change | 279 | nearz:i32 | farz:i32 | color_r:? | color_g:? | color_b:? | time:i32 | elapsed_time:i32 |
| 104 | `0x7CD8` | commander_support_end | 227 | team:u8/bool | troops:u8/bool | support_type:i32 | ent_id:i16/u16 | spt_ms_index:i16/u16 | spt_spot_index:u8/bool |
| 105 | `0x7CE0` | msma_AI_update_order | 195 | AI_ent_id:i16/u16 | kind:u8/bool | param:i32 |
| 106 | `0x7D22` | chara_effect | 297 | ent_id:i16/u16 | effect_id:i16/u16 | is_start:u8/bool |
| 107 | `0x7D59` | roomlobby_pick_vote_result | 34 | state:i32 | vote_count[]:i32 | pick_msma_id[]:i32 | member_count:i32 |
| 108 | `0x8043` | tumble_ukemi_r | 108 | ent_id:i16/u16 | tmp:i32 |
| 109 | `0x80E8` | commander_support_cooltime_notice | 233 | support_type:i32 | remain_msec:i32 | target_change_msec:i32 |
| 110 | `0x8297` | game_resume | 57 | - |
| 111 | `0x844B` | kill_count_update | 171 | reason:i32 | ent_id_dead:i16/u16 | world_id_kill:i32 | pilot_id_kill:i32 | kill_streak:i32 | weapon_itemid:i32 | is_extend_style_change_limit:u8/bool |
| 112 | `0x84A5` | weapon_fire__wrestle_counter_r | 122 | ent_id:i16/u16 | itemid:i32 | target_ent_id:i16/u16 |
| 113 | `0x86B2` | msma_spawn_select_r | 76 | result:i32 | ms_index:i32 | post_index:i32 | spt_spot_index:i32 | respawn_ent_id:i16/u16 | script_ini:i32 |
| 114 | `0x894B` | weapon_fire__destruct | 142 | ent_id:i16/u16 | weapon_itemid:i32 |
| 115 | `0x8A10` | setwpnparam | 290 | ent_id:i32 | val:? | type:i32 |
| 116 | `0x8C24` | roomlobby_pick_vote_cancel_r | 31 | result:i32 |
| 117 | `0x8D1F` | commander_support_spot_lock | 222 | index:u8/bool | is_lock:u8/bool |
| 118 | `0x8D3C` | weapon_hit_chain_mine | 157 | weapon_itemid:i32 | to_ent_id:i16/u16 | from_ent_id:i16/u16 | hit_pos_x:i16/u16 | hit_pos_y:i16/u16 | hit_pos_z:i16/u16 |
| 119 | `0x8D42` | game_mapeffect_update | 67 | fx_id:i32 | is_scale:u8/bool |
| 120 | `0x8D58` | eqparts_ready_start_r | 166 | result:i32 | frame_count:i32 | AI_ent_id:i16/u16 | group_id:i16/u16 | reason:i32 |
| 121 | `0x8D59` | score_update | 172 | reason:i32 | point_gain:i16/u16 | point_total:i32 | is_taskforce_aux:i16/u16 | point_atk:i32 | point_spt:i32 | point_con:i32 | kill_streak_chain_num:i32 |
| 122 | `0x8DE4` | msma_spawn_wait_update | 74 | deck_index:u8/bool | respawn_wait_sec:i16/u16 | respawn_wait_max:i16/u16 |
| 123 | `0x8EFD` | weapon_hit_from_with_module | 162 | ent_id:i16/u16 | module_hp:i32 | is_force:u8/bool |
| 124 | `0x8FFA` | commander_support_tell | 226 | team:u8/bool | troops:u8/bool | support_type:i32 | ent_id:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | spt_ms_index:i16/u16 | spt_spot_index:u8/bool | spt_spot_dir:i16/u16 | remain_cnt:i16/u16 | remain_msec:i32 | use_worldid:i32 | use_pilotid:i32 | setter_ms:i16/u16 | val:i32 |
| 125 | `0x9105` | entity_msma_dead | 88 | ent_id_dead:i16/u16 | world_id_kill:i32 | pilot_id_kill:i32 | decal_kill:i32 | weapon_itemid:i32 | repair_wait_sec:i16/u16 | kill_streak_count:i16/u16 | spbits:i32 | is_resurrect:u8/bool | is_extend_style_change_limit:u8/bool |
| 126 | `0x918E` | debug_message | 287 | msg:? | color:i32 |
| 127 | `0x91C9` | battle_buffitem_list | 269 | buffitem[]:? | buffitem_ex[]:i32 |
| 128 | `0x97EC` | roomlobby_pick_vote_r | 29 | result:i32 |
| 129 | `0x9951` | msma_spawn_list_get_r_begin | 71 | spawn1st_post:i32 | is_1st:i32 |
| 130 | `0x9A22` | eqparts_ready_cancel_r | 168 | result:i32 | frame_count:i32 | AI_ent_id:i16/u16 | group_id:i16/u16 |
| 131 | `0x9A39` | room_kick_master_r | 44 | result:i32 |
| 132 | `0x9C14` | msma_AI_update_hate | 189 | AI_ent_id:i16/u16 | ent_id[]:i16/u16 | val[]:i16/u16 |
| 133 | `0xA39E` | msma_AI_change_movetype | 196 | AI_ent_id:i16/u16 | action_type:u8/bool | route_number:i16/u16 |
| 134 | `0xA5DA` | authenticate_r | 3 | result:i32 | room_id:i32 | room_name:? | mission_id:i32 | extrule_id:i32 | dc_node_id:i32 | is_rankerbattle:i32 | map_id:i32 | is_vsclan:u8/bool | comeback_stat:i32 | is_playing:u8/bool | is_netcafe:u8/bool | team:u8/bool | is_practice:u8/bool | config:? | progress:? | expup_fgauge:i16/u16 | is_ev_caravan:u8/bool | flag_wideuse:u8/bool | extrarule_xwar_info:i32 |
| 135 | `0xA63E` | mission_clear_countdown_start | 266 | remain_msec:i32 | clear_remain_msec:i32 |
| 136 | `0xA716` | mission_clear_countdown_cancel | 267 | remain_msec:i32 |
| 137 | `0xA77E` | game_replay_result | 69 | win_team:u8/bool |
| 138 | `0xA78D` | weapon_fire__funnel_r | 148 | from_ent_id:i32 | wslot_idx:u8/bool | fire_points[]:i32 |
| 139 | `0xA7C3` | msma_AI_set_fire_point | 193 | AI_ent_id:i16/u16 | fire_x:i16/u16 | fire_y:i16/u16 | fire_z:i16/u16 | end_x:i16/u16 | end_y:i16/u16 | end_z:i16/u16 |
| 140 | `0xA8F2` | weapon_hit_from_with_tumble | 159 | ent_id:i16/u16 | hit_dir:i16/u16 | spbits:i32 | optbits:i32 | down_power:i16/u16 | down_msec:i16/u16 |
| 141 | `0xA8FB` | eqparts_ready_counter_notice | 170 | result:i32 | ent_id:i16/u16 | count:i32 | maxcount:i32 |
| 142 | `0xA959` | radar_captured_notice | 180 | ent_id_radar:i16/u16 |
| 143 | `0xA9E7` | weapon_fire__damage_field_r | 152 | ent_id:i16/u16 | itemid:i32 | grenade_id:i32 | parent_id:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target1_x:i16/u16 | target1_y:i16/u16 | target1_z:i16/u16 | target2_x:i16/u16 | target2_y:i16/u16 | target2_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | shot0_impact1:u8/bool | fx_opt:u8/bool | charge_lv:u8/bool |
| 144 | `0xAA98` | combat_operation_end | 242 | support_type:i32 | is_completed:u8/bool | stg_arms_initiation_ms:i32 |
| 145 | `0xAB6F` | msma_spawn_list_get_r_end | 73 | - |
| 146 | `0xAB9B` | combat_operation_target_change_r | 246 | result:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | use_worldid:i32 | use_pilotid:i32 |
| 147 | `0xAC3D` | msma_change_team | 200 | team:u8/bool | troops:u8/bool | ent_id:i16/u16 |
| 148 | `0xACB0` | commander_get_pilotinfo_r | 218 | target_member:u8/bool | target_ace:i16/u16 | kill_cnt:i16/u16 | death_cnt:i16/u16 |
| 149 | `0xB313` | system_message | 286 | msg:? | color:i32 |
| 150 | `0xB334` | active_weapon_change_r | 112 | ent_id:i16/u16 | result:i32 | equip_index:u8/bool | equip_itemid:i32 | is_force:u8/bool |
| 151 | `0xB40C` | weapon_fire__grenade_r | 124 | ent_id:i16/u16 | itemid:i32 | grenade_id:i32 | parent_id:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target1_x:i16/u16 | target1_y:i16/u16 | target1_z:i16/u16 | target2_x:i16/u16 | target2_y:i16/u16 | target2_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | shot0_impact1:u8/bool | fx_opt:u8/bool | charge_lv:u8/bool | impact_wall:u8/bool | action:u8/bool |
| 152 | `0xB463` | msma_AI_install | 181 | AI_ent_id:i16/u16 | AI:i32 |
| 153 | `0xB491` | weapon_fire__snipe_beam_r | 137 | ent_id:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | begin1_end0:u8/bool |
| 154 | `0xB572` | repair_pack_supply | 204 | val:i32 | equip_idx:i16/u16 |
| 155 | `0xB604` | msma_AI_resume | 185 | AI_ent_id:i16/u16 |
| 156 | `0xB881` | roomlobby_ban_vote_r | 25 | result:i32 |
| 157 | `0xBA73` | cpf_authenticate | 283 | data[]:i32 |
| 158 | `0xBAE4` | entity_snapshot_splitdelta_compress | 99 | frame_count:i32 | remain_msec:i32 | zbuff[]:i32 |
| 159 | `0xBC13` | commander_select_r | 212 | result:i32 |
| 160 | `0xBDC6` | game_read_ahead_route_notice | 52 | read_ahead_route[]:i32 |
| 161 | `0xBDD6` | roomlobby_pilot_add | 4 | team:u8/bool | troops:u8/bool | world_id:i32 | pilot:? | stat:i32 | is_commander:u8/bool | is_audience:u8/bool | member_index:u8/bool | dtaskf_order_number:u8/bool | kill_count:i32 | death_count:i32 |
| 162 | `0xC327` | pos_warp_force | 106 | ent_id:i16/u16 | pos_x:i16/u16 | pos_y:i16/u16 | pos_z:i16/u16 | dir:i16/u16 | reason:i16/u16 |
| 163 | `0xC64E` | roomlobby_pilot_del | 6 | world_id:i32 | pilot_id:i32 |
| 164 | `0xC66B` | game_round_end | 54 | win_team:u8/bool | win_troops:u8/bool | progress:i32 |
| 165 | `0xCDE6` | game_score_ranker_notice | 68 | - |
| 166 | `0xCE08` | eqparts_toggle | 164 | ent_id:i16/u16 | group_id:i32 | toggle:i16/u16 | reason:i32 |
| 167 | `0xCF40` | weapon_fire__hand_throw_bound_r | 128 | grenade_id:i32 | hit_x:i16/u16 | hit_y:i16/u16 | hit_z:i16/u16 | vec_x:i16/u16 | vec_y:i16/u16 | vec_z:i16/u16 | vec_power:i16/u16 |
| 168 | `0xD1B3` | game_respawn_post_update | 65 | post_progress[]:i32 |
| 169 | `0xD691` | commander_subcmdr_candidacy_start | 237 | remain_sec:i16/u16 |
| 170 | `0xD725` | weapon_fire__wrestle_r | 121 | ent_id:i16/u16 | itemid:i32 | dir_h:i16/u16 | dir_v:i16/u16 | msec:i16/u16 | wrestle_id:i32 | charge_lv:u8/bool | action:u8/bool | chase_ent_id:i16/u16 | is_dp_damage_cut:u8/bool |
| 171 | `0xD8B9` | module_toggle_time | 294 | ent_id:i16/u16 | msec:i32 | rate:i16/u16 |
| 172 | `0xD94A` | game_suspend | 56 | - |
| 173 | `0xDC00` | commander_support_execute_r | 225 | result:i32 |
| 174 | `0xDC1E` | bgm_change | 262 | bgm_desc:? | fade_msec:i32 | reset:i32 |
| 175 | `0xDCF2` | roomlobby_pilot_msdeck | 7 | world_id:i32 | pilot_id:i32 | deck_msid[]:i32 | deck_mscolor[]:u8/bool |
| 176 | `0xDDE9` | module_toggle_level | 295 | ent_id:i16/u16 | level_up_flag:i32 | next_level_max:i32 |
| 177 | `0xDDF7` | weapon_hit_to_r | 156 | weapon_itemid:i32 | ent_id:i16/u16 | optbit:i32 | hit_pos_x:i16/u16 | hit_pos_y:i16/u16 | hit_pos_z:i16/u16 |
| 178 | `0xDE24` | proto_version_check_r | 1 | version:i32 | crc:? | gentime:i32 |
| 179 | `0xE014` | battleship_ride_r | 253 | result:i32 | from_world_id:i32 | from_pilot_id:i32 | from_ent_id:i16/u16 | to_ent_id:i16/u16 | hp_now:i32 | hp_max:i32 | shield_hp_now:i32 | shield_hp_max:i32 |
| 180 | `0xE031` | repair_gauge_update | 178 | gauge_old:i16/u16 | gauge_now:i16/u16 |
| 181 | `0xE12A` | commander_candidacy_end | 216 | result:i32 | cmdr_world_id:i32 | cmdr_pilot_id:i32 |
| 182 | `0xE228` | msma_AI_reboot | 183 | AI_ent_id:i16/u16 |
| 183 | `0xE2DE` | module_toggle_point | 293 | ent_id:i16/u16 | point:i16/u16 | point_max:i16/u16 |
| 184 | `0xE31F` | roomlobby_pilot_leave_appeal | 8 | - |
| 185 | `0xE332` | weapon_hit_from_with_stumble | 160 | ent_id:i16/u16 | hit_dir:i16/u16 | spbits:i32 | optbits:i32 | stumble_power:i16/u16 | stumble_msec:i16/u16 |
| 186 | `0xE378` | weapon_fire__bit_r | 139 | ent_id:i16/u16 | itemid:i32 | bit_id:i32 | shot_alive:u8/bool | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | release0_shot1:u8/bool | fx_opt:u8/bool |
| 187 | `0xE4DB` | entity_msma_show_hp | 95 | ent_id[]:i16/u16 | hp_max[]:i32 | gauge_max:i32 |
| 188 | `0xE5FC` | msma_spawn_warp_countdown_finish | 81 | ent_id:i16/u16 |
| 189 | `0xE861` | itembox_alarm | 208 | ent_id:i16/u16 |
| 190 | `0xE8EE` | demolition_breakthrough_result | 278 | group_id:i32 | is_succcess:i32 |
| 191 | `0xE96B` | repair_waittime_update | 179 | repair_wait_sec:i16/u16 |
| 192 | `0xEAB3` | mission_goal_text | 268 | text:i32 |
| 193 | `0xEAEA` | weapon_fire_prepare__destruct | 140 | ent_id:i16/u16 | weapon_itemid:i32 | fire_id:i32 |
| 194 | `0xEB53` | battle_contribute_rank | 175 | rank:i32 |
| 195 | `0xED22` | wrestle_chase_move_end_r | 301 | ent_id:i16/u16 |
| 196 | `0xEDFC` | weapon_fire__bit_reflect_r | 154 | ent_id:i16/u16 | itemid:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | charge_lv:u8/bool | reflect_ent_id:i16/u16 |
| 197 | `0xEE73` | map_event_linkfx_change | 280 | path:i32 |
| 198 | `0xF4D7` | shield_any_damage | 296 | ent_id:i16/u16 | damage:i32 |
| 199 | `0xF77B` | itembox_open | 207 | itembox_ent_id:i16/u16 | itemid:i32 | trap_weaponid:i32 |
| 200 | `0xF87E` | badge_add | 174 | rank:u8/bool | badge_type:u8/bool |
| 201 | `0xF88B` | mission_safety_area_over_penalty | 304 | ent_id:i16/u16 |
| 202 | `0xFD8A` | examination_progress_r | 271 | examination_info[]:? | examination_playscore:i32 | examination_playsec_remain_msec:i32 |
| 203 | `0xFE02` | daily_record_progress_r | 273 | daily_record_info[]:i32 |
| 204 | `0xFE50` | roomlobby_pick_vote_deck | 36 | state:i32 | msma_id[]:i32 | enemy_msma_id[]:i32 |
| 205 | `0xFEBB` | msma_spawn_warp_start_r | 79 | result:i32 | is_cancel:i32 | ent_id:i16/u16 | countdown_msec:i32 |

## 3. C→S 全表（服务端必须能收/解析）

| # | ID | 报文名 | 发送函数 | 字段（序） |
|---|---|---|---|---|
| 1 | `0x0372` | game_mission_progress_get | `sub_B33C10` | - |
| 2 | `0x03F7` | ban_transform | `sub_B40960` | ent_id:i32 | val:i32 |
| 3 | `0x0452` | room_kick_vote | `sub_B332B0` | target_world_id:i32 | target_pilot_id:i32 | kick_reason:i32 |
| 4 | `0x045B` | msma_AI_ping | `sub_B3CCB0` | AI_ent_id:i16/u16 |
| 5 | `0x05CA` | wrestle_chase_move_start | `sub_B40B50` | frame_count:i32 | dir_h:i16/u16 | wrestle_id:i32 | chase_time_msec:i32 | target_ent_id:i16/u16 | target_pos_x:i16/u16 | target_pos_y:i16/u16 | target_pos_z:i16/u16 | AI_ent_id:i16/u16 |
| 6 | `0x07C9` | entity_deploy_arms_attach | `sub_B34670` | arms_id:i32 | attach_parent_ent_id:i16/u16 | attach_pos_x:i16/u16 | attach_pos_y:i16/u16 | attach_pos_z:i16/u16 |
| 7 | `0x085F` | check_progress_quest | `sub_B40390` | - |
| 8 | `0x0BDD` | cpf_authenticate_r | `sub_B40520` | data[]:i32 |
| 9 | `0x11A9` | weapon_fire__shot_single_special | `sub_B36C80` | frame_count:i32 | itemid:i32 | AI_ent_id:i16/u16 |
| 10 | `0x16DB` | roomlobby_ban_vote | `sub_B32630` | msma_id:i32 |
| 11 | `0x1C33` | save_message | `sub_B40770` | msg:i32 |
| 12 | `0x1E04` | commander_subcmdr_candidacy_inbattle | `sub_B3EE70` | - |
| 13 | `0x271F` | battleship_crash_impact | `sub_B3FCD0` | from_ent_id:i16/u16 | to_ent_id:i16/u16 |
| 14 | `0x2761` | roomlobby_game_ready | `sub_B32180` | stat:i32 |
| 15 | `0x2ADC` | weapon_fire__wrestle | `sub_B36EC0` | frame_count:i32 | dir_h:i16/u16 | dir_v:i16/u16 | msec:i16/u16 | wrestle_id:i32 | charge_lv:u8/bool | AI_ent_id:i16/u16 | action:u8/bool | chase_ent_id:i16/u16 | is_dp_damage_cut:u8/bool |
| 16 | `0x2CAB` | game_round_ready | `sub_B33680` | - |
| 17 | `0x2DA4` | access_to | `sub_B35B70` | access_ent_id:i16/u16 | AI_ent_id:i16/u16 |
| 18 | `0x31D2` | active_weapon_mode_change | `sub_B362F0` | mode:i16/u16 | AI_ent_id:i16/u16 |
| 19 | `0x34A9` | proto_version_check | `sub_B318D0` | version:i32 | crc:? | gentime:i32 |
| 20 | `0x34BE` | preset_voice_up_commander | `sub_B34D20` | voice_id:i32 | AI_ent_id:i16/u16 |
| 21 | `0x34C8` | roomlobby_ban_vote_cancel | `sub_B327E0` | msma_id:i32 |
| 22 | `0x36AC` | weapon_fire__for_myself | `sub_B3A1F0` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | rcnt_bullet_mgz:i16/u16 | rcnt_bullet_all:i16/u16 | begin1_end0:u8/bool | AI_ent_id:i16/u16 |
| 23 | `0x379B` | cutin_up | `sub_B34F10` | `u32 cutin_category_id` | `u16 AI_ent_id` | `u32 to_world_id` | `u32 to_pilot_id` | `u8 to_range` ⇒ **体 15B**（缓冲 22B；**通知索引 103**）★2026-09-15 按写入器逐句定宽（旧记"2×u32+u8"✗） |
| 24 | `0x3AF6` | weapon_fire__hand_throw_bound | `sub_B37F60` | frame_count:i32 | grenade_id:i32 | hit_x:i16/u16 | hit_y:i16/u16 | hit_z:i16/u16 | vec_x:i16/u16 | vec_y:i16/u16 | vec_z:i16/u16 | vec_power:i16/u16 | AI_ent_id:i16/u16 |
| 25 | `0x421B` | pos_move | `sub_B351D0` | frame_count:i32 | pos_x:i16/u16 | pos_y:i16/u16 | pos_z:i16/u16 | dir:i16/u16 | dir_eye:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | spbits:i32 | spbits2:i16/u16 | lockon_ent_id:i16/u16 | in_water_index:? | layer_index:? | access_ent_id1:i16/u16 | access_ent_id2:i16/u16 | rideon_ent_id:i16/u16 | spot_ent_id:i16/u16 | AI_ent_id:i16/u16 | operate_ent_id:i16/u16 | is_under_water:? | hack_check[]:i32 |
| 26 | `0x434C` | msma_AI_move_stuckescape | `sub_B3D600` | AI_ent_id:i16/u16 | to_x:i16/u16 | to_y:i16/u16 | to_z:i16/u16 | msec:i16/u16 |
| 27 | `0x444D` | room_kick_master | `sub_B330C0` | world_id:i32 | pilot_id:i32 |
| 28 | `0x5456` | msma_AI_set_stat | `sub_B3CE60` | AI_ent_id:i16/u16 | idx[]:i32 | num[]:i32 |
| 29 | `0x5A5D` | eqparts_exec_toggle | `sub_B3C750` | frame_count:i32 | AI_ent_id:i16/u16 | group_id:i16/u16 |
| 30 | `0x6007` | wrestle_chase_move_end | `sub_B40F20` | frame_count:i32 | AI_ent_id:i16/u16 |
| 31 | `0x6486` | commander_support_execute | `sub_B3E580` | support_type:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | spt_spot_index:u8/bool | val:i32 |
| 32 | `0x6636` | commander_order_assist | `sub_B3E3D0` | type:u8/bool |
| 33 | `0x692B` | dynamic_taskforce_order_issue | `sub_B3F3F0` | order_kind:u8/bool | order_param:i32 | select_members[]:u8/bool | select_npcs[]:i16/u16 |
| 34 | `0x6BCD` | msma_AI_hate_control | `sub_B3D210` | AI_ent_id:i16/u16 | target_ent_id:i16/u16 | hate_adjust:i16/u16 |
| 35 | `0x6C48` | commander_candidacy_inbattle | `sub_B3E050` | - |
| 36 | `0x6FA1` | combat_operation_container_collect | `sub_B3F000` | destination:i32 |
| 37 | `0x770D` | weapon_hit_to | `sub_B3B7A0` | phash:i64 | frame_count:i32 | weapon_itemid:i32 | fire_id:i32 | ent_ids[]:i16/u16 | hit_pos_x[]:i16/u16 | hit_pos_y[]:i16/u16 | hit_pos_z[]:i16/u16 | hit_dirs[]:i16/u16 | hit_distance[]:i16(2B) | body_distance[]:i16(2B) | body_regions[]:i16/u16 | charge_lv:i32 | AI_ent_id:i16/u16 | instate_from_ent_id:i16/u16 | create_frame_count:i32 | is_down_range:i32 | is_wrestle_first_high_lockon:i32 |
| 38 | `0x77C0` | examination_progress | `sub_B40070` | - |
| 39 | `0x7916` | funnel_snapshot_self | `sub_B3AB30` | snapshot:i32 |
| 40 | `0x7938` | roomlobby_pick_vote_cancel | `sub_B32B40` | msma_id:i32 |
| 41 | `0x7B52` | msma_spawn_warp_start | `sub_B34240` | is_cancel:i32 |
| 42 | `0x7C0C` | weapon_fire__hand_throw | `sub_B379F0` | frame_count:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | shot0_impact1:u8/bool | fx_opt:u8/bool | impact_grenade_id:i32 | charge_lv:u8/bool | AI_ent_id:i16/u16 | salvo_slot:u8/bool |
| 43 | `0x7CA0` | weapon_fire__shot_single | `sub_B364E0` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | rcnt_bullet_mgz:i16/u16 | rcnt_bullet_all:i16/u16 | charge_lv:u8/bool | AI_ent_id:i16/u16 | salvo_slot:u8/bool |
| 44 | `0x7E45` | roomlobby_pick_vote | `sub_B32990` | msma_id:i32 |
| 45 | `0x800A` | msma_spawn_warp_select | `sub_B343F0` | post_index:i32 | spt_spot_index:i32 | is_btlship_ride:u8/bool | respawn_ent_id:i16/u16 |
| 46 | `0x8898` | weapon_fire__damage_field | `sub_B3AD30` | frame_count:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target1_x:i16/u16 | target1_y:i16/u16 | target1_z:i16/u16 | target2_x:i16/u16 | target2_y:i16/u16 | target2_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | shot0_impact1:u8/bool | fx_opt:u8/bool | impact_grenade_id:i32 | parent_grenade_id:i32 | charge_lv:u8/bool | AI_ent_id:i16/u16 |
| 47 | `0x9B19` | roomlobby_pilot_mindex_update | `sub_B31E20` | member_index:u8/bool |
| 48 | `0x9F0D` | preset_voice_up | `sub_B34930` | voice_id:i32 | AI_ent_id:i16/u16 | to_world_id:i32 | to_pilot_id:i32 | is_party:u8/bool | is_use_textmsg:u8/bool | textmsg:? | is_cutin:u8/bool | is_voice:u8/bool |
| 49 | `0xA0EA` | weapon_fire__bit_reflect | `sub_B3B350` | frame_count:i32 | itemid:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | charge_lv:u8/bool | AI_ent_id:i16/u16 | reflect_ent_id:i16/u16 |
| 50 | `0xA404` | weapon_fire__shot_rapid | `sub_B368B0` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | rcnt_bullet_mgz:i16/u16 | rcnt_bullet_all:i16/u16 | begin1_end0:u8/bool | AI_ent_id:i16/u16 | salvo_slot:u8/bool |
| 51 | `0xA4C9` | weapon_fire__bit | `sub_B39420` | frame_count:i32 | shot_bit_id:i32 | shot_ent_id:i16/u16 | shot_alive:u8/bool | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | release0_shot1:u8/bool | fx_opt:u8/bool | AI_ent_id:i16/u16 |
| 52 | `0xA537` | roomlobby_xwar_commander_lot | `sub_B31FD0` | is_lot:u8/bool |
| 53 | `0xA8FE` | weapon_fire_prepare__destruct_r | `sub_B39990` | frame_count:i32 | weapon_itemid:i32 | fire_id:i32 | ent_ids[]:i16/u16 | hit_pos_x[]:i16/u16 | hit_pos_y[]:i16/u16 | hit_pos_z[]:i16/u16 | hit_dirs[]:i16/u16 | hit_distance[]:i16(2B) | body_regions[]:i16/u16 | AI_ent_id:i16/u16 |
| 54 | `0xB015` | rideable_msma_get_down | `sub_B3FEC0` | reason:u8/bool |
| 55 | `0xB10A` | msma_AI_arrive_move_end | `sub_B3D450` | AI_ent_id:i16/u16 |
| 56 | `0xBA58` | battleship_ride | `sub_B3F970` | to_ent_id:i16/u16 |
| 57 | `0xBAFF` | room_chat_editing | `sub_B32F10` | is_editing:u8/bool |
| 58 | `0xBB1A` | room_chat_up | `sub_B32CF0` | msg:? | is_party:u8/bool |
| 59 | `0xBB6D` | xwar_commander_subcmdr_lot | `sub_B3ECC0` | is_lot:u8/bool |
| 60 | `0xBCA5` | dynamic_taskforce_order_change_party | `sub_B3F780` | order_kind:u8/bool | order_param:i32 |
| 61 | `0xBCB4` | commander_support_hit_to | `sub_B3E890` | ent_id:i16/u16 | hit_team:u8/bool | hit_troops:u8/bool | support_type:i32 | ent_ids[]:i16/u16 | hit_dirs[]:i16/u16 |
| 62 | `0xBDD2` | game_client_signal | `sub_B33A60` | sigval:i32 |
| 63 | `0xBEE3` | weapon_fire__start_homing | `sub_B38370` | frame_count:i32 | grenade_id:i32 | pos_x:i16/u16 | pos_y:i16/u16 | pos_z:i16/u16 | target_ent_id:i16/u16 |
| 64 | `0xBFA9` | weapon_fire__deploy_arms | `sub_B38670` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | target_ent_id:i16/u16 | state:u8/bool | fx_opt:u8/bool | impact_arms_id:i32 | AI_ent_id:i16/u16 | is_gmk:i32 | index:u8/bool |
| 65 | `0xC166` | eqparts_ready_start | `sub_B3C290` | frame_count:i32 | AI_ent_id:i16/u16 | group_id:i16/u16 | reason:i32 |
| 66 | `0xC3BD` | weapon_fire__snipe_beam | `sub_B39090` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | rcnt_bullet_mgz:i16/u16 | rcnt_bullet_all:i16/u16 | begin1_end0:u8/bool | AI_ent_id:i16/u16 |
| 67 | `0xC84F` | bullet_supply_r | `sub_B3D8D0` | percent_val:i16/u16 | equip_idx:i16/u16 |
| 68 | `0xC90D` | weapon_fire__air_bomb | `sub_B38AC0` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | shot0_drop1_impact2:u8/bool | fx_opt:u8/bool | airbomb_id:i32 | AI_ent_id:i16/u16 |
| 69 | `0xCAAE` | object_put | `sub_B35D60` | frame_count:i32 | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 | attach_parent_ent_id:i16/u16 | is_initiation:u8/bool | AI_ent_id:i16/u16 |
| 70 | `0xCAAF` | commander_get_pilotinfo | `sub_B3E1E0` | target_member:u8/bool | target_ace:i16/u16 |
| 71 | `0xCB97` | game_resume_enter | `sub_B33810` | is_initial:i32 | script_thread:u8/bool | src:i32 |
| 72 | `0xCF71` | room_kick_vote_get_enable_pilots | `sub_B334F0` | - |
| 73 | `0xCFC8` | emergency_escape | `sub_B3C990` | - |
| 74 | `0xD2AE` | repair_pack_supply_r | `sub_B3DAC0` | val:i32 | equip_idx:i16/u16 |
| 75 | `0xD2C3` | weapon_fire__grenade | `sub_B372D0` | frame_count:i32 | launch_x:i16/u16 | launch_y:i16/u16 | launch_z:i16/u16 | target1_x:i16/u16 | target1_y:i16/u16 | target1_z:i16/u16 | target2_x:i16/u16 | target2_y:i16/u16 | target2_z:i16/u16 | target_ent_id:i16/u16 | msec:i16/u16 | shot0_impact1:u8/bool | fx_opt:u8/bool | impact_grenade_id:i32 | parent_grenade_id:i32 | charge_lv:u8/bool | ent_id:i32 | AI_ent_id:i16/u16 | impact_wall:u8/bool | salvo_slot:u8/bool | action:u8/bool |
| 76 | `0xD97D` | roomlobby_exit | `sub_B324B0` | - |
| 77 | `0xDAE0` | commander_list_get | `sub_B3DCB0` | team:u8/bool | troops:u8/bool |
| 78 | `0xDDB7` | eqparts_ready_cancel | `sub_B3C510` | frame_count:i32 | AI_ent_id:i16/u16 | group_id:i16/u16 |
| 79 | `0xE041` | msma_spawn_list_get | `sub_B33DA0` | - |
| 80 | `0xE1C1` | weapon_fire__air_bomb_intercepted | `sub_B38E50` | ent_id:i16/u16 | airbomb_id:i32 | arms_id:i32 |
| 81 | `0xE314` | weapon_fire__camera | `sub_B3A580` | frame_count:i32 | ent_ids[]:i16/u16 | AI_ent_id:i16/u16 |
| 82 | `0xE650` | msma_spawn_select | `sub_B33F30` | ms_index:i32 | post_index:i32 | spt_spot_index:i32 | is_btlship_ride:u8/bool | is_msma_ride:u8/bool | respawn_ent_id:i16/u16 |
| 83 | `0xE742` | combat_operation_target_change | `sub_B3F1B0` | target_x:i16/u16 | target_y:i16/u16 | target_z:i16/u16 |
| 84 | `0xEA5A` | active_weapon_change | `sub_B360B0` | frame_count:i32 | equip_index:u8/bool | AI_ent_id:i16/u16 |
| 85 | `0xEDBC` | tumble_ukemi | `sub_B35980` | AI_ent_id:i16/u16 | tmp:i32 |
| 86 | `0xEDD6` | daily_record_progress | `sub_B40200` | - |
| 87 | `0xF24B` | authenticate | `sub_B31B10` | userid:i32 | world_id:i32 | pilot_id:i32 | room_id:i32 | otp_battle:? | is_comeback:u8/bool |
| 88 | `0xF4B9` | battleship_get_down | `sub_B3FB20` | reason:u8/bool |
| 89 | `0xF51E` | emergency_self_destruct | `sub_B3CB20` | - |
| 90 | `0xF741` | roomlobby_game_start | `sub_B32330` | - |
| 91 | `0xF79B` | commander_select | `sub_B3DEA0` | commander_id:i32 |
| 92 | `0xFBC1` | weapon_fire__funnel | `sub_B3A860` | from_ent_id:i32 | wslot_idx:u8/bool | fire_points[]:i32 |

