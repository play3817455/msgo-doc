# 汇编证据 —— CS-0x0A73-party_recruit_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B928B0 @ `0xb928b0`（`0xb928b0`..`0xb92a5d`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_recruit_list_get( ` @ `0xeeb240`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B928E0 jz      loc_B92A59
00B928E6 mov     ecx, [esi+0Ch]
00B928E9 test    ecx, ecx
00B928EB jz      loc_B92A59
00B928F1 mov     eax, [ecx]
00B928F3 mov     edx, [eax+78h]
00B928F6 push    6
00B928F8 call    edx
00B928FA mov     ebp, eax
00B928FC mov     eax, [esi+0Ch]
00B928FF push    eax
00B92900 lea     ecx, [esp+44h+var_2C]
00B92904 call    sub_ABB2F0
00B92909 lea     ecx, [ebp+6]
00B9290C lea     eax, [ebp+2]
00B9290F cmp     eax, ecx
00B92919 ja      loc_B92A48
00B9291F lea     ebx, [eax+4]
00B92922 cmp     ebx, ecx
00B92924 mov     word ptr [ebp+0], 0A73h
00B9292A ja      loc_B92A48
00B92930 mov     ecx, [esp+40h+arg_0]
00B92934 mov     [eax], ecx
00B92936 mov     edi, [esi+7CB4h]
00B9293C test    edi, edi
00B9293E jz      loc_B929E9
00B92944 lea     edx, [esp+40h+var_28]
00B92948 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B929E9 mov     edx, [esi]
00B929EB mov     eax, [edx+58h]
00B929EE sub     ebx, ebp
00B929F0 push    ebx
00B929F1 push    ebp
00B929F2 mov     ecx, esi
00B929F4 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb92924` | opcode 写入/分发指令 |
| `party_type` | `0xB92934` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEB240
00EE3184
```
