# 汇编证据 —— SC-0x228A-lounge-announce

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0xB7` @ `0xB58977`）

```asm
; VA: 0xB5895E .. （块入口，含守卫与容量申请）
00B5895E  push    58h ; 'X'
00B58960  mov     ecx, esi
00B58962  call    sub_B41120
00B58967  test    al, al
00B58969  jz      loc_B890FE
00B5896F  mov     ecx, [esi+0Ch]
00B58972  mov     eax, [ecx]
00B58974  mov     edx, [eax+78h]
00B58977  push    0B7h
00B5897C  call    edx
00B5897E  mov     edi, eax
00B58980  mov     eax, [esi+0Ch]
00B58983  push    eax
00B58984  lea     ecx, [esp+2C60h+var_27C4]
```

## E2 字段 1：`msg`（str，偏移 0，长度 L+1）

```asm
; VA: 0x0xB589B6 附近（公告文本（NUL 结尾；槽预算 181））
00B589A2  push    eax
00B589A3  mov     [esp+2C68h+var_4], 62h ; 'b'
00B589AE  mov     [esp+2C68h+var_2C3C], eax
00B589B2  mov     [esp+2C68h+var_2C20], edi
00B589B6  call    sub_B02BA0
00B589BB  add     esp, 0Ch
00B589BE  test    al, al
00B589C0  jnz     short loc_B589DB
00B589C2  mov     edx, [esi]
00B589C4  mov     eax, [edx+64h]
```

## E3 字段 2：`priority`（u16，偏移 串之后，长度 2）

```asm
; VA: 0x0xB589F3 附近（公告优先级）
00B589E9  mov     eax, [esp+2C5Ch+var_2C48]
00B589ED  lea     edx, [esp+2C5Ch+var_2C44]
00B589F1  push    edx
00B589F2  push    eax
00B589F3  call    sub_B02DF0
00B589F8  add     esp, 8
00B589FB  test    al, al
00B589FD  jz      short loc_B589C2
00B589FF  mov     ebx, [esp+2C5Ch+var_2C44]
00B58A03  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB58A03
00B589F2  push    eax
00B589F3  call    sub_B02DF0
00B589F8  add     esp, 8
00B589FB  test    al, al
00B589FD  jz      short loc_B589C2
00B589FF  mov     ebx, [esp+2C5Ch+var_2C44]
00B58A03  cmp     ebx, [esp+2C5Ch+var_2C40]
00B58A07  mov     ecx, esi
00B58A09  jz      short loc_B58A22
00B58A0B  mov     edx, [esi]
00B58A0D  mov     eax, [edx+64h]
00B58A10  push    1
00B58A12  push    58h ; 'X'
00B58A14  call    eax
```
