# 汇编证据 —— SC-0x19FD-lounge-mission_info_unlock_coop

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x4` @ `0xB56B69`）

```asm
; VA: 0xB56B50 .. （块入口，含守卫与容量申请）
00B56B50  push    5Fh ; '_'
00B56B52  mov     ecx, esi
00B56B54  call    sub_B41120
00B56B59  test    al, al
00B56B5B  jz      loc_B890FE
00B56B61  mov     ecx, [esi+0Ch]
00B56B64  mov     eax, [ecx]
00B56B66  mov     edx, [eax+78h]
00B56B69  push    4
00B56B6B  call    edx
00B56B6D  mov     [esp+2C5Ch+var_2C3C], eax
00B56B71  mov     eax, [esi+0Ch]
00B56B74  push    eax
00B56B75  lea     ecx, [esp+2C60h+var_268C]
```

## E2 字段 1：`mission_id`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB56BA4 附近（解锁的合作（coop）任务 ID）
00B56B9A  mov     eax, [esp+2C5Ch+var_2C48]
00B56B9E  lea     edx, [esp+2C5Ch+var_2C44]
00B56BA2  push    edx
00B56BA3  push    eax
00B56BA4  call    sub_B02DD0
00B56BA9  add     esp, 8
00B56BAC  test    al, al
00B56BAE  mov     ecx, esi
00B56BB0  jnz     short loc_B56BC9
00B56BB2  mov     edx, [esi]
```

## E3 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB56BCD
00B56BB7  push    1
00B56BB9  push    5Fh ; '_'
00B56BBB  call    eax
00B56BBD  lea     ecx, [esp+2C5Ch+var_268C]
00B56BC4  jmp     loc_B890EE
00B56BC9  mov     ebx, [esp+2C5Ch+var_2C44]
00B56BCD  cmp     ebx, [esp+2C5Ch+var_2C40]
00B56BD1  jnz     short loc_B56BB2
00B56BD3  push    5Fh ; '_'
00B56BD5  call    sub_B41110
00B56BDA  mov     edi, eax
00B56BDC  test    edi, edi
00B56BDE  jz      loc_B56C90
00B56BE4  lea     ecx, [esp+2C5Ch+var_1190]
```
