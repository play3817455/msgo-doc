# 汇编证据 —— CS-0x045B-msma_AI_ping

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3CCB0 @ `0xb3ccb0`（`0xb3ccb0`..`0xb3ce5f`）
- 命令名字符串：`)<-_proto_battle_client::send_msma_AI_ping( ` @ `0xee1234`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B3CCE0 jz      loc_B3CE5B
00B3CCE6 mov     ecx, [esi+0Ch]
00B3CCE9 test    ecx, ecx
00B3CCEB jz      loc_B3CE5B
00B3CCF1 mov     eax, [ecx]
00B3CCF3 mov     edx, [eax+78h]
00B3CCF6 push    6
00B3CCF8 call    edx
00B3CCFA mov     ebp, eax
00B3CCFC mov     eax, [esi+0Ch]
00B3CCFF push    eax
00B3CD00 lea     ecx, [esp+44h+var_2C]
00B3CD04 call    sub_ABB2F0
00B3CD09 lea     ecx, [ebp+6]
00B3CD0C lea     eax, [ebp+2]
00B3CD0F cmp     eax, ecx
00B3CD19 ja      loc_B3CE4A
00B3CD1F lea     ebx, [eax+2]
00B3CD22 cmp     ebx, ecx
00B3CD24 mov     word ptr [ebp+0], 45Bh
00B3CD2A ja      loc_B3CE4A
00B3CD30 mov     cx, word ptr [esp+40h+arg_0]
00B3CD35 mov     [eax], cx
00B3CD38 mov     edi, [esi+3EE0h]
00B3CD3E test    edi, edi
00B3CD40 jz      loc_B3CDEB
00B3CD46 lea     edx, [esp+40h+var_28]
00B3CD4A push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B3CDEB mov     edx, [esi]
00B3CDED mov     eax, [edx+58h]
00B3CDF0 sub     ebx, ebp
00B3CDF2 push    ebx
00B3CDF3 push    ebp
00B3CDF4 mov     ecx, esi
00B3CDF6 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb3cd24` | opcode 写入/分发指令 |
| `AI_ent_id` | `0xB3CD35` | u16 |

## 5. 块内字符串常量（含义取证用）

```
00EE1234
00EDC870
```
