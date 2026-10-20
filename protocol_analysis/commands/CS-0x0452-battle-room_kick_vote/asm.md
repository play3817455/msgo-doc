# 汇编证据 —— CS-0x0452-room_kick_vote

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B332B0 @ `0xb332b0`（`0xb332b0`..`0xb334e7`）
- 命令名字符串：`)<-_proto_battle_client::send_room_kick_vote( ` @ `0xee083c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B332E0 jz      loc_B334E3
00B332E6 mov     ecx, [edi+0Ch]
00B332E9 test    ecx, ecx
00B332EB jz      loc_B334E3
00B332F1 mov     eax, [ecx]
00B332F3 mov     edx, [eax+78h]
00B332F6 push    0Eh
00B332F8 call    edx
00B332FA mov     ebp, eax
00B332FC mov     eax, [edi+0Ch]
00B332FF push    eax
00B33300 lea     ecx, [esp+4Ch+var_34]
00B33304 call    sub_ABB2F0
00B33309 lea     ecx, [ebp+0Eh]
00B3330C lea     eax, [ebp+2]
00B3330F cmp     eax, ecx
00B33319 mov     [esp+48h+var_30], ebp
00B3331D mov     dword ptr [esp+48h+var_2C], ecx
00B33321 ja      loc_B334D2
00B33327 lea     edx, [eax+4]
00B3332A cmp     edx, ecx
00B3332C mov     word ptr [ebp+0], 452h
00B33332 ja      loc_B334D2
00B33338 mov     esi, [esp+48h+arg_0]
00B3333C mov     [eax], esi
00B3333E mov     eax, edx
00B33340 lea     edx, [eax+4]
00B33343 cmp     edx, ecx
00B33345 ja      loc_B334D2
00B3334B mov     ecx, [esp+48h+arg_4]
00B3334F mov     [esp+48h+var_30], edx
00B33353 lea     edx, [esp+48h+var_30]
00B33357 mov     [eax], ecx
00B33359 push    edx
00B3335A lea     eax, [esp+4Ch+arg_8]
00B3335E push    eax
00B3335F call    sub_B02D80
00B33367 test    al, al
00B33369 jz      loc_B334D2
00B3336F mov     esi, [edi+3CB0h]
00B33375 test    esi, esi
00B33377 mov     ebx, [esp+48h+var_30]
00B3337B jz      loc_B33476
00B33381 lea     ecx, [esp+48h+var_28]
00B33385 push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B33476 mov     edx, [edi]
00B33478 mov     eax, [edx+58h]
00B3347B sub     ebx, ebp
00B3347D push    ebx
00B3347E push    ebp
00B3347F mov     ecx, edi
00B33481 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb3332c` | opcode 写入/分发指令 |
| `target_world_id` | `0xB3333C` | u32 |
| `target_pilot_id` | `0xB33357` | u32 |
| `kick_reason` | `0xB3335F` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EE083C
00EDC8A0
00EDC88C
00EDC87C
```
