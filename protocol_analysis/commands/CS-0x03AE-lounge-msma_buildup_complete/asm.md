# 汇编证据 —— CS-0x03AE-msma_buildup_complete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B967E0 @ `0xb967e0`（`0xb967e0`..`0xb96a66`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_buildup_complete( ` @ `0xeeb8f8`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B96810 jz      loc_B96A62
00B96816 mov     ecx, [edi+0Ch]
00B96819 test    ecx, ecx
00B9681B jz      loc_B96A62
00B96821 mov     eax, [ecx]
00B96823 mov     edx, [eax+78h]
00B96826 push    16h
00B96828 call    edx
00B9682A mov     ebp, eax
00B9682C mov     eax, [edi+0Ch]
00B9682F push    eax
00B96830 lea     ecx, [esp+4Ch+var_34]
00B96834 call    sub_ABB2F0
00B96839 lea     ecx, [ebp+16h]
00B9683C lea     eax, [ebp+2]
00B9683F cmp     eax, ecx
00B96849 mov     [esp+48h+var_30], ebp
00B9684D mov     dword ptr [esp+48h+var_2C], ecx
00B96851 ja      loc_B96A51
00B96857 lea     edx, [eax+8]
00B9685A cmp     edx, ecx
00B9685C mov     word ptr [ebp+0], 3AEh
00B96862 ja      loc_B96A51
00B96868 mov     esi, [esp+48h+arg_0]
00B9686C mov     [eax], esi
00B9686E mov     esi, [esp+48h+arg_4]
00B96872 mov     [eax+4], esi
00B96875 lea     eax, [edx+4]
00B96878 cmp     eax, ecx
00B9687A ja      loc_B96A51
00B96880 mov     ecx, [esp+48h+arg_8]
00B96884 mov     [edx], ecx
00B96886 lea     edx, [esp+48h+var_30]
00B9688A mov     [esp+48h+var_30], eax
00B9688E push    edx
00B9688F lea     eax, [esp+4Ch+arg_C]
00B96893 push    eax
00B96894 call    sub_B02DA0
00B9689C test    al, al
00B9689E jz      loc_B96A51
00B968A4 lea     ecx, [esp+48h+var_30]
00B968A8 push    ecx
00B968A9 lea     edx, [esp+4Ch+arg_10]
00B968AD push    edx
00B968AE call    sub_B02DA0
00B968B6 test    al, al
00B968B8 jz      loc_B96A51
00B968BE mov     esi, [edi+7DDCh]
00B968C4 test    esi, esi
00B968C6 mov     ebx, [esp+48h+var_30]
00B968CA jz      loc_B969F2
00B968D0 lea     eax, [esp+48h+var_28]
00B968D4 push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B969F2 mov     edx, [edi]
00B969F4 mov     eax, [edx+58h]
00B969F7 sub     ebx, ebp
00B969F9 push    ebx
00B969FA push    ebp
00B969FB mov     ecx, edi
00B969FD call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb9685c` | opcode 写入/分发指令 |
| `uniqid_ms` | `0xB9686C,0xB96872` | u64 |
| `ticket_id` | `0xB96884` | u32 |
| `usenum` | `0xB96894` | u16 |
| `param_idx` | `0xB968AE` | u16 |

## 5. 块内字符串常量（含义取证用）

```
00EEB8F8
00EE41BC
00EE41B0
00EE41A8
00EE419C
```
