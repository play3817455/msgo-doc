# 汇编证据 —— SC-0x19B2-lounge-player_navi_exchange_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xB5674F`）

```asm
; VA: 0xB5673A .. （块入口，含守卫与容量申请）
00B5673A  call    sub_B41120
00B5673F  test    al, al
00B56741  jz      loc_B890FE
00B56747  mov     ecx, [esi+0Ch]
00B5674A  mov     eax, [ecx]
00B5674C  mov     edx, [eax+78h]
00B5674F  push    14h
00B56751  call    edx
00B56753  mov     [esp+2C5Ch+var_2C48], eax
00B56757  mov     eax, [esi+0Ch]
00B5675A  push    eax
00B5675B  lea     ecx, [esp+2C60h+var_29C4]
00B56762  call    sub_ABB2F0
00B56767  lea     ecx, [esp+2C5Ch+var_2C48]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5678A 附近（交换结果码）
00B56780  mov     eax, [esp+2C5Ch+var_2C30]
00B56784  lea     edx, [esp+2C5Ch+var_2C44]
00B56788  push    edx
00B56789  push    eax
00B5678A  call    sub_B02DD0
00B5678F  add     esp, 8
00B56792  test    al, al
00B56794  jnz     short loc_B567B2
00B56796  mov     edx, [esi]
00B56798  mov     eax, [edx+64h]
```

## E3 字段 2：`old_navi`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB567CA 附近（交换前导航员（navi）唯一 ID）
00B567C0  mov     eax, [esp+2C5Ch+var_2C34]
00B567C4  lea     edx, [esp+2C5Ch+var_2C44]
00B567C8  push    edx
00B567C9  push    eax
00B567CA  call    sub_B434B0
00B567CF  add     esp, 8
00B567D2  test    al, al
00B567D4  jz      short loc_B56796
00B567D6  lea     ecx, [esp+2C5Ch+var_2C48]
00B567DA  push    ecx
```

## E4 字段 3：`new_navi`（u64，偏移 12，长度 8）

```asm
; VA: 0x0xB567EE 附近（交换后导航员唯一 ID）
00B567E4  mov     eax, [esp+2C5Ch+var_2C38]
00B567E8  lea     edx, [esp+2C5Ch+var_2C44]
00B567EC  push    edx
00B567ED  push    eax
00B567EE  call    sub_B434B0
00B567F3  add     esp, 8
00B567F6  test    al, al
00B567F8  jz      short loc_B56796
00B567FA  mov     ebx, [esp+2C5Ch+var_2C44]
00B567FE  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB567FE
00B567ED  push    eax
00B567EE  call    sub_B434B0
00B567F3  add     esp, 8
00B567F6  test    al, al
00B567F8  jz      short loc_B56796
00B567FA  mov     ebx, [esp+2C5Ch+var_2C44]
00B567FE  cmp     ebx, [esp+2C5Ch+var_2C40]
00B56802  mov     ecx, esi
00B56804  jz      short loc_B56820
00B56806  mov     edx, [esi]
00B56808  mov     eax, [edx+64h]
00B5680B  push    1
00B5680D  push    24Bh
00B56812  call    eax
```
