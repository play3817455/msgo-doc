# 汇编证据 —— SC-0x214C-battle-commander_support_rendition_end

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x7` @ `0xB124B9`）

```asm
; VA: 0xB124A4 .. （块入口，含守卫与容量申请）
00B124A4  call    sub_B05DA0
00B124A9  test    al, al
00B124AB  jz      loc_B317C7
00B124B1  mov     ecx, [esi+0Ch]
00B124B4  mov     eax, [ecx]
00B124B6  mov     edx, [eax+78h]
00B124B9  push    7
00B124BB  call    edx
00B124BD  mov     [esp+1B3Ch+var_1B2C], eax
00B124C1  mov     eax, [esi+0Ch]
00B124C4  push    eax
00B124C5  lea     ecx, [esp+1B40h+var_1994]
00B124CC  call    sub_ABB2F0
00B124D1  lea     ecx, [esp+1B3Ch+var_1B2C]
```

## E2 字段 1：`team`（u8，偏移 0，长度 1）

```asm
; VA: 0x0xB124F4 附近（阵营）
00B124EA  mov     eax, [esp+1B3Ch+var_1B00]
00B124EE  lea     edx, [esp+1B3Ch+var_1B28]
00B124F2  push    edx
00B124F3  push    eax
00B124F4  call    sub_B06230
00B124F9  add     esp, 8
00B124FC  test    al, al
00B124FE  jnz     short loc_B1251C
00B12500  mov     edx, [esi]
00B12502  mov     eax, [edx+64h]
```

## E3 字段 2：`troops`（u8，偏移 1，长度 1）

```asm
; VA: 0x0xB12534 附近（势力）
00B1252A  mov     eax, [esp+1B3Ch+var_1B0C]
00B1252E  lea     edx, [esp+1B3Ch+var_1B28]
00B12532  push    edx
00B12533  push    eax
00B12534  call    sub_B06230
00B12539  add     esp, 8
00B1253C  test    al, al
00B1253E  jz      short loc_B12500
00B12540  lea     ecx, [esp+1B3Ch+var_1B2C]
00B12544  push    ecx
```

## E4 字段 3：`support_type`（u32，偏移 2，长度 4）

```asm
; VA: 0x0xB12558 附近（支援类型）
00B1254E  mov     eax, [esp+1B3Ch+var_1B18]
00B12552  lea     edx, [esp+1B3Ch+var_1B28]
00B12556  push    edx
00B12557  push    eax
00B12558  call    sub_B02DD0
00B1255D  add     esp, 8
00B12560  test    al, al
00B12562  jz      short loc_B12500
00B12564  lea     ecx, [esp+1B3Ch+var_1B2C]
00B12568  push    ecx
```

## E5 字段 4：`spt_spot_index`（u8，偏移 6，长度 1）

```asm
; VA: 0x0xB1257C 附近（支援投放点下标）
00B12572  mov     eax, [esp+1B3Ch+var_1B20]
00B12576  lea     edx, [esp+1B3Ch+var_1B28]
00B1257A  push    edx
00B1257B  push    eax
00B1257C  call    sub_B06230
00B12581  add     esp, 8
00B12584  test    al, al
00B12586  jz      loc_B12500
00B1258C  mov     ebx, [esp+1B3Ch+var_1B28]
00B12590  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12590
00B1257B  push    eax
00B1257C  call    sub_B06230
00B12581  add     esp, 8
00B12584  test    al, al
00B12586  jz      loc_B12500
00B1258C  mov     ebx, [esp+1B3Ch+var_1B28]
00B12590  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12594  mov     ecx, esi
00B12596  jz      short loc_B125B2
00B12598  mov     edx, [esi]
00B1259A  mov     eax, [edx+64h]
00B1259D  push    1
00B1259F  push    0E5h
00B125A4  call    eax
```
