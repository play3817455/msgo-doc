# 汇编证据 —— CS-0x0C2A-msma_trialms_back

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B99C20 @ `0xb99c20`（`0xb99c20`..`0xb99dd9`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_trialms_back( ` @ `0xeebe2c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B99C50 jz      loc_B99DD5
00B99C56 mov     ecx, [esi+0Ch]
00B99C59 test    ecx, ecx
00B99C5B jz      loc_B99DD5
00B99C61 mov     eax, [ecx]
00B99C63 mov     edx, [eax+78h]
00B99C66 push    0Ah
00B99C68 call    edx
00B99C6A mov     ebp, eax
00B99C6C mov     eax, [esi+0Ch]
00B99C6F push    eax
00B99C70 lea     ecx, [esp+44h+var_2C]
00B99C74 call    sub_ABB2F0
00B99C79 lea     ecx, [ebp+0Ah]
00B99C7C lea     eax, [ebp+2]
00B99C7F cmp     eax, ecx
00B99C89 ja      loc_B99DC4
00B99C8F lea     ebx, [eax+8]
00B99C92 cmp     ebx, ecx
00B99C94 mov     word ptr [ebp+0], 0C2Ah
00B99C9A ja      loc_B99DC4
00B99CA0 mov     ecx, [esp+40h+arg_0]
00B99CA4 mov     edx, [esp+40h+arg_4]
00B99CA8 mov     [eax], ecx
00B99CAA mov     [eax+4], edx
00B99CAD mov     edi, [esi+7EA4h]
00B99CB3 test    edi, edi
00B99CB5 jz      loc_B99D65
00B99CBB lea     eax, [esp+40h+var_28]
00B99CBF push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B99D65 mov     edx, [esi]
00B99D67 mov     eax, [edx+58h]
00B99D6A sub     ebx, ebp
00B99D6C push    ebx
00B99D6D push    ebp
00B99D6E mov     ecx, esi
00B99D70 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb99c94` | opcode 写入/分发指令 |
| `uniqid_ms` | `0xB99CA8,0xB99CAA` | u64 |

## 5. 块内字符串常量（含义取证用）

```
00EEBE2C
00EE41BC
```
