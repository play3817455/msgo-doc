# 汇编证据 —— SC-0x243B-battle-game_btlfield_change

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB128BB`）

```asm
; VA: 0xB128A2 .. （块入口，含守卫与容量申请）
00B128A2  push    33h ; '3'
00B128A4  mov     ecx, esi
00B128A6  call    sub_B05DA0
00B128AB  test    al, al
00B128AD  jz      loc_B317C7
00B128B3  mov     ecx, [esi+0Ch]
00B128B6  mov     eax, [ecx]
00B128B8  mov     edx, [eax+78h]
00B128BB  push    4
00B128BD  call    edx
00B128BF  mov     [esp+1B3Ch+var_1B14], eax
00B128C3  mov     eax, [esi+0Ch]
00B128C6  push    eax
00B128C7  lea     ecx, [esp+1B40h+var_1764]
```

## E2 字段 1：`btlfield`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB128F6 附近（战场（btlfield）ID）
00B128EC  mov     eax, [esp+1B3Ch+var_1B2C]
00B128F0  lea     edx, [esp+1B3Ch+var_1B28]
00B128F4  push    edx
00B128F5  push    eax
00B128F6  call    sub_B02DD0
00B128FB  add     esp, 8
00B128FE  test    al, al
00B12900  mov     ecx, esi
00B12902  jnz     short loc_B1291B
00B12904  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB1291F
00B12909  push    1
00B1290B  push    33h ; '3'
00B1290D  call    eax
00B1290F  lea     ecx, [esp+1B3Ch+var_1764]
00B12916  jmp     loc_B317B7
00B1291B  mov     ebx, [esp+1B3Ch+var_1B28]
00B1291F  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12923  jnz     short loc_B12904
00B12925  push    33h ; '3'
00B12927  call    sub_B05D90
00B1292C  mov     edi, eax
00B1292E  test    edi, edi
00B12930  jz      loc_B129E2
00B12936  lea     ecx, [esp+1B3Ch+var_12E0]
```
