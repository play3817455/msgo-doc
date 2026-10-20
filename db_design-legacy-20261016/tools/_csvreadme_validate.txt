命令目录 915   字段行 3833
列数/表头结构性异常 0
README 无字段表 0   序号对不上 README 的行 13
有差异的行 439

按列差异计数：
  线类型    19
  字段名    1
  含义     75
  用途     321
  取值     55
  证据VA   82

CS-0x050A-lounge-ranking_clan_get:2
    ! 用途: csv='来源=入参 arg_0（`0xBA3AA7 mov edx,dword ptr [esp+arg_0]`，指向该 10B' readme='来源=入参 arg_0（`0xBA3AA7 mov edx,dword ptr [esp+arg_0]`，指向该 10B'
CS-0x2EE7-lounge-friend_xworld_search:3
    ! 用途: csv='经写原语 `sub_B02B40`；服务端据此跨世界搜索该角色；串槽预算 25（`push 19h`）；日志名 `to_' readme='经写原语 `sub_B02B40`；服务端据此跨世界搜索该角色；串槽预算 25（`push 19h`）；日志名 `to_'
CS-0x3E7E-lounge-chat_clan_up:3
    ! 用途: csv='经写原语 `sub_B02B40`；服务端存库并广播到部队频道；串槽预算 181（`push 0B5h`）；日志名 `m' readme='经写原语 `sub_B02B40`；服务端存库并广播到部队频道；串槽预算 181（`push 0B5h`）；日志名 `m'
CS-0x49D1-lounge-clan_invite_pilotlist_get:4
    ! 含义: csv='排序结构（邀请列表短形 9×u8 = 9B；成员名以打印器 `sub_B4EEF0` 为准：sort_type/is_c' readme='排序结构（邀请列表短形 9×u8 = 9B；勿与 clan_search 18B 形混用）'
CS-0x6E16-lounge-party_invite_refuse:6
    ! 取值: csv='取值域 {1,19}（1=手动婉拒 19=自动婉拒）；生产者 `sub_6557F0`/`sub_AF8680`' readme='枚举取值未取证（标 ?）'
CS-0x6E89-lounge-gacha_enter:3
    ! 取值: csv='取值域 {0,1,2,4,5,6}（无 3）；exe 取证 `sub_9955E0` switch + `sub_995' readme='枚举取值未取证（标 ?）'
CS-0x7A7C-lounge-clan_msgboard_news_get:3
    ! 取值: csv='取值域 {0,1}（0=部隊 1=大会チーム）' readme='枚举取值未取证（标 ?）'
CS-0x7ABC-lounge-btlroom_get:3
    ! 取值: csv='取值域 {0,1,2,3}；四调用点绑界面 id 0x5AA/1429/0x59D/0x59E' readme='枚举取值未取证（标 ?）'
CS-0x7B73-lounge-quest_clienttrigger:3
    ! 取值: csv='取值域 {1,2,3,4,5}（无 0）；8 个写侧点：1=登录/主界面 2=编成设定完成 3=教程步进 4=一览/榜打' readme='枚举取值未取证（标 ?）'
CS-0x7D9B-lounge-mail_get_present:4
    ! 取值: csv='不定域：值来自 `IF::CSendMailWindow` 字段 `[this+0x180]`（礼物附件类型选择），ex' readme='枚举取值未取证（标 ?）'
CS-0x817C-lounge-clan_mshipbid_request_cancel:3
    ! 取值: csv='取值域 {0,1}（0=部隊 1=大会チーム）；`sub_63BC20`→0 / `sub_696E20`→1' readme='枚举取值未取证（标 ?）'
CS-0x8196-lounge-clan_rokaku_ms_deck_set:4
    ! 取值: csv='取值域 {0,1}；`sub_831C90` 两分支绑界面按钮 1973056928/867979786' readme='枚举取值未取证（标 ?）'
