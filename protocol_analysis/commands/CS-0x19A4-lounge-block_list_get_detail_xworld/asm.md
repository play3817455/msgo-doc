# 汇编证据 —— CS-0x19A4-block_list_get_detail_xworld

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9B300 @ `0xb9b300`（`0xb9b300`..`0xb9b486`）
- 命令名字符串：`)<-_proto_lounge_client::send_block_list_get_detail_xworld( ` @ `0xeec0f8`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9B330 jz      loc_B9B424
00B9B336 mov     ecx, [esi+0Ch]
00B9B339 test    ecx, ecx
00B9B33B jz      loc_B9B424
00B9B341 mov     eax, [ecx]
00B9B343 mov     edx, [eax+78h]
00B9B346 push    2
00B9B348 call    edx
00B9B34A mov     edi, eax
00B9B34C mov     eax, [esi+0Ch]
00B9B34F push    eax
00B9B350 lea     ecx, [esp+44h+var_2C]
00B9B354 call    sub_ABB2F0
00B9B359 mov     word ptr [edi], 19A4h
00B9B35E mov     ebp, [esi+7F30h]
00B9B364 test    ebp, ebp
00B9B36E lea     ebx, [edi+2]
00B9B371 jz      loc_B9B402
00B9B377 lea     ecx, [esp+40h+var_28]
00B9B37B push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9B402 mov     edx, [esi]
00B9B404 mov     eax, [edx+58h]
00B9B407 sub     ebx, edi
00B9B409 push    ebx
00B9B40A push    edi
00B9B40B mov     ecx, esi
00B9B40D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb9b359` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EEC0F8
```
