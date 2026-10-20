# 归位复核批次 · ref

> 引用未解析：判定 FK 目标或登记为不落库

待判 **65** 项。裁决写回 `schema/homing/_overrides.json`，然后 `python tools/review_homing.py --check`。

| 对象 | 字段 | 原因 | 证据 VA |
|---|---|---|---|
| `AI` | `param_id` | 词干 'param' 无对应对象 | `0xB07283` |
| `activity` | `clan_id` | 词干 'clan' 无对应对象 | `0xb422b5` |
| `adop_list` | `equip_wid` | 词干 'equip_w' 无对应对象 | `0xb43db9` |
| `appear_info` | `arms_id` | 词干 'arms' 无对应对象 | `0xB07FAD` |
| `bgm_desc` | `ace_bgm_id` | 词干 'ace_bgm' 无对应对象 | `B07E36|B0B38F` |
| `bgm_desc` | `field_bgm_id` | 词干 'field_bgm' 无对应对象 | `B07E24|B0B368` |
| `bgm_desc` | `force_bgm_id` | 词干 'force_bgm' 无对应对象 | `B07E48|B0B3B6` |
| `bmgpack` | `shopitem_id` | 词干 'shopitem' 无对应对象 | `0xb458b6` |
| `bonus_info` | `rwd_item_id` | 词干 'rwd_item' 无对应对象 | `0xb4472c` |
| `bracket_info` | `losers_bracket_id` | 词干 'losers_bracket' 无对应对象 | `0xB46E19` |
| `bracket_info` | `winners_bracket_id` | 词干 'winners_bracket' 无对应对象 | `0xB46E07` |
| `bracket_node` | `node_id` | 词干 'node' 无对应对象 | `0xB46FDA` |
| `bracket_node` | `win_team_id` | 词干 'win_team' 无对应对象 | `0xB46FFC` |
| `cinfo` | `clan_id` | 词干 'clan' 无对应对象 | `0xB45940` |
| `cinfo` | `leader_id` | 词干 'leader' 无对应对象 | `0xb45b15` |
| `cinfo` | `npc_id` | 词干 'npc' 无对应对象 | `0xb45988` |
| `comment` | `msg_id` | 词干 'msg' 无对应对象 | `0xb45e3a` |
| `comment` | `npc_id` | 词干 'npc' 无对应对象 | `0xb45ee4` |
| `comment` | `parent_msgid` | 词干 'parent_msg' 无对应对象 | `0xb45e55` |
| `dailycup_conf` | `extrule_id` | 词干 'extrule' 无对应对象 | `B46F8F|B50C82` |
| `dailycup_conf` | `tournament_id` | 词干 'tournament' 无对应对象 | `B46EAF|B50A5F` |
| `favms` | `favorite_ms_id` | 词干 'favorite_ms' 无对应对象 | `` |
| `favms_add` | `favorite_ms_id` | 词干 'favorite_ms' 无对应对象 | `` |
| `hack_check` | `weapon_itemid` | 词干 'weapon_item' 无对应对象 | `0xB06653|B0B9E0` |
| `item_list` | `shopitem_id` | 词干 'shopitem' 无对应对象 | `0xb458b8` |
| `mail` | `attach_id` | 词干 'attach' 无对应对象 | `0xb45881` |
| `ms_rokaku` | `crew_msma_id` | 词干 'crew_msma' 无对应对象 | `0xb06dce` |
| `ms_rokaku` | `eqshield_itemid` | 词干 'eqshield_item' 无对应对象 | `0xb436ff` |
| `ms_rokaku` | `eqspecial_itemid` | 词干 'eqspecial_item' 无对应对象 | `0xb43715` |
| `ms_rokaku` | `eqweapon_itemid` | 词干 'eqweapon_item' 无对应对象 | `0xb436df` |
| `ms_rokaku` | `sitem_id` | 词干 'sitem' 无对应对象 | `0xb06f34` |
| `ms_rokaku` | `spitem_id` | 词干 'spitem' 无对应对象 | `0xb06f49` |
| `ms_rokaku` | `wbu_rapid` | 词干 'wbu_rap' 无对应对象 | `0xb06fa6` |
| `ms_rokaku` | `witem_id` | 词干 'witem' 无对应对象 | `0xb06f14` |
| `lpcard` | `clan_id` | 词干 'clan' 无对应对象 | `0xb43280` |
| `news` | `msg_id` | 词干 'msg' 无对应对象 | `0xB45D3A` |
| `news` | `npc_id` | 词干 'npc' 无对应对象 | `0xB45DDE` |
| `pcard` | `clan_id` | 词干 'clan' 无对应对象 | `0xb42f79` |
| `pcard` | `cupteam_id` | 词干 'cupteam' 无对应对象 | `0xb43019` |
| `pilot` | `clan_id` | 词干 'clan' 无对应对象 | `B8A18E|B08AD0|B06980` |
| `pilot` | `cupteam_id` | 词干 'cupteam' 无对应对象 | `B8A18E|B08AD0|B06980` |
| `pilot_detail` | `check_progress_quest_id` | 词干 'check_progress_quest' 无对应对象 | `0xB42A3D` |
| `pilot_detail` | `clan_id` | 词干 'clan' 无对应对象 | `0xb42688` |
| `pilot_detail` | `cupteam_id` | 词干 'cupteam' 无对应对象 | `0xb426bb` |
| `pilot_detail` | `heroms_uniqid` | 词干 'heroms_uniq' 无对应对象 | `0xB429DD` |
| `pilot_detail` | `monthly_bonus_holding_id` | 词干 'monthly_bonus_holding' 无对应对象 | `0xB42B34` |
| `pilot_detail` | `rokaku_space_uniq_msid` | 词干 'rokaku_space_uniq_ms' 无对应对象 | `0xb428a7` |
| `pilot_detail` | `rokaku_uniq_msid` | 词干 'rokaku_uniq_ms' 无对应对象 | `0xb4288f` |
| `pilots_list` | `clan_id` | 词干 'clan' 无对应对象 | `0xb42f79` |
| `pilots_list` | `cupteam_id` | 词干 'cupteam' 无对应对象 | `0xb43019` |
| `quest_info` | `pay_byword_id` | 词干 'pay_byword' 无对应对象 | `0xB46CA0` |
| `quest_info` | `pay_item_id` | 词干 'pay_item' 无对应对象 | `0xB46C64` |
| `quest_info` | `pay_msma_id` | 词干 'pay_msma' 无对应对象 | `0xB46C8C` |
| `recruit` | `party_id` | 词干 'party' 命中多个对象：['party_member', 'party_member_stat'] | `0xB4542F|B4D840` |
| `recruits` | `party_id` | 词干 'party' 命中多个对象：['party_member', 'party_member_stat'] | `0xb45432` |
| `replay_info` | `missionId` | 词干 'mission' 无对应对象 | `0xB47378|B6FA42` |
| `respawn_post_entry` | `post_chara_id` | 词干 'post_chara' 无对应对象 | `0xB07A28` |
| `result_detail` | `fight_ms_uniqid` | 词干 'fight_ms_uniq' 无对应对象 | `0xb44e84` |
| `result_detail` | `itm_id` | 词干 'itm' 无对应对象 | `0xb44e84` |
| `result_detail` | `no_fight_ms_uniqid` | 词干 'no_fight_ms_uniq' 无对应对象 | `0xb44e84` |
| `result_detail` | `use_buffitem_id` | 词干 'use_buffitem' 无对应对象 | `0xb44e84` |
| `roominfo` | `extrule_id` | 词干 'extrule' 无对应对象 | `0xB44928` |
| `season_rb_conf` | `tournament_id` | 词干 'tournament' 无对应对象 | `0xB4720A|B64D92` |
| `ranking` | `clan_id` | 词干 'clan' 无对应对象 | `0xB465F2` |
| `world_entry` | `icon_id` | 词干 'icon' 无对应对象 | `0xB02EB8` |

裁决写法：`"fk": {"<对象>.<字段>": "<对象>.<列>"}`，或 `"ignore": {"<对象>.<字段>": "<理由>"}` 登记不落库。
