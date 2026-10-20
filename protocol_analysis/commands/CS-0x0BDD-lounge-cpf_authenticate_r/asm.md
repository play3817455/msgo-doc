# 汇编证据 —— CS-0x0BDD-cpf_authenticate_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA4B00 @ `0xba4b00`（`0xba4b00`..`0xba4d43`）
- 命令名字符串：`)<-_proto_lounge_client::send_cpf_authenticate_r( ` @ `0xeed018`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA4B36 mov     ecx, [ebx+0Ch]
00BA4B39 test    ecx, ecx
00BA4B3B jz      loc_BA4D3F
00BA4B41 mov     eax, [ecx]
00BA4B43 mov     edx, [eax+78h]
00BA4B46 push    86h
00BA4B4B call    edx
00BA4B4D mov     esi, eax
00BA4B4F mov     eax, [ebx+0Ch]
00BA4B52 push    eax
00BA4B53 lea     ecx, [esp+50h+var_38]
00BA4B57 mov     [esp+50h+var_34], esi
00BA4B5B call    sub_ABB2F0
00BA4B60 lea     ecx, [esi+86h]
00BA4B66 lea     eax, [esi+2]
00BA4B69 cmp     eax, ecx
00BA4B73 ja      loc_BA4D2E
00BA4B79 mov     ebp, [esp+4Ch+arg_4]
00BA4B7D cmp     ebp, 80h
00BA4B83 mov     word ptr [esi], 0BDDh
00BA4B88 ja      loc_BA4D2E
00BA4B8E lea     esi, [eax+4]
00BA4B91 cmp     esi, ecx
00BA4B93 ja      loc_BA4D2E
00BA4B99 mov     [eax], ebp
00BA4B9B xor     eax, eax
00BA4B9D test    ebp, ebp
00BA4B9F mov     [esp+4Ch+var_30], esi
00BA4BA3 jbe     short loc_BA4BCA
00BA4BA5 lea     edi, [esi+1]
00BA4BA8 cmp     edi, ecx
00BA4BAA ja      loc_BA4D2A
00BA4BB0 mov     edx, [esp+4Ch+arg_0]
00BA4BB4 mov     dl, [eax+edx]
00BA4BB7 mov     [esi], dl
00BA4BB9 add     eax, 1
00BA4BBC add     esi, 1
00BA4BBF add     edi, 1
00BA4BC2 cmp     eax, ebp
00BA4BC4 jb      short loc_BA4BA8
00BA4BC6 mov     [esp+4Ch+var_30], esi
00BA4BCA mov     edi, [ebx+81FCh]
00BA4BD0 test    edi, edi
00BA4BD2 jz      loc_BA4CC7
00BA4BD8 lea     eax, [esp+4Ch+var_28]
00BA4BDC push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA4CCB mov     edx, [ebx]
00BA4CCD mov     eax, [edx+58h]
00BA4CD0 sub     esi, edi
00BA4CD2 push    esi
00BA4CD3 push    edi
00BA4CD4 mov     ecx, ebx
00BA4CD6 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba4b83` | opcode 写入/分发指令 |
| `data_len` | `0xBA4B99` | u32 |
| `data` | `0xBA4BB7` | bytes |

## 5. 块内字符串常量（含义取证用）

```
00BA4BA8
00EED018
00EDC7C0
00BA4C77
00BA4C52
00EDABE4
```
