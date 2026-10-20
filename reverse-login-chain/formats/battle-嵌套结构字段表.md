# 战服（battle）嵌套结构字段表 —— 由打印器自动提取

> 工具：`reverse-login-chain/tools/dump_nested_structs.py`（IDA，2026-09-15）
> 原理：客户端 dump 代码里每字段 = 读字段 + `push "xxx="` + 拼接 ⇒ xref 排序 = **线序**。
> 机读版：`battle_nested_fields.json`。`off` 为**内存槽偏移**（线序可能更紧凑，见各结构备注）。

## ★关键结构索引（本次已定名，2026-09-15）

| 打印器 | 字段数 | 槽大小 | 是什么 | 出现于 |
|---|---|---|---|---|
| `sub_B09240` | 31 | **264B** | **`ms` 出击机体**（uniqid/msma_id/crew_msma_id/decal/color/deck_index/cost/…/witem_id[3]/sitem_id/spitem_id/wbu_*[3]×7/eq_modules[10]/adop_items_ms[4]/adop_items_eq[12]/…） | `msma_spawn_list_get_r_one`(0x1E2F)、`entity_msma_appear`(0x717D)、`entity_msma_appear_self`(0x7621) |
| `sub_B0A260` | **21（+1 未打印）** | **44B** | **实体快照条目**（ent_id/pos_x/y/z/**dir**/target_x/y/z/score1-3/hp_percent(_shield)/down_power/equip_index/water_index/layer_index/rideon_ent_id/lockon_ent_id/special_bits/special_bits2）= 线序 **39B** | `entity_snapshot`(0x568A)、`entity_msma_appear` 的 `snapshot{}` |
| `sub_B0B9E0` | 29 | — | **`send_pos_move` 的 `hack_check{}`**（move_spd/boost_gauge/boost_recov/boost_consume/clcheck_result/weapon_itemid/cooltime/rapidtime/reload/debugger_found/proc_ref_count/reserved1-2/weapon_bullet_speed/range/charge_time/bullet_mgz/bullet_all…） | 上行 `pos_move`（反外挂校验，服务端可只校验不强判） |
| `sub_B0AEA0` | 21 | — | **AI/路线托管结构**（type/stat/ent_id/gauge_max/msma_id/msma_id2/pos_x/y/z/pos2_x/y/z/ctrl_count/route_number/route_initial_index/move_speed/rot_speed/door_auto_sensor_height/radius/attach_barrier_npc_ent_id/local_ctrl_id） | NPC AI 托管族 |
| `sub_B09C10` | 26 | — | 地图/任务单位（type/name/param_id/action_type/move_spd/pop_init_x/y/z…） | `game_begin` 等 |
| `sub_B0B4B0` | 17 | — | 出击/房间成员信息（team/troops/world_id/pilot_id/ent_id/index/msma_id/item_id…） | `entity_msma_appear` 等 |
| `sub_B08AD0` / `sub_B48C10` / `sub_B49580` | 24 / 58 / 20 | — | 机师(pilot)信息族（pilot_id/name/troops/level/mil_class/byword/avatar/clan_*/…） | 大厅/房间 |
| `sub_B4B240` / `sub_B4C650` / `sub_B48010` | 61 / 63 / 45 | — | 战绩/评分统计族（rec_point/kill_cnt/…、teamside/money/cmdr_fame/…、money/clan_id/deckcost…） | 结算/大厅 |

> ⚠ 数组型字段（`xxx={` / 循环内多次 push）在本表中可能只出现一次，需结合 `loop` 列与解析器宽度确认。