CS-0x85BF-lounge-mail_get_box:3
    ! 取值: csv='取值域 {0,1,2}（0=主箱 1=系统/礼物 2=运营日志）；`sub_64B510` 三分支' readme='枚举取值未取证（标 ?）'
CS-0x9226-lounge-party_info_edit:5
    ! 取值: csv='取值域 {0,1}（布尔，比较结果直送）' readme='枚举取值未取证（标 ?）'
CS-0xBCB4-battle-commander_support_hit_to:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:7
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:8
    ! 用途: csv='来源=入参 `arg_10`；循环写入（循环上界由前一个计数 `ent_ids_num` 驱动）→ `vt[0x58](' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:9
    ! 用途: csv='来源=入参 `arg_1C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_1C` → 随 `vt[0x58]` 发送'
CS-0xBCB4-battle-commander_support_hit_to:10
    ! 用途: csv='来源=入参 `arg_18`；循环写入（循环上界由前一个计数 `hit_dirs_num` 驱动）→ `vt[0x58]' readme='来源=入参 `arg_18` → 随 `vt[0x58]` 发送'
CS-0xBD2D-lounge-pilot_evflag_3_set:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xBDC5-lounge-msma_energy_charge_deck:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xBDC5-lounge-msma_energy_charge_deck:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xBDD2-battle-game_client_signal:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xBEDC-lounge-xwar_booking_cancel:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xBEE3-battle-weapon_fire__start_homing:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xBEE3-battle-weapon_fire__start_homing:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xBEE3-battle-weapon_fire__start_homing:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xBEE3-battle-weapon_fire__start_homing:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xBEE3-battle-weapon_fire__start_homing:7
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xBEE3-battle-weapon_fire__start_homing:8
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:7
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:8
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:9
    ! 用途: csv='来源=入参 `arg_18`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_18` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:10
    ! 用途: csv='来源=入参 `arg_1C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_1C` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:11
    ! 用途: csv='来源=入参 `arg_20`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_20` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:12
    ! 用途: csv='来源=入参 `arg_24`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_24` → 随 `vt[0x58]` 发送'
CS-0xBFA9-battle-weapon_fire__deploy_arms:13
    ! 用途: csv='来源=入参 `arg_28`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_28` → 随 `vt[0x58]` 发送'
CS-0xC166-battle-eqparts_ready_start:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC166-battle-eqparts_ready_start:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC166-battle-eqparts_ready_start:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC166-battle-eqparts_ready_start:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xC2E9-lounge-msma_equip_bonus_modules_lot_redraw:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xC2E9-lounge-msma_equip_bonus_modules_lot_redraw:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC2E9-lounge-msma_equip_bonus_modules_lot_redraw:5
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:7
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:8
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:9
    ! 用途: csv='来源=入参 `arg_18`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_18` → 随 `vt[0x58]` 发送'
CS-0xC3BD-battle-weapon_fire__snipe_beam:10
    ! 用途: csv='来源=入参 `arg_1C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_1C` → 随 `vt[0x58]` 发送'
CS-0xC3DF-lounge-clan_msgboard_nicecount_add:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xC3DF-lounge-clan_msgboard_nicecount_add:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC40D-lounge-party_booking_ready:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC40D-lounge-party_booking_ready:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC475-lounge-channellobby_scene_transition:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC4A2-lounge-item_use_uniqid_in_battle:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xC4B0-lounge-btlroom_invite_refuse:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC4B0-lounge-btlroom_invite_refuse:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC4B0-lounge-btlroom_invite_refuse:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC59B-lounge-clan_text_notice_set:3
    ! 用途: csv='来源=入参 `arg_0`（`sub_B02B40(src,cursor,maxlen)`，maxlen = 串槽预算）' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC59B-lounge-clan_text_notice_set:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC61E-lounge-gacha_prize_lineup:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC636-lounge-msma_newmark_delete:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xC6E2-lounge-msma_buyback:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xC6E2-lounge-msma_buyback:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC6E3-lounge-clan_memberlist_get:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC84F-battle-bullet_supply_r:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC84F-battle-bullet_supply_r:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:7
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:8
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:9
    ! 用途: csv='来源=入参 `arg_18`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_18` → 随 `vt[0x58]` 发送'
