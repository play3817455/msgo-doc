# 汇编证据 —— CS-0x11AA-gacha_reset

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9E760 @ `0xb9e760`（`0xb9e760`..`0xb9e90d`）
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_reset( ` @ `0xeec590`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9E790 jz      loc_B9E909
00B9E796 mov     ecx, [esi+0Ch]
00B9E799 test    ecx, ecx
00B9E79B jz      loc_B9E909
00B9E7A1 mov     eax, [ecx]
00B9E7A3 mov     edx, [eax+78h]
00B9E7A6 push    6
00B9E7A8 call    edx
00B9E7AA mov     ebp, eax
00B9E7AC mov     eax, [esi+0Ch]
00B9E7AF push    eax
00B9E7B0 lea     ecx, [esp+44h+var_2C]
00B9E7B4 call    sub_ABB2F0
00B9E7B9 lea     ecx, [ebp+6]
00B9E7BC lea     eax, [ebp+2]
00B9E7BF cmp     eax, ecx
00B9E7C9 ja      loc_B9E8F8
00B9E7CF lea     ebx, [eax+4]
00B9E7D2 cmp     ebx, ecx
00B9E7D4 mov     word ptr [ebp+0], 11AAh
00B9E7DA ja      loc_B9E8F8
00B9E7E0 mov     ecx, [esp+40h+arg_0]
00B9E7E4 mov     [eax], ecx
00B9E7E6 mov     edi, [esi+8008h]
00B9E7EC test    edi, edi
00B9E7EE jz      loc_B9E899
00B9E7F4 lea     edx, [esp+40h+var_28]
00B9E7F8 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9E899 mov     edx, [esi]
00B9E89B mov     eax, [edx+58h]
00B9E89E sub     ebx, ebp
00B9E8A0 push    ebx
00B9E8A1 push    ebp
00B9E8A2 mov     ecx, esi
00B9E8A4 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb9e7d4` | opcode 写入/分发指令 |
| `gacha_id` | `0xB9E7E4` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEC590
00EE373C
```
