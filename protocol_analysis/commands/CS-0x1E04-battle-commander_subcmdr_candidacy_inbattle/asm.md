# 汇编证据 —— CS-0x1E04-commander_subcmdr_candidacy_inbattle

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3EE70 @ `0xb3ee70`（`0xb3ee70`..`0xb3eff6`）
- 命令名字符串：`)<-_proto_battle_client::send_commander_subcmdr_candidacy_inbattle( ` @ `0xee1578`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B3EEA0 jz      loc_B3EF94
00B3EEA6 mov     ecx, [esi+0Ch]
00B3EEA9 test    ecx, ecx
00B3EEAB jz      loc_B3EF94
00B3EEB1 mov     eax, [ecx]
00B3EEB3 mov     edx, [eax+78h]
00B3EEB6 push    2
00B3EEB8 call    edx
00B3EEBA mov     edi, eax
00B3EEBC mov     eax, [esi+0Ch]
00B3EEBF push    eax
00B3EEC0 lea     ecx, [esp+44h+var_2C]
00B3EEC4 call    sub_ABB2F0
00B3EEC9 mov     word ptr [edi], 1E04h
00B3EECE mov     ebp, [esi+3FB0h]
00B3EED4 test    ebp, ebp
00B3EEDE lea     ebx, [edi+2]
00B3EEE1 jz      loc_B3EF72
00B3EEE7 lea     ecx, [esp+40h+var_28]
00B3EEEB push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3EF72 mov     edx, [esi]
00B3EF74 mov     eax, [edx+58h]
00B3EF77 sub     ebx, edi
00B3EF79 push    ebx
00B3EF7A push    edi
00B3EF7B mov     ecx, esi
00B3EF7D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb3eec9` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EE1578
```
