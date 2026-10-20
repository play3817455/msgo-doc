# 汇编证据 —— CS-0x1F3E-party_enter

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B92160 @ `0xb92160`（`0xb92160`..`0xb9230d`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_enter( ` @ `0xeeb184`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B92190 jz      loc_B92309
00B92196 mov     ecx, [esi+0Ch]
00B92199 test    ecx, ecx
00B9219B jz      loc_B92309
00B921A1 mov     eax, [ecx]
00B921A3 mov     edx, [eax+78h]
00B921A6 push    6
00B921A8 call    edx
00B921AA mov     ebp, eax
00B921AC mov     eax, [esi+0Ch]
00B921AF push    eax
00B921B0 lea     ecx, [esp+44h+var_2C]
00B921B4 call    sub_ABB2F0
00B921B9 lea     ecx, [ebp+6]
00B921BC lea     eax, [ebp+2]
00B921BF cmp     eax, ecx
00B921C9 ja      loc_B922F8
00B921CF lea     ebx, [eax+4]
00B921D2 cmp     ebx, ecx
00B921D4 mov     word ptr [ebp+0], 1F3Eh
00B921DA ja      loc_B922F8
00B921E0 mov     ecx, [esp+40h+arg_0]
00B921E4 mov     [eax], ecx
00B921E6 mov     edi, [esi+7C84h]
00B921EC test    edi, edi
00B921EE jz      loc_B92299
00B921F4 lea     edx, [esp+40h+var_28]
00B921F8 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B92299 mov     edx, [esi]
00B9229B mov     eax, [edx+58h]
00B9229E sub     ebx, ebp
00B922A0 push    ebx
00B922A1 push    ebp
00B922A2 mov     ecx, esi
00B922A4 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb921d4` | opcode 写入/分发指令 |
| `party_id` | `0xB921E4` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEB184
00EE31A8
```
