# 汇编证据 —— CS-0x048E-clan_mshipbid_get_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA00B0 @ `0xba00b0`（`0xba00b0`..`0xba025e`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_mshipbid_get_list( ` @ `0xeec864`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA00E0 jz      loc_BA025A
00BA00E6 mov     ecx, [esi+0Ch]
00BA00E9 test    ecx, ecx
00BA00EB jz      loc_BA025A
00BA00F1 mov     eax, [ecx]
00BA00F3 mov     edx, [eax+78h]
00BA00F6 push    6
00BA00F8 call    edx
00BA00FA mov     edi, eax
00BA00FC mov     eax, [esi+0Ch]
00BA00FF push    eax
00BA0100 lea     ecx, [esp+44h+var_2C]
00BA0104 call    sub_ABB2F0
00BA0109 lea     ecx, [edi+6]
00BA010C lea     eax, [edi+2]
00BA010F cmp     eax, ecx
00BA0119 ja      loc_BA0249
00BA011F lea     ebx, [eax+1]
00BA0122 cmp     ebx, ecx
00BA0124 mov     word ptr [edi], 48Eh
00BA0129 ja      loc_BA0249
00BA012F mov     cl, [esp+40h+arg_0]
00BA0133 mov     [eax], cl
00BA0135 mov     ebp, [esi+8090h]
00BA013B test    ebp, ebp
00BA013D jz      loc_BA01EA
00BA0143 lea     edx, [esp+40h+var_28]
00BA0147 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA01EA mov     edx, [esi]
00BA01EC mov     eax, [edx+58h]
00BA01EF sub     ebx, edi
00BA01F1 push    ebx
00BA01F2 push    edi
00BA01F3 mov     ecx, esi
00BA01F5 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba0124` | opcode 写入/分发指令 |
| `clan_kind` | `0xBA0133` | u8 |

## 5. 块内字符串常量（含义取证用）

```
00EEC864
00EE3398
```
