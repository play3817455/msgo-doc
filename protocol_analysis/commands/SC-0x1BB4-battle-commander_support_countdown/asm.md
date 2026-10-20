# 汇编证据 —— SC-0x1BB4-battle-commander_support_countdown

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x11` @ `0xB116B4`）

```asm
; VA: 0xB11698 .. （块入口，含守卫与容量申请）
00B11698  push    0E6h
00B1169D  mov     ecx, esi
00B1169F  call    sub_B05DA0
00B116A4  test    al, al
00B116A6  jz      loc_B317C7
00B116AC  mov     ecx, [esi+0Ch]
00B116AF  mov     eax, [ecx]
00B116B1  mov     edx, [eax+78h]
00B116B4  push    11h
00B116B6  call    edx
00B116B8  mov     [esp+1B3Ch+var_1B1C], eax
00B116BC  mov     eax, [esi+0Ch]
00B116BF  push    eax
00B116C0  lea     ecx, [esp+1B40h+var_1A5C]
```

## E2 字段 1：`ent_id`（u16，偏移 0，长度 2）

```asm
; VA: 0x0xB116EF 附近（指挥官支援实体 ID）
00B116E5  mov     eax, [esp+1B3Ch+var_1AE0]
00B116E9  lea     edx, [esp+1B3Ch+var_1B28]
00B116ED  push    edx
00B116EE  push    eax
00B116EF  call    sub_B02DF0
00B116F4  add     esp, 8
00B116F7  test    al, al
00B116F9  jnz     short loc_B11717
00B116FB  mov     edx, [esi]
00B116FD  mov     eax, [edx+64h]
```

## E3 字段 2：`support_type`（u32，偏移 2，长度 4）

```asm
; VA: 0x0xB1172F 附近（支援类型）
00B11725  mov     eax, [esp+1B3Ch+var_1AF0]
00B11729  lea     edx, [esp+1B3Ch+var_1B28]
00B1172D  push    edx
00B1172E  push    eax
00B1172F  call    sub_B02DD0
00B11734  add     esp, 8
00B11737  test    al, al
00B11739  jz      short loc_B116FB
00B1173B  lea     ecx, [esp+1B3Ch+var_1B1C]
00B1173F  push    ecx
```

## E4 字段 3：`team`（u8，偏移 6，长度 1）

```asm
; VA: 0x0xB11753 附近（阵营）
00B11749  mov     eax, [esp+1B3Ch+var_1AF8]
00B1174D  lea     edx, [esp+1B3Ch+var_1B28]
00B11751  push    edx
00B11752  push    eax
00B11753  call    sub_B06230
00B11758  add     esp, 8
00B1175B  test    al, al
00B1175D  jz      short loc_B116FB
00B1175F  lea     ecx, [esp+1B3Ch+var_1B1C]
00B11763  push    ecx
```

## E5 字段 4：`troops`（u8，偏移 7，长度 1）

```asm
; VA: 0x0xB11777 附近（势力）
00B1176D  mov     eax, [esp+1B3Ch+var_1AEC]
00B11771  lea     edx, [esp+1B3Ch+var_1B28]
00B11775  push    edx
00B11776  push    eax
00B11777  call    sub_B06230
00B1177C  add     esp, 8
00B1177F  test    al, al
00B11781  jz      loc_B116FB
00B11787  lea     ecx, [esp+1B3Ch+var_1B1C]
00B1178B  push    ecx
```

## E6 字段 5：`target_x`（u16，偏移 8，长度 2）

```asm
; VA: 0x0xB1179F 附近（支援目标 X）
00B11795  mov     eax, [esp+1B3Ch+var_1B00]
00B11799  lea     edx, [esp+1B3Ch+var_1B28]
00B1179D  push    edx
00B1179E  push    eax
00B1179F  call    sub_B02DF0
00B117A4  add     esp, 8
00B117A7  test    al, al
00B117A9  jz      loc_B116FB
00B117AF  lea     ecx, [esp+1B3Ch+var_1B1C]
00B117B3  push    ecx
```

## E7 字段 6：`target_y`（u16，偏移 10，长度 2）

```asm
; VA: 0x0xB117C7 附近（支援目标 Y）
00B117BD  mov     eax, [esp+1B3Ch+var_1B0C]
00B117C1  lea     edx, [esp+1B3Ch+var_1B28]
00B117C5  push    edx
00B117C6  push    eax
00B117C7  call    sub_B02DF0
00B117CC  add     esp, 8
00B117CF  test    al, al
00B117D1  jz      loc_B116FB
00B117D7  lea     ecx, [esp+1B3Ch+var_1B1C]
00B117DB  push    ecx
```

## E8 字段 7：`target_z`（u16，偏移 12，长度 2）

```asm
; VA: 0x0xB117EF 附近（支援目标 Z）
00B117E5  mov     eax, [esp+1B3Ch+var_1B18]
00B117E9  lea     edx, [esp+1B3Ch+var_1B28]
00B117ED  push    edx
00B117EE  push    eax
00B117EF  call    sub_B02DF0
00B117F4  add     esp, 8
00B117F7  test    al, al
00B117F9  jz      loc_B116FB
00B117FF  lea     ecx, [esp+1B3Ch+var_1B1C]
00B11803  push    ecx
```

## E9 字段 8：`count`（u16，偏移 14，长度 2）

```asm
; VA: 0x0xB11817 附近（支援倒计时计数）
00B1180D  mov     eax, [esp+1B3Ch+var_1B20]
00B11811  lea     edx, [esp+1B3Ch+var_1B28]
00B11815  push    edx
00B11816  push    eax
00B11817  call    sub_B02DF0
00B1181C  add     esp, 8
00B1181F  test    al, al
00B11821  jz      loc_B116FB
00B11827  lea     ecx, [esp+1B3Ch+var_1B1C]
00B1182B  push    ecx
```

## E10 字段 9：`is_hit_send`（u8，偏移 16，长度 1）

```asm
; VA: 0x0xB1183F 附近（是否已发送命中）
00B11835  mov     eax, [esp+1B3Ch+var_1B2C]
00B11839  lea     edx, [esp+1B3Ch+var_1B28]
00B1183D  push    edx
00B1183E  push    eax
00B1183F  call    sub_B06230
00B11844  add     esp, 8
00B11847  test    al, al
00B11849  jz      loc_B116FB
00B1184F  mov     ebx, [esp+1B3Ch+var_1B28]
00B11853  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E11 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB11853
00B1183E  push    eax
00B1183F  call    sub_B06230
00B11844  add     esp, 8
00B11847  test    al, al
00B11849  jz      loc_B116FB
00B1184F  mov     ebx, [esp+1B3Ch+var_1B28]
00B11853  cmp     ebx, [esp+1B3Ch+var_1B24]
00B11857  mov     ecx, esi
00B11859  jz      short loc_B11875
00B1185B  mov     edx, [esi]
00B1185D  mov     eax, [edx+64h]
00B11860  push    1
00B11862  push    0E6h
00B11867  call    eax
```
