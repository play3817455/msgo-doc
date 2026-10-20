# 汇编证据 —— CS-0x16BD-chat_whisper_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8D3D0 @ `0xb8d3d0`（`0xb8d3d0`..`0xb8d602`）
- 命令名字符串：`)<-_proto_lounge_client::send_chat_whisper_up( ` @ `0xeea8f0`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B8D400 jz      loc_B8D5FE
00B8D406 mov     ecx, [edi+0Ch]
00B8D409 test    ecx, ecx
00B8D40B jz      loc_B8D5FE
00B8D411 mov     eax, [ecx]
00B8D413 mov     edx, [eax+78h]
00B8D416 push    0D6h
00B8D41B call    edx
00B8D41D mov     ebp, eax
00B8D41F mov     eax, [edi+0Ch]
00B8D422 push    eax
00B8D423 lea     ecx, [esp+4Ch+var_34]
00B8D427 call    sub_ABB2F0
00B8D42C lea     ecx, [ebp+0D6h]
00B8D432 lea     eax, [ebp+2]
00B8D435 cmp     eax, ecx
00B8D43F mov     [esp+48h+var_30], ebp
00B8D443 mov     dword ptr [esp+48h+var_2C], ecx
00B8D447 ja      loc_B8D5ED
00B8D44D mov     edx, [esp+48h+arg_0]
00B8D451 push    19h
00B8D453 lea     ecx, [esp+4Ch+var_30]
00B8D457 push    ecx
00B8D458 push    edx
00B8D459 mov     word ptr [ebp+0], 16BDh
00B8D45F mov     [esp+54h+var_30], eax
00B8D463 call    sub_B02B40
00B8D46B test    al, al
00B8D46D jz      loc_B8D5ED
00B8D473 mov     ecx, [esp+48h+arg_4]
00B8D477 push    0B5h
00B8D47C lea     eax, [esp+4Ch+var_30]
00B8D480 push    eax
00B8D481 push    ecx
00B8D482 call    sub_B02B40
00B8D48A test    al, al
00B8D48C jz      loc_B8D5ED
00B8D492 mov     esi, [edi+7AF4h]
00B8D498 test    esi, esi
00B8D49A mov     ebx, [esp+48h+var_30]
00B8D49E jz      loc_B8D591
00B8D4A4 lea     edx, [esp+48h+var_28]
00B8D4A8 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B8D591 mov     edx, [edi]
00B8D593 mov     eax, [edx+58h]
00B8D596 sub     ebx, ebp
00B8D598 push    ebx
00B8D599 push    ebp
00B8D59A mov     ecx, edi
00B8D59C call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb8d459` | opcode 写入/分发指令 |
| `to_pilot_name` | `0xB8D463` | str |
| `msg` | `0xB8D482` | str |

## 5. 块内字符串常量（含义取证用）

```
00EEA8F0
00EE41E8
00EDC7B8
```
