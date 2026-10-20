# 汇编证据 —— SC-0x305D-lounge-party_recruit_detail_get_r

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x1DC` @ `0xB5AD27`）

```asm
; VA: 0xB5AD0B .. （块入口，含守卫与容量申请）
00B5AD0B  push    0C4h
00B5AD10  mov     ecx, esi
00B5AD12  call    sub_B41120
00B5AD17  test    al, al
00B5AD19  jz      loc_B890FE
00B5AD1F  mov     ecx, [esi+0Ch]
00B5AD22  mov     eax, [ecx]
00B5AD24  mov     edx, [eax+78h]
00B5AD27  push    1DCh
00B5AD2C  call    edx
00B5AD2E  mov     [esp+2C5Ch+var_2C48], eax
00B5AD32  mov     eax, [esi+0Ch]
00B5AD35  push    eax
00B5AD36  lea     ecx, [esp+2C60h+var_2A94]
```

## E2 字段 1：`result`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB5AD65 附近（招募详情查询结果码）
00B5AD5B  mov     eax, [esp+2C5Ch+var_2C34]
00B5AD5F  lea     edx, [esp+2C5Ch+var_2C44]
00B5AD63  push    edx
00B5AD64  push    eax
00B5AD65  call    sub_B02DD0
00B5AD6A  add     esp, 8
00B5AD6D  test    al, al
00B5AD6F  jnz     short loc_B5AD8D
00B5AD71  mov     edx, [esi]
00B5AD73  mov     eax, [edx+64h]
```

## E3 字段 2：`recruit`（struct{74/槽84}，偏移 4，长度 74）

```asm
; VA: 0x0xB5ADA5 附近（招募信息结构（线上 74B；缓冲槽 84））
00B5AD9B  mov     eax, [esp+2C5Ch+var_2C38]
00B5AD9F  lea     edx, [esp+2C5Ch+var_2C44]
00B5ADA3  push    edx
00B5ADA4  push    eax
00B5ADA5  call    sub_B45400
00B5ADAA  add     esp, 8
00B5ADAD  test    al, al
00B5ADAF  jz      short loc_B5AD71
00B5ADB1  lea     ecx, [esp+2C5Ch+var_2C44]
00B5ADB5  push    ecx
```

## E11 字段 10：`members_num`（u32，偏移 78，长度 4）

```asm
; VA: 0x0xB5ADBB 附近（成员条目数 N）
00B5ADB1  lea     ecx, [esp+2C5Ch+var_2C44]
00B5ADB5  push    ecx
00B5ADB6  lea     edx, [esp+2C60h+var_2C3C]
00B5ADBA  push    edx
00B5ADBB  call    sub_B02DD0
00B5ADC0  add     esp, 8
00B5ADC3  test    al, al
00B5ADC5  jnz     short loc_B5ADE3
00B5ADC7  mov     eax, [esi]
00B5ADC9  mov     edx, [eax+64h]
```

## E12 字段 11：`members`（array<elem 34>，偏移 82，长度 34·N）

```asm
; VA: 0x0xB5AE13 附近（成员列表（元素线上 34B / 缓冲槽步进 64B））
00B5AE09  mov     eax, [esp+2C5Ch+var_2C48]
00B5AE0D  lea     edx, [esp+2C5Ch+var_2C44]
00B5AE11  push    edx
00B5AE12  push    eax
00B5AE13  call    sub_B454D0
00B5AE18  add     esp, 8
00B5AE1B  test    al, al
00B5AE1D  jz      short loc_B5AE2D
00B5AE1F  add     [esp+2C5Ch+var_2C48], 40h ; '@'
00B5AE24  add     edi, 1
```

## E19 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB5AE41
00B5AE2F  mov     eax, [edx+64h]
00B5AE32  push    1
00B5AE34  push    0C4h
00B5AE39  mov     ecx, esi
00B5AE3B  call    eax
00B5AE3D  mov     ecx, [esp+2C5Ch+var_2C44]
00B5AE41  cmp     ecx, [esp+2C5Ch+var_2C40]
00B5AE45  mov     ecx, esi
00B5AE47  jz      short loc_B5AE63
00B5AE49  mov     edx, [esi]
00B5AE4B  mov     eax, [edx+64h]
00B5AE4E  push    1
00B5AE50  push    0C4h
00B5AE55  call    eax
```
