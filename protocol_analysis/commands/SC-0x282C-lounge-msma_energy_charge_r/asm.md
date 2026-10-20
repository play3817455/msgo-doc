# 汇编证据 —— SC-0x282C-lounge-msma_energy_charge_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB59787`）

```asm
; VA: 0xB5976B .. （块入口，含守卫与容量申请）
00B5976B  push    0F5h
00B59770  mov     ecx, esi
00B59772  call    sub_B41120
00B59777  test    al, al
00B59779  jz      loc_B890FE
00B5977F  mov     ecx, [esi+0Ch]
00B59782  mov     eax, [ecx]
00B59784  mov     edx, [eax+78h]
00B59787  push    4
00B59789  call    edx
00B5978B  mov     [esp+2C5Ch+var_2C3C], eax
00B5978F  mov     eax, [esi+0Ch]
00B59792  push    eax
00B59793  lea     ecx, [esp+2C60h+var_2768]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB597C2 附近（机体能量充能结果码）
00B597B8  mov     eax, [esp+2C5Ch+var_2C48]
00B597BC  lea     edx, [esp+2C5Ch+var_2C44]
00B597C0  push    edx
00B597C1  push    eax
00B597C2  call    sub_B02DD0
00B597C7  add     esp, 8
00B597CA  test    al, al
00B597CC  mov     ecx, esi
00B597CE  jnz     short loc_B597EA
00B597D0  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB597EE
00B597D5  push    1
00B597D7  push    0F5h
00B597DC  call    eax
00B597DE  lea     ecx, [esp+2C5Ch+var_2768]
00B597E5  jmp     loc_B890EE
00B597EA  mov     ebx, [esp+2C5Ch+var_2C44]
00B597EE  cmp     ebx, [esp+2C5Ch+var_2C40]
00B597F2  jnz     short loc_B597D0
00B597F4  push    0F5h
00B597F9  call    sub_B41110
00B597FE  mov     edi, eax
00B59800  test    edi, edi
00B59802  jz      loc_B598B4
00B59808  lea     ecx, [esp+2C5Ch+var_860]
```
