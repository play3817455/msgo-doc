# 汇编证据 —— SC-0x1908-lounge-msma_missionunit_store_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB56987`）

```asm
; VA: 0xB5696B .. （块入口，含守卫与容量申请）
00B5696B  push    13Ah
00B56970  mov     ecx, esi
00B56972  call    sub_B41120
00B56977  test    al, al
00B56979  jz      loc_B890FE
00B5697F  mov     ecx, [esi+0Ch]
00B56982  mov     eax, [ecx]
00B56984  mov     edx, [eax+78h]
00B56987  push    10h
00B56989  call    edx
00B5698B  mov     [esp+2C5Ch+var_2C3C], eax
00B5698F  mov     eax, [esi+0Ch]
00B56992  push    eax
00B56993  lea     ecx, [esp+2C60h+var_27E4]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB569C2 附近（处理结果码）
00B569B8  mov     eax, [esp+2C5Ch+var_2C38]
00B569BC  lea     edx, [esp+2C5Ch+var_2C44]
00B569C0  push    edx
00B569C1  push    eax
00B569C2  call    sub_B02DD0
00B569C7  add     esp, 8
00B569CA  test    al, al
00B569CC  jnz     short loc_B569EA
00B569CE  mov     edx, [esi]
00B569D0  mov     eax, [edx+64h]
```

## E3 字段 2：`missionunit_set`（struct{12}，偏移 4，长度 12）

```asm
; VA: 0x0xB56A02 附近（任务编成单元（机体）数据块）
00B569F8  mov     eax, [esp+2C5Ch+var_2C48]
00B569FC  lea     edx, [esp+2C5Ch+var_2C44]
00B56A00  push    edx
00B56A01  push    eax
00B56A02  call    sub_B43BE0
00B56A07  add     esp, 8
00B56A0A  test    al, al
00B56A0C  jz      short loc_B569CE
00B56A0E  mov     ebx, [esp+2C5Ch+var_2C44]
00B56A12  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E4 字段 3：`missionunit_set.deck_type`（u16，偏移 +0，长度 2）

```asm
; VA: 0x0xB43BEE 附近（编成卡组类型）
00B5696B  push    13Ah
00B56970  mov     ecx, esi
00B56972  call    sub_B41120
00B56977  test    al, al
00B56979  jz      loc_B890FE
00B5697F  mov     ecx, [esi+0Ch]
```

## E5 字段 4：`missionunit_set.deck_set`（u16，偏移 +2，长度 2）

```asm
; VA: 0x0xB43C06 附近（编成卡组套编号）
00B5696B  push    13Ah
00B56970  mov     ecx, esi
00B56972  call    sub_B41120
00B56977  test    al, al
00B56979  jz      loc_B890FE
00B5697F  mov     ecx, [esi+0Ch]
```

## E6 字段 5：`missionunit_set.missionunit_id`（u64，偏移 +4，长度 8）

```asm
; VA: 0x0xB43C20 附近（任务单元 ID（打印器成对打印低/高 32 位））
00B5696B  push    13Ah
00B56970  mov     ecx, esi
00B56972  call    sub_B41120
00B56977  test    al, al
00B56979  jz      loc_B890FE
00B5697F  mov     ecx, [esi+0Ch]
```

## E7 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB56A12
00B56A01  push    eax
00B56A02  call    sub_B43BE0
00B56A07  add     esp, 8
00B56A0A  test    al, al
00B56A0C  jz      short loc_B569CE
00B56A0E  mov     ebx, [esp+2C5Ch+var_2C44]
00B56A12  cmp     ebx, [esp+2C5Ch+var_2C40]
00B56A16  mov     ecx, esi
00B56A18  jz      short loc_B56A34
00B56A1A  mov     edx, [esi]
00B56A1C  mov     eax, [edx+64h]
00B56A1F  push    1
00B56A21  push    13Ah
00B56A26  call    eax
```
