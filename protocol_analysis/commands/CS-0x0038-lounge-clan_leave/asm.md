# 汇编证据 —— CS-0x0038-clan_leave

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9FAD0 @ `0xb9fad0`（`0xb9fad0`..`0xb9fd0e`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_leave( ` @ `0xeec7c0`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9FB00 jz      loc_B9FD0A
00B9FB06 mov     ecx, [edi+0Ch]
00B9FB09 test    ecx, ecx
00B9FB0B jz      loc_B9FD0A
00B9FB11 mov     eax, [ecx]
00B9FB13 mov     edx, [eax+78h]
00B9FB16 push    0Eh
00B9FB18 call    edx
00B9FB1A mov     ebp, eax
00B9FB1C mov     eax, [edi+0Ch]
00B9FB1F push    eax
00B9FB20 lea     ecx, [esp+4Ch+var_34]
00B9FB24 call    sub_ABB2F0
00B9FB29 lea     eax, [ebp+0Eh]
00B9FB2C lea     ecx, [ebp+2]
00B9FB2F cmp     ecx, eax
00B9FB39 mov     [esp+48h+var_30], ebp
00B9FB3D mov     dword ptr [esp+48h+var_2C], eax
00B9FB41 ja      loc_B9FCF9
00B9FB47 lea     edx, [ecx+4]
00B9FB4A cmp     edx, eax
00B9FB4C mov     word ptr [ebp+0], 38h
00B9FB52 ja      loc_B9FCF9
00B9FB58 mov     esi, [esp+48h+arg_0]
00B9FB5C mov     [ecx], esi
00B9FB5E lea     ecx, [edx+1]
00B9FB61 cmp     ecx, eax
00B9FB63 ja      loc_B9FCF9
00B9FB69 mov     al, [esp+48h+arg_4]
00B9FB6D mov     [esp+48h+var_30], ecx
00B9FB71 lea     ecx, [esp+48h+var_30]
00B9FB75 mov     [edx], al
00B9FB77 push    ecx
00B9FB78 lea     edx, [esp+4Ch+arg_8]
00B9FB7C push    edx
00B9FB7D call    sub_B061C0
00B9FB85 test    al, al
00B9FB87 jz      loc_B9FCF9
00B9FB8D mov     esi, [edi+8070h]
00B9FB93 test    esi, esi
00B9FB95 mov     ebx, [esp+48h+var_30]
00B9FB99 jz      loc_B9FC98
00B9FB9F lea     eax, [esp+48h+var_28]
00B9FBA3 push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9FC98 mov     eax, [edi]
00B9FC9A mov     edx, [eax+58h]
00B9FC9D mov     esi, ebx
00B9FC9F sub     esi, ebp
00B9FCA1 push    esi
00B9FCA2 push    ebp
00B9FCA3 mov     ecx, edi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb9fb4c` | opcode 写入/分发指令 |
| `clan_id` | `0xB9FB5C` | u32 |
| `clan_kind` | `0xB9FB75` | u8 |
| `is_GMtool` | `0xB9FB7D` | u8 |

## 5. 块内字符串常量（含义取证用）

```
00EEC7C0
00EDB2C8
00EE3398
00EE41C8
```
