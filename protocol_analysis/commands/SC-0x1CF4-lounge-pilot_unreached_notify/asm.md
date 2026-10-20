# 汇编证据 —— SC-0x1CF4-lounge-pilot_unreached_notify

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x10` @ `0xB577FB`）

```asm
; VA: 0xB577DF .. （块入口，含守卫与容量申请）
00B577DF  push    226h
00B577E4  mov     ecx, esi
00B577E6  call    sub_B41120
00B577EB  test    al, al
00B577ED  jz      loc_B890FE
00B577F3  mov     ecx, [esi+0Ch]
00B577F6  mov     eax, [ecx]
00B577F8  mov     edx, [eax+78h]
00B577FB  push    10h
00B577FD  call    edx
00B577FF  mov     [esp+2C5Ch+var_2C24], eax
00B57803  mov     eax, [esi+0Ch]
00B57806  push    eax
00B57807  lea     ecx, [esp+2C60h+var_2AC4]
```

## E2 字段 1：`notify_type`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB57836 附近（通知类型）
00B5782C  mov     eax, [esp+2C5Ch+var_2C30]
00B57830  lea     edx, [esp+2C5Ch+var_2C44]
00B57834  push    edx
00B57835  push    eax
00B57836  call    sub_B02DD0
00B5783B  add     esp, 8
00B5783E  test    al, al
00B57840  jnz     short loc_B5785E
00B57842  mov     edx, [esi]
00B57844  mov     eax, [edx+64h]
```

## E3 字段 2：`data1`（u32，偏移 4，长度 4）

```asm
; VA: 0x0xB57876 附近（通知数据 1（含义随 `notify_type`））
00B5786C  mov     eax, [esp+2C5Ch+var_2C34]
00B57870  lea     edx, [esp+2C5Ch+var_2C44]
00B57874  push    edx
00B57875  push    eax
00B57876  call    sub_B02DD0
00B5787B  add     esp, 8
00B5787E  test    al, al
00B57880  jz      short loc_B57842
00B57882  lea     ecx, [esp+2C5Ch+var_2C24]
00B57886  push    ecx
```

## E4 字段 3：`data2`（u32，偏移 8，长度 4）

```asm
; VA: 0x0xB5789A 附近（通知数据 2）
00B57890  mov     eax, [esp+2C5Ch+var_2C38]
00B57894  lea     edx, [esp+2C5Ch+var_2C44]
00B57898  push    edx
00B57899  push    eax
00B5789A  call    sub_B02DD0
00B5789F  add     esp, 8
00B578A2  test    al, al
00B578A4  jz      short loc_B57842
00B578A6  lea     ecx, [esp+2C5Ch+var_2C24]
00B578AA  push    ecx
```

## E5 字段 4：`data3`（u32，偏移 12，长度 4）

```asm
; VA: 0x0xB578BE 附近（通知数据 3）
00B578B4  mov     eax, [esp+2C5Ch+var_2C48]
00B578B8  lea     edx, [esp+2C5Ch+var_2C44]
00B578BC  push    edx
00B578BD  push    eax
00B578BE  call    sub_B02DD0
00B578C3  add     esp, 8
00B578C6  test    al, al
00B578C8  jz      loc_B57842
00B578CE  mov     ebx, [esp+2C5Ch+var_2C44]
00B578D2  cmp     ebx, [esp+2C5Ch+var_2C40]
```

## E6 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB578D2
00B578BD  push    eax
00B578BE  call    sub_B02DD0
00B578C3  add     esp, 8
00B578C6  test    al, al
00B578C8  jz      loc_B57842
00B578CE  mov     ebx, [esp+2C5Ch+var_2C44]
00B578D2  cmp     ebx, [esp+2C5Ch+var_2C40]
00B578D6  mov     ecx, esi
00B578D8  jz      short loc_B578F4
00B578DA  mov     edx, [esi]
00B578DC  mov     eax, [edx+64h]
00B578DF  push    1
00B578E1  push    226h
00B578E6  call    eax
```
