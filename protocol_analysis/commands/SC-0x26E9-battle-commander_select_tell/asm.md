# 汇编证据 —— SC-0x26E9-battle-commander_select_tell

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB12BC7`）

```asm
; VA: 0xB12BAB .. （块入口，含守卫与容量申请）
00B12BAB  push    0D5h
00B12BB0  mov     ecx, esi
00B12BB2  call    sub_B05DA0
00B12BB7  test    al, al
00B12BB9  jz      loc_B317C7
00B12BBF  mov     ecx, [esi+0Ch]
00B12BC2  mov     eax, [ecx]
00B12BC4  mov     edx, [eax+78h]
00B12BC7  push    6
00B12BC9  call    edx
00B12BCB  mov     [esp+1B3Ch+var_1B2C], eax
00B12BCF  mov     eax, [esi+0Ch]
00B12BD2  push    eax
00B12BD3  lea     ecx, [esp+1B40h+var_18DC]
```

## E2 字段 1：`team`（u8，偏移 0，长度 1）

```asm
; VA: 0x0xB12C02 附近（阵营）
00B12BF8  mov     eax, [esp+1B3Ch+var_1B0C]
00B12BFC  lea     edx, [esp+1B3Ch+var_1B28]
00B12C00  push    edx
00B12C01  push    eax
00B12C02  call    sub_B06230
00B12C07  add     esp, 8
00B12C0A  test    al, al
00B12C0C  jnz     short loc_B12C2A
00B12C0E  mov     edx, [esi]
00B12C10  mov     eax, [edx+64h]
```

## E3 字段 2：`troops`（u8，偏移 1，长度 1）

```asm
; VA: 0x0xB12C42 附近（势力）
00B12C38  mov     eax, [esp+1B3Ch+var_1B18]
00B12C3C  lea     edx, [esp+1B3Ch+var_1B28]
00B12C40  push    edx
00B12C41  push    eax
00B12C42  call    sub_B06230
00B12C47  add     esp, 8
00B12C4A  test    al, al
00B12C4C  jz      short loc_B12C0E
00B12C4E  lea     ecx, [esp+1B3Ch+var_1B2C]
00B12C52  push    ecx
```

## E4 字段 3：`commander_id`（u32，偏移 2，长度 4）

```asm
; VA: 0x0xB12C66 附近（指挥官 ID）
00B12C5C  mov     eax, [esp+1B3Ch+var_1B20]
00B12C60  lea     edx, [esp+1B3Ch+var_1B28]
00B12C64  push    edx
00B12C65  push    eax
00B12C66  call    sub_B02DD0
00B12C6B  add     esp, 8
00B12C6E  test    al, al
00B12C70  jz      short loc_B12C0E
00B12C72  mov     ebx, [esp+1B3Ch+var_1B28]
00B12C76  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12C76
00B12C65  push    eax
00B12C66  call    sub_B02DD0
00B12C6B  add     esp, 8
00B12C6E  test    al, al
00B12C70  jz      short loc_B12C0E
00B12C72  mov     ebx, [esp+1B3Ch+var_1B28]
00B12C76  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12C7A  mov     ecx, esi
00B12C7C  jz      short loc_B12C98
00B12C7E  mov     edx, [esi]
00B12C80  mov     eax, [edx+64h]
00B12C83  push    1
00B12C85  push    0D5h
00B12C8A  call    eax
```
