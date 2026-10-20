# 汇编证据 —— SC-0x1365-battle-game_begin

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。
> 复合读取器**已按整函数边界扫描**（失败出口 `retn` 之后仍有成功路径者已补全）。

## E1 case 入口 + 解码缓冲申请（容量 `0x2806`）

```asm
; VA: 0xB0FBDA .. 0xB0FC09
0xB0FBDA  push    32h                      ; ← 本 case 错误码
0xB0FBDC  mov     ecx, esi
0xB0FBDE  call    sub_B05DA0               ; case 起始守卫（不读线）
0xB0FBE3  test    al, al
0xB0FBE5  jz      loc_B317C7
0xB0FBEB  mov     ecx, [esi+0Ch]
0xB0FBEE  mov     eax, [ecx]
0xB0FBF0  mov     edx, [eax+78h]
0xB0FBF3  push    2806h                    ; ← 容量 10246
0xB0FBF8  call    edx
0xB0FBFA  mov     [esp+1B3Ch+var_1B1C], eax ; 解码缓冲基址
0xB0FC02  lea     ecx, [esp+1B40h+var_1AB8]
0xB0FC09  call    sub_ABB2F0               ; 初始化线游标
```

## E2 字段 1~6（6×u32）：各「槽预留 + bounded 读」成对

```asm
; VA: 0xB0FC25 .. 0xB0FD17
0xB0FC25  call    sub_B41470               ; 槽预留（非字段）
0xB0FC37  call    sub_B02DD0               ; ← 读 u32 → snapshot_int_msec
0xB0FC68  call    sub_B41470
0xB0FC7A  call    sub_B02DD0               ; ← 读 u32 → snapshot_res_msec
0xB0FC8F  call    sub_B41470
0xB0FC9E  call    sub_B02DD0               ; ← 读 u32 → pos_factor
0xB0FCB3  call    sub_B41470
0xB0FCC2  call    sub_B02DD0               ; ← 读 u32 → map_id
0xB0FCDB  call    sub_B41470
0xB0FCEA  call    sub_B02DD0               ; ← 读 u32 → btlfield
0xB0FD03  call    sub_B41470
0xB0FD12  call    sub_B02DD0               ; ← 读 u32 → clear_remain_msec
```

## E3 字段 7~8（2×u8）：`is_disable_conq_sp`、`is_room_suspend`

```asm
; VA: 0xB0FD2B .. 0xB0FD62
0xB0FD2B  call    sub_B05E30               ; u8 槽预留（非字段）
0xB0FD3A  call    sub_B06230               ; ← 读 u8 → is_disable_conq_sp
0xB0FD53  call    sub_B05E30
0xB0FD62  call    sub_B06230               ; ← 读 u8 → is_room_suspend
```

## E4 字段 9~13（5×u32）：`mission_id`…`exp_max`

```asm
; VA: 0xB0FD7B .. 0xB0FE2F
0xB0FD8A  call    sub_B02DD0               ; → mission_id
0xB0FDB2  call    sub_B02DD0               ; → sudden_type
0xB0FDDA  call    sub_B02DD0               ; → sudden_bonus_target
0xB0FE02  call    sub_B02DD0               ; → exp_min
0xB0FE2A  call    sub_B02DD0               ; → exp_max
```

## E5 字段 14：`config`（结构体；预留 `sub_B418C0` 槽 0x28，读取器 `sub_B077B0`）

```asm
; VA: 0xB0FE3A .. 0xB0FE57
0xB0FE3F  lea     ecx, [esp+1B3Ch+var_1B0C]
0xB0FE43  call    sub_B418C0               ; 预留 0x28（40）字节槽（非字段）
0xB0FE48  mov     eax, [esp+1B3Ch+var_1B0C]
0xB0FE52  call    sub_B077B0               ; ← 复合读取器（整函数消费 34 字节）
0xB0FE5C  jz      loc_B0FC43
```

```asm
; sub_B418C0（0xB418C0..0xB418CF）：单槽预留，步进 0x28 = 40
0xB418C6  mov     edx, [ecx]
0xB418C8  mov     [eax], edx
0xB418CA  add     dword ptr [ecx], 28h     ; ← 结构体 claim = 40（≠ 线长 34）
```

