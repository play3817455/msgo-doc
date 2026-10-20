# 汇编证据 —— SC-0x1A13-battle-weapon_fire__hand_throw_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1D` @ `0xB10A44`）

```asm
; VA: 0xB10A2B .. （块入口，含守卫与容量申请）
00B10A2B  push    7Eh ; '~'
00B10A2D  mov     ecx, esi
00B10A2F  call    sub_B05DA0
00B10A34  test    al, al
00B10A36  jz      loc_B317C7
00B10A3C  mov     ecx, [esi+0Ch]
00B10A3F  mov     edx, [ecx]
00B10A41  mov     eax, [edx+78h]
00B10A44  push    1Dh
00B10A46  call    eax
00B10A48  mov     ecx, [esi+0Ch]
00B10A4B  push    ecx
00B10A4C  lea     ecx, [esp+1B40h+var_1A94]
00B10A53  mov     [esp+1B40h+var_1B1C], eax
```

## E2 字段 1：`ent_id`（u16，偏移 0，长度 2）

```asm
; VA: 0x0xB10A7F 附近（发射者实体 ID）
00B10A75  mov     ecx, [esp+1B3Ch+var_1AD0]
00B10A79  lea     eax, [esp+1B3Ch+var_1B28]
00B10A7D  push    eax
00B10A7E  push    ecx
00B10A7F  call    sub_B02DF0
00B10A84  add     esp, 8
00B10A87  test    al, al
00B10A89  jnz     short loc_B10AA4
00B10A8B  mov     edx, [esi]
00B10A8D  mov     eax, [edx+64h]
```

## E3 字段 2：`itemid`（u32，偏移 2，长度 4）

```asm
; VA: 0x0xB10ABC 附近（投掷物道具 ID）
00B10AB2  mov     eax, [esp+1B3Ch+var_1ACC]
00B10AB6  lea     edx, [esp+1B3Ch+var_1B28]
00B10ABA  push    edx
00B10ABB  push    eax
00B10ABC  call    sub_B02DD0
00B10AC1  add     esp, 8
00B10AC4  test    al, al
00B10AC6  jz      short loc_B10A8B
00B10AC8  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10ACC  push    ecx
```

## E4 字段 3：`grenade_id`（u32，偏移 6，长度 4）

```asm
; VA: 0x0xB10AE0 附近（手雷（投掷武器）ID）
00B10AD6  mov     eax, [esp+1B3Ch+var_1AD4]
00B10ADA  lea     edx, [esp+1B3Ch+var_1B28]
00B10ADE  push    edx
00B10ADF  push    eax
00B10AE0  call    sub_B02DD0
00B10AE5  add     esp, 8
00B10AE8  test    al, al
00B10AEA  jz      short loc_B10A8B
00B10AEC  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10AF0  push    ecx
```

## E5 字段 4：`launch_x`（u16，偏移 10，长度 2）

```asm
; VA: 0x0xB10B04 附近（投掷起点 X）
00B10AFA  mov     eax, [esp+1B3Ch+var_1AD8]
00B10AFE  lea     edx, [esp+1B3Ch+var_1B28]
00B10B02  push    edx
00B10B03  push    eax
00B10B04  call    sub_B02DF0
00B10B09  add     esp, 8
00B10B0C  test    al, al
00B10B0E  jz      loc_B10A8B
00B10B14  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10B18  push    ecx
```

## E6 字段 5：`launch_y`（u16，偏移 12，长度 2）

```asm
; VA: 0x0xB10B2C 附近（投掷起点 Y）
00B10B22  mov     eax, [esp+1B3Ch+var_1ADC]
00B10B26  lea     edx, [esp+1B3Ch+var_1B28]
00B10B2A  push    edx
00B10B2B  push    eax
00B10B2C  call    sub_B02DF0
00B10B31  add     esp, 8
00B10B34  test    al, al
00B10B36  jz      loc_B10A8B
00B10B3C  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10B40  push    ecx
```

## E7 字段 6：`launch_z`（u16，偏移 14，长度 2）

```asm
; VA: 0x0xB10B54 附近（投掷起点 Z）
00B10B4A  mov     eax, [esp+1B3Ch+var_1AE0]
00B10B4E  lea     edx, [esp+1B3Ch+var_1B28]
00B10B52  push    edx
00B10B53  push    eax
00B10B54  call    sub_B02DF0
00B10B59  add     esp, 8
00B10B5C  test    al, al
00B10B5E  jz      loc_B10A8B
00B10B64  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10B68  push    ecx
```

## E8 字段 7：`target_x`（u16，偏移 16，长度 2）

```asm
; VA: 0x0xB10B7C 附近（落点 X）
00B10B72  mov     eax, [esp+1B3Ch+var_1AF0]
00B10B76  lea     edx, [esp+1B3Ch+var_1B28]
00B10B7A  push    edx
00B10B7B  push    eax
00B10B7C  call    sub_B02DF0
00B10B81  add     esp, 8
00B10B84  test    al, al
00B10B86  jz      loc_B10A8B
00B10B8C  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10B90  push    ecx
```