## `0xb51930`（227302 字节，836 字段）← 调用者: 0xeedbc0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `result` |  |
| 2 | 0x0 | u32 | `uniqid_ms` |  |
| 3 | 0x0 | u32 | `item_id` |  |
| 4 | 0x0 | u32 | `result` |  |
| 5 | 0x0 | u32 | `uniqid_ms` |  |
| 6 | 0x0 | u32 | `e_fgauge` |  |
| 7 | 0x0 | u32 | `z_fgauge` |  |
| 8 | 0x0 | u32 | `lose_troops` |  |
| 9 | 0x0 | u16 | `expup_fgauge` |  |
| 10 | 0x0 | u32 | `result` |  |
| 11 | 0x8 | u32 | `cshist_item` |  |
| 12 | 0x0 | u16 | `slot_num_main` |  |
| 13 | 0x0 | u16 | `slot_num_consume` |  |
| 14 | 0x0 | u16 | `slot_num_trash` |  |
| 15 | 0x0 | u16 | `slot_num_plan` |  |
| 16 | 0x0 | u32 | `sort_tm_sec_main` |  |
| 17 | 0x0 | u32 | `sort_tm_usec_main` |  |
| 18 | 0x0 | u32 | `sort_tm_sec_consume` |  |
| 19 | 0x0 | u32 | `sort_tm_usec_consume` |  |
| 20 | 0x0 | u32 | `sort_tm_sec_plan` |  |
| 21 | 0x0 | u32 | `sort_tm_usec_plan` |  |
| 22 | 0x0 | u32 | `msma_plan_sort_type` |  |
| 23 | 0x0 | u32 | `msma_plan_sort_order` |  |
| 24 | 0x0 | u32 | `sort_plan_sec` |  |
| 25 | 0x0 | u32 | `sort_plan_usec` |  |
| 26 | 0x0 | u32 | `term_sec` |  |
| 27 | 0x0 | u32 | `chargepoint` |  |
| 28 | 0x0 | u32 | `result` |  |
| 29 | 0x0 | u32 | `custom_id` |  |
| 30 | 0x8 | u32 | `is_open_info` |  |
| 31 | 0x0 | u32 | `result` |  |
| 32 | 0x0 | u32 | `restore_channel` |  |
| 33 | 0x0 | u32 | `charge_point` |  |
| 34 | 0x0 | u32 | `tuto_step` |  |
| 35 | 0x0 | u32 | `tuto_flags` |  |
| 36 | 0x0 | u32 | `tuto_missionid` |  |
| 37 | 0x0 | u32 | `pilot_detail` |  |
| 38 | ? | ? | `is_netcafe` |  |
| 39 | ? | ? | `is_processing_comeback` |  |
| 40 | 0x0 | u32 | `vip_lv` |  |
| 41 | 0x0 | u32 | `overplay_type` |  |
| 42 | 0x0 | u32 | `accum_playtime` |  |
| 43 | 0x0 | u32 | `daily_compcnt` |  |
| 44 | 0x0 | u32 | `ncafe_compcnt` |  |
| 45 | ? | ? | `flag_wideuse` |  |
| 46 | 0x0 | u32 | `level_point` |  |
| 47 | 0x8 | u32 | `is_recruiting` |  |
| 48 | 0x0 | u32 | `party_type` |  |
| 49 | 0x0 | u32 | `result` |  |
| 50 | 0x0 | u32 | `uniqid_ms` |  |
| 51 | 0x0 | u32 | `item_id` |  |
| 52 | 0x0 | u32 | `ticket_id` |  |
| 53 | 0x0 | u16 | `usenum` |  |
| 54 | 0x0 | u16 | `param_target` |  |
| 55 | 0x0 | u32 | `workres` |  |
| 56 | 0x0 | u16 | `buildup_cnt` |  |
| 57 | 0x0 | u16 | `up_param` |  |
| 58 | 0x0 | u32 | `mech_npcpict` |  |
| 59 | 0x0 | u32 | `money` |  |
| 60 | 0x0 | u32 | `result` |  |
| 61 | 0x0 | u32 | `reward_id` |  |
| 62 | 0x0 | u32 | `result` |  |
| 63 | 0x0 | u32 | `slot_num` |  |
| 64 | 0x0 | u32 | `result` |  |
| 65 | 0x0 | u16 | `deck_type` |  |
| 66 | 0x0 | u16 | `slot` |  |
| 67 | ? | ? | `is_perfect` |  |
| 68 | 0x0 | u16 | `year` |  |
| 69 | 0x0 | u16 | `month` |  |
| 70 | ? | ? | `clan_forbidden` |  |
| 71 | 0x0 | u32 | `result` |  |
| 72 | 0x0 | u32 | `price` |  |
| 73 | 0x0 | u32 | `uniq_msid` |  |
| 74 | 0x0 | u32 | `result` |  |
| 75 | 0x0 | u32 | `clan_kind` |  |
| 76 | 0x0 | u32 | `result` |  |
| 77 | 0x0 | u32 | `clan_id` |  |
| 78 | 0x0 | u32 | `clan_kind` |  |
| 79 | 0x0 | u32 | `deckcost` |  |
| 80 | 0x0 | u32 | `result` |  |
| 81 | 0x0 | u32 | `npc_id` |  |
| 82 | 0x0 | u32 | `result` |  |
| 83 | 0x0 | u32 | `uniqid_ms` |  |
| 84 | 0x0 | u32 | `ticket_id` |  |
| 85 | 0x0 | u16 | `usenum` |  |
| 86 | 0x0 | u32 | `workres` |  |
| 87 | 0x0 | u16 | `buildup_cnt` |  |
| 88 | 0x0 | u32 | `mech_npcpict` |  |
| 89 | 0x0 | u32 | `result` |  |
| 90 | 0x0 | u32 | `old_navi` |  |
| 91 | 0x0 | u32 | `new_navi` |  |
| 92 | 0x0 | u32 | `result` |  |
| 93 | 0x0 | u32 | `missionunit_set` |  |
| 94 | 0x0 | u32 | `mission_id` |  |
| 95 | 0x0 | u32 | `tuto_step` |  |
| 96 | 0x0 | u32 | `tuto_flags` |  |
| 97 | 0x0 | u32 | `tuto_missionid` |  |
| 98 | 0x0 | u32 | `result` |  |
| 99 | 0x0 | u32 | `order` |  |
| 100 | 0x0 | u32 | `rankself` |  |
| 101 | 0x0 | u32 | `page_now` |  |
| 102 | 0x0 | u32 | `page_max` |  |
| 103 | ? | ? | `clan_kind` |  |
| 104 | 0x0 | u32 | `is_simple` |  |
| 105 | 0x0 | u32 | `world_client_num` |  |
| 106 | 0x0 | u32 | `notify_type` |  |
| 107 | 0x0 | u32 | `data1` |  |
| 108 | 0x0 | u32 | `data2` |  |
| 109 | 0x0 | u32 | `data3` |  |
| 110 | 0x0 | u32 | `result` |  |
| 111 | 0x0 | u32 | `is_recruiting` |  |
| 112 | 0x0 | u16 | `remain_minutes` |  |
| 113 | 0x0 | u32 | `party_type` |  |
| 114 | 0x0 | u32 | `result` |  |
| 115 | 0x0 | u32 | `uniq_msid` |  |
| 116 | 0x0 | u32 | `result` |  |
| 117 | 0x0 | u32 | `module_id` |  |
| 118 | 0x0 | u32 | `result` |  |
| 119 | ? | ? | `clan_kind` |  |
| 120 | 0x0 | u32 | `result` |  |
| 121 | 0x0 | u32 | `mailid` |  |
| 122 | 0x0 | u32 | `result` |  |
| 123 | 0x0 | u32 | `uniqid_ms` |  |
| 124 | 0x0 | u16 | `eq_slot1` |  |
| 125 | 0x0 | u16 | `eq_slot2` |  |
| 126 | 0x0 | u16 | `priority` |  |
| 127 | 0x8 | u32 | `is_new` |  |
| 128 | ? | ? | `roominfo` |  |
| 129 | ? | ? | `clan_eff` |  |
| 130 | ? | ? | `clan_zeon` |  |
| 131 | 0x0 | u32 | `result` |  |
| 132 | 0x0 | u32 | `result` |  |
| 133 | 0x0 | u32 | `result` |  |
| 134 | 0x0 | u32 | `result` |  |
| 135 | 0x0 | u32 | `pilot_id` |  |
| 136 | 0x0 | u32 | `is_kick` |  |
| 137 | 0x0 | u32 | `result` |  |
| 138 | 0x0 | u32 | `custom_id` |  |
| 139 | 0x0 | u32 | `result` |  |
| 140 | 0x0 | u32 | `dc_point` |  |
| 141 | 0x0 | u32 | `sv_time` |  |
| 142 | 0x0 | u16 | `slot_num` |  |
| 143 | 0x0 | u32 | `sort_tm_sec` |  |
| 144 | 0x0 | u32 | `sort_tm_usec` |  |
| 145 | 0x0 | u16 | `conf_payload_boost_penalty` |  |
| 146 | 0x0 | u16 | `conf_payload_boost_bonus` |  |
| 147 | 0x0 | u16 | `conf_payload_body_balance_max` |  |
| 148 | 0x0 | u32 | `msma_sort_type` |  |
| 149 | 0x0 | u32 | `msma_sort_order` |  |
| 150 | 0x0 | u32 | `result` |  |
| 151 | 0x0 | u32 | `result` |  |
| 152 | 0x0 | u32 | `matching_type` |  |
| 153 | 0x0 | u32 | `mission_id` |  |
| 154 | 0x0 | u32 | `room_id` |  |
| 155 | 0x0 | u32 | `result` |  |
| 156 | 0x0 | u32 | `pilot_id` |  |
| 157 | 0x0 | u32 | `reason` |  |
| 158 | 0x0 | u32 | `result` |  |
| 159 | 0x0 | u32 | `uniqid_ms` |  |
| 160 | 0x0 | u32 | `color_id` |  |
| 161 | 0x0 | u32 | `unlocked_colors` |  |
| 162 | 0x0 | u32 | `result` |  |
| 163 | 0x0 | u32 | `recruit` |  |
| 164 | 0x0 | u32 | `sort_tm_sec` |  |
| 165 | 0x0 | u32 | `sort_tm_usec` |  |
| 166 | 0x0 | u32 | `msma_sort_type` |  |
| 167 | 0x0 | u32 | `msma_sort_order` |  |
| 168 | 0x8 | u32 | `get_reward` |  |
| 169 | ? | ? | `num_reward` |  |
| 170 | 0x0 | u32 | `highscore` |  |
| 171 | 0x0 | u32 | `result` |  |
| 172 | ? | ? | `clan_kind` |  |
| 173 | 0x0 | u32 | `cupteam_rate` |  |
| 174 | 0x0 | u32 | `last_bracket_id` |  |
| 175 | 0x8 | u32 | `is_enable` |  |
| 176 | 0x0 | u32 | `result` |  |
| 177 | 0x0 | u32 | `mailid` |  |
| 178 | 0x0 | u32 | `attach_type` |  |
| 179 | 0x0 | u32 | `attach_id` |  |
| 180 | 0x0 | u32 | `amount` |  |
| 181 | 0x0 | u32 | `result` |  |
| 182 | 0x0 | u32 | `pilot_id` |  |
| 183 | 0x0 | u32 | `world_id` |  |
| 184 | 0x0 | u32 | `result` |  |
| 185 | 0x0 | u32 | `gacha_id` |  |
| 186 | 0x0 | u32 | `act_date` |  |
| 187 | 0x0 | u16 | `act_num` |  |
| 188 | 0x0 | u32 | `buff_id` |  |
| 189 | 0x0 | u32 | `result` |  |
| 190 | 0x0 | u32 | `on_clear` |  |
| 191 | 0x0 | u32 | `result` |  |
| 192 | 0x0 | u32 | `result` |  |
| 193 | 0x0 | u32 | `remaining_days` |  |
| 194 | 0x0 | u32 | `result` |  |
| 195 | 0x0 | u32 | `state` |  |
| 196 | 0x0 | u32 | `buff_id` |  |
| 197 | 0x0 | u32 | `remain_sec` |  |
| 198 | 0x0 | u32 | `remain_max` |  |
| 199 | 0x0 | u32 | `result` |  |
| 200 | 0x0 | u32 | `remain` |  |
| 201 | 0x8 | u32 | `dailycup_conf` |  |
| 202 | ? | ? | `dailycup_conf_next` |  |
| 203 | 0x0 | u32 | `result` |  |
| 204 | 0x0 | u32 | `uniqid_ms` |  |
| 205 | 0x0 | u32 | `item_id` |  |
| 206 | 0x0 | u32 | `db_index` |  |
| 207 | 0x0 | u32 | `result` |  |
| 208 | 0x0 | u32 | `gacha_id` |  |
| 209 | 0x0 | u32 | `result` |  |
| 210 | 0x0 | u32 | `is_firstonetime` |  |
| 211 | 0x0 | u16 | `rate_vslocal` |  |
| 212 | 0x0 | u16 | `rate_vslocal_4ev` |  |
| 213 | 0x8 | u32 | `is_open_info` |  |
| 214 | 0x0 | u32 | `result` |  |
| 215 | 0x0 | u32 | `result` |  |
| 216 | 0x0 | u32 | `sv_time` |  |
| 217 | ? | ? | `clan_kind` |  |
| 218 | 0x0 | u32 | `result` |  |
| 219 | 0x0 | u32 | `result` |  |
| 220 | 0x0 | u32 | `result` |  |
| 221 | 0x0 | u32 | `uniqid` |  |
| 222 | 0x0 | u32 | `result` |  |
| 223 | 0x0 | u32 | `mailid` |  |
| 224 | 0x8 | u32 | `type` |  |
| 225 | 0x0 | u32 | `accum_playtime` |  |
| 226 | 0x8 | u32 | `pilot` |  |
| 227 | ? | ? | `stat` |  |
| 228 | 0x0 | u32 | `mission_id` |  |
| 229 | 0x0 | u32 | `is_party_leader` |  |
| 230 | 0x0 | u32 | `comeback_limittime` |  |
| 231 | 0x0 | u32 | `is_booking` |  |
| 232 | 0x8 | u32 | `challenge_info` |  |
| 233 | 0x0 | u32 | `result` |  |
| 234 | 0x0 | u32 | `hashval` |  |
| 235 | 0x0 | u32 | `src_bytes` |  |
| 236 | 0x0 | u16 | `compress` |  |
| 237 | 0x0 | u32 | `result` |  |
| 238 | 0x0 | u32 | `uniqid_ms` |  |
| 239 | 0x0 | u32 | `result` |  |
| 240 | 0x0 | u32 | `box_type` |  |
| 241 | 0x0 | u32 | `result` |  |
| 242 | 0x0 | u32 | `pilot_id_sub` |  |
| 243 | 0x0 | u32 | `is_set` |  |
| 244 | 0x0 | u32 | `clan_kind` |  |
| 245 | 0x0 | u32 | `result` |  |
| 246 | 0x0 | u32 | `uniqid_ms` |  |
| 247 | 0x0 | u32 | `equip_set` |  |
| 248 | 0x0 | u32 | `cost` |  |
| 249 | 0x0 | u32 | `result` |  |
| 250 | 0x0 | u32 | `matching_type` |  |
| 251 | 0x0 | u32 | `battlesv_port` |  |
| 252 | 0x0 | u32 | `room_id` |  |
| 253 | 0x0 | u32 | `attach_type` |  |
| 254 | 0x0 | u32 | `attach_id` |  |
| 255 | 0x0 | u32 | `amount` |  |
| 256 | 0x0 | u32 | `result` |  |
| 257 | 0x0 | u32 | `page_now` |  |
| 258 | 0x0 | u32 | `page_max` |  |
| 259 | 0x0 | u32 | `sort_info` |  |
| 260 | 0x0 | u32 | `result` |  |
| 261 | 0x0 | u32 | `uniqid_ms` |  |
| 262 | 0x0 | u32 | `workres` |  |
| 263 | 0x0 | u32 | `mech_npcpict` |  |
| 264 | 0x0 | u32 | `result` |  |
| 265 | 0x0 | u32 | `cinfo` |  |
| 266 | ? | ? | `clan_kind` |  |
| 267 | 0x0 | u32 | `result` |  |
| 268 | 0x0 | u32 | `pilot_id` |  |
| 269 | 0x0 | u32 | `result` |  |
| 270 | 0x0 | u32 | `uniqid_ms` |  |
| 271 | 0x0 | u32 | `cost` |  |
| 272 | 0x0 | u32 | `result` |  |
| 273 | 0x0 | u32 | `module_id` |  |
| 274 | 0x0 | u32 | `result` |  |
| 275 | 0x0 | u16 | `deckcost` |  |
| 276 | 0x0 | u16 | `remain` |  |
| 277 | 0x0 | u32 | `result` |  |
| 278 | 0x0 | u32 | `result` |  |
| 279 | 0x0 | u32 | `uniqid_ms` |  |
| 280 | 0x0 | u16 | `weapon_buildup_extra_cnt` |  |
| 281 | 0x0 | u32 | `party_id` |  |
| 282 | 0x0 | u32 | `channel_id` |  |
| 283 | 0x0 | u32 | `pilot_id` |  |
| 284 | 0x0 | u32 | `result` |  |
| 285 | 0x0 | u32 | `uniqid` |  |
| 286 | 0x0 | u32 | `energy_now` |  |
| 287 | 0x0 | u32 | `result` |  |
| 288 | 0x0 | u32 | `is_active` |  |
| 289 | ? | ? | `clan_kind` |  |
| 290 | 0x0 | u32 | `result` |  |
| 291 | 0x0 | u32 | `channel_id` |  |
| 292 | 0x0 | u32 | `party_id` |  |
| 293 | 0x0 | u32 | `remain_cnt` |  |
| 294 | 0x0 | u32 | `uniqid` |  |
| 295 | 0x0 | u32 | `msma_id` |  |
| 296 | 0x0 | u32 | `room_id` |  |
| 297 | 0x0 | u32 | `factor` |  |
| 298 | 0x0 | u32 | `sign_addr` |  |
| 299 | 0x0 | u32 | `sign_codelen` |  |
| 300 | 0x8 | u32 | `season_rb_conf` |  |
| 301 | ? | ? | `season_rb_conf_next` |  |
| 302 | 0x0 | u32 | `comeback_stat` |  |
| 303 | 0x0 | u32 | `result` |  |
| 304 | 0x0 | u32 | `uniqid_ms` |  |
| 305 | 0x0 | u32 | `decal` |  |
| 306 | 0x0 | u32 | `uniqid_decal` |  |
| 307 | 0x0 | u32 | `deckcost` |  |
| 308 | 0x0 | u32 | `result` |  |
| 309 | 0x0 | u32 | `result` |  |
| 310 | 0x0 | u32 | `roominfo` |  |
| 311 | 0x0 | u32 | `result` |  |
| 312 | 0x0 | u32 | `result` |  |
| 313 | 0x0 | u32 | `emb_base` |  |
| 314 | 0x0 | u32 | `emb_parts1` |  |
| 315 | ? | ? | `emb_parts2` |  |
| 316 | 0x0 | u32 | `result` |  |
| 317 | 0x0 | u32 | `ready_ok` |  |
| 318 | 0x0 | u32 | `result` |  |
| 319 | ? | ? | `clan_kind` |  |
| 320 | 0x0 | u32 | `result` |  |
| 321 | 0x0 | u32 | `uniqid_ms` |  |
| 322 | 0x0 | u16 | `slot` |  |
| 323 | 0x0 | u32 | `cost` |  |
| 324 | 0x0 | u32 | `result` |  |
| 325 | 0x0 | u32 | `uniqid_ms` |  |
| 326 | 0x0 | u32 | `equip_set` |  |
| 327 | 0x0 | u32 | `result` |  |
| 328 | 0x0 | u32 | `tree_id` |  |
| 329 | 0x0 | u32 | `node_no` |  |
| 330 | 0x0 | u32 | `idx_no` |  |
| 331 | 0x0 | u32 | `point_use` |  |
| 332 | 0x0 | u32 | `is_supply` |  |
| 333 | 0x0 | u32 | `result` |  |
| 334 | 0x0 | u32 | `uniqid_ms` |  |
| 335 | 0x0 | u32 | `item_id` |  |
| 336 | 0x0 | u32 | `result` |  |
| 337 | 0x0 | u32 | `matching_type` |  |
| 338 | 0x0 | u32 | `rescode` |  |
| 339 | 0x0 | u32 | `bracket_idx` |  |
| 340 | 0x0 | u32 | `team_id` |  |
| 341 | 0x0 | u32 | `result` |  |
| 342 | 0x0 | u32 | `remaining_days` |  |
| 343 | 0x0 | u32 | `result` |  |
| 344 | 0x0 | u32 | `result` |  |
| 345 | 0x0 | u32 | `quest_id` |  |
| 346 | 0x0 | u32 | `result` |  |
| 347 | 0x0 | u32 | `result` |  |
| 348 | 0x0 | u32 | `result` |  |
| 349 | 0x0 | u32 | `uniq_msid` |  |
| 350 | 0x0 | u32 | `level` |  |
| 351 | 0x0 | u32 | `uniq_msid` |  |
| 352 | 0x0 | u16 | `param_idx` |  |
| 353 | 0x0 | u16 | `up_param` |  |
| 354 | 0x0 | u32 | `penalty_sec` |  |
| 355 | 0x0 | u32 | `result` |  |
| 356 | 0x0 | u32 | `uniq_msid` |  |
| 357 | 0x0 | u32 | `item_id` |  |
| 358 | 0x0 | u32 | `result` |  |
| 359 | 0x0 | u32 | `module_id` |  |
| 360 | 0x0 | u32 | `count` |  |
| 361 | 0x0 | u32 | `is_revoked` |  |
| 362 | 0x0 | u32 | `item_id` |  |
| 363 | 0x0 | u16 | `stack` |  |
| 364 | 0x0 | u32 | `fixed_team_num` |  |
| 365 | 0x0 | u32 | `result` |  |
| 366 | 0x0 | u32 | `clan_kind` |  |
| 367 | 0x0 | u32 | `sort_info` |  |
| 368 | 0x8 | u32 | `remain` |  |
| 369 | 0x0 | u32 | `result` |  |
| 370 | 0x0 | u32 | `quest_id` |  |
| 371 | 0x0 | u32 | `room_id` |  |
| 372 | 0x0 | u32 | `pilot_id` |  |
| 373 | ? | ? | `is_gm_camera` |  |
| 374 | ? | ? | `is_all_clear` |  |
| 375 | 0x0 | u32 | `cnt_completed` |  |
| 376 | 0x0 | u16 | `year` |  |
| 377 | 0x0 | u16 | `month` |  |
| 378 | 0x0 | u32 | `world_id` |  |
| 379 | 0x0 | u32 | `result` |  |
| 380 | 0x0 | u32 | `uniqid_ms` |  |
| 381 | 0x0 | u32 | `item_id` |  |
| 382 | 0x0 | u32 | `db_index` |  |
| 383 | 0x0 | u32 | `result` |  |
| 384 | 0x0 | u32 | `uniqid_ms` |  |
| 385 | 0x0 | u32 | `result` |  |
| 386 | 0x0 | u32 | `to_pilotid` |  |
| 387 | 0x0 | u32 | `result` |  |
| 388 | 0x0 | u32 | `result` |  |
| 389 | 0x0 | u32 | `team_id` |  |
| 390 | 0x0 | u32 | `troops` |  |
| 391 | 0x0 | u32 | `result` |  |
| 392 | 0x0 | u32 | `slot_num` |  |
| 393 | 0x0 | u32 | `pilot_id` |  |
| 394 | 0x0 | u16 | `deckcost` |  |
| 395 | 0x0 | u16 | `remain` |  |
| 396 | 0x0 | u32 | `rokaku_pt` |  |
| 397 | 0x0 | u32 | `result` |  |
| 398 | 0x0 | u32 | `from_pilotid` |  |
| 399 | 0x0 | u32 | `from_clan_id` |  |
| 400 | 0x0 | u32 | `mailid` |  |
| 401 | 0x0 | u32 | `result` |  |
| 402 | 0x0 | u32 | `info` |  |
| 403 | 0x0 | u32 | `next` |  |
| 404 | 0x0 | u32 | `type` |  |
| 405 | 0x0 | u32 | `uniqid` |  |
| 406 | 0x0 | u32 | `result` |  |
| 407 | 0x0 | u32 | `reason` |  |
| 408 | 0x0 | u32 | `cinfo` |  |
| 409 | ? | ? | `clan_kind` |  |
| 410 | ? | ? | `clan_forbidden` |  |
| 411 | 0x0 | u32 | `result` |  |
| 412 | 0x0 | u32 | `result` |  |
| 413 | 0x0 | u32 | `uniqid_ms` |  |
| 414 | 0x0 | u16 | `slot` |  |
| 415 | 0x0 | u32 | `color` |  |
| 416 | 0x0 | u32 | `sort_tm_sec` |  |
| 417 | 0x0 | u32 | `sort_tm_usec` |  |
| 418 | 0x0 | u32 | `msma_sort_type` |  |
| 419 | 0x0 | u32 | `msma_sort_order` |  |
| 420 | 0x0 | u32 | `result` |  |
| 421 | 0x0 | u32 | `pilot_id_kick` |  |
| 422 | 0x0 | u32 | `clan_kind` |  |
| 423 | 0x0 | u32 | `result` |  |
| 424 | 0x0 | u32 | `strg_msma` |  |
| 425 | 0x0 | u32 | `strg_item` |  |
| 426 | 0x0 | u32 | `clan_emblem` |  |
| 427 | 0x0 | u32 | `clan_npc` |  |
| 428 | 0x0 | u32 | `msma_energy` |  |
| 429 | 0x0 | u32 | `deckcost` |  |
| 430 | 0x0 | u32 | `avatar_reset` |  |
| 431 | 0x0 | u16 | `periodpath_ticket_0_bc` |  |
| 432 | 0x0 | u16 | `periodpath_ticket_1_bc` |  |
| 433 | 0x0 | u16 | `periodpath_ticket_2_bc` |  |
| 434 | 0x0 | u16 | `periodpath_ticket_0_days` |  |
| 435 | ? | ? | `periodpath_ticket_1_days` |  |
| 436 | ? | ? | `periodpath_ticket_2_days` |  |
| 437 | 0x0 | u32 | `item_id` |  |
| 438 | 0x0 | u32 | `amount` |  |
| 439 | 0x0 | u32 | `pilot_id` |  |
| 440 | 0x0 | u32 | `result` |  |
| 441 | 0x0 | u32 | `pilot_id` |  |
| 442 | 0x0 | u32 | `del_kind` |  |
| 443 | 0x0 | u32 | `del_remain_sec` |  |
| 444 | 0x0 | u32 | `result` |  |
| 445 | 0x0 | u32 | `price` |  |
| 446 | 0x0 | u32 | `result` |  |
| 447 | 0x0 | u32 | `id_type` |  |
| 448 | 0x0 | u32 | `result` |  |
| 449 | 0x0 | u32 | `send_sysmes` |  |
| 450 | 0x0 | u32 | `quest_id` |  |
| 451 | 0x0 | u32 | `achieve_denom` |  |
| 452 | 0x0 | u32 | `achieve_num` |  |
| 453 | 0x0 | u32 | `result` |  |
| 454 | 0x0 | u32 | `result` |  |
| 455 | 0x0 | u32 | `uniqid_ms` |  |
| 456 | 0x0 | u32 | `item_id` |  |
| 457 | 0x0 | u32 | `result` |  |
| 458 | 0x0 | u32 | `order` |  |
| 459 | 0x0 | u32 | `result` |  |
| 460 | 0x0 | u32 | `result` |  |
| 461 | 0x0 | u32 | `uniqid_ms` |  |
| 462 | 0x0 | u32 | `color` |  |
| 463 | 0x0 | u32 | `result` |  |
| 464 | 0x0 | u32 | `unlocked_navi` |  |
| 465 | 0x0 | u32 | `box_type` |  |
| 466 | 0x8 | u32 | `replay_info` |  |
| 467 | 0x0 | u32 | `win_troops` |  |
| 468 | 0x0 | u32 | `pilot_id` |  |
| 469 | 0x0 | u32 | `exam_state` |  |
| 470 | 0x0 | u32 | `result` |  |
| 471 | 0x0 | u32 | `uniqid_ms` |  |
| 472 | 0x0 | u32 | `workres` |  |
| 473 | 0x0 | u32 | `mech_npcpict` |  |
| 474 | 0x0 | u32 | `result` |  |
| 475 | 0x0 | u32 | `result` |  |
| 476 | 0x0 | u32 | `admin_lv` |  |
| 477 | 0x0 | u32 | `term_sec` |  |
| 478 | 0x8 | u32 | `is_accept` |  |
| 479 | 0x0 | u32 | `val1` |  |
| 480 | 0x0 | u32 | `val2` |  |
| 481 | 0x0 | u32 | `result` |  |
| 482 | 0x0 | u32 | `intro_info` |  |
| 483 | 0x0 | u32 | `clan_kind` |  |
| 484 | 0x0 | u32 | `uniqid_ms` |  |
| 485 | 0x0 | u32 | `sp_parts` |  |
| 486 | 0x0 | u32 | `result` |  |
| 487 | 0x0 | u32 | `uniqid_ms` |  |
| 488 | 0x0 | u32 | `pilot_id` |  |
| 489 | 0x0 | u32 | `troops` |  |
| 490 | 0x0 | u32 | `result` |  |
| 491 | 0x0 | u32 | `uniqid_ms` |  |
| 492 | 0x0 | u32 | `sp_parts_id` |  |
| 493 | 0x0 | u32 | `result` |  |
| 494 | 0x0 | u32 | `item_id` |  |
| 495 | 0x0 | u32 | `pilot_id` |  |
| 496 | 0x0 | u32 | `count` |  |
| 497 | 0x0 | u32 | `type` |  |
| 498 | 0x0 | u32 | `result` |  |
| 499 | 0x0 | u32 | `clan_kind` |  |
| 500 | 0x0 | u32 | `result` |  |
| 501 | ? | ? | `is_mission_vs_force_entry` |  |
| 502 | ? | ? | `xwar_entry_is_freeze` |  |
| 503 | ? | ? | `vswar_entry_is_freeze` |  |
| 504 | 0x0 | u32 | `matching_type` |  |
| 505 | 0x0 | u32 | `room_id` |  |
| 506 | 0x0 | u32 | `wait_sec` |  |
| 507 | 0x0 | u32 | `mission_id` |  |
| 508 | 0x0 | u32 | `sc_lv_max` |  |
| 509 | 0x0 | u32 | `result` |  |
| 510 | 0x0 | u32 | `pilot_id_new` |  |
| 511 | 0x0 | u32 | `clan_kind` |  |
| 512 | 0x0 | u32 | `color` |  |
| 513 | 0x0 | u16 | `is_invalid` |  |
| 514 | 0x0 | u32 | `result` |  |
| 515 | 0x0 | u32 | `mission_id` |  |
| 516 | 0x0 | u32 | `is_lock` |  |
| 517 | 0x0 | u32 | `result` |  |
| 518 | 0x0 | u32 | `cnt_completed` |  |
| 519 | 0x0 | u32 | `item_id` |  |
| 520 | 0x0 | u16 | `item_cnt` |  |
| 521 | 0x0 | u32 | `money_gp` |  |
| 522 | 0x0 | u32 | `result` |  |
| 523 | 0x0 | u32 | `world_id` |  |
| 524 | 0x0 | u32 | `pcard` |  |
| 525 | 0x0 | u32 | `result` |  |
| 526 | 0x0 | u32 | `uniqid_ms` |  |
| 527 | 0x0 | u32 | `result` |  |
| 528 | 0x0 | u32 | `index` |  |
| 529 | 0x0 | u32 | `bracket` |  |
| 530 | 0x0 | u32 | `result` |  |
| 531 | 0x0 | u32 | `clan_kind` |  |
| 532 | 0x0 | u32 | `result` |  |
| 533 | 0x0 | u32 | `slot_num` |  |
| 534 | 0x0 | u32 | `result` |  |
| 535 | 0x0 | u32 | `ms_set` |  |
| 536 | 0x0 | u32 | `pilot_id` |  |
| 537 | 0x0 | u32 | `pilot_id` |  |
| 538 | 0x0 | u32 | `favms_id` |  |
| 539 | 0x0 | u32 | `exp_mine` |  |
| 540 | 0x0 | u32 | `exp_top` |  |
| 541 | 0x0 | u32 | `my_rank` |  |
| 542 | 0x0 | u32 | `result` |  |
| 543 | 0x0 | u32 | `is_revoke` |  |
| 544 | 0x0 | u32 | `order` |  |
| 545 | ? | ? | `rankself` |  |
| 546 | 0x0 | u32 | `page_now` |  |
| 547 | 0x0 | u32 | `page_max` |  |
| 548 | 0x0 | u32 | `result` |  |
| 549 | 0x0 | u32 | `clan_kind` |  |
| 550 | 0x0 | u32 | `result` |  |
| 551 | 0x0 | u32 | `uniqid_ms` |  |
| 552 | 0x0 | u32 | `ticket_id` |  |
| 553 | 0x0 | u16 | `usenum` |  |
| 554 | 0x0 | u32 | `workres` |  |
| 555 | 0x0 | u16 | `buildup_cnt` |  |
| 556 | 0x0 | u16 | `param_idx` |  |
| 557 | 0x0 | u16 | `up_param` |  |
| 558 | 0x0 | u32 | `mech_npcpict` |  |
| 559 | 0x0 | u32 | `result` |  |
| 560 | 0x0 | u32 | `result` |  |
| 561 | 0x0 | u16 | `deck_type` |  |
| 562 | 0x0 | u16 | `slot` |  |
| 563 | 0x0 | u32 | `result` |  |
| 564 | 0x0 | u32 | `troops` |  |
| 565 | 0x0 | u32 | `slot` |  |
| 566 | 0x0 | u32 | `pilot_id` |  |
| 567 | ? | ? | `request_status` |  |
| 568 | 0x0 | u32 | `pilot_rename_remaintime` |  |
| 569 | 0x0 | u32 | `notice_id` |  |
| 570 | 0x0 | u32 | `width` |  |
| 571 | 0x0 | u32 | `height` |  |
| 572 | 0x0 | u32 | `userid` |  |
| 573 | 0x0 | u32 | `pilot_id` |  |
| 574 | 0x0 | u32 | `accum_point` |  |
| 575 | 0x0 | u32 | `rank` |  |
| 576 | 0x0 | u32 | `base_accump` |  |
| 577 | 0x0 | u32 | `req_accump` |  |
| 578 | 0x0 | u32 | `deckcost` |  |
| 579 | 0x0 | u32 | `result` |  |
| 580 | 0x0 | u32 | `price_gp` |  |
| 581 | 0x0 | u32 | `price_cp` |  |
| 582 | 0x0 | u32 | `result` |  |
| 583 | 0x0 | u32 | `id_type` |  |
| 584 | 0x0 | u32 | `itemid` |  |
| 585 | 0x0 | u32 | `result` |  |
| 586 | 0x0 | u32 | `pilot` |  |
| 587 | 0x0 | u32 | `result` |  |
| 588 | 0x0 | u32 | `result` |  |
| 589 | 0x0 | u32 | `uniq_msid` |  |
| 590 | 0x0 | u32 | `decktype` |  |
| 591 | 0x0 | u32 | `result` |  |
| 592 | 0x0 | u32 | `is_revoke` |  |
| 593 | 0x0 | u32 | `order` |  |
| 594 | ? | ? | `rankself` |  |
| 595 | 0x0 | u32 | `page_now` |  |
| 596 | 0x0 | u32 | `page_max` |  |
| 597 | 0x0 | u32 | `term_rankerbattle` |  |
| 598 | 0x0 | u32 | `result` |  |
| 599 | 0x0 | u32 | `order` |  |
| 600 | 0x0 | u32 | `result` |  |
| 601 | 0x0 | u32 | `price` |  |
| 602 | 0x0 | u32 | `result` |  |
| 603 | 0x0 | u32 | `result` |  |
| 604 | 0x0 | u32 | `emblem_id` |  |
| 605 | 0x0 | u32 | `use_gp` |  |
| 606 | 0x0 | u32 | `result` |  |
| 607 | 0x0 | u32 | `result` |  |
| 608 | 0x0 | u32 | `result` |  |
| 609 | 0x0 | u32 | `progress_id` |  |
| 610 | 0x0 | u32 | `remain` |  |
| 611 | 0x0 | u32 | `result` |  |
| 612 | 0x0 | u32 | `result` |  |
| 613 | 0x0 | u32 | `quest_id` |  |
| 614 | 0x0 | u32 | `result` |  |
| 615 | 0x0 | u32 | `clan_kind` |  |
| 616 | 0x0 | u32 | `result` |  |
| 617 | 0x0 | u32 | `uniqid_ms` |  |
| 618 | 0x0 | u32 | `result` |  |
| 619 | 0x0 | u32 | `heroms_uniqid` |  |
| 620 | 0x0 | u32 | `result` |  |
| 621 | 0x0 | u32 | `matching_type` |  |
| 622 | 0x0 | u32 | `matching_request_flag` |  |
| 623 | 0x0 | u32 | `matching_battlerule_flag` |  |
| 624 | 0x0 | u32 | `matching_extrule_flag` |  |
| 625 | 0x0 | u32 | `ext_subrule` |  |
| 626 | 0x0 | u32 | `xwar_ext_rule` |  |
| 627 | 0x0 | u32 | `result` |  |
| 628 | 0x0 | u16 | `adop_result` |  |
| 629 | 0x0 | u32 | `adop_uniq_msid` |  |
| 630 | 0x0 | u32 | `adop_get` |  |
| 631 | 0x8 | u32 | `wbonus` |  |
| 632 | 0x0 | u32 | `pilot_id` |  |
| 633 | 0x0 | u32 | `result` |  |
| 634 | 0x0 | u32 | `remain_count` |  |
| 635 | 0x0 | u32 | `state` |  |
| 636 | 0x0 | u32 | `rb_rank` |  |
| 637 | 0x0 | u32 | `reccode` |  |
| 638 | 0x0 | u32 | `is_set` |  |
| 639 | 0x0 | u32 | `result` |  |
| 640 | 0x0 | u32 | `uniqid_ms` |  |
| 641 | 0x0 | u32 | `uniqid` |  |
| 642 | 0x0 | u16 | `inv_place` |  |
| 643 | 0x0 | u32 | `sort_tm_sec` |  |
| 644 | 0x0 | u32 | `sort_tm_usec` |  |
| 645 | 0x0 | u32 | `result` |  |
| 646 | 0x0 | u32 | `result` |  |
| 647 | ? | ? | `clan_kind` |  |
| 648 | 0x0 | u32 | `result` |  |
| 649 | 0x0 | u32 | `uniqid_ms` |  |
| 650 | 0x0 | u32 | `result` |  |
| 651 | 0x0 | u32 | `matching_type` |  |
| 652 | 0x0 | u32 | `is_newbie` |  |
| 653 | 0x0 | u32 | `matching_request_flag` |  |
| 654 | 0x0 | u32 | `matching_battlerule_flag` |  |
| 655 | 0x0 | u32 | `matching_extrule_flag` |  |
| 656 | 0x0 | u32 | `is_party_wait` |  |
| 657 | 0x0 | u16 | `party_wait_sec` |  |
| 658 | 0x0 | u32 | `uniqid` |  |
| 659 | 0x0 | u16 | `stack` |  |
| 660 | 0x0 | u32 | `win_team` |  |
| 661 | 0x0 | u32 | `res_coop` |  |
| 662 | 0x0 | u32 | `progress` |  |
| 663 | ? | ? | `result` |  |
| 664 | ? | ? | `result_wbonus` |  |
| 665 | ? | ? | `totalresult_wave` |  |
| 666 | 0x0 | u16 | `ranking_highscore` |  |
| 667 | ? | ? | `dcpoint` |  |
| 668 | 0x0 | u32 | `dbbonus_get` |  |
| 669 | 0x0 | u32 | `pointdmg` |  |
| 670 | 0x0 | u16 | `adop_result` |  |
| 671 | 0x0 | u32 | `adop_uniq_msid` |  |
| 672 | 0x0 | u32 | `adop_get` |  |
| 673 | 0x0 | u32 | `season_class_up_promotion_point` |  |
| 674 | 0x0 | u32 | `from_pilot_id` |  |
| 675 | 0x0 | u32 | `result` |  |
| 676 | 0x0 | u32 | `troops` |  |
| 677 | 0x0 | u32 | `result` |  |
| 678 | 0x0 | u32 | `uniqid` |  |
| 679 | 0x0 | u16 | `decktype` |  |
| 680 | 0x0 | u16 | `deckslot` |  |
| 681 | 0x0 | u16 | `is_costover` |  |
| 682 | 0x0 | u32 | `result` |  |
| 683 | 0x0 | u32 | `gacha_id` |  |
| 684 | 0x0 | u32 | `cupteam_rate` |  |
| 685 | 0x0 | u32 | `last_bracket_id` |  |
| 686 | 0x0 | u32 | `phase` |  |
| 687 | 0x0 | u32 | `bracket` |  |
| 688 | 0x0 | u32 | `uniq_msid` |  |
| 689 | 0x0 | u32 | `result` |  |
| 690 | 0x0 | u32 | `uniqid_ms` |  |
| 691 | 0x0 | u16 | `eq_slot` |  |
| 692 | 0x0 | u32 | `item_id` |  |
| 693 | 0x0 | u32 | `result` |  |
| 694 | 0x0 | u32 | `uniqid_ms` |  |
| 695 | 0x0 | u32 | `ticket_id` |  |
| 696 | 0x0 | u16 | `usenum` |  |
| 697 | 0x0 | u32 | `workres` |  |
| 698 | 0x0 | u16 | `buildup_cnt` |  |
| 699 | 0x0 | u16 | `param_idx` |  |
| 700 | 0x0 | u16 | `up_param` |  |
| 701 | 0x0 | u32 | `mech_npcpict` |  |
| 702 | ? | ? | `clan_kind` |  |
| 703 | 0x0 | u32 | `result` |  |
| 704 | ? | ? | `clan_kind` |  |
| 705 | ? | ? | `coop_entry_is_freeze` |  |
| 706 | 0x0 | u32 | `result` |  |
| 707 | 0x0 | u32 | `pilot_id` |  |
| 708 | 0x0 | u32 | `world_id` |  |
| 709 | 0x0 | u32 | `precord` |  |
| 710 | ? | ? | `plvhist` |  |
| 711 | 0x0 | u32 | `result` |  |
| 712 | 0x0 | u32 | `hashval` |  |
| 713 | 0x0 | u32 | `src_bytes` |  |
| 714 | 0x0 | u16 | `compress` |  |
| 715 | 0x0 | u32 | `msma_id` |  |
| 716 | 0x0 | u16 | `stack` |  |
| 717 | 0x0 | u16 | `node_id` |  |
| 718 | 0x0 | u32 | `wait_sec` |  |
| 719 | 0x0 | u32 | `result` |  |
| 720 | 0x0 | u32 | `uniqid_ms` |  |
| 721 | 0x0 | u32 | `item_id` |  |
| 722 | 0x0 | u32 | `ticket_id` |  |
| 723 | 0x0 | u16 | `usenum` |  |
| 724 | 0x0 | u16 | `param_target` |  |
| 725 | 0x0 | u32 | `workres` |  |
| 726 | 0x0 | u16 | `buildup_cnt` |  |
| 727 | 0x0 | u16 | `up_param` |  |
| 728 | 0x0 | u32 | `mech_npcpict` |  |
| 729 | 0x0 | u32 | `version` |  |
| 730 | 0x0 | u32 | `gentime` |  |
| 731 | 0x0 | u32 | `result` |  |
| 732 | 0x0 | u32 | `send_sysmes` |  |
| 733 | 0x0 | u32 | `result` |  |
| 734 | 0x0 | u32 | `cnt_completed` |  |
| 735 | 0x0 | u32 | `item_id` |  |
| 736 | 0x0 | u16 | `item_cnt` |  |
| 737 | 0x0 | u32 | `money_gp` |  |
| 738 | 0x0 | u32 | `evflag3` |  |
| 739 | 0x0 | u32 | `result` |  |
| 740 | 0x0 | u32 | `charge_point` |  |
| 741 | ? | ? | `is_tutorial_end` |  |
| 742 | 0x0 | u32 | `pilot_rename_price` |  |
| 743 | 0x0 | u32 | `pilot_rename_time_efsf` |  |
| 744 | 0x0 | u32 | `pilot_rename_forbidtime_efsf` |  |
| 745 | 0x0 | u32 | `pilot_rename_time_zeon` |  |
| 746 | 0x0 | u32 | `pilot_rename_forbidtime_zeon` |  |
| 747 | 0x0 | u32 | `penalty_exp` |  |
| 748 | 0x0 | u32 | `penalty_money` |  |
| 749 | 0x0 | u32 | `result` |  |
| 750 | 0x0 | u32 | `info` |  |
| 751 | 0x0 | u32 | `pilot_id` |  |
| 752 | 0x0 | u16 | `lv_new` |  |
| 753 | 0x0 | u16 | `lv_old` |  |
| 754 | 0x0 | u32 | `lv_point` |  |
| 755 | 0x0 | u16 | `deckcost` |  |
| 756 | 0x0 | u16 | `reason` |  |
| 757 | 0x0 | u16 | `is_penalty` |  |
| 758 | 0x0 | u32 | `result` |  |
| 759 | 0x0 | u32 | `is_recruiting` |  |
| 760 | 0x0 | u32 | `party_type` |  |
| 761 | 0x0 | u32 | `result` |  |
| 762 | 0x0 | u32 | `uniq_msid` |  |
| 763 | 0x0 | u32 | `buildup_cnt` |  |
| 764 | 0x0 | u32 | `buildup_info` |  |
| 765 | 0x0 | u32 | `result` |  |
| 766 | 0x0 | u32 | `result` |  |
| 767 | 0x0 | u32 | `avatar` |  |
| 768 | 0x0 | u32 | `result` |  |
| 769 | 0x0 | u32 | `mclan_id` |  |
| 770 | ? | ? | `clan_kind` |  |
| 771 | 0x0 | u32 | `lvpt_now` |  |
| 772 | 0x0 | u32 | `pilot_id` |  |
| 773 | 0x0 | u32 | `result` |  |
| 774 | 0x0 | u32 | `id_type` |  |
| 775 | 0x0 | u32 | `item` |  |
| 776 | 0x0 | u32 | `result` |  |
| 777 | 0x0 | u32 | `pilot_id` |  |
| 778 | 0x0 | u32 | `connet_world_num` |  |
| 779 | 0x0 | u32 | `connet_world_id` |  |
| 780 | 0x0 | u32 | `matching_type` |  |
| 781 | 0x0 | u32 | `is_active` |  |
| 782 | 0x0 | u32 | `room_cnt` |  |
| 783 | 0x0 | u32 | `remain_count` |  |
| 784 | 0x0 | u32 | `remain_seconds` |  |
| 785 | 0x0 | u32 | `pilot_id` |  |
| 786 | 0x0 | u32 | `result` |  |
| 787 | 0x0 | u32 | `event_flag` |  |
| 788 | 0x0 | u32 | `is_set` |  |
| 789 | 0x0 | u32 | `fame_now` |  |
| 790 | 0x0 | u32 | `result` |  |
| 791 | 0x0 | u32 | `uniqid_ms` |  |
| 792 | 0x0 | u32 | `cost` |  |
| 793 | 0x0 | u32 | `result` |  |
| 794 | 0x0 | u32 | `uniqid_ms` |  |
| 795 | 0x0 | u32 | `result` |  |
| 796 | 0x0 | u32 | `result` |  |
| 797 | 0x0 | u32 | `on_event` |  |
| 798 | 0x0 | u32 | `result` |  |
| 799 | 0x0 | u32 | `to_pilot_id` |  |
| 800 | 0x0 | u32 | `factor` |  |
| 801 | 0x0 | u32 | `index` |  |
| 802 | 0x0 | u32 | `item_id` |  |
| 803 | 0x0 | u32 | `amount` |  |
| 804 | 0x0 | u32 | `result` |  |
| 805 | 0x0 | u32 | `clan_kind` |  |
| 806 | 0x0 | u32 | `pilot_id_old_leader` |  |
| 807 | 0x0 | u32 | `pilot_id_new_leader` |  |
| 808 | 0x0 | u32 | `result` |  |
| 809 | 0x0 | u32 | `price_gp` |  |
| 810 | 0x0 | u32 | `price_cp` |  |
| 811 | 0x0 | u32 | `result` |  |
| 812 | 0x0 | u32 | `gacha_id` |  |
| 813 | 0x0 | u32 | `result` |  |
| 814 | 0x0 | u32 | `archive` |  |
| 815 | 0x0 | u32 | `holding_id` |  |
| 816 | 0x0 | u32 | `logincnt` |  |
| 817 | 0x0 | u32 | `xwarcnt` |  |
| 818 | ? | ? | `is_all_clear` |  |
| 819 | 0x0 | u32 | `cnt_completed` |  |
| 820 | 0x0 | u16 | `year` |  |
| 821 | 0x0 | u16 | `month` |  |
| 822 | 0x0 | u16 | `inv_place` |  |
| 823 | 0x0 | u16 | `item` |  |
| 824 | 0x0 | u32 | `result` |  |
| 825 | 0x0 | u32 | `channel_id` |  |
| 826 | 0x0 | u32 | `loungesv_port` |  |
| 827 | 0x0 | u32 | `userid` |  |
| 828 | 0x0 | u32 | `pilot_id` |  |
| 829 | 0x0 | u32 | `result` |  |
| 830 | 0x0 | u32 | `refuse_pilot_id` |  |
| 831 | 0x0 | u32 | `reason` |  |
| 832 | 0x0 | u32 | `result` |  |
| 833 | 0x0 | u32 | `price` |  |
| 834 | 0x0 | u32 | `clan_id` |  |
| 835 | 0x0 | u32 | `point_use` |  |
| 836 | 0x0 | u32 | `point_pool` |  |

