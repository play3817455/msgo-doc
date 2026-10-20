# 汇编证据 —— SC-0x27F3-battle-room_kick_vote_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB12E02`）

```asm
; VA: 0xB12DE9 .. （块入口，含守卫与容量申请）
00B12DE9  push    2Fh ; '/'
00B12DEB  mov     ecx, esi
00B12DED  call    sub_B05DA0
00B12DF2  test    al, al
00B12DF4  jz      loc_B317C7
00B12DFA  mov     ecx, [esi+0Ch]
00B12DFD  mov     eax, [ecx]
00B12DFF  mov     edx, [eax+78h]
00B12E02  push    4
00B12E04  call    edx
00B12E06  mov     [esp+1B3Ch+var_1B14], eax
00B12E0A  mov     eax, [esi+0Ch]
00B12E0D  push    eax
00B12E0E  lea     ecx, [esp+1B40h+var_180C]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB12E3D 附近（房间踢人投票结果码）
00B12E33  mov     eax, [esp+1B3Ch+var_1B2C]
00B12E37  lea     edx, [esp+1B3Ch+var_1B28]
00B12E3B  push    edx
00B12E3C  push    eax
00B12E3D  call    sub_B02DD0
00B12E42  add     esp, 8
00B12E45  test    al, al
00B12E47  mov     ecx, esi
00B12E49  jnz     short loc_B12E62
00B12E4B  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12E66
00B12E50  push    1
00B12E52  push    2Fh ; '/'
00B12E54  call    eax
00B12E56  lea     ecx, [esp+1B3Ch+var_180C]
00B12E5D  jmp     loc_B317B7
00B12E62  mov     ebx, [esp+1B3Ch+var_1B28]
00B12E66  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12E6A  jnz     short loc_B12E4B
00B12E6C  push    2Fh ; '/'
00B12E6E  call    sub_B05D90
00B12E73  mov     edi, eax
00B12E75  test    edi, edi
00B12E77  jz      loc_B12F29
00B12E7D  lea     ecx, [esp+1B3Ch+var_278]
```