```asm
; sub_B077B0 整函数（0xB077B0 .. 0xB0787F）：线长 = 2+4+4+2+4+4+4+2+4+4 = 34
0xB077C3  mov     dx, [eax]                ; ← u16 @+0    → A_troops
0xB077DF  mov     edx, [eax]               ; ← u32 @+4    → A_point_max
0xB077F1  mov     edx, [eax]               ; ← u32 @+8    → A_win_cnt
0xB07803  mov     dx, [eax]                ; ← u16 @+0xC  → B_troops
0xB07812  call    sub_B02DD0               ; ← u32 @+0x10 → B_point_max
0xB07823  call    sub_B02DD0               ; ← u32 @+0x14 → B_win_cnt
0xB07834  call    sub_B02DD0               ; ← u32 @+0x18 → dotdmg_min
0xB07845  call    sub_B02DF0               ; ← u16 @+0x1C → atk_team
0xB07856  call    sub_B02DD0               ; ← u32 @+0x20 → round_now
0xB07870  add     edi, 24h                 ; ↓ 成功路径（0xB0786B 起，位于失败出口 0xB07862 之后）
0xB07870  call    sub_B02DD0               ; ← u32 @+0x24 → round_max
```

## E6 字段 15：`progress`（预留 `sub_B05ED0` 槽 0x40，读取器 `sub_B07880`）

```asm
; VA: 0xB0FE5E .. 0xB0FE7F
0xB0FE67  lea     ecx, [esp+1B3Ch+var_1B18]
0xB0FE6B  call    sub_B05ED0               ; 预留 0x40（64）字节槽（非字段）
0xB0FE7A  call    sub_B07880               ; ← 复合读取器（整函数消费 46 字节）
```

```asm
; sub_B05ED0（0xB05ED0..0xB05EDF）：单槽预留，步进 0x40 = 64
0xB05EDA  add     dword ptr [ecx], 40h     ; ← 结构体 claim = 64（≠ 线长 46）
```

```asm
; sub_B07880 整函数（0xB07880 .. 0xB0799B）：线长 = 4×4 + 2+2 + 1+1 + 4×6 = 46
0xB0789A  mov     [edi], edx               ; u32 @+0    → remain_msec
0xB078AF  mov     [edi+4], edx             ; u32 @+4    → coop_step
0xB078C5  mov     [edi+8], edx             ; u32 @+8    → A_point_now
0xB078DB  mov     [edi+0Ch], edx           ; u32 @+0xC  → B_point_now
0xB078E6  call    sub_B02DF0               ; u16 @+0x10 → A_gauge_dmg_scale
0xB078FB  call    sub_B02DF0               ; u16 @+0x12 → B_gauge_dmg_scale
0xB0790C  call    sub_B06230               ; u8  @+0x14 → coop_dead_remain（i8 语义，打印器 movsx）
0xB0791D  call    sub_B06230               ; u8  @+0x15 → is_prestart（同上）
0xB0792E  call    sub_B02DD0               ; u32 @+0x18 → rule_status
0xB0793F  call    sub_B02DD0               ; u32 @+0x1C → rule_timer_msec
0xB07950  call    sub_B02DD0               ; u32 @+0x20 → rule_param1
0xB07961  call    sub_B02DD0               ; u32 @+0x24 → rule_param2
0xB07972  call    sub_B02DD0               ; u32 @+0x28 → A_dot_dmg
0xB07988  add     edi, 2Ch                 ; ↓ 成功路径（0xB07987 起）
0xB0798C  call    sub_B02DD0               ; u32 @+0x2C → B_dot_dmg
```

## E7 字段 16/17：`respawn_posts_num`（u32，上限 50）+ 数组（预留 `sub_B05F20` 步进 0x50）

```asm
; VA: 0xB0FE94 .. 0xB0FF09
0xB0FE94  call    sub_B02DD0               ; ← 读 u32 → respawn_posts_num
0xB0FEB9  mov     ebx, [esp+1B3Ch+var_1B08]
0xB0FEBD  cmp     ebx, 32h                 ; ← 上限 50
0xB0FEC0  ja      short loc_B0FEA0
0xB0FEC2  push    ebx
0xB0FECF  call    sub_B05F20               ; 预留 N×0x50（推进缓冲游标，非字段）
0xB0FEEF  call    sub_B079A0               ; ← 元素读取器（消费 58 字节）
0xB0FEFB  add     [esp+1B3Ch+var_1B2C], 50h ; ← 缓冲步进 80（≠ 元素线长 58）
0xB0FF03  cmp     edi, ebx
0xB0FF05  jb      short loc_B0FEE5
```