## `0xb0cc20`（150463 字节，705 字段）← 调用者: 0xd91ce0, 0xeed800

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `ent_id` |  |
| 2 | 0x0 | u32 | `itemid` |  |
| 3 | 0x0 | u32 | `airbomb_id` |  |
| 4 | 0x0 | u16 | `target_x` |  |
| 5 | 0x0 | u16 | `target_y` |  |
| 6 | 0x0 | u16 | `target_z` |  |
| 7 | 0x0 | u16 | `shot0_drop1_impact2` |  |
| 8 | 0x0 | u16 | `fx_opt` |  |
| 9 | 0x0 | u16 | `ent_id` |  |
| 10 | 0x0 | u32 | `result` |  |
| 11 | 0x0 | u16 | `ent_id` |  |
| 12 | 0x0 | u16 | `ent_id` |  |
| 13 | 0x0 | u32 | `itemid` |  |
| 14 | 0x0 | u16 | `dir_h` |  |
| 15 | 0x0 | u32 | `wrestle_id` |  |
| 16 | 0x0 | u16 | `target_ent_id` |  |
| 17 | 0x0 | u16 | `target_pos_x` |  |
| 18 | 0x0 | u16 | `target_pos_y` |  |
| 19 | 0x0 | u16 | `target_pos_z` |  |
| 20 | 0x8 | u32 | `appear_info` |  |
| 21 | 0x0 | u16 | `to_ent_id` |  |
| 22 | 0x0 | u32 | `remain_msec` |  |
| 23 | 0x0 | u32 | `result` |  |
| 24 | 0x0 | u16 | `ent_id` |  |
| 25 | 0x0 | u32 | `reason` |  |
| 26 | 0x0 | u16 | `not_use` |  |
| 27 | 0x0 | u16 | `ent_id` |  |
| 28 | 0x0 | u16 | `weapon_state` |  |
| 29 | 0x0 | u16 | `weapon_change_flag` |  |
| 30 | 0x0 | u32 | `result` |  |
| 31 | 0x0 | u32 | `world_id` |  |
| 32 | 0x0 | u32 | `pilot_id` |  |
| 33 | 0x0 | u32 | `member_index` |  |
| 34 | 0x0 | u32 | `is_commander` |  |
| 35 | 0x0 | u16 | `remain_sec` |  |
| 36 | 0x0 | u32 | `reason` |  |
| 37 | 0x0 | u32 | `world_id` |  |
| 38 | 0x0 | u32 | `pilot_id` |  |
| 39 | 0x0 | u16 | `point_gain` |  |
| 40 | 0x0 | u32 | `point_total` |  |
| 41 | 0x0 | u16 | `n_cont_kill` |  |
| 42 | 0x0 | u16 | `bonus_cont_kill` |  |
| 43 | 0x0 | u32 | `result` |  |
| 44 | ? | ? | `is_with_resume` |  |
| 45 | ? | ? | `script_thread` |  |
| 46 | 0x0 | u16 | `ent_id` |  |
| 47 | 0x8 | u32 | `team` |  |
| 48 | ? | ? | `troops` |  |
| 49 | 0x0 | u32 | `world_id` |  |
| 50 | 0x0 | u32 | `pilot_id` |  |
| 51 | ? | ? | `is_all` |  |
| 52 | ? | ? | `is_party` |  |
| 53 | ? | ? | `is_audience` |  |
| 54 | 0x0 | u32 | `snapshot_int_msec` |  |
| 55 | 0x0 | u32 | `snapshot_res_msec` |  |
| 56 | 0x0 | u32 | `pos_factor` |  |
| 57 | 0x0 | u32 | `map_id` |  |
| 58 | 0x0 | u32 | `btlfield` |  |
| 59 | 0x0 | u32 | `clear_remain_msec` |  |
| 60 | 0x0 | u32 | `is_disable_conq_sp` |  |
| 61 | ? | ? | `is_room_suspend` |  |
| 62 | 0x0 | u32 | `mission_id` |  |
| 63 | 0x0 | u32 | `sudden_type` |  |
| 64 | 0x0 | u32 | `sudden_bonus_target` |  |
| 65 | 0x0 | u32 | `exp_min` |  |
| 66 | 0x0 | u32 | `exp_max` |  |
| 67 | 0x0 | u32 | `config` |  |
| 68 | ? | ? | `progress` |  |
| 69 | ? | ? | `bgm_desc` |  |
| 70 | 0x0 | u32 | `mission_phase` |  |
| 71 | 0x0 | u16 | `ent_id` |  |
| 72 | 0x0 | u16 | `ent_id` |  |
| 73 | 0x0 | u32 | `itemid` |  |
| 74 | 0x0 | u32 | `grenade_id` |  |
| 75 | 0x0 | u16 | `launch_x` |  |
| 76 | 0x0 | u16 | `launch_y` |  |
| 77 | 0x0 | u16 | `launch_z` |  |
| 78 | 0x0 | u16 | `target_x` |  |
| 79 | 0x0 | u16 | `target_y` |  |
| 80 | 0x0 | u16 | `target_z` |  |
| 81 | 0x0 | u16 | `target_ent_id` |  |
| 82 | 0x0 | u16 | `msec` |  |
| 83 | 0x0 | u16 | `shot0_impact1` |  |
| 84 | ? | ? | `fx_opt` |  |
| 85 | ? | ? | `charge_lv` |  |
| 86 | 0x0 | u32 | `result` |  |
| 87 | 0x0 | u16 | `access_type` |  |
| 88 | 0x0 | u32 | `from_world_id` |  |
| 89 | 0x0 | u32 | `from_pilot_id` |  |
| 90 | 0x0 | u16 | `from_ent_id` |  |
| 91 | 0x0 | u16 | `to_ent_id` |  |
| 92 | 0x0 | u32 | `hp_now` |  |
| 93 | 0x0 | u32 | `hp_max` |  |
| 94 | 0x0 | u16 | `ent_id` |  |
| 95 | 0x0 | u32 | `support_type` |  |
| 96 | 0x0 | u32 | `team` |  |
| 97 | ? | ? | `troops` |  |
| 98 | 0x0 | u16 | `target_x` |  |
| 99 | 0x0 | u16 | `target_y` |  |
| 100 | 0x0 | u16 | `target_z` |  |
| 101 | 0x0 | u16 | `count` |  |
| 102 | 0x0 | u16 | `is_hit_send` |  |
| 103 | 0x0 | u16 | `ent_id` |  |
| 104 | 0x0 | u16 | `hp_percent` |  |
| 105 | 0x0 | u32 | `index` |  |
| 106 | 0x0 | u16 | `ent_id` |  |
| 107 | 0x0 | u32 | `voice_id` |  |
| 108 | 0x0 | u32 | `voice_volume` |  |
| 109 | ? | ? | `is_cutin` |  |
| 110 | ? | ? | `is_party` |  |
| 111 | ? | ? | `is_use_textmsg` |  |
| 112 | 0x0 | u32 | `result` |  |
| 113 | 0x0 | u16 | `to_ent_id` |  |
| 114 | 0x8 | u32 | `team` |  |
| 115 | ? | ? | `troops` |  |
| 116 | 0x0 | u32 | `support_type` |  |
| 117 | 0x0 | u32 | `spt_spot_index` |  |
| 118 | 0x0 | u32 | `result` |  |
| 119 | 0x0 | u32 | `btlfield` |  |
| 120 | 0x8 | u32 | `is_lot` |  |
| 121 | 0x8 | u32 | `team` |  |
| 122 | ? | ? | `troops` |  |
| 123 | 0x0 | u32 | `commander_id` |  |
| 124 | 0x0 | u32 | `result` |  |
| 125 | 0x0 | u32 | `result` |  |
| 126 | 0x0 | u32 | `ent_id` |  |
| 127 | 0x0 | u32 | `type` |  |
| 128 | 0x0 | u16 | `ent_id` |  |
| 129 | 0x0 | u32 | `limit_msec` |  |
| 130 | 0x0 | u32 | `elapsed_msec` |  |
| 131 | 0x0 | u16 | `ent_id` |  |
| 132 | 0x0 | u32 | `countdown_msec` |  |
| 133 | 0x0 | u32 | `result` |  |
| 134 | 0x0 | u32 | `is_lot` |  |
| 135 | 0x0 | u16 | `lot_count` |  |
| 136 | 0x0 | u32 | `state` |  |
| 137 | 0x0 | u32 | `member_count` |  |
| 138 | 0x0 | u32 | `result` |  |
| 139 | 0x0 | u32 | `world_id` |  |
| 140 | 0x0 | u32 | `pilot_id` |  |
| 141 | 0x0 | u32 | `stat` |  |
| 142 | 0x0 | u16 | `percent_val` |  |
| 143 | 0x0 | u16 | `equip_idx` |  |
| 144 | 0x0 | u16 | `to_x` |  |
| 145 | 0x0 | u16 | `to_y` |  |
| 146 | 0x0 | u16 | `to_z` |  |
| 147 | 0x0 | u16 | `msec` |  |
| 148 | 0x0 | u32 | `ent_id` |  |
| 149 | 0x0 | u16 | `target_x` |  |
| 150 | 0x0 | u16 | `target_y` |  |
| 151 | 0x0 | u16 | `target_z` |  |
| 152 | 0x0 | u16 | `begin1_end0` |  |
| 153 | 0x0 | u32 | `world_id` |  |
| 154 | 0x0 | u32 | `pilot_id` |  |
| 155 | 0x0 | u32 | `is_editing` |  |
| 156 | 0x0 | u16 | `end_x` |  |
| 157 | 0x0 | u16 | `end_y` |  |
| 158 | 0x0 | u16 | `end_z` |  |
| 159 | 0x0 | u16 | `ent_id` |  |
| 160 | 0x8 | u32 | `mprogress` |  |
| 161 | 0x0 | u16 | `ent_id` |  |
| 162 | 0x0 | u32 | `cutin_category_id` |  |
| 163 | 0x0 | u32 | `result` |  |
| 164 | 0x0 | u32 | `order_index` |  |
| 165 | 0x0 | u32 | `order_number` |  |
| 166 | ? | ? | `order_kind` |  |
| 167 | 0x0 | u32 | `order_param` |  |
| 168 | 0x0 | u32 | `conquer` |  |
| 169 | 0x0 | u16 | `ent_id` |  |
| 170 | 0x0 | u16 | `hit_dir` |  |
| 171 | 0x0 | u32 | `spbits` |  |
| 172 | 0x0 | u32 | `optbits` |  |
| 173 | 0x0 | u16 | `staggery_power` |  |
| 174 | 0x0 | u16 | `staggery_msec` |  |
| 175 | 0x0 | u16 | `ent_id` |  |
| 176 | 0x0 | u16 | `from_ent_id` |  |
| 177 | 0x0 | u32 | `weapon_itemid` |  |
| 178 | 0x0 | u32 | `charge_lv` |  |
| 179 | 0x0 | u32 | `hp_now` |  |
| 180 | 0x0 | u32 | `hp_max` |  |
| 181 | 0x0 | u32 | `damage` |  |
| 182 | 0x0 | u32 | `spbits` |  |
| 183 | 0x0 | u16 | `hit_pos_x` |  |
| 184 | 0x0 | u16 | `hit_pos_y` |  |
| 185 | 0x0 | u16 | `hit_pos_z` |  |
| 186 | 0x0 | u16 | `hit_dir` |  |
| 187 | 0x0 | u16 | `body_region` |  |
| 188 | 0x0 | u32 | `optbits` |  |
| 189 | 0x0 | u32 | `shield_hp_now` |  |
| 190 | 0x0 | u16 | `ent_id` |  |
| 191 | 0x0 | u16 | `state_bit` |  |
| 192 | 0x0 | u32 | `result` |  |
| 193 | 0x0 | u16 | `access_type` |  |
| 194 | 0x0 | u16 | `from_ent_id` |  |
| 195 | 0x0 | u32 | `to_world_id` |  |
| 196 | 0x0 | u32 | `to_pilot_id` |  |
| 197 | 0x0 | u16 | `to_ent_id` |  |
| 198 | 0x0 | u32 | `hp_now` |  |
| 199 | 0x0 | u32 | `hp_max` |  |
| 200 | 0x0 | u32 | `sigval` |  |
| 201 | 0x0 | u16 | `ent_id` |  |
| 202 | 0x0 | u32 | `itemid` |  |
| 203 | 0x0 | u16 | `to_ent_id` |  |
| 204 | 0x0 | u16 | `from_ent_id` |  |
| 205 | 0x0 | u32 | `remain_msec` |  |
| 206 | 0x0 | u32 | `gauge_val` |  |
| 207 | 0x0 | u32 | `no_complement` |  |
| 208 | 0x0 | u16 | `fire_sx` |  |
| 209 | 0x0 | u16 | `fire_sy` |  |
| 210 | 0x0 | u16 | `fire_sz` |  |
| 211 | 0x0 | u16 | `fire_ex` |  |
| 212 | 0x0 | u16 | `fire_ey` |  |
| 213 | 0x0 | u16 | `fire_ez` |  |
| 214 | 0x0 | u16 | `end_x` |  |
| 215 | 0x0 | u16 | `end_y` |  |
| 216 | 0x0 | u16 | `end_z` |  |
| 217 | 0x0 | u32 | `party_worldid` |  |
| 218 | 0x0 | u32 | `party_pilotid` |  |
| 219 | 0x0 | u32 | `frame_count` |  |
| 220 | 0x0 | u32 | `remain_msec` |  |
| 221 | 0x8 | u32 | `type` |  |
| 222 | 0x0 | u32 | `support_type` |  |
| 223 | 0x0 | u16 | `ent_id` |  |
| 224 | 0x0 | u32 | `hp_now` |  |
| 225 | 0x0 | u32 | `hp_max` |  |
| 226 | 0x0 | u32 | `spbits` |  |
| 227 | 0x0 | u16 | `hit_dir` |  |
| 228 | 0x0 | u32 | `world_id` |  |
| 229 | 0x0 | u32 | `pilot_id` |  |
| 230 | 0x0 | u16 | `ent_id` |  |
| 231 | 0x0 | u16 | `to_ent_id` |  |
| 232 | 0x0 | u32 | `limit_msec` |  |
| 233 | 0x8 | u32 | `team` |  |
| 234 | ? | ? | `troops` |  |
| 235 | 0x0 | u32 | `clan_id` |  |
| 236 | ? | ? | `clan_emb_base` |  |
| 237 | ? | ? | `clan_emb_parts1` |  |
| 238 | ? | ? | `clan_emb_parts2` |  |
| 239 | 0x0 | u16 | `supplyer_end_id` |  |
| 240 | 0x0 | u32 | `frame_count` |  |
| 241 | 0x0 | u32 | `remain_msec` |  |
| 242 | 0x8 | u32 | `check_quest` |  |
| 243 | 0x0 | u32 | `remain_sec` |  |
| 244 | 0x8 | u32 | `team` |  |
| 245 | ? | ? | `troops` |  |
| 246 | 0x0 | u32 | `support_type` |  |
| 247 | 0x0 | u32 | `remain_msec` |  |
| 248 | 0x0 | u16 | `target_x` |  |
| 249 | 0x0 | u16 | `target_y` |  |
| 250 | 0x0 | u16 | `target_z` |  |
| 251 | 0x0 | u32 | `use_worldid` |  |
| 252 | 0x0 | u32 | `use_pilotid` |  |
| 253 | ? | ? | `script_thread` |  |
| 254 | 0x8 | u32 | `type` |  |
| 255 | 0x0 | u16 | `args` |  |
| 256 | 0x8 | u32 | `wave_res` |  |
| 257 | 0x0 | u16 | `ent_id` |  |
| 258 | 0x0 | u16 | `val2` |  |
| 259 | 0x0 | u32 | `voice_id` |  |
| 260 | 0x0 | u32 | `elap_msec` |  |
| 261 | 0x0 | u32 | `world_id` |  |
| 262 | 0x0 | u32 | `pilot_id` |  |
| 263 | 0x0 | u16 | `lv_old` |  |
| 264 | 0x0 | u16 | `lv_new` |  |
| 265 | 0x0 | u32 | `state` |  |
| 266 | 0x0 | u32 | `state` |  |
| 267 | 0x8 | u32 | `team` |  |
| 268 | 0x0 | u32 | `cupteam_id` |  |
| 269 | 0x0 | u32 | `cupteam_rate` |  |
| 270 | 0x0 | u32 | `tournament_vs_type` |  |
| 271 | 0x0 | u16 | `ent_id` |  |
| 272 | 0x0 | u32 | `itemid` |  |
| 273 | 0x0 | u32 | `arms_id` |  |
| 274 | 0x0 | u16 | `target_x` |  |
| 275 | 0x0 | u16 | `target_y` |  |
| 276 | 0x0 | u16 | `target_z` |  |
| 277 | 0x0 | u16 | `target_ent_id` |  |
| 278 | 0x0 | u16 | `state` |  |
| 279 | ? | ? | `fx_opt` |  |
| 280 | 0x0 | u32 | `judge_worldid` |  |
| 281 | 0x0 | u32 | `judge_pilotid` |  |
| 282 | 0x8 | u32 | `team` |  |
| 283 | ? | ? | `troops` |  |
| 284 | 0x0 | u32 | `support_type` |  |
| 285 | 0x0 | u16 | `ent_id` |  |
| 286 | 0x0 | u16 | `spt_ms_index` |  |
| 287 | 0x0 | u16 | `spt_spot_index` |  |
| 288 | 0x8 | u32 | `team` |  |
| 289 | ? | ? | `troops` |  |
| 290 | 0x0 | u32 | `pilot_id` |  |
| 291 | 0x0 | u16 | `level` |  |
| 292 | 0x0 | u32 | `cutin_id` |  |
| 293 | ? | ? | `gender` |  |
| 294 | ? | ? | `platoon` |  |
| 295 | ? | ? | `platoon_slot` |  |
| 296 | ? | ? | `is_platoon_leader` |  |
| 297 | ? | ? | `dtaskf_order_number` |  |
| 298 | ? | ? | `is_disable_scoreboard` |  |
| 299 | 0x0 | u32 | `result` |  |
| 300 | 0x0 | u32 | `elapsed_sec` |  |
| 301 | 0x0 | u32 | `limit_sec` |  |
| 302 | 0x0 | u32 | `kill_count` |  |
| 303 | 0x0 | u32 | `death_count` |  |
| 304 | 0x8 | u32 | `team` |  |
| 305 | 0x0 | u32 | `troops` |  |
| 306 | 0x0 | u32 | `world_id` |  |
| 307 | 0x0 | u32 | `pilot_id` |  |
| 308 | ? | ? | `snapshot` |  |
| 309 | ? | ? | `funnelss` |  |
| 310 | 0x0 | u16 | `unattended_state_bit` |  |
| 311 | 0x0 | u16 | `weapon_state_bits` |  |
| 312 | 0x0 | u16 | `target_icon` |  |
| 313 | ? | ? | `is_respawn` |  |
| 314 | ? | ? | `is_using_ss` |  |
| 315 | ? | ? | `stghold_number` |  |
| 316 | ? | ? | `xweapon_fired` |  |
| 317 | 0x0 | u32 | `grenade_id` |  |
| 318 | 0x0 | u16 | `pos_x` |  |
| 319 | 0x0 | u16 | `pos_y` |  |
| 320 | 0x0 | u16 | `pos_z` |  |
| 321 | 0x0 | u16 | `target_ent_id` |  |
| 322 | 0x0 | u16 | `from_ent_id` |  |
| 323 | 0x0 | u16 | `to_ent_id` |  |
| 324 | 0x0 | u32 | `weapon_itemid` |  |
| 325 | 0x0 | u32 | `fire_id` |  |
| 326 | 0x0 | u16 | `ent_id` |  |
| 327 | 0x0 | u16 | `attach_parent_ent_id` |  |
| 328 | 0x0 | u16 | `attach_socket` |  |
| 329 | 0x0 | u16 | `attach_pos_x` |  |
| 330 | 0x0 | u16 | `attach_pos_y` |  |
| 331 | 0x0 | u16 | `attach_pos_z` |  |
| 332 | 0x8 | u32 | `team` |  |
| 333 | ? | ? | `troops` |  |
| 334 | 0x0 | u16 | `ent_id` |  |
| 335 | 0x0 | u16 | `target_x` |  |
| 336 | 0x0 | u16 | `target_y` |  |
| 337 | 0x0 | u16 | `target_z` |  |
| 338 | 0x0 | u16 | `spt_spot_index` |  |
| 339 | 0x0 | u16 | `spt_spot_dir` |  |
| 340 | 0x0 | u32 | `remain_msec` |  |
| 341 | 0x8 | u32 | `team` |  |
| 342 | ? | ? | `troops` |  |
| 343 | ? | ? | `snapshot` |  |
| 344 | ? | ? | `funnelss` |  |
| 345 | 0x0 | u32 | `hp_now` |  |
| 346 | 0x0 | u32 | `hp_max` |  |
| 347 | 0x0 | u32 | `shield_hp_now` |  |
| 348 | 0x0 | u32 | `shield_hp_max` |  |
| 349 | 0x0 | u16 | `weapon_state_bits` |  |
| 350 | 0x0 | u32 | `nearz` |  |
| 351 | 0x0 | u32 | `farz` |  |
| 352 | 0x0 | u32 | `color_r` |  |
| 353 | ? | ? | `color_g` |  |
| 354 | ? | ? | `color_b` |  |
| 355 | 0x0 | u32 | `time` |  |
| 356 | 0x0 | u32 | `elapsed_time` |  |
| 357 | 0x0 | u16 | `ent_id` |  |
| 358 | 0x0 | u16 | `effect_id` |  |
| 359 | 0x0 | u16 | `is_start` |  |
| 360 | 0x0 | u16 | `kind` |  |
| 361 | 0x0 | u32 | `param` |  |
| 362 | 0x8 | u32 | `team` |  |
| 363 | ? | ? | `troops` |  |
| 364 | 0x0 | u32 | `support_type` |  |
| 365 | 0x0 | u16 | `ent_id` |  |
| 366 | 0x0 | u16 | `spt_ms_index` |  |
| 367 | 0x0 | u16 | `spt_spot_index` |  |
| 368 | 0x0 | u32 | `state` |  |
| 369 | 0x0 | u32 | `member_count` |  |
| 370 | 0x0 | u32 | `support_type` |  |
| 371 | 0x0 | u32 | `remain_msec` |  |
| 372 | 0x0 | u32 | `target_change_msec` |  |
| 373 | 0x0 | u16 | `ent_id` |  |
| 374 | 0x0 | u16 | `ent_id` |  |
| 375 | 0x0 | u32 | `itemid` |  |
| 376 | 0x0 | u16 | `target_ent_id` |  |
| 377 | 0x0 | u32 | `reason` |  |
| 378 | 0x0 | u16 | `ent_id_dead` |  |
| 379 | 0x0 | u32 | `world_id_kill` |  |
| 380 | 0x0 | u32 | `pilot_id_kill` |  |
| 381 | 0x0 | u32 | `kill_streak` |  |
| 382 | 0x0 | u32 | `weapon_itemid` |  |
| 383 | 0x0 | u32 | `is_extend_style_change_limit` |  |
| 384 | 0x0 | u32 | `result` |  |
| 385 | 0x0 | u32 | `ms_index` |  |
| 386 | 0x0 | u32 | `post_index` |  |
| 387 | 0x0 | u32 | `spt_spot_index` |  |
| 388 | 0x0 | u16 | `respawn_ent_id` |  |
| 389 | 0x0 | u32 | `ent_id` |  |
| 390 | 0x0 | u32 | `type` |  |
| 391 | 0x0 | u16 | `ent_id` |  |
| 392 | 0x0 | u32 | `weapon_itemid` |  |
| 393 | 0x0 | u32 | `result` |  |
| 394 | 0x0 | u32 | `fx_id` |  |
| 395 | 0x0 | u32 | `is_scale` |  |
| 396 | 0x8 | u32 | `deck_index` |  |
| 397 | 0x0 | u16 | `respawn_wait_sec` |  |
| 398 | 0x0 | u16 | `respawn_wait_max` |  |
| 399 | 0x0 | u32 | `weapon_itemid` |  |
| 400 | 0x0 | u16 | `to_ent_id` |  |
| 401 | 0x0 | u16 | `from_ent_id` |  |
| 402 | 0x0 | u16 | `hit_pos_x` |  |
| 403 | 0x0 | u16 | `hit_pos_y` |  |
| 404 | 0x0 | u16 | `hit_pos_z` |  |
| 405 | 0x0 | u32 | `result` |  |
| 406 | 0x0 | u32 | `frame_count` |  |
| 407 | 0x0 | u16 | `group_id` |  |
| 408 | 0x0 | u16 | `reason` |  |
| 409 | 0x0 | u32 | `reason` |  |
| 410 | 0x0 | u16 | `point_gain` |  |
| 411 | 0x0 | u32 | `point_total` |  |
| 412 | 0x0 | u16 | `is_taskforce_aux` |  |
| 413 | 0x0 | u32 | `point_atk` |  |
| 414 | 0x0 | u32 | `point_spt` |  |
| 415 | 0x0 | u32 | `point_con` |  |
| 416 | 0x0 | u32 | `kill_streak_chain_num` |  |
| 417 | 0x8 | u32 | `index` |  |
| 418 | ? | ? | `is_lock` |  |
| 419 | 0x0 | u16 | `ent_id` |  |
| 420 | 0x0 | u32 | `module_hp` |  |
| 421 | 0x0 | u32 | `is_force` |  |
| 422 | 0x0 | u16 | `ent_id_dead` |  |
| 423 | 0x0 | u32 | `world_id_kill` |  |
| 424 | 0x0 | u32 | `pilot_id_kill` |  |
| 425 | 0x0 | u32 | `decal_kill` |  |
| 426 | 0x0 | u32 | `weapon_itemid` |  |
| 427 | 0x0 | u16 | `repair_wait_sec` |  |
| 428 | 0x0 | u16 | `kill_streak_count` |  |
| 429 | 0x0 | u32 | `spbits` |  |
| 430 | 0x0 | u32 | `is_resurrect` |  |
| 431 | 0x0 | u32 | `is_extend_style_change_limit` |  |
| 432 | 0x8 | u32 | `team` |  |
| 433 | ? | ? | `troops` |  |
| 434 | 0x0 | u32 | `support_type` |  |
| 435 | 0x0 | u16 | `ent_id` |  |
| 436 | 0x0 | u16 | `target_x` |  |
| 437 | 0x0 | u16 | `target_y` |  |
| 438 | 0x0 | u16 | `target_z` |  |
| 439 | 0x0 | u16 | `spt_ms_index` |  |
| 440 | 0x0 | u16 | `spt_spot_index` |  |
| 441 | 0x0 | u16 | `spt_spot_dir` |  |
| 442 | 0x0 | u16 | `remain_cnt` |  |
| 443 | 0x0 | u32 | `remain_msec` |  |
| 444 | 0x0 | u32 | `use_worldid` |  |
| 445 | 0x0 | u32 | `use_pilotid` |  |
| 446 | 0x0 | u16 | `setter_ms` |  |
| 447 | 0x0 | u32 | `color` |  |
| 448 | 0x0 | u32 | `result` |  |
| 449 | 0x0 | u32 | `spawn1st_post` |  |
| 450 | 0x0 | u32 | `is_1st` |  |
| 451 | 0x0 | u32 | `result` |  |
| 452 | 0x0 | u32 | `result` |  |
| 453 | 0x0 | u32 | `frame_count` |  |
| 454 | 0x0 | u16 | `group_id` |  |
| 455 | 0x0 | u16 | `action_type` |  |
| 456 | 0x0 | u16 | `route_number` |  |
| 457 | 0x0 | u32 | `remain_msec` |  |
| 458 | 0x0 | u32 | `clear_remain_msec` |  |
| 459 | 0x0 | u32 | `result` |  |
| 460 | 0x0 | u32 | `room_id` |  |
| 461 | 0x0 | u32 | `mission_id` |  |
| 462 | 0x0 | u32 | `extrule_id` |  |
| 463 | 0x0 | u32 | `dc_node_id` |  |
| 464 | 0x0 | u32 | `is_rankerbattle` |  |
| 465 | 0x0 | u32 | `map_id` |  |
| 466 | 0x0 | u32 | `is_vsclan` |  |
| 467 | 0x0 | u32 | `comeback_stat` |  |
| 468 | 0x0 | u32 | `is_playing` |  |
| 469 | ? | ? | `is_netcafe` |  |
| 470 | ? | ? | `team` |  |
| 471 | ? | ? | `is_practice` |  |
| 472 | ? | ? | `config` |  |
| 473 | ? | ? | `progress` |  |
| 474 | 0x0 | u16 | `expup_fgauge` |  |
| 475 | 0x0 | u16 | `is_ev_caravan` |  |
| 476 | ? | ? | `flag_wideuse` |  |
| 477 | ? | ? | `extrarule_xwar_info` |  |
| 478 | 0x0 | u32 | `remain_msec` |  |
| 479 | 0x0 | u32 | `from_ent_id` |  |
| 480 | 0x0 | u32 | `wslot_idx` |  |
| 481 | 0x8 | u32 | `win_team` |  |
| 482 | 0x0 | u16 | `fire_x` |  |
| 483 | 0x0 | u16 | `fire_y` |  |
| 484 | 0x0 | u16 | `fire_z` |  |
| 485 | 0x0 | u16 | `end_x` |  |
| 486 | 0x0 | u16 | `end_y` |  |
| 487 | 0x0 | u16 | `end_z` |  |
| 488 | 0x0 | u32 | `result` |  |
| 489 | 0x0 | u16 | `ent_id` |  |
| 490 | 0x0 | u32 | `count` |  |
| 491 | 0x0 | u32 | `maxcount` |  |
| 492 | 0x0 | u16 | `ent_id` |  |
| 493 | 0x0 | u16 | `hit_dir` |  |
| 494 | 0x0 | u32 | `spbits` |  |
| 495 | 0x0 | u32 | `optbits` |  |
| 496 | 0x0 | u16 | `down_power` |  |
| 497 | 0x0 | u16 | `down_msec` |  |
| 498 | 0x0 | u16 | `ent_id_radar` |  |
| 499 | 0x0 | u32 | `support_type` |  |
| 500 | 0x0 | u32 | `is_completed` |  |
| 501 | 0x0 | u32 | `stg_arms_initiation_ms` |  |
| 502 | 0x0 | u16 | `ent_id` |  |
| 503 | 0x0 | u32 | `itemid` |  |
| 504 | 0x0 | u32 | `grenade_id` |  |
| 505 | 0x0 | u32 | `parent_id` |  |
| 506 | 0x0 | u16 | `launch_x` |  |
| 507 | 0x0 | u16 | `launch_y` |  |
| 508 | 0x0 | u16 | `launch_z` |  |
| 509 | 0x0 | u16 | `target1_x` |  |
| 510 | 0x0 | u16 | `target1_y` |  |
| 511 | 0x0 | u16 | `target1_z` |  |
| 512 | 0x0 | u16 | `target2_x` |  |
| 513 | 0x0 | u16 | `target2_y` |  |
| 514 | 0x0 | u16 | `target2_z` |  |
| 515 | 0x0 | u16 | `target_ent_id` |  |
| 516 | 0x0 | u16 | `msec` |  |
| 517 | 0x0 | u16 | `shot0_impact1` |  |
| 518 | ? | ? | `fx_opt` |  |
| 519 | ? | ? | `charge_lv` |  |
| 520 | 0x0 | u32 | `result` |  |
| 521 | 0x0 | u16 | `target_x` |  |
| 522 | 0x0 | u16 | `target_y` |  |
| 523 | 0x0 | u16 | `target_z` |  |
| 524 | 0x0 | u32 | `use_worldid` |  |
| 525 | 0x0 | u32 | `use_pilotid` |  |
| 526 | 0x8 | u32 | `target_member` |  |
| 527 | 0x0 | u16 | `target_ace` |  |
| 528 | 0x0 | u16 | `kill_cnt` |  |
| 529 | 0x0 | u16 | `death_cnt` |  |
| 530 | 0x8 | u32 | `team` |  |
| 531 | ? | ? | `troops` |  |
| 532 | 0x0 | u16 | `ent_id` |  |
| 533 | 0x0 | u32 | `color` |  |
| 534 | 0x0 | u16 | `ent_id` |  |
| 535 | 0x0 | u32 | `itemid` |  |
| 536 | 0x0 | u32 | `grenade_id` |  |
| 537 | 0x0 | u32 | `parent_id` |  |
| 538 | 0x0 | u16 | `launch_x` |  |
| 539 | 0x0 | u16 | `launch_y` |  |
| 540 | 0x0 | u16 | `launch_z` |  |
| 541 | 0x0 | u16 | `target1_x` |  |
| 542 | 0x0 | u16 | `target1_y` |  |
| 543 | 0x0 | u16 | `target1_z` |  |
| 544 | 0x0 | u16 | `target2_x` |  |
| 545 | 0x0 | u16 | `target2_y` |  |
| 546 | 0x0 | u16 | `target2_z` |  |
| 547 | 0x0 | u16 | `target_ent_id` |  |
| 548 | 0x0 | u16 | `msec` |  |
| 549 | 0x0 | u16 | `shot0_impact1` |  |
| 550 | ? | ? | `fx_opt` |  |
| 551 | ? | ? | `charge_lv` |  |
| 552 | ? | ? | `impact_wall` |  |
| 553 | ? | ? | `action` |  |
| 554 | 0x0 | u16 | `ent_id` |  |
| 555 | 0x0 | u32 | `result` |  |
| 556 | 0x0 | u32 | `equip_index` |  |
| 557 | 0x0 | u32 | `equip_itemid` |  |
| 558 | 0x0 | u32 | `is_force` |  |
| 559 | 0x0 | u16 | `equip_idx` |  |
| 560 | 0x0 | u32 | `ent_id` |  |
| 561 | 0x0 | u16 | `target_x` |  |
| 562 | 0x0 | u16 | `target_y` |  |
| 563 | 0x0 | u16 | `target_z` |  |
| 564 | 0x0 | u16 | `begin1_end0` |  |
| 565 | 0x0 | u32 | `frame_count` |  |
| 566 | 0x0 | u32 | `remain_msec` |  |
| 567 | 0x0 | u32 | `result` |  |
| 568 | 0x0 | u32 | `result` |  |
| 569 | 0x8 | u32 | `team` |  |
| 570 | ? | ? | `troops` |  |
| 571 | 0x0 | u32 | `world_id` |  |
| 572 | 0x0 | u32 | `pilot` |  |
| 573 | 0x0 | u32 | `stat` |  |
| 574 | 0x0 | u32 | `is_commander` |  |
| 575 | ? | ? | `is_audience` |  |
| 576 | ? | ? | `member_index` |  |
| 577 | ? | ? | `dtaskf_order_number` |  |
| 578 | 0x0 | u32 | `kill_count` |  |
| 579 | 0x0 | u32 | `death_count` |  |
| 580 | 0x0 | u16 | `ent_id` |  |
| 581 | 0x0 | u16 | `pos_x` |  |
| 582 | 0x0 | u16 | `pos_y` |  |
| 583 | 0x0 | u16 | `pos_z` |  |
| 584 | 0x0 | u16 | `reason` |  |
| 585 | 0x8 | u32 | `win_team` |  |
| 586 | ? | ? | `win_troops` |  |
| 587 | ? | ? | `progress` |  |
| 588 | 0x0 | u32 | `world_id` |  |
| 589 | 0x0 | u32 | `pilot_id` |  |
| 590 | 0x0 | u32 | `grenade_id` |  |
| 591 | 0x0 | u16 | `hit_x` |  |
| 592 | 0x0 | u16 | `hit_y` |  |
| 593 | 0x0 | u16 | `hit_z` |  |
| 594 | 0x0 | u16 | `vec_x` |  |
| 595 | 0x0 | u16 | `vec_y` |  |
| 596 | 0x0 | u16 | `vec_z` |  |
| 597 | 0x0 | u16 | `vec_power` |  |
| 598 | 0x0 | u16 | `ent_id` |  |
| 599 | 0x0 | u32 | `group_id` |  |
| 600 | 0x0 | u16 | `toggle` |  |
| 601 | 0x0 | u16 | `reason` |  |
| 602 | 0x0 | u16 | `ent_id` |  |
| 603 | 0x0 | u32 | `msec` |  |
| 604 | 0x0 | u16 | `rate` |  |
| 605 | 0x0 | u16 | `ent_id` |  |
| 606 | 0x0 | u32 | `itemid` |  |
| 607 | 0x0 | u16 | `dir_h` |  |
| 608 | 0x0 | u16 | `dir_v` |  |
| 609 | 0x0 | u16 | `msec` |  |
| 610 | 0x0 | u32 | `wrestle_id` |  |
| 611 | 0x0 | u32 | `charge_lv` |  |
| 612 | ? | ? | `action` |  |
| 613 | 0x0 | u16 | `chase_ent_id` |  |
| 614 | 0x0 | u16 | `is_dp_damage_cut` |  |
| 615 | 0x0 | u16 | `remain_sec` |  |
| 616 | 0x8 | u32 | `bgm_desc` |  |
| 617 | 0x0 | u32 | `fade_msec` |  |
| 618 | 0x0 | u32 | `reset` |  |
| 619 | 0x0 | u32 | `result` |  |
| 620 | 0x0 | u32 | `world_id` |  |
| 621 | 0x0 | u32 | `pilot_id` |  |
| 622 | 0x0 | u32 | `weapon_itemid` |  |
| 623 | 0x0 | u16 | `ent_id` |  |
| 624 | 0x0 | u32 | `optbit` |  |
| 625 | 0x0 | u16 | `hit_pos_x` |  |
| 626 | 0x0 | u16 | `hit_pos_y` |  |
| 627 | 0x0 | u16 | `hit_pos_z` |  |
| 628 | 0x0 | u16 | `ent_id` |  |
| 629 | 0x0 | u32 | `level_up_flag` |  |
| 630 | 0x0 | u32 | `next_level_max` |  |
| 631 | 0x0 | u32 | `version` |  |
| 632 | 0x0 | u32 | `gentime` |  |
| 633 | 0x0 | u16 | `gauge_old` |  |
| 634 | 0x0 | u16 | `gauge_now` |  |
| 635 | 0x0 | u32 | `result` |  |
| 636 | 0x0 | u32 | `from_world_id` |  |
| 637 | 0x0 | u32 | `from_pilot_id` |  |
| 638 | 0x0 | u16 | `from_ent_id` |  |
| 639 | 0x0 | u16 | `to_ent_id` |  |
| 640 | 0x0 | u32 | `hp_now` |  |
| 641 | 0x0 | u32 | `hp_max` |  |
| 642 | 0x0 | u32 | `shield_hp_now` |  |
| 643 | 0x0 | u32 | `shield_hp_max` |  |
| 644 | 0x0 | u32 | `result` |  |
| 645 | 0x0 | u32 | `cmdr_world_id` |  |
| 646 | 0x0 | u32 | `cmdr_pilot_id` |  |
| 647 | 0x0 | u16 | `ent_id` |  |
| 648 | 0x0 | u16 | `point` |  |
| 649 | 0x0 | u16 | `point_max` |  |
| 650 | 0x0 | u16 | `ent_id` |  |
| 651 | 0x0 | u16 | `hit_dir` |  |
| 652 | 0x0 | u32 | `spbits` |  |
| 653 | 0x0 | u32 | `optbits` |  |
| 654 | 0x0 | u16 | `stumble_power` |  |
| 655 | 0x0 | u16 | `stumble_msec` |  |
| 656 | 0x0 | u32 | `gauge_max` |  |
| 657 | 0x0 | u16 | `ent_id` |  |
| 658 | 0x0 | u32 | `itemid` |  |
| 659 | 0x0 | u32 | `bit_id` |  |
| 660 | 0x0 | u32 | `shot_alive` |  |
| 661 | 0x0 | u16 | `launch_x` |  |
| 662 | 0x0 | u16 | `launch_y` |  |
| 663 | 0x0 | u16 | `launch_z` |  |
| 664 | 0x0 | u16 | `target_x` |  |
| 665 | 0x0 | u16 | `target_y` |  |
| 666 | 0x0 | u16 | `target_z` |  |
| 667 | 0x0 | u16 | `target_ent_id` |  |
| 668 | 0x0 | u16 | `msec` |  |
| 669 | 0x0 | u16 | `release0_shot1` |  |
| 670 | 0x0 | u16 | `fx_opt` |  |
| 671 | 0x0 | u16 | `ent_id` |  |
| 672 | 0x0 | u32 | `group_id` |  |
| 673 | 0x0 | u32 | `is_succcess` |  |
| 674 | 0x0 | u16 | `ent_id` |  |
| 675 | 0x0 | u16 | `repair_wait_sec` |  |
| 676 | 0x0 | u16 | `ent_id` |  |
| 677 | 0x0 | u32 | `weapon_itemid` |  |
| 678 | 0x0 | u32 | `fire_id` |  |
| 679 | 0x0 | u32 | `rank` |  |
| 680 | 0x0 | u16 | `ent_id` |  |
| 681 | 0x0 | u32 | `itemid` |  |
| 682 | 0x0 | u16 | `launch_x` |  |
| 683 | 0x0 | u16 | `launch_y` |  |
| 684 | 0x0 | u16 | `launch_z` |  |
| 685 | 0x0 | u16 | `target_x` |  |
| 686 | 0x0 | u16 | `target_y` |  |
| 687 | 0x0 | u16 | `target_z` |  |
| 688 | 0x0 | u16 | `charge_lv` |  |
| 689 | 0x0 | u16 | `reflect_ent_id` |  |
| 690 | 0x0 | u16 | `ent_id` |  |
| 691 | 0x0 | u16 | `itembox_ent_id` |  |
| 692 | 0x0 | u32 | `itemid` |  |
| 693 | 0x0 | u32 | `trap_weaponid` |  |
| 694 | 0x0 | u16 | `ent_id` |  |
| 695 | 0x0 | u32 | `damage` |  |
| 696 | 0x8 | u32 | `rank` |  |
| 697 | ? | ? | `badge_type` |  |
| 698 | 0x0 | u32 | `examination_playscore` |  |
| 699 | 0x0 | u32 | `examination_playsec_remain_msec` |  |
| 700 | 0x0 | u16 | `ent_id` |  |
| 701 | 0x0 | u32 | `result` |  |
| 702 | 0x0 | u32 | `is_cancel` |  |
| 703 | 0x0 | u16 | `ent_id` |  |
| 704 | 0x0 | u32 | `countdown_msec` |  |
| 705 | 0x0 | u32 | `state` |  |

