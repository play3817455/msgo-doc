# 汇编证据 —— SC-0x1EA5-battle-entity_msma_reborn

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB11B60`）

```asm
; VA: 0xB11B4B .. （块入口，含守卫与容量申请）
00B11B4B  call    sub_B05DA0
00B11B50  test    al, al
00B11B52  jz      loc_B317C7
00B11B58  mov     ecx, [esi+0Ch]
00B11B5B  mov     edx, [ecx]
00B11B5D  mov     eax, [edx+78h]
00B11B60  push    4
00B11B62  call    eax
00B11B64  mov     ecx, [esi+0Ch]
00B11B67  push    ecx
00B11B68  lea     ecx, [esp+1B40h+var_1828]
00B11B6F  mov     [esp+1B40h+var_1B14], eax
00B11B73  call    sub_ABB2F0
00B11B78  lea     edx, [esp+1B3Ch+var_1B14]
```

## E2 字段 1：`ent_id`（u16，偏移 0，长度 2）

```asm
; VA: 0x0xB11B9B 附近（重生实体 ID）
00B11B91  mov     ecx, [esp+1B3Ch+var_1B20]
00B11B95  lea     eax, [esp+1B3Ch+var_1B28]
00B11B99  push    eax
00B11B9A  push    ecx
00B11B9B  call    sub_B02DF0
00B11BA0  add     esp, 8
00B11BA3  test    al, al
00B11BA5  jnz     short loc_B11BC0
00B11BA7  mov     edx, [esi]
00B11BA9  mov     eax, [edx+64h]
```

## E3 字段 2：`hp_percent`（u16，偏移 2，长度 2）

```asm
; VA: 0x0xB11BD8 附近（重生 HP 百分比）
00B11BCE  mov     eax, [esp+1B3Ch+var_1B2C]
00B11BD2  lea     edx, [esp+1B3Ch+var_1B28]
00B11BD6  push    edx
00B11BD7  push    eax
00B11BD8  call    sub_B02DF0
00B11BDD  add     esp, 8
00B11BE0  test    al, al
00B11BE2  jz      short loc_B11BA7
00B11BE4  mov     ebx, [esp+1B3Ch+var_1B28]
00B11BE8  cmp     ebx, [esp+1B3Ch+var_1B24]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB11BE8
00B11BD7  push    eax
00B11BD8  call    sub_B02DF0
00B11BDD  add     esp, 8
00B11BE0  test    al, al
00B11BE2  jz      short loc_B11BA7
00B11BE4  mov     ebx, [esp+1B3Ch+var_1B28]
00B11BE8  cmp     ebx, [esp+1B3Ch+var_1B24]
00B11BEC  mov     ecx, esi
00B11BEE  jz      short loc_B11C07
00B11BF0  mov     edx, [esi]
00B11BF2  mov     eax, [edx+64h]
00B11BF5  push    1
00B11BF7  push    59h ; 'Y'
00B11BF9  call    eax
```
