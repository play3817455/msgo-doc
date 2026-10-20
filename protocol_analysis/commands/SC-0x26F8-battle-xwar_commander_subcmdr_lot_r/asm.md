# 汇编证据 —— SC-0x26F8-battle-xwar_commander_subcmdr_lot_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1` @ `0xB12A50`）

```asm
; VA: 0xB12A3B .. （块入口，含守卫与容量申请）
00B12A3B  call    sub_B05DA0
00B12A40  test    al, al
00B12A42  jz      loc_B317C7
00B12A48  mov     ecx, [esi+0Ch]
00B12A4B  mov     eax, [ecx]
00B12A4D  mov     edx, [eax+78h]
00B12A50  push    1
00B12A52  call    edx
00B12A54  mov     [esp+1B3Ch+var_1B14], eax
00B12A58  mov     eax, [esi+0Ch]
00B12A5B  push    eax
00B12A5C  lea     ecx, [esp+1B40h+var_1778]
00B12A63  call    sub_ABB2F0
00B12A68  lea     ecx, [esp+1B3Ch+var_1B14]
```

## E2 字段 1：`is_lot`（u8，偏移 0，长度 1）

```asm
; VA: 0x0xB12A8B 附近（副司令抽选是否成立（抽中标志））
00B12A81  mov     eax, [esp+1B3Ch+var_1B2C]
00B12A85  lea     edx, [esp+1B3Ch+var_1B28]
00B12A89  push    edx
00B12A8A  push    eax
00B12A8B  call    sub_B06230
00B12A90  add     esp, 8
00B12A93  test    al, al
00B12A95  mov     ecx, esi
00B12A97  jnz     short loc_B12AB3
00B12A99  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12AB7
00B12A9E  push    1
00B12AA0  push    0ECh
00B12AA5  call    eax
00B12AA7  lea     ecx, [esp+1B3Ch+var_1778]
00B12AAE  jmp     loc_B317B7
00B12AB3  mov     ebx, [esp+1B3Ch+var_1B28]
00B12AB7  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12ABB  jnz     short loc_B12A99
00B12ABD  push    0ECh
00B12AC2  call    sub_B05D90
00B12AC7  mov     edi, eax
00B12AC9  test    edi, edi
00B12ACB  jz      loc_B12B7D
00B12AD1  lea     ecx, [esp+1B3Ch+var_978]
```
