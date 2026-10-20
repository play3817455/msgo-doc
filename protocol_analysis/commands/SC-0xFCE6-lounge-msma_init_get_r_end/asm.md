# 汇编证据 —— SC-0xFCE6-msma_init_get_r_end

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb884cd`..`0xb8861d`
- 命令名字符串：`)->_proto_lounge_client::recv_msma_init_get_r_end( ` @ `0xee556c`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B884CD push    0CAh
00B884D2 mov     ecx, esi
00B884D4 call    sub_B41120
00B884D9 test    al, al
00B884DB jz      loc_B890FE
00B884E1 mov     ebx, [esp+2C5Ch+var_2C44]
00B884E5 cmp     ebx, [esp+2C5Ch+var_2C40]
00B884E9 mov     ecx, esi
00B884EB jz      short loc_B88513
00B884ED mov     eax, [esi]
00B884EF mov     edx, [eax+64h]
00B884F2 push    1
00B884F4 push    0CAh
00B884F9 call    edx
00B88513 push    0CAh
00B88518 call    sub_B41110
00B8851D mov     edi, eax
00B8851F test    edi, edi
00B88521 jz      loc_B885BD
00B88527 lea     eax, [esp+2C5Ch+var_10C]
00B8852E push    eax
00B88537 mov     ecx, [esi+8]
00B8853A push    offset aProtoLoungeCli_344
00B8853F push    ecx
00B88540 push    offset aId
00B88545 push    eax
00B88546 push    edi
00B8855A push    eax
00B88563 mov     ecx, eax
00B8856A push    eax
00B88573 lea     ecx, [esp+2C5Ch+var_10C]
00B88585 call    sub_B02FF0
00B8858A sub     ebx, [ebp+arg_0]
00B8858D push    offset sub_B03810
00B88592 push    offset aByte
00B88597 push    ebx
00B88598 push    offset asc_EDAD58
00B8859D push    edi
00B885A6 mov     ecx, eax
00B885AD push    eax
00B885B6 mov     ecx, eax
00B885B8 call    sub_B02D30
00B885BD mov     edx, [esi]
00B885BF mov     eax, [edx+234h]
00B885C5 mov     ecx, esi
00B885C7 call    eax
00B885C9 add     dword ptr [esi+2B38h], 1
00B885EF cmp     eax, 0FEF1h
00B885F4 jg      loc_B88C75
00B885FA jz      loc_B88A8E
00B88600 cmp     eax, 0FCE9h
00B88605 jz      loc_B88852
00B8860B cmp     eax, 0FE46h
00B88610 jnz     def_B605BD
00B88616 push    0D0h
00B8861B mov     ecx, esi
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb8853a` | opcode 写入/分发指令 |

## 4. 块内字符串常量（含义取证用）

```
00B88513
00EE556C
00B02D30
00B88C75
00B88A8E
00B88852
00B88C7C
```
