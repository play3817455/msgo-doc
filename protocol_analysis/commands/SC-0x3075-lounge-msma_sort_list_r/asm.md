# 汇编证据 —— SC-0x3075-lounge-msma_sort_list_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB5B157`）

```asm
; VA: 0xB5B13B .. （块入口，含守卫与容量申请）
00B5B13B  push    0FBh
00B5B140  mov     ecx, esi
00B5B142  call    sub_B41120
00B5B147  test    al, al
00B5B149  jz      loc_B890FE
00B5B14F  mov     ecx, [esi+0Ch]
00B5B152  mov     edx, [ecx]
00B5B154  mov     eax, [edx+78h]
00B5B157  push    10h
00B5B159  call    eax
00B5B15B  mov     ecx, [esi+0Ch]
00B5B15E  push    ecx
00B5B15F  lea     ecx, [esp+2C60h+var_2A8C]
00B5B166  mov     [esp+2C60h+var_2C24], eax
```

## E2 字段 1：`sort_tm_sec`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5B192 附近（排序时间戳（秒））
00B5B188  mov     ecx, [esp+2C5Ch+var_2C30]
00B5B18C  lea     eax, [esp+2C5Ch+var_2C44]
00B5B190  push    eax
00B5B191  push    ecx
00B5B192  call    sub_B02DD0
00B5B197  add     esp, 8
00B5B19A  test    al, al
00B5B19C  jnz     short loc_B5B1BA
00B5B19E  mov     edx, [esi]
00B5B1A0  mov     eax, [edx+64h]
```

## E3 字段 2：`sort_tm_usec`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB5B1D2 附近（排序时间戳（微秒））
00B5B1C8  mov     eax, [esp+2C5Ch+var_2C34]
00B5B1CC  lea     edx, [esp+2C5Ch+var_2C44]
00B5B1D0  push    edx
00B5B1D1  push    eax
00B5B1D2  call    sub_B02DD0
00B5B1D7  add     esp, 8
00B5B1DA  test    al, al
00B5B1DC  jz      short loc_B5B19E
00B5B1DE  lea     ecx, [esp+2C5Ch+var_2C24]
00B5B1E2  push    ecx
```

## E4 字段 3：`msma_sort_type`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB5B1F6 附近（机体排序类型）
00B5B1EC  mov     eax, [esp+2C5Ch+var_2C38]
00B5B1F0  lea     edx, [esp+2C5Ch+var_2C44]
00B5B1F4  push    edx
00B5B1F5  push    eax
00B5B1F6  call    sub_B02DD0
00B5B1FB  add     esp, 8
00B5B1FE  test    al, al
00B5B200  jz      short loc_B5B19E
00B5B202  lea     ecx, [esp+2C5Ch+var_2C24]
00B5B206  push    ecx
```

## E5 字段 4：`msma_sort_order`（u32，偏移 12，长度 4）

```asm
; VA: 0x0xB5B1F6 附近（机体排序方向）
00B5B1EC  mov     eax, [esp+2C5Ch+var_2C38]
00B5B1F0  lea     edx, [esp+2C5Ch+var_2C44]
00B5B1F4  push    edx
00B5B1F5  push    eax
00B5B1F6  call    sub_B02DD0
00B5B1FB  add     esp, 8
00B5B1FE  test    al, al
00B5B200  jz      short loc_B5B19E
00B5B202  lea     ecx, [esp+2C5Ch+var_2C24]
00B5B206  push    ecx
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5B250
00B5B238  mov     eax, [edx+64h]
00B5B23B  push    1
00B5B23D  push    0FBh
00B5B242  call    eax
00B5B244  lea     ecx, [esp+2C5Ch+var_2A8C]
00B5B24B  jmp     loc_B890EE
00B5B250  push    0FBh
00B5B255  call    sub_B41110
00B5B25A  mov     edi, eax
00B5B25C  test    edi, edi
00B5B25E  jz      loc_B5B38E
00B5B264  lea     ecx, [esp+2C5Ch+var_1FC8]
00B5B26B  push    ecx
00B5B26C  call    sub_CA0CE0
```
