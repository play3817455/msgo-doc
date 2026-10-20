# 汇编证据 —— CS-0x0519-msma_equip_bonus_modules_lot_draw

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B93E70 @ `0xb93e70`（`0xb93e70`..`0xb94029`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_bonus_modules_lot_draw( ` @ `0xeeb4b8`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B93EA0 jz      loc_B94025
00B93EA6 mov     ecx, [esi+0Ch]
00B93EA9 test    ecx, ecx
00B93EAB jz      loc_B94025
00B93EB1 mov     eax, [ecx]
00B93EB3 mov     edx, [eax+78h]
00B93EB6 push    0Ah
00B93EB8 call    edx
00B93EBA mov     ebp, eax
00B93EBC mov     eax, [esi+0Ch]
00B93EBF push    eax
00B93EC0 lea     ecx, [esp+44h+var_2C]
00B93EC4 call    sub_ABB2F0
00B93EC9 lea     ecx, [ebp+0Ah]
00B93ECC lea     eax, [ebp+2]
00B93ECF cmp     eax, ecx
00B93ED9 ja      loc_B94014
00B93EDF lea     ebx, [eax+8]
00B93EE2 cmp     ebx, ecx
00B93EE4 mov     word ptr [ebp+0], 519h
00B93EEA ja      loc_B94014
00B93EF0 mov     ecx, [esp+40h+arg_0]
00B93EF4 mov     edx, [esp+40h+arg_4]
00B93EF8 mov     [eax], ecx
00B93EFA mov     [eax+4], edx
00B93EFD mov     edi, [esi+7D38h]
00B93F03 test    edi, edi
00B93F05 jz      loc_B93FB5
00B93F0B lea     eax, [esp+40h+var_28]
00B93F0F push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B93FB5 mov     edx, [esi]
00B93FB7 mov     eax, [edx+58h]
00B93FBA sub     ebx, ebp
00B93FBC push    ebx
00B93FBD push    ebp
00B93FBE mov     ecx, esi
00B93FC0 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb93ee4` | opcode 写入/分发指令 |
| `uniqid_ms` | `0xB93EF8,0xB93EFA` | u64 |

## 5. 块内字符串常量（含义取证用）

```
00EEB4B8
00EE41BC
```
