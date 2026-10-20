# 战服报文 · 交互总表（ID / 闸门 / 体长 / 字段 / 处理者 / 解析序列）

> 生成：`tools/dump_battle_protocol.py` + `tools/battle_bodylen.py` + `tools/battle_handlers.py`（可重跑）。
> `处理者` = 收包 case 尾部 `call vt[OFF]` 经 thunk 跟到的实现；`解析序列` = case 入口→dump 头之间的读取器调用（u32/u16/u8/变长）。
> `体长` 判据见 `battle-体长线索.md`（143/205 三条验证）。

## 0. 规模

| 项 | 值 |
|---|---|
| S→C | 205 条 |
| C→S | 92 条 |
| 体长已定（★定长） | 143 条 |
| 解析含循环/变长 | 21 条 |

## 1. S→C 全表

| ID | 报文 | 闸门 | 体长 | 处理者(impl) | 参数数 | 解析序列 | 处理者一级被调 | 字段（序） |
|---|---|---|---|---|---|---|---|---|
| `0x0120` | entity_msma_show | 93 | ★定长 2B | `sub_BA96A0` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0x02D8` | combat_operation_container_collect_r | 244 | ★定长 6B | `sub_BAA7B0` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id result |
| `0x03CC` | weapon_fire__air_bomb_r | 134 | ★定长 18B | `sub_BA9CD0` | 8 | B413B0×4() B02DF0×4(u16) B41470×2() B02DD0×2(u32) B05E30×2() B06230×2(u8) | - | ent_id itemid airbomb_id target_x target_y target_z shot0_drop1_impact2 fx_opt |
| `0x049D` | wrestle_chase_move_start_r | 299 | ★定长 20B | `sub_BAACA0` | 8 | B413B0×6() B02DF0×6(u16) B41470×2() B02DD0×2(u32) | - | ent_id itemid dir_h wrestle_id target_ent_id target_pos_x target_pos_y target_pos_z |
| `0x056D` | battleship_cooltime_notice | 258 | ★定长 6B | `sub_BAA8F0` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | to_ent_id remain_msec |
| `0x057A` | entity_deploy_arms_appear | 85 | 待人工（alloc=0x60, sum=0） | `sub_BA9550` | 1 | - | - | appear_info |
| `0x07E9` | room_kick_vote_get_enable_pilots_r | 49 | 待人工（alloc=0x1AC, sum=20） | `sub_BA90F0` | 5 | B02DD0×5(u32) B41470×1() | - | enable_worlds[] enable_pilots[] result |
| `0x0825` | weapon_state_update | 115 | ★定长 6B | `sub_BA9AA0` | 3 | B413B0×3() B02DF0×3(u16) | - | ent_id weapon_state weapon_change_flag |
| `0x0943` | entity_msma_disappear | 87 | ★定长 8B | `sub_BA95C0` | 3 | B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) | - | ent_id reason not_use |
| `0x0B3E` | roomlobby_pilot_mindex_update_r | 11 | ★定长 14B | `sub_BA8E70` | 5 | B41470×3() B02DD0×3(u32) B05E30×2() B06230×2(u8) | - | result world_id pilot_id member_index is_commander |
| `0x0BCE` | score_update_coopwave | 173 | ★定长 22B | `sub_BAA1B0` | 7 | B41470×4() B02DD0×4(u32) B413B0×3() B02DF0×3(u16) | - | reason world_id pilot_id point_gain point_total n_cont_kill bonus_cont_kill |
| `0x0C5F` | commander_candidacy_start | 214 | ★定长 2B | `sub_BAA4D0` | 1 | B413B0×1() B02DF0×1(u16) | - | remain_sec |
| `0x0E85` | commander_list_get_r | 210 | 待人工（alloc=0x18, sum=12） | `sub_BAA480` | 3 | B02DD0×3(u32) B41470×1() | - | result commander_id[] |
| `0x0EC5` | room_kick_to | 45 | 待人工（alloc=0x2D, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0x1113` | game_script_play | 61 | 待人工（alloc=0x43, sum=2） | `sub_BAAED0` | None | B05E30×2() B06230×2(u8) B02BA0?×1() | - | src is_with_resume script_thread |
| `0x1159` | game_mapgimmick_update | 66 | 待人工（alloc=0x404, sum=4） | `sub_BA9320` | 2 | B02DD0×1(u32) | - | gimmick_progress[] |
| `0x1165` | msma_AI_uninstall | 182 | ★定长 2B | `sub_BAA270` | 1 | B413B0×1() B02DF0×1(u16) | - | AI_ent_id |
| `0x12EC` | room_chat_down | 40 | 待人工（alloc=0xDB, sum=13） | `sub_BA9040` | 9 | B05E30×5() B06230×5(u8) B41470×2() B02DD0×2(u32) B02BA0?×2() | - | team troops world_id pilot_id pilot_name msg is_all is_party is_audience |
| `0x130A` | entity_msma_hide | 92 | ★定长 2B | `sub_BA9690` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0x1365` | game_begin | 50 | 待人工（alloc=0x2806, sum=66） | `sub_BA9120` | 23 | B02DD0×16(u32) B41470×12() B05E30×2() B06230×2(u8) B418C0?×1() B077B0?×1() B05ED0?×1() B07880?×1() | - | snapshot_int_msec snapshot_res_msec pos_factor map_id btlfield clear_remain_msec is_disable_conq_sp is_room_suspend mission_id sudden_type sudden_bonus_target exp_min exp_max config progress respawn_posts[] mapgimmicks[] bgm_desc missionunit_set[] mission_phase |
| `0x14C5` | roomlobby_exit_r | 23 | 待人工（alloc=0x17, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0x16AA` | eqparts_execute | 163 | 待人工（alloc=0x2086, sum=6） | `sub_BAAED0` | None | B413B0×1() B02DF0×1(u16) B02DD0×1(u32) | - | ent_id parts_exec[] |
| `0x1A13` | weapon_fire__hand_throw_r | 126 | ★定长 29B | `sub_BA9BB0` | 14 | B413B0×9() B02DF0×9(u16) B05E30×3() B06230×3(u8) B41470×2() B02DD0×2(u32) | - | ent_id itemid grenade_id launch_x launch_y launch_z target_x target_y target_z target_ent_id msec shot0_impact1 fx_opt charge_lv |
| `0x1B32` | rideable_msma_ride | 259 | ★定长 26B | `sub_BAA910` | 8 | B41470×5() B02DD0×5(u32) B413B0×3() B02DF0×3(u16) | - | result access_type from_world_id from_pilot_id from_ent_id to_ent_id hp_now hp_max |
| `0x1B67` | funnel_snapshot_all | 150 | 待人工（alloc=0x4E4, sum=4） | `sub_BA9E50` | 2 | B02DD0×1(u32) | - | snapshot_arr[] |
| `0x1BB4` | commander_support_countdown | 230 | ★定长 17B | `sub_BAA690` | 9 | B413B0×5() B02DF0×5(u16) B05E30×3() B06230×3(u8) B41470×1() B02DD0×1(u32) | - | ent_id support_type team troops target_x target_y target_z count is_hit_send |
| `0x1E0F` | preset_voice_down | 101 | 待人工（alloc=0xBF, sum=10） | `sub_BA99D0` | 7 | B05E30×4() B06230×4(u8) B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) B02BA0?×1() | - | ent_id voice_id voice_volume is_cutin is_party is_use_textmsg textmsg |
| `0x1E2F` | msma_spawn_list_get_r_one | 72 | 待人工（alloc=0x10C, sum=4） | `sub_BAAED0` | None | B41470×1() B02DD0×1(u32) | - | index ms |
| `0x1EA5` | entity_msma_reborn | 89 | ★定长 4B | `sub_BA9630` | 2 | B413B0×2() B02DF0×2(u16) | - | ent_id hp_percent |
| `0x1EC7` | battleship_get_down_r | 255 | ★定长 6B | `sub_BAA8B0` | 2 | B41470×1() B02DD0×1(u32) B413B0×1() B02DF0×1(u16) | - | result to_ent_id |
| `0x1ED8` | roomlobby_ban_vote_cancel_r | 27 | ★定长 4B | `sub_BA8F90` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0x214C` | commander_support_rendition_end | 229 | ★定长 7B | `sub_BAA660` | 4 | B05E30×3() B06230×3(u8) B41470×1() B02DD0×1(u32) | - | team troops support_type spt_spot_index |
| `0x243B` | game_btlfield_change | 51 | ★定长 4B | `sub_BA9220` | 1 | B41470×1() B02DD0×1(u32) | - | btlfield |
| `0x26E9` | commander_select_tell | 213 | ★定长 6B | `sub_BAA4B0` | 3 | B05E30×2() B06230×2(u8) B41470×1() B02DD0×1(u32) | - | team troops commander_id |
| `0x26F8` | xwar_commander_subcmdr_lot_r | 236 | ★定长 1B | `sub_BAA700` | 1 | B05E30×1() B06230×1(u8) | - | is_lot |
| `0x27F3` | room_kick_vote_r | 47 | ★定长 4B | `sub_BA90E0` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0x2B4D` | setmsparam | 289 | ★定长 12B | `sub_BAABA0` | 3 | B41470×3() B02DD0×3(u32) | - | ent_id val type |
| `0x2C60` | cpf_authenticate_error | 285 | ★定长 4B | `sub_BAAB90` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0x2D27` | area_over_penalty_countdown | 302 | ★定长 10B | `sub_BAACF0` | 3 | B41470×2() B02DD0×2(u32) B413B0×1() B02DF0×1(u16) | - | ent_id limit_msec elapsed_msec |
| `0x30A9` | roomlobby_ban_vote_result | 32 | 待人工（alloc=0x30, sum=16） | `sub_BA8FA0` | 4 | B02DD0×4(u32) B41470×2() | - | state vote_count[] ban_msma_id[] member_count |
| `0x315C` | roomlobby_xwar_commander_lot_r | 15 | ★定长 7B | `sub_BA8ED0` | 3 | B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) B413B0×1() B02DF0×1(u16) | - | result is_lot lot_count |
| `0x3298` | msma_spawn_force_warp_start | 80 | ★定长 6B | `sub_BA9470` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id countdown_msec |
| `0x339C` | roomlobby_game_ready_r | 19 | ★定长 16B | `sub_BA8F40` | 4 | B41470×4() B02DD0×4(u32) | - | result world_id pilot_id stat |
| `0x3638` | msma_AI_move_stuckescape_r | 198 | ★定长 10B | `sub_BAA380` | 5 | B413B0×5() B02DF0×5(u16) | - | AI_ent_id to_x to_y to_z msec |
| `0x377D` | bullet_supply | 201 | ★定长 4B | `sub_BAA3D0` | 2 | B413B0×2() B02DF0×2(u16) | - | percent_val equip_idx |
| `0x37C1` | weapon_fire__for_myself_r | 144 | ★定长 11B | `sub_BA9DE0` | 5 | B413B0×3() B02DF0×3(u16) B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | ent_id target_x target_y target_z begin1_end0 |
| `0x39B3` | msma_AI_update_move_end | 191 | ★定长 8B | `sub_BAA2E0` | 4 | B413B0×4() B02DF0×4(u16) | - | AI_ent_id end_x end_y end_z |
| `0x3BBE` | room_chat_editing_r | 42 | ★定长 9B | `sub_BA9080` | 3 | B41470×2() B02DD0×2(u32) B05E30×1() B06230×1(u8) | - | world_id pilot_id is_editing |
| `0x3C70` | mission_safety_area_return_to_area | 303 | ★定长 2B | `sub_BAAD10` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0x3E07` | commander_subcmdr_candidacy_end | 239 | 待人工（alloc=0xEF, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0x3E23` | game_mission_progress_update | 64 | 待人工（alloc=0x40, sum=0） | `sub_BA92F0` | 1 | B05ED0?×1() B07880?×1() | - | mprogress |
| `0x412B` | cutin_down | 104 | ★定长 6B | `sub_BA9A00` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id cutin_category_id |
| `0x45FC` | weapon_hit_from_with_staggery | 161 | ★定长 16B | `sub_BAA040` | 6 | B413B0×4() B02DF0×4(u16) B41470×2() B02DD0×2(u32) | - | ent_id hit_dir spbits optbits staggery_power staggery_msec |
| `0x47C2` | conquer_spoint_change | 265 | ★定长 4B | `sub_BAAA30` | 1 | B41470×1() B02DD0×1(u32) | - | conquer |
| `0x483F` | dynamic_taskforce_order_result | 251 | ★定长 11B | `sub_BAA840` | 5 | B05E30×3() B06230×3(u8) B41470×2() B02DD0×2(u32) | - | result order_index order_number order_kind order_param |
| `0x49C6` | weapon_hit_from | 158 | ★定长 43B | `sub_BA9F80` | 15 | B413B0×7() B02DF0×7(u16) B41470×7() B02DD0×7(u32) B05E30×1() B06230×1(u8) | - | ent_id from_ent_id weapon_itemid charge_lv hp_now hp_max damage spbits hit_pos_x hit_pos_y hit_pos_z hit_dir body_region optbits shield_hp_now |
| `0x4C36` | rideable_msma_get_down_r | 261 | ★定长 26B | `sub_BAA950` | 8 | B41470×5() B02DD0×5(u32) B413B0×3() B02DF0×3(u16) | - | result access_type from_ent_id to_world_id to_pilot_id to_ent_id hp_now hp_max |
| `0x4C7D` | entity_msma_unattended_state | 96 | ★定长 4B | `sub_BA9720` | 2 | B413B0×2() B02DF0×2(u16) | - | ent_id state_bit |
| `0x4D96` | game_client_signal_r | 60 | ★定长 4B | `sub_BA92A0` | 1 | B41470×1() B02DD0×1(u32) | - | sigval |
| `0x4E9F` | weapon_fire__shot_single_special_r | 119 | ★定长 6B | `sub_BA9AC0` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id itemid |
| `0x4FCE` | msma_AI_move_stuckescape_end | 199 | ★定长 2B | `sub_BADBF0` | 1 | B413B0×1() B02DF0×1(u16) | - | AI_ent_id |
| `0x501D` | commander_support_debug_cooltime_end | 234 | 待人工（alloc=0xEA, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0x5080` | msma_AI_suspend | 184 | ★定长 2B | `sub_BAA290` | 1 | B413B0×1() B02DF0×1(u16) | - | AI_ent_id |
| `0x5092` | commander_support_spot_notice | 221 | 待人工（alloc=0x784, sum=4） | `sub_BAA530` | 2 | B02DD0×1(u32) | - | support_spots[] |
| `0x5157` | access_state | 206 | ★定长 8B | `sub_BAA430` | 3 | B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) | - | to_ent_id from_ent_id remain_msec |
| `0x54C6` | dynamic_taskforce_info_update | 247 | 待人工（alloc=0x1AB, sum=26） | `sub_BAA800` | 10 | B02DD0×5(u32) B06230×4(u8) B02DF0×1(u16) B05EA0?×1() B41470×1() | - | order_all_number[] order_all_kind[] order_all_param[] members_order_idx[] npc_entid[] npc_order_index[] party_worldid party_pilotid |
| `0x54DD` | msma_AI_set_fire_area | 194 | ★定长 20B | `sub_BAA300` | 10 | B413B0×10() B02DF0×10(u16) | - | AI_ent_id fire_sx fire_sy fire_sz fire_ex fire_ey fire_ez end_x end_y end_z |
| `0x553F` | commander_support_gauge_update | 223 | ★定长 5B | `sub_BAA570` | 2 | B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | gauge_val no_complement |
| `0x568A` | entity_snapshot | 97 | 待人工（alloc=0x8F0C, sum=12） | `sub_BA9740` | 4 | B02DD0×3(u32) B41470×2() | - | frame_count remain_msec snapshots[] |
| `0x56CF` | commander_support_hit_from | 232 | ★定长 20B | `nullsub_42` | 6 | B41470×4() B02DD0×4(u32) B413B0×2() B02DF0×2(u16) | - | support_type ent_id hp_now hp_max spbits hit_dir |
| `0x58FC` | commander_order_assist_r | 220 | ★定长 1B | `sub_BAA520` | 1 | B05E30×1() B06230×1(u8) | - | type |
| `0x5913` | roomlobby_roommaster_notice | 12 | ★定长 8B | `sub_BA8EA0` | 2 | B41470×2() B02DD0×2(u32) | - | world_id pilot_id |
| `0x5B98` | battleship_limittime_notice | 257 | ★定长 6B | `sub_BAA8D0` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | to_ent_id limit_msec |
| `0x5C4F` | entity_msma_detach | 91 | ★定长 2B | `sub_BA9680` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0x5D2A` | roomlobby_clan_notice | 16 | 待人工（alloc=0x28, sum=9） | `sub_BA8EF0` | 7 | B05E30×5() B06230×5(u8) B41470×1() B02DD0×1(u32) B02BA0?×1() | - | team troops clan_id clan_name clan_emb_base clan_emb_parts1 clan_emb_parts2 |
| `0x5EEA` | entity_snapshot_splitdelta | 98 | 待人工（alloc=0x9FC4, sum=167） | `sub_BAAED0` | None | B02DD0×33(u32) B02DF0×18(u16) B05EA0?×13() B06230×13(u8) B41470×2() | - | frame_count remain_msec ent_id[] dirty_bits[] pos_real_x[] pos_real_y[] pos_real_z[] pos_diff_x[] pos_diff_y[] pos_diff_z[] dir[] target_real_x[] target_real_y[] target_real_z[] target_diff_x[] target_diff_y[] target_diff_z[] spbit_ll[] spbit_l[] spbit_h[] spbit_hh[] spbit2[] hp_percent[] hp_percent_shield[] down_power[] equip_index[] score1[] water_index[] score2[] layer_index[] score3[] rideon_ent_id[] lockon_ent_id[] |
| `0x5F32` | bullet_supply_per_weapon_slot | 203 | 待人工（alloc=0xC, sum=8） | `sub_BAA3F0` | 3 | B02DF0×2(u16) B413B0×1() B02DD0×1(u32) | - | supplyer_end_id supply_amount_per_weapon_slot[] |
| `0x6059` | check_progress_quest_r | 277 | 待人工（alloc=0x88, sum=0） | `sub_BAAAC0` | 1 | - | - | check_quest |
| `0x611B` | game_script_play_also_replay | 62 | 待人工（alloc=0x42, sum=1） | `sub_BA92D0` | 2 | B02BA0?×1() B05E30×1() B06230×1(u8) | - | src script_thread |
| `0x6295` | combat_operation_start | 241 | ★定长 24B | `sub_BAA750` | 9 | B41470×4() B02DD0×4(u32) B413B0×3() B02DF0×3(u16) B05E30×2() B06230×2(u8) | - | team troops support_type remain_msec target_x target_y target_z use_worldid use_pilotid |
| `0x640D` | msma_spawn_info_prestart | 77 | 待人工（alloc=0x179, sum=27） | `sub_BA9410` | 9 | B02DD0×5(u32) B02DF0×3(u16) B41470×1() B05EA0?×1() B06230×1(u8) | - | remain_sec mstype[] post_index[] spt_spot_index[] stghold_entid[] |
| `0x6411` | gm_camera_change_r | 282 | ★定长 3B | `sub_BAAB50` | 2 | B05E30×1() B06230×1(u8) B413B0×1() B02DF0×1(u16) | - | type args |
| `0x645D` | module_val_update | 292 | ★定长 6B | `sub_BAABE0` | 3 | B413B0×3() B02DF0×3(u16) | - | ent_id val val2 |
| `0x6475` | game_coopwave_result | 53 | 待人工（alloc=0x2C, sum=0） | `sub_BA9250` | 1 | - | - | wave_res |
| `0x6735` | deliver_oration | 263 | ★定长 8B | `sub_BAA9D0` | 2 | B41470×2() B02DD0×2(u32) | - | voice_id elap_msec |
| `0x6A0F` | roomlobby_vote_get_comeback | 38 | 待人工（alloc=0x14, sum=8） | `sub_BAAED0` | None | B02DD0×2(u32) B41470×1() | - | state msma_id[] |
| `0x6A38` | roomlobby_pilot_level_update | 9 | ★定长 12B | `sub_BA8E50` | 4 | B41470×2() B02DD0×2(u32) B413B0×2() B02DF0×2(u16) | - | world_id pilot_id lv_old lv_new |
| `0x6A8D` | roomlobby_xwar_countdown | 13 | ★定长 4B | `sub_BA8EC0` | 1 | B41470×1() B02DD0×1(u32) | - | sec |
| `0x6B2C` | roomlobby_cupteam_notice | 17 | ★定长 13B | `sub_BA8F20` | 4 | B41470×3() B02DD0×3(u32) B05E30×1() B06230×1(u8) | - | team cupteam_id cupteam_rate tournament_vs_type |
| `0x6B71` | roomlobby_vote_state | 37 | ★定长 8B | `sub_BA9000` | 2 | B41470×2() B02DD0×2(u32) | - | state sec |
| `0x6D20` | weapon_fire__deploy_arms_r | 132 | ★定长 28B | `sub_BA9C80` | 11 | B413B0×5() B02DF0×5(u16) B41470×4() B02DD0×4(u32) B05E30×2() B06230×2(u8) | - | ent_id itemid arms_id target_x target_y target_z target_ent_id state fx_opt judge_worldid judge_pilotid |
| `0x6D4B` | commander_subcmdr_notice | 240 | 待人工（alloc=0x1A0, sum=16） | `sub_BAA730` | 4 | B02DD0×4(u32) | - | worldids[] pilotids[] |
| `0x6D8F` | commander_support_debug_end | 228 | ★定长 11B | `sub_BAA630` | 6 | B05E30×3() B06230×3(u8) B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) | - | team troops support_type ent_id spt_ms_index spt_spot_index |
| `0x7155` | roomlobby_pilot_add_npc | 5 | 待人工（alloc=0x5B, sum=18） | `sub_BA8D00` | 12 | B05E30×8() B06230×8(u8) B41470×2() B02DD0×2(u32) B413B0×1() B02DF0×1(u16) B02BA0?×1() | - | team troops pilot_id level cutin_id name gender platoon platoon_slot is_platoon_leader dtaskf_order_number is_disable_scoreboard |
| `0x717D` | entity_msma_appear | 84 | 待人工（alloc=0x156, sum=22） | `sub_BA94F0` | 14 | B05E30×6() B06230×6(u8) B41470×3() B02DD0×3(u32) B413B0×2() B02DF0×2(u16) | - | team troops world_id pilot_id ms snapshot funnelss unattended_state_bit weapon_state_bits target_icon is_respawn is_using_ss stghold_number xweapon_fired |
| `0x7206` | roomlobby_game_start_r | 21 | ★定长 20B | `sub_BA8F60` | 5 | B41470×5() B02DD0×5(u32) | - | result elapsed_sec limit_sec kill_count death_count |
| `0x731C` | weapon_fire__start_homing_r | 130 | ★定长 12B | `sub_BA9C50` | 5 | B413B0×4() B02DF0×4(u16) B41470×1() B02DD0×1(u32) | - | grenade_id pos_x pos_y pos_z target_ent_id |
| `0x73CE` | entity_msma_attach | 90 | ★定长 11B | `sub_BA9650` | 6 | B413B0×5() B02DF0×5(u16) B05E30×1() B06230×1(u8) | - | ent_id attach_parent_ent_id attach_socket attach_pos_x attach_pos_y attach_pos_z |
| `0x747B` | weapon_fire__chain_mine | 146 | ★定长 12B | `sub_BA9E10` | 4 | B413B0×2() B02DF0×2(u16) B41470×2() B02DD0×2(u32) | - | from_ent_id to_ent_id weapon_itemid fire_id |
| `0x759C` | deliver_assault_stghold_ace_status | 264 | ★定长 17B | `sub_BAA9F0` | 9 | B413B0×5() B02DF0×5(u16) B05E30×3() B06230×3(u8) B41470×1() B02DD0×1(u32) | - | team troops ent_id target_x target_y target_z spt_spot_index spt_spot_dir remain_msec |
| `0x7621` | entity_msma_appear_self | 83 | 待人工（alloc=0x154, sum=20） | `sub_BAAED0` | None | B41470×4() B02DD0×4(u32) B05E30×2() B06230×2(u8) B413B0×1() B02DF0×1(u16) | - | team troops ms snapshot funnelss hp_now hp_max shield_hp_now shield_hp_max weapon_state_bits |
| `0x7626` | netcafe_challenge_progress_r | 275 | 待人工（alloc=0x3C, sum=0） | `sub_BAAED0` | None | - | - | netcafe_challenge_info[] |
| `0x7C83` | map_event_fog_change | 279 | ★定长 19B | `sub_BAAB10` | 7 | B41470×4() B02DD0×4(u32) B05E30×3() B06230×3(u8) | - | nearz farz color_r color_g color_b time elapsed_time |
| `0x7CD8` | commander_support_end | 227 | ★定长 11B | `sub_BAA600` | 6 | B05E30×3() B06230×3(u8) B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) | - | team troops support_type ent_id spt_ms_index spt_spot_index |
| `0x7CE0` | msma_AI_update_order | 195 | ★定长 7B | `sub_BAA340` | 3 | B413B0×1() B02DF0×1(u16) B05E30×1() B06230×1(u8) B41470×1() B02DD0×1(u32) | - | AI_ent_id kind param |
| `0x7D22` | chara_effect | 297 | ★定长 5B | `sub_BAAC80` | 3 | B413B0×2() B02DF0×2(u16) B05E30×1() B06230×1(u8) | - | ent_id effect_id is_start |
| `0x7D59` | roomlobby_pick_vote_result | 34 | 待人工（alloc=0x30, sum=16） | `sub_BA8FC0` | 4 | B02DD0×4(u32) B41470×2() | - | state vote_count[] pick_msma_id[] member_count |
| `0x8043` | tumble_ukemi_r | 108 | ★定长 6B | `sub_BA9A50` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id tmp |
| `0x80E8` | commander_support_cooltime_notice | 233 | ★定长 12B | `sub_BAA6D0` | 3 | B41470×3() B02DD0×3(u32) | - | support_type remain_msec target_change_msec |
| `0x8297` | game_resume | 57 | 待人工（alloc=0x39, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0x844B` | kill_count_update | 171 | ★定长 23B | `sub_BAA140` | 7 | B41470×5() B02DD0×5(u32) B413B0×1() B02DF0×1(u16) B05E30×1() B06230×1(u8) | - | reason ent_id_dead world_id_kill pilot_id_kill kill_streak weapon_itemid is_extend_style_change_limit |
| `0x84A5` | weapon_fire__wrestle_counter_r | 122 | ★定长 8B | `sub_BA9B20` | 3 | B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) | - | ent_id itemid target_ent_id |
| `0x86B2` | msma_spawn_select_r | 76 | 待人工（alloc=0x53, sum=18） | `sub_BA93E0` | 6 | B41470×4() B02DD0×4(u32) B413B0×1() B02DF0×1(u16) B02BA0?×1() | - | result ms_index post_index spt_spot_index respawn_ent_id script_ini |
| `0x894B` | weapon_fire__destruct | 142 | ★定长 6B | `sub_BA9DC0` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id weapon_itemid |
| `0x8A10` | setwpnparam | 290 | 待人工（alloc=0xC, sum=8） | `sub_BAABC0` | 3 | B41470×3() B02DD0×2(u32) | - | ent_id val type |
| `0x8C24` | roomlobby_pick_vote_cancel_r | 31 | ★定长 4B | `sub_BA8F90` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0x8D1F` | commander_support_spot_lock | 222 | ★定长 2B | `sub_BAA550` | 2 | B05E30×2() B06230×2(u8) | - | index is_lock |
| `0x8D3C` | weapon_hit_chain_mine | 157 | ★定长 14B | `sub_BA9F50` | 6 | B413B0×5() B02DF0×5(u16) B41470×1() B02DD0×1(u32) | - | weapon_itemid to_ent_id from_ent_id hit_pos_x hit_pos_y hit_pos_z |
| `0x8D42` | game_mapeffect_update | 67 | ★定长 5B | `sub_BA9340` | 2 | B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | fx_id is_scale |
| `0x8D58` | eqparts_ready_start_r | 166 | ★定长 13B | `sub_BAA0F0` | 5 | B41470×2() B02DD0×2(u32) B413B0×2() B02DF0×2(u16) B05E30×1() B06230×1(u8) | - | result frame_count AI_ent_id group_id reason |
| `0x8D59` | score_update | 172 | ★定长 28B | `sub_BAA170` | 8 | B41470×6() B02DD0×6(u32) B413B0×2() B02DF0×2(u16) | - | reason point_gain point_total is_taskforce_aux point_atk point_spt point_con kill_streak_chain_num |
| `0x8DE4` | msma_spawn_wait_update | 74 | ★定长 5B | `sub_BA93C0` | 3 | B413B0×2() B02DF0×2(u16) B05E30×1() B06230×1(u8) | - | deck_index respawn_wait_sec respawn_wait_max |
| `0x8EFD` | weapon_hit_from_with_module | 162 | ★定长 7B | `sub_BAA070` | 3 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | ent_id module_hp is_force |
| `0x8FFA` | commander_support_tell | 226 | ★定长 39B | `sub_BAA5A0` | 16 | B413B0×8() B02DF0×8(u16) B41470×5() B02DD0×5(u32) B05E30×3() B06230×3(u8) | - | team troops support_type ent_id target_x target_y target_z spt_ms_index spt_spot_index spt_spot_dir remain_cnt remain_msec use_worldid use_pilotid setter_ms val |
| `0x9105` | entity_msma_dead | 88 | ★定长 28B | `sub_BA95F0` | 10 | B41470×5() B02DD0×5(u32) B413B0×3() B02DF0×3(u16) B05E30×2() B06230×2(u8) | - | ent_id_dead world_id_kill pilot_id_kill decal_kill weapon_itemid repair_wait_sec kill_streak_count spbits is_resurrect is_extend_style_change_limit |
| `0x918E` | debug_message | 287 | 待人工（alloc=0xB9, sum=4） | `sub_BAAED0` | None | B02BA0?×1() B41470×1() B02DD0×1(u32) | - | msg color |
| `0x91C9` | battle_buffitem_list | 269 | 待人工（alloc=0xE0, sum=0） | `sub_BAAA80` | 2 | - | - | buffitem[] buffitem_ex[] |
| `0x97EC` | roomlobby_pick_vote_r | 29 | ★定长 4B | `sub_BA8F90` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0x9951` | msma_spawn_list_get_r_begin | 71 | ★定长 8B | `sub_BA9370` | 2 | B41470×2() B02DD0×2(u32) | - | spawn1st_post is_1st |
| `0x9A22` | eqparts_ready_cancel_r | 168 | ★定长 12B | `sub_BAA120` | 4 | B41470×2() B02DD0×2(u32) B413B0×2() B02DF0×2(u16) | - | result frame_count AI_ent_id group_id |
| `0x9A39` | room_kick_master_r | 44 | ★定长 4B | `sub_BA90C0` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0x9C14` | msma_AI_update_hate | 189 | 待人工（alloc=0x32, sum=14） | `sub_BAA2B0` | 5 | B02DF0×3(u16) B02DD0×2(u32) B413B0×1() | - | AI_ent_id ent_id[] val[] |
| `0xA39E` | msma_AI_change_movetype | 196 | ★定长 5B | `sub_BAA360` | 3 | B413B0×2() B02DF0×2(u16) B05E30×1() B06230×1(u8) | - | AI_ent_id action_type route_number |
| `0xA5DA` | authenticate_r | 3 | 待人工（alloc=0x2DE, sum=41） | `sub_BA8C20` | 20 | B41470×8() B02DD0×8(u32) B05E30×7() B06230×7(u8) B02BA0?×1() B418C0?×1() B077B0?×1() B05ED0?×1() B07880?×1() B413B0×1() B02DF0×1(u16) B05EE0?×1() B08160?×1() | - | result room_id room_name mission_id extrule_id dc_node_id is_rankerbattle map_id is_vsclan comeback_stat is_playing is_netcafe team is_practice config progress expup_fgauge is_ev_caravan flag_wideuse extrarule_xwar_info |
| `0xA63E` | mission_clear_countdown_start | 266 | ★定长 8B | `sub_BAAA40` | 2 | B41470×2() B02DD0×2(u32) | - | remain_msec clear_remain_msec |
| `0xA716` | mission_clear_countdown_cancel | 267 | ★定长 4B | `sub_BAAA60` | 1 | B41470×1() B02DD0×1(u32) | - | remain_msec |
| `0xA77E` | game_replay_result | 69 | ★定长 1B | `sub_BADBF0` | 1 | B05E30×1() B06230×1(u8) | - | win_team |
| `0xA78D` | weapon_fire__funnel_r | 148 | 待人工（alloc=0x51, sum=9） | `sub_BA9E30` | 4 | B02DD0×2(u32) B41470×1() B05E30×1() B06230×1(u8) | - | from_ent_id wslot_idx fire_points[] |
| `0xA7C3` | msma_AI_set_fire_point | 193 | ★定长 14B | `nullsub_38` | 7 | B413B0×7() B02DF0×7(u16) | - | AI_ent_id fire_x fire_y fire_z end_x end_y end_z |
| `0xA8F2` | weapon_hit_from_with_tumble | 159 | ★定长 16B | `sub_BA9FE0` | 6 | B413B0×4() B02DF0×4(u16) B41470×2() B02DD0×2(u32) | - | ent_id hit_dir spbits optbits down_power down_msec |
| `0xA8FB` | eqparts_ready_counter_notice | 170 | ★定长 14B | `sub_BAA0B0` | 4 | B41470×3() B02DD0×3(u32) B413B0×1() B02DF0×1(u16) | - | result ent_id count maxcount |
| `0xA959` | radar_captured_notice | 180 | ★定长 2B | `sub_BAA240` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id_radar |
| `0xA9E7` | weapon_fire__damage_field_r | 152 | ★定长 39B | `sub_BA9E70` | 18 | B413B0×12() B02DF0×12(u16) B41470×3() B02DD0×3(u32) B05E30×3() B06230×3(u8) | - | ent_id itemid grenade_id parent_id launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt charge_lv |
| `0xAA98` | combat_operation_end | 242 | ★定长 9B | `sub_BAA790` | 3 | B41470×2() B02DD0×2(u32) B05E30×1() B06230×1(u8) | - | support_type is_completed stg_arms_initiation_ms |
| `0xAB6F` | msma_spawn_list_get_r_end | 73 | 待人工（alloc=0x49, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0xAB9B` | combat_operation_target_change_r | 246 | ★定长 18B | `sub_BAA7D0` | 6 | B41470×3() B02DD0×3(u32) B413B0×3() B02DF0×3(u16) | - | result target_x target_y target_z use_worldid use_pilotid |
| `0xAC3D` | msma_change_team | 200 | ★定长 4B | `sub_BAA3B0` | 3 | B05E30×2() B06230×2(u8) B413B0×1() B02DF0×1(u16) | - | team troops ent_id |
| `0xACB0` | commander_get_pilotinfo_r | 218 | ★定长 7B | `sub_BAA500` | 4 | B413B0×3() B02DF0×3(u16) B05E30×1() B06230×1(u8) | - | target_member target_ace kill_cnt death_cnt |
| `0xB313` | system_message | 286 | 待人工（alloc=0xB9, sum=4） | `sub_BAAED0` | None | B02BA0?×1() B41470×1() B02DD0×1(u32) | - | msg color |
| `0xB334` | active_weapon_change_r | 112 | ★定长 12B | `sub_BA9A70` | 5 | B41470×2() B02DD0×2(u32) B05E30×2() B06230×2(u8) B413B0×1() B02DF0×1(u16) | - | ent_id result equip_index equip_itemid is_force |
| `0xB40C` | weapon_fire__grenade_r | 124 | ★定长 41B | `sub_BA9B40` | 20 | B413B0×12() B02DF0×12(u16) B05E30×5() B06230×5(u8) B41470×3() B02DD0×3(u32) | - | ent_id itemid grenade_id parent_id launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt charge_lv impact_wall action |
| `0xB463` | msma_AI_install | 181 | 待人工（alloc=0xAA, sum=2） | `sub_BAAED0` | None | B413B0×1() B02DF0×1(u16) | - | AI_ent_id AI |
| `0xB491` | weapon_fire__snipe_beam_r | 137 | ★定长 11B | `sub_BA9D10` | 5 | B413B0×3() B02DF0×3(u16) B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | ent_id target_x target_y target_z begin1_end0 |
| `0xB572` | repair_pack_supply | 204 | ★定长 6B | `sub_BAA410` | 2 | B41470×1() B02DD0×1(u32) B413B0×1() B02DF0×1(u16) | - | val equip_idx |
| `0xB604` | msma_AI_resume | 185 | ★定长 2B | `sub_BAA2A0` | 1 | B413B0×1() B02DF0×1(u16) | - | AI_ent_id |
| `0xB881` | roomlobby_ban_vote_r | 25 | ★定长 4B | `sub_BA8F90` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0xBA73` | cpf_authenticate | 283 | 待人工（alloc=0x84, sum=5） | `sub_BAAB70` | 2 | B02DD0×1(u32) B05EA0?×1() B06230×1(u8) | - | data[] |
| `0xBAE4` | entity_snapshot_splitdelta_compress | 99 | 待人工（alloc=0x750C, sum=13） | `sub_BA9990` | 4 | B02DD0×3(u32) B41470×2() B05EA0?×1() B06230×1(u8) | - | frame_count remain_msec zbuff[] |
| `0xBC13` | commander_select_r | 212 | ★定长 4B | `sub_BAA4A0` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0xBDC6` | game_read_ahead_route_notice | 52 | 待人工（alloc=0x104, sum=8） | `sub_BA9230` | 2 | B02DD0×2(u32) | - | read_ahead_route[] |
| `0xBDD6` | roomlobby_pilot_add | 4 | 待人工（alloc=0xC6, sum=22） | `sub_BAAED0` | None | B05E30×6() B06230×6(u8) B41470×4() B02DD0×4(u32) | - | team troops world_id pilot stat is_commander is_audience member_index dtaskf_order_number kill_count death_count |
| `0xC327` | pos_warp_force | 106 | ★定长 12B | `sub_BA9A20` | 6 | B413B0×6() B02DF0×6(u16) | - | ent_id pos_x pos_y pos_z dir reason |
| `0xC64E` | roomlobby_pilot_del | 6 | ★定长 8B | `sub_BA8DF0` | 2 | B41470×2() B02DD0×2(u32) | - | world_id pilot_id |
| `0xC66B` | game_round_end | 54 | 待人工（alloc=0x42, sum=2） | `sub_BAAED0` | None | B05E30×2() B06230×2(u8) B05ED0?×1() B07880?×1() | - | win_team win_troops progress |
| `0xCDE6` | game_score_ranker_notice | 68 | 待人工（alloc=0x44, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0xCE08` | eqparts_toggle | 164 | ★定长 9B | `sub_BAA0D0` | 4 | B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | ent_id group_id toggle reason |
| `0xCF40` | weapon_fire__hand_throw_bound_r | 128 | ★定长 18B | `sub_BA9C10` | 8 | B413B0×7() B02DF0×7(u16) B41470×1() B02DD0×1(u32) | - | grenade_id hit_x hit_y hit_z vec_x vec_y vec_z vec_power |
| `0xD1B3` | game_respawn_post_update | 65 | 待人工（alloc=0x7D4, sum=4） | `sub_BA9300` | 2 | B02DD0×1(u32) | - | post_progress[] |
| `0xD691` | commander_subcmdr_candidacy_start | 237 | ★定长 2B | `sub_BAA710` | 1 | B413B0×1() B02DF0×1(u16) | - | remain_sec |
| `0xD725` | weapon_fire__wrestle_r | 121 | ★定长 21B | `sub_BA9AE0` | 10 | B413B0×5() B02DF0×5(u16) B05E30×3() B06230×3(u8) B41470×2() B02DD0×2(u32) | - | ent_id itemid dir_h dir_v msec wrestle_id charge_lv action chase_ent_id is_dp_damage_cut |
| `0xD8B9` | module_toggle_time | 294 | ★定长 8B | `sub_BAAC20` | 3 | B413B0×2() B02DF0×2(u16) B41470×1() B02DD0×1(u32) | - | ent_id msec rate |
| `0xD94A` | game_suspend | 56 | 待人工（alloc=0x38, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0xDC00` | commander_support_execute_r | 225 | ★定长 4B | `sub_BAA590` | 1 | B41470×1() B02DD0×1(u32) | - | result |
| `0xDC1E` | bgm_change | 262 | 待人工（alloc=0x19, sum=5） | `sub_BAA990` | 2 | B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | bgm_desc fade_msec reset |
| `0xDCF2` | roomlobby_pilot_msdeck | 7 | 待人工（alloc=0x24, sum=21） | `sub_BA8E10` | 6 | B02DD0×5(u32) B41470×2() B05EA0?×1() B06230×1(u8) | - | world_id pilot_id deck_msid[] deck_mscolor[] |
| `0xDDE9` | module_toggle_level | 295 | ★定长 10B | `sub_BAAC40` | 3 | B41470×2() B02DD0×2(u32) B413B0×1() B02DF0×1(u16) | - | ent_id level_up_flag next_level_max |
| `0xDDF7` | weapon_hit_to_r | 156 | ★定长 16B | `sub_BA9F20` | 6 | B413B0×4() B02DF0×4(u16) B41470×2() B02DD0×2(u32) | - | weapon_itemid ent_id optbit hit_pos_x hit_pos_y hit_pos_z |
| `0xDE24` | proto_version_check_r | 1 | ★定长 12B | `sub_BAAE70` | 3 | B41470×3() B02DD0×3(u32) | - | version crc gentime |
| `0xE014` | battleship_ride_r | 253 | ★定长 32B | `sub_BAA870` | 9 | B41470×7() B02DD0×7(u32) B413B0×2() B02DF0×2(u16) | - | result from_world_id from_pilot_id from_ent_id to_ent_id hp_now hp_max shield_hp_now shield_hp_max |
| `0xE031` | repair_gauge_update | 178 | ★定长 4B | `sub_BAA210` | 2 | B413B0×2() B02DF0×2(u16) | - | gauge_old gauge_now |
| `0xE12A` | commander_candidacy_end | 216 | ★定长 12B | `sub_BAA4E0` | 3 | B41470×3() B02DD0×3(u32) | - | result cmdr_world_id cmdr_pilot_id |
| `0xE228` | msma_AI_reboot | 183 | ★定长 2B | `sub_BAA280` | 1 | B413B0×1() B02DF0×1(u16) | - | AI_ent_id |
| `0xE2DE` | module_toggle_point | 293 | ★定长 6B | `sub_BAAC00` | 3 | B413B0×3() B02DF0×3(u16) | - | ent_id point point_max |
| `0xE31F` | roomlobby_pilot_leave_appeal | 8 | 待人工（alloc=0x8, sum=0） | `sub_BAAED0` | None | - | - | - |
| `0xE332` | weapon_hit_from_with_stumble | 160 | ★定长 16B | `sub_BAA010` | 6 | B413B0×4() B02DF0×4(u16) B41470×2() B02DD0×2(u32) | - | ent_id hit_dir spbits optbits stumble_power stumble_msec |
| `0xE378` | weapon_fire__bit_r | 139 | ★定长 29B | `sub_BA9D40` | 14 | B413B0×9() B02DF0×9(u16) B05E30×3() B06230×3(u8) B41470×2() B02DD0×2(u32) | - | ent_id itemid bit_id shot_alive launch_x launch_y launch_z target_x target_y target_z target_ent_id msec release0_shot1 fx_opt |
| `0xE4DB` | entity_msma_show_hp | 95 | 待人工（alloc=0x6C, sum=18） | `sub_BA96F0` | 5 | B02DD0×4(u32) B02DF0×1(u16) B41470×1() | - | ent_id[] hp_max[] gauge_max |
| `0xE5FC` | msma_spawn_warp_countdown_finish | 81 | ★定长 2B | `sub_BA9490` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0xE861` | itembox_alarm | 208 | ★定长 2B | `sub_BAA470` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0xE8EE` | demolition_breakthrough_result | 278 | ★定长 5B | `sub_BAAAF0` | 2 | B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | group_id is_succcess |
| `0xE96B` | repair_waittime_update | 179 | ★定长 2B | `sub_BAA230` | 1 | B413B0×1() B02DF0×1(u16) | - | repair_wait_sec |
| `0xEAB3` | mission_goal_text | 268 | 待人工（alloc=0x61, sum=0） | `sub_BAAED0` | None | B02BA0?×1() | - | text |
| `0xEAEA` | weapon_fire_prepare__destruct | 140 | ★定长 10B | `sub_BA9DA0` | 3 | B41470×2() B02DD0×2(u32) B413B0×1() B02DF0×1(u16) | - | ent_id weapon_itemid fire_id |
| `0xEB53` | battle_contribute_rank | 175 | ★定长 4B | `sub_BAA200` | 1 | B41470×1() B02DD0×1(u32) | - | rank |
| `0xED22` | wrestle_chase_move_end_r | 301 | ★定长 2B | `sub_BAACE0` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0xEDFC` | weapon_fire__bit_reflect_r | 154 | ★定长 21B | `sub_BA9EE0` | 10 | B413B0×8() B02DF0×8(u16) B41470×1() B02DD0×1(u32) B05E30×1() B06230×1(u8) | - | ent_id itemid launch_x launch_y launch_z target_x target_y target_z charge_lv reflect_ent_id |
| `0xEE73` | map_event_linkfx_change | 280 | 待人工（alloc=0x41, sum=0） | `sub_BAAB40` | 1 | B02BA0?×1() | - | path |
| `0xF4D7` | shield_any_damage | 296 | ★定长 6B | `sub_BAAC60` | 2 | B413B0×1() B02DF0×1(u16) B41470×1() B02DD0×1(u32) | - | ent_id damage |
| `0xF77B` | itembox_open | 207 | ★定长 10B | `sub_BAA450` | 3 | B41470×2() B02DD0×2(u32) B413B0×1() B02DF0×1(u16) | - | itembox_ent_id itemid trap_weaponid |
| `0xF87E` | badge_add | 174 | ★定长 2B | `sub_BAA1E0` | 2 | B05E30×2() B06230×2(u8) | - | rank badge_type |
| `0xF88B` | mission_safety_area_over_penalty | 304 | ★定长 2B | `sub_BAAD20` | 1 | B413B0×1() B02DF0×1(u16) | - | ent_id |
| `0xFD8A` | examination_progress_r | 271 | 待人工（alloc=0x58, sum=8） | `sub_BAAAA0` | 3 | B41470×2() B02DD0×2(u32) | - | examination_info[] examination_playscore examination_playsec_remain_msec |
| `0xFE02` | daily_record_progress_r | 273 | 待人工（alloc=0x3C, sum=0） | `sub_BAAED0` | None | - | - | daily_record_info[] |
| `0xFE50` | roomlobby_pick_vote_deck | 36 | 待人工（alloc=0x24, sum=12） | `sub_BA8FE0` | 3 | B02DD0×3(u32) B41470×1() | - | state msma_id[] enemy_msma_id[] |
| `0xFEBB` | msma_spawn_warp_start_r | 79 | ★定长 14B | `sub_BA9450` | 4 | B41470×3() B02DD0×3(u32) B413B0×1() B02DF0×1(u16) | - | result is_cancel ent_id countdown_msec |

## 2. C→S 全表

| ID | 报文 | 发送函数 | 解析/打包序列 | 字段（序） |
|---|---|---|---|---|
| `0x0372` | game_mission_progress_get | `sub_B33C10` | - | - |
| `0x03F7` | ban_transform | `sub_B40960` | - | ent_id val |
| `0x0452` | room_kick_vote | `sub_B332B0` | B02D80?×1() | target_world_id target_pilot_id kick_reason |
| `0x045B` | msma_AI_ping | `sub_B3CCB0` | - | AI_ent_id |
| `0x05CA` | wrestle_chase_move_start | `sub_B40B50` | B02DA0?×5() B02D80?×2() | frame_count dir_h wrestle_id chase_time_msec target_ent_id target_pos_x target_pos_y target_pos_z AI_ent_id |
| `0x07C9` | entity_deploy_arms_attach | `sub_B34670` | B02DA0?×3() | arms_id attach_parent_ent_id attach_pos_x attach_pos_y attach_pos_z |
| `0x085F` | check_progress_quest | `sub_B40390` | - | - |
| `0x0BDD` | cpf_authenticate_r | `sub_B40520` | - | data[] |
| `0x11A9` | weapon_fire__shot_single_special | `sub_B36C80` | B02DA0?×1() | frame_count itemid AI_ent_id |
| `0x16DB` | roomlobby_ban_vote | `sub_B32630` | - | msma_id |
| `0x1C33` | save_message | `sub_B40770` | B02B40?×1() | msg |
| `0x1E04` | commander_subcmdr_candidacy_inbattle | `sub_B3EE70` | - | - |
| `0x271F` | battleship_crash_impact | `sub_B3FCD0` | - | from_ent_id to_ent_id |
| `0x2761` | roomlobby_game_ready | `sub_B32180` | - | stat |
| `0x2ADC` | weapon_fire__wrestle | `sub_B36EC0` | B02DA0?×4() B061C0?×3() B02D80?×1() | frame_count dir_h dir_v msec wrestle_id charge_lv AI_ent_id action chase_ent_id is_dp_damage_cut |
| `0x2CAB` | game_round_ready | `sub_B33680` | - | - |
| `0x2DA4` | access_to | `sub_B35B70` | - | access_ent_id AI_ent_id |
| `0x31D2` | active_weapon_mode_change | `sub_B362F0` | - | mode AI_ent_id |
| `0x34A9` | proto_version_check | `sub_B318D0` | B02D80?×1() | version crc gentime |
| `0x34BE` | preset_voice_up_commander | `sub_B34D20` | - | voice_id AI_ent_id |
| `0x34C8` | roomlobby_ban_vote_cancel | `sub_B327E0` | - | msma_id |
| `0x36AC` | weapon_fire__for_myself | `sub_B3A1F0` | B02DA0?×5() B061C0?×1() | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all begin1_end0 AI_ent_id |
| `0x379B` | cutin_up | `sub_B34F10` | B02D80×3(u32) B032A0×1(u16) B061C0×1(u8) | cutin_category_id AI_ent_id to_world_id to_pilot_id to_range（**体 15B**；缓冲 22B；**通知 103**） |
| `0x3AF6` | weapon_fire__hand_throw_bound | `sub_B37F60` | B02DA0?×8() | frame_count grenade_id hit_x hit_y hit_z vec_x vec_y vec_z vec_power AI_ent_id |
| `0x421B` | pos_move | `sub_B351D0` | B02DA0?×15() B061C0?×3() B02D80?×2() | frame_count pos_x pos_y pos_z dir dir_eye target_x target_y target_z spbits spbits2 lockon_ent_id in_water_index layer_index access_ent_id1 access_ent_id2 rideon_ent_id spot_ent_id AI_ent_id operate_ent_id is_under_water hack_check[] |
| `0x434C` | msma_AI_move_stuckescape | `sub_B3D600` | B02DA0?×3() | AI_ent_id to_x to_y to_z msec |
| `0x444D` | room_kick_master | `sub_B330C0` | - | world_id pilot_id |
| `0x5456` | msma_AI_set_stat | `sub_B3CE60` | B02D80?×2() | AI_ent_id idx[] num[] |
| `0x5A5D` | eqparts_exec_toggle | `sub_B3C750` | B02DA0?×1() | frame_count AI_ent_id group_id |
| `0x6007` | wrestle_chase_move_end | `sub_B40F20` | - | frame_count AI_ent_id |
| `0x6486` | commander_support_execute | `sub_B3E580` | B02DA0?×2() B061C0?×1() B02D80?×1() | support_type target_x target_y target_z spt_spot_index val |
| `0x6636` | commander_order_assist | `sub_B3E3D0` | - | type |
| `0x692B` | dynamic_taskforce_order_issue | `sub_B3F3F0` | B02D80?×2() B061C0?×1() B02DA0?×1() | order_kind order_param select_members[] select_npcs[] |
| `0x6BCD` | msma_AI_hate_control | `sub_B3D210` | B02DA0?×1() | AI_ent_id target_ent_id hate_adjust |
| `0x6C48` | commander_candidacy_inbattle | `sub_B3E050` | - | - |
| `0x6FA1` | combat_operation_container_collect | `sub_B3F000` | - | destination |
| `0x770D` | weapon_hit_to | `sub_B3B7A0` | B02D80?×11() B02DA0?×10() B061C0?×3() | phash frame_count weapon_itemid fire_id ent_ids[] hit_pos_x[] hit_pos_y[] hit_pos_z[] hit_dirs[] hit_distance[] body_distance[] body_regions[] charge_lv AI_ent_id instate_from_ent_id create_frame_count is_down_range is_wrestle_first_high_lockon |
| `0x77C0` | examination_progress | `sub_B40070` | - | - |
| `0x7916` | funnel_snapshot_self | `sub_B3AB30` | - | snapshot |
| `0x7938` | roomlobby_pick_vote_cancel | `sub_B32B40` | - | msma_id |
| `0x7B52` | msma_spawn_warp_start | `sub_B34240` | - | is_cancel |
| `0x7C0C` | weapon_fire__hand_throw | `sub_B379F0` | B02DA0?×8() B061C0?×4() B02D80?×1() | frame_count launch_x launch_y launch_z target_x target_y target_z target_ent_id msec shot0_impact1 fx_opt impact_grenade_id charge_lv AI_ent_id salvo_slot |
| `0x7CA0` | weapon_fire__shot_single | `sub_B364E0` | B02DA0?×5() B061C0?×2() | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all charge_lv AI_ent_id salvo_slot |
| `0x7E45` | roomlobby_pick_vote | `sub_B32990` | - | msma_id |
| `0x800A` | msma_spawn_warp_select | `sub_B343F0` | B061C0?×1() B02DA0?×1() | post_index spt_spot_index is_btlship_ride respawn_ent_id |
| `0x8898` | weapon_fire__damage_field | `sub_B3AD30` | B02DA0?×11() B061C0?×3() B02D80?×2() | frame_count launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt impact_grenade_id parent_grenade_id charge_lv AI_ent_id |
| `0x9B19` | roomlobby_pilot_mindex_update | `sub_B31E20` | - | member_index |
| `0x9F0D` | preset_voice_up | `sub_B34930` | B061C0?×4() B02D80?×2() B02B40?×1() | voice_id AI_ent_id to_world_id to_pilot_id is_party is_use_textmsg textmsg is_cutin is_voice |
| `0xA0EA` | weapon_fire__bit_reflect | `sub_B3B350` | B02DA0?×8() B061C0?×1() | frame_count itemid launch_x launch_y launch_z target_x target_y target_z charge_lv AI_ent_id reflect_ent_id |
| `0xA404` | weapon_fire__shot_rapid | `sub_B368B0` | B02DA0?×5() B061C0?×2() | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all begin1_end0 AI_ent_id salvo_slot |
| `0xA4C9` | weapon_fire__bit | `sub_B39420` | B02DA0?×10() B061C0?×3() | frame_count shot_bit_id shot_ent_id shot_alive launch_x launch_y launch_z target_x target_y target_z target_ent_id msec release0_shot1 fx_opt AI_ent_id |
| `0xA537` | roomlobby_xwar_commander_lot | `sub_B31FD0` | - | is_lot |
| `0xA8FE` | weapon_fire_prepare__destruct_r | `sub_B39990` | B02D80?×8() B02DA0?×6() | frame_count weapon_itemid fire_id ent_ids[] hit_pos_x[] hit_pos_y[] hit_pos_z[] hit_dirs[] hit_distance[] body_regions[] AI_ent_id |
| `0xB015` | rideable_msma_get_down | `sub_B3FEC0` | - | reason |
| `0xB10A` | msma_AI_arrive_move_end | `sub_B3D450` | - | AI_ent_id |
| `0xBA58` | battleship_ride | `sub_B3F970` | - | to_ent_id |
| `0xBAFF` | room_chat_editing | `sub_B32F10` | - | is_editing |
| `0xBB1A` | room_chat_up | `sub_B32CF0` | B02B40?×1() | msg is_party |
| `0xBB6D` | xwar_commander_subcmdr_lot | `sub_B3ECC0` | - | is_lot |
| `0xBCA5` | dynamic_taskforce_order_change_party | `sub_B3F780` | - | order_kind order_param |
| `0xBCB4` | commander_support_hit_to | `sub_B3E890` | B02D80?×3() B02DA0?×2() B061C0?×1() | ent_id hit_team hit_troops support_type ent_ids[] hit_dirs[] |
| `0xBDD2` | game_client_signal | `sub_B33A60` | - | sigval |
| `0xBEE3` | weapon_fire__start_homing | `sub_B38370` | B02DA0?×4() | frame_count grenade_id pos_x pos_y pos_z target_ent_id |
| `0xBFA9` | weapon_fire__deploy_arms | `sub_B38670` | B02DA0?×4() B061C0?×3() B02D80?×2() | frame_count target_x target_y target_z target_ent_id state fx_opt impact_arms_id AI_ent_id is_gmk index |
| `0xC166` | eqparts_ready_start | `sub_B3C290` | B02DA0?×1() B061C0?×1() | frame_count AI_ent_id group_id reason |
| `0xC3BD` | weapon_fire__snipe_beam | `sub_B39090` | B02DA0?×5() B061C0?×1() | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all begin1_end0 AI_ent_id |
| `0xC84F` | bullet_supply_r | `sub_B3D8D0` | - | percent_val equip_idx |
| `0xC90D` | weapon_fire__air_bomb | `sub_B38AC0` | B02DA0?×3() B061C0?×2() B02D80?×1() | frame_count target_x target_y target_z shot0_drop1_impact2 fx_opt airbomb_id AI_ent_id |
| `0xCAAE` | object_put | `sub_B35D60` | B02DA0?×4() B061C0?×1() | frame_count target_x target_y target_z attach_parent_ent_id is_initiation AI_ent_id |
| `0xCAAF` | commander_get_pilotinfo | `sub_B3E1E0` | - | target_member target_ace |
| `0xCB97` | game_resume_enter | `sub_B33810` | B02B40?×1() | is_initial script_thread src |
| `0xCF71` | room_kick_vote_get_enable_pilots | `sub_B334F0` | - | - |
| `0xCFC8` | emergency_escape | `sub_B3C990` | - | - |
| `0xD2AE` | repair_pack_supply_r | `sub_B3DAC0` | - | val equip_idx |
| `0xD2C3` | weapon_fire__grenade | `sub_B372D0` | B02DA0?×11() B061C0?×6() B02D80?×3() | frame_count launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt impact_grenade_id parent_grenade_id charge_lv ent_id AI_ent_id impact_wall salvo_slot action |
| `0xD97D` | roomlobby_exit | `sub_B324B0` | - | - |
| `0xDAE0` | commander_list_get | `sub_B3DCB0` | - | team troops |
| `0xDDB7` | eqparts_ready_cancel | `sub_B3C510` | B02DA0?×1() | frame_count AI_ent_id group_id |
| `0xE041` | msma_spawn_list_get | `sub_B33DA0` | - | - |
| `0xE1C1` | weapon_fire__air_bomb_intercepted | `sub_B38E50` | B02D80?×1() | ent_id airbomb_id arms_id |
| `0xE314` | weapon_fire__camera | `sub_B3A580` | B02D80?×1() | frame_count ent_ids[] AI_ent_id |
| `0xE650` | msma_spawn_select | `sub_B33F30` | B061C0?×2() B02D80?×1() B02DA0?×1() | ms_index post_index spt_spot_index is_btlship_ride is_msma_ride respawn_ent_id |
| `0xE742` | combat_operation_target_change | `sub_B3F1B0` | B02DA0?×1() | target_x target_y target_z |
| `0xEA5A` | active_weapon_change | `sub_B360B0` | B02DA0?×1() | frame_count equip_index AI_ent_id |
| `0xEDBC` | tumble_ukemi | `sub_B35980` | - | AI_ent_id tmp |
| `0xEDD6` | daily_record_progress | `sub_B40200` | - | - |
| `0xF24B` | authenticate | `sub_B31B10` | B02D80?×2() B02B40?×1() B061C0?×1() | userid world_id pilot_id room_id otp_battle is_comeback |
| `0xF4B9` | battleship_get_down | `sub_B3FB20` | - | reason |
| `0xF51E` | emergency_self_destruct | `sub_B3CB20` | - | - |
| `0xF741` | roomlobby_game_start | `sub_B32330` | - | - |
| `0xF79B` | commander_select | `sub_B3DEA0` | - | commander_id |
| `0xFBC1` | weapon_fire__funnel | `sub_B3A860` | B02D80?×1() | from_ent_id wslot_idx fire_points[] |

## 3. 生命周期分组（把 287 条按战斗流程归位）

### S1 连接/握手（7 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| C→S | `0x0BDD` | cpf_authenticate_r | - | `sub_B40520`(发送) | data[] |
| S→C | `0x2C60` | cpf_authenticate_error | ★定长 4B / 1参 | `sub_BAAB90` | result |
| C→S | `0x34A9` | proto_version_check | - | `sub_B318D0`(发送) | version crc gentime |
| S→C | `0xA5DA` | authenticate_r | 待人工（alloc=0x2DE, sum=41） / 20参 | `sub_BA8C20` | result room_id room_name mission_id extrule_id dc_node_id is_rankerbattle map_id is_vsclan comeback_stat is_playing is_netcafe team is_practice config progress expup_fgauge is_ev_caravan flag_wideuse extrarule_xwar_info |
| S→C | `0xBA73` | cpf_authenticate | 待人工（alloc=0x84, sum=5） / 2参 | `sub_BAAB70` | data[] |
| S→C | `0xDE24` | proto_version_check_r | ★定长 12B / 3参 | `sub_BAAE70` | version crc gentime |
| C→S | `0xF24B` | authenticate | - | `sub_B31B10`(发送) | userid world_id pilot_id room_id otp_battle is_comeback |

### S2 房间大厅（44 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| C→S | `0x0452` | room_kick_vote | - | `sub_B332B0`(发送) | target_world_id target_pilot_id kick_reason |
| S→C | `0x07E9` | room_kick_vote_get_enable_pilots_r | 待人工（alloc=0x1AC, sum=20） / 5参 | `sub_BA90F0` | enable_worlds[] enable_pilots[] result |
| S→C | `0x0B3E` | roomlobby_pilot_mindex_update_r | ★定长 14B / 5参 | `sub_BA8E70` | result world_id pilot_id member_index is_commander |
| S→C | `0x0EC5` | room_kick_to | 待人工（alloc=0x2D, sum=0） / None参 | `sub_BAAED0` | - |
| S→C | `0x12EC` | room_chat_down | 待人工（alloc=0xDB, sum=13） / 9参 | `sub_BA9040` | team troops world_id pilot_id pilot_name msg is_all is_party is_audience |
| S→C | `0x14C5` | roomlobby_exit_r | 待人工（alloc=0x17, sum=0） / None参 | `sub_BAAED0` | - |
| C→S | `0x16DB` | roomlobby_ban_vote | - | `sub_B32630`(发送) | msma_id |
| S→C | `0x1ED8` | roomlobby_ban_vote_cancel_r | ★定长 4B / 1参 | `sub_BA8F90` | result |
| C→S | `0x2761` | roomlobby_game_ready | - | `sub_B32180`(发送) | stat |
| S→C | `0x27F3` | room_kick_vote_r | ★定长 4B / 1参 | `sub_BA90E0` | result |
| S→C | `0x30A9` | roomlobby_ban_vote_result | 待人工（alloc=0x30, sum=16） / 4参 | `sub_BA8FA0` | state vote_count[] ban_msma_id[] member_count |
| S→C | `0x315C` | roomlobby_xwar_commander_lot_r | ★定长 7B / 3参 | `sub_BA8ED0` | result is_lot lot_count |
| S→C | `0x339C` | roomlobby_game_ready_r | ★定长 16B / 4参 | `sub_BA8F40` | result world_id pilot_id stat |
| C→S | `0x34C8` | roomlobby_ban_vote_cancel | - | `sub_B327E0`(发送) | msma_id |
| S→C | `0x3BBE` | room_chat_editing_r | ★定长 9B / 3参 | `sub_BA9080` | world_id pilot_id is_editing |
| C→S | `0x444D` | room_kick_master | - | `sub_B330C0`(发送) | world_id pilot_id |
| S→C | `0x5913` | roomlobby_roommaster_notice | ★定长 8B / 2参 | `sub_BA8EA0` | world_id pilot_id |
| S→C | `0x5D2A` | roomlobby_clan_notice | 待人工（alloc=0x28, sum=9） / 7参 | `sub_BA8EF0` | team troops clan_id clan_name clan_emb_base clan_emb_parts1 clan_emb_parts2 |
| S→C | `0x6A0F` | roomlobby_vote_get_comeback | 待人工（alloc=0x14, sum=8） / None参 | `sub_BAAED0` | state msma_id[] |
| S→C | `0x6A38` | roomlobby_pilot_level_update | ★定长 12B / 4参 | `sub_BA8E50` | world_id pilot_id lv_old lv_new |
| S→C | `0x6A8D` | roomlobby_xwar_countdown | ★定长 4B / 1参 | `sub_BA8EC0` | sec |
| S→C | `0x6B2C` | roomlobby_cupteam_notice | ★定长 13B / 4参 | `sub_BA8F20` | team cupteam_id cupteam_rate tournament_vs_type |
| S→C | `0x6B71` | roomlobby_vote_state | ★定长 8B / 2参 | `sub_BA9000` | state sec |
| S→C | `0x7155` | roomlobby_pilot_add_npc | 待人工（alloc=0x5B, sum=18） / 12参 | `sub_BA8D00` | team troops pilot_id level cutin_id name gender platoon platoon_slot is_platoon_leader dtaskf_order_number is_disable_scoreboard |
| S→C | `0x7206` | roomlobby_game_start_r | ★定长 20B / 5参 | `sub_BA8F60` | result elapsed_sec limit_sec kill_count death_count |
| C→S | `0x7938` | roomlobby_pick_vote_cancel | - | `sub_B32B40`(发送) | msma_id |
| S→C | `0x7D59` | roomlobby_pick_vote_result | 待人工（alloc=0x30, sum=16） / 4参 | `sub_BA8FC0` | state vote_count[] pick_msma_id[] member_count |
| C→S | `0x7E45` | roomlobby_pick_vote | - | `sub_B32990`(发送) | msma_id |
| S→C | `0x8C24` | roomlobby_pick_vote_cancel_r | ★定长 4B / 1参 | `sub_BA8F90` | result |
| S→C | `0x97EC` | roomlobby_pick_vote_r | ★定长 4B / 1参 | `sub_BA8F90` | result |
| S→C | `0x9A39` | room_kick_master_r | ★定长 4B / 1参 | `sub_BA90C0` | result |
| C→S | `0x9B19` | roomlobby_pilot_mindex_update | - | `sub_B31E20`(发送) | member_index |
| C→S | `0xA537` | roomlobby_xwar_commander_lot | - | `sub_B31FD0`(发送) | is_lot |
| S→C | `0xB881` | roomlobby_ban_vote_r | ★定长 4B / 1参 | `sub_BA8F90` | result |
| C→S | `0xBAFF` | room_chat_editing | - | `sub_B32F10`(发送) | is_editing |
| C→S | `0xBB1A` | room_chat_up | - | `sub_B32CF0`(发送) | msg is_party |
| S→C | `0xBDD6` | roomlobby_pilot_add | 待人工（alloc=0xC6, sum=22） / None参 | `sub_BAAED0` | team troops world_id pilot stat is_commander is_audience member_index dtaskf_order_number kill_count death_count |
| S→C | `0xC64E` | roomlobby_pilot_del | ★定长 8B / 2参 | `sub_BA8DF0` | world_id pilot_id |
| C→S | `0xCF71` | room_kick_vote_get_enable_pilots | - | `sub_B334F0`(发送) | - |
| C→S | `0xD97D` | roomlobby_exit | - | `sub_B324B0`(发送) | - |
| S→C | `0xDCF2` | roomlobby_pilot_msdeck | 待人工（alloc=0x24, sum=21） / 6参 | `sub_BA8E10` | world_id pilot_id deck_msid[] deck_mscolor[] |
| S→C | `0xE31F` | roomlobby_pilot_leave_appeal | 待人工（alloc=0x8, sum=0） / None参 | `sub_BAAED0` | - |
| C→S | `0xF741` | roomlobby_game_start | - | `sub_B32330`(发送) | - |
| S→C | `0xFE50` | roomlobby_pick_vote_deck | 待人工（alloc=0x24, sum=12） / 3参 | `sub_BA8FE0` | state msma_id[] enemy_msma_id[] |

### S3 开局/出击（37 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x0120` | entity_msma_show | ★定长 2B / 1参 | `sub_BA96A0` | ent_id |
| C→S | `0x0372` | game_mission_progress_get | - | `sub_B33C10`(发送) | - |
| S→C | `0x057A` | entity_deploy_arms_appear | 待人工（alloc=0x60, sum=0） / 1参 | `sub_BA9550` | appear_info |
| C→S | `0x07C9` | entity_deploy_arms_attach | - | `sub_B34670`(发送) | arms_id attach_parent_ent_id attach_pos_x attach_pos_y attach_pos_z |
| S→C | `0x1113` | game_script_play | 待人工（alloc=0x43, sum=2） / None参 | `sub_BAAED0` | src is_with_resume script_thread |
| S→C | `0x1159` | game_mapgimmick_update | 待人工（alloc=0x404, sum=4） / 2参 | `sub_BA9320` | gimmick_progress[] |
| S→C | `0x1365` | game_begin | 待人工（alloc=0x2806, sum=66） / 23参 | `sub_BA9120` | snapshot_int_msec snapshot_res_msec pos_factor map_id btlfield clear_remain_msec is_disable_conq_sp is_room_suspend mission_id sudden_type sudden_bonus_target exp_min exp_max config progress respawn_posts[] mapgimmicks[] bgm_desc missionunit_set[] mission_phase |
| S→C | `0x1E2F` | msma_spawn_list_get_r_one | 待人工（alloc=0x10C, sum=4） / None参 | `sub_BAAED0` | index ms |
| S→C | `0x243B` | game_btlfield_change | ★定长 4B / 1参 | `sub_BA9220` | btlfield |
| C→S | `0x2CAB` | game_round_ready | - | `sub_B33680`(发送) | - |
| S→C | `0x3298` | msma_spawn_force_warp_start | ★定长 6B / 2参 | `sub_BA9470` | ent_id countdown_msec |
| S→C | `0x3E23` | game_mission_progress_update | 待人工（alloc=0x40, sum=0） / 1参 | `sub_BA92F0` | mprogress |
| S→C | `0x4D96` | game_client_signal_r | ★定长 4B / 1参 | `sub_BA92A0` | sigval |
| S→C | `0x611B` | game_script_play_also_replay | 待人工（alloc=0x42, sum=1） / 2参 | `sub_BA92D0` | src script_thread |
| S→C | `0x640D` | msma_spawn_info_prestart | 待人工（alloc=0x179, sum=27） / 9参 | `sub_BA9410` | remain_sec mstype[] post_index[] spt_spot_index[] stghold_entid[] |
| S→C | `0x6475` | game_coopwave_result | 待人工（alloc=0x2C, sum=0） / 1参 | `sub_BA9250` | wave_res |
| C→S | `0x7B52` | msma_spawn_warp_start | - | `sub_B34240`(发送) | is_cancel |
| C→S | `0x800A` | msma_spawn_warp_select | - | `sub_B343F0`(发送) | post_index spt_spot_index is_btlship_ride respawn_ent_id |
| S→C | `0x8297` | game_resume | 待人工（alloc=0x39, sum=0） / None参 | `sub_BAAED0` | - |
| S→C | `0x86B2` | msma_spawn_select_r | 待人工（alloc=0x53, sum=18） / 6参 | `sub_BA93E0` | result ms_index post_index spt_spot_index respawn_ent_id script_ini |
| S→C | `0x8D42` | game_mapeffect_update | ★定长 5B / 2参 | `sub_BA9340` | fx_id is_scale |
| S→C | `0x8DE4` | msma_spawn_wait_update | ★定长 5B / 3参 | `sub_BA93C0` | deck_index respawn_wait_sec respawn_wait_max |
| S→C | `0x9951` | msma_spawn_list_get_r_begin | ★定长 8B / 2参 | `sub_BA9370` | spawn1st_post is_1st |
| S→C | `0xA77E` | game_replay_result | ★定长 1B / 1参 | `sub_BADBF0` | win_team |
| S→C | `0xAB6F` | msma_spawn_list_get_r_end | 待人工（alloc=0x49, sum=0） / None参 | `sub_BAAED0` | - |
| S→C | `0xBDC6` | game_read_ahead_route_notice | 待人工（alloc=0x104, sum=8） / 2参 | `sub_BA9230` | read_ahead_route[] |
| C→S | `0xBDD2` | game_client_signal | - | `sub_B33A60`(发送) | sigval |
| S→C | `0xC66B` | game_round_end | 待人工（alloc=0x42, sum=2） / None参 | `sub_BAAED0` | win_team win_troops progress |
| C→S | `0xCB97` | game_resume_enter | - | `sub_B33810`(发送) | is_initial script_thread src |
| S→C | `0xCDE6` | game_score_ranker_notice | 待人工（alloc=0x44, sum=0） / None参 | `sub_BAAED0` | - |
| S→C | `0xD1B3` | game_respawn_post_update | 待人工（alloc=0x7D4, sum=4） / 2参 | `sub_BA9300` | post_progress[] |
| S→C | `0xD94A` | game_suspend | 待人工（alloc=0x38, sum=0） / None参 | `sub_BAAED0` | - |
| C→S | `0xE041` | msma_spawn_list_get | - | `sub_B33DA0`(发送) | - |
| S→C | `0xE4DB` | entity_msma_show_hp | 待人工（alloc=0x6C, sum=18） / 5参 | `sub_BA96F0` | ent_id[] hp_max[] gauge_max |
| S→C | `0xE5FC` | msma_spawn_warp_countdown_finish | ★定长 2B / 1参 | `sub_BA9490` | ent_id |
| C→S | `0xE650` | msma_spawn_select | - | `sub_B33F30`(发送) | ms_index post_index spt_spot_index is_btlship_ride is_msma_ride respawn_ent_id |
| S→C | `0xFEBB` | msma_spawn_warp_start_r | ★定长 14B / 4参 | `sub_BA9450` | result is_cancel ent_id countdown_msec |