## `0xb4c650`（4231 字节，63 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `teamside` |  |
| 2 | 0x8 | u32 | `money` |  |
| 3 | 0x10 | u32 | `cmdr_fame` |  |
| 4 | 0x14 | u32 | `victory_fame` |  |
| 5 | 0x18 | u32 | `victory_score` |  |
| 6 | 0x1C | u32 | `alloy_chip` |  |
| 7 | 0x20 | u16 | `rate_vslocal` |  |
| 8 | 0x22 | u16 | `rate_vslocal_4ev` |  |
| 9 | 0x24 | u16 | `lv_point_self` |  |
| 10 | 0x26 | u16 | `lv_point_team` |  |
| 11 | 0x28 | u16 | `over_custom_exp` |  |
| 12 | 0x2A | u16 | `rate_vslocal_clan` |  |
| 13 | 0x2C | u16 | `rate_vslocal_clan_total` |  |
| 14 | 0x2E | u8 | `cnt_kill` |  |
| 15 | 0x2F | u8 | `cnt_death` |  |
| 16 | 0x30 | u8 | `cnt_assist` |  |
| 17 | 0x31 | u8 | `cnt_resurrect` |  |
| 18 | 0x32 | u16 | `cnt_search` |  |
| 19 | 0x34 | u32 | `cnt_repair` |  |
| 20 | 0x38 | s8 | `openable_num_win_bonus` |  |
| 21 | 0x39 | s8 | `openable_num_member_bonus` |  |
| 22 | 0x3A | s8 | `openable_num_bc_bonus` |  |
| 23 | 0x3B | s8 | `openable_num_event_bonus` |  |
| 24 | 0x3C | u16 | `expup_campaign` |  |
| 25 | 0x3E | u16 | `expup_bc` |  |
| 26 | 0x40 | u16 | `expup_fgauge` |  |
| 27 | 0x42 | u16 | `moneyup_campaign` |  |
| 28 | 0x44 | u16 | `moneyup_bc` |  |
| 29 | 0x46 | u16 | `moneyup_event` |  |
| 30 | 0x48 | u16 | `moneyup_win` |  |
| 31 | 0x4A | u16 | `accumpup_event` |  |
| 32 | 0x4C | s8 | `buffnum` |  |
| 33 | 0x4D | s8 | `result_spbits` |  |
| 34 | 0x4E | s8 | `enemy_avg_lv` |  |
| 35 | 0x50 | u16 | `enemy_avg_rate` |  |
| 36 | 0x54 | u32 | `avg_lv_diff` |  |
| 37 | 0x58 | s8 | `overplay_rate` |  |
| 38 | 0x7C | s8 | `itm_num` |  |
| 39 | 0xB8 | s8 | `use_buffitem_num` |  |
| 40 | 0x188 | s8 | `fight_ms_num` |  |
| 41 | 0x1B8 | s8 | `no_fight_ms_num` |  |
| 42 | 0x1D8 | s8 | `badge_score` |  |
| 43 | 0x1D9 | s8 | `badge_result` |  |
| 44 | 0x1DA | s8 | `badge_rankmember` |  |
| 45 | 0x1DB | s8 | `badge_deadcnt` |  |
| 46 | 0x1DC | s8 | `badge_cleartime` |  |
| 47 | 0x1DD | s8 | `badge_cmdr` |  |
| 48 | 0x1DE | s8 | `badge_cmdr2` |  |
| 49 | 0x1E0 | u32 | `team_pilot_rate_adjusted_level` |  |
| 50 | 0x1E4 | u32 | `contribute_rank` |  |
| 51 | 0x1E8 | s8 | `dtf_score_rate` |  |
| 52 | 0x1E9 | s8 | `conquer_rate` |  |
| 53 | 0x1EC | u32 | `elapsed_sec` |  |
| 54 | 0x1F0 | u32 | `accump_inc` |  |
| 55 | 0x234 | u16 | `bef_cupteam_rate` |  |
| 56 | 0x236 | u16 | `cupteam_rate_delta` |  |
| 57 | 0x238 | u16 | `enemy_cupteam_rate` |  |
| 58 | 0x23C | u32 | `rokaku_pt` |  |
| 59 | 0x240 | u32 | `rokaku_pt_reason` |  |
| 60 | 0x244 | u32 | `examination_playsec_elapsed` |  |
| 61 | 0x248 | u32 | `examination_playscore` |  |
| 62 | 0x24C | u32 | `special_contributed_point` |  |
| 63 | 0x250 | s8 | `is_periodpath` |  |

