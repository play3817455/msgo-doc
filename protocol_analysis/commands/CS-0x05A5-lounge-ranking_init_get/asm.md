# 汇编证据 —— CS-0x05A5-ranking_init_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA34C0 @ `0xba34c0`（`0xba34c0`..`0xba3646`）
- 命令名字符串：`)<-_proto_lounge_client::send_ranking_init_get( ` @ `0xeecdc0`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA34F0 jz      loc_BA35E4
00BA34F6 mov     ecx, [esi+0Ch]
00BA34F9 test    ecx, ecx
00BA34FB jz      loc_BA35E4
00BA3501 mov     eax, [ecx]
00BA3503 mov     edx, [eax+78h]
00BA3506 push    2
00BA3508 call    edx
00BA350A mov     edi, eax
00BA350C mov     eax, [esi+0Ch]
00BA350F push    eax
00BA3510 lea     ecx, [esp+44h+var_2C]
00BA3514 call    sub_ABB2F0
00BA3519 mov     word ptr [edi], 5A5h
00BA351E mov     ebp, [esi+8168h]
00BA3524 test    ebp, ebp
00BA352E lea     ebx, [edi+2]
00BA3531 jz      loc_BA35C2
00BA3537 lea     ecx, [esp+40h+var_28]
00BA353B push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA35C2 mov     edx, [esi]
00BA35C4 mov     eax, [edx+58h]
00BA35C7 sub     ebx, edi
00BA35C9 push    ebx
00BA35CA push    edi
00BA35CB mov     ecx, esi
00BA35CD call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba3519` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EECDC0
```
