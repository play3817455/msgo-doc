# 汇编证据 —— SC-0x20C4-lounge-mail_get_present_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xC` @ `0xB584D4`）

```asm
; VA: 0xB584BF .. （块入口，含守卫与容量申请）
00B584BF  call    sub_B41120
00B584C4  test    al, al
00B584C6  jz      loc_B890FE
00B584CC  mov     ecx, [esi+0Ch]
00B584CF  mov     eax, [ecx]
00B584D1  mov     edx, [eax+78h]
00B584D4  push    0Ch
00B584D6  call    edx
00B584D8  mov     [esp+2C5Ch+var_2C3C], eax
00B584DC  mov     eax, [esi+0Ch]
00B584DF  push    eax
00B584E0  lea     ecx, [esp+2C60h+var_27CC]
00B584E7  call    sub_ABB2F0
00B584EC  lea     ecx, [esp+2C5Ch+var_2C3C]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5850F 附近（领取邮件附件结果码）
00B58505  mov     eax, [esp+2C5Ch+var_2C48]
00B58509  lea     edx, [esp+2C5Ch+var_2C44]
00B5850D  push    edx
00B5850E  push    eax
00B5850F  call    sub_B02DD0
00B58514  add     esp, 8
00B58517  test    al, al
00B58519  jnz     short loc_B58537
00B5851B  mov     edx, [esi]
00B5851D  mov     eax, [edx+64h]
```

## E3 字段 2：`mailid`（u64，偏移 4，长度 8）

```asm
; VA: 0x0xB5854F 附近（邮件唯一 ID）
00B58545  mov     ebx, [esp+2C5Ch+var_2C20]
00B58549  lea     edx, [esp+2C5Ch+var_2C44]
00B5854D  push    edx
00B5854E  push    ebx
00B5854F  call    sub_B06200
00B58554  add     esp, 8
00B58557  test    al, al
00B58559  mov     ecx, esi
00B5855B  jnz     short loc_B58577
00B5855D  mov     eax, [esi]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5857B
00B58562  push    1
00B58564  push    171h
00B58569  call    edx
00B5856B  lea     ecx, [esp+2C5Ch+var_27CC]
00B58572  jmp     loc_B890EE
00B58577  mov     eax, [esp+2C5Ch+var_2C44]
00B5857B  cmp     eax, [esp+2C5Ch+var_2C40]
00B5857F  jz      short loc_B5859B
00B58581  mov     edx, [esi]
00B58583  mov     eax, [edx+64h]
00B58586  push    1
00B58588  push    171h
00B5858D  call    eax
00B5858F  lea     ecx, [esp+2C5Ch+var_27CC]
```
