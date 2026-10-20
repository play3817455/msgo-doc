# 汇编证据 —— SC-0x1A39-lounge-pilot_tutorial_step_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB56CE1`）

```asm
; VA: 0xB56CCC .. （块入口，含守卫与容量申请）
00B56CCC  call    sub_B41120
00B56CD1  test    al, al
00B56CD3  jz      loc_B890FE
00B56CD9  mov     ecx, [esi+0Ch]
00B56CDC  mov     eax, [ecx]
00B56CDE  mov     edx, [eax+78h]
00B56CE1  push    10h
00B56CE3  call    edx
00B56CE5  mov     [esp+2C5Ch+var_2C48], eax
00B56CE9  mov     eax, [esi+0Ch]
00B56CEC  push    eax
00B56CED  lea     ecx, [esp+2C60h+var_29B4]
00B56CF4  call    sub_ABB2F0
00B56CF9  lea     ecx, [esp+2C5Ch+var_2C48]
```

## E2 字段 1：`tuto_step`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB56D1C 附近（教学当前步骤）
00B56D12  mov     eax, [esp+2C5Ch+var_2C30]
00B56D16  lea     edx, [esp+2C5Ch+var_2C44]
00B56D1A  push    edx
00B56D1B  push    eax
00B56D1C  call    sub_B02DD0
00B56D21  add     esp, 8
00B56D24  test    al, al
00B56D26  jnz     short loc_B56D41
00B56D28  mov     edx, [esi]
00B56D2A  mov     eax, [edx+64h]
```

## E3 字段 2：`tuto_flags`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB56D59 附近（教学进度标志位（64 位位域））
00B56D4F  mov     eax, [esp+2C5Ch+var_2C34]
00B56D53  lea     edx, [esp+2C5Ch+var_2C44]
00B56D57  push    edx
00B56D58  push    eax
00B56D59  call    sub_B06200
00B56D5E  add     esp, 8
00B56D61  test    al, al
00B56D63  jz      short loc_B56D28
00B56D65  lea     ecx, [esp+2C5Ch+var_2C48]
00B56D69  push    ecx
```

## E4 字段 3：`tuto_missionid`（u32，偏移 12，长度 4）

```asm
; VA: 0x0xB56D7D 附近（教学任务 ID）
00B56D73  mov     eax, [esp+2C5Ch+var_2C38]
00B56D77  lea     edx, [esp+2C5Ch+var_2C44]
00B56D7B  push    edx
00B56D7C  push    eax
00B56D7D  call    sub_B02DD0
00B56D82  add     esp, 8
00B56D85  test    al, al
00B56D87  jz      short loc_B56D28
00B56D89  mov     ebx, [esp+2C5Ch+var_2C44]
00B56D8D  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB56D8D
00B56D7C  push    eax
00B56D7D  call    sub_B02DD0
00B56D82  add     esp, 8
00B56D85  test    al, al
00B56D87  jz      short loc_B56D28
00B56D89  mov     ebx, [esp+2C5Ch+var_2C44]
00B56D8D  cmp     ebx, [esp+2C5Ch+var_2C40]
00B56D91  mov     ecx, esi
00B56D93  jz      short loc_B56DAC
00B56D95  mov     edx, [esi]
00B56D97  mov     eax, [edx+64h]
00B56D9A  push    1
00B56D9C  push    1Bh
00B56D9E  call    eax
```
