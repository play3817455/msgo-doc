# 战服 recv 报文 · 体长线索（自动估计）

> 工具 `reverse-login-chain/tools/battle_bodylen.py`；机读 `battle_bodylen.json`。
> 判据：只有已知宽度读取器（B02DD0=4B/B02DF0=2B/B06230=1B；B41470/B413B0/B05E30=0B「取指针」）**且** 解析字节数 == 客户端解析结构体分配大小(alloc) ⇒ ★定长。
> ★**三重交叉验证**：**143** 条 ★定长中，**137 条**『按 dump 字段类型求和（i32=4/i16=2/u8=1/i64=8）』==『解析字节数』，
> 3 条含 `?` 类型字段、仅 3 条不一致（各差 3B，疑单字段宽度标注误差）⇒ **字段序 + 体长同时可信**，可直接照抄造包。
> 其余含变长串/循环/复合跳读 ⇒ 需逐条反编译（见 `_battle_case_trace.txt`）。

| ID | 报文 | 闸门 | 字段数 | alloc | 解析字节 | 判定 | 备注 |
|---|---|---|---|---|---|---|---|
| `0x0120` | entity_msma_show | 93 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x02D8` | combat_operation_container_collect_r | 244 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x03CC` | weapon_fire__air_bomb_r | 134 | 8 | 0x12 | 18 | ★定长 18B |  |
| `0x049D` | wrestle_chase_move_start_r | 299 | 8 | 0x14 | 20 | ★定长 20B |  |
| `0x056D` | battleship_cooltime_notice | 258 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x057A` | entity_deploy_arms_appear | 85 | 1 | 0x60 | 0 | 待人工（alloc=0x60, sum=0） |  |
| `0x07E9` | room_kick_vote_get_enable_pilots_r | 49 | 3 | 0x1AC | 20 | 待人工（alloc=0x1AC, sum=20） |  |
| `0x0825` | weapon_state_update | 115 | 3 | 0x6 | 6 | ★定长 6B |  |
| `0x0943` | entity_msma_disappear | 87 | 3 | 0x8 | 8 | ★定长 8B |  |
| `0x0B3E` | roomlobby_pilot_mindex_update_r | 11 | 5 | 0xE | 14 | ★定长 14B |  |
| `0x0BCE` | score_update_coopwave | 173 | 7 | 0x16 | 22 | ★定长 22B |  |
| `0x0C5F` | commander_candidacy_start | 214 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x0E85` | commander_list_get_r | 210 | 2 | 0x18 | 12 | 待人工（alloc=0x18, sum=12） |  |
| `0x0EC5` | room_kick_to | 45 | 0 | 0x2D | 0 | 待人工（alloc=0x2D, sum=0） |  |
| `0x1113` | game_script_play | 61 | 3 | 0x43 | 2 | 待人工（alloc=0x43, sum=2） | 含变长/复合: sub_B02BA0 |
| `0x1159` | game_mapgimmick_update | 66 | 1 | 0x404 | 4 | 待人工（alloc=0x404, sum=4） |  |
| `0x1165` | msma_AI_uninstall | 182 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x12EC` | room_chat_down | 40 | 9 | 0xDB | 13 | 待人工（alloc=0xDB, sum=13） | 含变长/复合: sub_B02BA0 |
| `0x130A` | entity_msma_hide | 92 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x1365` | game_begin | 50 | 20 | 0x2806 | 66 | 待人工（alloc=0x2806, sum=66） | 含变长/复合: sub_B05ED0,sub_B077B0,sub_B07880,sub_B418C0 |
| `0x14C5` | roomlobby_exit_r | 23 | 0 | 0x17 | 0 | 待人工（alloc=0x17, sum=0） |  |
| `0x16AA` | eqparts_execute | 163 | 2 | 0x2086 | 6 | 待人工（alloc=0x2086, sum=6） |  |
| `0x1A13` | weapon_fire__hand_throw_r | 126 | 14 | 0x1D | 29 | ★定长 29B |  |
| `0x1B32` | rideable_msma_ride | 259 | 8 | 0x1A | 26 | ★定长 26B |  |
| `0x1B67` | funnel_snapshot_all | 150 | 1 | 0x4E4 | 4 | 待人工（alloc=0x4E4, sum=4） |  |
| `0x1BB4` | commander_support_countdown | 230 | 9 | 0x11 | 17 | ★定长 17B |  |
| `0x1E0F` | preset_voice_down | 101 | 7 | 0xBF | 10 | 待人工（alloc=0xBF, sum=10） | 含变长/复合: sub_B02BA0 |
| `0x1E2F` | msma_spawn_list_get_r_one | 72 | 2 | 0x10C | 4 | 待人工（alloc=0x10C, sum=4） |  |
| `0x1EA5` | entity_msma_reborn | 89 | 2 | 0x4 | 4 | ★定长 4B |  |
| `0x1EC7` | battleship_get_down_r | 255 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x1ED8` | roomlobby_ban_vote_cancel_r | 27 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x214C` | commander_support_rendition_end | 229 | 4 | 0x7 | 7 | ★定长 7B |  |
| `0x243B` | game_btlfield_change | 51 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x26E9` | commander_select_tell | 213 | 3 | 0x6 | 6 | ★定长 6B |  |
| `0x26F8` | xwar_commander_subcmdr_lot_r | 236 | 1 | 0x1 | 1 | ★定长 1B |  |
| `0x27F3` | room_kick_vote_r | 47 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x2B4D` | setmsparam | 289 | 3 | 0xC | 12 | ★定长 12B |  |
| `0x2C60` | cpf_authenticate_error | 285 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x2D27` | area_over_penalty_countdown | 302 | 3 | 0xA | 10 | ★定长 10B |  |
| `0x30A9` | roomlobby_ban_vote_result | 32 | 4 | 0x30 | 16 | 待人工（alloc=0x30, sum=16） |  |
| `0x315C` | roomlobby_xwar_commander_lot_r | 15 | 3 | 0x7 | 7 | ★定长 7B |  |
| `0x3298` | msma_spawn_force_warp_start | 80 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x339C` | roomlobby_game_ready_r | 19 | 4 | 0x10 | 16 | ★定长 16B |  |
| `0x3638` | msma_AI_move_stuckescape_r | 198 | 5 | 0xA | 10 | ★定长 10B |  |
| `0x377D` | bullet_supply | 201 | 2 | 0x4 | 4 | ★定长 4B |  |
| `0x37C1` | weapon_fire__for_myself_r | 144 | 5 | 0xB | 11 | ★定长 11B |  |
| `0x39B3` | msma_AI_update_move_end | 191 | 4 | 0x8 | 8 | ★定长 8B |  |
| `0x3BBE` | room_chat_editing_r | 42 | 3 | 0x9 | 9 | ★定长 9B |  |
| `0x3C70` | mission_safety_area_return_to_area | 303 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x3E07` | commander_subcmdr_candidacy_end | 239 | 0 | 0xEF | 0 | 待人工（alloc=0xEF, sum=0） |  |
| `0x3E23` | game_mission_progress_update | 64 | 1 | 0x40 | 0 | 待人工（alloc=0x40, sum=0） | 含变长/复合: sub_B05ED0,sub_B07880 |
| `0x412B` | cutin_down | 104 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x45FC` | weapon_hit_from_with_staggery | 161 | 6 | 0x10 | 16 | ★定长 16B |  |
| `0x47C2` | conquer_spoint_change | 265 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x483F` | dynamic_taskforce_order_result | 251 | 5 | 0xB | 11 | ★定长 11B |  |
| `0x49C6` | weapon_hit_from | 158 | 15 | 0x2B | 43 | ★定长 43B |  |
| `0x4C36` | rideable_msma_get_down_r | 261 | 8 | 0x1A | 26 | ★定长 26B |  |
| `0x4C7D` | entity_msma_unattended_state | 96 | 2 | 0x4 | 4 | ★定长 4B |  |
| `0x4D96` | game_client_signal_r | 60 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x4E9F` | weapon_fire__shot_single_special_r | 119 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x4FCE` | msma_AI_move_stuckescape_end | 199 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x501D` | commander_support_debug_cooltime_end | 234 | 0 | 0xEA | 0 | 待人工（alloc=0xEA, sum=0） |  |
| `0x5080` | msma_AI_suspend | 184 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x5092` | commander_support_spot_notice | 221 | 1 | 0x784 | 4 | 待人工（alloc=0x784, sum=4） |  |
| `0x5157` | access_state | 206 | 3 | 0x8 | 8 | ★定长 8B |  |
| `0x54C6` | dynamic_taskforce_info_update | 247 | 8 | 0x1AB | 26 | 待人工（alloc=0x1AB, sum=26） | 含变长/复合: sub_B05EA0 |
| `0x54DD` | msma_AI_set_fire_area | 194 | 10 | 0x14 | 20 | ★定长 20B |  |
| `0x553F` | commander_support_gauge_update | 223 | 2 | 0x5 | 5 | ★定长 5B |  |
| `0x568A` | entity_snapshot | 97 | 3 | 0x8F0C | 12 | 待人工（alloc=0x8F0C, sum=12） |  |
| `0x56CF` | commander_support_hit_from | 232 | 6 | 0x14 | 20 | ★定长 20B |  |
| `0x58FC` | commander_order_assist_r | 220 | 1 | 0x1 | 1 | ★定长 1B |  |
| `0x5913` | roomlobby_roommaster_notice | 12 | 2 | 0x8 | 8 | ★定长 8B |  |
| `0x5B98` | battleship_limittime_notice | 257 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x5C4F` | entity_msma_detach | 91 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0x5D2A` | roomlobby_clan_notice | 16 | 7 | 0x28 | 9 | 待人工（alloc=0x28, sum=9） | 含变长/复合: sub_B02BA0 |
| `0x5EEA` | entity_snapshot_splitdelta | 98 | 33 | 0x9FC4 | 167 | 待人工（alloc=0x9FC4, sum=167） | 含变长/复合: sub_B05EA0 |
| `0x5F32` | bullet_supply_per_weapon_slot | 203 | 2 | 0xC | 8 | 待人工（alloc=0xC, sum=8） |  |
| `0x6059` | check_progress_quest_r | 277 | 1 | 0x88 | 0 | 待人工（alloc=0x88, sum=0） |  |
| `0x611B` | game_script_play_also_replay | 62 | 2 | 0x42 | 1 | 待人工（alloc=0x42, sum=1） | 含变长/复合: sub_B02BA0 |
| `0x6295` | combat_operation_start | 241 | 9 | 0x18 | 24 | ★定长 24B |  |
| `0x640D` | msma_spawn_info_prestart | 77 | 5 | 0x179 | 27 | 待人工（alloc=0x179, sum=27） | 含变长/复合: sub_B05EA0 |
| `0x6411` | gm_camera_change_r | 282 | 2 | 0x3 | 3 | ★定长 3B |  |
| `0x645D` | module_val_update | 292 | 3 | 0x6 | 6 | ★定长 6B |  |
| `0x6475` | game_coopwave_result | 53 | 1 | 0x2C | 0 | 待人工（alloc=0x2C, sum=0） |  |
| `0x6735` | deliver_oration | 263 | 2 | 0x8 | 8 | ★定长 8B |  |
| `0x6A0F` | roomlobby_vote_get_comeback | 38 | 2 | 0x14 | 8 | 待人工（alloc=0x14, sum=8） |  |
| `0x6A38` | roomlobby_pilot_level_update | 9 | 4 | 0xC | 12 | ★定长 12B |  |
| `0x6A8D` | roomlobby_xwar_countdown | 13 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x6B2C` | roomlobby_cupteam_notice | 17 | 4 | 0xD | 13 | ★定长 13B |  |
| `0x6B71` | roomlobby_vote_state | 37 | 2 | 0x8 | 8 | ★定长 8B |  |
| `0x6D20` | weapon_fire__deploy_arms_r | 132 | 11 | 0x1C | 28 | ★定长 28B |  |
| `0x6D4B` | commander_subcmdr_notice | 240 | 2 | 0x1A0 | 16 | 待人工（alloc=0x1A0, sum=16） |  |
| `0x6D8F` | commander_support_debug_end | 228 | 6 | 0xB | 11 | ★定长 11B |  |
| `0x7155` | roomlobby_pilot_add_npc | 5 | 12 | 0x5B | 18 | 待人工（alloc=0x5B, sum=18） | 含变长/复合: sub_B02BA0 |
| `0x717D` | entity_msma_appear | 84 | 14 | 0x156 | 22 | 待人工（alloc=0x156, sum=22） |  |
| `0x7206` | roomlobby_game_start_r | 21 | 5 | 0x14 | 20 | ★定长 20B |  |
| `0x731C` | weapon_fire__start_homing_r | 130 | 5 | 0xC | 12 | ★定长 12B |  |
| `0x73CE` | entity_msma_attach | 90 | 6 | 0xB | 11 | ★定长 11B |  |
| `0x747B` | weapon_fire__chain_mine | 146 | 4 | 0xC | 12 | ★定长 12B |  |
| `0x759C` | deliver_assault_stghold_ace_status | 264 | 9 | 0x11 | 17 | ★定长 17B |  |
| `0x7621` | entity_msma_appear_self | 83 | 10 | 0x154 | 20 | 待人工（alloc=0x154, sum=20） |  |
| `0x7626` | netcafe_challenge_progress_r | 275 | 1 | 0x3C | 0 | 待人工（alloc=0x3C, sum=0） |  |
| `0x7C83` | map_event_fog_change | 279 | 7 | 0x13 | 19 | ★定长 19B |  |
| `0x7CD8` | commander_support_end | 227 | 6 | 0xB | 11 | ★定长 11B |  |
| `0x7CE0` | msma_AI_update_order | 195 | 3 | 0x7 | 7 | ★定长 7B |  |
| `0x7D22` | chara_effect | 297 | 3 | 0x5 | 5 | ★定长 5B |  |
| `0x7D59` | roomlobby_pick_vote_result | 34 | 4 | 0x30 | 16 | 待人工（alloc=0x30, sum=16） |  |
| `0x8043` | tumble_ukemi_r | 108 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x80E8` | commander_support_cooltime_notice | 233 | 3 | 0xC | 12 | ★定长 12B |  |
| `0x8297` | game_resume | 57 | 0 | 0x39 | 0 | 待人工（alloc=0x39, sum=0） |  |
| `0x844B` | kill_count_update | 171 | 7 | 0x17 | 23 | ★定长 23B |  |
| `0x84A5` | weapon_fire__wrestle_counter_r | 122 | 3 | 0x8 | 8 | ★定长 8B |  |
| `0x86B2` | msma_spawn_select_r | 76 | 6 | 0x53 | 18 | 待人工（alloc=0x53, sum=18） | 含变长/复合: sub_B02BA0 |
| `0x894B` | weapon_fire__destruct | 142 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0x8A10` | setwpnparam | 290 | 3 | 0xC | 8 | 待人工（alloc=0xC, sum=8） |  |
| `0x8C24` | roomlobby_pick_vote_cancel_r | 31 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x8D1F` | commander_support_spot_lock | 222 | 2 | 0x2 | 2 | ★定长 2B |  |
| `0x8D3C` | weapon_hit_chain_mine | 157 | 6 | 0xE | 14 | ★定长 14B |  |
| `0x8D42` | game_mapeffect_update | 67 | 2 | 0x5 | 5 | ★定长 5B |  |
| `0x8D58` | eqparts_ready_start_r | 166 | 5 | 0xD | 13 | ★定长 13B |  |
| `0x8D59` | score_update | 172 | 8 | 0x1C | 28 | ★定长 28B |  |
| `0x8DE4` | msma_spawn_wait_update | 74 | 3 | 0x5 | 5 | ★定长 5B |  |
| `0x8EFD` | weapon_hit_from_with_module | 162 | 3 | 0x7 | 7 | ★定长 7B |  |
| `0x8FFA` | commander_support_tell | 226 | 16 | 0x27 | 39 | ★定长 39B |  |
| `0x9105` | entity_msma_dead | 88 | 10 | 0x1C | 28 | ★定长 28B |  |
| `0x918E` | debug_message | 287 | 2 | 0xB9 | 4 | 待人工（alloc=0xB9, sum=4） | 含变长/复合: sub_B02BA0 |
| `0x91C9` | battle_buffitem_list | 269 | 2 | 0xE0 | 0 | 待人工（alloc=0xE0, sum=0） |  |
| `0x97EC` | roomlobby_pick_vote_r | 29 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x9951` | msma_spawn_list_get_r_begin | 71 | 2 | 0x8 | 8 | ★定长 8B |  |
| `0x9A22` | eqparts_ready_cancel_r | 168 | 4 | 0xC | 12 | ★定长 12B |  |
| `0x9A39` | room_kick_master_r | 44 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0x9C14` | msma_AI_update_hate | 189 | 3 | 0x32 | 14 | 待人工（alloc=0x32, sum=14） |  |
| `0xA39E` | msma_AI_change_movetype | 196 | 3 | 0x5 | 5 | ★定长 5B |  |
| `0xA5DA` | authenticate_r | 3 | 20 | 0x2DE | 41 | 待人工（alloc=0x2DE, sum=41） | 含变长/复合: sub_B02BA0,sub_B05ED0,sub_B05EE0,sub_B077B0,sub_B07880,sub_B08160,sub_B418C0 |
| `0xA63E` | mission_clear_countdown_start | 266 | 2 | 0x8 | 8 | ★定长 8B |  |
| `0xA716` | mission_clear_countdown_cancel | 267 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0xA77E` | game_replay_result | 69 | 1 | 0x1 | 1 | ★定长 1B |  |
| `0xA78D` | weapon_fire__funnel_r | 148 | 3 | 0x51 | 9 | 待人工（alloc=0x51, sum=9） |  |
| `0xA7C3` | msma_AI_set_fire_point | 193 | 7 | 0xE | 14 | ★定长 14B |  |
| `0xA8F2` | weapon_hit_from_with_tumble | 159 | 6 | 0x10 | 16 | ★定长 16B |  |
| `0xA8FB` | eqparts_ready_counter_notice | 170 | 4 | 0xE | 14 | ★定长 14B |  |
| `0xA959` | radar_captured_notice | 180 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xA9E7` | weapon_fire__damage_field_r | 152 | 18 | 0x27 | 39 | ★定长 39B |  |
| `0xAA98` | combat_operation_end | 242 | 3 | 0x9 | 9 | ★定长 9B |  |
| `0xAB6F` | msma_spawn_list_get_r_end | 73 | 0 | 0x49 | 0 | 待人工（alloc=0x49, sum=0） |  |
| `0xAB9B` | combat_operation_target_change_r | 246 | 6 | 0x12 | 18 | ★定长 18B |  |
| `0xAC3D` | msma_change_team | 200 | 3 | 0x4 | 4 | ★定长 4B |  |
| `0xACB0` | commander_get_pilotinfo_r | 218 | 4 | 0x7 | 7 | ★定长 7B |  |
| `0xB313` | system_message | 286 | 2 | 0xB9 | 4 | 待人工（alloc=0xB9, sum=4） | 含变长/复合: sub_B02BA0 |
| `0xB334` | active_weapon_change_r | 112 | 5 | 0xC | 12 | ★定长 12B |  |
| `0xB40C` | weapon_fire__grenade_r | 124 | 20 | 0x29 | 41 | ★定长 41B |  |
| `0xB463` | msma_AI_install | 181 | 2 | 0xAA | 2 | 待人工（alloc=0xAA, sum=2） |  |
| `0xB491` | weapon_fire__snipe_beam_r | 137 | 5 | 0xB | 11 | ★定长 11B |  |
| `0xB572` | repair_pack_supply | 204 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0xB604` | msma_AI_resume | 185 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xB881` | roomlobby_ban_vote_r | 25 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0xBA73` | cpf_authenticate | 283 | 1 | 0x84 | 5 | 待人工（alloc=0x84, sum=5） | 含变长/复合: sub_B05EA0 |
| `0xBAE4` | entity_snapshot_splitdelta_compress | 99 | 3 | 0x750C | 13 | 待人工（alloc=0x750C, sum=13） | 含变长/复合: sub_B05EA0 |
| `0xBC13` | commander_select_r | 212 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0xBDC6` | game_read_ahead_route_notice | 52 | 1 | 0x104 | 8 | 待人工（alloc=0x104, sum=8） |  |
| `0xBDD6` | roomlobby_pilot_add | 4 | 11 | 0xC6 | 22 | 待人工（alloc=0xC6, sum=22） |  |
| `0xC327` | pos_warp_force | 106 | 6 | 0xC | 12 | ★定长 12B |  |
| `0xC64E` | roomlobby_pilot_del | 6 | 2 | 0x8 | 8 | ★定长 8B |  |
| `0xC66B` | game_round_end | 54 | 3 | 0x42 | 2 | 待人工（alloc=0x42, sum=2） | 含变长/复合: sub_B05ED0,sub_B07880 |
| `0xCDE6` | game_score_ranker_notice | 68 | 0 | 0x44 | 0 | 待人工（alloc=0x44, sum=0） |  |
| `0xCE08` | eqparts_toggle | 164 | 4 | 0x9 | 9 | ★定长 9B |  |
| `0xCF40` | weapon_fire__hand_throw_bound_r | 128 | 8 | 0x12 | 18 | ★定长 18B |  |
| `0xD1B3` | game_respawn_post_update | 65 | 1 | 0x7D4 | 4 | 待人工（alloc=0x7D4, sum=4） |  |
| `0xD691` | commander_subcmdr_candidacy_start | 237 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xD725` | weapon_fire__wrestle_r | 121 | 10 | 0x15 | 21 | ★定长 21B |  |
| `0xD8B9` | module_toggle_time | 294 | 3 | 0x8 | 8 | ★定长 8B |  |
| `0xD94A` | game_suspend | 56 | 0 | 0x38 | 0 | 待人工（alloc=0x38, sum=0） |  |
| `0xDC00` | commander_support_execute_r | 225 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0xDC1E` | bgm_change | 262 | 3 | 0x19 | 5 | 待人工（alloc=0x19, sum=5） |  |
| `0xDCF2` | roomlobby_pilot_msdeck | 7 | 4 | 0x24 | 21 | 待人工（alloc=0x24, sum=21） | 含变长/复合: sub_B05EA0 |
| `0xDDE9` | module_toggle_level | 295 | 3 | 0xA | 10 | ★定长 10B |  |
| `0xDDF7` | weapon_hit_to_r | 156 | 6 | 0x10 | 16 | ★定长 16B |  |
| `0xDE24` | proto_version_check_r | 1 | 3 | 0xC | 12 | ★定长 12B |  |
| `0xE014` | battleship_ride_r | 253 | 9 | 0x20 | 32 | ★定长 32B |  |
| `0xE031` | repair_gauge_update | 178 | 2 | 0x4 | 4 | ★定长 4B |  |
| `0xE12A` | commander_candidacy_end | 216 | 3 | 0xC | 12 | ★定长 12B |  |
| `0xE228` | msma_AI_reboot | 183 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xE2DE` | module_toggle_point | 293 | 3 | 0x6 | 6 | ★定长 6B |  |
| `0xE31F` | roomlobby_pilot_leave_appeal | 8 | 0 | 0x8 | 0 | 待人工（alloc=0x8, sum=0） |  |
| `0xE332` | weapon_hit_from_with_stumble | 160 | 6 | 0x10 | 16 | ★定长 16B |  |
| `0xE378` | weapon_fire__bit_r | 139 | 14 | 0x1D | 29 | ★定长 29B |  |
| `0xE4DB` | entity_msma_show_hp | 95 | 3 | 0x6C | 18 | 待人工（alloc=0x6C, sum=18） |  |
| `0xE5FC` | msma_spawn_warp_countdown_finish | 81 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xE861` | itembox_alarm | 208 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xE8EE` | demolition_breakthrough_result | 278 | 2 | 0x5 | 5 | ★定长 5B |  |
| `0xE96B` | repair_waittime_update | 179 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xEAB3` | mission_goal_text | 268 | 1 | 0x61 | 0 | 待人工（alloc=0x61, sum=0） | 含变长/复合: sub_B02BA0 |
| `0xEAEA` | weapon_fire_prepare__destruct | 140 | 3 | 0xA | 10 | ★定长 10B |  |
| `0xEB53` | battle_contribute_rank | 175 | 1 | 0x4 | 4 | ★定长 4B |  |
| `0xED22` | wrestle_chase_move_end_r | 301 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xEDFC` | weapon_fire__bit_reflect_r | 154 | 10 | 0x15 | 21 | ★定长 21B |  |
| `0xEE73` | map_event_linkfx_change | 280 | 1 | 0x41 | 0 | 待人工（alloc=0x41, sum=0） | 含变长/复合: sub_B02BA0 |
| `0xF4D7` | shield_any_damage | 296 | 2 | 0x6 | 6 | ★定长 6B |  |
| `0xF77B` | itembox_open | 207 | 3 | 0xA | 10 | ★定长 10B |  |
| `0xF87E` | badge_add | 174 | 2 | 0x2 | 2 | ★定长 2B |  |
| `0xF88B` | mission_safety_area_over_penalty | 304 | 1 | 0x2 | 2 | ★定长 2B |  |
| `0xFD8A` | examination_progress_r | 271 | 3 | 0x58 | 8 | 待人工（alloc=0x58, sum=8） |  |
| `0xFE02` | daily_record_progress_r | 273 | 1 | 0x3C | 0 | 待人工（alloc=0x3C, sum=0） |  |
| `0xFE50` | roomlobby_pick_vote_deck | 36 | 3 | 0x24 | 12 | 待人工（alloc=0x24, sum=12） |  |
| `0xFEBB` | msma_spawn_warp_start_r | 79 | 4 | 0xE | 14 | ★定长 14B |  |