```asm
; sub_B05F20（0xB05F20..0xB05F4B）：数组预留，每槽步进 0x50 = 80
0xB05F40  add     dword ptr [edx], 50h
```

```asm
; sub_B079A0 整函数（0xB079A0 .. 0xB07AF9）：元素线长 = 4+2+2+13+4+4+2+2+2+2+1+4+4+4+4+4 = 58
0xB079BA  mov     [edi], edx               ; u32  @+0    → type
0xB079D0  mov     [edi+4], dx              ; u16  @+4    → ini_team
0xB079E8  mov     [edi+6], dx              ; u16  @+6    → ini_troops
0xB079F1  mov     cl, [ecx]                ; 13 次 u8 循环 → name[13] @+8
0xB07A0D  cmp     eax, 0Dh
0xB07A20  mov     [edi+18h], eax           ; u32  @+0x18 → gauge_max
0xB07A36  mov     [edi+1Ch], edx           ; u32  @+0x1C → post_chara_id
0xB07A51  mov     [edi+20h], dx            ; u16  @+0x20 → pos_x
0xB07A65  call    sub_B02DF0               ; u16  @+0x22 → pos_y
0xB07A76  call    sub_B02DF0               ; u16  @+0x24 → pos_z
0xB07A87  call    sub_B02DF0               ; u16  @+0x26 → dir
0xB07A98  call    sub_B06230               ; u8   @+0x28 → cmdr_sptype（i8 语义）
0xB07AA9  call    sub_B02DD0               ; u32  @+0x2C → group_id
0xB07ABA  call    sub_B02DD0               ; u32  @+0x30 → npc_ba_point_ent_id
0xB07ACB  call    sub_B02DD0               ; u32  @+0x34 → npc_ba_point_move_range_abs_x
0xB07AE5  add     edi, 3Ch                 ; ↓ 成功路径（0xB07AE5 起）
0xB07AEA  call    sub_B02DD0               ; u32  @+0x38 → param1
0xB07AEA  call    sub_B02DD0               ; u32  @+0x3C → param2
```

## E8 字段 18/19：`mapgimmicks_num`（u32，上限 32）+ 数组（预留 `sub_B05F50` 步进 0xBC）

```asm
; VA: 0xB0FF16 .. 0xB0FF8B
0xB0FF20  call    sub_B02DD0               ; ← 读 u32 → mapgimmicks_num
0xB0FF30  cmp     [esp+1B3Ch+var_1AFC], 20h ; ← 上限 32
0xB0FF35  ja      loc_B0FEA0
0xB0FF4C  call    sub_B05F50               ; 预留 N×0xBC（非字段）
0xB0FF6E  call    sub_B07BD0               ; ← 元素读取器（消费 52 字节）
0xB0FF7A  add     [esp+1B3Ch+var_1B2C], 0BCh ; ← 缓冲步进 188（≠ 元素线长 52）
0xB0FF89  jb      short loc_B0FF64
```

```asm
; sub_B05F50（0xB05F50..0xB05F7E）：数组预留，每槽步进 0xBC = 188
0xB05F70  add     dword ptr [edx], 0BCh
```

