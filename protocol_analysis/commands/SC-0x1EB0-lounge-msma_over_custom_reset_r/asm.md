# 汇编证据 —— SC-0x1EB0-lounge-msma_over_custom_reset_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB57DB6`）

```asm
; VA: 0xB57DA1 .. （块入口，含守卫与容量申请）
00B57DA1  call    sub_B41120
00B57DA6  test    al, al
00B57DA8  jz      loc_B890FE
00B57DAE  mov     ecx, [esi+0Ch]
00B57DB1  mov     eax, [ecx]
00B57DB3  mov     edx, [eax+78h]
00B57DB6  push    0Ch
00B57DB8  call    edx
00B57DBA  mov     [esp+2C5Ch+var_2C3C], eax
00B57DBE  mov     eax, [esi+0Ch]
00B57DC1  push    eax
00B57DC2  lea     ecx, [esp+2C60h+var_27DC]
00B57DC9  call    sub_ABB2F0
00B57DCE  lea     ecx, [esp+2C5Ch+var_2C3C]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB57DF1 附近（改造重置结果码）
00B57DE7  mov     eax, [esp+2C5Ch+var_2C48]
00B57DEB  lea     edx, [esp+2C5Ch+var_2C44]
00B57DEF  push    edx
00B57DF0  push    eax
00B57DF1  call    sub_B02DD0
00B57DF6  add     esp, 8
00B57DF9  test    al, al
00B57DFB  jnz     short loc_B57E19
00B57DFD  mov     edx, [esi]
00B57DFF  mov     eax, [edx+64h]
```

## E3 字段 2：`uniq_msid`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB57E31 附近（机体唯一 ID）
00B57E27  mov     ebx, [esp+2C5Ch+var_2C20]
00B57E2B  lea     edx, [esp+2C5Ch+var_2C44]
00B57E2F  push    edx
00B57E30  push    ebx
00B57E31  call    sub_B06200
00B57E36  add     esp, 8
00B57E39  test    al, al
00B57E3B  mov     ecx, esi
00B57E3D  jnz     short loc_B57E59
00B57E3F  mov     eax, [esi]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB57E5D
00B57E44  push    1
00B57E46  push    264h
00B57E4B  call    edx
00B57E4D  lea     ecx, [esp+2C5Ch+var_27DC]
00B57E54  jmp     loc_B890EE
00B57E59  mov     eax, [esp+2C5Ch+var_2C44]
00B57E5D  cmp     eax, [esp+2C5Ch+var_2C40]
00B57E61  jz      short loc_B57E7D
00B57E63  mov     edx, [esi]
00B57E65  mov     eax, [edx+64h]
00B57E68  push    1
00B57E6A  push    264h
00B57E6F  call    eax
00B57E71  lea     ecx, [esp+2C5Ch+var_27DC]
```
