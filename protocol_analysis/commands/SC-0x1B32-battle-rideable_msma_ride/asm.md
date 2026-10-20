# 汇编证据 —— SC-0x1B32-battle-rideable_msma_ride

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1A` @ `0xB112B5`）

```asm
; VA: 0xB11299 .. （块入口，含守卫与容量申请）
00B11299  push    103h
00B1129E  mov     ecx, esi
00B112A0  call    sub_B05DA0
00B112A5  test    al, al
00B112A7  jz      loc_B317C7
00B112AD  mov     ecx, [esi+0Ch]
00B112B0  mov     eax, [ecx]
00B112B2  mov     edx, [eax+78h]
00B112B5  push    1Ah
00B112B7  call    edx
00B112B9  mov     [esp+1B3Ch+var_1AF4], eax
00B112BD  mov     eax, [esi+0Ch]
00B112C0  push    eax
00B112C1  lea     ecx, [esp+1B40h+var_1A48]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB112F0 附近（搭乘（ride）结果码）
00B112E6  mov     eax, [esp+1B3Ch+var_1AF0]
00B112EA  lea     edx, [esp+1B3Ch+var_1B28]
00B112EE  push    edx
00B112EF  push    eax
00B112F0  call    sub_B02DD0
00B112F5  add     esp, 8
00B112F8  test    al, al
00B112FA  jnz     short loc_B11318
00B112FC  mov     edx, [esi]
00B112FE  mov     eax, [edx+64h]
```

## E3 字段 2：`access_type`（u16，偏移 4，长度 2）

```asm
; VA: 0x0xB11330 附近（可搭乘方式/权限类型）
00B11326  mov     eax, [esp+1B3Ch+var_1AF8]
00B1132A  lea     edx, [esp+1B3Ch+var_1B28]
00B1132E  push    edx
00B1132F  push    eax
00B11330  call    sub_B02DF0
00B11335  add     esp, 8
00B11338  test    al, al
00B1133A  jz      short loc_B112FC
00B1133C  lea     ecx, [esp+1B3Ch+var_1AF4]
00B11340  push    ecx
```

## E4 字段 3：`from_world_id`（u32，偏移 6，长度 4）

```asm
; VA: 0x0xB11354 附近（来源大区 ID）
00B1134A  mov     eax, [esp+1B3Ch+var_1AEC]
00B1134E  lea     edx, [esp+1B3Ch+var_1B28]
00B11352  push    edx
00B11353  push    eax
00B11354  call    sub_B02DD0
00B11359  add     esp, 8
00B1135C  test    al, al
00B1135E  jz      short loc_B112FC
00B11360  lea     ecx, [esp+1B3Ch+var_1AF4]
00B11364  push    ecx
```

## E5 字段 4：`from_pilot_id`（u32，偏移 10，长度 4）

```asm
; VA: 0x0xB11378 附近（来源驾驶员 ID）
00B1136E  mov     eax, [esp+1B3Ch+var_1B00]
00B11372  lea     edx, [esp+1B3Ch+var_1B28]
00B11376  push    edx
00B11377  push    eax
00B11378  call    sub_B02DD0
00B1137D  add     esp, 8
00B11380  test    al, al
00B11382  jz      loc_B112FC
00B11388  lea     ecx, [esp+1B3Ch+var_1AF4]
00B1138C  push    ecx
```

## E6 字段 5：`from_ent_id`（u16，偏移 14，长度 2）

```asm
; VA: 0x0xB113A0 附近（来源实体 ID）
00B11396  mov     eax, [esp+1B3Ch+var_1B0C]
00B1139A  lea     edx, [esp+1B3Ch+var_1B28]
00B1139E  push    edx
00B1139F  push    eax
00B113A0  call    sub_B02DF0
00B113A5  add     esp, 8
00B113A8  test    al, al
00B113AA  jz      loc_B112FC
00B113B0  lea     ecx, [esp+1B3Ch+var_1AF4]
00B113B4  push    ecx
```

## E7 字段 6：`to_ent_id`（u16，偏移 16，长度 2）

```asm
; VA: 0x0xB113C8 附近（目标实体 ID）
00B113BE  mov     eax, [esp+1B3Ch+var_1B18]
00B113C2  lea     edx, [esp+1B3Ch+var_1B28]
00B113C6  push    edx
00B113C7  push    eax
00B113C8  call    sub_B02DF0
00B113CD  add     esp, 8
00B113D0  test    al, al
00B113D2  jz      loc_B112FC
00B113D8  lea     ecx, [esp+1B3Ch+var_1AF4]
00B113DC  push    ecx
```

## E8 字段 7：`hp_now`（u32，偏移 18，长度 4）

```asm
; VA: 0x0xB113F0 附近（当前 HP）
00B113E6  mov     eax, [esp+1B3Ch+var_1B20]
00B113EA  lea     edx, [esp+1B3Ch+var_1B28]
00B113EE  push    edx
00B113EF  push    eax
00B113F0  call    sub_B02DD0
00B113F5  add     esp, 8
00B113F8  test    al, al
00B113FA  jz      loc_B112FC
00B11400  lea     ecx, [esp+1B3Ch+var_1AF4]
00B11404  push    ecx
```

## E9 字段 8：`hp_max`（u32，偏移 22，长度 4）

```asm
; VA: 0x0xB11418 附近（最大 HP）
00B1140E  mov     eax, [esp+1B3Ch+var_1B2C]
00B11412  lea     edx, [esp+1B3Ch+var_1B28]
00B11416  push    edx
00B11417  push    eax
00B11418  call    sub_B02DD0
00B1141D  add     esp, 8
00B11420  test    al, al
00B11422  jz      loc_B112FC
00B11428  mov     ebx, [esp+1B3Ch+var_1B28]
00B1142C  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E10 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1142C
00B11417  push    eax
00B11418  call    sub_B02DD0
00B1141D  add     esp, 8
00B11420  test    al, al
00B11422  jz      loc_B112FC
00B11428  mov     ebx, [esp+1B3Ch+var_1B28]
00B1142C  cmp     ebx, [esp+1B3Ch+var_1B24]
00B11430  mov     ecx, esi
00B11432  jz      short loc_B1144E
00B11434  mov     edx, [esi]
00B11436  mov     eax, [edx+64h]
00B11439  push    1
00B1143B  push    103h
00B11440  call    eax
```