```asm
; sub_B07BD0 整函数（0xB07BD0 .. 0xB07DA2）：元素线长 = 1+1+2+4+4+4+7×2+2×2+8×2+2 = 52
0xB07BEA  mov     [edi], dl                ; u8   @+0    → type（i8 语义）
0xB07BFF  mov     [edi+1], dl              ; u8   @+1    → stat（i8 语义）
0xB07C16  mov     [edi+2], dx              ; u16  @+2    → ent_id
0xB07C31  mov     [edi+4], edx             ; u32  @+4    → gauge_max
0xB07C38  call    sub_B02DD0               ; u32  @+8    → msma_id
0xB07C4D  call    sub_B02DD0               ; u32  @+0xC  → msma_id2
0xB07C5E  call    sub_B02DF0               ; u16  @+0x10 → pos_x
0xB07C6F  call    sub_B02DF0               ; u16  @+0x12 → pos_y
0xB07C80  call    sub_B02DF0               ; u16  @+0x14 → pos_z
0xB07C91  call    sub_B02DF0               ; u16  @+0x16 → dir
0xB07CA2  call    sub_B02DF0               ; u16  @+0x18 → pos2_x
0xB07CB3  call    sub_B02DF0               ; u16  @+0x1A → pos2_y
0xB07CC4  call    sub_B02DF0               ; u16  @+0x1C → pos2_z
0xB07CE0  call    sub_B02DF0               ; u16  @+0x1E → ctrl_ent_id[0]（2 次循环）
0xB07CF8  cmp     ebx, 2
0xB07D02  call    sub_B02DF0               ; u16  @+0x22 → ctrl_count
0xB07D13  call    sub_B02DF0               ; u16  @+0x24 → route_number
0xB07D24  call    sub_B02DF0               ; u16  @+0x26 → route_initial_index
0xB07D35  call    sub_B02DF0               ; u16  @+0x28 → move_speed
0xB07D46  call    sub_B02DF0               ; u16  @+0x2A → rot_speed
0xB07D57  call    sub_B02DF0               ; u16  @+0x2C → door_auto_sensor_height
0xB07D68  call    sub_B02DF0               ; u16  @+0x2E → door_auto_sensor_radius
0xB07D79  call    sub_B02DF0               ; u16  @+0x30 → attach_barrier_npc_ent_id
0xB07D8C  add     edi, 32h                 ; ↓ 成功路径（0xB07D8C 起）
0xB07D91  call    sub_B02DF0               ; u16  @+0x32 → local_ctrl_id
```

## E9 字段 20：`bgm_desc`（预留 `sub_B41740` 槽 0x14，读取器 `sub_B07E00`）

```asm
; VA: 0xB0FF9A .. 0xB0FFBC
0xB0FF9A  lea     ecx, [esp+1B3Ch+var_1B1C]
0xB0FFA3  call    sub_B41740               ; 预留 0x14（20）字节槽（非字段）
0xB0FFB2  call    sub_B07E00               ; ← 复合读取器（整函数消费 14 字节）
```

```asm
; sub_B41740（0xB41740..0xB4174F）：单槽预留，步进 0x14 = 20
0xB4174A  add     dword ptr [ecx], 14h

; sub_B07E00 整函数（0xB07E00 .. 0xB07E6A）：线长 = 1+4+4+4+1 = 14
0xB07E0E  mov     dl, [ecx]                ; u8  @+0    → is_final_phase（i8 语义）
0xB07E26  mov     [ecx+4], edx             ; u32 @+4    → field_bgm_id
0xB07E38  mov     [ecx+8], edx             ; u32 @+8    → ace_bgm_id
0xB07E4A  mov     [ecx+0Ch], edx           ; u32 @+0xC  → force_bgm_id
0xB07E55  call    sub_B06230               ; u8  @+0x10 → is_one_shot（i8 语义）
```

## E10 字段 21/22/23：`missionunit_num`（上限 11）+ u32 数组 + `mission_phase` + 闭合

```asm
; VA: 0xB0FFCC .. 0xB10075
0xB0FFCC  call    sub_B02DD0               ; ← 读 u32 → missionunit_num
0xB0FFDC  cmp     [esp+1B3Ch+var_1AF4], 0Bh ; ← 上限 11
0xB0FFE1  ja      loc_B0FEA0
0xB0FFF8  call    sub_B41850               ; 预留 N×4（非字段）
0xB1001A  call    sub_B02DD0               ; ← 元素读取器（u32，消费 4）
0xB10026  add     [esp+1B3Ch+var_1B2C], 4  ; ← 缓冲步进 4（= 元素线长 4）
0xB10032  jb      short loc_B10010
0xB1004C  call    sub_B41470               ; u32 槽预留（非字段）
0xB1005B  call    sub_B02DD0               ; ← 读 u32 → mission_phase（最后一个字段）
0xB1006F  mov     ecx, [esp+1B3Ch+var_1B28] ; 读完后的线游标
0xB1006F  cmp     ecx, [esp+1B3Ch+var_1B24] ; vs 报文末尾
0xB10075  jz      short loc_B1008E         ; ← 不等 ⇒ push 1 / push 32h 报错
```

