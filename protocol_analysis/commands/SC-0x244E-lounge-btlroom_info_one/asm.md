# 汇编证据 —— SC-0x244E-lounge-btlroom_info_one

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA9` @ `0xB58B72`）

```asm
; VA: 0xB58B5D .. （块入口，含守卫与容量申请）
00B58B5D  call    sub_B41120
00B58B62  test    al, al
00B58B64  jz      loc_B890FE
00B58B6A  mov     ecx, [esi+0Ch]
00B58B6D  mov     eax, [ecx]
00B58B6F  mov     edx, [eax+78h]
00B58B72  push    0A9h
00B58B77  call    edx
00B58B79  mov     [esp+2C5Ch+var_2C24], eax
00B58B7D  mov     eax, [esi+0Ch]
00B58B80  push    eax
00B58B81  lea     ecx, [esp+2C60h+var_2AAC]
00B58B88  call    sub_ABB2F0
00B58B8D  lea     ecx, [esp+2C5Ch+var_2C24]
```

## E2 字段 1：`is_new`（u8，偏移 0，长度 1）

```asm
; VA: 0x0xB58BB0 附近（是否新建房间）
00B58BA6  mov     eax, [esp+2C5Ch+var_2C30]
00B58BAA  lea     edx, [esp+2C5Ch+var_2C44]
00B58BAE  push    edx
00B58BAF  push    eax
00B58BB0  call    sub_B06230
00B58BB5  add     esp, 8
00B58BB8  test    al, al
00B58BBA  jnz     short loc_B58BD8
00B58BBC  mov     edx, [esi]
00B58BBE  mov     eax, [edx+64h]
```

## E3 字段 2：`roominfo`（struct{95/槽144}，偏移 1，长度 95）

```asm
; VA: 0x0xB58BF0 附近（对战房间信息结构体（线上 95B；缓冲槽步进 144））
00B58BE6  mov     eax, [esp+2C5Ch+var_2C34]
00B58BEA  lea     edx, [esp+2C5Ch+var_2C44]
00B58BEE  push    edx
00B58BEF  push    eax
00B58BF0  call    sub_B44880
00B58BF5  add     esp, 8
00B58BF8  test    al, al
00B58BFA  jz      short loc_B58BBC
00B58BFC  lea     ecx, [esp+2C5Ch+var_2C24]
00B58C00  push    ecx
```

## E12 字段 11：`clan_eff`（struct{12}，偏移 数组后，长度 12）

```asm
; VA: 0x0xB58C14 附近（联邦侧战队编成信息）
00B58C0A  mov     eax, [esp+2C5Ch+var_2C38]
00B58C0E  lea     edx, [esp+2C5Ch+var_2C44]
00B58C12  push    edx
00B58C13  push    eax
00B58C14  call    sub_B45F30
00B58C19  add     esp, 8
00B58C1C  test    al, al
00B58C1E  jz      short loc_B58BBC
00B58C20  lea     ecx, [esp+2C5Ch+var_2C24]
00B58C24  push    ecx
```

## E13 字段 12：`clan_zeon`（struct{12}，偏移 数组后，长度 12）

```asm
; VA: 0x0xB58C38 附近（吉翁侧战队编成信息）
00B58C2E  mov     eax, [esp+2C5Ch+var_2C48]
00B58C32  lea     edx, [esp+2C5Ch+var_2C44]
00B58C36  push    edx
00B58C37  push    eax
00B58C38  call    sub_B45F30
00B58C3D  add     esp, 8
00B58C40  test    al, al
00B58C42  jz      loc_B58BBC
00B58C48  mov     ebx, [esp+2C5Ch+var_2C44]
00B58C4C  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E20 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB58C4C
00B58C37  push    eax
00B58C38  call    sub_B45F30
00B58C3D  add     esp, 8
00B58C40  test    al, al
00B58C42  jz      loc_B58BBC
00B58C48  mov     ebx, [esp+2C5Ch+var_2C44]
00B58C4C  cmp     ebx, [esp+2C5Ch+var_2C40]
00B58C50  mov     ecx, esi
00B58C52  jz      short loc_B58C6E
00B58C54  mov     edx, [esi]
00B58C56  mov     eax, [edx+64h]
00B58C59  push    1
00B58C5B  push    87h
00B58C60  call    eax
```
