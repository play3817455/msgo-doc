# 汇编证据 —— SC-0x2ACF-lounge-msma_init_get_r_begin

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1C` @ `0xB59F8C`）

```asm
; VA: 0xB59F70 .. （块入口，含守卫与容量申请）
00B59F70  push    0C9h
00B59F75  mov     ecx, esi
00B59F77  call    sub_B41120
00B59F7C  test    al, al
00B59F7E  jz      loc_B890FE
00B59F84  mov     ecx, [esi+0Ch]
00B59F87  mov     eax, [ecx]
00B59F89  mov     edx, [eax+78h]
00B59F8C  push    1Ch
00B59F8E  call    edx
00B59F90  mov     [esp+2C5Ch+var_2C28], eax
00B59F94  mov     eax, [esi+0Ch]
00B59F97  push    eax
00B59F98  lea     ecx, [esp+2C60h+var_2B94]
```

## E2 字段 1：`sv_time`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB59FC7 附近（服务器时间）
00B59FBD  mov     eax, [esp+2C5Ch+var_2BEC]
00B59FC1  lea     edx, [esp+2C5Ch+var_2C44]
00B59FC5  push    edx
00B59FC6  push    eax
00B59FC7  call    sub_B02DD0
00B59FCC  add     esp, 8
00B59FCF  test    al, al
00B59FD1  jnz     short loc_B59FEF
00B59FD3  mov     edx, [esi]
00B59FD5  mov     eax, [edx+64h]
```

## E3 字段 2：`slot_num`（u16，偏移 4，长度 2）

```asm
; VA: 0x0xB5A007 附近（机体槽位数（本报文为 `*_begin`，随后由 `0xA832` 续传））
00B59FFD  mov     eax, [esp+2C5Ch+var_2BF0]
00B5A001  lea     edx, [esp+2C5Ch+var_2C44]
00B5A005  push    edx
00B5A006  push    eax
00B5A007  call    sub_B02DF0
00B5A00C  add     esp, 8
00B5A00F  test    al, al
00B5A011  jz      short loc_B59FD3
00B5A013  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A017  push    ecx
```

## E4 字段 3：`sort_tm_sec`（u32，偏移 6，长度 4）

```asm
; VA: 0x0xB5A02B 附近（排序时间戳（秒））
00B5A021  mov     eax, [esp+2C5Ch+var_2BFC]
00B5A025  lea     edx, [esp+2C5Ch+var_2C44]
00B5A029  push    edx
00B5A02A  push    eax
00B5A02B  call    sub_B02DD0
00B5A030  add     esp, 8
00B5A033  test    al, al
00B5A035  jz      short loc_B59FD3
00B5A037  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A03B  push    ecx
```

## E5 字段 4：`sort_tm_usec`（u32，偏移 10，长度 4）

```asm
; VA: 0x0xB5A04F 附近（排序时间戳（微秒））
00B5A045  mov     eax, [esp+2C5Ch+var_2C08]
00B5A049  lea     edx, [esp+2C5Ch+var_2C44]
00B5A04D  push    edx
00B5A04E  push    eax
00B5A04F  call    sub_B02DD0
00B5A054  add     esp, 8
00B5A057  test    al, al
00B5A059  jz      loc_B59FD3
00B5A05F  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A063  push    ecx
```

## E6 字段 5：`conf_payload_boost_penalty`（u16，偏移 14，长度 2）

```asm
; VA: 0x0xB5A077 附近（配置：负载强化扣减）
00B5A06D  mov     eax, [esp+2C5Ch+var_2C0C]
00B5A071  lea     edx, [esp+2C5Ch+var_2C44]
00B5A075  push    edx
00B5A076  push    eax
00B5A077  call    sub_B02DF0
00B5A07C  add     esp, 8
00B5A07F  test    al, al
00B5A081  jz      loc_B59FD3
00B5A087  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A08B  push    ecx
```

## E7 字段 6：`conf_payload_boost_bonus`（u16，偏移 16，长度 2）

```asm
; VA: 0x0xB5A09F 附近（配置：负载强化加成）
00B5A095  mov     eax, [esp+2C5Ch+var_2C30]
00B5A099  lea     edx, [esp+2C5Ch+var_2C44]
00B5A09D  push    edx
00B5A09E  push    eax
00B5A09F  call    sub_B02DF0
00B5A0A4  add     esp, 8
00B5A0A7  test    al, al
00B5A0A9  jz      loc_B59FD3
00B5A0AF  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A0B3  push    ecx
```

## E8 字段 7：`conf_payload_body_balance_max`（u16，偏移 18，长度 2）

```asm
; VA: 0x0xB5A0C7 附近（配置：机体平衡上限）
00B5A0BD  mov     eax, [esp+2C5Ch+var_2C34]
00B5A0C1  lea     edx, [esp+2C5Ch+var_2C44]
00B5A0C5  push    edx
00B5A0C6  push    eax
00B5A0C7  call    sub_B02DF0
00B5A0CC  add     esp, 8
00B5A0CF  test    al, al
00B5A0D1  jz      loc_B59FD3
00B5A0D7  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A0DB  push    ecx
```

## E9 字段 8：`msma_sort_type`（u32，偏移 20，长度 4）

```asm
; VA: 0x0xB5A0EF 附近（机体排序类型）
00B5A0E5  mov     eax, [esp+2C5Ch+var_2C38]
00B5A0E9  lea     edx, [esp+2C5Ch+var_2C44]
00B5A0ED  push    edx
00B5A0EE  push    eax
00B5A0EF  call    sub_B02DD0
00B5A0F4  add     esp, 8
00B5A0F7  test    al, al
00B5A0F9  jz      loc_B59FD3
00B5A0FF  lea     ecx, [esp+2C5Ch+var_2C28]
00B5A103  push    ecx
```

## E10 字段 9：`msma_sort_order`（u32，偏移 24，长度 4）

```asm
; VA: 0x0xB5A117 附近（机体排序方向）
00B5A10D  mov     eax, [esp+2C5Ch+var_2C48]
00B5A111  lea     edx, [esp+2C5Ch+var_2C44]
00B5A115  push    edx
00B5A116  push    eax
00B5A117  call    sub_B02DD0
00B5A11C  add     esp, 8
00B5A11F  test    al, al
00B5A121  jz      loc_B59FD3
00B5A127  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A12B  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E11 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5A12B
00B5A116  push    eax
00B5A117  call    sub_B02DD0
00B5A11C  add     esp, 8
00B5A11F  test    al, al
00B5A121  jz      loc_B59FD3
00B5A127  mov     ebx, [esp+2C5Ch+var_2C44]
00B5A12B  cmp     ebx, [esp+2C5Ch+var_2C40]
00B5A12F  mov     ecx, esi
00B5A131  jz      short loc_B5A14D
00B5A133  mov     edx, [esi]
00B5A135  mov     eax, [edx+64h]
00B5A138  push    1
00B5A13A  push    0C9h
00B5A13F  call    eax
```