### S4 实体同步（27 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x0825` | weapon_state_update | ★定长 6B / 3参 | `sub_BA9AA0` | ent_id weapon_state weapon_change_flag |
| S→C | `0x0943` | entity_msma_disappear | ★定长 8B / 3参 | `sub_BA95C0` | ent_id reason not_use |
| S→C | `0x130A` | entity_msma_hide | ★定长 2B / 1参 | `sub_BA9690` | ent_id |
| S→C | `0x16AA` | eqparts_execute | 待人工（alloc=0x2086, sum=6） / None参 | `sub_BAAED0` | ent_id parts_exec[] |
| S→C | `0x1B67` | funnel_snapshot_all | 待人工（alloc=0x4E4, sum=4） / 2参 | `sub_BA9E50` | snapshot_arr[] |
| S→C | `0x1EA5` | entity_msma_reborn | ★定长 4B / 2参 | `sub_BA9630` | ent_id hp_percent |
| C→S | `0x31D2` | active_weapon_mode_change | - | `sub_B362F0`(发送) | mode AI_ent_id |
| S→C | `0x4C7D` | entity_msma_unattended_state | ★定长 4B / 2参 | `sub_BA9720` | ent_id state_bit |
| S→C | `0x568A` | entity_snapshot | 待人工（alloc=0x8F0C, sum=12） / 4参 | `sub_BA9740` | frame_count remain_msec snapshots[] |
| C→S | `0x5A5D` | eqparts_exec_toggle | - | `sub_B3C750`(发送) | frame_count AI_ent_id group_id |
| S→C | `0x5C4F` | entity_msma_detach | ★定长 2B / 1参 | `sub_BA9680` | ent_id |
| S→C | `0x5EEA` | entity_snapshot_splitdelta | 待人工（alloc=0x9FC4, sum=167） / None参 | `sub_BAAED0` | frame_count remain_msec ent_id[] dirty_bits[] pos_real_x[] pos_real_y[] pos_real_z[] pos_diff_x[] pos_diff_y[] pos_diff_z[] dir[] target_real_x[] target_real_y[] target_real_z[] target_diff_x[] target_diff_y[] target_diff_z[] spbit_ll[] spbit_l[] spbit_h[] spbit_hh[] spbit2[] hp_percent[] hp_percent_shield[] down_power[] equip_index[] score1[] water_index[] score2[] layer_index[] score3[] rideon_ent_id[] lockon_ent_id[] |
| S→C | `0x717D` | entity_msma_appear | 待人工（alloc=0x156, sum=22） / 14参 | `sub_BA94F0` | team troops world_id pilot_id ms snapshot funnelss unattended_state_bit weapon_state_bits target_icon is_respawn is_using_ss stghold_number xweapon_fired |
| S→C | `0x73CE` | entity_msma_attach | ★定长 11B / 6参 | `sub_BA9650` | ent_id attach_parent_ent_id attach_socket attach_pos_x attach_pos_y attach_pos_z |
| S→C | `0x7621` | entity_msma_appear_self | 待人工（alloc=0x154, sum=20） / None参 | `sub_BAAED0` | team troops ms snapshot funnelss hp_now hp_max shield_hp_now shield_hp_max weapon_state_bits |
| C→S | `0x7916` | funnel_snapshot_self | - | `sub_B3AB30`(发送) | snapshot |
| S→C | `0x8D58` | eqparts_ready_start_r | ★定长 13B / 5参 | `sub_BAA0F0` | result frame_count AI_ent_id group_id reason |
| S→C | `0x9105` | entity_msma_dead | ★定长 28B / 10参 | `sub_BA95F0` | ent_id_dead world_id_kill pilot_id_kill decal_kill weapon_itemid repair_wait_sec kill_streak_count spbits is_resurrect is_extend_style_change_limit |
| S→C | `0x9A22` | eqparts_ready_cancel_r | ★定长 12B / 4参 | `sub_BAA120` | result frame_count AI_ent_id group_id |
| S→C | `0xA8FB` | eqparts_ready_counter_notice | ★定长 14B / 4参 | `sub_BAA0B0` | result ent_id count maxcount |
| S→C | `0xB334` | active_weapon_change_r | ★定长 12B / 5参 | `sub_BA9A70` | ent_id result equip_index equip_itemid is_force |
| S→C | `0xBAE4` | entity_snapshot_splitdelta_compress | 待人工（alloc=0x750C, sum=13） / 4参 | `sub_BA9990` | frame_count remain_msec zbuff[] |
| C→S | `0xC166` | eqparts_ready_start | - | `sub_B3C290`(发送) | frame_count AI_ent_id group_id reason |
| S→C | `0xC327` | pos_warp_force | ★定长 12B / 6参 | `sub_BA9A20` | ent_id pos_x pos_y pos_z dir reason |
| S→C | `0xCE08` | eqparts_toggle | ★定长 9B / 4参 | `sub_BAA0D0` | ent_id group_id toggle reason |
| C→S | `0xDDB7` | eqparts_ready_cancel | - | `sub_B3C510`(发送) | frame_count AI_ent_id group_id |
| C→S | `0xEA5A` | active_weapon_change | - | `sub_B360B0`(发送) | frame_count equip_index AI_ent_id |

