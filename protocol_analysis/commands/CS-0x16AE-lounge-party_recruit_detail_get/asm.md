# 汇编证据 —— CS-0x16AE-party_recruit_detail_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B92A60 @ `0xb92a60`（`0xb92a60`..`0xb92c46`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_recruit_detail_get( ` @ `0xeeb278`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B92A90 jz      loc_B92C42
00B92A96 mov     ecx, [edi+0Ch]
00B92A99 test    ecx, ecx
00B92A9B jz      loc_B92C42
00B92AA1 mov     eax, [ecx]
00B92AA3 mov     edx, [eax+78h]
00B92AA6 push    0Ah
00B92AA8 call    edx
00B92AAA mov     ebp, eax
00B92AAC mov     eax, [edi+0Ch]
00B92AAF push    eax
00B92AB0 lea     ecx, [esp+44h+var_2C]
00B92AB4 call    sub_ABB2F0
00B92AB9 lea     ecx, [ebp+0Ah]
00B92ABC lea     eax, [ebp+2]
00B92ABF cmp     eax, ecx
00B92AC9 ja      loc_B92C31
00B92ACF lea     edx, [eax+4]
00B92AD2 cmp     edx, ecx
00B92AD4 mov     word ptr [ebp+0], 16AEh
00B92ADA ja      loc_B92C31
00B92AE0 mov     esi, [esp+40h+arg_0]
00B92AE4 lea     ebx, [edx+4]
00B92AE7 cmp     ebx, ecx
00B92AE9 mov     [eax], esi
00B92AEB ja      loc_B92C31
00B92AF1 mov     ecx, [esp+40h+arg_4]
00B92AF5 mov     [edx], ecx
00B92AF7 mov     esi, [edi+7CBCh]
00B92AFD test    esi, esi
00B92AFF jz      loc_B92BD2
00B92B05 lea     edx, [esp+40h+var_28]
00B92B09 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B92BD2 mov     edx, [edi]
00B92BD4 mov     eax, [edx+58h]
00B92BD7 sub     ebx, ebp
00B92BD9 push    ebx
00B92BDA push    ebp
00B92BDB mov     ecx, edi
00B92BDD call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb92ad4` | opcode 写入/分发指令 |
| `channel_id` | `0xB92AE9` | u32 |
| `party_id` | `0xB92AF5` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEB278
00EE2018
00EE31A8
```
