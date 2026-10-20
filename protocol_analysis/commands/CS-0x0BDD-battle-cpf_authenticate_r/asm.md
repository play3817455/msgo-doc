# 汇编证据 —— CS-0x0BDD-cpf_authenticate_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40520 @ `0xb40520`（`0xb40520`..`0xb40763`）
- 命令名字符串：`)<-_proto_battle_client::send_cpf_authenticate_r( ` @ `0xee184c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B40556 mov     ecx, [ebx+0Ch]
00B40559 test    ecx, ecx
00B4055B jz      loc_B4075F
00B40561 mov     eax, [ecx]
00B40563 mov     edx, [eax+78h]
00B40566 push    86h
00B4056B call    edx
00B4056D mov     esi, eax
00B4056F mov     eax, [ebx+0Ch]
00B40572 push    eax
00B40573 lea     ecx, [esp+50h+var_38]
00B40577 mov     [esp+50h+var_34], esi
00B4057B call    sub_ABB2F0
00B40580 lea     ecx, [esi+86h]
00B40586 lea     eax, [esi+2]
00B40589 cmp     eax, ecx
00B40593 ja      loc_B4074E
00B40599 mov     ebp, [esp+4Ch+arg_4]
00B4059D cmp     ebp, 80h
00B405A3 mov     word ptr [esi], 0BDDh
00B405A8 ja      loc_B4074E
00B405AE lea     esi, [eax+4]
00B405B1 cmp     esi, ecx
00B405B3 ja      loc_B4074E
00B405B9 mov     [eax], ebp
00B405BB xor     eax, eax
00B405BD test    ebp, ebp
00B405BF mov     [esp+4Ch+var_30], esi
00B405C3 jbe     short loc_B405EA
00B405C5 lea     edi, [esi+1]
00B405C8 cmp     edi, ecx
00B405CA ja      loc_B4074A
00B405D0 mov     edx, [esp+4Ch+arg_0]
00B405D4 mov     dl, [eax+edx]
00B405D7 mov     [esi], dl
00B405D9 add     eax, 1
00B405DC add     esi, 1
00B405DF add     edi, 1
00B405E2 cmp     eax, ebp
00B405E4 jb      short loc_B405C8
00B405E6 mov     [esp+4Ch+var_30], esi
00B405EA mov     edi, [ebx+4068h]
00B405F0 test    edi, edi
00B405F2 jz      loc_B406E7
00B405F8 lea     eax, [esp+4Ch+var_28]
00B405FC push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B406EB mov     edx, [ebx]
00B406ED mov     eax, [edx+58h]
00B406F0 sub     esi, edi
00B406F2 push    esi
00B406F3 push    edi
00B406F4 mov     ecx, ebx
00B406F6 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb405a3` | opcode 写入/分发指令 |
| `data_len` | `0xB405B9` | u32 |
| `data` | `0xB405D7` | bytes |

## 5. 块内字符串常量（含义取证用）

```
00B405C8
00EE184C
00EDC7C0
00B40697
00B40672
00EDABE4
```