## `0xb4b240`（2495 字节，61 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rec_point` |  |
| 2 | 0x4 | u32 | `kill_cnt` |  |
| 3 | 0x8 | u32 | `kill_wrestle_cnt` |  |
| 4 | 0xC | u32 | `kill_shot_cnt` |  |
| 5 | 0x10 | u32 | `kill_cannon_cnt` |  |
| 6 | 0x14 | u32 | `kill_throw_cnt` |  |
| 7 | 0x18 | u32 | `kill_deparms_cnt` |  |
| 8 | 0x1C | u32 | `kill_assist_cnt` |  |
| 9 | 0x20 | u32 | `mapobj_killcnt` |  |
| 10 | 0x24 | u32 | `battery_killcnt` |  |
| 11 | 0x28 | u32 | `stronghold_killcnt` |  |
| 12 | 0x2C | u32 | `death_cnt` |  |
| 13 | 0x30 | u32 | `search_cnt` |  |
| 14 | 0x34 | u32 | `resurrect_cnt` |  |
| 15 | 0x38 | u32 | `respawn_defeat_cnt` |  |
| 16 | 0x3C | u32 | `respawn_conquer_cnt` |  |
| 17 | 0x40 | u32 | `container_cnt` |  |
| 18 | 0x44 | u32 | `protect_cnt` |  |
| 19 | 0x48 | u32 | `stgarms_set_cnt` |  |
| 20 | 0x4C | u32 | `odrcomp_pl_cnt` |  |
| 21 | 0x50 | u32 | `move_length` |  |
| 22 | 0x54 | u32 | `stgarms_move_length` |  |
| 23 | 0x58 | u32 | `repair_armor` |  |
| 24 | 0x5C | u32 | `stghold_damage` |  |
| 25 | 0x60 | u32 | `btlship_damage` |  |
| 26 | 0x64 | u32 | `tender_damage` |  |
| 27 | 0x68 | u32 | `ace_damage` |  |
| 28 | 0x6C | u32 | `result_gold` |  |
| 29 | 0x70 | u32 | `result_gold_score` |  |
| 30 | 0x74 | u32 | `result_gold_rank` |  |
| 31 | 0x78 | u32 | `result_gold_dss` |  |
| 32 | 0x7C | u32 | `result_gold_conquer` |  |
| 33 | 0x80 | u32 | `score_atk` |  |
| 34 | 0x84 | u32 | `score_spt` |  |
| 35 | 0x88 | u32 | `score_con` |  |
| 36 | 0x8C | u32 | `score_total` |  |
| 37 | 0x90 | u32 | `score_atk_max` |  |
| 38 | 0x94 | u32 | `score_spt_max` |  |
| 39 | 0x98 | u32 | `score_con_max` |  |
| 40 | 0x9C | u32 | `vsl_kill_cnt` |  |
| 41 | 0xA0 | u32 | `vsl_kill_wrestle_cnt` |  |
| 42 | 0xA4 | u32 | `vsl_kill_shot_cnt` |  |
| 43 | 0xA8 | u32 | `vsl_kill_cannon_cnt` |  |
| 44 | 0xAC | u32 | `vsl_kill_throw_cnt` |  |
| 45 | 0xB0 | u32 | `vsl_kill_deparms_cnt` |  |
| 46 | 0xB4 | u32 | `vsl_kill_assist_cnt` |  |
| 47 | 0xB8 | u32 | `vsl_death_cnt` |  |
| 48 | 0xBC | u32 | `vsl_search_cnt` |  |
| 49 | 0xC0 | u32 | `vsl_repair_armor` |  |
| 50 | 0xC4 | u32 | `vsl_resurrect_cnt` |  |
| 51 | 0xC8 | u32 | `vsl_td_kill_cnt` |  |
| 52 | 0xCC | u32 | `vsl_td_death_cnt` |  |
| 53 | 0xD0 | u16 | `vsl_td_score_best` |  |
| 54 | 0xD4 | u32 | `vsl_td_score_total` |  |
| 55 | 0xD8 | u32 | `dc_victory` |  |
| 56 | 0xDC | u32 | `dc_kill_cnt` |  |
| 57 | 0xE0 | u32 | `dc_death_cnt` |  |
| 58 | 0xE4 | u32 | `ms_develop_cnt` |  |
| 59 | 0xE8 | u32 | `ms_buildup_cnt` |  |
| 60 | 0xEC | u32 | `weapon_unlock_cnt` |  |
| 61 | 0xF0 | u32 | `weapon_buildup_cnt` |  |

## `0xb48c10`（2415 字节，58 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x20 | u32 | `last_in` |  |
| 4 | 0x24 | s8 | `troops` |  |
| 5 | 0x25 | s8 | `level` |  |
| 6 | 0x26 | s8 | `mil_class` |  |
| 7 | 0x28 | u16 | `byword` |  |
| 8 | 0x28 | u16 | `avatar` |  |
| 9 | 0x44 | u32 | `cmdr_fame` |  |
| 10 | 0x48 | u16 | `rate_vslocal` |  |
| 11 | 0x4A | u16 | `rate_vslocal_4ev` |  |
| 12 | 0x4C | u16 | `rate_vslocal_clan` |  |
| 13 | 0x50 | u32 | `rec_vs` |  |
| 14 | 0x54 | u32 | `rec_vs_win` |  |
| 15 | 0x58 | u32 | `rec_vs_lose` |  |
| 16 | 0x5C | u32 | `rec_vsl_td` |  |
| 17 | 0x60 | u32 | `rec_vsl_td_win` |  |
| 18 | 0x64 | u32 | `rec_vsl_td_lose` |  |
| 19 | 0x68 | u32 | `rec_xwar` |  |
| 20 | 0x6C | u32 | `rec_xwar_win` |  |
| 21 | 0x70 | u32 | `rec_xwar_lose` |  |
| 22 | 0x74 | u32 | `rec_xwar_last1` |  |
| 23 | 0x78 | u32 | `rec_xwar_win_last1` |  |
| 24 | 0x7C | u32 | `rec_xwar_lose_last1` |  |
| 25 | 0x80 | u32 | `rec_xwar_win_term` |  |
| 26 | 0x84 | u32 | `rec_xwar_win_term_last1` |  |
| 27 | 0x88 | u32 | `rec_cmd` |  |
| 28 | 0x8C | u32 | `rec_cmd_win` |  |
| 29 | 0x90 | u32 | `rec_cmd_lose` |  |
| 30 | 0x94 | u32 | `rec_cmd_last1` |  |
| 31 | 0x98 | u32 | `rec_cmd_win_last1` |  |
| 32 | 0x9C | u32 | `rec_cmd_lose_last1` |  |
| 33 | 0xA0 | u32 | `rec_dc` |  |
| 34 | 0xA4 | u32 | `rec_dc_win` |  |
| 35 | 0xA8 | u32 | `rec_dc_lose` |  |
| 36 | 0xAC | u32 | `score_assault_a` |  |
| 37 | 0xB0 | u32 | `score_assault_b` |  |
| 38 | 0xB4 | u32 | `score_snipe` |  |
| 39 | 0xB8 | u32 | `score_cannon` |  |
| 40 | 0xBC | u32 | `score_support` |  |
| 41 | 0xBC | u32 | `comment` |  |
| 42 | 0x134 | u32 | `clan_id` |  |
| 43 | 0x134 | u32 | `clan_name` |  |
| 44 | 0x157 | s8 | `clan_emb_base` |  |
| 45 | 0x158 | s8 | `clan_emb_parts1` |  |
| 46 | 0x159 | s8 | `clan_emb_parts2` |  |
| 47 | 0x15C | u32 | `clan_memb_exp` |  |
| 48 | 0x160 | u32 | `cupteam_id` |  |
| 49 | 0x160 | u32 | `cupteam_name` |  |
| 50 | 0x183 | s8 | `channel_id` |  |
| 51 | 0x184 | u8 | `state_bits` |  |
| 52 | 0x188 | u32 | `accum_point` |  |
| 53 | 0x18C | u32 | `rank` |  |
| 54 | 0x190 | u32 | `base_accump` |  |
| 55 | 0x194 | u32 | `req_accump` |  |
| 56 | 0x198 | u32 | `level_point` |  |
| 57 | 0x19C | s8 | `capture_bonus_state` |  |
| 58 | 0x1A0 | u32 | `capture_bonus_limit` |  |

## `0xb48010`（3058 字节，45 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x4 | u32 | `money` |  |
| 2 | 0x8 | u32 | `clan_id` |  |
| 3 | 0xC | u32 | `clan_memb_exp` |  |
| 4 | 0x10 | u32 | `clan_forbidden` |  |
| 5 | 0x14 | u32 | `cupteam_id` |  |
| 6 | 0x18 | u16 | `deckcost` |  |
| 7 | 0x1C | u32 | `last_battle` |  |
| 8 | 0x20 | u32 | `cw_chscore` |  |
| 9 | 0x24 | u32 | `score_special_a` |  |
| 10 | 0x28 | u32 | `last_play_bonus` |  |
| 11 | 0x2C | u32 | `last_play_bonus_vsl` |  |
| 12 | 0x30 | u16 | `last_play_bonus_vsl_cnt` |  |
| 13 | 0x34 | u32 | `last_dormant_ret_cc` |  |
| 14 | 0x38 | u32 | `capture_bonus_state` |  |
| 15 | 0x3C | u32 | `capture_bonus_limit` |  |
| 16 | 0x40 | u32 | `clan_rokaku_btime_limit` |  |
| 17 | 0x40 | u32 | `comment` |  |
| 18 | 0x0 | u32 | `examination_state` |  |
| 19 | 0x900 | u32 | `rokaku_uniq_msid` |  |
| 20 | 0x908 | u32 | `rokaku_space_uniq_msid` |  |
| 21 | 0x910 | u32 | `rokaku_pt` |  |
| 22 | 0x914 | u32 | `rokaku_pt_use` |  |
| 23 | 0x914 | u32 | `cshist` |  |
| 24 | 0xA18 | s8 | `second_chance_free` |  |
| 25 | 0xA1C | u32 | `second_chance_free_upd` |  |
| 26 | 0xA20 | u32 | `module_id` |  |
| 27 | 0xA24 | u32 | `count` |  |
| 28 | 0x0 | u32 | `module_id` | 是 |
| 29 | 0x4 | u32 | `count` | 是 |
| 30 | 0xE20 | u32 | `dc_point` |  |
| 31 | 0xD8D0 | u32 | `heroms_uniqid` |  |
| 32 | 0xD8D8 | u32 | `last_period_bonus` |  |
| 33 | 0xD8DC | u32 | `daily_battle_bonus_flg` |  |
| 34 | 0xD8E0 | u32 | `last_daily_battle_bonus` |  |
| 35 | 0xD8E4 | u32 | `check_progress_quest_id` |  |
| 36 | 0xD8EC | u32 | `pilot_made_timestamp` |  |
| 37 | 0xD8F0 | u16 | `newpilot_challenge_nextindex` |  |
| 38 | 0xD8F4 | u32 | `newpilot_challenge_last` |  |
| 39 | 0xD936 | u16 | `sc_lv_max` |  |
| 40 | 0xD938 | u32 | `last_pilot_channel_in` |  |
| 41 | 0xD93C | u16 | `monthly_bonus_holding_id` |  |
| 42 | 0xD93E | u16 | `monthly_bonus_logincnt` |  |
| 43 | 0xD940 | u16 | `monthly_bonus_xwarcnt` |  |
| 44 | 0xD944 | u32 | `periodpath_end` |  |
| 45 | 0xD944 | u32 | `beginner_challenge_info` |  |

## `0xb09240`（2499 字节，31 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `uniqid` |  |
| 2 | 0x8 | u32 | `msma_id` |  |
| 3 | 0xC | u32 | `crew_msma_id` |  |
| 4 | 0x10 | u32 | `decal` |  |
| 5 | 0x14 | s8 | `color` |  |
| 6 | 0x15 | s8 | `deck_index` |  |
| 7 | 0x18 | u32 | `cost` |  |
| 8 | 0x1C | s8 | `is_costover` |  |
| 9 | 0x20 | u32 | `energy_now` |  |
| 10 | 0x24 | u16 | `weight_balance` |  |
| 11 | 0x26 | u16 | `shield_weight` |  |
| 12 | 0x28 | u32 | `sp_parts` |  |
| 13 | 0x2C | u16 | `armor_up` |  |
| 14 | 0x2E | u16 | `warp_up` |  |
| 15 | 0x30 | u16 | `boost_offset` |  |
| 16 | 0x32 | u16 | `boost_offset_ns` |  |
| 17 | 0x34 | u16 | `over_custom_armor` |  |
| 18 | 0x36 | u16 | `over_custom_warp` |  |
| 19 | 0x38 | u16 | `over_custom_level` |  |
| 20 | 0x48 | u32 | `sitem_id` |  |
| 21 | 0x4C | u32 | `spitem_id` |  |
| 22 | 0xEC | s8 | `is_exdeck` |  |
| 23 | 0xED | s8 | `is_rokaku` |  |
| 24 | 0xF0 | u32 | `rokakums_limit_use` |  |
| 25 | 0xF4 | u16 | `respawn_wait_sec` |  |
| 26 | 0xF6 | u16 | `respawn_wait_max` |  |
| 27 | 0x100 | s8 | `is_reduce_respawn_wait` |  |
| 28 | 0x101 | s8 | `is_extrule_invalid` |  |
| 29 | 0x102 | s8 | `is_heroms` |  |
| 30 | 0x102 | s8 | `additional_info` |  |
| 31 | 0x104 | u32 | `level_gauge_now_level` |  |

## `0xb0b9e0`（1235 字节，29 字段）← 调用者: sub_B351D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `move_spd` |  |
| 2 | 0x2 | u16 | `boost_gauge` |  |
| 3 | 0x4 | u16 | `boost_recov` |  |
| 4 | 0x6 | u16 | `boost_consume` |  |
| 5 | 0x8 | s8 | `clcheck_result` |  |
| 6 | 0xC | u32 | `weapon_itemid` |  |
| 7 | 0x10 | u32 | `weapon_cooltime` |  |
| 8 | 0x14 | u32 | `weapon_rapidtime` |  |
| 9 | 0x18 | u32 | `weapon_reload` |  |
| 10 | 0x1C | u8 | `debugger_found` |  |
| 11 | 0x1D | u8 | `proc_ref_count` |  |
| 12 | 0x1E | u8 | `reserved1` |  |
| 13 | 0x1F | u8 | `reserved2` |  |
| 14 | 0x20 | u32 | `weapon_bullet_speed` |  |
| 15 | 0x24 | u16 | `weapon_range` |  |
| 16 | 0x26 | u16 | `weapon_charge_time` |  |
| 17 | 0x28 | u16 | `weapon_bullet_mgz` |  |
| 18 | 0x2A | u16 | `weapon_bullet_all` |  |
| 19 | 0x2C | u16 | `weapon_batch_fire` |  |
| 20 | 0x30 | u32 | `weapon_fired` |  |
| 21 | 0x34 | u16 | `wrestle_size` |  |
| 22 | 0x36 | u8 | `wrestle_hack_check_ex` |  |
| 23 | 0x3C | u8 | `ai_num` |  |
| 24 | 0x3C | u8 | `perf_pre_chara` |  |
| 25 | ? | ? | `perf_chara` |  |
| 26 | ? | ? | `perf_ai` |  |
| 27 | ? | ? | `perf_last` |  |
| 28 | ? | ? | `perf_if` |  |
| 29 | ? | ? | `perf_rdr` |  |

## `0xb49de0`（1950 字节，27 字段）← 调用者: sub_B4A6D0, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `uniqid` |  |
| 2 | 0x8 | u32 | `msma_id` |  |
| 3 | 0xC | u32 | `tm_sec` |  |
| 4 | 0x10 | u32 | `tm_usec` |  |
| 5 | 0x14 | u32 | `rental_time_limit` |  |
| 6 | 0x14 | u32 | `nickname` |  |
| 7 | 0x58 | u32 | `energy_now` |  |
| 8 | 0x5C | u32 | `decal` |  |
| 9 | 0x60 | s8 | `color` |  |
| 10 | 0x60 | s8 | `deckslot` |  |
| 11 | ? | ? | `is_costover` |  |
| 12 | 0x68 | u32 | `cost` |  |
| 13 | 0x6C | u32 | `mission_cost` |  |
| 14 | 0x7C | u32 | `eqshield_itemid` |  |
| 15 | 0x80 | u32 | `eqspecial_itemid` |  |
| 16 | 0xC0 | u32 | `sp_parts` |  |
| 17 | 0xC4 | u32 | `sp_parts_exp` |  |
| 18 | 0xC8 | u16 | `buildup_cnt` |  |
| 19 | 0xE6 | u16 | `weapon_buildup_extra_cnt` |  |
| 20 | 0xE8 | u32 | `over_custom_exp` |  |
| 21 | 0xEC | u32 | `over_custom_level` |  |
| 22 | 0xF0 | u32 | `over_custom_buildup_cnt` |  |
| 23 | 0x12C | u16 | `msbits` |  |
| 24 | 0x130 | u32 | `unlocked_colors` |  |
| 25 | 0x134 | s8 | `spticket_success_ms` |  |
| 26 | 0x135 | s8 | `spticket_greatest_ms` |  |
| 27 | 0x136 | s8 | `is_favorite` |  |

## `0xb09c10`（1411 字节，26 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `type` |  |
| 2 | 0x0 | s8 | `name` |  |
| 3 | 0x24 | u32 | `param_id` |  |
| 4 | 0x28 | s8 | `action_type` |  |
| 5 | 0x2A | u16 | `move_spd` |  |
| 6 | 0x7C | u16 | `pop_init_x` |  |
| 7 | 0x7E | u16 | `pop_init_y` |  |
| 8 | 0x80 | u16 | `pop_init_z` |  |
| 9 | 0x82 | u16 | `pop_init_dir` |  |
| 10 | 0x84 | u16 | `fire_start_x` |  |
| 11 | 0x86 | u16 | `fire_start_y` |  |
| 12 | 0x88 | u16 | `fire_start_z` |  |
| 13 | 0x8A | u16 | `fire_end_x` |  |
| 14 | 0x8C | u16 | `fire_end_y` |  |
| 15 | 0x8E | u16 | `fire_end_z` |  |
| 16 | 0x90 | u16 | `move_end_x` |  |
| 17 | 0x92 | u16 | `move_end_y` |  |
| 18 | 0x94 | u16 | `move_end_z` |  |
| 19 | 0x96 | u16 | `order_kind` |  |
| 20 | 0x98 | u32 | `order_param` |  |
| 21 | 0x9C | u32 | `group_id` |  |
| 22 | 0xA0 | u16 | `center_ms_entid` |  |
| 23 | 0xA2 | u16 | `route_number` |  |
| 24 | 0xA4 | u16 | `formation_id` |  |
| 25 | 0xA6 | s8 | `formation_number` |  |
| 26 | 0xA7 | s8 | `stuck_escape` |  |

## `0xb08ad0`（997 字节，24 字段）← 调用者: sub_B0CC20, sub_B51930, sub_B8A100

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x1D | s8 | `troops` |  |
| 4 | 0x1E | s8 | `level` |  |
| 5 | 0x1F | s8 | `mil_class` |  |
| 6 | 0x20 | u16 | `byword` |  |
| 7 | 0x24 | u32 | `cmdr_fame` |  |
| 8 | 0x28 | u16 | `rate_vslocal` |  |
| 9 | 0x2A | u16 | `rate_vslocal_4ev` |  |
| 10 | 0x2C | u16 | `rate_vslocal_clan` |  |
| 11 | 0x30 | u32 | `level_point` |  |
| 12 | 0x30 | u32 | `avatar` |  |
| 13 | 0x4C | u32 | `clan_id` |  |
| 14 | 0x4C | u32 | `clan_name` |  |
| 15 | 0x6F | s8 | `clan_emb_base` |  |
| 16 | 0x70 | s8 | `clan_emb_parts1` |  |
| 17 | 0x71 | s8 | `clan_emb_parts2` |  |
| 18 | 0x74 | u32 | `cupteam_id` |  |
| 19 | 0x74 | u32 | `cupteam_name` |  |
| 20 | 0x98 | u32 | `accum_point` |  |
| 21 | 0x9C | u32 | `rank` |  |
| 22 | 0xA0 | u32 | `base_accump` |  |
| 23 | 0xA4 | u32 | `req_accump` |  |
| 24 | 0xA8 | u32 | `penalty` |  |

## `0xb4e240`（1087 字节，23 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `clan_id` |  |
| 2 | 0x4 | s8 | `troops` |  |
| 3 | 0x8 | u32 | `npc_id` |  |
| 4 | 0xC | u32 | `npc_id2` |  |
| 5 | 0xC | u32 | `clan_name` |  |
| 6 | 0x2F | s8 | `level` |  |
| 7 | 0x34 | s8 | `emb_base` |  |
| 8 | 0x35 | s8 | `emb_parts1` |  |
| 9 | 0x36 | s8 | `emb_parts2` |  |
| 10 | 0x38 | u16 | `member_num` |  |
| 11 | 0x3A | u16 | `member_max` |  |
| 12 | 0x3C | u32 | `leader_id` |  |
| 13 | 0x40 | u32 | `vs_win` |  |
| 14 | 0x44 | u32 | `vs_lose` |  |
| 15 | 0x48 | u32 | `rank` |  |
| 16 | 0x4C | u32 | `rank_score` |  |
| 17 | 0x50 | u32 | `rank_rate_vsl` |  |
| 18 | 0x54 | u32 | `rate_vsl_score` |  |
| 19 | 0x58 | s8 | `offer_is_active` |  |
| 20 | 0x58 | s8 | `notice_body` |  |
| 21 | 0x20C | u32 | `active_time_bits` |  |
| 22 | 0x210 | s8 | `play_style` |  |
| 23 | 0x214 | u32 | `capture_unlock_num` |  |

## `0xb0aea0`（985 字节，21 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `type` |  |
| 2 | 0x1 | s8 | `stat` |  |
| 3 | 0x2 | u16 | `ent_id` |  |
| 4 | 0x4 | u32 | `gauge_max` |  |
| 5 | 0x8 | u32 | `msma_id` |  |
| 6 | 0xC | u32 | `msma_id2` |  |
| 7 | 0x10 | u16 | `pos_x` |  |
| 8 | 0x12 | u16 | `pos_y` |  |
| 9 | 0x14 | u16 | `pos_z` |  |
| 10 | 0x18 | u16 | `pos2_x` |  |
| 11 | 0x1A | u16 | `pos2_y` |  |
| 12 | 0x1C | u16 | `pos2_z` |  |
| 13 | 0x22 | u16 | `ctrl_count` |  |
| 14 | 0x24 | u16 | `route_number` |  |
| 15 | 0x26 | u16 | `route_initial_index` |  |
| 16 | 0x28 | u16 | `move_speed` |  |
| 17 | 0x2A | u16 | `rot_speed` |  |
| 18 | 0x2C | u16 | `door_auto_sensor_height` |  |
| 19 | 0x2E | u16 | `door_auto_sensor_radius` |  |
| 20 | 0x30 | u16 | `attach_barrier_npc_ent_id` |  |
| 21 | 0x32 | u16 | `local_ctrl_id` |  |

## `0xb372d0`（1813 字节，21 字段）← 调用者: sub_B01F00

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `launch_x` |  |
| 3 | ? | ? | `launch_y` |  |
| 4 | ? | ? | `launch_z` |  |
| 5 | ? | ? | `target1_x` |  |
| 6 | ? | ? | `target1_y` |  |
| 7 | ? | ? | `target1_z` |  |
| 8 | ? | ? | `target2_x` |  |
| 9 | ? | ? | `target2_y` |  |
| 10 | ? | ? | `target2_z` |  |
| 11 | ? | ? | `target_ent_id` |  |
| 12 | ? | ? | `msec` |  |
| 13 | ? | ? | `shot0_impact1` |  |
| 14 | ? | ? | `fx_opt` |  |
| 15 | ? | ? | `impact_grenade_id` |  |
| 16 | ? | ? | `parent_grenade_id` |  |
| 17 | ? | ? | `charge_lv` |  |
| 18 | ? | ? | `ent_id` |  |
| 19 | ? | ? | `impact_wall` |  |
| 20 | ? | ? | `salvo_slot` |  |
| 21 | ? | ? | `action` |  |

