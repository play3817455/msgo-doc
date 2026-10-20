# 汇编证据 —— CS-0x1C33-save_message

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40770 @ `0xb40770`（`0xb40770`..`0xb40952`）
- 命令名字符串：`)<-_proto_battle_client::send_save_message( ` @ `0xee1880`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B407A0 jz      loc_B4094E
00B407A6 mov     ecx, [esi+0Ch]
00B407A9 test    ecx, ecx
00B407AB jz      loc_B4094E
00B407B1 mov     eax, [ecx]
00B407B3 mov     edx, [eax+78h]
00B407B6 push    0BAh
00B407BB call    edx
00B407BD mov     edi, eax
00B407BF mov     eax, [esi+0Ch]
00B407C2 push    eax
00B407C3 lea     ecx, [esp+4Ch+var_34]
00B407C7 call    sub_ABB2F0
00B407CC lea     ecx, [edi+0BAh]
00B407D2 lea     eax, [edi+2]
00B407D5 cmp     eax, ecx
00B407DF mov     [esp+48h+var_30], edi
00B407E3 mov     dword ptr [esp+48h+var_2C], ecx
00B407E7 ja      loc_B4093D
00B407ED mov     edx, [esp+48h+arg_0]
00B407F1 push    0B5h
00B407F6 lea     ecx, [esp+4Ch+var_30]
00B407FA push    ecx
00B407FB push    edx
00B407FC mov     word ptr [edi], 1C33h
00B40801 mov     [esp+54h+var_30], eax
00B40805 call    sub_B02B40
00B4080D test    al, al
00B4080F jz      loc_B4093D
00B40815 mov     ebp, [esi+4078h]
00B4081B test    ebp, ebp
00B4081D mov     ebx, [esp+48h+var_30]
00B40821 jz      loc_B408DC
00B40827 lea     eax, [esp+48h+var_28]
00B4082B push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B408DC mov     edx, [esi]
00B408DE mov     eax, [edx+58h]
00B408E1 mov     ebp, ebx
00B408E3 sub     ebp, edi
00B408E5 push    ebp
00B408E6 push    edi
00B408E7 mov     ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb407fc` | opcode 写入/分发指令 |
| `msg` | `0xB40805` | str |

## 5. 块内字符串常量（含义取证用）

```
00EE1880
00EDC7B8
```
