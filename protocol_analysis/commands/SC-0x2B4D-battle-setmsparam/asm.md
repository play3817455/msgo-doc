# 汇编证据 —— SC-0x2B4D-battle-setmsparam

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB130FE`）

```asm
; VA: 0xB130E2 .. （块入口，含守卫与容量申请）
00B130E2  push    121h
00B130E7  mov     ecx, esi
00B130E9  call    sub_B05DA0
00B130EE  test    al, al
00B130F0  jz      loc_B317C7
00B130F6  mov     ecx, [esi+0Ch]
00B130F9  mov     eax, [ecx]
00B130FB  mov     edx, [eax+78h]
00B130FE  push    0Ch
00B13100  call    edx
00B13102  mov     [esp+1B3Ch+var_1B2C], eax
00B13106  mov     eax, [esi+0Ch]
00B13109  push    eax
00B1310A  lea     ecx, [esp+1B40h+var_18D4]
```

## E2 字段 1：`ent_id`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB13139 附近（实体 ID）
00B1312F  mov     eax, [esp+1B3Ch+var_1B0C]
00B13133  lea     edx, [esp+1B3Ch+var_1B28]
00B13137  push    edx
00B13138  push    eax
00B13139  call    sub_B02DD0
00B1313E  add     esp, 8
00B13141  test    al, al
00B13143  jnz     short loc_B13161
00B13145  mov     edx, [esi]
00B13147  mov     eax, [edx+64h]
```

## E3 字段 2：`val`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB13179 附近（参数值）
00B1316F  mov     eax, [esp+1B3Ch+var_1B18]
00B13173  lea     edx, [esp+1B3Ch+var_1B28]
00B13177  push    edx
00B13178  push    eax
00B13179  call    sub_B02DD0
00B1317E  add     esp, 8
00B13181  test    al, al
00B13183  jz      short loc_B13145
00B13185  lea     ecx, [esp+1B3Ch+var_1B2C]
00B13189  push    ecx
```

## E4 字段 3：`type`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB1319D 附近（参数类型）
00B13193  mov     eax, [esp+1B3Ch+var_1B20]
00B13197  lea     edx, [esp+1B3Ch+var_1B28]
00B1319B  push    edx
00B1319C  push    eax
00B1319D  call    sub_B02DD0
00B131A2  add     esp, 8
00B131A5  test    al, al
00B131A7  jz      short loc_B13145
00B131A9  mov     ebx, [esp+1B3Ch+var_1B28]
00B131AD  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB131AD
00B1319C  push    eax
00B1319D  call    sub_B02DD0
00B131A2  add     esp, 8
00B131A5  test    al, al
00B131A7  jz      short loc_B13145
00B131A9  mov     ebx, [esp+1B3Ch+var_1B28]
00B131AD  cmp     ebx, [esp+1B3Ch+var_1B24]
00B131B1  mov     ecx, esi
00B131B3  jz      short loc_B131CF
00B131B5  mov     edx, [esi]
00B131B7  mov     eax, [edx+64h]
00B131BA  push    1
00B131BC  push    121h
00B131C1  call    eax
```
