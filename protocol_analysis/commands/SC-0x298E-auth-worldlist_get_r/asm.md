# 汇编证据 —— SC-0x298E-auth-worldlist_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x278C` @ `0xB03DDD`）

```asm
; VA: 0xB03DC8 .. （块入口，含守卫与容量申请）
00B03DC8  call    sub_B02C90
00B03DCD  test    al, al
00B03DCF  jz      loc_B04C46
00B03DD5  mov     ecx, [esi+0Ch]
00B03DD8  mov     edx, [ecx]
00B03DDA  mov     eax, [edx+78h]
00B03DDD  push    278Ch
00B03DE2  call    eax
00B03DE4  mov     ecx, [esi+0Ch]
00B03DE7  push    ecx
00B03DE8  lea     ecx, [esp+128h+var_110]
00B03DEC  mov     edi, eax
00B03DEE  call    sub_ABB2F0
00B03DF3  mov     eax, edi
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB03E0D 附近（大区列表查询结果码）
00B03DFA  push    eax
00B03DFB  mov     [esp+12Ch+var_4], 9
00B03E06  mov     [esp+12Ch+var_F0], eax
00B03E0A  add     edi, 4
00B03E0D  call    sub_B02DD0
00B03E12  add     esp, 8
00B03E15  test    al, al
00B03E17  jnz     short loc_B03E3B
00B03E19  mov     eax, [esi]
00B03E1B  mov     edx, [eax+64h]
```

## E3 字段 2：`last_world`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB03E4E 附近（上次登录的大区 ID）
00B03E42  add     edi, 4
00B03E45  push    eax
00B03E46  mov     [esp+12Ch+var_F8], eax
00B03E4A  mov     [esp+12Ch+var_F4], edi
00B03E4E  call    sub_B02DD0
00B03E53  add     esp, 8
00B03E56  test    al, al
00B03E58  jnz     short loc_B03E63
00B03E5A  push    1
00B03E5C  push    0Bh
```

## E4 字段 3：`worlds_num`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB03E6D 附近（大区条目数 N）
00B03E63  lea     ecx, [esp+124h+var_10C]
00B03E67  push    ecx
00B03E68  lea     edx, [esp+128h+var_100]
00B03E6C  push    edx
00B03E6D  call    sub_B02DD0
00B03E72  add     esp, 8
00B03E75  test    al, al
00B03E77  jz      short loc_B03E19
00B03E79  mov     ebx, [esp+124h+var_100]
00B03E7D  cmp     ebx, 20h ; ' '
```

## E5 字段 4：`worlds`（array<elem 309>，偏移 12，长度 309·N）

```asm
; VA: 0x0xB03EA6 附近（大区列表（N ≤ 32；元素线上 309B / 缓冲槽步进 316B））
00B03E9D  align 10h
00B03EA0  lea     ecx, [esp+124h+var_10C]
00B03EA4  push    ecx
00B03EA5  push    ebp
00B03EA6  call    sub_B02E20
00B03EAB  add     esp, 8
00B03EAE  test    al, al
00B03EB0  jz      short loc_B03EC1
00B03EB2  add     edi, 1
00B03EB5  add     ebp, 13Ch
```

## E14 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB03ED2
00B03EC3  mov     eax, [edx+64h]
00B03EC6  push    1
00B03EC8  push    0Bh
00B03ECA  mov     ecx, esi
00B03ECC  call    eax
00B03ECE  mov     ecx, [esp+124h+var_10C]
00B03ED2  cmp     ecx, [esp+124h+var_108]
00B03ED6  jnz     short loc_B03E5A
00B03ED8  mov     edi, [esi+3B4h]
00B03EDE  test    edi, edi
00B03EE0  jz      loc_B04038
00B03EE6  lea     ecx, [esp+124h+var_EC]
00B03EEA  push    ecx
00B03EEB  call    sub_CA0CE0
```