## 统计

- ★定长：**143** 条（可直接造包）
- 待人工：**62** 条
- ★定长 1B → commander_order_assist_r、game_replay_result、xwar_commander_subcmdr_lot_r
- ★定长 2B → badge_add、commander_candidacy_start、commander_subcmdr_candidacy_start、commander_support_spot_lock、entity_msma_detach、entity_msma_hide、entity_msma_show、itembox_alarm、mission_safety_area_over_penalty、mission_safety_area_return_to_area、msma_AI_move_stuckescape_end、msma_AI_reboot、msma_AI_resume、msma_AI_suspend、msma_AI_uninstall、msma_spawn_warp_countdown_finish、radar_captured_notice、repair_waittime_update、wrestle_chase_move_end_r
- ★定长 3B → gm_camera_change_r
- ★定长 4B → battle_contribute_rank、bullet_supply、commander_select_r、commander_support_execute_r、conquer_spoint_change、cpf_authenticate_error、entity_msma_reborn、entity_msma_unattended_state、game_btlfield_change、game_client_signal_r、mission_clear_countdown_cancel、msma_change_team、repair_gauge_update、room_kick_master_r、room_kick_vote_r、roomlobby_ban_vote_cancel_r、roomlobby_ban_vote_r、roomlobby_pick_vote_cancel_r、roomlobby_pick_vote_r、roomlobby_xwar_countdown
- ★定长 5B → chara_effect、commander_support_gauge_update、demolition_breakthrough_result、game_mapeffect_update、msma_AI_change_movetype、msma_spawn_wait_update
- ★定长 6B → battleship_cooltime_notice、battleship_get_down_r、battleship_limittime_notice、combat_operation_container_collect_r、commander_select_tell、cutin_down、module_toggle_point、module_val_update、msma_spawn_force_warp_start、repair_pack_supply、shield_any_damage、tumble_ukemi_r、weapon_fire__destruct、weapon_fire__shot_single_special_r、weapon_state_update
- ★定长 7B → commander_get_pilotinfo_r、commander_support_rendition_end、msma_AI_update_order、roomlobby_xwar_commander_lot_r、weapon_hit_from_with_module
- ★定长 8B → access_state、deliver_oration、entity_msma_disappear、mission_clear_countdown_start、module_toggle_time、msma_AI_update_move_end、msma_spawn_list_get_r_begin、roomlobby_pilot_del、roomlobby_roommaster_notice、roomlobby_vote_state、weapon_fire__wrestle_counter_r
- ★定长 9B → combat_operation_end、eqparts_toggle、room_chat_editing_r
- ★定长 10B → area_over_penalty_countdown、itembox_open、module_toggle_level、msma_AI_move_stuckescape_r、weapon_fire_prepare__destruct
- ★定长 11B → commander_support_debug_end、commander_support_end、dynamic_taskforce_order_result、entity_msma_attach、weapon_fire__for_myself_r、weapon_fire__snipe_beam_r
- ★定长 12B → active_weapon_change_r、commander_candidacy_end、commander_support_cooltime_notice、eqparts_ready_cancel_r、pos_warp_force、proto_version_check_r、roomlobby_pilot_level_update、setmsparam、weapon_fire__chain_mine、weapon_fire__start_homing_r
- ★定长 13B → eqparts_ready_start_r、roomlobby_cupteam_notice
- ★定长 14B → eqparts_ready_counter_notice、msma_AI_set_fire_point、msma_spawn_warp_start_r、roomlobby_pilot_mindex_update_r、weapon_hit_chain_mine
- ★定长 16B → roomlobby_game_ready_r、weapon_hit_from_with_staggery、weapon_hit_from_with_stumble、weapon_hit_from_with_tumble、weapon_hit_to_r
- ★定长 17B → commander_support_countdown、deliver_assault_stghold_ace_status
- ★定长 18B → combat_operation_target_change_r、weapon_fire__air_bomb_r、weapon_fire__hand_throw_bound_r
- ★定长 19B → map_event_fog_change
- ★定长 20B → commander_support_hit_from、msma_AI_set_fire_area、roomlobby_game_start_r、wrestle_chase_move_start_r
- ★定长 21B → weapon_fire__bit_reflect_r、weapon_fire__wrestle_r
- ★定长 22B → score_update_coopwave
- ★定长 23B → kill_count_update
- ★定长 24B → combat_operation_start
- ★定长 26B → rideable_msma_get_down_r、rideable_msma_ride
- ★定长 28B → entity_msma_dead、score_update、weapon_fire__deploy_arms_r
- ★定长 29B → weapon_fire__bit_r、weapon_fire__hand_throw_r
- ★定长 32B → battleship_ride_r
- ★定长 39B → commander_support_tell、weapon_fire__damage_field_r
- ★定长 41B → weapon_fire__grenade_r
- ★定长 43B → weapon_hit_from