### S5 开火/弹道（44 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x03CC` | weapon_fire__air_bomb_r | ★定长 18B / 8参 | `sub_BA9CD0` | ent_id itemid airbomb_id target_x target_y target_z shot0_drop1_impact2 fx_opt |
| S→C | `0x049D` | wrestle_chase_move_start_r | ★定长 20B / 8参 | `sub_BAACA0` | ent_id itemid dir_h wrestle_id target_ent_id target_pos_x target_pos_y target_pos_z |
| C→S | `0x05CA` | wrestle_chase_move_start | - | `sub_B40B50`(发送) | frame_count dir_h wrestle_id chase_time_msec target_ent_id target_pos_x target_pos_y target_pos_z AI_ent_id |
| C→S | `0x11A9` | weapon_fire__shot_single_special | - | `sub_B36C80`(发送) | frame_count itemid AI_ent_id |
| S→C | `0x1A13` | weapon_fire__hand_throw_r | ★定长 29B / 14参 | `sub_BA9BB0` | ent_id itemid grenade_id launch_x launch_y launch_z target_x target_y target_z target_ent_id msec shot0_impact1 fx_opt charge_lv |
| C→S | `0x2ADC` | weapon_fire__wrestle | - | `sub_B36EC0`(发送) | frame_count dir_h dir_v msec wrestle_id charge_lv AI_ent_id action chase_ent_id is_dp_damage_cut |
| C→S | `0x36AC` | weapon_fire__for_myself | - | `sub_B3A1F0`(发送) | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all begin1_end0 AI_ent_id |
| S→C | `0x377D` | bullet_supply | ★定长 4B / 2参 | `sub_BAA3D0` | percent_val equip_idx |
| S→C | `0x37C1` | weapon_fire__for_myself_r | ★定长 11B / 5参 | `sub_BA9DE0` | ent_id target_x target_y target_z begin1_end0 |
| C→S | `0x3AF6` | weapon_fire__hand_throw_bound | - | `sub_B37F60`(发送) | frame_count grenade_id hit_x hit_y hit_z vec_x vec_y vec_z vec_power AI_ent_id |
| S→C | `0x4E9F` | weapon_fire__shot_single_special_r | ★定长 6B / 2参 | `sub_BA9AC0` | ent_id itemid |
| S→C | `0x5F32` | bullet_supply_per_weapon_slot | 待人工（alloc=0xC, sum=8） / 3参 | `sub_BAA3F0` | supplyer_end_id supply_amount_per_weapon_slot[] |
| C→S | `0x6007` | wrestle_chase_move_end | - | `sub_B40F20`(发送) | frame_count AI_ent_id |
| S→C | `0x6D20` | weapon_fire__deploy_arms_r | ★定长 28B / 11参 | `sub_BA9C80` | ent_id itemid arms_id target_x target_y target_z target_ent_id state fx_opt judge_worldid judge_pilotid |
| S→C | `0x731C` | weapon_fire__start_homing_r | ★定长 12B / 5参 | `sub_BA9C50` | grenade_id pos_x pos_y pos_z target_ent_id |
| S→C | `0x747B` | weapon_fire__chain_mine | ★定长 12B / 4参 | `sub_BA9E10` | from_ent_id to_ent_id weapon_itemid fire_id |
| C→S | `0x7C0C` | weapon_fire__hand_throw | - | `sub_B379F0`(发送) | frame_count launch_x launch_y launch_z target_x target_y target_z target_ent_id msec shot0_impact1 fx_opt impact_grenade_id charge_lv AI_ent_id salvo_slot |
| C→S | `0x7CA0` | weapon_fire__shot_single | - | `sub_B364E0`(发送) | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all charge_lv AI_ent_id salvo_slot |
| S→C | `0x84A5` | weapon_fire__wrestle_counter_r | ★定长 8B / 3参 | `sub_BA9B20` | ent_id itemid target_ent_id |
| C→S | `0x8898` | weapon_fire__damage_field | - | `sub_B3AD30`(发送) | frame_count launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt impact_grenade_id parent_grenade_id charge_lv AI_ent_id |
| S→C | `0x894B` | weapon_fire__destruct | ★定长 6B / 2参 | `sub_BA9DC0` | ent_id weapon_itemid |
| C→S | `0xA0EA` | weapon_fire__bit_reflect | - | `sub_B3B350`(发送) | frame_count itemid launch_x launch_y launch_z target_x target_y target_z charge_lv AI_ent_id reflect_ent_id |
| C→S | `0xA404` | weapon_fire__shot_rapid | - | `sub_B368B0`(发送) | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all begin1_end0 AI_ent_id salvo_slot |
| C→S | `0xA4C9` | weapon_fire__bit | - | `sub_B39420`(发送) | frame_count shot_bit_id shot_ent_id shot_alive launch_x launch_y launch_z target_x target_y target_z target_ent_id msec release0_shot1 fx_opt AI_ent_id |
| S→C | `0xA78D` | weapon_fire__funnel_r | 待人工（alloc=0x51, sum=9） / 4参 | `sub_BA9E30` | from_ent_id wslot_idx fire_points[] |
| C→S | `0xA8FE` | weapon_fire_prepare__destruct_r | - | `sub_B39990`(发送) | frame_count weapon_itemid fire_id ent_ids[] hit_pos_x[] hit_pos_y[] hit_pos_z[] hit_dirs[] hit_distance[] body_regions[] AI_ent_id |
| S→C | `0xA9E7` | weapon_fire__damage_field_r | ★定长 39B / 18参 | `sub_BA9E70` | ent_id itemid grenade_id parent_id launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt charge_lv |
| S→C | `0xB40C` | weapon_fire__grenade_r | ★定长 41B / 20参 | `sub_BA9B40` | ent_id itemid grenade_id parent_id launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt charge_lv impact_wall action |
| S→C | `0xB491` | weapon_fire__snipe_beam_r | ★定长 11B / 5参 | `sub_BA9D10` | ent_id target_x target_y target_z begin1_end0 |
| C→S | `0xBEE3` | weapon_fire__start_homing | - | `sub_B38370`(发送) | frame_count grenade_id pos_x pos_y pos_z target_ent_id |
| C→S | `0xBFA9` | weapon_fire__deploy_arms | - | `sub_B38670`(发送) | frame_count target_x target_y target_z target_ent_id state fx_opt impact_arms_id AI_ent_id is_gmk index |
| C→S | `0xC3BD` | weapon_fire__snipe_beam | - | `sub_B39090`(发送) | frame_count target_x target_y target_z rcnt_bullet_mgz rcnt_bullet_all begin1_end0 AI_ent_id |
| C→S | `0xC84F` | bullet_supply_r | - | `sub_B3D8D0`(发送) | percent_val equip_idx |
| C→S | `0xC90D` | weapon_fire__air_bomb | - | `sub_B38AC0`(发送) | frame_count target_x target_y target_z shot0_drop1_impact2 fx_opt airbomb_id AI_ent_id |
| S→C | `0xCF40` | weapon_fire__hand_throw_bound_r | ★定长 18B / 8参 | `sub_BA9C10` | grenade_id hit_x hit_y hit_z vec_x vec_y vec_z vec_power |
| C→S | `0xD2C3` | weapon_fire__grenade | - | `sub_B372D0`(发送) | frame_count launch_x launch_y launch_z target1_x target1_y target1_z target2_x target2_y target2_z target_ent_id msec shot0_impact1 fx_opt impact_grenade_id parent_grenade_id charge_lv ent_id AI_ent_id impact_wall salvo_slot action |
| S→C | `0xD725` | weapon_fire__wrestle_r | ★定长 21B / 10参 | `sub_BA9AE0` | ent_id itemid dir_h dir_v msec wrestle_id charge_lv action chase_ent_id is_dp_damage_cut |
| C→S | `0xE1C1` | weapon_fire__air_bomb_intercepted | - | `sub_B38E50`(发送) | ent_id airbomb_id arms_id |
| C→S | `0xE314` | weapon_fire__camera | - | `sub_B3A580`(发送) | frame_count ent_ids[] AI_ent_id |
| S→C | `0xE378` | weapon_fire__bit_r | ★定长 29B / 14参 | `sub_BA9D40` | ent_id itemid bit_id shot_alive launch_x launch_y launch_z target_x target_y target_z target_ent_id msec release0_shot1 fx_opt |
| S→C | `0xEAEA` | weapon_fire_prepare__destruct | ★定长 10B / 3参 | `sub_BA9DA0` | ent_id weapon_itemid fire_id |
| S→C | `0xED22` | wrestle_chase_move_end_r | ★定长 2B / 1参 | `sub_BAACE0` | ent_id |
| S→C | `0xEDFC` | weapon_fire__bit_reflect_r | ★定长 21B / 10参 | `sub_BA9EE0` | ent_id itemid launch_x launch_y launch_z target_x target_y target_z charge_lv reflect_ent_id |
| C→S | `0xFBC1` | weapon_fire__funnel | - | `sub_B3A860`(发送) | from_ent_id wslot_idx fire_points[] |

