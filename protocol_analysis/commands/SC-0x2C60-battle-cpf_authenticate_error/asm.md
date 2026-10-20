# 汇编证据 —— SC-0x2C60-battle-cpf_authenticate_error

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB12F88`）

```asm
; VA: 0xB12F73 .. （块入口，含守卫与容量申请）
00B12F73  call    sub_B05DA0
00B12F78  test    al, al
00B12F7A  jz      loc_B317C7
00B12F80  mov     ecx, [esi+0Ch]
00B12F83  mov     eax, [ecx]
00B12F85  mov     edx, [eax+78h]
00B12F88  push    4
00B12F8A  call    edx
00B12F8C  mov     [esp+1B3Ch+var_1B14], eax
00B12F90  mov     eax, [esi+0Ch]
00B12F93  push    eax
00B12F94  lea     ecx, [esp+1B40h+var_17AC]
00B12F9B  call    sub_ABB2F0
00B12FA0  lea     ecx, [esp+1B3Ch+var_1B14]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB12FC3 附近（CPF 认证错误码）
00B12FB9  mov     eax, [esp+1B3Ch+var_1B2C]
00B12FBD  lea     edx, [esp+1B3Ch+var_1B28]
00B12FC1  push    edx
00B12FC2  push    eax
00B12FC3  call    sub_B02DD0
00B12FC8  add     esp, 8
00B12FCB  test    al, al
00B12FCD  mov     ecx, esi
00B12FCF  jnz     short loc_B12FEB
00B12FD1  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12FEF
00B12FD6  push    1
00B12FD8  push    11Dh
00B12FDD  call    eax
00B12FDF  lea     ecx, [esp+1B3Ch+var_17AC]
00B12FE6  jmp     loc_B317B7
00B12FEB  mov     ebx, [esp+1B3Ch+var_1B28]
00B12FEF  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12FF3  jnz     short loc_B12FD1
00B12FF5  push    11Dh
00B12FFA  call    sub_B05D90
00B12FFF  mov     edi, eax
00B13001  test    edi, edi
00B13003  jz      loc_B130B5
00B13009  lea     ecx, [esp+1B3Ch+var_1270]
```