## `0xb0a260`（867 字节，20 字段）← 调用者: sub_B0B4B0, sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `ent_id` |  |
| 2 | 0x2 | u16 | `pos_x` |  |
| 3 | 0x4 | u16 | `pos_y` |  |
| 4 | 0x6 | u16 | `pos_z` |  |
| 5 | 0xA | u16 | `target_x` |  |
| 6 | 0xC | u16 | `target_y` |  |
| 7 | 0xE | u16 | `target_z` |  |
| 8 | 0x10 | u16 | `score1` |  |
| 9 | 0x12 | u16 | `score2` |  |
| 10 | 0x14 | u16 | `score3` |  |
| 11 | 0x16 | s8 | `hp_percent` |  |
| 12 | 0x17 | s8 | `hp_percent_shield` |  |
| 13 | 0x18 | u16 | `down_power` |  |
| 14 | 0x1A | s8 | `equip_index` |  |
| 15 | 0x1B | u8 | `water_index` |  |
| 16 | 0x1C | u8 | `layer_index` |  |
| 17 | 0x1E | u16 | `rideon_ent_id` |  |
| 18 | 0x20 | u16 | `lockon_ent_id` |  |
| 19 | 0x24 | u32 | `special_bits` |  |
| 20 | 0x28 | u16 | `special_bits2` |  |

## `0xb49580`（827 字节，20 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x20 | u32 | `last_in` |  |
| 4 | 0x24 | s8 | `troops` |  |
| 5 | 0x25 | s8 | `level` |  |
| 6 | 0x26 | s8 | `mil_class` |  |
| 7 | 0x28 | u16 | `byword` |  |
| 8 | 0x28 | u16 | `avatar` |  |
| 9 | 0x44 | u32 | `clan_id` |  |
| 10 | 0x44 | u32 | `clan_name` |  |
| 11 | 0x67 | s8 | `clan_emb_base` |  |
| 12 | 0x68 | s8 | `clan_emb_parts1` |  |
| 13 | 0x69 | s8 | `clan_emb_parts2` |  |
| 14 | 0x6C | u32 | `clan_memb_exp` |  |
| 15 | 0x70 | u32 | `clan_memb_exp_use` |  |
| 16 | 0x74 | s8 | `channel_id` |  |
| 17 | 0x75 | s8 | `capture_bonus_state` |  |
| 18 | 0x78 | u32 | `capture_bonus_limit` |  |
| 19 | 0x7C | u32 | `rokaku_pt_use` |  |
| 20 | 0x80 | u8 | `state_bits` |  |

## `0xb351d0`（1967 字节，19 字段）← 调用者: sub_B01B90

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `pos_x` |  |
| 3 | ? | ? | `pos_y` |  |
| 4 | ? | ? | `pos_z` |  |
| 5 | ? | ? | `dir_eye` |  |
| 6 | ? | ? | `target_x` |  |
| 7 | ? | ? | `target_y` |  |
| 8 | ? | ? | `target_z` |  |
| 9 | ? | ? | `spbits` |  |
| 10 | ? | ? | `spbits2` |  |
| 11 | ? | ? | `lockon_ent_id` |  |
| 12 | ? | ? | `in_water_index` |  |
| 13 | ? | ? | `layer_index` |  |
| 14 | ? | ? | `access_ent_id1` |  |
| 15 | ? | ? | `access_ent_id2` |  |
| 16 | ? | ? | `rideon_ent_id` |  |
| 17 | ? | ? | `spot_ent_id` |  |
| 18 | ? | ? | `operate_ent_id` |  |
| 19 | ? | ? | `is_under_water` |  |

## `0xb4c340`（775 字节，19 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x4 | u32 | `world_id` |  |
| 3 | 0x8 | s8 | `is_cmdr` |  |
| 4 | 0x9 | s8 | `is_xbnpc` |  |
| 5 | 0xA | u16 | `rank` |  |
| 6 | 0xC | u32 | `totalpoint` |  |
| 7 | 0x10 | u32 | `stghold_dmg` |  |
| 8 | 0x14 | u16 | `kill_cnt` |  |
| 9 | 0x18 | u32 | `atk_point` |  |
| 10 | 0x1C | u32 | `spt_point` |  |
| 11 | 0x20 | u32 | `con_point` |  |
| 12 | 0x24 | u32 | `victory_score` |  |
| 13 | 0x28 | u32 | `ranking_point` |  |
| 14 | 0x2C | u32 | `last_msma` |  |
| 15 | 0x30 | u32 | `last_weapon` |  |
| 16 | 0x34 | u32 | `last_shield` |  |
| 17 | 0x38 | u32 | `last_decal` |  |
| 18 | 0x3C | s8 | `last_mscolor` |  |
| 19 | 0x3E | u16 | `add_rate_vslocal` |  |

## `0xb47cc0`（732 字节，18 字段）← 调用者: sub_B48010, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x4 | u32 | `favorite_ms_id` |  |
| 3 | 0x8 | s8 | `battle_rule` |  |
| 4 | 0xC | u32 | `favorite_exp_sum` |  |
| 5 | 0x10 | u32 | `kill_cnt` |  |
| 6 | 0x14 | u32 | `kill_assist_cnt` |  |
| 7 | 0x18 | u32 | `resurrect_cnt` |  |
| 8 | 0x1C | u32 | `stghold_damage` |  |
| 9 | 0x20 | u32 | `battle_cnt` |  |
| 10 | 0x24 | u32 | `score_max_atk` |  |
| 11 | 0x28 | u32 | `score_max_spt` |  |
| 12 | 0x2C | u32 | `score_max_con` |  |
| 13 | 0x30 | u32 | `score_sum_atk` |  |
| 14 | 0x34 | u32 | `score_sum_spt` |  |
| 15 | 0x38 | u32 | `score_sum_con` |  |
| 16 | 0x3C | u32 | `score_sum_sum` |  |
| 17 | 0x40 | u32 | `last_update` |  |
| 18 | 0x44 | s8 | `dirty_flag` |  |

## `0xb0b4b0`（699 字节，17 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `team` |  |
| 2 | 0x1 | s8 | `troops` |  |
| 3 | 0x4 | u32 | `world_id` |  |
| 4 | 0x8 | u32 | `pilot_id` |  |
| 5 | 0xC | u32 | `ent_id` |  |
| 6 | 0x10 | u32 | `index` |  |
| 7 | 0x14 | u32 | `msma_id` |  |
| 8 | 0x18 | u32 | `item_id` |  |
| 9 | 0x1C | s8 | `type` |  |
| 10 | 0x20 | u32 | `eff_range` |  |
| 11 | 0x20 | u32 | `snapshot` |  |
| 12 | 0x50 | u32 | `arms_id` |  |
| 13 | 0x54 | u16 | `state_bit` |  |
| 14 | 0x56 | s8 | `is_gmk` |  |
| 15 | 0x57 | s8 | `is_using_ss` |  |
| 16 | 0x58 | u32 | `remain_msec` |  |
| 17 | 0x5C | u32 | `buildup_eff_range` |  |

## `0xb3ad30`（1554 字节，17 字段）← 调用者: sub_B026D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `launch_x` |  |
| 3 | ? | ? | `launch_y` |  |
| 4 | ? | ? | `launch_z` |  |
| 5 | ? | ? | `target1_x` |  |
| 6 | ? | ? | `target1_y` |  |
| 7 | ? | ? | `target1_z` |  |
| 8 | ? | ? | `target2_x` |  |
| 9 | ? | ? | `target2_y` |  |
| 10 | ? | ? | `target2_z` |  |
| 11 | ? | ? | `target_ent_id` |  |
| 12 | ? | ? | `msec` |  |
| 13 | ? | ? | `shot0_impact1` |  |
| 14 | ? | ? | `fx_opt` |  |
| 15 | ? | ? | `impact_grenade_id` |  |
| 16 | ? | ? | `parent_grenade_id` |  |
| 17 | ? | ? | `charge_lv` |  |

## `0xb4fe20`（814 字节，17 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rank` |  |
| 2 | 0x4 | u32 | `score` |  |
| 3 | 0x8 | u32 | `pilot_id` |  |
| 4 | 0x8 | u32 | `name` |  |
| 5 | 0x25 | s8 | `troops` |  |
| 6 | 0x28 | u32 | `world_id` |  |
| 7 | 0x2C | u32 | `season_class_lv` |  |
| 8 | 0x2C | u32 | `tm_upd` |  |
| 9 | 0x2C | u32 | `avatar` |  |
| 10 | 0x98 | u32 | `last_score` |  |
| 11 | 0x9C | u32 | `last_rank` |  |
| 12 | 0x9C | u32 | `clan_name` |  |
| 13 | 0xBF | s8 | `emb_base` |  |
| 14 | 0xC0 | s8 | `emb_parts1` |  |
| 15 | 0xC1 | s8 | `emb_parts2` |  |
| 16 | 0xC2 | s8 | `is_regular` |  |
| 17 | 0xC3 | s8 | `is_reserve` |  |

## `0xb499f0`（652 字节，16 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `main_rate` |  |
| 2 | 0x4 | u32 | `main_priority` |  |
| 3 | 0x8 | u32 | `gp_rate` |  |
| 4 | 0xC | u32 | `reward_rate` |  |
| 5 | 0x10 | u32 | `raredrop_rate` |  |
| 6 | 0x14 | u32 | `accump_rate` |  |
| 7 | 0x18 | u32 | `over_custom_rate` |  |
| 8 | 0x1C | u32 | `gp_offset` |  |
| 9 | 0x20 | u32 | `reward_num` |  |
| 10 | 0x24 | u32 | `accump_offset` |  |
| 11 | 0x28 | u32 | `over_custom_offset` |  |
| 12 | 0x2C | u32 | `buildup_odds_offset` |  |
| 13 | 0x30 | u32 | `bonus_target` |  |
| 14 | 0x34 | u32 | `game_type` |  |
| 15 | 0x38 | u32 | `begin_time` |  |
| 16 | 0x3C | u32 | `end_time` |  |

## `0xb0aa70`（661 字节，15 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `type` |  |
| 2 | 0x4 | u16 | `ini_team` |  |
| 3 | 0x6 | u16 | `ini_troops` |  |
| 4 | 0x6 | u16 | `name` |  |
| 5 | 0x18 | u32 | `gauge_max` |  |
| 6 | 0x1C | u32 | `post_chara_id` |  |
| 7 | 0x20 | u16 | `pos_x` |  |
| 8 | 0x22 | u16 | `pos_y` |  |
| 9 | 0x24 | u16 | `pos_z` |  |
| 10 | 0x28 | s8 | `cmdr_sptype` |  |
| 11 | 0x2C | u32 | `group_id` |  |
| 12 | 0x30 | u32 | `npc_ba_point_ent_id` |  |
| 13 | 0x34 | u32 | `npc_ba_point_move_range_abs_x` |  |
| 14 | 0x38 | u32 | `param1` |  |
| 15 | 0x3C | u32 | `param2` |  |

## `0xb0b770`（623 字节，15 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `wave` |  |
| 2 | 0x1 | s8 | `wave_rank` |  |
| 3 | 0x2 | s8 | `result_coop` |  |
| 4 | 0x4 | u32 | `cleartime_sec` |  |
| 5 | 0x8 | s8 | `cleartime_rank` |  |
| 6 | 0xC | u32 | `cleartime_score` |  |
| 7 | 0x10 | u16 | `container_num` |  |
| 8 | 0x12 | u16 | `container_max` |  |
| 9 | 0x14 | s8 | `container_rank` |  |
| 10 | 0x18 | u32 | `container_score` |  |
| 11 | 0x1C | u16 | `enemybase_num` |  |
| 12 | 0x1E | u16 | `enemybase_max` |  |
| 13 | 0x20 | s8 | `enemybase_rank` |  |
| 14 | 0x24 | u32 | `enemybase_score` |  |
| 15 | 0x28 | u32 | `total_score` |  |

## `0xb4c0d0`（620 字节，15 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `room_id` |  |
| 2 | 0x0 | u32 | `room_name` |  |
| 3 | 0x50 | u32 | `room_type` |  |
| 4 | 0x54 | s8 | `room_stat` |  |
| 5 | 0x58 | u32 | `play_elapsed` |  |
| 6 | 0x5C | u32 | `mission_id` |  |
| 7 | 0x60 | u32 | `extrule_id` |  |
| 8 | 0x64 | s8 | `is_lock` |  |
| 9 | 0x65 | s8 | `is_vsclan` |  |
| 10 | 0x66 | u16 | `count_eff` |  |
| 11 | 0x68 | u16 | `count_zeon` |  |
| 12 | 0x6A | u16 | `count_max` |  |
| 13 | 0x6C | u32 | `master_pilotid` |  |
| 14 | 0x70 | u32 | `master_worldid` |  |
| 15 | 0x70 | u32 | `master_name` |  |

## `0xb4e680`（626 字节，15 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `clan_id` |  |
| 2 | 0x4 | s8 | `emb_base` |  |
| 3 | 0x5 | s8 | `emb_parts1` |  |
| 4 | 0x6 | s8 | `emb_parts2` |  |
| 5 | 0x6 | s8 | `clan_name` |  |
| 6 | 0x26 | s8 | `level` |  |
| 7 | 0x26 | s8 | `offer_body` |  |
| 8 | ? | ? | `leader_name` |  |
| 9 | 0x60 | u32 | `member_num` |  |
| 10 | 0x64 | u32 | `member_max` |  |
| 11 | 0x68 | s8 | `offer_is_active` |  |
| 12 | 0x69 | s8 | `clan_kind` |  |
| 13 | 0x6C | u32 | `active_time_bits` |  |
| 14 | 0x70 | s8 | `play_style` |  |
| 15 | 0x74 | u32 | `capture_unlock_num` |  |

## `0xb379f0`（1388 字节，14 字段）← 调用者: sub_B02050

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `launch_x` |  |
| 3 | ? | ? | `launch_y` |  |
| 4 | ? | ? | `launch_z` |  |
| 5 | ? | ? | `target_x` |  |
| 6 | ? | ? | `target_y` |  |
| 7 | ? | ? | `target_z` |  |
| 8 | ? | ? | `target_ent_id` |  |
| 9 | ? | ? | `msec` |  |
| 10 | ? | ? | `shot0_impact1` |  |
| 11 | ? | ? | `fx_opt` |  |
| 12 | ? | ? | `impact_grenade_id` |  |
| 13 | ? | ? | `charge_lv` |  |
| 14 | ? | ? | `salvo_slot` |  |

## `0xb39420`（1389 字节，14 字段）← 调用者: sub_B02570

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `shot_bit_id` |  |
| 3 | ? | ? | `shot_ent_id` |  |
| 4 | ? | ? | `shot_alive` |  |
| 5 | ? | ? | `launch_x` |  |
| 6 | ? | ? | `launch_y` |  |
| 7 | ? | ? | `launch_z` |  |
| 8 | ? | ? | `target_x` |  |
| 9 | ? | ? | `target_y` |  |
| 10 | ? | ? | `target_z` |  |
| 11 | ? | ? | `target_ent_id` |  |
| 12 | ? | ? | `msec` |  |
| 13 | ? | ? | `release0_shot1` |  |
| 14 | ? | ? | `fx_opt` |  |

## `0xb4f3d0`（578 字节，14 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `tree_id` |  |
| 2 | 0x4 | u32 | `node_no` |  |
| 3 | 0x8 | u32 | `idx_no` |  |
| 4 | 0xC | u32 | `unlock` |  |
| 5 | 0x10 | u32 | `pool_pt` |  |
| 6 | 0x14 | u32 | `need_pt_open` |  |
| 7 | 0x18 | u32 | `need_pt_rental` |  |
| 8 | 0x1C | u32 | `lv_min` |  |
| 9 | 0x20 | u32 | `lv_max` |  |
| 10 | 0x24 | u32 | `msma_id` |  |
| 11 | 0x28 | u32 | `uniq_msid` |  |
| 12 | 0x30 | u32 | `limit_use` |  |
| 13 | 0x34 | u32 | `limit_coolup` |  |
| 14 | 0x38 | u32 | `deck_mask` |  |

## `0xb50490`（592 字节，14 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `quest_id` |  |
| 2 | 0x0 | u32 | `title` |  |
| 3 | 0x65 | s8 | `is_event` |  |
| 4 | 0x66 | s8 | `is_known` |  |
| 5 | 0x68 | u16 | `achieve_trigger` |  |
| 6 | 0x6C | u32 | `achieve_denom` |  |
| 7 | 0x70 | u32 | `achieve_num` |  |
| 8 | 0x74 | u32 | `pay_gp` |  |
| 9 | 0x78 | u32 | `pay_exp` |  |
| 10 | 0x7C | u32 | `pay_item_id` |  |
| 11 | 0x80 | u32 | `pay_item_num` |  |
| 12 | 0x84 | u32 | `pay_msma_id` |  |
| 13 | 0x88 | u32 | `pay_byword_id` |  |
| 14 | 0x8C | s8 | `category` |  |

## `0xb4fb00`（543 字节，13 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rank` |  |
| 2 | 0x4 | u32 | `clan_id` |  |
| 3 | 0x4 | u32 | `clan_name` |  |
| 4 | 0x27 | s8 | `troops` |  |
| 5 | 0x28 | u32 | `clan_lv` |  |
| 6 | 0x2C | u32 | `leader_pilot_id` |  |
| 7 | 0x2C | u32 | `leader_pilot_name` |  |
| 8 | 0x49 | s8 | `leader_level` |  |
| 9 | 0x4A | s8 | `emb_base` |  |
| 10 | 0x4B | s8 | `emb_parts1` |  |
| 11 | 0x4C | s8 | `emb_parts2` |  |
| 12 | 0x50 | u32 | `score` |  |
| 13 | 0x50 | u32 | `avatar` |  |

## `0xb47660`（568 字节，12 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `pilot_name` |  |
| 3 | 0x1D | s8 | `level` |  |
| 4 | 0x1E | s8 | `is_admin` |  |
| 5 | 0x20 | u32 | `send_range` |  |
| 6 | 0x20 | u32 | `timestamp` |  |
| 7 | ? | ? | `avatar` |  |
| 8 | 0x148 | u32 | `clan_id` |  |
| 9 | 0x148 | u32 | `clan_name` |  |
| 10 | 0x16B | s8 | `clan_emb_base` |  |
| 11 | 0x16C | s8 | `clan_emb_parts1` |  |
| 12 | 0x16D | s8 | `clan_emb_parts2` |  |

## `0xb4f180`（507 字节，12 字段）← 调用者: sub_B51930, sub_BA1A20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `filter_type` |  |
| 2 | 0x2 | u8 | `lv_under` |  |
| 3 | 0x3 | u8 | `lv_upper` |  |
| 4 | 0x4 | u8 | `member_under` |  |
| 5 | 0x5 | u8 | `member_upper` |  |
| 6 | 0x6 | u8 | `rokaku_under` |  |
| 7 | 0x7 | u8 | `rokaku_upper` |  |
| 8 | 0x8 | u16 | `ranking_under` |  |
| 9 | 0xA | u16 | `ranking_upper` |  |
| 10 | 0xC | s8 | `recruit_value` |  |
| 11 | 0x10 | u32 | `time_value` |  |
| 12 | 0x14 | u8 | `style_value` |  |

## `0xb4f890`（504 字节，12 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rank` |  |
| 2 | 0x4 | u32 | `pilot_id` |  |
| 3 | 0x4 | u32 | `name` |  |
| 4 | 0x21 | s8 | `troops` |  |
| 5 | 0x22 | s8 | `level` |  |
| 6 | 0x24 | u32 | `clan_id` |  |
| 7 | 0x24 | u32 | `clan_name` |  |
| 8 | 0x47 | s8 | `emb_base` |  |
| 9 | 0x48 | s8 | `emb_parts1` |  |
| 10 | 0x49 | s8 | `emb_parts2` |  |
| 11 | 0x4C | u32 | `score` |  |
| 12 | 0x4C | u32 | `avatar` |  |

## `0xb03d30`（3890 字节，11 字段）← 调用者: 0x162d078, 0xeed768

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `result` |  |
| 2 | 0x0 | u32 | `last_world` |  |
| 3 | 0x0 | u32 | `result` |  |
| 4 | 0x0 | u32 | `loungesv_port` |  |
| 5 | 0x0 | u32 | `userid` |  |
| 6 | 0x0 | u32 | `reset_sec` |  |
| 7 | 0x0 | u32 | `otp_type` |  |
| 8 | 0x0 | u32 | `result` |  |
| 9 | 0x0 | u32 | `version` |  |
| 10 | 0x0 | u32 | `gentime` | 是 |
| 11 | 0x0 | u32 | `result` |  |

## `0xb50840`（460 字节，11 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `phase` |  |
| 2 | 0x4 | u32 | `round` |  |
| 3 | 0x8 | u32 | `mission_id` |  |
| 4 | 0xC | u32 | `bracket_id` |  |
| 5 | 0xC | u32 | `bracket_name` |  |
| 6 | 0x1C | u32 | `winners_bracket_id` |  |
| 7 | 0x20 | u32 | `losers_bracket_id` |  |
| 8 | 0x24 | u32 | `open_time` |  |
| 9 | 0x28 | u32 | `close_time` |  |
| 10 | 0x2C | u32 | `cupteam_id_a` |  |
| 11 | 0x30 | u32 | `cupteam_id_b` |  |

## `0xb50a10`（697 字节，11 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `state` |  |
| 2 | 0x4 | u32 | `tournament_id` |  |
| 3 | 0x8 | u32 | `mode` |  |
| 4 | 0xC | u32 | `open_date` |  |
| 5 | 0x10 | u32 | `team_num` |  |
| 6 | 0x14 | u16 | `bracket_num` |  |
| 7 | 0x16 | u16 | `bracket_max` |  |
| 8 | 0x18 | u32 | `booking_start` |  |
| 9 | 0x1C | u32 | `booking_end` |  |
| 10 | 0x40 | u32 | `matching_extrule` |  |
| 11 | 0x44 | u32 | `extrule_id` |  |

## `0xb08920`（426 字节，10 字段）← 调用者: sub_B08AD0, sub_B47660, sub_B48C10, sub_B49580, sub_B498C0, sub_B4D9D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `avatar_id` |  |
| 2 | 0x4 | s8 | `gender` |  |
| 3 | 0x5 | u8 | `face` |  |
| 4 | 0x6 | u8 | `skincolor` |  |
| 5 | 0x8 | u16 | `clothes` |  |
| 6 | 0xC | u32 | `hair` |  |
| 7 | 0x10 | u8 | `accessory` |  |
| 8 | 0x11 | u8 | `frame` |  |
| 9 | 0x12 | u8 | `voice` |  |
| 10 | 0x14 | u16 | `byword` |  |

## `0xb0c020`（460 字节，10 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `team` |  |
| 2 | 0x2 | u16 | `troops` |  |
| 3 | 0x4 | u32 | `type` |  |
| 4 | 0x8 | u32 | `stat` |  |
| 5 | 0xC | s8 | `is_lock` |  |
| 6 | 0x10 | u32 | `pos_x` |  |
| 7 | 0x14 | u32 | `pos_y` |  |
| 8 | 0x18 | u32 | `pos_z` |  |
| 9 | 0x20 | u32 | `route_no` |  |
| 10 | 0x3C | u32 | `ai_priority` |  |

## `0xb38670`（1104 字节，10 字段）← 调用者: sub_B022A0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `target_ent_id` |  |
| 6 | ? | ? | `state` |  |
| 7 | ? | ? | `fx_opt` |  |
| 8 | ? | ? | `impact_arms_id` |  |
| 9 | ? | ? | `is_gmk` |  |
| 10 | ? | ? | `index` |  |

## `0xb3b350`（1100 字节，10 字段）← 调用者: sub_B02800

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `itemid` |  |
| 3 | ? | ? | `launch_x` |  |
| 4 | ? | ? | `launch_y` |  |
| 5 | ? | ? | `launch_z` |  |
| 6 | ? | ? | `target_x` |  |
| 7 | ? | ? | `target_y` |  |
| 8 | ? | ? | `target_z` |  |
| 9 | ? | ? | `charge_lv` |  |
| 10 | ? | ? | `reflect_ent_id` |  |

## `0xb474b0`（428 字节，10 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `channelid` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x29 | s8 | `type` |  |
| 4 | 0x2A | s8 | `pilotlv_min` |  |
| 5 | 0x2B | s8 | `pilotlv_max` |  |
| 6 | 0x2C | u16 | `user_num_eff` |  |
| 7 | 0x2E | u16 | `user_num_zeon` |  |
| 8 | 0x30 | u16 | `user_max` |  |
| 9 | 0x32 | u16 | `user_conn` |  |
| 10 | 0x34 | u16 | `user_comeback` |  |