### S6 命中/伤害/死亡（17 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x45FC` | weapon_hit_from_with_staggery | ★定长 16B / 6参 | `sub_BAA040` | ent_id hit_dir spbits optbits staggery_power staggery_msec |
| S→C | `0x49C6` | weapon_hit_from | ★定长 43B / 15参 | `sub_BA9F80` | ent_id from_ent_id weapon_itemid charge_lv hp_now hp_max damage spbits hit_pos_x hit_pos_y hit_pos_z hit_dir body_region optbits shield_hp_now |
| S→C | `0x645D` | module_val_update | ★定长 6B / 3参 | `sub_BAABE0` | ent_id val val2 |
| C→S | `0x770D` | weapon_hit_to | - | `sub_B3B7A0`(发送) | phash frame_count weapon_itemid fire_id ent_ids[] hit_pos_x[] hit_pos_y[] hit_pos_z[] hit_dirs[] hit_distance[] body_distance[] body_regions[] charge_lv AI_ent_id instate_from_ent_id create_frame_count is_down_range is_wrestle_first_high_lockon |
| S→C | `0x8D3C` | weapon_hit_chain_mine | ★定长 14B / 6参 | `sub_BA9F50` | weapon_itemid to_ent_id from_ent_id hit_pos_x hit_pos_y hit_pos_z |
| S→C | `0x8EFD` | weapon_hit_from_with_module | ★定长 7B / 3参 | `sub_BAA070` | ent_id module_hp is_force |
| S→C | `0xA8F2` | weapon_hit_from_with_tumble | ★定长 16B / 6参 | `sub_BA9FE0` | ent_id hit_dir spbits optbits down_power down_msec |
| S→C | `0xB572` | repair_pack_supply | ★定长 6B / 2参 | `sub_BAA410` | val equip_idx |
| C→S | `0xD2AE` | repair_pack_supply_r | - | `sub_B3DAC0`(发送) | val equip_idx |
| S→C | `0xD8B9` | module_toggle_time | ★定长 8B / 3参 | `sub_BAAC20` | ent_id msec rate |
| S→C | `0xDDE9` | module_toggle_level | ★定长 10B / 3参 | `sub_BAAC40` | ent_id level_up_flag next_level_max |
| S→C | `0xDDF7` | weapon_hit_to_r | ★定长 16B / 6参 | `sub_BA9F20` | weapon_itemid ent_id optbit hit_pos_x hit_pos_y hit_pos_z |
| S→C | `0xE031` | repair_gauge_update | ★定长 4B / 2参 | `sub_BAA210` | gauge_old gauge_now |
| S→C | `0xE2DE` | module_toggle_point | ★定长 6B / 3参 | `sub_BAAC00` | ent_id point point_max |
| S→C | `0xE332` | weapon_hit_from_with_stumble | ★定长 16B / 6参 | `sub_BAA010` | ent_id hit_dir spbits optbits stumble_power stumble_msec |
| S→C | `0xE96B` | repair_waittime_update | ★定长 2B / 1参 | `sub_BAA230` | repair_wait_sec |
| S→C | `0xF4D7` | shield_any_damage | ★定长 6B / 2参 | `sub_BAAC60` | ent_id damage |

