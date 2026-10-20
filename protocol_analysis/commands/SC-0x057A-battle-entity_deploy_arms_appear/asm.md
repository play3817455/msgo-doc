# 汇编证据 —— SC-0x057A-battle-entity_deploy_arms_appear

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 case 入口 + 解码缓冲申请（容量 `0x60` = 96）

```asm
; VA: 0xB0D8AC .. 0xB0D8D4
0xB0D8AC  call    sub_B05DA0               ; battle case 入口/开关（错误码 0x55）
0xB0D8B1  test    al, al
0xB0D8B3  jz      loc_B317C7
0xB0D8B9  mov     ecx, [esi+0Ch]
0xB0D8BC  mov     eax, [ecx]
0xB0D8BE  mov     edx, [eax+78h]           ; vt[0x78] = 申请解码缓冲
0xB0D8C1  push    60h                      ; ← 容量 96（= 结构体 claim，≠ 线长 86）
0xB0D8C3  call    edx
0xB0D8C5  mov     [esp+1B3Ch+var_1B14], eax ; 缓冲基址
0xB0D8C9  mov     eax, [esi+0Ch]
0xB0D8CC  push    eax
0xB0D8CD  lea     ecx, [esp+1B40h+var_17DC]
0xB0D8D4  call    sub_ABB2F0               ; 初始化 {cur,end} 读游标
```

## E2 结构体：缓冲预留 `sub_B06020` + 复合读取器 `sub_B07EC0`

```asm
; VA: 0xB0D8D9 .. 0xB0D908
0xB0D8DD  push    ecx                         ; arg_0 = &缓冲游标
0xB0D8DE  lea     ecx, [esp+1B40h+var_1B2C]   ; this = &结构体槽
0xB0D8ED  call    sub_B06020                  ; ← 缓冲预留：claim 0x60 = 96B
0xB0D8F2  mov     eax, [esp+1B3Ch+var_1B2C]
0xB0D8F6  lea     edx, [esp+1B3Ch+var_1B28]   ; 线游标
0xB0D8FC  call    sub_B07EC0                  ; ← 复合读取器（appear_info）
0xB0D908  jnz     short loc_B0D921
```

预留器本体（claim 量取证；**claim 推进的是「解码缓冲」游标，与线游标无关**）：

```asm
; VA: 0xB06020 .. 0xB0602D
0xB06020  mov     eax, ecx
0xB06022  mov     ecx, [esp+arg_0]
0xB06026  mov     edx, [ecx]
0xB06028  mov     [eax], edx
0xB0602A  add     dword ptr [ecx], 60h    ; ← 结构体 claim = 96 字节（= 容量）
0xB0602D  retn    4
```

## E3 复合读取器 `sub_B07EC0`（函数体 `0xB07EC0..0xB0801B`，**17 次读取，线长 86**）

```asm
; VA: 0xB07EC0 .. 0xB07FFB（主干）
0xB07EC7  lea     ecx, [eax+1]             ; ① 1B
0xB07ED3  mov     dl, [eax]
0xB07EDA  mov     [edi], dl                ; ← team（mem +0）
0xB07EE1  lea     ecx, [eax+1]             ; ② 1B
0xB07EED  mov     dl, [eax]
0xB07EEF  mov     [edi+1], dl              ; ← troops（mem +1）
0xB07EF7  lea     ecx, [eax+4]             ; ③ 4B
0xB07F03  mov     edx, [eax]
0xB07F05  mov     [edi+4], edx             ; ← world_id（mem +4）
0xB07F0D  lea     ecx, [eax+4]             ; ④ 4B
0xB07F19  mov     edx, [eax]
0xB07F1F  mov     [edi+8], edx             ; ← pilot_id（mem +8）
0xB07F26  call    sub_B02DD0               ; ⑤ u32 → mem +0Ch  = ent_id
0xB07F3B  call    sub_B02DD0               ; ⑥ u32 → mem +10h  = index
0xB07F50  call    sub_B02DD0               ; ⑦ u32 → mem +14h  = msma_id
0xB07F65  call    sub_B02DD0               ; ⑧ u32 → mem +18h  = item_id
0xB07F7A  call    sub_B06230               ; ⑨ u8  → mem +1Ch  = type
0xB07F8B  call    sub_B02DD0               ; ⑩ u32 → mem +20h  = eff_range
0xB07F9C  call    sub_B075A0               ; ⑪ 子结构 snapshot（39B → mem +24h）
0xB07FAD  call    sub_B02DD0               ; ⑫ u32 → mem +50h  = arms_id
0xB07FBE  call    sub_B02DF0               ; ⑬ u16 → mem +54h  = state_bit
0xB07FCF  call    sub_B06230               ; ⑭ u8  → mem +56h  = is_gmk
0xB07FE0  call    sub_B06230               ; ⑮ u8  → mem +57h  = is_using_ss
0xB07FF1  call    sub_B02DD0               ; ⑯ u32 → mem +58h  = remain_msec
0xB07FFB  jnz     short loc_B08006          ; 全部成功 ⇒ 跳成功路径
```

