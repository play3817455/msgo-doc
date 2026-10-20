# 汇编证据 —— CS-0x0680-activity_request

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA47E0 @ `0xba47e0`（`0xba47e0`..`0xba4966`）
- 命令名字符串：`)<-_proto_lounge_client::send_activity_request( ` @ `0xeecfa8`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA4810 jz      loc_BA4904
00BA4816 mov     ecx, [esi+0Ch]
00BA4819 test    ecx, ecx
00BA481B jz      loc_BA4904
00BA4821 mov     eax, [ecx]
00BA4823 mov     edx, [eax+78h]
00BA4826 push    2
00BA4828 call    edx
00BA482A mov     edi, eax
00BA482C mov     eax, [esi+0Ch]
00BA482F push    eax
00BA4830 lea     ecx, [esp+44h+var_2C]
00BA4834 call    sub_ABB2F0
00BA4839 mov     word ptr [edi], 680h
00BA483E mov     ebp, [esi+81CCh]
00BA4844 test    ebp, ebp
00BA484E lea     ebx, [edi+2]
00BA4851 jz      loc_BA48E2
00BA4857 lea     ecx, [esp+40h+var_28]
00BA485B push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA48E2 mov     edx, [esi]
00BA48E4 mov     eax, [edx+58h]
00BA48E7 sub     ebx, edi
00BA48E9 push    ebx
00BA48EA push    edi
00BA48EB mov     ecx, esi
00BA48ED call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba4839` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EECFA8
```
