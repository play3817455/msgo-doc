# 汇编证据 —— CS-0x085F-check_progress_quest

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40390 @ `0xb40390`（`0xb40390`..`0xb40516`）
- 命令名字符串：`)<-_proto_battle_client::send_check_progress_quest( ` @ `0xee1814`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B403C0 jz      loc_B404B4
00B403C6 mov     ecx, [esi+0Ch]
00B403C9 test    ecx, ecx
00B403CB jz      loc_B404B4
00B403D1 mov     eax, [ecx]
00B403D3 mov     edx, [eax+78h]
00B403D6 push    2
00B403D8 call    edx
00B403DA mov     edi, eax
00B403DC mov     eax, [esi+0Ch]
00B403DF push    eax
00B403E0 lea     ecx, [esp+44h+var_2C]
00B403E4 call    sub_ABB2F0
00B403E9 mov     word ptr [edi], 85Fh
00B403EE mov     ebp, [esi+4048h]
00B403F4 test    ebp, ebp
00B403FE lea     ebx, [edi+2]
00B40401 jz      loc_B40492
00B40407 lea     ecx, [esp+40h+var_28]
00B4040B push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B40492 mov     edx, [esi]
00B40494 mov     eax, [edx+58h]
00B40497 sub     ebx, edi
00B40499 push    ebx
00B4049A push    edi
00B4049B mov     ecx, esi
00B4049D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb403e9` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EE1814
```
