# 汇编证据 —— CS-0x03F7-ban_transform

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40960 @ `0xb40960`（`0xb40960`..`0xb40b46`）
- 命令名字符串：`)<-_proto_battle_client::send_ban_transform( ` @ `0xee18b0`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B40990 jz      loc_B40B42
00B40996 mov     ecx, [edi+0Ch]
00B40999 test    ecx, ecx
00B4099B jz      loc_B40B42
00B409A1 mov     eax, [ecx]
00B409A3 mov     edx, [eax+78h]
00B409A6 push    0Ah
00B409A8 call    edx
00B409AA mov     ebp, eax
00B409AC mov     eax, [edi+0Ch]
00B409AF push    eax
00B409B0 lea     ecx, [esp+44h+var_2C]
00B409B4 call    sub_ABB2F0
00B409B9 lea     ecx, [ebp+0Ah]
00B409BC lea     eax, [ebp+2]
00B409BF cmp     eax, ecx
00B409C9 ja      loc_B40B31
00B409CF lea     edx, [eax+4]
00B409D2 cmp     edx, ecx
00B409D4 mov     word ptr [ebp+0], 3F7h
00B409DA ja      loc_B40B31
00B409E0 mov     esi, [esp+40h+arg_0]
00B409E4 lea     ebx, [edx+4]
00B409E7 cmp     ebx, ecx
00B409E9 mov     [eax], esi
00B409EB ja      loc_B40B31
00B409F1 mov     ecx, [esp+40h+arg_4]
00B409F5 mov     [edx], ecx
00B409F7 mov     esi, [edi+4084h]
00B409FD test    esi, esi
00B409FF jz      loc_B40AD2
00B40A05 lea     edx, [esp+40h+var_28]
00B40A09 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B40AD2 mov     edx, [edi]
00B40AD4 mov     eax, [edx+58h]
00B40AD7 sub     ebx, ebp
00B40AD9 push    ebx
00B40ADA push    ebp
00B40ADB mov     ecx, edi
00B40ADD call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb409d4` | opcode 写入/分发指令 |
| `ent_id` | `0xB409E9` | u32 |
| `val` | `0xB409F5` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EE18B0
00EDB98C
00EDB88C
```