### S7 得分/进度（12 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x0BCE` | score_update_coopwave | ★定长 22B / 7参 | `sub_BAA1B0` | reason world_id pilot_id point_gain point_total n_cont_kill bonus_cont_kill |
| S→C | `0x2D27` | area_over_penalty_countdown | ★定长 10B / 3参 | `sub_BAACF0` | ent_id limit_msec elapsed_msec |
| S→C | `0x3C70` | mission_safety_area_return_to_area | ★定长 2B / 1参 | `sub_BAAD10` | ent_id |
| S→C | `0x47C2` | conquer_spoint_change | ★定长 4B / 1参 | `sub_BAAA30` | conquer |
| S→C | `0x844B` | kill_count_update | ★定长 23B / 7参 | `sub_BAA140` | reason ent_id_dead world_id_kill pilot_id_kill kill_streak weapon_itemid is_extend_style_change_limit |
| S→C | `0x8D59` | score_update | ★定长 28B / 8参 | `sub_BAA170` | reason point_gain point_total is_taskforce_aux point_atk point_spt point_con kill_streak_chain_num |
| S→C | `0xA63E` | mission_clear_countdown_start | ★定长 8B / 2参 | `sub_BAAA40` | remain_msec clear_remain_msec |
| S→C | `0xA716` | mission_clear_countdown_cancel | ★定长 4B / 1参 | `sub_BAAA60` | remain_msec |
| S→C | `0xB313` | system_message | 待人工（alloc=0xB9, sum=4） / None参 | `sub_BAAED0` | msg color |
| S→C | `0xEAB3` | mission_goal_text | 待人工（alloc=0x61, sum=0） / None参 | `sub_BAAED0` | text |
| S→C | `0xEB53` | battle_contribute_rank | ★定长 4B / 1参 | `sub_BAA200` | rank |
| S→C | `0xF88B` | mission_safety_area_over_penalty | ★定长 2B / 1参 | `sub_BAAD20` | ent_id |