## `0xb4db10`（426 字节，10 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `wave_rank` |  |
| 2 | 0x4 | u32 | `cleartime_sec` |  |
| 3 | 0x8 | s8 | `cleartime_rank` |  |
| 4 | 0xA | u16 | `container_num` |  |
| 5 | 0xC | u16 | `container_max` |  |
| 6 | 0xE | s8 | `container_rank` |  |
| 7 | 0x10 | u16 | `enemybase_num` |  |
| 8 | 0x12 | u16 | `enemybase_max` |  |
| 9 | 0x14 | s8 | `enemybase_rank` |  |
| 10 | 0x18 | u32 | `total_score` |  |

## `0xb4ea90`（443 字节，10 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `msg_id` |  |
| 2 | 0x8 | u32 | `parent_msgid` |  |
| 3 | 0x10 | u32 | `date` |  |
| 4 | 0x14 | u16 | `nice_count` |  |
| 5 | 0x16 | s8 | `is_niced` |  |
| 6 | 0x16 | s8 | `body` |  |
| 7 | 0xD8 | u32 | `pilot_id` |  |
| 8 | 0xDC | u32 | `npc_id` |  |
| 9 | 0xDC | u32 | `name` |  |
| 10 | 0xDC | u32 | `avatar` |  |

## `0xb4ed40`（422 字节，10 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x1D | s8 | `mil_class` |  |
| 4 | 0x20 | u32 | `rank` |  |
| 5 | 0x24 | u32 | `xwar_cnt` |  |
| 6 | 0x28 | u32 | `vslocal_cnt` |  |
| 7 | 0x2C | u32 | `last_login` |  |
| 8 | 0x30 | u32 | `last_logout` |  |
| 9 | 0x34 | u32 | `continued_login_days` |  |
| 10 | 0x38 | s8 | `is_bonus` |  |

## `0xb36ec0`（1035 字节，9 字段）← 调用者: sub_B01EA0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `dir_h` |  |
| 3 | ? | ? | `dir_v` |  |
| 4 | ? | ? | `msec` |  |
| 5 | ? | ? | `wrestle_id` |  |
| 6 | ? | ? | `charge_lv` |  |
| 7 | ? | ? | `action` |  |
| 8 | ? | ? | `chase_ent_id` |  |
| 9 | ? | ? | `is_dp_damage_cut` |  |

## `0xb37f60`（1029 字节，9 字段）← 调用者: sub_B02140

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `grenade_id` |  |
| 3 | ? | ? | `hit_x` |  |
| 4 | ? | ? | `hit_y` |  |
| 5 | ? | ? | `hit_z` |  |
| 6 | ? | ? | `vec_x` |  |
| 7 | ? | ? | `vec_y` |  |
| 8 | ? | ? | `vec_z` |  |
| 9 | ? | ? | `vec_power` |  |

## `0xb3b7a0`（2786 字节，9 字段）← 调用者: sub_B028D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `phash` |  |
| 2 | ? | ? | `frame_count` |  |
| 3 | ? | ? | `weapon_itemid` |  |
| 4 | ? | ? | `fire_id` |  |
| 5 | 0x0 | u16 | `charge_lv` |  |
| 6 | ? | ? | `instate_from_ent_id` |  |
| 7 | ? | ? | `create_frame_count` |  |
| 8 | ? | ? | `is_down_range` |  |
| 9 | ? | ? | `is_wrestle_first_high_lockon` |  |

## `0xb4d840`（386 字节，9 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `channel_id` |  |
| 2 | 0x4 | u32 | `party_id` |  |
| 3 | 0x8 | s8 | `troops` |  |
| 4 | 0xA | u16 | `member_count` |  |
| 5 | 0xA | u16 | `comment` |  |
| 6 | 0x49 | s8 | `pstat` |  |
| 7 | 0x4A | s8 | `is_lock` |  |
| 8 | 0x4C | u16 | `remain_minutes` |  |
| 9 | 0x50 | u32 | `party_type` |  |

## `0xb4df80`（390 字节，9 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `mailid` |  |
| 2 | 0x8 | u32 | `kind` |  |
| 3 | 0xC | u32 | `state` |  |
| 4 | 0xC | u32 | `pilot_name` |  |
| 5 | ? | ? | `subject` |  |
| 6 | 0x74 | u32 | `date` |  |
| 7 | 0x78 | u32 | `accept_term` |  |
| 8 | 0x7C | u32 | `attach_type` |  |
| 9 | 0x80 | u32 | `attach_id` |  |

## `0xb4e900`（396 字节，9 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `msg_id` |  |
| 2 | 0x8 | u32 | `date` |  |
| 3 | 0xC | u16 | `kind` |  |
| 4 | 0xE | u16 | `nice_count` |  |
| 5 | 0x10 | u16 | `child_count` |  |
| 6 | 0x10 | u16 | `body` |  |
| 7 | 0xD4 | u32 | `pilot_id` |  |
| 8 | 0xD8 | u32 | `npc_id` |  |
| 9 | 0xD8 | u32 | `name` |  |

## `0xb4eef0`（388 字节，9 字段）← 调用者: sub_B51930, sub_BA2680

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `sort_type` |  |
| 2 | 0x1 | s8 | `is_class_filter` |  |
| 3 | 0x2 | s8 | `class_filter_begin` |  |
| 4 | 0x3 | s8 | `class_filter_end` |  |
| 5 | 0x4 | s8 | `is_time_filter` |  |
| 6 | 0x5 | s8 | `time_filter_begin` |  |
| 7 | 0x6 | s8 | `time_filter_end` |  |
| 8 | 0x7 | s8 | `is_bonus_filter` |  |
| 9 | 0x8 | s8 | `bonus_filter` |  |

## `0xb51120`（481 字节，9 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `state` |  |
| 2 | 0x4 | u32 | `tournament_id` |  |
| 3 | 0x8 | u32 | `mode` |  |
| 4 | 0xC | u32 | `open_date` |  |
| 5 | 0x10 | u32 | `booking_start` |  |
| 6 | 0x14 | u32 | `booking_end` |  |
| 7 | 0x18 | u32 | `mission_id` |  |
| 8 | 0x2C | u32 | `is_end` |  |
| 9 | 0x30 | u32 | `is_debug` |  |

## `0xb03830`（359 字节，8 字段）← 调用者: sub_B03D30

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `worldid` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | ? | ? | `name_en` |  |
| 4 | ? | ? | `desc` |  |
| 5 | 0x128 | u32 | `stat` |  |
| 6 | 0x12C | u16 | `icon_id` |  |
| 7 | 0x130 | u32 | `client_now` |  |
| 8 | 0x134 | u32 | `client_max` |  |

## `0xb0a820`（578 字节，8 字段）← 调用者: sub_B0CC20, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `remain_msec` |  |
| 2 | 0x4 | u32 | `coop_step` |  |
| 3 | 0x14 | s8 | `coop_dead_remain` |  |
| 4 | 0x15 | s8 | `is_prestart` |  |
| 5 | 0x18 | u32 | `rule_status` |  |
| 6 | 0x1C | u32 | `rule_timer_msec` |  |
| 7 | 0x20 | u32 | `rule_param1` |  |
| 8 | 0x24 | u32 | `rule_param2` |  |

## `0xb364e0`（967 字节，8 字段）← 调用者: sub_B01D50

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `rcnt_bullet_mgz` |  |
| 6 | ? | ? | `rcnt_bullet_all` |  |
| 7 | ? | ? | `charge_lv` |  |
| 8 | ? | ? | `salvo_slot` |  |

## `0xb368b0`（967 字节，8 字段）← 调用者: sub_B01DE0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `rcnt_bullet_mgz` |  |
| 6 | ? | ? | `rcnt_bullet_all` |  |
| 7 | ? | ? | `begin1_end0` |  |
| 8 | ? | ? | `salvo_slot` |  |

## `0xb40b50`（966 字节，8 字段）← 调用者: sub_B02A70

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `dir_h` |  |
| 3 | ? | ? | `wrestle_id` |  |
| 4 | ? | ? | `chase_time_msec` |  |
| 5 | ? | ? | `target_ent_id` |  |
| 6 | ? | ? | `target_pos_x` |  |
| 7 | ? | ? | `target_pos_y` |  |
| 8 | ? | ? | `target_pos_z` |  |

## `0xb08f80`（426 字节，7 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `quest_id` |  |
| 2 | 0x0 | u32 | `title` |  |
| 3 | 0x68 | u32 | `achv_trig` |  |
| 4 | 0x6C | u32 | `achv_trigbit` |  |
| 5 | 0x7C | u32 | `denom_val` |  |
| 6 | 0x80 | u32 | `num_val` |  |
| 7 | 0x84 | u32 | `common_value` |  |

## `0xb0ad10`（385 字节，7 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `team` |  |
| 2 | 0x2 | u16 | `troops` |  |
| 3 | 0xC | s8 | `is_visible` |  |
| 4 | 0xD | s8 | `is_lock` |  |
| 5 | 0xE | s8 | `is_keep` |  |
| 6 | 0xE | s8 | `near_ms_num` |  |
| 7 | 0xE | s8 | `conquer_remain_sec` |  |

## `0xb34930`（998 字节，7 字段）← 调用者: sub_B01260

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `voice_id` |  |
| 2 | ? | ? | `to_world_id` |  |
| 3 | ? | ? | `to_pilot_id` |  |
| 4 | ? | ? | `is_party` |  |
| 5 | ? | ? | `is_use_textmsg` |  |
| 6 | ? | ? | `is_cutin` |  |
| 7 | ? | ? | `is_voice` |  |

## `0xb38ac0`（904 字节，7 字段）← 调用者: sub_B02340

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `shot0_drop1_impact2` |  |
| 6 | ? | ? | `fx_opt` |  |
| 7 | ? | ? | `airbomb_id` |  |

## `0xb39090`（902 字节，7 字段）← 调用者: sub_B023D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `rcnt_bullet_mgz` |  |
| 6 | ? | ? | `rcnt_bullet_all` |  |
| 7 | ? | ? | `begin1_end0` |  |

## `0xb3a1f0`（902 字节，7 字段）← 调用者: sub_B024E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `rcnt_bullet_mgz` |  |
| 6 | ? | ? | `rcnt_bullet_all` |  |
| 7 | ? | ? | `begin1_end0` |  |

## `0xb47910`（400 字节，7 字段）← 调用者: sub_B48010, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `state` |  |
| 2 | 0x4 | u32 | `chances_used` |  |
| 3 | 0x8 | u32 | `chances_total` |  |
| 4 | 0xC | u32 | `playsec_total` |  |
| 5 | 0x10 | u32 | `playsec_elapsed` |  |
| 6 | 0x14 | u32 | `playscore_sum` |  |
| 7 | 0x40 | u32 | `interval_cnt` |  |

## `0xb4bc80`（341 字节，7 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x4 | u32 | `battle_num` |  |
| 2 | 0x8 | u32 | `begin_time` |  |
| 3 | 0xC | u32 | `end_time` |  |
| 4 | 0x10 | u32 | `rwd_item_id` |  |
| 5 | 0x14 | u32 | `rwd_item_num` |  |
| 6 | 0x18 | u32 | `rwd_gp_amount` |  |
| 7 | 0x1C | s8 | `is_completed` |  |

## `0xb4d9d0`（309 字节，7 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x1D | s8 | `level` |  |
| 4 | 0x1E | u16 | `rate_vslocal` |  |
| 5 | 0x20 | s8 | `is_leader` |  |
| 6 | 0x20 | s8 | `avatar` |  |
| 7 | 0x3C | s8 | `pstat` |  |

## `0xb4dcc0`（304 字节，7 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `end_wave` |  |
| 2 | 0x1 | s8 | `result_coop` |  |
| 3 | 0x2 | s8 | `rank` |  |
| 4 | 0x4 | u32 | `rank_score` |  |
| 5 | 0x8 | u32 | `container_comp` |  |
| 6 | 0xC | u32 | `enemyobj_comp` |  |
| 7 | 0x10 | u32 | `total_score` |  |

## `0xb4e110`（303 字节，7 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `shopitem_id` |  |
| 2 | 0x4 | u32 | `gp_x01` |  |
| 3 | 0x8 | u32 | `gp_x10` |  |
| 4 | 0xC | u32 | `cp_x01` |  |
| 5 | 0x10 | u32 | `cp_x10` |  |
| 6 | 0x14 | s8 | `bit_eff` |  |
| 7 | 0x16 | u16 | `stock` |  |

## `0xb501c0`（303 字节，7 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `score` |  |
| 2 | 0x4 | u32 | `pilot_id` |  |
| 3 | 0x4 | u32 | `name` |  |
| 4 | 0x21 | s8 | `troops` |  |
| 5 | 0x24 | u32 | `world_id` |  |
| 6 | 0x28 | u32 | `season_class_lv` |  |
| 7 | 0x28 | u32 | `clan_name` |  |

## `0xb50360`（304 字节，7 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `prize_id` |  |
| 2 | 0x4 | u32 | `id_type` |  |
| 3 | 0x8 | u16 | `stack` |  |
| 4 | 0xA | s8 | `rare_type` |  |
| 5 | 0xC | u32 | `odds` |  |
| 6 | 0x10 | u32 | `odds_max` |  |
| 7 | 0x14 | u16 | `csv_index` |  |

## `0xb913e0`（834 字节，7 字段）← 调用者: sub_AFF100

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `matching_type` |  |
| 2 | ? | ? | `matching_request_flag` |  |
| 3 | ? | ? | `matching_battlerule_flag` |  |
| 4 | ? | ? | `matching_extrule_flag` |  |
| 5 | ? | ? | `mission_select_type` |  |
| 6 | ? | ? | `mission_select_value` |  |
| 7 | ? | ? | `client_bogo_version` |  |

## `0xb9e240`（908 字节，7 字段）← 调用者: sub_B00170

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `shopitemid` |  |
| 2 | ? | ? | `id_type` |  |
| 3 | ? | ? | `tab_type` |  |
| 4 | ? | ? | `is_cp` |  |
| 5 | ? | ? | `total_price` |  |
| 6 | ? | ? | `gacha_id` |  |
| 7 | ? | ? | `is_bundle` |  |

## `0xb09130`（265 字节，6 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `item_id` |  |
| 2 | 0x4 | u32 | `effect_msec` |  |
| 3 | 0x8 | s8 | `effect_catego` |  |
| 4 | 0xA | u16 | `effect_param` |  |
| 5 | 0xC | u32 | `effect_value` |  |
| 6 | 0x10 | u16 | `effect_value2` |  |

## `0xb0c210`（873 字节，6 字段）← 调用者: 0xedb1b0, sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `ent_id` |  |
| 2 | 0x0 | u16 | `pos_x` |  |
| 3 | 0x0 | u16 | `pos_y` |  |
| 4 | 0x0 | u16 | `pos_z` |  |
| 5 | 0x0 | u16 | `attach_parent_ent_id` |  |
| 6 | 0x0 | u16 | `is_using_ss` |  |

## `0xb0c910`（771 字节，6 字段）← 调用者: sub_B01AB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ent_id` |  |
| 2 | ? | ? | `pos_x` |  |
| 3 | ? | ? | `pos_y` |  |
| 4 | ? | ? | `pos_z` |  |
| 5 | ? | ? | `attach_parent_ent_id` |  |
| 6 | ? | ? | `is_using_ss` |  |

## `0xb33f30`（769 字节，6 字段）← 调用者: sub_B01A20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ms_index` |  |
| 2 | ? | ? | `post_index` |  |
| 3 | ? | ? | `spt_spot_index` |  |
| 4 | ? | ? | `is_btlship_ride` |  |
| 5 | ? | ? | `is_msma_ride` |  |
| 6 | ? | ? | `respawn_ent_id` |  |

## `0xb35d60`（833 字节，6 字段）← 调用者: sub_B01CA0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `attach_parent_ent_id` |  |
| 6 | ? | ? | `is_initiation` |  |

## `0xb38370`（768 字节，6 字段）← 调用者: sub_B02220

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `grenade_id` |  |
| 3 | ? | ? | `pos_x` |  |
| 4 | ? | ? | `pos_y` |  |
| 5 | ? | ? | `pos_z` |  |
| 6 | ? | ? | `target_ent_id` |  |

## `0xb498c0`（304 字节，6 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x6 | u16 | `rate_vslocal` |  |
| 3 | 0x8 | s8 | `stat` |  |
| 4 | 0x9 | s8 | `is_booking` |  |
| 5 | 0xC | u32 | `mission_id` |  |
| 6 | 0xC | u32 | `avatar` |  |

## `0xb8fac0`（955 字节，6 字段）← 调用者: sub_AFEEF0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `matching_type` |  |
| 2 | ? | ? | `mission_id` |  |
| 3 | ? | ? | `extrule_id` |  |
| 4 | ? | ? | `is_lock` |  |
| 5 | ? | ? | `is_vsclan` |  |
| 6 | ? | ? | `is_ev_caravan` |  |

## `0xba4110`（840 字节，6 字段）← 调用者: sub_B00AD0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `shopitemid` |  |
| 2 | ? | ? | `id_type` |  |
| 3 | ? | ? | `tab_type` |  |
| 4 | ? | ? | `is_cp` |  |
| 5 | ? | ? | `total_price` |  |
| 6 | ? | ? | `extend_num` |  |

## `0xb0b320`（225 字节，5 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `is_final_phase` |  |
| 2 | 0x4 | u32 | `field_bgm_id` |  |
| 3 | 0x8 | u32 | `ace_bgm_id` |  |
| 4 | 0xC | u32 | `force_bgm_id` |  |
| 5 | 0x10 | s8 | `is_one_shot` |  |

## `0xb31b10`（782 字节，5 字段）← 调用者: sub_B01030

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `userid` |  |
| 2 | ? | ? | `world_id` |  |
| 3 | ? | ? | `pilot_id` |  |
| 4 | ? | ? | `room_id` |  |
| 5 | ? | ? | `is_comeback` |  |

## `0xb34670`（699 字节，5 字段）← 调用者: sub_B01B20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `arms_id` |  |
| 2 | ? | ? | `attach_parent_ent_id` |  |
| 3 | ? | ? | `attach_pos_x` |  |
| 4 | ? | ? | `attach_pos_y` |  |
| 5 | ? | ? | `attach_pos_z` |  |

## `0xb3e580`（770 字节，5 字段）← 调用者: sub_B016E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `support_type` |  |
| 2 | ? | ? | `target_x` |  |
| 3 | ? | ? | `target_y` |  |
| 4 | ? | ? | `target_z` |  |
| 5 | ? | ? | `spt_spot_index` |  |

## `0xb49cf0`（228 字节，5 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `uniqid` |  |
| 2 | 0x8 | u32 | `item_id` |  |
| 3 | 0xC | u32 | `tm_sec` |  |
| 4 | 0x10 | u32 | `tm_usec` |  |
| 5 | 0x14 | u16 | `stack` |  |

## `0xb4a580`（326 字节，5 字段）← 调用者: sub_B4A6D0, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `item_id` |  |
| 2 | 0x4 | u16 | `db_index` |  |
| 3 | 0x6 | u16 | `buildup_cnt` |  |
| 4 | 0x1C | s8 | `spticket_success_wp` |  |
| 5 | 0x1D | s8 | `spticket_greatest_wp` |  |

## `0xb4aa30`（531 字节，5 字段）← 调用者: sub_B51930, sub_B98E80, sub_B992A0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `uniq_id` |  |
| 2 | 0x8 | u16 | `slot` |  |
| 3 | 0x18 | u32 | `eq_shield` |  |
| 4 | 0x1C | u32 | `eq_special` |  |
| 5 | 0x4C | u32 | `setname` |  |

## `0xb4ec50`（226 字节，5 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `clan_id` |  |
| 2 | 0x4 | u32 | `world_id` |  |
| 3 | 0x8 | s8 | `emb_base` |  |
| 4 | 0x9 | s8 | `emb_parts1` |  |
| 5 | 0xA | s8 | `emb_parts2` |  |

## `0xb4f620`（228 字节，5 字段）← 调用者: sub_B51930, sub_BA3650, sub_BA3820, sub_BA3A30, sub_BA3C40, sub_BA7770

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `kind` |  |
| 2 | 0x2 | u16 | `term` |  |
| 3 | 0x4 | u16 | `filter` |  |
| 4 | 0x6 | u16 | `reason` |  |
| 5 | 0x8 | u16 | `troops` |  |

## `0xb50f80`（416 字节，5 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `is_dc` |  |
| 2 | 0x4 | u32 | `bef_dcpoint` |  |
| 3 | 0x8 | u32 | `aft_dcpoint` |  |
| 4 | 0x8 | u32 | `bef_next` |  |
| 5 | ? | ? | `aft_next` |  |

## `0xb51310`（224 字节，5 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x20 | u32 | `level` |  |
| 4 | 0x24 | u32 | `world_id` |  |
| 5 | 0x24 | u32 | `avatar` |  |

## `0xb8a8b0`（698 字节，5 字段）← 调用者: sub_AFE850

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `troops` |  |
| 2 | ? | ? | `pilot_id` |  |
| 3 | ? | ? | `is_tutorial_skip` |  |
| 4 | ? | ? | `dbg_comeback_disable` |  |
| 5 | ? | ? | `channeling_type` |  |

## `0xb8fe80`（790 字节，5 字段）← 调用者: sub_AFEF40

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `matching_type` |  |
| 2 | ? | ? | `room_id` |  |
| 3 | ? | ? | `is_audience` |  |
| 4 | ? | ? | `audience_teamside` |  |
| 5 | ? | ? | `extrule_id` |  |

## `0xb96e30`（712 字节，5 字段）← 调用者: sub_AFF8E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `ticket_id` |  |
| 4 | ? | ? | `usenum` |  |
| 5 | ? | ? | `param_target` |  |

## `0xb97100`（712 字节，5 字段）← 调用者: sub_AFF920

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `ticket_id` |  |
| 4 | ? | ? | `usenum` |  |
| 5 | ? | ? | `param_target` |  |

## `0xb973d0`（712 字节，5 字段）← 调用者: sub_AFF960

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `ticket_id` |  |
| 4 | ? | ? | `usenum` |  |
| 5 | ? | ? | `param_target` |  |

## `0xb9cd70`（1033 字节，5 字段）← 调用者: sub_AFFFD0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `shopitemid` |  |
| 2 | ? | ? | `id_type` |  |
| 3 | ? | ? | `tab_type` |  |
| 4 | ? | ? | `is_cp` |  |
| 5 | ? | ? | `total_price` |  |

## `0xba2a80`（704 字节，5 字段）← 调用者: sub_B00910

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `tree_id` |  |
| 2 | ? | ? | `node_no` |  |
| 3 | ? | ? | `idx_no` |  |
| 4 | ? | ? | `point_use` |  |
| 5 | ? | ? | `is_supply` |  |

## `0xb0a670`（421 字节，4 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x18 | u32 | `dotdmg_min` |  |
| 2 | 0x1C | u16 | `atk_team` |  |
| 3 | 0x20 | u32 | `round_now` |  |
| 4 | 0x24 | u32 | `round_max` |  |

## `0xb343f0`（635 字节，4 字段）← 调用者: sub_B01A70

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `post_index` |  |
| 2 | ? | ? | `spt_spot_index` |  |
| 3 | ? | ? | `is_btlship_ride` |  |
| 4 | ? | ? | `respawn_ent_id` |  |

## `0xb34f10`（701 字节，4 字段）← 调用者: sub_B012C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `cutin_category_id` |  |
| 2 | ? | ? | `to_world_id` |  |
| 3 | ? | ? | `to_pilot_id` |  |
| 4 | ? | ? | `to_range` |  |

## `0xb3d600`（706 字节，4 字段）← 调用者: sub_B01560

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | ? | ? | `to_x` |  |
| 2 | ? | ? | `to_y` |  |
| 3 | ? | ? | `to_z` |  |
| 4 | ? | ? | `msec` |  |

## `0xb3e890`（1070 字节，4 字段）← 调用者: sub_B01720

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ent_id` |  |
| 2 | ? | ? | `hit_team` |  |
| 3 | ? | ? | `hit_troops` |  |
| 4 | ? | ? | `support_type` |  |

## `0xb4a7e0`（387 字节，4 字段）← 调用者: sub_B51930, sub_B988D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `uniq_id` |  |
| 2 | 0x8 | u16 | `deck_type` |  |
| 3 | 0xA | u16 | `deck_slot` |  |
| 4 | 0xA | u16 | `setname` |  |

## `0xb4be80`（579 字节，4 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x64 | u32 | `lv_history_num` |  |
| 3 | 0x68 | u32 | `lv_history_max` |  |
| 4 | 0x0 | u16 | `termstr_now` |  |

## `0xb4d6e0`（187 字节，4 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `id_type` |  |
| 2 | 0x4 | u32 | `itemid` |  |
| 3 | 0x8 | s8 | `is_itmbox` |  |
| 4 | 0xA | u16 | `amount` |  |

## `0xb4f710`（375 字节，4 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rank` |  |
| 2 | 0x4 | u32 | `score_now` |  |
| 3 | 0x8 | u16 | `entry_until` |  |
| 4 | 0x18 | u16 | `entry_until_es` |  |