```asm
; VA: 0xB07FFD .. 0xB0801A（失败出口 + **成功路径尾读**）
0xB07FFD  pop     edi
0xB07FFE  xor     al, al
0xB08001  retn
0xB08002  xor     al, al
0xB08005  retn
0xB08006  push    esi                       ; ← 成功路径
0xB08007  add     edi, 5Ch
0xB0800A  push    edi
0xB0800B  call    sub_B02DD0               ; ⑰ ← u32 → mem +5Ch = buildup_eff_range（4B）
0xB08010  add     esp, 8
0xB08016  setnz   al
0xB0801A  retn
```

> ⚠️ 若只在 `0xB08001`（失败分支）处停止扫描，会漏掉 ⑰ 而把线长误算成 80。

## E4 子结构读取器 `sub_B075A0`（函数体 `0xB075A0..0xB07757`，**21 次读取，线长 39**）

```asm
; VA: 0xB075A0 .. 0xB07737（主干）
0xB075A7  lea     ecx, [eax+2]             ; ① u16 → mem +0   = ent_id
0xB075C3  lea     ecx, [eax+2]             ; ② u16 → mem +2   = pos_x
0xB075DB  lea     ecx, [eax+2]             ; ③ u16 → mem +4   = pos_y
0xB075F3  lea     ecx, [eax+2]             ; ④ u16 → mem +6   = pos_z
0xB0760E  call    sub_B02DF0               ; ⑤ u16 → mem +8   = dir
0xB07623  call    sub_B02DF0               ; ⑥ u16 → mem +0Ah = target_x
0xB07638  call    sub_B02DF0               ; ⑦ u16 → mem +0Ch = target_y
0xB0764D  call    sub_B02DF0               ; ⑧ u16 → mem +0Eh = target_z
0xB07662  call    sub_B02DF0               ; ⑨ u16 → mem +10h = score1
0xB07677  call    sub_B02DF0               ; ⑩ u16 → mem +12h = score2
0xB0768C  call    sub_B02DF0               ; ⑪ u16 → mem +14h = score3
0xB076A1  call    sub_B06230               ; ⑫ u8  → mem +16h = hp_percent
0xB076B6  call    sub_B06230               ; ⑬ u8  → mem +17h = hp_percent_shield
0xB076C7  call    sub_B02DF0               ; ⑭ u16 → mem +18h = down_power
0xB076D8  call    sub_B06230               ; ⑮ u8  → mem +1Ah = equip_index
0xB076E9  call    sub_B06230               ; ⑯ u8  → mem +1Bh = water_index
0xB076FA  call    sub_B06230               ; ⑰ u8  → mem +1Ch = layer_index
0xB0770B  call    sub_B02DF0               ; ⑱ u16 → mem +1Eh = rideon_ent_id
0xB0771C  call    sub_B02DF0               ; ⑲ u16 → mem +20h = lockon_ent_id
0xB0772D  call    sub_B02DD0               ; ⑳ u32 → mem +24h = special_bits
0xB07737  jnz     short loc_B07742
```

```asm
; VA: 0xB07739 .. 0xB07756（失败出口 + **成功路径尾读**）
0xB07739  pop     edi
0xB0773A  xor     al, al
0xB0773D  retn
0xB07742  push    esi                       ; ← 成功路径
0xB07743  add     edi, 28h
0xB07746  push    edi
0xB07747  call    sub_B02DF0               ; ㉑ ← u16 → mem +28h = special_bits2（2B）
0xB07752  setnz   al
0xB07756  retn
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB0D921 .. 0xB0D929
0xB0D921  mov     ebx, [esp+1B3Ch+var_1B28]   ; 读完后的游标
0xB0D925  cmp     ebx, [esp+1B3Ch+var_1B24]   ; vs 报文末尾
0xB0D929  jnz     short loc_B0D90A            ; ← 不等 ⇒ push 55h 报错
```

## E6 含义取证：结构体打印器 `sub_B0B4B0`（17 个顶层成员名）

