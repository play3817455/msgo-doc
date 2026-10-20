# 汇编证据 —— SC-0x063E-lounge-pilot_select_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0xDB85` = 56197）

```asm
; VA: 0xB53684 .. 0xB536B3
0xB53684  push    16h                      ; ← 本 case 错误码
0xB53686  mov     ecx, esi
0xB53688  call    sub_B41120
0xB5368D  test    al, al
0xB5368F  jz      loc_B890FE
0xB53695  mov     ecx, [esi+0Ch]
0xB53698  mov     eax, [ecx]
0xB5369A  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB5369D  push    0DB85h                   ; ← 容量 56197（= Σ各字段 claim，≠ 线长）
0xB536A2  call    edx
0xB536A4  mov     [esp+2C5Ch+var_2C28], eax ; 缓冲基址（= 缓冲游标起点）
0xB536A8  mov     eax, [esi+0Ch]
0xB536AB  push    eax
0xB536AC  lea     ecx, [esp+2C60h+var_2BD8]
0xB536B3  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 字段 1 ~ 6（28B）

```asm
; VA: 0xB536CC .. 0xB537E1
0xB536CC  call    sub_B41470               ; 预留 4B（非字段）
0xB536DB  call    sub_B02DD0               ; ① result（u32，槽 var_2C24）
0xB53709  call    sub_B41470
0xB53718  call    sub_B02DD0               ; ② restore_channel（u32，槽 var_2C04）
0xB53730  call    sub_B41470
0xB53742  call    sub_B02DD0               ; ③ charge_point（u32，槽 var_2BC8）
0xB5375A  call    sub_B41470
0xB5376C  call    sub_B02DD0               ; ④ tuto_step（u32，槽 var_2BCC）
0xB53785  call    sub_B41A10               ; 预留 8B（非字段）
0xB53794  call    sub_B06200               ; ⑤ tuto_flags（u64，槽 var_2C3C）
0xB537C5  call    sub_B41470
0xB537D7  call    sub_B02DD0               ; ⑥ tuto_missionid（u32，槽 var_2BD0）
```

## E3 字段 7：`pilot_detail`（缓冲 claim `0xDB10` + 复合读取器 `sub_B42640`）

```asm
; VA: 0xB537E3 .. 0xB53807（调用点）
0xB537E3  lea     eax, [esp+2C5Ch+var_2C28]
0xB537E7  push    eax                         ; arg_0 = &缓冲游标
0xB537E8  lea     ecx, [esp+2C60h+var_2BD4]   ; this = &结构体槽
0xB537EF  call    sub_B41260                  ; ← 缓冲预留：claim 0xDB10 = 56080B
0xB537FB  lea     ecx, [esp+2C5Ch+var_2C44]   ; 线游标
0xB53800  push    edx
0xB53801  call    sub_B42640                  ; ← 复合读取器（pilot_detail，消费 51672B）
```

预留器本体（claim 量取证）：

```asm
; VA: 0xB41260 .. 0xB41270
0xB41260  mov     eax, ecx
0xB41262  mov     ecx, [esp+arg_0]
0xB41266  mov     edx, [ecx]
0xB41268  mov     [eax], edx
0xB4126A  add     dword ptr [ecx], 0DB10h  ; ← 结构体 claim = 56080 字节（≠ 线长 51672）
0xB41270  retn    4
```

**函数边界（关键）**：`sub_B42640` = `0xB42640..0xB42BA3`（1379B / 464 条指令，`ida_funcs.get_func()` 实测）。
其「失败出口」在 `0xB42796` / `0xB42799`，**成功路径从 `0xB4279B` 起**并继续读取到函数末尾。

```asm
; VA: 0xB42640 .. 0xB42790（头部 17 个标量，线长 64）
0xB42653  mov     edx, [eax]
0xB4265A  mov     [edi], edx                ; exp（mem +0）
0xB4266F  mov     [edi+4], edx              ; money（mem +4）
0xB42685  mov     [edi+8], edx              ; clan_id（mem +8）
0xB4269F  mov     [edi+0Ch], edx            ; clan_memb_exp（mem +0Ch）
0xB426A6  call    sub_B02DD0                ; clan_forbidden（mem +10h）
0xB426BB  call    sub_B02DD0                ; cupteam_id（mem +14h）
0xB426D0  call    sub_B02DF0                ; deckcost（mem +18h，u16）
0xB426E5  call    sub_B02DD0                ; last_battle（mem +1Ch）
0xB426FA  call    sub_B02DD0                ; cw_chscore（mem +20h）
0xB4270F  call    sub_B02DD0                ; score_special_a（mem +24h）
0xB42720  call    sub_B02DD0                ; last_play_bonus（mem +28h）
0xB42731  call    sub_B02DD0                ; last_play_bonus_vsl（mem +2Ch）
0xB42742  call    sub_B02DF0                ; last_play_bonus_vsl_cnt（mem +30h，u16）
0xB42753  call    sub_B02DD0                ; last_dormant_ret_cc（mem +34h）
0xB42764  call    sub_B02DD0                ; capture_bonus_state（mem +38h）
0xB42775  call    sub_B02DD0                ; capture_bonus_limit（mem +3Ch）
0xB42786  call    sub_B02DD0                ; clan_rokaku_btime_limit（mem +40h）
0xB42790  jnz     short loc_B4279B
```

```asm
; VA: 0xB42792 .. 0xB4279A（失败出口）
0xB42792  pop     edi
0xB42793  xor     al, al
0xB42796  retn
0xB42797  xor     al, al
0xB4279A  retn
```

```asm
; VA: 0xB4279B .. 0xB42B7A（**成功路径**：定长数组 + 标量 + 嵌套读取器）
0xB427A0  lea     ecx, [edi+ebx+44h]        ; comment：u8 × 0x73 = 115B（mem +44h）
0xB427A6  call    sub_B06230
0xB427B9  cmp     ebx, 73h
0xB427BC  jb      short loc_B427A0
0xB427C1  lea     ebp, [edi+0B8h]           ; hav_medal：u64 × 0x10 = 128B（mem +0B8h）
0xB427C9  call    sub_B06200
0xB427DF  cmp     ebx, 10h
0xB427E6  lea     ebp, [edi+138h]           ; hav_emblem：u64 × 8 = 64B（mem +138h）
0xB42808  cmp     ebx, 8
0xB4280F  lea     ebp, [edi+178h]           ; hav_avatar：u64 × 0A0h = 1280B（mem +178h）
0xB4282D  cmp     ebx, 0A0h
0xB42837  lea     ebp, [edi+678h]           ; hav_voice：u64 × 8 = 64B（mem +678h）
0xB42858  cmp     ebx, 8
0xB4285F  lea     ecx, [edi+6B8h]           ; hav_modules：u32 × 80h = 512B（mem +6B8h）
0xB42880  cmp     eax, 80h
0xB4288F  call    sub_B42330                ; examination_state（68B，mem +8B8h）
0xB428A7  call    sub_B06200                ; rokaku_uniq_msid（u64，mem +900h）
0xB428BF  call    sub_B06200                ; rokaku_space_uniq_msid（u64，mem +908h）
0xB428D7  call    sub_B02DD0                ; rokaku_pt（u32，mem +910h）
0xB428EF  call    sub_B02DD0                ; rokaku_pt_use（u32，mem +914h）
0xB42907  call    sub_B423F0                ; cshist（192B，mem +918h）
0xB4291F  call    sub_B06230                ; second_chance_free（u8，mem +0A18h）
0xB42937  call    sub_B02DD0                ; second_chance_free_upd（u32，mem +0A1Ch）
0xB42950  call    sub_B434B0                ; hav_rental_modules：8B × 80h = 1024B（mem +0A20h）
0xB4296E  cmp     ebx, 80h
0xB42978  call    sub_B02DD0                ; dc_point（u32，mem +0E20h）
0xB42990  call    sub_B424D0                ; favms_arr：66B × 2D0h = 47520B（mem +0E24h，步进 0x48）
0xB429AE  cmp     ebx, 2D0h
0xB429B8  call    sub_B02DD0                ; heroms_grants：u32 × 0Ah = 40B（mem +0D8A4h）
0xB429D3  cmp     ebx, 0Ah
0xB429DD  call    sub_B06200                ; heroms_uniqid（u64，mem +0D8D0h）
0xB429F5  call    sub_B02DD0                ; last_period_bonus（mem +0D8D8h）
0xB42A0D  call    sub_B02DD0                ; daily_battle_bonus_flg（mem +0D8DCh）
0xB42A25  call    sub_B02DD0                ; last_daily_battle_bonus（mem +0D8E0h）
0xB42A3D  call    sub_B02DD0                ; check_progress_quest_id（mem +0D8E4h）
0xB42A57  call    sub_B02DF0                ; lvjudge_hist：u16 × 1 = 2B（mem +0D8E8h）
0xB42A7A  call    sub_B02DD0                ; pilot_made_timestamp（mem +0D8ECh）
0xB42A92  call    sub_B02DF0                ; newpilot_challenge_nextindex（mem +0D8F0h）
0xB42AAA  call    sub_B02DD0                ; newpilot_challenge_last（mem +0D8F4h）
0xB42AC4  call    sub_B02DF0                ; sc_lv_up_reward_get：u16 × 13h = 38B（mem +0D8F8h）
0xB42ADD  cmp     ebx, 13h
0xB42AE9  call    sub_B02DF0                ; sc_lv_max_pre：u16 × 0Ch = 24B（mem +0D91Eh）
0xB42B02  cmp     ebx, 0Ch
0xB42B0C  call    sub_B02DF0                ; sc_lv_max（mem +0D936h）
0xB42B20  call    sub_B02DD0                ; last_pilot_channel_in（mem +0D938h）
0xB42B34  call    sub_B02DF0                ; monthly_bonus_holding_id（mem +0D93Eh 前）
0xB42B48  call    sub_B02DF0                ; monthly_bonus_logincnt
0xB42B5C  call    sub_B02DF0                ; monthly_bonus_xwarcnt
0xB42B70  call    sub_B02DD0                ; periodpath_end（mem +0D944h）
0xB42B7A  jnz     short loc_B42B89
```

```asm
; VA: 0xB42B89 .. 0xB42BA2（末字段 beginner_challenge_info + 返回）
0xB42B89  push    esi
0xB42B8A  add     edi, 0D948h
0xB42B90  push    edi
0xB42B91  call    sub_B42440                ; beginner_challenge_info（454B，mem +0D948h）
0xB42B9E  setnz   al
0xB42BA2  retn
```

## E4 `pilot_detail` 的 7 个被调读取器（全函数体已核对）

| 读取器 | 函数体 | 消费（线字节） | 说明 |
|---|---|---|---|
| `sub_B42330` | `0xB42330..0xB423EC` | **68** | 4×u32 直拷 + 2×u32(`sub_B02DD0`) + 5×`sub_B434B0`(40) + u32 直拷 |
| `sub_B423F0` | `0xB423F0..0xB42438` | **192** | 32 × {u32, u16}（`0xB4240C` u32 / `0xB4241F` u16） |
| `sub_B434B0` | `0xB434B0..0xB434E2` | **8** | 2 × u32 |
| `sub_B424D0` | `0xB424D0..0xB4263F` | **66** | 16 × u32 + 2 × u8（`favms_arr` 元素） |
| `sub_B42440` | `0xB42440..0xB424CE` | **454** | u32 + u16 + 32×u16(64) + 96×u32(384) |
| `sub_B06200` | `0xB06200..0xB06226` | **8** | u64（`+8`） |
| `sub_B02BA0` | `0xB02BA0..0xB02BF5` | `L+1` | NUL 串：`sub_CC8400` 找 NUL → `esi+1`；`0xB02BEE mov [edi],esi`（游标 = NUL+1） |

## E5 `pilot_detail` 线长核算（**51672**）

| # | 项 | 字节 |
|---|---|---|
| 1–17 | 头部 17 个标量（4×4 + 2 + 4×9 + 2 + …，见 E3 头部） | 64 |
| 18 | `comment` u8 × 115 | 115 |
| 19 | `hav_medal` u64 × 16 | 128 |
| 20 | `hav_emblem` u64 × 8 | 64 |
| 21 | `hav_avatar` u64 × 160 | 1280 |
| 22 | `hav_voice` u64 × 8 | 64 |
| 23 | `hav_modules` u32 × 128 | 512 |
| 24 | `examination_state`（`sub_B42330`） | 68 |
| 25–26 | `rokaku_uniq_msid` / `rokaku_space_uniq_msid`（u64 × 2） | 16 |
| 27–28 | `rokaku_pt` / `rokaku_pt_use` | 8 |
| 29 | `cshist`（`sub_B423F0`） | 192 |
| 30 | `second_chance_free` | 1 |
| 31 | `second_chance_free_upd` | 4 |
| 32 | `hav_rental_modules`（`sub_B434B0` × 128） | 1024 |
| 33 | `dc_point` | 4 |
| 34 | `favms_arr`（`sub_B424D0` × 720 = 66 × 720） | 47520 |
| 35 | `heroms_grants` u32 × 10 | 40 |
| 36 | `heroms_uniqid` | 8 |
| 37–40 | `last_period_bonus` / `daily_battle_bonus_flg` / `last_daily_battle_bonus` / `check_progress_quest_id` | 16 |
| 41 | `lvjudge_hist` u16 × 1 | 2 |
| 42 | `pilot_made_timestamp` | 4 |
| 43 | `newpilot_challenge_nextindex` | 2 |
| 44 | `newpilot_challenge_last` | 4 |
| 45 | `sc_lv_up_reward_get` u16 × 19 | 38 |
| 46 | `sc_lv_max_pre` u16 × 12 | 24 |
| 47 | `sc_lv_max` | 2 |
| 48 | `last_pilot_channel_in` | 4 |
| 49–51 | `monthly_bonus_holding_id` / `logincnt` / `xwarcnt` | 6 |
| 52 | `periodpath_end` | 4 |
| 53 | `beginner_challenge_info`（`sub_B42440`） | 454 |
| | **合计** | **51672** ✓ |

结构体跨度校验（claim `0xDB10` = 56080）：末成员 `beginner_challenge_info` 位于 `mem +0D948h`、跨度 456B ⇒ `0D948h + 0x1C8 = 0xDB10` = claim ✓

## E6 字段 8 ~ 14（u8/u32 混排，19B）

```asm
; VA: 0xB5380D .. 0xB5391F
0xB53825  call    sub_B06230               ; ⑧ is_netcafe（u8，槽 var_2BEC）
0xB5384D  call    sub_B06230               ; ⑨ is_processing_comeback（u8，槽 var_2BF0）
0xB53875  call    sub_B02DD0               ; ⑩ vip_lv（u32，槽 var_2BFC）
0xB5389D  call    sub_B06230               ; ⑪ overplay_type（u8，槽 var_2C08）
0xB538C5  call    sub_B02DD0               ; ⑫ accum_playtime（u32，槽 var_2C0C）
0xB538ED  call    sub_B02DD0               ; ⑬ daily_compcnt（u32，槽 var_2C30）
0xB53915  call    sub_B02DD0               ; ⑭ ncafe_compcnt（u32，槽 var_2C34）
```

## E7 字段 15 ~ 17 + 长度闭合

```asm
; VA: 0xB53925 .. 0xB539A8
0xB5392B  add     eax, 41h                    ; 串槽推进 65
0xB53932  push    41h                         ; ← 槽位预算 65（上限，不是串长）
0xB5393E  call    sub_B02BA0                  ; ⑮ heroms_term（消费 = L+1）
0xB53966  call    sub_B06230                  ; ⑯ flag_wideuse（u8，槽 var_2C38）
0xB5398E  call    sub_B02DD0                  ; ⑰ level_point（u32，槽 var_2C48）
0xB5399E  mov     ecx, [esp+2C5Ch+var_2C44]   ; 读完后的游标
0xB539A2  cmp     ecx, [esp+2C5Ch+var_2C40]   ; vs 报文末尾
0xB539A8  jz      short loc_B539C1            ; ← 不等 ⇒ push 16h 报错
```

## E8 NUL 串读取器 `sub_B02BA0`（消费 = 串长 + 1）

```asm
; VA: 0xB02BA0 .. 0xB02BF4
0xB02BA9  mov     ecx, [edi]                  ; 游标
0xB02BAB  mov     eax, [edi+4]
0xB02BAE  sub     eax, ecx                    ; 剩余 = end - cur
0xB02BB0  cmp     edx, eax                    ; edx = 槽位预算
0xB02BB2  jge     short loc_B02BB6
0xB02BB4  mov     eax, edx                    ; 取 min(预算, 剩余)
0xB02BC3  call    sub_CC8400                  ; ← 在范围内找 NUL，返回其地址（esi）
0xB02BDC  add     esi, 1                      ; ← 串尾 = NUL + 1
0xB02BDF  mov     ecx, esi
0xB02BE1  sub     ecx, eax                    ; 长度 = (NUL+1) - cur
0xB02BE6  call    sub_CC56B0                  ; memcpy 到串槽
0xB02BEE  mov     [edi], esi                  ; ← 游标推进 = 串长 + 1
0xB02BF1  mov     al, 1
```

## E9 含义取证：块内 18 条日志格式串（顺序 == 线序）

```asm
; VA: 0xB53A3B .. 0xB53CF0
0xB53A3B  push    offset aResult             ; "result="
0xB53A65  push    offset aRestoreChannel     ; "restore_channel="
0xB53A92  push    offset aChargePoint        ; "charge_point="
0xB53ABF  push    offset aTutoStep           ; "tuto_step="
0xB53AE9  push    offset aTutoFlags          ; "tuto_flags="（u64 打印器 sub_B08500）
0xB53B16  push    offset aTutoMissionid      ; "tuto_missionid="
0xB53B41  push    offset aPilotDetail        ; "pilot_detail="（打印器 sub_B48010）
0xB53B6B  push    offset aIsNetcafe          ; "is_netcafe="（布尔打印器 sub_B0C1F0）
0xB53B95  push    offset aIsProcessingCo     ; "is_processing_comeback="
0xB53BC1  push    offset aVipLv              ; "vip_lv="
0xB53BE9  push    offset aOverplayType       ; "overplay_type="
0xB53C15  push    offset aAccumPlaytime      ; "accum_playtime="
0xB53C3F  push    offset aDailyCompcnt       ; "daily_compcnt="
0xB53C69  push    offset aNcafeCompcnt       ; "ncafe_compcnt="
0xB53C96  push    offset aHeromsTerm         ; "heroms_term=\""
0xB53CC9  push    offset aFlagWideuse        ; "flag_wideuse="
0xB53CF0  push    offset aLevelPoint         ; "level_point="
```

## E10 含义取证：`pilot_detail` 及其内嵌结构的打印器

```asm
; VA: 0xB48010 .. 0xB48C01（sub_B48010，904 条指令；节选）
0xB48032  push    offset aExp                ; "exp="（mem +0）
0xB48059  push    offset aMoney              ; "money="（+4）
0xB48080  push    offset aClanId             ; "clan_id="（+8）
0xB480A7  push    offset aClanMembExp        ; "clan_memb_exp="（+0Ch）
0xB480CE  push    offset aClanForbidden      ; "clan_forbidden="（+10h）
0xB480F5  push    offset aCupteamId          ; "cupteam_id="（+14h）
0xB4811D  push    offset aDeckcost           ; "deckcost="（+18h，u16）
0xB48144  push    offset aLastBattle         ; "last_battle="（+1Ch）
0xB4816B  push    offset aCwChscore          ; "cw_chscore="（+20h）
0xB48192  push    offset aScoreSpecialA      ; "score_special_a="（+24h）
0xB481B9  push    offset aLastPlayBonus      ; "last_play_bonus="（+28h）
0xB481E0  push    offset aLastPlayBonusV     ; "last_play_bonus_vsl="（+2Ch）
0xB48208  push    offset aLastPlayBonusV_0   ; "last_play_bonus_vsl_cnt="（+30h，u16）
0xB4822F  push    offset aLastDormantRet     ; "last_dormant_ret_cc="（+34h）
0xB48256  push    offset aCaptureBonusSt     ; "capture_bonus_state="（+38h）
0xB4827D  push    offset aCaptureBonusLi     ; "capture_bonus_limit="（+3Ch）
0xB482A4  push    offset aClanRokakuBtim     ; "clan_rokaku_btime_limit="（+40h）
0xB482CB  push    offset aComment            ; "comment="（+44h；此处为**定长 115B 字节块**，按串打印）
0xB482F9  push    offset aHavMedal           ; "hav_medal={"（+0B8h，循环 0Fh+1=16）
0xB4836E  push    offset aHavEmblem          ; "hav_emblem={"（+138h，循环 7+1=8）
0xB483DE  push    offset aHavAvatar          ; "hav_avatar={"（+178h，循环 9Fh+1=160）
0xB4844E  push    offset aHavVoice           ; "hav_voice={"（+678h，循环 7+1=8）
0xB484B7  push    offset aHavModules         ; "hav_modules={"（+6B8h，循环 7Fh+1=128）
0xB4851F  push    offset aExaminationSta     ; "examination_state="（+8B8h → sub_B47910）
0xB48552  push    offset aRokakuUniqMsid     ; "rokaku_uniq_msid="（+900h）
0xB48583  push    offset aRokakuSpaceUni     ; "rokaku_space_uniq_msid="（+908h）
0xB485AD  push    offset aRokakuPt           ; "rokaku_pt="（+910h）
0xB485D7  push    offset aRokakuPtUse        ; "rokaku_pt_use="（+914h）
0xB48601  push    offset aCshist             ; "cshist="（+918h → sub_B47B10 → sub_B47AA0）
0xB4862E  push    offset aSecondChanceFr     ; "second_chance_free="（+0A18h）
0xB48658  push    offset aSecondChanceFr_0   ; "second_chance_free_upd="（+0A1Ch）
0xB48673  push    offset aHavRentalModul     ; "hav_rental_modules={"（+0A20h，循环 7Fh+1=128）
0xB4878B  push    offset aDcPoint            ; "dc_point="（+0E20h）
0xB487B0  push    offset aFavmsArr           ; "favms_arr={"（+0E24h → sub_B47CC0，循环 2CFh+1=720）
0xB48815  push    offset aHeromsGrants       ; "heroms_grants={"（+0D8A4h，循环 9+1=10）
0xB48884  push    offset aHeromsUniqid       ; "heroms_uniqid="（+0D8D0h）
0xB488AE  push    offset aLastPeriodBonu     ; "last_period_bonus="（+0D8D8h）
0xB488D8  push    offset aDailyBattleBon     ; "daily_battle_bonus_flg="（+0D8DCh）
0xB48902  push    offset aLastDailyBattl     ; "last_daily_battle_bonus="（+0D8E0h）
0xB4892C  push    offset aCheckProgressQ     ; "check_progress_quest_id="（+0D8E4h）
0xB48952  push    offset aLvjudgeHist        ; "lvjudge_hist={"（+0D8E8h）
0xB4898F  push    offset aPilotMadeTimes     ; "pilot_made_timestamp="（+0D8ECh）
0xB489BA  push    offset aNewpilotChalle     ; "newpilot_challenge_nextindex="（+0D8F0h）
0xB489E4  push    offset aNewpilotChalle_0   ; "newpilot_challenge_last="（+0D8F4h）
0xB48A0A  push    offset aScLvUpRewardGe     ; "sc_lv_up_reward_get={"（+0D8F8h，循环 12h+1=19）
0xB48A75  push    offset aScLvMaxPre         ; "sc_lv_max_pre={"（+0D91Eh，循环 0Bh+1=12）
0xB48ADF  push    offset aScLvMax            ; "sc_lv_max="（+0D936h）
0xB48B09  push    offset aLastPilotChann     ; "last_pilot_channel_in="（+0D938h）
0xB48B34  push    offset aMonthlyBonusHo     ; "monthly_bonus_holding_id="（+0D93Ch）
0xB48B5F  push    offset aMonthlyBonusLo     ; "monthly_bonus_logincnt="（+0D93Eh）
0xB48B8A  push    offset aMonthlyBonusXw     ; "monthly_bonus_xwarcnt="（+0D940h）
0xB48BB4  push    offset aPeriodpathEnd      ; "periodpath_end="（+0D944h）
0xB48BD9  push    offset aBeginnerChalle     ; "beginner_challenge_info="（+0D948h → sub_B47B90）
```

```asm
; sub_B47910（examination_state 打印器，0xB47910..0xB47A9F）
0xB47932  push    offset aState              ; "state="（+0）
0xB47959  push    offset aChancesUsed        ; "chances_used="（+4）
0xB47980  push    offset aChancesTotal       ; "chances_total="（+8）
0xB479A7  push    offset aPlaysecTotal       ; "playsec_total="（+0Ch）
0xB479CE  push    offset aPlaysecElapsed     ; "playsec_elapsed="（+10h）
0xB479F5  push    offset aPlayscoreSum       ; "playscore_sum="（+14h）
0xB47A17  push    offset aExaminationLis     ; "examination_list={"（+18h，5 元素）
0xB47A76  push    offset aIntervalCnt        ; "interval_cnt="（+40h）
; sub_B478A0（examination_list 元素）
0xB478C0  push    offset aId_0               ; "id="（u32）
0xB478E2  push    offset aGainVal            ; "gain_val="（u32）
; sub_B47AA0（cshist 元素）
0xB47AC0  push    offset aItemId             ; "item_id="（u32）
0xB47AE3  push    offset aNum               ; "num="（u16）
; sub_B47CC0（favms_arr 元素，0xB47CC0..0xB47F9B）
0xB47CE0  push    offset aPilotId            ; "pilot_id="（+0，u32）
0xB47D07  push    offset aFavoriteMsId       ; "favorite_ms_id="（+4）
0xB47D2F  push    offset aBattleRule         ; "battle_rule="（+8，u8）
0xB47D56  push    offset aFavoriteExpSum     ; "favorite_exp_sum="（+0Ch）
0xB47D7D  push    offset aKillCnt            ; "kill_cnt="（+10h）
0xB47DA4  push    offset aKillAssistCnt      ; "kill_assist_cnt="（+14h）
0xB47DCB  push    offset aResurrectCnt       ; "resurrect_cnt="（+18h）
0xB47DF2  push    offset aStgholdDamage      ; "stghold_damage="（+1Ch）
0xB47E19  push    offset aBattleCnt          ; "battle_cnt="（+20h）
0xB47E40  push    offset aScoreMaxAtk        ; "score_max_atk="（+24h）
0xB47E67  push    offset aScoreMaxSpt        ; "score_max_spt="（+28h）
0xB47E8E  push    offset aScoreMaxCon        ; "score_max_con="（+2Ch）
0xB47EB5  push    offset aScoreSumAtk        ; "score_sum_atk="（+30h）
0xB47EDC  push    offset aScoreSumSpt        ; "score_sum_spt="（+34h）
0xB47F03  push    offset aScoreSumCon        ; "score_sum_con="（+38h）
0xB47F2A  push    offset aScoreSumSum        ; "score_sum_sum="（+3Ch）
0xB47F51  push    offset aLastUpdate         ; "last_update="（+40h）
0xB47F74  push    offset aDirtyFlag          ; "dirty_flag="（+44h，u8）
; sub_B47B90（beginner_challenge_info 打印器）
0xB47BB2  push    offset aBeginTime          ; "begin_time="（+0，u32）
0xB47BDA  push    offset aElapsedDays        ; "elapsed_days="（+4，u16）
0xB47BFD  push    offset aArchived           ; "archived={"（+6，32×u16）
0xB47C61  push    offset aValue_0            ; "value={"（+48h，96×u32）
```

## E11 去向：`vt[0x94]`（18 个实参，压栈 = 逆序）

```asm
; VA: 0xB53D3C .. 0xB53DE9
0xB53D46  push    ecx                         ; 实参 18 = level_point
0xB53D4E  push    ecx                         ; 实参 17 = flag_wideuse
0xB53D53  push    eax                         ; 实参 16 = heroms_term 串指针
0xB53D5A  push    eax                         ; 实参 15 = ncafe_compcnt
0xB53D61  push    eax                         ; 实参 14 = daily_compcnt
0xB53D68  push    eax                         ; 实参 13 = accum_playtime
0xB53D70  push    eax                         ; 实参 12 = overplay_type
0xB53D7A  push    eax                         ; 实参 11 = vip_lv
0xB53D85  push    eax                         ; 实参 10 = is_processing_comeback
0xB53D90  push    eax                         ; 实参 9  = is_netcafe
0xB53D9A  push    ecx                         ; 实参 8  = pilot_detail 结构体指针
0xB53DA6  push    ecx                         ; 实参 7  = tuto_missionid
0xB53DA9  push    eax                         ; 实参 6  = tuto_flags 高 4 字节
0xB53DB1  push    ecx                         ; 实参 5  = tuto_flags 低 4 字节
0xB53DBB  push    ecx                         ; 实参 4  = tuto_step
0xB53DC5  push    ecx                         ; 实参 3  = charge_point
0xB53DCC  push    ecx                         ; 实参 2  = restore_channel
0xB53DCF  push    ecx                         ; 实参 1  = result
0xB53DA0  mov     edx, [edx+94h]              ; ← vt[0x94]
0xB53DD0  mov     ecx, esi
0xB53DD2  call    edx
0xB53DD4  add     dword ptr [esi+978h], 1     ; 本命令接收计数（64 位）
0xB53DE2  adc     dword ptr [esi+97Ch], 0
```
