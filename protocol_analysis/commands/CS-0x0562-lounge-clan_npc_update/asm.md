# 汇编证据 —— CS-0x0562-clan_npc_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA0920 @ `0xba0920`（`0xba0920`..`0xba0acd`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_npc_update( ` @ `0xeec93c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA0950 jz      loc_BA0AC9
00BA0956 mov     ecx, [esi+0Ch]
00BA0959 test    ecx, ecx
00BA095B jz      loc_BA0AC9
00BA0961 mov     eax, [ecx]
00BA0963 mov     edx, [eax+78h]
00BA0966 push    6
00BA0968 call    edx
00BA096A mov     ebp, eax
00BA096C mov     eax, [esi+0Ch]
00BA096F push    eax
00BA0970 lea     ecx, [esp+44h+var_2C]
00BA0974 call    sub_ABB2F0
00BA0979 lea     ecx, [ebp+6]
00BA097C lea     eax, [ebp+2]
00BA097F cmp     eax, ecx
00BA0989 ja      loc_BA0AB8
00BA098F lea     ebx, [eax+4]
00BA0992 cmp     ebx, ecx
00BA0994 mov     word ptr [ebp+0], 562h
00BA099A ja      loc_BA0AB8
00BA09A0 mov     ecx, [esp+40h+arg_0]
00BA09A4 mov     [eax], ecx
00BA09A6 mov     edi, [esi+80B0h]
00BA09AC test    edi, edi
00BA09AE jz      loc_BA0A59
00BA09B4 lea     edx, [esp+40h+var_28]
00BA09B8 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA0A59 mov     edx, [esi]
00BA0A5B mov     eax, [edx+58h]
00BA0A5E sub     ebx, ebp
00BA0A60 push    ebx
00BA0A61 push    ebp
00BA0A62 mov     ecx, esi
00BA0A64 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba0994` | opcode 写入/分发指令 |
| `npc_id` | `0xBA09A4` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEC93C
00EE3390
```
