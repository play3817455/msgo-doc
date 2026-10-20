# 汇编证据 —— SC-0x2DA6-lounge-msma_color_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x14` @ `0xB5AA76`）

```asm
; VA: 0xB5AA5A .. （块入口，含守卫与容量申请）
00B5AA5A  push    120h
00B5AA5F  mov     ecx, esi
00B5AA61  call    sub_B41120
00B5AA66  test    al, al
00B5AA68  jz      loc_B890FE
00B5AA6E  mov     ecx, [esi+0Ch]
00B5AA71  mov     edx, [ecx]
00B5AA73  mov     eax, [edx+78h]
00B5AA76  push    14h
00B5AA78  call    eax
00B5AA7A  mov     ecx, [esi+0Ch]
00B5AA7D  push    ecx
00B5AA7E  lea     ecx, [esp+2C60h+var_2A9C]
00B5AA85  mov     [esp+2C60h+var_2C24], eax
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5AAB1 附近（机体配色解锁结果码）
00B5AAA7  mov     ecx, [esp+2C5Ch+var_2C34]
00B5AAAB  lea     eax, [esp+2C5Ch+var_2C44]
00B5AAAF  push    eax
00B5AAB0  push    ecx
00B5AAB1  call    sub_B02DD0
00B5AAB6  add     esp, 8
00B5AAB9  test    al, al
00B5AABB  jnz     short loc_B5AAD9
00B5AABD  mov     edx, [esi]
00B5AABF  mov     eax, [edx+64h]
```

## E3 字段 2：`uniqid_ms`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB5AAF1 附近（机体唯一 ID）
00B5AAE7  mov     ebx, [esp+2C5Ch+var_2C3C]
00B5AAEB  lea     edx, [esp+2C5Ch+var_2C44]
00B5AAEF  push    edx
00B5AAF0  push    ebx
00B5AAF1  call    sub_B06200
00B5AAF6  add     esp, 8
00B5AAF9  test    al, al
00B5AAFB  jnz     short loc_B5AB19
00B5AAFD  mov     eax, [esi]
00B5AAFF  mov     edx, [eax+64h]
```

## E4 字段 3：`color_id`（u32，偏移 12，长度 4）

```asm
; VA: 0x0xB5AB31 附近（本次解锁的配色 ID）
00B5AB27  mov     edx, [esp+2C5Ch+var_2C38]
00B5AB2B  lea     ecx, [esp+2C5Ch+var_2C44]
00B5AB2F  push    ecx
00B5AB30  push    edx
00B5AB31  call    sub_B02DD0
00B5AB36  add     esp, 8
00B5AB39  test    al, al
00B5AB3B  jz      short loc_B5AAFD
00B5AB3D  lea     eax, [esp+2C5Ch+var_2C24]
00B5AB41  push    eax
```

## E5 字段 4：`unlocked_colors`（u32，偏移 16，长度 4）

```asm
; VA: 0x0xB5AB55 附近（已解锁配色位图）
00B5AB4B  mov     edx, [esp+2C5Ch+var_2C48]
00B5AB4F  lea     ecx, [esp+2C5Ch+var_2C44]
00B5AB53  push    ecx
00B5AB54  push    edx
00B5AB55  call    sub_B02DD0
00B5AB5A  add     esp, 8
00B5AB5D  test    al, al
00B5AB5F  jz      short loc_B5AAFD
00B5AB61  mov     eax, [esp+2C5Ch+var_2C44]
00B5AB65  cmp     eax, [esp+2C5Ch+var_2C40]
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5AB65
00B5AB54  push    edx
00B5AB55  call    sub_B02DD0
00B5AB5A  add     esp, 8
00B5AB5D  test    al, al
00B5AB5F  jz      short loc_B5AAFD
00B5AB61  mov     eax, [esp+2C5Ch+var_2C44]
00B5AB65  cmp     eax, [esp+2C5Ch+var_2C40]
00B5AB69  mov     ecx, esi
00B5AB6B  jz      short loc_B5AB87
00B5AB6D  mov     edx, [esi]
00B5AB6F  mov     eax, [edx+64h]
00B5AB72  push    1
00B5AB74  push    120h
00B5AB79  call    eax
```
