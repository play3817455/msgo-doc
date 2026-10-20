# 汇编证据 —— CS-0x16AC-msma_init_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B92E40 @ `0xb92e40`（`0xb92e40`..`0xb92fc6`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_init_get( ` @ `0xeeb2e8`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B92E70 jz      loc_B92F64
00B92E76 mov     ecx, [esi+0Ch]
00B92E79 test    ecx, ecx
00B92E7B jz      loc_B92F64
00B92E81 mov     eax, [ecx]
00B92E83 mov     edx, [eax+78h]
00B92E86 push    2
00B92E88 call    edx
00B92E8A mov     edi, eax
00B92E8C mov     eax, [esi+0Ch]
00B92E8F push    eax
00B92E90 lea     ecx, [esp+44h+var_2C]
00B92E94 call    sub_ABB2F0
00B92E99 mov     word ptr [edi], 16ACh
00B92E9E mov     ebp, [esi+7CD0h]
00B92EA4 test    ebp, ebp
00B92EAE lea     ebx, [edi+2]
00B92EB1 jz      loc_B92F42
00B92EB7 lea     ecx, [esp+40h+var_28]
00B92EBB push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B92F42 mov     edx, [esi]
00B92F44 mov     eax, [edx+58h]
00B92F47 sub     ebx, edi
00B92F49 push    ebx
00B92F4A push    edi
00B92F4B mov     ecx, esi
00B92F4D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb92e99` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EEB2E8
```
