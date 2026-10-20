# 汇编证据 —— CS-0x16DB-roomlobby_ban_vote

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B32630 @ `0xb32630`（`0xb32630`..`0xb327d7`）
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_ban_vote( ` @ `0xee06c4`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B3265D jz      loc_B327D3
00B32663 mov     ecx, [esi+0Ch]
00B32666 test    ecx, ecx
00B32668 jz      loc_B327D3
00B3266E mov     eax, [ecx]
00B32670 mov     edx, [eax+78h]
00B32673 push    6
00B32675 call    edx
00B32677 mov     ebp, eax
00B32679 mov     eax, [esi+0Ch]
00B3267C push    eax
00B3267D lea     ecx, [esp+44h+var_2C]
00B32681 call    sub_ABB2F0
00B32686 lea     ecx, [ebp+6]
00B32689 lea     eax, [ebp+2]
00B3268C cmp     eax, ecx
00B32696 ja      loc_B327C2
00B3269C lea     ebx, [eax+4]
00B3269F cmp     ebx, ecx
00B326A1 mov     word ptr [ebp+0], 16DBh
00B326A7 ja      loc_B327C2
00B326AD mov     ecx, [esp+40h+arg_0]
00B326B1 mov     [eax], ecx
00B326B3 mov     edi, [esi+3C58h]
00B326B9 test    edi, edi
00B326BB jz      loc_B32766
00B326C1 lea     edx, [esp+40h+var_28]
00B326C5 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B32766 mov     edx, [esi]
00B32768 mov     eax, [edx+58h]
00B3276B sub     ebx, ebp
00B3276D push    ebx
00B3276E push    ebp
00B3276F mov     ecx, esi
00B32771 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb326a1` | opcode 写入/分发指令 |
| `msma_id` | `0xB326B1` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EE06C4
00EDB6E8
```