CS-0xC90D-battle-weapon_fire__air_bomb:10
    ! 用途: csv='来源=入参 `arg_1C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_1C` → 随 `vt[0x58]` 发送'
CS-0xC9F9-lounge-shop_sell:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xC9F9-lounge-shop_sell:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xC9F9-lounge-shop_sell:5
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xC9F9-lounge-shop_sell:6
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xC9F9-lounge-shop_sell:7
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:7
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:8
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xCAAE-battle-object_put:9
    ! 用途: csv='来源=入参 `arg_18`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_18` → 随 `vt[0x58]` 发送'
CS-0xCAAF-battle-commander_get_pilotinfo:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xCAAF-battle-commander_get_pilotinfo:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xCB97-battle-game_resume_enter:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xCB97-battle-game_resume_enter:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xCB97-battle-game_resume_enter:5
    ! 用途: csv='来源=入参 `arg_8`（`sub_B02B40(src,cursor,maxlen)`，maxlen = 串槽预算）' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xCB9B-lounge-pilot_comment_edit:3
    ! 用途: csv='来源=入参 `arg_0`（`sub_B02B40(src,cursor,maxlen)`，maxlen = 串槽预算）' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xCBD9-lounge-clan_subleader_set:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xCBD9-lounge-clan_subleader_set:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xCBD9-lounge-clan_subleader_set:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xCC9F-lounge-clan_mshipbid_request:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xCC9F-lounge-clan_mshipbid_request:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xCEF4-lounge-msma_overhaul:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xCEF4-lounge-msma_overhaul:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xCEF4-lounge-msma_overhaul:5
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xCFDB-lounge-msma_energy_charge:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xCFDB-lounge-msma_energy_charge:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xCFDB-lounge-msma_energy_charge:5
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xD12D-lounge-btlroom_quick_start:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD12D-lounge-btlroom_quick_start:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xD12D-lounge-btlroom_quick_start:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xD12D-lounge-btlroom_quick_start:6
    ! 用途: csv='来源=入参 `arg_C`（`sub_B02B40(src,cursor,maxlen)`，maxlen = 串槽预算）' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xD2AE-battle-repair_pack_supply_r:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD2AE-battle-repair_pack_supply_r:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:5
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:6
    ! 用途: csv='来源=入参 `arg_C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_C` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:7
    ! 用途: csv='来源=入参 `arg_10`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_10` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:8
    ! 用途: csv='来源=入参 `arg_14`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_14` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:9
    ! 用途: csv='来源=入参 `arg_18`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_18` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:10
    ! 用途: csv='来源=入参 `arg_1C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_1C` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:11
    ! 用途: csv='来源=入参 `arg_20`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_20` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:12
    ! 用途: csv='来源=入参 `arg_24`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_24` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:13
    ! 用途: csv='来源=入参 `arg_28`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_28` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:14
    ! 用途: csv='来源=入参 `arg_2C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_2C` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:15
    ! 用途: csv='来源=入参 `arg_30`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_30` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:16
    ! 用途: csv='来源=入参 `arg_34`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_34` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:17
    ! 用途: csv='来源=入参 `arg_38`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_38` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:18
    ! 用途: csv='来源=入参 `arg_3C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_3C` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:19
    ! 用途: csv='来源=入参 `arg_40`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_40` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:20
    ! 用途: csv='来源=入参 `arg_44`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_44` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:21
    ! 用途: csv='来源=入参 `arg_48`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_48` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:22
    ! 用途: csv='来源=入参 `arg_4C`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4C` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:23
    ! 用途: csv='来源=入参 `arg_50`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_50` → 随 `vt[0x58]` 发送'
