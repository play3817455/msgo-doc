# 汇编证据 —— SC-0x1E49-lounge-party_enter_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x48` @ `0xB57A90`）

```asm
; VA: 0xB57A74 .. （块入口，含守卫与容量申请）
00B57A74  push    0B6h
00B57A79  mov     ecx, esi
00B57A7B  call    sub_B41120
00B57A80  test    al, al
00B57A82  jz      loc_B890FE
00B57A88  mov     ecx, [esi+0Ch]
00B57A8B  mov     eax, [ecx]
00B57A8D  mov     edx, [eax+78h]
00B57A90  push    48h ; 'H'
00B57A92  call    edx
00B57A94  mov     [esp+2C5Ch+var_2C2C], eax
00B57A98  mov     eax, [esi+0Ch]
00B57A9B  push    eax
00B57A9C  lea     ecx, [esp+2C60h+var_2AEC]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB57ACB 附近（入队结果码）
00B57AC1  mov     eax, [esp+2C5Ch+var_2C30]
00B57AC5  lea     edx, [esp+2C5Ch+var_2C44]
00B57AC9  push    edx
00B57ACA  push    eax
00B57ACB  call    sub_B02DD0
00B57AD0  add     esp, 8
00B57AD3  test    al, al
00B57AD5  jnz     short loc_B57AF3
00B57AD7  mov     edx, [esi]
00B57AD9  mov     eax, [edx+64h]
```

## E3 字段 2：`is_recruiting`（u8，偏移 4，长度 1）

```asm
; VA: 0x0xB57B0B 附近（是否正在招募）
00B57B01  mov     eax, [esp+2C5Ch+var_2C34]
00B57B05  lea     edx, [esp+2C5Ch+var_2C44]
00B57B09  push    edx
00B57B0A  push    eax
00B57B0B  call    sub_B06230
00B57B10  add     esp, 8
00B57B13  test    al, al
00B57B15  jz      short loc_B57AD7
00B57B17  mov     eax, [esp+2C5Ch+var_2C2C]
00B57B1B  mov     ecx, eax
```

## E4 字段 3：`comment`（str，偏移 5，长度 L+1）

```asm
; VA: 0x0xB57B30 附近（招募/队伍留言（NUL 结尾；槽预算 61））
00B57B24  add     eax, 3Dh ; '='
00B57B27  push    ecx
00B57B28  mov     [esp+2C68h+var_2C3C], ecx
00B57B2C  mov     [esp+2C68h+var_2C2C], eax
00B57B30  call    sub_B02BA0
00B57B35  add     esp, 0Ch
00B57B38  test    al, al
00B57B3A  jnz     short loc_B57B58
00B57B3C  mov     eax, [esi]
00B57B3E  mov     edx, [eax+64h]
```

## E5 字段 4：`remain_minutes`（u16，偏移 串之后，长度 2）

```asm
; VA: 0x0xB57B70 附近（剩余有效时间（分钟））
00B57B66  mov     edx, [esp+2C5Ch+var_2C38]
00B57B6A  lea     ecx, [esp+2C5Ch+var_2C44]
00B57B6E  push    ecx
00B57B6F  push    edx
00B57B70  call    sub_B02DF0
00B57B75  add     esp, 8
00B57B78  test    al, al
00B57B7A  jz      short loc_B57B3C
00B57B7C  lea     eax, [esp+2C5Ch+var_2C2C]
00B57B80  push    eax
```

## E6 字段 5：`party_type`（u32，偏移 串之后，长度 4）

```asm
; VA: 0x0xB57B94 附近（队伍类型）
00B57B8A  mov     edx, [esp+2C5Ch+var_2C48]
00B57B8E  lea     ecx, [esp+2C5Ch+var_2C44]
00B57B92  push    ecx
00B57B93  push    edx
00B57B94  call    sub_B02DD0
00B57B99  add     esp, 8
00B57B9C  test    al, al
00B57B9E  jz      short loc_B57B3C
00B57BA0  mov     ebx, [esp+2C5Ch+var_2C44]
00B57BA4  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E7 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB57BA4
00B57B93  push    edx
00B57B94  call    sub_B02DD0
00B57B99  add     esp, 8
00B57B9C  test    al, al
00B57B9E  jz      short loc_B57B3C
00B57BA0  mov     ebx, [esp+2C5Ch+var_2C44]
00B57BA4  cmp     ebx, [esp+2C5Ch+var_2C40]
00B57BA8  mov     ecx, esi
00B57BAA  jz      short loc_B57BC6
00B57BAC  mov     eax, [esi]
00B57BAE  mov     edx, [eax+64h]
00B57BB1  push    1
00B57BB3  push    0B6h
00B57BB8  call    edx
```
