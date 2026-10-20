# 汇编证据 —— CS-0x0AA5-msma_equip_weapon_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B933B0 @ `0xb933b0`（`0xb933b0`..`0xb935f6`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_weapon_change( ` @ `0xeeb388`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B933E0 jz      loc_B935F2
00B933E6 mov     ecx, [edi+0Ch]
00B933E9 test    ecx, ecx
00B933EB jz      loc_B935F2
00B933F1 mov     eax, [ecx]
00B933F3 mov     edx, [eax+78h]
00B933F6 push    12h
00B933F8 call    edx
00B933FA mov     ebp, eax
00B933FC mov     eax, [edi+0Ch]
00B933FF push    eax
00B93400 lea     ecx, [esp+4Ch+var_34]
00B93404 call    sub_ABB2F0
00B93409 lea     ecx, [ebp+12h]
00B9340C lea     eax, [ebp+2]
00B9340F cmp     eax, ecx
00B93419 mov     [esp+48h+var_30], ebp
00B9341D mov     dword ptr [esp+48h+var_2C], ecx
00B93421 ja      loc_B935E1
00B93427 lea     edx, [eax+8]
00B9342A cmp     edx, ecx
00B9342C mov     word ptr [ebp+0], 0AA5h
00B93432 ja      loc_B935E1
00B93438 mov     esi, [esp+48h+arg_0]
00B9343C mov     [eax], esi
00B9343E mov     esi, [esp+48h+arg_4]
00B93442 mov     [eax+4], esi
00B93445 lea     eax, [edx+2]
00B93448 cmp     eax, ecx
00B9344A ja      loc_B935E1
00B93450 mov     cx, word ptr [esp+48h+arg_8]
00B93455 mov     [edx], cx
00B93458 lea     edx, [esp+48h+var_30]
00B9345C mov     [esp+48h+var_30], eax
00B93460 push    edx
00B93461 lea     eax, [esp+4Ch+arg_C]
00B93465 push    eax
00B93466 call    sub_B02D80
00B9346E test    al, al
00B93470 jz      loc_B935E1
00B93476 mov     esi, [edi+7D00h]
00B9347C test    esi, esi
00B9347E mov     ebx, [esp+48h+var_30]
00B93482 jz      loc_B93582
00B93488 lea     ecx, [esp+48h+var_28]
00B9348C push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B93582 mov     edx, [edi]
00B93584 mov     eax, [edx+58h]
00B93587 sub     ebx, ebp
00B93589 push    ebx
00B9358A push    ebp
00B9358B mov     ecx, edi
00B9358D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb9342c` | opcode 写入/分发指令 |
| `uniqid_ms` | `0xB9343C,0xB93442` | u64 |
| `eq_slot` | `0xB93455` | u16 |
| `item_id` | `0xB93466` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEB388
00EE41BC
00EE4188
00EDB448
```
