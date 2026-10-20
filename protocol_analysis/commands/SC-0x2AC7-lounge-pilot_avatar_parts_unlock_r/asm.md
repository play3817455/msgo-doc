# 汇编证据 —— SC-0x2AC7-lounge-pilot_avatar_parts_unlock_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x508` @ `0xB59B07`）

```asm
; VA: 0xB59AF2 .. （块入口，含守卫与容量申请）
00B59AF2  call    sub_B41120
00B59AF7  test    al, al
00B59AF9  jz      loc_B890FE
00B59AFF  mov     ecx, [esi+0Ch]
00B59B02  mov     edx, [ecx]
00B59B04  mov     eax, [edx+78h]
00B59B07  push    508h
00B59B0C  call    eax
00B59B0E  mov     ecx, [esi+0Ch]
00B59B11  push    ecx
00B59B12  lea     ecx, [esp+2C60h+var_27AC]
00B59B19  mov     [esp+2C60h+var_2C48], eax
00B59B1D  call    sub_ABB2F0
00B59B22  lea     edx, [esp+2C5Ch+var_2C48]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB59B45 附近（头像部件解锁结果码）
00B59B3B  mov     ecx, [esp+2C5Ch+var_2C34]
00B59B3F  lea     eax, [esp+2C5Ch+var_2C44]
00B59B43  push    eax
00B59B44  push    ecx
00B59B45  call    sub_B02DD0
00B59B4A  add     esp, 8
00B59B4D  test    al, al
00B59B4F  jnz     short loc_B59B6A
00B59B51  mov     edx, [esi]
00B59B53  mov     eax, [edx+64h]
```

## E3 字段 2：`custom_id`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB59B82 附近（自定义（配色/头像）ID）
00B59B78  mov     eax, [esp+2C5Ch+var_2C38]
00B59B7C  lea     edx, [esp+2C5Ch+var_2C44]
00B59B80  push    edx
00B59B81  push    eax
00B59B82  call    sub_B02DD0
00B59B87  add     esp, 8
00B59B8A  test    al, al
00B59B8C  jz      short loc_B59B51
00B59B8E  lea     ecx, [esp+2C5Ch+var_2C48]
00B59B92  push    ecx
```

## E4 字段 3：`hav_avatar`（u64[160]，偏移 8，长度 1280）

```asm
; VA: 0x0xB59BA8 附近（已拥有头像部件 ID 列表（固定 160 项 u64，无线上计数））
00B59BA0  xor     edi, edi
00B59BA2  lea     edx, [esp+2C5Ch+var_2C44]
00B59BA6  push    edx
00B59BA7  push    ebx
00B59BA8  call    sub_B06200
00B59BAD  add     esp, 8
00B59BB0  test    al, al
00B59BB2  jz      short loc_B59BC4
00B59BB4  add     edi, 1
00B59BB7  add     ebx, 8
```

## E5 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB59BD5
00B59BC6  mov     edx, [eax+64h]
00B59BC9  push    1
00B59BCB  push    2Fh ; '/'
00B59BCD  mov     ecx, esi
00B59BCF  call    edx
00B59BD1  mov     eax, [esp+2C5Ch+var_2C44]
00B59BD5  cmp     eax, [esp+2C5Ch+var_2C40]
00B59BD9  mov     ecx, esi
00B59BDB  jz      short loc_B59BF4
00B59BDD  mov     edx, [esi]
00B59BDF  mov     eax, [edx+64h]
00B59BE2  push    1
00B59BE4  push    2Fh ; '/'
00B59BE6  call    eax
```