CS-0xD2C3-battle-weapon_fire__grenade:24
    ! 用途: csv='来源=入参 `arg_54`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_54` → 随 `vt[0x58]` 发送'
CS-0xD377-lounge-channellobby_members_get:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD4E5-lounge-btlroom_member_detail_get:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD77C-lounge-clan_search_random:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD7B7-lounge-shop_lineup:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD8A6-lounge-heroms_set:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xD969-lounge-pilot_module_unlock_estimate:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xD9AE-lounge-ranking_pilot_get:3
    ! 用途: csv='来源=入参 `arg_0` 指向的结构体（由复合写入器一次写入）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xDADA-lounge-msma_breakup:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xDAE0-battle-commander_list_get:3
    ! 用途: csv='来源=入参 `arg_0`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_0` → 随 `vt[0x58]` 发送'
CS-0xDAE0-battle-commander_list_get:4
    ! 用途: csv='来源=入参 `arg_4`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_4` → 随 `vt[0x58]` 发送'
CS-0xDC1A-lounge-msma_equip_special_change:3
    ! 用途: csv='来源=入参 `arg_0/4`（低 32 位在前、高 32 位在后两次内联 `mov`）→ `vt[0x58](buf,' readme='来源=入参 `arg_0/4` → 随 `vt[0x58]` 发送'
CS-0xDC1A-lounge-msma_equip_special_change:4
    ! 用途: csv='来源=入参 `arg_8`（写线指令见证据列）→ `vt[0x58](buf,len)` 发送至服务端' readme='来源=入参 `arg_8` → 随 `vt[0x58]` 发送'
CS-0xDD4C-lounge-clan_introduction_set:4
    ! 取值: csv='取值域 {0|1}（0=部隊 1=大会チーム）' readme='?'
CS-0xE1DB-lounge-clan_kick_member:4
    ! 取值: csv='取值域 {0|1}（0=部隊 1=大会チーム）' readme='?'
CS-0xF0FA-lounge-ranking_clan_get_page:5
    ! 取值: csv='取值域 {0|1}（0=部隊 1=大会チーム）' readme='?'
CS-0xFC2B-lounge-player_navi_unlock:4
    ! 取值: csv='取值域 {0|1}（布尔）；`sub_69E6B0`：`entry[120] > sub_60D950(entry[11' readme='枚举取值未取证 `?`'
CS-0xFDE7-lounge-clan_info_get_self:3
    ! 取值: csv='取值域 {0|1}（0=部隊 1=大会チーム）；`sub_63BB90`→0 / `sub_696DA0`→1' readme='枚举取值未取证 `?`'
CS-0xFF32-lounge-gacha_lineup:3
    ! 取值: csv='取值域 {0|1|2|4|5|6}（无 3）' readme='枚举取值未取证 `?`'
SC-0x00C7-lounge-msma_trialms_back_r:3
    ! 用途: csv='交 vt[0x328] 第 1 实参；日志 result=' readme='交给 `vt[0x328]` 第 1 实参（`0xB51E7E`）；日志 `result=`（`0xB51DF5`）'
    ! 证据VA: csv='0xB51CEC|0xB51DE9|0xB51DF5' readme='`0xB51CEC`（`call sub_B02DD0`，内部 `0xB02E0B add dword ptr [eax'
SC-0x00C7-lounge-msma_trialms_back_r:4
    ! 用途: csv='交 vt[0x328] 第 2/3 实参；日志 uniqid_ms=' readme='交给 `vt[0x328]` 第 2/3 实参（`0xB51E66`/`0xB51E73` 压 `[ebx+4]`、`['
SC-0x00C7-lounge-msma_trialms_back_r:5
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x00F0-lounge-msma_weapon_buildup_reset_r:3
    ! 用途: csv='交 vt[0x2D8] 第 1 实参；日志 result=' readme='交 `vt[0x2D8]`（`0xB51C79`）第 1 实参；日志 `result=`（`0xB51BBB`）'
    ! 证据VA: csv='0xB51AA8|0xB02DE9|0xB51BBB' readme='`0xB51AA8`（`call sub_B02DD0`，本体 `0xB02DE9 add dword ptr [eax'