```asm
; VA: 0xB0B4B0 .. 0xB0B76A（节选）
0xB0B4C5  movsx   eax, byte ptr [edi]       ; mem +0
0xB0B4D1  push    offset aTeam              ; ← "team="
0xB0B4EC  movsx   ecx, byte ptr [edi+1]     ; mem +1
0xB0B4F9  push    offset aTroops            ; ← "troops="
0xB0B520  push    offset aWorldId           ; ← "world_id="（mem +4）
0xB0B547  push    offset aPilotId           ; ← "pilot_id="（mem +8）
0xB0B56E  push    offset aEntId             ; ← "ent_id="（mem +0Ch）
0xB0B595  push    offset aIndex             ; ← "index="（mem +10h）
0xB0B5BC  push    offset aMsmaId            ; ← "msma_id="（mem +14h）
0xB0B5E3  push    offset aItemId            ; ← "item_id="（mem +18h）
0xB0B5FE  movsx   edx, byte ptr [edi+1Ch]   ; mem +1Ch
0xB0B60B  push    offset aType_0            ; ← "type="
0xB0B632  push    offset aEffRange          ; ← "eff_range="（mem +20h）
0xB0B655  lea     ecx, [edi+24h]
0xB0B659  push    offset aSnapshot          ; ← "snapshot="（mem +24h → sub_B0A260）
0xB0B682  push    offset aArmsId            ; ← "arms_id="（mem +50h）
0xB0B6A4  push    offset aStateBit          ; ← "state_bit="（mem +54h，u16）
0xB0B6C5  movsx   ecx, byte ptr [edi+56h]   ; mem +56h
0xB0B6D2  push    offset aIsGmk             ; ← "is_gmk="
0xB0B6ED  movsx   edx, byte ptr [edi+57h]   ; mem +57h
0xB0B6FA  push    offset aIsUsingSs         ; ← "is_using_ss="
0xB0B721  push    offset aRemainMsec        ; ← "remain_msec="（mem +58h）
0xB0B743  push    offset aBuildupEffRang    ; ← "buildup_eff_range="（mem +5Ch，= 成功路径尾读的对端）
```

## E7 含义取证：子结构打印器 `sub_B0A260`（snapshot 成员名）

```asm
; VA: 0xB0A260 .. 0xB0A5C2（节选；末尾两名即成功路径尾读的对端）
0xB0A281  push    offset aEntId             ; ← "ent_id="（mem +0，u16）
0xB0A2A9  push    offset aPosX              ; ← "pos_x="（+2）
0xB0A2D1  push    offset aPosY              ; ← "pos_y="（+4）
0xB0A2F9  push    offset aPosZ              ; ← "pos_z="（+6）
0xB0A321  push    offset aDir               ; ← "dir="（+8）
0xB0A349  push    offset aTargetX           ; ← "target_x="（+0Ah）
0xB0A371  push    offset aTargetY           ; ← "target_y="（+0Ch）
0xB0A399  push    offset aTargetZ           ; ← "target_z="（+0Eh）
0xB0A3C1  push    offset aScore1            ; ← "score1="（+10h）
0xB0A3E9  push    offset aScore2            ; ← "score2="（+12h）
0xB0A411  push    offset aScore3            ; ← "score3="（+14h）
0xB0A42C  movsx   edx, byte ptr [edi+16h]
0xB0A439  push    offset aHpPercent         ; ← "hp_percent="
0xB0A454  movsx   eax, byte ptr [edi+17h]
0xB0A461  push    offset aHpPercentShiel    ; ← "hp_percent_shield="
0xB0A489  push    offset aDownPower         ; ← "down_power="（+18h）
0xB0A4A4  movsx   edx, byte ptr [edi+1Ah]
0xB0A4B1  push    offset aEquipIndex        ; ← "equip_index="
0xB0A4CC  movzx   eax, byte ptr [edi+1Bh]
0xB0A4D9  push    offset aWaterIndex        ; ← "water_index="
0xB0A4F4  movzx   ecx, byte ptr [edi+1Ch]
0xB0A501  push    offset aLayerIndex        ; ← "layer_index="
0xB0A529  push    offset aRideonEntId       ; ← "rideon_ent_id="（+1Eh）
0xB0A551  push    offset aLockonEntId       ; ← "lockon_ent_id="（+20h）
0xB0A578  push    offset aSpecialBits       ; ← "special_bits="（+24h，u32）
0xB0A593  movzx   edx, word ptr [edi+28h]
0xB0A59B  push    offset aSpecialBits2      ; ← "special_bits2="（+28h，u16）
```

## E8 去向：`vt[0x158]`（单实参 = 结构体基址）

```asm
; VA: 0xB0D9E8 .. 0xB0DA07
0xB0D9EA  mov     eax, [esp+1B3Ch+var_1B2C]   ; 结构体基址
0xB0D9EE  mov     edx, [edx+158h]             ; ← vt[0x158]
0xB0D9F4  push    eax
0xB0D9F7  call    edx
0xB0D9F9  add     dword ptr [esi+12D0h], 1    ; 本命令接收计数（64 位）
0xB0DA07  adc     dword ptr [esi+12D4h], 0
```
