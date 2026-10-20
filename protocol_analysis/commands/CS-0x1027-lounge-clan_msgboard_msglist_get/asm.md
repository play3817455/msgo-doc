# 汇编证据 —— CS-0x1027-clan_msgboard_msglist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA1DE0 @ `0xba1de0`（`0xba1de0`..`0xba1fc8`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_msgboard_msglist_get( ` @ `0xeecb4c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA1E10 jz      loc_BA1FC4
00BA1E16 mov     ecx, [esi+0Ch]
00BA1E19 test    ecx, ecx
00BA1E1B jz      loc_BA1FC4
00BA1E21 mov     eax, [ecx]
00BA1E23 mov     edx, [eax+78h]
00BA1E26 push    0Ah
00BA1E28 call    edx
00BA1E2A mov     ebp, eax
00BA1E2C mov     eax, [esi+0Ch]
00BA1E2F push    eax
00BA1E30 lea     ecx, [esp+44h+var_2C]
00BA1E34 call    sub_ABB2F0
00BA1E39 lea     eax, [ebp+0Ah]
00BA1E3C lea     ecx, [ebp+2]
00BA1E3F cmp     ecx, eax
00BA1E49 ja      loc_BA1FB3
00BA1E4F lea     edx, [ecx+4]
00BA1E52 cmp     edx, eax
00BA1E54 mov     word ptr [ebp+0], 1027h
00BA1E5A ja      loc_BA1FB3
00BA1E60 mov     edi, dword ptr [esp+40h+arg_0]
00BA1E64 lea     ebx, [edx+1]
00BA1E67 cmp     ebx, eax
00BA1E69 mov     [ecx], edi
00BA1E6B ja      loc_BA1FB3
00BA1E71 mov     cl, [esp+40h+arg_4]
00BA1E75 mov     [edx], cl
00BA1E77 mov     edi, [esi+8104h]
00BA1E7D test    edi, edi
00BA1E7F jz      loc_BA1F54
00BA1E85 lea     edx, [esp+40h+var_28]
00BA1E89 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA1F54 mov     edx, [esi]
00BA1F56 mov     eax, [edx+58h]
00BA1F59 sub     ebx, ebp
00BA1F5B push    ebx
00BA1F5C push    ebp
00BA1F5D mov     ecx, esi
00BA1F5F call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba1e54` | opcode 写入/分发指令 |
| `last_get` | `0xBA1E69` | u32 |
| `clan_kind` | `0xBA1E75` | u8 |

## 5. 块内字符串常量（含义取证用）

```
00EECB4C
00EE4170
00EE3398
```
