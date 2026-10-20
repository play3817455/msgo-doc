# 汇编证据 —— SC-0x2775-lounge-you9_cps_HDB_request

> 地址口径：完整 VA（ImageBase `0x400000`），IDA 中可直接跳转。

## E1 块入口 + 解码缓冲申请（容量 `0x19004` @ `0xB59427`）

```asm
; VA: 0xB5940B .. （块入口，含守卫与容量申请）
00B5940B  push    219h
00B59410  mov     ecx, esi
00B59412  call    sub_B41120
00B59417  test    al, al
00B59419  jz      loc_B890FE
00B5941F  mov     ecx, [esi+0Ch]
00B59422  mov     eax, [ecx]
00B59424  mov     edx, [eax+78h]
00B59427  push    19004h
00B5942C  call    edx
00B5942E  mov     [esp+2C5Ch+var_2C3C], eax
00B59432  mov     eax, [esi+0Ch]
00B59435  push    eax
00B59436  lea     ecx, [esp+2C60h+var_27BC]
```

## E2 字段 1：`hdb_size`（u32，偏移 0，长度 4）

```asm
; VA: 0x0xB59457 附近（HDB 数据块字节数 N）
00B59446  push    ecx
00B59447  lea     edx, [esp+2C60h+var_2C2C]
00B5944B  push    edx
00B5944C  mov     [esp+2C64h+var_4], 251h
00B59457  call    sub_B02DD0
00B5945C  add     esp, 8
00B5945F  test    al, al
00B59461  jnz     short loc_B5947F
00B59463  mov     eax, [esi]
00B59465  mov     edx, [eax+64h]
```

## E3 字段 2：`hdbdat`（u8[N]，偏移 4，长度 N）

```asm
; VA: 0x0xB594AC 附近（HDB 原始数据块（N 字节））
00B594A4  lea     ecx, [esp+2C5Ch+var_2C44]
00B594A8  push    ecx
00B594A9  add     edx, edi
00B594AB  push    edx
00B594AC  call    sub_B06230
00B594B1  add     esp, 8
00B594B4  test    al, al
00B594B6  jz      short loc_B594C1
00B594B8  add     edi, 1
00B594BB  cmp     edi, ebx
```

## E4 长度闭合（游标 == 报文末尾）

```asm
; VA: 0xB594D5
00B594C3  mov     edx, [eax+64h]
00B594C6  push    1
00B594C8  push    219h
00B594CD  mov     ecx, esi
00B594CF  call    edx
00B594D1  mov     eax, [esp+2C5Ch+var_2C44]
00B594D5  cmp     eax, [esp+2C5Ch+var_2C40]
00B594D9  mov     ecx, esi
00B594DB  jz      short loc_B594F7
00B594DD  mov     edx, [esi]
00B594DF  mov     eax, [edx+64h]
00B594E2  push    1
00B594E4  push    219h
00B594E9  call    eax
```
