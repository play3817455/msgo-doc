# 汇编证据 —— SC-0x2467-lounge-shop_buy_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB58E05`）

```asm
; VA: 0xB58DE9 .. （块入口，含守卫与容量申请）
00B58DE9  push    17Ch
00B58DEE  mov     ecx, esi
00B58DF0  call    sub_B41120
00B58DF5  test    al, al
00B58DF7  jz      loc_B890FE
00B58DFD  mov     ecx, [esi+0Ch]
00B58E00  mov     eax, [ecx]
00B58E02  mov     edx, [eax+78h]
00B58E05  push    4
00B58E07  call    edx
00B58E09  mov     [esp+2C5Ch+var_2C3C], eax
00B58E0D  mov     eax, [esi+0Ch]
00B58E10  push    eax
00B58E11  lea     ecx, [esp+2C60h+var_26E8]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB58E40 附近（商店购买结果码）
00B58E36  mov     eax, [esp+2C5Ch+var_2C48]
00B58E3A  lea     edx, [esp+2C5Ch+var_2C44]
00B58E3E  push    edx
00B58E3F  push    eax
00B58E40  call    sub_B02DD0
00B58E45  add     esp, 8
00B58E48  test    al, al
00B58E4A  mov     ecx, esi
00B58E4C  jnz     short loc_B58E68
00B58E4E  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB58E6C
00B58E53  push    1
00B58E55  push    17Ch
00B58E5A  call    eax
00B58E5C  lea     ecx, [esp+2C5Ch+var_26E8]
00B58E63  jmp     loc_B890EE
00B58E68  mov     ebx, [esp+2C5Ch+var_2C44]
00B58E6C  cmp     ebx, [esp+2C5Ch+var_2C40]
00B58E70  jnz     short loc_B58E4E
00B58E72  push    17Ch
00B58E77  call    sub_B41110
00B58E7C  mov     edi, eax
00B58E7E  test    edi, edi
00B58E80  jz      loc_B58F32
00B58E86  lea     ecx, [esp+2C5Ch+var_2188]
```
