# 汇编证据 —— SC-0x1EC7-battle-battleship_get_down_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x6` @ `0xB122BA`）

```asm
; VA: 0xB1229E .. （块入口，含守卫与容量申请）
00B1229E  push    0FFh
00B122A3  mov     ecx, esi
00B122A5  call    sub_B05DA0
00B122AA  test    al, al
00B122AC  jz      loc_B317C7
00B122B2  mov     ecx, [esi+0Ch]
00B122B5  mov     eax, [ecx]
00B122B7  mov     edx, [eax+78h]
00B122BA  push    6
00B122BC  call    edx
00B122BE  mov     [esp+1B3Ch+var_1B14], eax
00B122C2  mov     eax, [esi+0Ch]
00B122C5  push    eax
00B122C6  lea     ecx, [esp+1B40h+var_1848]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB122F5 附近（战舰下舰结果码）
00B122EB  mov     eax, [esp+1B3Ch+var_1B20]
00B122EF  lea     edx, [esp+1B3Ch+var_1B28]
00B122F3  push    edx
00B122F4  push    eax
00B122F5  call    sub_B02DD0
00B122FA  add     esp, 8
00B122FD  test    al, al
00B122FF  jnz     short loc_B1231D
00B12301  mov     edx, [esi]
00B12303  mov     eax, [edx+64h]
```

## E3 字段 2：`to_ent_id`（u16，偏移 4，长度 2）

```asm
; VA: 0x0xB12335 附近（目标实体 ID）
00B1232B  mov     eax, [esp+1B3Ch+var_1B2C]
00B1232F  lea     edx, [esp+1B3Ch+var_1B28]
00B12333  push    edx
00B12334  push    eax
00B12335  call    sub_B02DF0
00B1233A  add     esp, 8
00B1233D  test    al, al
00B1233F  jz      short loc_B12301
00B12341  mov     ebx, [esp+1B3Ch+var_1B28]
00B12345  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB12345
00B12334  push    eax
00B12335  call    sub_B02DF0
00B1233A  add     esp, 8
00B1233D  test    al, al
00B1233F  jz      short loc_B12301
00B12341  mov     ebx, [esp+1B3Ch+var_1B28]
00B12345  cmp     ebx, [esp+1B3Ch+var_1B24]
00B12349  mov     ecx, esi
00B1234B  jz      short loc_B12367
00B1234D  mov     edx, [esi]
00B1234F  mov     eax, [edx+64h]
00B12352  push    1
00B12354  push    0FFh
00B12359  call    eax
```