### S8 指挥官/战术（40 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x02D8` | combat_operation_container_collect_r | ★定长 6B / 2参 | `sub_BAA7B0` | ent_id result |
| S→C | `0x0C5F` | commander_candidacy_start | ★定长 2B / 1参 | `sub_BAA4D0` | remain_sec |
| S→C | `0x0E85` | commander_list_get_r | 待人工（alloc=0x18, sum=12） / 3参 | `sub_BAA480` | result commander_id[] |
| S→C | `0x1BB4` | commander_support_countdown | ★定长 17B / 9参 | `sub_BAA690` | ent_id support_type team troops target_x target_y target_z count is_hit_send |
| C→S | `0x1E04` | commander_subcmdr_candidacy_inbattle | - | `sub_B3EE70`(发送) | - |
| S→C | `0x214C` | commander_support_rendition_end | ★定长 7B / 4参 | `sub_BAA660` | team troops support_type spt_spot_index |
| S→C | `0x26E9` | commander_select_tell | ★定长 6B / 3参 | `sub_BAA4B0` | team troops commander_id |
| S→C | `0x3E07` | commander_subcmdr_candidacy_end | 待人工（alloc=0xEF, sum=0） / None参 | `sub_BAAED0` | - |
| S→C | `0x483F` | dynamic_taskforce_order_result | ★定长 11B / 5参 | `sub_BAA840` | result order_index order_number order_kind order_param |
| S→C | `0x501D` | commander_support_debug_cooltime_end | 待人工（alloc=0xEA, sum=0） / None参 | `sub_BAAED0` | - |
| S→C | `0x5092` | commander_support_spot_notice | 待人工（alloc=0x784, sum=4） / 2参 | `sub_BAA530` | support_spots[] |
| S→C | `0x54C6` | dynamic_taskforce_info_update | 待人工（alloc=0x1AB, sum=26） / 10参 | `sub_BAA800` | order_all_number[] order_all_kind[] order_all_param[] members_order_idx[] npc_entid[] npc_order_index[] party_worldid party_pilotid |
| S→C | `0x553F` | commander_support_gauge_update | ★定长 5B / 2参 | `sub_BAA570` | gauge_val no_complement |
| S→C | `0x56CF` | commander_support_hit_from | ★定长 20B / 6参 | `nullsub_42` | support_type ent_id hp_now hp_max spbits hit_dir |
| S→C | `0x58FC` | commander_order_assist_r | ★定长 1B / 1参 | `sub_BAA520` | type |
| S→C | `0x6295` | combat_operation_start | ★定长 24B / 9参 | `sub_BAA750` | team troops support_type remain_msec target_x target_y target_z use_worldid use_pilotid |
| C→S | `0x6486` | commander_support_execute | - | `sub_B3E580`(发送) | support_type target_x target_y target_z spt_spot_index val |
| C→S | `0x6636` | commander_order_assist | - | `sub_B3E3D0`(发送) | type |
| C→S | `0x692B` | dynamic_taskforce_order_issue | - | `sub_B3F3F0`(发送) | order_kind order_param select_members[] select_npcs[] |
| C→S | `0x6C48` | commander_candidacy_inbattle | - | `sub_B3E050`(发送) | - |
| S→C | `0x6D4B` | commander_subcmdr_notice | 待人工（alloc=0x1A0, sum=16） / 4参 | `sub_BAA730` | worldids[] pilotids[] |
| S→C | `0x6D8F` | commander_support_debug_end | ★定长 11B / 6参 | `sub_BAA630` | team troops support_type ent_id spt_ms_index spt_spot_index |
| C→S | `0x6FA1` | combat_operation_container_collect | - | `sub_B3F000`(发送) | destination |
| S→C | `0x7CD8` | commander_support_end | ★定长 11B / 6参 | `sub_BAA600` | team troops support_type ent_id spt_ms_index spt_spot_index |
| S→C | `0x80E8` | commander_support_cooltime_notice | ★定长 12B / 3参 | `sub_BAA6D0` | support_type remain_msec target_change_msec |
| S→C | `0x8D1F` | commander_support_spot_lock | ★定长 2B / 2参 | `sub_BAA550` | index is_lock |
| S→C | `0x8FFA` | commander_support_tell | ★定长 39B / 16参 | `sub_BAA5A0` | team troops support_type ent_id target_x target_y target_z spt_ms_index spt_spot_index spt_spot_dir remain_cnt remain_msec use_worldid use_pilotid setter_ms val |
| S→C | `0xAA98` | combat_operation_end | ★定长 9B / 3参 | `sub_BAA790` | support_type is_completed stg_arms_initiation_ms |
| S→C | `0xAB9B` | combat_operation_target_change_r | ★定长 18B / 6参 | `sub_BAA7D0` | result target_x target_y target_z use_worldid use_pilotid |
| S→C | `0xACB0` | commander_get_pilotinfo_r | ★定长 7B / 4参 | `sub_BAA500` | target_member target_ace kill_cnt death_cnt |
| S→C | `0xBC13` | commander_select_r | ★定长 4B / 1参 | `sub_BAA4A0` | result |
| C→S | `0xBCA5` | dynamic_taskforce_order_change_party | - | `sub_B3F780`(发送) | order_kind order_param |
| C→S | `0xBCB4` | commander_support_hit_to | - | `sub_B3E890`(发送) | ent_id hit_team hit_troops support_type ent_ids[] hit_dirs[] |
| C→S | `0xCAAF` | commander_get_pilotinfo | - | `sub_B3E1E0`(发送) | target_member target_ace |
| S→C | `0xD691` | commander_subcmdr_candidacy_start | ★定长 2B / 1参 | `sub_BAA710` | remain_sec |
| C→S | `0xDAE0` | commander_list_get | - | `sub_B3DCB0`(发送) | team troops |
| S→C | `0xDC00` | commander_support_execute_r | ★定长 4B / 1参 | `sub_BAA590` | result |
| S→C | `0xE12A` | commander_candidacy_end | ★定长 12B / 3参 | `sub_BAA4E0` | result cmdr_world_id cmdr_pilot_id |
| C→S | `0xE742` | combat_operation_target_change | - | `sub_B3F1B0`(发送) | target_x target_y target_z |
| C→S | `0xF79B` | commander_select | - | `sub_B3DEA0`(发送) | commander_id |

