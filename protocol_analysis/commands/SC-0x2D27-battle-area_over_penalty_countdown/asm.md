# 汇编证据 —— SC-0x2D27-battle-area_over_penalty_countdown

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xA` @ `0xB1333A`）

```asm
; VA: 0xB1331E .. （块入口，含守卫与容量申请）
00B1331E  push    12Eh
00B13323  mov     ecx, esi
00B13325  call    sub_B05DA0
00B1332A  test    al, al
00B1332C  jz      loc_B317C7
00B13332  mov     ecx, [esi+0Ch]
00B13335  mov     edx, [ecx]
00B13337  mov     eax, [edx+78h]
00B1333A  push    0Ah
00B1333C  call    eax
00B1333E  mov     ecx, [esi+0Ch]
00B13341  push    ecx
00B13342  lea     ecx, [esp+1B40h+var_1940]
00B13349  mov     [esp+1B40h+var_1B2C], eax
```

## E2 字段 1：`ent_id`（u16，偏移 0，长度 2）

```asm
; VA: 0x0xB13375 附近（实体 ID）
00B1336B  mov     ecx, [esp+1B3Ch+var_1B0C]
00B1336F  lea     eax, [esp+1B3Ch+var_1B28]
00B13373  push    eax
00B13374  push    ecx
00B13375  call    sub_B02DF0
00B1337A  add     esp, 8
00B1337D  test    al, al
00B1337F  jnz     short loc_B1339D
00B13381  mov     edx, [esi]
00B13383  mov     eax, [edx+64h]
```

## E3 字段 2：`limit_msec`（u32，偏移 2，长度 4）

```asm
; VA: 0x0xB133B5 附近（区域脱离惩罚时限（毫秒））
00B133AB  mov     eax, [esp+1B3Ch+var_1B18]
00B133AF  lea     edx, [esp+1B3Ch+var_1B28]
00B133B3  push    edx
00B133B4  push    eax
00B133B5  call    sub_B02DD0
00B133BA  add     esp, 8
00B133BD  test    al, al
00B133BF  jz      short loc_B13381
00B133C1  lea     ecx, [esp+1B3Ch+var_1B2C]
00B133C5  push    ecx
```

## E4 字段 3：`elapsed_msec`（u32，偏移 6，长度 4）

```asm
; VA: 0x0xB133D9 附近（已耗时（毫秒））
00B133CF  mov     eax, [esp+1B3Ch+var_1B20]
00B133D3  lea     edx, [esp+1B3Ch+var_1B28]
00B133D7  push    edx
00B133D8  push    eax
00B133D9  call    sub_B02DD0
00B133DE  add     esp, 8
00B133E1  test    al, al
00B133E3  jz      short loc_B13381
00B133E5  mov     ebx, [esp+1B3Ch+var_1B28]
00B133E9  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB133E9
00B133D8  push    eax
00B133D9  call    sub_B02DD0
00B133DE  add     esp, 8
00B133E1  test    al, al
00B133E3  jz      short loc_B13381
00B133E5  mov     ebx, [esp+1B3Ch+var_1B28]
00B133E9  cmp     ebx, [esp+1B3Ch+var_1B24]
00B133ED  mov     ecx, esi
00B133EF  jz      short loc_B1340B
00B133F1  mov     edx, [esi]
00B133F3  mov     eax, [edx+64h]
00B133F6  push    1
00B133F8  push    12Eh
00B133FD  call    eax
```