## E11 含义取证：块内 23 个日志串（字段名一一对位）

```asm
; VA: 0xB1010B .. 0xB1051C
0xB1010B  push    offset aSnapshotIntMse   ; ← "snapshot_int_msec="
0xB10138  push    offset aSnapshotResMse   ; ← "snapshot_res_msec="
0xB10162  push    offset aPosFactor         ; ← "pos_factor="
0xB1018C  push    offset aMapId             ; ← "map_id="
0xB101B6  push    offset aBtlfield          ; ← "btlfield="
0xB101E0  push    offset aClearRemainMse    ; ← "clear_remain_msec="
0xB10208  push    offset aIsDisableConqS    ; ← "is_disable_conq_sp="
0xB10232  push    offset aIsRoomSuspend     ; ← "is_room_suspend="
0xB1025E  push    offset aMissionId         ; ← "mission_id="
0xB10288  push    offset aSuddenType        ; ← "sudden_type="
0xB102B2  push    offset aSuddenBonusTar    ; ← "sudden_bonus_target="
0xB102DC  push    offset aExpMin            ; ← "exp_min="
0xB10306  push    offset aExpMax            ; ← "exp_max="
0xB1032E  push    offset aConfig            ; ← "config="   （打印器 sub_B0A670）
0xB10358  push    offset aProgress          ; ← "progress=" （打印器 sub_B0A820）
0xB10375  push    offset aRespawnPosts      ; ← "respawn_posts={"（元素打印器 sub_B0AA70）
0xB103EB  push    offset aMapgimmicks       ; ← "mapgimmicks={" （元素打印器 sub_B0AEA0）
0xB1047B  push    offset aBgmDesc           ; ← "bgm_desc="  （打印器 sub_B0B320）
0xB10498  push    offset aMissionunitSet    ; ← "missionunit_set={"
0xB1051C  push    offset aMissionPhase      ; ← "mission_phase="
```

## E12 去向：`vt[0xEC](...23 个实参...)`

```asm
; VA: 0xB10568 .. 0xB10630（推送序 = cdecl 逆序，故按顺序倒读即声明序）
0xB10572  push    ecx                      ; #1（最后实参）  = mission_phase
0xB10577  push    eax                      ; #2 = missionunit_num (N3)
0xB1057F  push    ecx                      ; #3 = missionunit_set 基址
0xB10584  push    eax                      ; #4 = bgm_desc 指针
0xB10589  push    ecx                      ; #5 = mapgimmicks_num (N2)
0xB10591  push    eax                      ; #6 = mapgimmicks 基址
0xB1059D  push    ebx                      ; #7 = respawn_posts_num (N1)
0xB1059E  push    ecx                      ; #8 = respawn_posts 基址
0xB105A3  push    eax                      ; #9 = progress 指针
0xB105A8  push    ecx                      ; #10 = config 指针
0xB105AF  push    ecx                      ; #11 = exp_max
0xB105B6  push    ecx                      ; #12 = exp_min
0xB105BD  push    ecx                      ; #13 = sudden_bonus_target
0xB105C7  push    ecx                      ; #14 = sudden_type
0xB105D1  push    ecx                      ; #15 = mission_id
0xB105DC  push    ecx                      ; #16 = is_room_suspend（movzx）
0xB105E9  push    ecx                      ; #17 = is_disable_conq_sp（movzx）
0xB105F9  push    ecx                      ; #18 = clear_remain_msec
0xB10603  push    ecx                      ; #19 = btlfield
0xB1060D  push    ecx                      ; #20 = map_id
0xB10617  push    ecx                      ; #21 = pos_factor
0xB10621  push    ecx                      ; #22 = snapshot_res_msec
0xB10624  push    ecx                      ; #23（第 1 实参） = snapshot_int_msec
0xB105F3  mov     edx, [edx+0ECh]           ; ← vt[0xEC]
0xB10627  call    edx
0xB10629  add     dword ptr [esi+0C40h], 1  ; 本命令接收计数（64 位）
```
