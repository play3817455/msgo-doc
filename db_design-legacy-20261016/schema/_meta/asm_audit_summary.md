# ASM 审计总览

> 生成：2026-09-20 · 工具：`_gen_asm_audit_summary.py`

## 结论

| 指标 | 值 |
|---|---|
| 表（complete） | 73 |
| wire 链 pass | **73/73** |
| wire 链 fail | 0 |
| memory_offset / memory_only 字段 | 533 |
| memory 链 pass | **73/73**（0 无槽差跳过） |
| 审计批次 | #1–#8 complete |

## 逐表

| 表 | composite | ASM | 成员 | mem≠wire | reader | 线长 |
|---|---|---|---:|---:|---|---:|
| `tbl_adop_get` | `adop_get` | ✓ pass | 3 | 2 | `sub_B43D90` | 13 |
| `tbl_adop_list` | `adop_list` | ✓ pass | 3 | 2 | `sub_B43D90` | 13 |
| `tbl_AI` | `AI` | ✓ pass | 29 | 27 | `sub_B07230` | 165 |
| `tbl_appear_info` | `appear_info` | ✓ pass | 17 | 15 | `sub_B07EC0` | 86 |
| `tbl_avatar` | `avatar` | ✓ pass | 10 | 6 | `sub_B068B0` | 18 |
| `tbl_beginner_challenge_info` | `beginner_challenge_info` | ✓ pass | 4 | 1 | `sub_B42440` | 454 |
| `tbl_bgm_desc` | `bgm_desc` | ✓ pass | 5 | 4 | `sub_B07E00` | 14 |
| `tbl_block_detail` | `block_detail` | ✓ pass | 20 | 18 | `sub_B43100` | 113 |
| `tbl_bracket` | `bracket` | ✓ pass | 2 | 1 | `sub_B47060` | 166 |
| `tbl_bracket_info` | `bracket_info` | ✓ pass | 11 | 10 | `sub_B46D80` | 46 |
| `tbl_buffitem` | `buffitem` | ✓ pass | 3 | 0 | `sub_B07E70` | 6 |
| `tbl_buffitem_ex` | `buffitem_ex` | ✓ pass | 3 | 0 | `sub_B07E70` | 6 |
| `tbl_buildup_info` | `buildup_info` | ✓ pass | 2 | 1 | `sub_B44050` | 42 |
| `tbl_challenge_info` | `challenge_info` | ✓ pass | 4 | 0 | `sub_B07540` | 13 |
| `tbl_check_quest` | `check_quest` | ✓ pass | 10 | 8 | `sub_B06C00` | 133 |
| `tbl_cinfo` | `cinfo` | ✓ pass | 25 | 23 | `sub_B45940` | 639 |
| `tbl_clan_eff` | `clan_eff` | ✓ pass | 6 | 0 | `sub_B45F30` | 12 |
| `tbl_clan_zeon` | `clan_zeon` | ✓ pass | 6 | 0 | `sub_B45F30` | 12 |
| `tbl_config` | `config` | ✓ pass | 10 | 9 | `sub_B077B0` | 34 |
| `tbl_dailycup_conf` | `dailycup_conf` | ✓ pass | 14 | 0 | `sub_B46E80` | 73 |
| `tbl_dailycup_conf_next` | `dailycup_conf_next` | ✓ pass | 14 | 0 | `sub_B46E80` | 73 |
| `tbl_dc_point` | `dc_point` | ✓ pass | 7 | 6 | `sub_B47120` | 41 |
| `tbl_dcpoint_detail` | `dcpoint_detail` | ✓ pass | 7 | 6 | `sub_B47120` | 41 |
| `tbl_eq_bonus_modules_lot` | `eq_bonus_modules_lot` | ✓ pass | 3 | 0 | `—` | 12 |
| `tbl_equip_set` | `equip_set` | ✓ pass | 9 | 7 | `—` | 121 |
| `tbl_exam_state` | `exam_state` | ✓ pass | 8 | 0 | `sub_B42330` | 68 |
| `tbl_ext_subrule` | `ext_subrule` | ✓ pass | 2 | 0 | `sub_B456F0` | 20 |
| `tbl_extrarule_xwar_info` | `extrarule_xwar_info` | ✓ pass | 7 | 5 | `sub_B08160` | 514 |
| `tbl_friend_histories` | `friend_histories` | ✓ pass | 20 | 18 | `sub_B43100` | 113 |
| `tbl_funnelss` | `funnelss` | ✓ pass | 3 | 0 | `sub_B081C0` | 10 |
| `tbl_hack_check` | `hack_check` | ✓ pass | 30 | 25 | `—` | 79 |
| `tbl_intro_info` | `intro_info` | ✓ pass | 4 | 0 | `sub_B46140` | 547 |
| `tbl_item` | `item` | ✓ pass | 5 | 0 | `sub_B434F0` | 22 |
| `tbl_item_list` | `item_list` | ✓ pass | 7 | 1 | `sub_B458A0` | 23 |
| `tbl_leaders` | `leaders` | ✓ pass | 7 | 2 | `sub_B454D0` | 52 |
| `tbl_lpcard` | `lpcard` | ✓ pass | 20 | 18 | `sub_B43100` | 113 |
| `tbl_lvjudge_hist` | `lvjudge_hist` | ✓ pass | 8 | 1 | `sub_B44750` | 369 |
| `tbl_member` | `member` | ✓ pass | 7 | 2 | `sub_B454D0` | 52 |
| `tbl_missionunit_set` | `missionunit_set` | ✓ pass | 3 | 0 | `sub_B43BE0` | 12 |
| `tbl_mprogress` | `mprogress` | ✓ pass | 14 | 6 | `sub_B07880` | 46 |
| `tbl_ms` | `ms` | ✓ pass | 43 | 42 | `sub_B06D80` | 244 |
| `tbl_ms_set` | `ms_set` | ✓ pass | 6 | 0 | `sub_B43B00` | 95 |
| `tbl_netcafe_challenge_info` | `netcafe_challenge_info` | ✓ pass | 4 | 0 | `sub_B07540` | 13 |
| `tbl_order` | `order` | ✓ pass | 5 | 0 | `sub_B46420` | 10 |
| `tbl_party_member_stat` | `party_member_stat` | ✓ pass | 7 | 5 | `sub_B432C0` | 31 |
| `tbl_pcard` | `pcard` | ✓ pass | 58 | 56 | `sub_B42BB0` | 398 |
| `tbl_phase_info` | `phase_info` | ✓ pass | 4 | 3 | `sub_B46D20` | 13 |
| `tbl_pilot` | `pilot` | ✓ pass | 24 | 18 | `sub_B06980` | 159 |
| `tbl_pilot_detail` | `pilot_detail` | ✓ pass | 53 | 46 | `sub_B42640` | 51672 |
| `tbl_pilots_list` | `pilots_list` | ✓ pass | 58 | 56 | `sub_B42BB0` | 398 |
| `tbl_pointdmg` | `pointdmg` | ✓ pass | 1 | 0 | `sub_B45760` | 12 |
| `tbl_precord` | `precord` | ✓ pass | 61 | 8 | `sub_B440B0` | 242 |
| `tbl_progress` | `progress` | ✓ pass | 14 | 6 | `sub_B07880` | 46 |
| `tbl_ranking` | `ranking` | ✓ pass | 12 | 7 | `sub_B46560` | 95 |
| `tbl_ranking_info` | `ranking_info` | ✓ pass | 5 | 0 | `sub_B46420` | 10 |
| `tbl_rankself` | `rankself` | ✓ pass | 6 | 0 | `sub_B464A0` | 40 |
| `tbl_recruit` | `recruit` | ✓ pass | 7 | 4 | `sub_B45400` | 74 |
| `tbl_recruits` | `recruits` | ✓ pass | 9 | 6 | `sub_B45400` | 80 |
| `tbl_replay_info` | `replay_info` | ✓ pass | 10 | 5 | `sub_B47340` | 38 |
| `tbl_roominfo` | `roominfo` | ✓ pass | 15 | 13 | `sub_B44880` | 135 |
| `tbl_season_rb_conf` | `season_rb_conf` | ✓ pass | 10 | 0 | `sub_B471E0` | 52 |
| `tbl_snapshot` | `snapshot` | ✓ pass | 21 | 4 | `sub_B075A0` | 39 |
| `tbl_sort_info` | `sort_info` | ✓ pass | 12 | 2 | `sub_B461E0` | 18 |
| `tbl_special_a_info` | `special_a_info` | ✓ pass | 6 | 0 | `sub_B464A0` | 40 |
| `tbl_special_a_next` | `special_a_next` | ✓ pass | 3 | 0 | `sub_B46CD0` | 12 |
| `tbl_toppilots` | `toppilots` | ✓ pass | 12 | 7 | `sub_B46560` | 95 |
| `tbl_total_result_wave` | `total_result_wave` | ✓ pass | 7 | 4 | `sub_B45580` | 19 |
| `tbl_trchallenge_info` | `trchallenge_info` | ✓ pass | 4 | 0 | `sub_B07540` | 13 |
| `tbl_unlocked_navi` | `unlocked_navi` | ✓ pass | 2 | 0 | `sub_B434B0` | 8 |
| `tbl_unlockw` | `unlockw` | ✓ pass | 6 | 0 | `sub_B439D0` | 30 |
| `tbl_wave_res` | `wave_res` | ✓ pass | 15 | 12 | `sub_B08020` | 34 |
| `tbl_wbonus` | `wbonus` | ✓ pass | 3 | 0 | `sub_B453B0` | 4 |
| `tbl_xwar_ext_rule` | `xwar_ext_rule` | ✓ pass | 7 | 5 | `sub_B08160` | 514 |

## 批次队列

- **Batch #1** · 2026-09-20 · pass 10/10
- **Batch #2** · 2026-09-20 · pass 10/10
- **Batch #3** · 2026-09-20 · pass 10/10
- **Batch #4** · 2026-09-20 · pass 10/10
- **Batch #5** · 2026-09-20 · pass 10/10
- **Batch #6** · 2026-09-20 · pass 10/10
- **Batch #7** · 2026-09-20 · pass 10/10
- **Batch #8** · 2026-09-20 · pass 3/3

## 相关文档

- `asm_chain_remediation.md` — wire vs memory 修法
- `asm_audit_batch01.md` … `asm_audit_batch08.md` — 分批取证记录

