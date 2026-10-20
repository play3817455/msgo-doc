# 汇编证据 —— CS-0x002A-chat_dcteam_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8D7F0 @ `0xb8d7f0`（`0xb8d7f0`..`0xb8d9cf`）
- 命令名字符串：`)<-_proto_lounge_client::send_chat_dcteam_up( ` @ `0xeea950`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8D820 jz      loc_B8D9CB
00B8D826 mov     ecx, [esi+0Ch]
00B8D829 test    ecx, ecx
00B8D82B jz      loc_B8D9CB
00B8D831 mov     eax, [ecx]
00B8D833 mov     edx, [eax+78h]
00B8D836 push    0BAh
00B8D83B call    edx
00B8D83D mov     edi, eax
00B8D83F mov     eax, [esi+0Ch]
00B8D842 push    eax
00B8D843 lea     ecx, [esp+4Ch+var_34]
00B8D847 call    sub_ABB2F0
00B8D84C lea     ecx, [edi+0BAh]
00B8D852 lea     eax, [edi+2]
00B8D855 cmp     eax, ecx
00B8D85F mov     [esp+48h+var_30], edi
00B8D863 mov     dword ptr [esp+48h+var_2C], ecx
00B8D867 ja      loc_B8D9BA
00B8D86D mov     edx, [esp+48h+arg_0]
00B8D871 push    0B5h
00B8D876 lea     ecx, [esp+4Ch+var_30]
00B8D87A push    ecx
00B8D87B push    edx
00B8D87C mov     word ptr [edi], 2Ah
00B8D881 mov     [esp+54h+var_30], eax
00B8D885 call    sub_B02B40
00B8D88D test    al, al
00B8D88F jz      loc_B8D9BA
00B8D895 mov     ebp, [esi+7B08h]
00B8D89B test    ebp, ebp
00B8D89D mov     ebx, [esp+48h+var_30]
00B8D8A1 jz      loc_B8D95C
00B8D8A7 lea     eax, [esp+48h+var_28]
00B8D8AB push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8D95C mov     edx, [esi]
00B8D95E mov     eax, [edx+58h]
00B8D961 mov     ebp, ebx
00B8D963 sub     ebp, edi
00B8D965 push    ebp
00B8D966 push    edi
00B8D967 mov     ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb8d87c` | opcode 写入/分发指令 |
| `msg` | `0xB8D885` | str |

## 5. 块内字符串常量（含义取证用）

```
00EEA950
00EDC7B8
```
