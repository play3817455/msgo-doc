# 汇编证据 —— SC-0x24CF-lounge-gacha_enter_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB592B1`）

```asm
; VA: 0xB59295 .. （块入口，含守卫与容量申请）
00B59295  push    189h
00B5929A  mov     ecx, esi
00B5929C  call    sub_B41120
00B592A1  test    al, al
00B592A3  jz      loc_B890FE
00B592A9  mov     ecx, [esi+0Ch]
00B592AC  mov     edx, [ecx]
00B592AE  mov     eax, [edx+78h]
00B592B1  push    4
00B592B3  call    eax
00B592B5  mov     ecx, [esi+0Ch]
00B592B8  push    ecx
00B592B9  lea     ecx, [esp+2C60h+var_267C]
00B592C0  mov     [esp+2C60h+var_2C3C], eax
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB592EC 附近（扭蛋（gacha）入场结果码）
00B592E2  mov     ecx, [esp+2C5Ch+var_2C48]
00B592E6  lea     eax, [esp+2C5Ch+var_2C44]
00B592EA  push    eax
00B592EB  push    ecx
00B592EC  call    sub_B02DD0
00B592F1  add     esp, 8
00B592F4  test    al, al
00B592F6  mov     ecx, esi
00B592F8  jnz     short loc_B59314
00B592FA  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB59318
00B592FF  push    1
00B59301  push    189h
00B59306  call    eax
00B59308  lea     ecx, [esp+2C5Ch+var_267C]
00B5930F  jmp     loc_B890EE
00B59314  mov     ebx, [esp+2C5Ch+var_2C44]
00B59318  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5931C  jnz     short loc_B592FA
00B5931E  push    189h
00B59323  call    sub_B41110
00B59328  mov     edi, eax
00B5932A  test    edi, edi
00B5932C  jz      loc_B593DE
00B59332  lea     ecx, [esp+2C5Ch+var_2150]
```