SC-0x00F0-lounge-msma_weapon_buildup_reset_r:4
    ! 用途: csv='交 vt[0x2D8] 第 2/3 实参；日志 uniqid_ms=' readme='交 `vt[0x2D8]` 第 2/3 实参（`0xB51C56`/`0xB51C69` 压 `[eax+4]`、`[e'
SC-0x00F0-lounge-msma_weapon_buildup_reset_r:5
    ! 用途: csv='交 vt[0x2D8] 第 4 实参；日志 item_id=' readme='交 `vt[0x2D8]` 第 4 实参（`0xB51C5A`/`0xB51C68` 压 `[eax]`）；日志 `it'
    ! 证据VA: csv='0xB51B0C|0xB02DE9|0xB51C0E' readme='`0xB51B0C`（`call sub_B02DD0`）；日志 `0xB51C04`~`0xB51C0E`'
SC-0x00F0-lounge-msma_weapon_buildup_reset_r:6
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x0120-battle-entity_msma_show:3
    ! 用途: csv='交 vt[0x174]；日志 ent_id=' readme='交 `vt[0x174]`（`0xB0D473`）；日志 `ent_id=`（`0xB0D419`）'
    ! 证据VA: csv='0xB0D374|0xB02E01|0xB02E0B|0xB0D419' readme='`0xB0D374`（`call sub_B02DF0`，本体 `0xB02E01 mov cx,[ecx]`、`0xB'
SC-0x0120-battle-entity_msma_show:4
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x0124-lounge-xwar_forcegauge_get_r:3
    ! 证据VA: csv='0xB51EF4|0xB02DE9|0xB52079' readme='`0xB51EF4`（`sub_B02DD0`）；`0xB02DE9 add dword ptr [eax], 4`；日'
SC-0x0124-lounge-xwar_forcegauge_get_r:4
    ! 证据VA: csv='0xB51F34|0xB02DE9|0xB520A3' readme='`0xB51F34`（`sub_B02DD0`）；日志 `0xB52094`~`0xB520A3`'
SC-0x0124-lounge-xwar_forcegauge_get_r:5
    ! 含义: csv='当前排名赛期字符串' readme='当前排名赛期（字符串）'
    ! 证据VA: csv='0xB51F55|0xB02BEE|0xB520D0' readme='`0xB51F55`（`call sub_B02BA0`，`0xB51F46 push 41h` 槽上限 65）；rea'
SC-0x0124-lounge-xwar_forcegauge_get_r:6
    ! 含义: csv='上期排名赛期字符串' readme='上期排名赛期（字符串）'
    ! 证据VA: csv='0xB51F76|0xB02BEE|0xB52108' readme='`0xB51F76`（`call sub_B02BA0`，`0xB51F63 push 41h`）；reader 本体 '
SC-0x0124-lounge-xwar_forcegauge_get_r:7
    ! 证据VA: csv='0xB51F9E|0xB02DE9|0xB5213D' readme='`0xB51F9E`（`sub_B02DD0`）；日志 `0xB5212E`~`0xB5213D`'
SC-0x0124-lounge-xwar_forcegauge_get_r:8
    ! 证据VA: csv='0xB51FC6|0xB02E0B|0xB52163' readme='`0xB51FC6`（`sub_B02DF0`）；`0xB02E0B add dword ptr [eax], 2`；日'
SC-0x0124-lounge-xwar_forcegauge_get_r:9
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x0249-lounge-clan_shop_buying_history_update:4
    ! 用途: csv='结构体第 2 成员一并交 vt[0x4A4]；格式串 num=' readme='同上（结构体第 2 成员）；格式串 `num=`（`0xB47AE3`）'
