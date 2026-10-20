# 汇编证据 —— SC-0x2064-lounge-msma_equip_weapon_exchange_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB586D9`）

```asm
; VA: 0xB586BD .. （块入口，含守卫与容量申请）
00B586BD  push    0D7h
00B586C2  mov     ecx, esi
00B586C4  call    sub_B41120
00B586C9  test    al, al
00B586CB  jz      loc_B890FE
00B586D1  mov     ecx, [esi+0Ch]
00B586D4  mov     eax, [ecx]
00B586D6  mov     edx, [eax+78h]
00B586D9  push    10h
00B586DB  call    edx
00B586DD  mov     [esp+2C5Ch+var_2C24], eax
00B586E1  mov     eax, [esi+0Ch]
00B586E4  push    eax
00B586E5  lea     ecx, [esp+2C60h+var_2AB4]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB58714 附近（装备武器交换结果码）
00B5870A  mov     eax, [esp+2C5Ch+var_2C30]
00B5870E  lea     edx, [esp+2C5Ch+var_2C44]
00B58712  push    edx
00B58713  push    eax
00B58714  call    sub_B02DD0
00B58719  add     esp, 8
00B5871C  test    al, al
00B5871E  jnz     short loc_B5873C
00B58720  mov     edx, [esi]
00B58722  mov     eax, [edx+64h]
```

## E3 字段 2：`uniqid_ms`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB58754 附近（机体唯一 ID）
00B5874A  mov     eax, [esp+2C5Ch+var_2C34]
00B5874E  lea     edx, [esp+2C5Ch+var_2C44]
00B58752  push    edx
00B58753  push    eax
00B58754  call    sub_B06200
00B58759  add     esp, 8
00B5875C  test    al, al
00B5875E  jz      short loc_B58720
00B58760  lea     ecx, [esp+2C5Ch+var_2C24]
00B58764  push    ecx
```

## E4 字段 3：`eq_slot1`（u16，偏移 12，长度 2）

```asm
; VA: 0x0xB58778 附近（装备槽 1）
00B5876E  mov     eax, [esp+2C5Ch+var_2C38]
00B58772  lea     edx, [esp+2C5Ch+var_2C44]
00B58776  push    edx
00B58777  push    eax
00B58778  call    sub_B02DF0
00B5877D  add     esp, 8
00B58780  test    al, al
00B58782  jz      short loc_B58720
00B58784  lea     ecx, [esp+2C5Ch+var_2C24]
00B58788  push    ecx
```

## E5 字段 4：`eq_slot2`（u16，偏移 14，长度 2）

```asm
; VA: 0x0xB5879C 附近（装备槽 2）
00B58792  mov     eax, [esp+2C5Ch+var_2C48]
00B58796  lea     edx, [esp+2C5Ch+var_2C44]
00B5879A  push    edx
00B5879B  push    eax
00B5879C  call    sub_B02DF0
00B587A1  add     esp, 8
00B587A4  test    al, al
00B587A6  jz      loc_B58720
00B587AC  mov     ebx, [esp+2C5Ch+var_2C44]
00B587B0  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB587B0
00B5879B  push    eax
00B5879C  call    sub_B02DF0
00B587A1  add     esp, 8
00B587A4  test    al, al
00B587A6  jz      loc_B58720
00B587AC  mov     ebx, [esp+2C5Ch+var_2C44]
00B587B0  cmp     ebx, [esp+2C5Ch+var_2C40]
00B587B4  mov     ecx, esi
00B587B6  jz      short loc_B587D2
00B587B8  mov     edx, [esi]
00B587BA  mov     eax, [edx+64h]
00B587BD  push    1
00B587BF  push    0D7h
00B587C4  call    eax
```
