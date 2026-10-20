# 汇编证据 —— CS-0x17E0-season_class_up_reward_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA7980 @ `0xba7980`（`0xba7980`..`0xba7b06`）
- 命令名字符串：`)<-_proto_lounge_client::send_season_class_up_reward_get( ` @ `0xeed50c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA79B0 jz      loc_BA7AA4
00BA79B6 mov     ecx, [esi+0Ch]
00BA79B9 test    ecx, ecx
00BA79BB jz      loc_BA7AA4
00BA79C1 mov     eax, [ecx]
00BA79C3 mov     edx, [eax+78h]
00BA79C6 push    2
00BA79C8 call    edx
00BA79CA mov     edi, eax
00BA79CC mov     eax, [esi+0Ch]
00BA79CF push    eax
00BA79D0 lea     ecx, [esp+44h+var_2C]
00BA79D4 call    sub_ABB2F0
00BA79D9 mov     word ptr [edi], 17E0h
00BA79DE mov     ebp, [esi+82E8h]
00BA79E4 test    ebp, ebp
00BA79EE lea     ebx, [edi+2]
00BA79F1 jz      loc_BA7A82
00BA79F7 lea     ecx, [esp+40h+var_28]
00BA79FB push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA7A82 mov     edx, [esi]
00BA7A84 mov     eax, [edx+58h]
00BA7A87 sub     ebx, edi
00BA7A89 push    ebx
00BA7A8A push    edi
00BA7A8B mov     ecx, esi
00BA7A8D call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba79d9` | opcode 写入/分发指令 |

## 5. 块内字符串常量（含义取证用）

```
00EED50C
```