SC-0x0249-lounge-clan_shop_buying_history_update:5
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x02C0-lounge-dailycup_exit_r:3
    ! 用途: csv='交 vt[0x568]；日志 result=' readme='交 `vt[0x568]`（`0xB52366`）；日志 `result=`（`0xB5230D`）'
    ! 证据VA: csv='0xB52263|0xB02DE1|0xB02DE9|0xB5230D' readme='`0xB52263`（`call sub_B02DD0`）；本体 `0xB02DE1`（`mov ecx,[ecx]`）'
SC-0x02C0-lounge-dailycup_exit_r:4
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x02D8-battle-combat_operation_container_collect_r:3
    ! 证据VA: csv='0xB0D18E|0xB02E01|0xB02E0B|0xB0D27E' readme='`0xB0D18E`（`call sub_B02DF0`）；本体 `0xB02E01`（`mov cx,[ecx]`）+'
SC-0x02D8-battle-combat_operation_container_collect_r:4
    ! 证据VA: csv='0xB0D1CE|0xB02DE1|0xB02DE9|0xB0D2A3' readme='`0xB0D1CE`（`call sub_B02DD0`）；本体 `0xB02DE1` + `0xB02DE9`；日志 '
SC-0x02D8-battle-combat_operation_container_collect_r:5
    ! 含义: csv='游标必须==末尾' readme='—'
    ! 用途: csv='-' readme='游标必须 == 末尾'
SC-0x02EE-lounge-item_init_get_r:3
    ! 证据VA: csv='0xB52550|0xB02E0B|0xB52A46' readme='`0xB52550`（`sub_B02DF0`）；`0xB02E0B add [eax],2`；日志 `0xB52A39'
SC-0x02EE-lounge-item_init_get_r:4
    ! 证据VA: csv='0xB52590|0xB02E0B|0xB52A71' readme='`0xB52590`（`sub_B02DF0`）；日志 `0xB52A65`'
SC-0x02EE-lounge-item_init_get_r:5
    ! 含义: csv='垃圾栏槽位数' readme='垃圾（废弃）栏槽位数'
    ! 证据VA: csv='0xB525B4|0xB02E0B|0xB52A9C' readme='`0xB525B4`（`sub_B02DF0`）；日志 `0xB52A90`'
SC-0x02EE-lounge-item_init_get_r:6
    ! 证据VA: csv='0xB525D8|0xB02E0B|0xB52AC7' readme='`0xB525D8`（`sub_B02DF0`）；日志 `0xB52ABB`'
SC-0x02EE-lounge-item_init_get_r:7
    ! 证据VA: csv='0xB52600|0xB02DE9|0xB52AF1' readme='`0xB52600`（`sub_B02DD0`）；`0xB02DE9 add [eax],4`；日志 `0xB52AE6'
SC-0x02EE-lounge-item_init_get_r:8
    ! 用途: csv='交 vt[0x32C]；日志 sort_tm_usec_main=' readme='同上；日志 `sort_tm_usec_main=`（`0xB52B1B`）'
    ! 证据VA: csv='0xB52628|0xB02DE9|0xB52B1B' readme='`0xB52628`（`sub_B02DD0`）；日志 `0xB52B10`'
SC-0x02EE-lounge-item_init_get_r:9
    ! 用途: csv='交 vt[0x32C]；日志 sort_tm_sec_consume=' readme='同上；日志 `sort_tm_sec_consume=`（`0xB52B45`）'
    ! 证据VA: csv='0xB52650|0xB02DE9|0xB52B45' readme='`0xB52650`（`sub_B02DD0`）；日志 `0xB52B3A`'
SC-0x02EE-lounge-item_init_get_r:10
    ! 用途: csv='交 vt[0x32C]；日志 sort_tm_usec_consume=' readme='同上；日志 `sort_tm_usec_consume=`（`0xB52B6F`）'
    ! 证据VA: csv='0xB52678|0xB02DE9|0xB52B6F' readme='`0xB52678`（`sub_B02DD0`）；日志 `0xB52B64`'