## E9 字段 8：`target_y`（u16，偏移 18，长度 2）

```asm
; VA: 0x0xB10BA4 附近（落点 Y）
00B10B9A  mov     eax, [esp+1B3Ch+var_1AF8]
00B10B9E  lea     edx, [esp+1B3Ch+var_1B28]
00B10BA2  push    edx
00B10BA3  push    eax
00B10BA4  call    sub_B02DF0
00B10BA9  add     esp, 8
00B10BAC  test    al, al
00B10BAE  jz      loc_B10A8B
00B10BB4  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10BB8  push    ecx
```

## E10 字段 9：`target_z`（u16，偏移 20，长度 2）

```asm
; VA: 0x0xB10BCC 附近（落点 Z）
00B10BC2  mov     eax, [esp+1B3Ch+var_1AEC]
00B10BC6  lea     edx, [esp+1B3Ch+var_1B28]
00B10BCA  push    edx
00B10BCB  push    eax
00B10BCC  call    sub_B02DF0
00B10BD1  add     esp, 8
00B10BD4  test    al, al
00B10BD6  jz      loc_B10A8B
00B10BDC  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10BE0  push    ecx
```

## E11 字段 10：`target_ent_id`（u16，偏移 22，长度 2）

```asm
; VA: 0x0xB10BF4 附近（目标实体 ID）
00B10BEA  mov     eax, [esp+1B3Ch+var_1B00]
00B10BEE  lea     edx, [esp+1B3Ch+var_1B28]
00B10BF2  push    edx
00B10BF3  push    eax
00B10BF4  call    sub_B02DF0
00B10BF9  add     esp, 8
00B10BFC  test    al, al
00B10BFE  jz      loc_B10A8B
00B10C04  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10C08  push    ecx
```

## E12 字段 11：`msec`（u16，偏移 24，长度 2）

```asm
; VA: 0x0xB10C1C 附近（飞行/引爆计时（毫秒））
00B10C12  mov     eax, [esp+1B3Ch+var_1B0C]
00B10C16  lea     edx, [esp+1B3Ch+var_1B28]
00B10C1A  push    edx
00B10C1B  push    eax
00B10C1C  call    sub_B02DF0
00B10C21  add     esp, 8
00B10C24  test    al, al
00B10C26  jz      loc_B10A8B
00B10C2C  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10C30  push    ecx
```

## E13 字段 12：`shot0_impact1`（u8，偏移 26，长度 1）

```asm
; VA: 0x0xB10C44 附近（第 0 发射击命中标志）
00B10C3A  mov     eax, [esp+1B3Ch+var_1B18]
00B10C3E  lea     edx, [esp+1B3Ch+var_1B28]
00B10C42  push    edx
00B10C43  push    eax
00B10C44  call    sub_B06230
00B10C49  add     esp, 8
00B10C4C  test    al, al
00B10C4E  jz      loc_B10A8B
00B10C54  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10C58  push    ecx
```

## E14 字段 13：`fx_opt`（u8，偏移 27，长度 1）

```asm
; VA: 0x0xB10C6C 附近（特效选项位）
00B10C62  mov     eax, [esp+1B3Ch+var_1B20]
00B10C66  lea     edx, [esp+1B3Ch+var_1B28]
00B10C6A  push    edx
00B10C6B  push    eax
00B10C6C  call    sub_B06230
00B10C71  add     esp, 8
00B10C74  test    al, al
00B10C76  jz      loc_B10A8B
00B10C7C  lea     ecx, [esp+1B3Ch+var_1B1C]
00B10C80  push    ecx
```

## E15 字段 14：`charge_lv`（u8，偏移 28，长度 1）

```asm
; VA: 0x0xB10C94 附近（蓄力等级）
00B10C8A  mov     eax, [esp+1B3Ch+var_1B2C]
00B10C8E  lea     edx, [esp+1B3Ch+var_1B28]
00B10C92  push    edx
00B10C93  push    eax
00B10C94  call    sub_B06230
00B10C99  add     esp, 8
00B10C9C  test    al, al
00B10C9E  jz      loc_B10A8B
00B10CA4  mov     ebx, [esp+1B3Ch+var_1B28]
00B10CA8  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E16 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB10CA8
00B10C93  push    eax
00B10C94  call    sub_B06230
00B10C99  add     esp, 8
00B10C9C  test    al, al
00B10C9E  jz      loc_B10A8B
00B10CA4  mov     ebx, [esp+1B3Ch+var_1B28]
00B10CA8  cmp     ebx, [esp+1B3Ch+var_1B24]
00B10CAC  mov     ecx, esi
00B10CAE  jz      short loc_B10CC7
00B10CB0  mov     edx, [esi]
00B10CB2  mov     eax, [edx+64h]
00B10CB5  push    1
00B10CB7  push    7Eh ; '~'
00B10CB9  call    eax
```