### S9 NPC AI 托管（18 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| C→S | `0x045B` | msma_AI_ping | - | `sub_B3CCB0`(发送) | AI_ent_id |
| S→C | `0x1165` | msma_AI_uninstall | ★定长 2B / 1参 | `sub_BAA270` | AI_ent_id |
| S→C | `0x3638` | msma_AI_move_stuckescape_r | ★定长 10B / 5参 | `sub_BAA380` | AI_ent_id to_x to_y to_z msec |
| S→C | `0x39B3` | msma_AI_update_move_end | ★定长 8B / 4参 | `sub_BAA2E0` | AI_ent_id end_x end_y end_z |
| C→S | `0x434C` | msma_AI_move_stuckescape | - | `sub_B3D600`(发送) | AI_ent_id to_x to_y to_z msec |
| S→C | `0x4FCE` | msma_AI_move_stuckescape_end | ★定长 2B / 1参 | `sub_BADBF0` | AI_ent_id |
| S→C | `0x5080` | msma_AI_suspend | ★定长 2B / 1参 | `sub_BAA290` | AI_ent_id |
| C→S | `0x5456` | msma_AI_set_stat | - | `sub_B3CE60`(发送) | AI_ent_id idx[] num[] |
| S→C | `0x54DD` | msma_AI_set_fire_area | ★定长 20B / 10参 | `sub_BAA300` | AI_ent_id fire_sx fire_sy fire_sz fire_ex fire_ey fire_ez end_x end_y end_z |
| C→S | `0x6BCD` | msma_AI_hate_control | - | `sub_B3D210`(发送) | AI_ent_id target_ent_id hate_adjust |
| S→C | `0x7CE0` | msma_AI_update_order | ★定长 7B / 3参 | `sub_BAA340` | AI_ent_id kind param |
| S→C | `0x9C14` | msma_AI_update_hate | 待人工（alloc=0x32, sum=14） / 5参 | `sub_BAA2B0` | AI_ent_id ent_id[] val[] |
| S→C | `0xA39E` | msma_AI_change_movetype | ★定长 5B / 3参 | `sub_BAA360` | AI_ent_id action_type route_number |
| S→C | `0xA7C3` | msma_AI_set_fire_point | ★定长 14B / 7参 | `nullsub_38` | AI_ent_id fire_x fire_y fire_z end_x end_y end_z |
| C→S | `0xB10A` | msma_AI_arrive_move_end | - | `sub_B3D450`(发送) | AI_ent_id |
| S→C | `0xB463` | msma_AI_install | 待人工（alloc=0xAA, sum=2） / None参 | `sub_BAAED0` | AI_ent_id AI |
| S→C | `0xB604` | msma_AI_resume | ★定长 2B / 1参 | `sub_BAA2A0` | AI_ent_id |
| S→C | `0xE228` | msma_AI_reboot | ★定长 2B / 1参 | `sub_BAA280` | AI_ent_id |

