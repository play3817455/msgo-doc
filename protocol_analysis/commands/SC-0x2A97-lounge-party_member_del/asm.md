# 汇编证据 —— SC-0x2A97-lounge-party_member_del

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x5` @ `0xB598FD`）

```asm
; VA: 0xB598E1 .. （块入口，含守卫与容量申请）
00B598E1  push    0BBh
00B598E6  mov     ecx, esi
00B598E8  call    sub_B41120
00B598ED  test    al, al
00B598EF  jz      loc_B890FE
00B598F5  mov     ecx, [esi+0Ch]
00B598F8  mov     eax, [ecx]
00B598FA  mov     edx, [eax+78h]
00B598FD  push    5
00B598FF  call    edx
00B59901  mov     [esp+2C5Ch+var_2C3C], eax
00B59905  mov     eax, [esi+0Ch]
00B59908  push    eax
00B59909  lea     ecx, [esp+2C60h+var_27B4]
```

## E2 字段 1：`pilot_id`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB59938 附近（被移除的驾驶员 ID）
00B5992E  mov     eax, [esp+2C5Ch+var_2C38]
00B59932  lea     edx, [esp+2C5Ch+var_2C44]
00B59936  push    edx
00B59937  push    eax
00B59938  call    sub_B02DD0
00B5993D  add     esp, 8
00B59940  test    al, al
00B59942  jnz     short loc_B59960
00B59944  mov     edx, [esi]
00B59946  mov     eax, [edx+64h]
```

## E3 字段 2：`is_kick`（u8，偏移 4，长度 1）

```asm
; VA: 0x0xB59978 附近（是否被踢出（而非主动退出））
00B5996E  mov     eax, [esp+2C5Ch+var_2C48]
00B59972  lea     edx, [esp+2C5Ch+var_2C44]
00B59976  push    edx
00B59977  push    eax
00B59978  call    sub_B06230
00B5997D  add     esp, 8
00B59980  test    al, al
00B59982  jz      short loc_B59944
00B59984  mov     ebx, [esp+2C5Ch+var_2C44]
00B59988  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB59988
00B59977  push    eax
00B59978  call    sub_B06230
00B5997D  add     esp, 8
00B59980  test    al, al
00B59982  jz      short loc_B59944
00B59984  mov     ebx, [esp+2C5Ch+var_2C44]
00B59988  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5998C  mov     ecx, esi
00B5998E  jz      short loc_B599AA
00B59990  mov     edx, [esi]
00B59992  mov     eax, [edx+64h]
00B59995  push    1
00B59997  push    0BBh
00B5999C  call    eax
```
