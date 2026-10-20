# 汇编证据 —— CS-0x0372-game_mission_progress_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B33C10 @ `0xb33c10`（`0xb33c10`..`0xb33d93`）
- 命令名字符串：`)<-_proto_battle_client::send_game_mission_progress_get( ` @ `0xee0950`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B33C40 jz      loc_B33D34
00B33C46 mov     ecx, [esi+0Ch]
00B33C49 test    ecx, ecx
00B33C4B jz      loc_B33D34
00B33C51 mov     eax, [ecx]
00B33C53 mov     edx, [eax+78h]
00B33C56 push    2
00B33C58 call    edx
00B33C5A mov     edi, eax
00B33C5C mov     eax, [esi+0Ch]
00B33C5F push    eax
00B33C60 lea     ecx, [esp+44h+var_2C]
00B33C64 call    sub_ABB2F0
00B33C69 mov     word ptr [edi], 372h
00B33C6E mov     ebp, [esi+3CF4h]
00B33C74 test    ebp, ebp
00B33C7E lea     ebx, [edi+2]
00B33C81 jz      loc_B33D12
00B33C87 lea     ecx, [esp+40h+var_28]
00B33C8B push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B33D12 mov     edx, [esi]
00B33D14 mov     eax, [edx+58h]
00B33D17 sub     ebx, edi
00B33D19 push    ebx
00B33D1A push    edi
00B33D1B mov     ecx, esi
00B33D1D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb33c69` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EE0950
```