### S10 载具/道具（20 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| S→C | `0x056D` | battleship_cooltime_notice | ★定长 6B / 2参 | `sub_BAA8F0` | to_ent_id remain_msec |
| S→C | `0x1B32` | rideable_msma_ride | ★定长 26B / 8参 | `sub_BAA910` | result access_type from_world_id from_pilot_id from_ent_id to_ent_id hp_now hp_max |
| S→C | `0x1E0F` | preset_voice_down | 待人工（alloc=0xBF, sum=10） / 7参 | `sub_BA99D0` | ent_id voice_id voice_volume is_cutin is_party is_use_textmsg textmsg |
| S→C | `0x1EC7` | battleship_get_down_r | ★定长 6B / 2参 | `sub_BAA8B0` | result to_ent_id |
| C→S | `0x271F` | battleship_crash_impact | - | `sub_B3FCD0`(发送) | from_ent_id to_ent_id |
| C→S | `0x34BE` | preset_voice_up_commander | - | `sub_B34D20`(发送) | voice_id AI_ent_id |
| C→S | `0x379B` | cutin_up | **体 15B** | `sub_B34F10`(发送，通知 103) | cutin_category_id AI_ent_id to_world_id to_pilot_id to_range |
| S→C | `0x412B` | cutin_down | ★定长 6B / 2参 | `sub_BA9A00` | ent_id cutin_category_id |
| S→C | `0x4C36` | rideable_msma_get_down_r | ★定长 26B / 8参 | `sub_BAA950` | result access_type from_ent_id to_world_id to_pilot_id to_ent_id hp_now hp_max |
| S→C | `0x5B98` | battleship_limittime_notice | ★定长 6B / 2参 | `sub_BAA8D0` | to_ent_id limit_msec |
| S→C | `0x7C83` | map_event_fog_change | ★定长 19B / 7参 | `sub_BAAB10` | nearz farz color_r color_g color_b time elapsed_time |
| S→C | `0x7D22` | chara_effect | ★定长 5B / 3参 | `sub_BAAC80` | ent_id effect_id is_start |
| C→S | `0x9F0D` | preset_voice_up | - | `sub_B34930`(发送) | voice_id AI_ent_id to_world_id to_pilot_id is_party is_use_textmsg textmsg is_cutin is_voice |
| C→S | `0xB015` | rideable_msma_get_down | - | `sub_B3FEC0`(发送) | reason |
| C→S | `0xBA58` | battleship_ride | - | `sub_B3F970`(发送) | to_ent_id |
| S→C | `0xE014` | battleship_ride_r | ★定长 32B / 9参 | `sub_BAA870` | result from_world_id from_pilot_id from_ent_id to_ent_id hp_now hp_max shield_hp_now shield_hp_max |
| S→C | `0xE861` | itembox_alarm | ★定长 2B / 1参 | `sub_BAA470` | ent_id |
| S→C | `0xEE73` | map_event_linkfx_change | 待人工（alloc=0x41, sum=0） / 1参 | `sub_BAAB40` | path |
| C→S | `0xF4B9` | battleship_get_down | - | `sub_B3FB20`(发送) | reason |
| S→C | `0xF77B` | itembox_open | ★定长 10B / 3参 | `sub_BAA450` | itembox_ent_id itemid trap_weaponid |

### S11 其它（31 条）

| 方向 | ID | 报文 | 体长/参数 | 处理者 | 字段 |
|---|---|---|---|---|---|
| C→S | `0x03F7` | ban_transform | - | `sub_B40960`(发送) | ent_id val |
| C→S | `0x085F` | check_progress_quest | - | `sub_B40390`(发送) | - |
| C→S | `0x1C33` | save_message | - | `sub_B40770`(发送) | msg |
| S→C | `0x26F8` | xwar_commander_subcmdr_lot_r | ★定长 1B / 1参 | `sub_BAA700` | is_lot |
| S→C | `0x2B4D` | setmsparam | ★定长 12B / 3参 | `sub_BAABA0` | ent_id val type |
| C→S | `0x2DA4` | access_to | - | `sub_B35B70`(发送) | access_ent_id AI_ent_id |
| C→S | `0x421B` | pos_move | - | `sub_B351D0`(发送) | frame_count pos_x pos_y pos_z dir dir_eye target_x target_y target_z spbits spbits2 lockon_ent_id in_water_index layer_index access_ent_id1 access_ent_id2 rideon_ent_id spot_ent_id AI_ent_id operate_ent_id is_under_water hack_check[] |
| S→C | `0x5157` | access_state | ★定长 8B / 3参 | `sub_BAA430` | to_ent_id from_ent_id remain_msec |
| S→C | `0x6059` | check_progress_quest_r | 待人工（alloc=0x88, sum=0） / 1参 | `sub_BAAAC0` | check_quest |
| S→C | `0x6411` | gm_camera_change_r | ★定长 3B / 2参 | `sub_BAAB50` | type args |
| S→C | `0x6735` | deliver_oration | ★定长 8B / 2参 | `sub_BAA9D0` | voice_id elap_msec |
| S→C | `0x759C` | deliver_assault_stghold_ace_status | ★定长 17B / 9参 | `sub_BAA9F0` | team troops ent_id target_x target_y target_z spt_spot_index spt_spot_dir remain_msec |
| S→C | `0x7626` | netcafe_challenge_progress_r | 待人工（alloc=0x3C, sum=0） / None参 | `sub_BAAED0` | netcafe_challenge_info[] |
| C→S | `0x77C0` | examination_progress | - | `sub_B40070`(发送) | - |
| S→C | `0x8043` | tumble_ukemi_r | ★定长 6B / 2参 | `sub_BA9A50` | ent_id tmp |
| S→C | `0x8A10` | setwpnparam | 待人工（alloc=0xC, sum=8） / 3参 | `sub_BAABC0` | ent_id val type |
| S→C | `0x918E` | debug_message | 待人工（alloc=0xB9, sum=4） / None参 | `sub_BAAED0` | msg color |
| S→C | `0x91C9` | battle_buffitem_list | 待人工（alloc=0xE0, sum=0） / 2参 | `sub_BAAA80` | buffitem[] buffitem_ex[] |
| S→C | `0xA959` | radar_captured_notice | ★定长 2B / 1参 | `sub_BAA240` | ent_id_radar |
| S→C | `0xAC3D` | msma_change_team | ★定长 4B / 3参 | `sub_BAA3B0` | team troops ent_id |
| C→S | `0xBB6D` | xwar_commander_subcmdr_lot | - | `sub_B3ECC0`(发送) | is_lot |
| C→S | `0xCAAE` | object_put | - | `sub_B35D60`(发送) | frame_count target_x target_y target_z attach_parent_ent_id is_initiation AI_ent_id |
| C→S | `0xCFC8` | emergency_escape | - | `sub_B3C990`(发送) | - |
| S→C | `0xDC1E` | bgm_change | 待人工（alloc=0x19, sum=5） / 2参 | `sub_BAA990` | bgm_desc fade_msec reset |
| S→C | `0xE8EE` | demolition_breakthrough_result | ★定长 5B / 2参 | `sub_BAAAF0` | group_id is_succcess |
| C→S | `0xEDBC` | tumble_ukemi | - | `sub_B35980`(发送) | AI_ent_id tmp |
| C→S | `0xEDD6` | daily_record_progress | - | `sub_B40200`(发送) | - |
| C→S | `0xF51E` | emergency_self_destruct | - | `sub_B3CB20`(发送) | - |
| S→C | `0xF87E` | badge_add | ★定长 2B / 2参 | `sub_BAA1E0` | rank badge_type |
| S→C | `0xFD8A` | examination_progress_r | 待人工（alloc=0x58, sum=8） / 3参 | `sub_BAAAA0` | examination_info[] examination_playscore examination_playsec_remain_msec |
| S→C | `0xFE02` | daily_record_progress_r | 待人工（alloc=0x3C, sum=0） / None参 | `sub_BAAED0` | daily_record_info[] |