## `0xb50780`（185 字节，4 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `phase` |  |
| 2 | 0x4 | u32 | `round` |  |
| 3 | 0x8 | u32 | `open_time` |  |
| 4 | 0xC | u32 | `close_time` |  |

## `0xb50ec0`（186 字节，4 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `pilot_id` |  |
| 2 | 0x0 | u32 | `name` |  |
| 3 | 0x1D | s8 | `level` |  |
| 4 | 0x1D | s8 | `avatar` |  |

## `0xb8a310`（800 字节，4 字段）← 调用者: sub_AFE7E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `troops` |  |
| 2 | ? | ? | `slot` |  |
| 3 | ? | ? | `pilot_id` |  |
| 4 | ? | ? | `is_check_only` |  |

## `0xb8a630`（632 字节，4 字段）← 调用者: sub_AFE820

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `troops` |  |
| 2 | ? | ? | `slot` |  |
| 3 | ? | ? | `pilot_id` |  |
| 4 | ? | ? | `del_kind` |  |

## `0xb91ee0`（636 字节，4 字段）← 调用者: sub_AFF1E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `party_id` |  |
| 2 | ? | ? | `channel_id` |  |
| 3 | ? | ? | `pilot_id` |  |
| 4 | ? | ? | `reason` |  |

## `0xb962c0`（646 字节，4 字段）← 调用者: sub_AFF7C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `ticket_id` |  |
| 3 | ? | ? | `usenum` |  |
| 4 | ? | ? | `param_idx` |  |

## `0xb96550`（646 字节，4 字段）← 调用者: sub_AFF800

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `ticket_id` |  |
| 3 | ? | ? | `usenum` |  |
| 4 | ? | ? | `param_idx` |  |

## `0xb967e0`（646 字节，4 字段）← 调用者: sub_AFF840

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `ticket_id` |  |
| 3 | ? | ? | `usenum` |  |
| 4 | ? | ? | `param_idx` |  |

## `0xb978a0`（646 字节，4 字段）← 调用者: sub_AFF9D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `use_gp` |  |
| 4 | ? | ? | `use_bc` |  |

## `0xb97b30`（646 字节，4 字段）← 调用者: sub_AFFA10

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `use_gp` |  |
| 4 | ? | ? | `use_bc` |  |

## `0xb97dc0`（646 字节，4 字段）← 调用者: sub_AFFA50

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `use_gp` |  |
| 4 | ? | ? | `use_bc` |  |

## `0xb9d180`（714 字节，4 字段）← 调用者: sub_B00020

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid` |  |
| 2 | ? | ? | `id_type` |  |
| 3 | ? | ? | `inv_place` |  |
| 4 | ? | ? | `total_price` |  |

## `0xba3e90`（636 字节，4 字段）← 调用者: sub_B00AA0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `count` |  |
| 2 | ? | ? | `total_price` |  |
| 3 | ? | ? | `use_bc` |  |
| 4 | ? | ? | `token_id` |  |

## `0xb08ec0`（184 字节，3 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x4 | u32 | `gain_val` |  |
| 2 | 0x8 | u32 | `type` |  |
| 3 | 0xC | u32 | `badge_rank` |  |

## `0xb0b280`（147 字节，3 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `gauge_now` |  |
| 2 | 0x4 | s8 | `stat` |  |
| 3 | 0x6 | u16 | `access_ent_id` |  |

## `0xb0b410`（147 字节，3 字段）← 调用者: sub_B0CC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `itemid` |  |
| 2 | 0x4 | s8 | `is_used` |  |
| 3 | 0x5 | s8 | `is_usable` |  |

## `0xb0bf80`（145 字节，3 字段）← 调用者: sub_B0CC20, sub_B3AB30

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `ent_id` |  |
| 2 | 0x4 | s8 | `wslot_idx` |  |
| 3 | 0x4 | s8 | `move_info` |  |

## `0xb332b0`（567 字节，3 字段）← 调用者: sub_B01440

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `target_world_id` |  |
| 2 | ? | ? | `target_pilot_id` |  |
| 3 | ? | ? | `kick_reason` |  |

## `0xb38e50`（570 字节，3 字段）← 调用者: sub_B01380

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ent_id` |  |
| 2 | ? | ? | `airbomb_id` |  |
| 3 | ? | ? | `arms_id` |  |

## `0xb39990`（2140 字节，3 字段）← 调用者: sub_B02460

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `weapon_itemid` |  |
| 3 | ? | ? | `fire_id` |  |

## `0xb3c290`（638 字节，3 字段）← 调用者: sub_B01960

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `group_id` |  |
| 3 | ? | ? | `reason` |  |

## `0xb3f1b0`（574 字节，3 字段）← 调用者: sub_B01780

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `target_x` |  |
| 2 | ? | ? | `target_y` |  |
| 3 | ? | ? | `target_z` |  |

## `0xb4a6d0`（263 字节，3 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | ? | ? | `body` |  |
| 2 | 0x198 | u32 | `limit_use` |  |
| 3 | 0x19C | u32 | `limit_coolup` |  |

## `0xb4f080`（249 字节，3 字段）← 调用者: sub_B51930, sub_BA1200

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `active_time_bits` |  |
| 2 | 0x1 | s8 | `play_style` |  |
| 3 | ? | ? | `notice_body` |  |

## `0xb506e0`（145 字节，3 字段）← 调用者: sub_B50F80, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `point` |  |
| 2 | 0x4 | u32 | `item_id` |  |
| 3 | 0x8 | u32 | `item_num` |  |

## `0xb8e290`（569 字节，3 字段）← 调用者: sub_AFED00

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id` |  |
| 2 | ? | ? | `world_id` |  |
| 3 | ? | ? | `is_checkmedal` |  |

## `0xb8f830`（654 字节，3 字段）← 调用者: sub_AFEEC0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `matching_type` |  |
| 2 | ? | ? | `is_coop` |  |
| 3 | ? | ? | `mission_id` |  |

## `0xb90390`（570 字节，3 字段）← 调用者: sub_AFEFB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `room_id` |  |
| 2 | ? | ? | `pilot_id` |  |
| 3 | ? | ? | `reason` |  |

## `0xb93160`（582 字节，3 字段）← 调用者: sub_AFF360

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid` |  |
| 2 | ? | ? | `decktype` |  |
| 3 | ? | ? | `deckslot` |  |

## `0xb933b0`（582 字节，3 字段）← 调用者: sub_AFF390

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `eq_slot` |  |
| 3 | ? | ? | `item_id` |  |

## `0xb93600`（582 字节，3 字段）← 调用者: 0x15da310, sub_AFF3C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `eq_slot1` |  |
| 3 | ? | ? | `eq_slot2` |  |

## `0xb94030`（580 字节，3 字段）← 调用者: sub_AFF4B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |
| 3 | ? | ? | `status` |  |

## `0xb94a10`（585 字节，3 字段）← 调用者: sub_AFF570

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `decal` |  |
| 3 | ? | ? | `uniqid_decal` |  |

## `0xb94e60`（582 字节，3 字段）← 调用者: sub_AFF5E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `use_bc` |  |
| 3 | ? | ? | `price` |  |

## `0xb95a40`（570 字节，3 字段）← 调用者: sub_AFF700

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ms_plan_id` |  |
| 2 | ? | ? | `ticket_id` |  |
| 3 | ? | ? | `usenum` |  |

## `0xb95c80`（570 字节，3 字段）← 调用者: sub_AFF730

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ms_plan_id` |  |
| 2 | ? | ? | `ticket_id` |  |
| 3 | ? | ? | `usenum` |  |

## `0xb95ec0`（570 字节，3 字段）← 调用者: sub_AFF760

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ms_plan_id` |  |
| 2 | ? | ? | `ticket_id` |  |
| 3 | ? | ? | `usenum` |  |

## `0xb98050`（580 字节，3 字段）← 调用者: sub_AFFA90

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `color_id` |  |
| 3 | ? | ? | `use_gp` |  |

## `0xb982a0`（580 字节，3 字段）← 调用者: sub_AFFAC0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `ms_plan_id` |  |
| 3 | ? | ? | `ms_plan_num` |  |

## `0xb984f0`（580 字节，3 字段）← 调用者: sub_AFFAF0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `bef_sp_parts_id` |  |
| 3 | ? | ? | `aft_sp_parts_id` |  |

## `0xb9b490`（654 字节，3 字段）← 调用者: sub_AFFF20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilotid` |  |
| 2 | ? | ? | `world_id` |  |
| 3 | ? | ? | `send_sysmes` |  |

## `0xb9b720`（654 字节，3 字段）← 调用者: sub_AFFF50

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilotid` |  |
| 2 | ? | ? | `world_id` |  |
| 3 | ? | ? | `send_sysmes` |  |

## `0xb9c530`（580 字节，3 字段）← 调用者: sub_B00310

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `mailid` |  |
| 2 | ? | ? | `attach_type` |  |
| 3 | ? | ? | `attach_id` |  |

## `0xb9c780`（580 字节，3 字段）← 调用者: sub_B00340

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `mailid` |  |
| 2 | ? | ? | `attach_type` |  |
| 3 | ? | ? | `attach_id` |  |

## `0xb9e000`（572 字节，3 字段）← 调用者: sub_B00140

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `gacha_id` |  |
| 2 | ? | ? | `exec_type` |  |
| 3 | ? | ? | `is_bundle` |  |

## `0xb9f830`（663 字节，3 字段）← 调用者: sub_B00480

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `npc_id` |  |
| 2 | ? | ? | `is_active` |  |
| 3 | ? | ? | `clan_kind` |  |

## `0xba0260`（572 字节，3 字段）← 调用者: sub_B00550

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id_applicant` |  |
| 2 | ? | ? | `is_ok` |  |
| 3 | ? | ? | `clan_kind` |  |

## `0xba04a0`（572 字节，3 字段）← 调用者: sub_B00580

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id_sub` |  |
| 2 | ? | ? | `is_set` |  |
| 3 | ? | ? | `clan_kind` |  |

## `0xba06e0`（576 字节，3 字段）← 调用者: sub_B005B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `emb_base` |  |
| 2 | ? | ? | `emb_parts1` |  |
| 3 | ? | ? | `emb_parts2` |  |

## `0xba1fd0`（677 字节，3 字段）← 调用者: sub_B007C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `parent_msgid` |  |
| 2 | ? | ? | `kind` |  |
| 3 | ? | ? | `clan_kind` |  |

## `0xba3c40`（591 字节，3 字段）← 调用者: sub_B00A40

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `order` |  |
| 2 | ? | ? | `page` |  |
| 3 | ? | ? | `clan_kind` |  |

## `0xba6cc0`（570 字节，3 字段）← 调用者: sub_B00E10

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id` |  |
| 2 | ? | ? | `world_id` |  |
| 3 | ? | ? | `favms_id` |  |

## `0xb04c70`（566 字节，2 字段）← 调用者: sub_BA8B80

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `version` |  |
| 2 | ? | ? | `gentime` |  |

## `0xb05a30`（480 字节，2 字段）← 调用者: sub_AFE6B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `world_id` |  |
| 2 | ? | ? | `channeling_type` |  |

## `0xb0a1a0`（185 字节，2 字段）← 调用者: sub_B0CC20, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `sub_val` |  |
| 2 | 0xC | s8 | `is_clear` |  |

## `0xb318d0`（566 字节，2 字段）← 调用者: sub_BAAF00

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `version` |  |
| 2 | ? | ? | `gentime` |  |

## `0xb330c0`（483 字节，2 字段）← 调用者: sub_B01410

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `world_id` |  |
| 2 | ? | ? | `pilot_id` |  |

## `0xb33810`（585 字节，2 字段）← 调用者: sub_B014B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `is_initial` |  |
| 2 | ? | ? | `script_thread` |  |

## `0xb360b0`（569 字节，2 字段）← 调用者: sub_B01D20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `equip_index` |  |

## `0xb36c80`（567 字节，2 字段）← 调用者: sub_B01E70

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `itemid` |  |

## `0xb3a860`（710 字节，2 字段）← 调用者: sub_B026A0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `from_ent_id` |  |
| 2 | ? | ? | `wslot_idx` |  |

## `0xb3c510`（570 字节，2 字段）← 调用者: sub_B01990

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `group_id` |  |

## `0xb3c750`（570 字节，2 字段）← 调用者: sub_B019C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `frame_count` |  |
| 2 | ? | ? | `group_id` |  |

## `0xb3d210`（574 字节，2 字段）← 调用者: sub_B02A30

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | ? | ? | `target_ent_id` |  |
| 2 | ? | ? | `hate_adjust` |  |

## `0xb3d8d0`（490 字节，2 字段）← 调用者: sub_B015A0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `percent_val` |  |
| 2 | ? | ? | `equip_idx` |  |

## `0xb3dcb0`（490 字节，2 字段）← 调用者: sub_B01600

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `team` |  |
| 2 | ? | ? | `troops` |  |

## `0xb3e1e0`（490 字节，2 字段）← 调用者: sub_B01690

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `target_member` |  |
| 2 | ? | ? | `target_ace` |  |

## `0xb3f3f0`（910 字节，2 字段）← 调用者: sub_B017B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `order_kind` |  |
| 2 | ? | ? | `order_param` |  |

## `0xb3f780`（488 字节，2 字段）← 调用者: sub_B017F0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `order_kind` |  |
| 2 | ? | ? | `order_param` |  |

## `0xb3fcd0`（490 字节，2 字段）← 调用者: sub_B01860

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `from_ent_id` |  |
| 2 | ? | ? | `to_ent_id` |  |

## `0xb47b90`（304 字节，2 字段）← 调用者: sub_B48010, sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `begin_time` |  |
| 2 | 0x4 | u16 | `elapsed_days` |  |

## `0xb47fa0`（106 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `module_id` |  |
| 2 | 0x4 | u32 | `count` |  |

## `0xb49c80`（106 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `navi_id` |  |
| 2 | 0x4 | u32 | `status` |  |

## `0xb4a970`（183 字节，2 字段）← 调用者: sub_B51930, sub_B99850

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `deck_type` |  |
| 2 | 0x2 | u16 | `deck_set` |  |

## `0xb4ac50`（208 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | s8 | `db_index` |  |
| 2 | 0x4 | u32 | `equip_wid` |  |

## `0xb4d7a0`（148 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x1 | s8 | `openbox` |  |
| 2 | 0x2 | u16 | `gp_rate` |  |

## `0xb4fa90`（106 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rank` |  |
| 2 | 0x4 | u32 | `score_now` |  |

## `0xb50150`（106 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `rank` |  |
| 2 | 0x4 | u32 | `season_class_lv` |  |

## `0xb502f0`（107 字节，2 字段）← 调用者: sub_B51930

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u32 | `gacha_id` |  |
| 2 | 0x4 | u16 | `stock` |  |

## `0xb50cd0`（308 字节，2 字段）← 调用者: sub_B50E10

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x0 | u16 | `node_id` |  |
| 2 | 0x4 | u16 | `win_team_id` |  |

## `0xb89460`（566 字节，2 字段）← 调用者: sub_BAE160

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `version` |  |
| 2 | ? | ? | `gentime` |  |

## `0xb8a100`（515 字节，2 字段）← 调用者: sub_AFE7B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot` |  |
| 2 | ? | ? | `slot` |  |

## `0xb8b1a0`（480 字节，2 字段）← 调用者: sub_AFE900

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `tuto_step_now` |  |
| 2 | ? | ? | `tuto_step_next` |  |

## `0xb8b8e0`（516 字节，2 字段）← 调用者: sub_AFE9B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `avatar` |  |
| 2 | ? | ? | `is_reset` |  |

## `0xb8baf0`（483 字节，2 字段）← 调用者: sub_AFE9E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `kind` |  |
| 2 | ? | ? | `custom_id` |  |

## `0xb8bce0`（485 字节，2 字段）← 调用者: sub_AFEA10

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `custom_id` |  |
| 2 | ? | ? | `use_bc` |  |

## `0xb8bed0`（483 字节，2 字段）← 调用者: sub_AFEA40

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `emblem_id` |  |
| 2 | ? | ? | `use_gp` |  |

## `0xb8c420`（483 字节，2 字段）← 调用者: sub_AFEAB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `module_id` |  |
| 2 | ? | ? | `count` |  |

## `0xb8e0a0`（483 字节，2 字段）← 调用者: sub_AFECD0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id` |  |
| 2 | ? | ? | `world_id` |  |

## `0xb8e4d0`（483 字节，2 字段）← 调用者: sub_AFED30

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id` |  |
| 2 | ? | ? | `world_id` |  |

## `0xb901a0`（488 字节，2 字段）← 调用者: sub_AFEF80

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id` |  |
| 2 | ? | ? | `is_gm_camera` |  |

## `0xb905d0`（607 字节，2 字段）← 调用者: sub_AFEFE0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | ? | ? | `mission_id` |  |
| 2 | ? | ? | `is_lock` |  |

## `0xb91040`（486 字节，2 字段）← 调用者: sub_AFF0B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `matching_type` |  |
| 2 | ? | ? | `matching_request_flag` |  |

## `0xb918e0`（486 字节，2 字段）← 调用者: sub_AFF160

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `matching_type` |  |
| 2 | ? | ? | `room_id` |  |

## `0xb91ad0`（599 字节，2 字段）← 调用者: sub_AFF190

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `is_recruiting` |  |
| 2 | ? | ? | `party_type` |  |

## `0xb92650`（599 字节，2 字段）← 调用者: sub_AFF270

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `is_recruiting` |  |
| 2 | ? | ? | `party_type` |  |

## `0xb92a60`（486 字节，2 字段）← 调用者: sub_AFF2C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `channel_id` |  |
| 2 | ? | ? | `party_id` |  |

## `0xb92c50`（488 字节，2 字段）← 调用者: sub_AFF2F0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `ready_ok` |  |
| 2 | ? | ? | `client_bogo_version` |  |

## `0xb93850`（498 字节，2 字段）← 调用者: sub_AFF3F0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |

## `0xb93a50`（498 字节，2 字段）← 调用者: sub_AFF420

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |

## `0xb94c60`（498 字节，2 字段）← 调用者: sub_AFF5B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `color` |  |

## `0xb950b0`（488 字节，2 字段）← 调用者: sub_AFF610

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `use_bc` |  |
| 2 | ? | ? | `price` |  |

## `0xb95460`（498 字节，2 字段）← 调用者: sub_AFF670

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid` |  |
| 2 | ? | ? | `is_favorite` |  |

## `0xb95660`（486 字节，2 字段）← 调用者: sub_AFF6A0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `msma_sort_type` |  |
| 2 | ? | ? | `msma_sort_order` |  |

## `0xb95850`（486 字节，2 字段）← 调用者: sub_AFF6D0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `msma_sort_type` |  |
| 2 | ? | ? | `msma_sort_order` |  |

## `0xb96c30`（500 字节，2 字段）← 调用者: sub_AFF8B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `weapon_buildup_extra_cnt` |  |

## `0xb976a0`（498 字节，2 字段）← 调用者: sub_AFF9A0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `item_id` |  |

## `0xb98aa0`（490 字节，2 字段）← 调用者: sub_AFFB60

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `deck_type` |  |
| 2 | ? | ? | `slot` |  |

## `0xb98c90`（490 字节，2 字段）← 调用者: sub_AFFB90

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `deck_type` |  |
| 2 | ? | ? | `slot` |  |

## `0xb98e80`（531 字节，2 字段）← 调用者: sub_AFFBC0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `equip_set` |  |

## `0xb990a0`（500 字节，2 字段）← 调用者: sub_AFFBF0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `slot` |  |

## `0xb992a0`（531 字节，2 字段）← 调用者: sub_AFFC20

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `equip_set` |  |

## `0xb994c0`（500 字节，2 字段）← 调用者: sub_AFFC50

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `slot` |  |

## `0xb99a20`（498 字节，2 字段）← 调用者: sub_AFFCC0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid_ms` |  |
| 2 | ? | ? | `price` |  |

## `0xb9a4e0`（582 字节，2 字段）← 调用者: sub_AFFDE0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniqid` |  |
| 2 | ? | ? | `total_price` |  |

## `0xb9aa50`（498 字节，2 字段）← 调用者: sub_AFFE50

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `mailid` |  |
| 2 | ? | ? | `pilotid` |  |

## `0xb9bf20`（488 字节，2 字段）← 调用者: sub_B00220

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `box_type` |  |
| 2 | ? | ? | `force_present_get` |  |

## `0xb9c110`（518 字节，2 字段）← 调用者: sub_B00250

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `box_type` |  |
| 2 | ? | ? | `mailid` |  |

## `0xb9c320`（518 字节，2 字段）← 调用者: sub_B002E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `box_type` |  |
| 2 | ? | ? | `mailid` |  |

## `0xb9cb80`（488 字节，2 字段）← 调用者: sub_AFFFA0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `tab_type` |  |
| 2 | ? | ? | `shopitem_id` |  |

## `0xb9f300`（488 字节，2 字段）← 调用者: sub_B00410

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `clan_id` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xb9fad0`（574 字节，2 字段）← 调用者: sub_B004B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `clan_id` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xb9fd10`（488 字节，2 字段）← 调用者: sub_B004E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `clan_id` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba0ad0`（597 字节，2 字段）← 调用者: sub_B00600

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id_new` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba0f50`（681 字节，2 字段）← 调用者: sub_B00660

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `is_active` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba1200`（525 字节，2 字段）← 调用者: sub_B00690

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `intro_info` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba1410`（488 字节，2 字段）← 调用者: sub_B006C0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `pilot_id_kick` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba1600`（611 字节，2 字段）← 调用者: sub_B006F0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | ? | ? | `clan_kind` |  |
| 2 | ? | ? | `search_kind` |  |

## `0xba1a20`（517 字节，2 字段）← 调用者: sub_B00740

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `clan_kind` |  |
| 2 | ? | ? | `sort_info` |  |

## `0xba1de0`（488 字节，2 字段）← 调用者: sub_B00790

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `last_get` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba2280`（500 字节，2 字段）← 调用者: sub_B00800

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `msg_id` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba2480`（500 字节，2 字段）← 调用者: sub_B00830

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `msg_id` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba2680`（515 字节，2 字段）← 调用者: sub_B00860

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `page` |  |
| 2 | ? | ? | `sort_info` |  |

## `0xba2890`（486 字节，2 字段）← 调用者: sub_B008E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `clan_id` |  |
| 2 | ? | ? | `page` |  |

## `0xba2d40`（498 字节，2 字段）← 调用者: sub_B00950

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniq_msid` |  |
| 2 | ? | ? | `decktype` |  |

## `0xba3280`（570 字节，2 字段）← 调用者: sub_B008B0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `shopitemid` |  |
| 2 | ? | ? | `total_price` |  |

## `0xba3820`（515 字节，2 字段）← 调用者: sub_B009E0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `order` |  |
| 2 | ? | ? | `page` |  |

## `0xba3a30`（519 字节，2 字段）← 调用者: sub_B00A10

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `order` |  |
| 2 | ? | ? | `clan_kind` |  |

## `0xba4460`（486 字节，2 字段）← 调用者: sub_B00B10

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `use_bc` |  |
| 2 | ? | ? | `token_id` |  |

## `0xba4d50`（490 字节，2 字段）← 调用者: sub_BAE060

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `debugger_found` |  |
| 2 | ? | ? | `proc_ref_count` |  |

## `0xba4f40`（486 字节，2 字段）← 调用者: sub_B00BB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `factor` |  |
| 2 | ? | ? | `cps_result` |  |

## `0xba52e0`（486 字节，2 字段）← 调用者: 0xb00c1a

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `factor` |  |
| 2 | ? | ? | `cps_result` |  |

## `0xba57d0`（1030 字节，2 字段）← 调用者: 0xb00c98

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `cps_result` |  |
| 2 | ? | ? | `caller_md_size` |  |

## `0xba5be0`（750 字节，2 字段）← 调用者: sub_B00CB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `occured_time` |  |
| 2 | ? | ? | `excode` |  |

## `0xba6890`（616 字节，2 字段）← 调用者: sub_B00DB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | ? | ? | `type` |  |
| 2 | ? | ? | `is_save_db` |  |

## `0xba7770`（515 字节，2 字段）← 调用者: sub_B00A70

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `order` |  |
| 2 | ? | ? | `page` |  |

## `0xba7ce0`（498 字节，2 字段）← 调用者: sub_B00F50

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniq_msid` |  |
| 2 | ? | ? | `level` |  |

## `0xba7ee0`（525 字节，2 字段）← 调用者: sub_B00F80

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniq_msid` |  |
| 2 | ? | ? | `buildup_info` |  |

## `0xba80f0`（498 字节，2 字段）← 调用者: sub_B00FB0

| # | 槽偏移 | 宽度 | 字段名 | 数组 |
|---|---|---|---|---|
| 1 | 0x8 | u32 | `uniq_msid` |  |
| 2 | ? | ? | `item_id` |  |
