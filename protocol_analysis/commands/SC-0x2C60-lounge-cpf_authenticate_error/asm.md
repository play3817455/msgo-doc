# 汇编证据 —— SC-0x2C60-lounge-cpf_authenticate_error

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB5A3F7`）

```asm
; VA: 0xB5A3E2 .. （块入口，含守卫与容量申请）
00B5A3E2  call    sub_B41120
00B5A3E7  test    al, al
00B5A3E9  jz      loc_B890FE
00B5A3EF  mov     ecx, [esi+0Ch]
00B5A3F2  mov     edx, [ecx]
00B5A3F4  mov     eax, [edx+78h]
00B5A3F7  push    4
00B5A3F9  call    eax
00B5A3FB  mov     ecx, [esi+0Ch]
00B5A3FE  push    ecx
00B5A3FF  lea     ecx, [esp+2C60h+var_26E0]
00B5A406  mov     [esp+2C60h+var_2C3C], eax
00B5A40A  call    sub_ABB2F0
00B5A40F  lea     edx, [esp+2C5Ch+var_2C3C]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5A432 附近（CPF 认证错误码）
00B5A428  mov     ecx, [esp+2C5Ch+var_2C48]
00B5A42C  lea     eax, [esp+2C5Ch+var_2C44]
00B5A430  push    eax
00B5A431  push    ecx
00B5A432  call    sub_B02DD0
00B5A437  add     esp, 8
00B5A43A  test    al, al
00B5A43C  mov     ecx, esi
00B5A43E  jnz     short loc_B5A45A
00B5A440  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5A45E
00B5A445  push    1
00B5A447  push    214h
00B5A44C  call    eax
00B5A44E  lea     ecx, [esp+2C5Ch+var_26E0]
00B5A455  jmp     loc_B890EE
00B5A45A  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A45E  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5A462  jnz     short loc_B5A440
00B5A464  push    214h
00B5A469  call    sub_B41110
00B5A46E  mov     edi, eax
00B5A470  test    edi, edi
00B5A472  jz      loc_B5A524
00B5A478  lea     ecx, [esp+2C5Ch+var_2070]
```
