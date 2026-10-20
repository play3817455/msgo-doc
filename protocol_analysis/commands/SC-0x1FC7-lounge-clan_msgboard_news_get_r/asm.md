# 汇编证据 —— SC-0x1FC7-lounge-clan_msgboard_news_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xE91` @ `0xB581A2`）

```asm
; VA: 0xB58186 .. （块入口，含守卫与容量申请）
00B58186  push    1D4h
00B5818B  mov     ecx, esi
00B5818D  call    sub_B41120
00B58192  test    al, al
00B58194  jz      loc_B890FE
00B5819A  mov     ecx, [esi+0Ch]
00B5819D  mov     eax, [ecx]
00B5819F  mov     edx, [eax+78h]
00B581A2  push    0E91h
00B581A7  call    edx
00B581A9  mov     [esp+2C5Ch+var_2C38], eax
00B581AD  mov     eax, [esi+0Ch]
00B581B0  push    eax
00B581B1  lea     ecx, [esp+2C60h+var_2AD0]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB581E0 附近（战队留言板新闻查询结果码）
00B581D6  mov     eax, [esp+2C5Ch+var_2C30]
00B581DA  lea     edx, [esp+2C5Ch+var_2C44]
00B581DE  push    edx
00B581DF  push    eax
00B581E0  call    sub_B02DD0
00B581E5  add     esp, 8
00B581E8  test    al, al
00B581EA  jnz     short loc_B58208
00B581EC  mov     edx, [esi]
00B581EE  mov     eax, [edx+64h]
```

## E3 字段 2：`news_num`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB58212 附近（新闻条目数 N）
00B58208  lea     ecx, [esp+2C5Ch+var_2C44]
00B5820C  push    ecx
00B5820D  lea     edx, [esp+2C60h+var_2C34]
00B58211  push    edx
00B58212  call    sub_B02DD0
00B58217  add     esp, 8
00B5821A  test    al, al
00B5821C  jnz     short loc_B5823A
00B5821E  mov     eax, [esi]
00B58220  mov     edx, [eax+64h]
```

## E4 字段 3：`news`（array<elem 242>，偏移 8，长度 242·N）

```asm
; VA: 0x0xB5826A 附近（战队新闻列表（元素线上 242B / 缓冲槽步进 248B））
00B58260  mov     eax, [esp+2C5Ch+var_2C48]
00B58264  lea     edx, [esp+2C5Ch+var_2C44]
00B58268  push    edx
00B58269  push    eax
00B5826A  call    sub_B45D20
00B5826F  add     esp, 8
00B58272  test    al, al
00B58274  jz      short loc_B58287
00B58276  add     [esp+2C5Ch+var_2C48], 0F8h
00B5827E  add     edi, 1
```

## E6 字段 5：`clan_kind`（u8，偏移 数组后，长度 1）

```asm
; VA: 0x0xB582AF 附近（战队类别）
00B582A5  mov     eax, [esp+2C5Ch+var_2C48]
00B582A9  lea     edx, [esp+2C5Ch+var_2C44]
00B582AD  push    edx
00B582AE  push    eax
00B582AF  call    sub_B06230
00B582B4  add     esp, 8
00B582B7  test    al, al
00B582B9  jz      loc_B581EC
00B582BF  mov     ecx, [esp+2C5Ch+var_2C44]
00B582C3  cmp     ecx, [esp+2C5Ch+var_2C40]
```

## E7 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB582C3
00B582AE  push    eax
00B582AF  call    sub_B06230
00B582B4  add     esp, 8
00B582B7  test    al, al
00B582B9  jz      loc_B581EC
00B582BF  mov     ecx, [esp+2C5Ch+var_2C44]
00B582C3  cmp     ecx, [esp+2C5Ch+var_2C40]
00B582C7  mov     ecx, esi
00B582C9  jz      short loc_B582E5
00B582CB  mov     edx, [esi]
00B582CD  mov     eax, [edx+64h]
00B582D0  push    1
00B582D2  push    1D4h
00B582D7  call    eax
```
