# 汇编证据 —— CS-0x1AD9-msma_equip_bonus_modules_update

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B93C50 @ `0xb93c50`（`0xb93c50`..`0xb93e70`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_bonus_modules_update( ` @ `0xeeb478`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B93C80 jz      loc_B93E6C
00B93C86 mov     ecx, [ebp+0Ch]
00B93C89 test    ecx, ecx
00B93C8B jz      loc_B93E6C
00B93C91 mov     eax, [ecx]
00B93C93 mov     edx, [eax+78h]
00B93C96 push    0Eh
00B93C98 call    edx
00B93C9A mov     ebx, eax
00B93C9C mov     eax, [ebp+0Ch]
00B93C9F push    eax
00B93CA0 lea     ecx, [esp+44h+var_2C]
00B93CA4 call    sub_ABB2F0
00B93CA9 lea     ecx, [ebx+0Eh]
00B93CAC lea     eax, [ebx+2]
00B93CAF cmp     eax, ecx
00B93CB9 ja      loc_B93E5B
00B93CBF lea     edi, [eax+8]
00B93CC2 cmp     edi, ecx
00B93CC4 mov     word ptr [ebx], 1AD9h
00B93CC9 ja      loc_B93E5B
00B93CCF mov     ecx, [esp+40h+arg_0]
00B93CD3 mov     edx, [esp+40h+arg_4]
00B93CD7 mov     [eax], ecx
00B93CD9 mov     [eax+4], edx
00B93CDC mov     edx, [esp+40h+arg_8]
00B93CE0 test    edx, edx
00B93CE2 jz      loc_B93E5B
00B93CE8 xor     eax, eax
00B93CEA lea     ecx, [edi+4]
00B93CED lea     ecx, [ecx+0]
00B93CF0 lea     esi, [ebx+0Eh]
00B93CF3 cmp     ecx, esi
00B93CF5 ja      loc_B93E5B
00B93CFB mov     esi, [edx+eax*4]
00B93CFE mov     [edi], esi
00B93D00 add     eax, 1
00B93D03 add     edi, 4
00B93D06 add     ecx, 4
00B93D09 cmp     eax, 1
00B93D0C jb      short loc_B93CF0
00B93D0E mov     esi, [ebp+7D28h]
00B93D14 test    esi, esi
00B93D16 jz      loc_B93DFB
00B93D1C lea     eax, [esp+40h+var_28]
00B93D20 push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B93DFB mov     edx, [ebp+0]
00B93DFE mov     eax, [edx+58h]
00B93E01 sub     edi, ebx
00B93E03 push    edi
00B93E04 push    ebx
00B93E05 mov     ecx, ebp
00B93E07 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb93cc4` | opcode 写入/分发指令 |
| `uniqid_ms` | `0xB93CD7,0xB93CD9` | u64 |
| `eq_bonus_modules` | `0xB93CFB` | array<u32,1> |

## 5. 块内字符串常量（含义取证用）

```
00EEB478
00EE41BC
00EDB540
00EDABE4
```
