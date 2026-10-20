# 汇编证据 —— SC-0xFE50-roomlobby_pick_vote_deck

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B0CC20 @ `0xb0cc20`　块 `0xb314fe`..`0xb317df`
- 命令名字符串：`)->_proto_battle_client::recv_roomlobby_pick_vote_deck( ` @ `0xedd7d4`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B314FE push    24h
00B31500 mov     ecx, esi
00B31502 call    sub_B05DA0
00B31507 test    al, al
00B31509 jz      loc_B317C7
00B3150F mov     ecx, [esi+0Ch]
00B31512 mov     eax, [ecx]
00B31514 mov     edx, [eax+78h]
00B31517 push    24h
00B31519 call    edx
00B3151B mov     [esp+1B3Ch+var_1B14], eax
00B3151F mov     eax, [esi+0Ch]
00B31522 push    eax
00B31523 lea     ecx, [esp+1B40h+var_1798]
00B3152A call    sub_ABB2F0
00B3152F lea     ecx, [esp+1B3Ch+var_1B14]
00B31533 push    ecx
00B31534 lea     ecx, [esp+1B40h+var_1B08]
00B31543 call    sub_B41470
00B31548 mov     eax, [esp+1B3Ch+var_1B08]
00B3154C lea     edx, [esp+1B3Ch+var_1B28]
00B31550 push    edx
00B31551 push    eax
00B31552 call    sub_B02DD0
00B3155A test    al, al
00B3155C jnz     short loc_B31570
00B3155E mov     edx, [esi]
00B31560 mov     eax, [edx+64h]
00B31563 push    1
00B31565 push    24h
00B31567 mov     ecx, esi
00B31569 call    eax
00B31570 lea     ecx, [esp+1B3Ch+var_1B14]
00B31574 push    ecx
00B31575 lea     ecx, [esp+1B40h+var_1B20]
00B31579 call    sub_B41990
00B3157E mov     ebx, [esp+1B3Ch+var_1B20]
00B31582 xor     edi, edi
00B31584 lea     edx, [esp+1B3Ch+var_1B28]
00B31588 push    edx
00B31589 push    ebx
00B3158A call    sub_B02DD0
00B31592 test    al, al
00B31594 jz      short loc_B315A3
00B31596 add     edi, 1
00B31599 add     ebx, 4
00B3159C cmp     edi, 4
00B3159F jb      short loc_B31584
00B315A3 mov     eax, [esi]
00B315A5 mov     edx, [eax+64h]
00B315A8 push    1
00B315AA push    24h
00B315AC mov     ecx, esi
00B315AE call    edx
00B315B0 lea     eax, [esp+1B3Ch+var_1B14]
00B315B4 push    eax
00B315B5 lea     ecx, [esp+1B40h+var_1B2C]
00B315B9 call    sub_B41990
00B315BE mov     ebx, [esp+1B3Ch+var_1B2C]
00B315C2 xor     edi, edi
00B315C4 lea     ecx, [esp+1B3Ch+var_1B28]
00B315C8 push    ecx
00B315C9 push    ebx
00B315CA call    sub_B02DD0
00B315D2 test    al, al
00B315D4 jz      short loc_B315E3
00B315D6 add     edi, 1
00B315D9 add     ebx, 4
00B315DC cmp     edi, 4
00B315DF jb      short loc_B315C4
00B315E3 mov     edx, [esi]
00B315E5 mov     eax, [edx+64h]
00B315E8 push    1
00B315EA push    24h
00B315EC mov     ecx, esi
00B315EE call    eax
00B315F0 mov     ecx, [esp+1B3Ch+var_1B28]
00B315F4 cmp     ecx, [esp+1B3Ch+var_1B24]
00B315F8 mov     ecx, esi
00B315FA jz      short loc_B3160C
00B315FC mov     edx, [esi]
00B315FE mov     eax, [edx+64h]
00B31601 push    1
00B31603 push    24h
00B31605 call    eax
00B3160C push    24h
00B3160E call    sub_B05D90
00B31613 mov     edi, eax
00B31615 test    edi, edi
00B31617 jz      loc_B31785
00B3161D lea     ecx, [esp+1B3Ch+var_2C]
00B31624 push    ecx
00B3162D mov     edx, [esi+8]
00B31630 push    offset aProtoBattleCli_203
00B31635 push    edx
00B31636 push    offset aId
00B3163B push    eax
00B3163C push    edi
00B3164D push    eax
00B31656 mov     ecx, eax
00B3165D push    eax
00B31666 lea     ecx, [esp+1B3Ch+var_2C]
00B31675 call    sub_B02FF0
00B3167A mov     eax, [esp+1B3Ch+var_1B08]
00B3167E mov     ecx, [eax]
00B31680 push    offset word_F641DC
00B31685 push    ecx
00B31686 push    offset aState
00B3168B push    edi
00B31694 mov     ecx, eax
00B3169B push    eax
00B316A1 push    offset aMsmaId_0
00B316A6 push    edi
00B316AC mov     edx, [esp+1B4Ch+var_1B20]
00B316B0 mov     eax, [edx]
00B316B5 push    eax
00B316B6 mov     ecx, edi
00B316BD mov     ebx, 1
00B316C2 mov     ecx, [esp+1B3Ch+var_1B20]
00B316C6 mov     edx, [ecx+ebx*4]
00B316C9 push    edx
00B316CA push    offset word_F641DC
00B316CF push    edi
00B316D8 mov     ecx, eax
00B316DF add     ebx, 1
00B316E2 cmp     ebx, 4
00B316E5 jb      short loc_B316C2
00B316E7 push    offset word_F641DC
00B316EC push    offset unk_EDABE4
00B316F1 push    edi
00B316FA push    eax
00B31700 push    offset aEnemyMsmaId
00B31705 push    edi
00B3170B mov     eax, [esp+1B4Ch+var_1B2C]
00B3170F mov     ecx, [eax]
00B31714 push    ecx
00B31715 mov     ecx, edi
00B3171C mov     ebx, 1
00B31721 mov     edx, [esp+1B3Ch+var_1B2C]
00B31725 mov     eax, [edx+ebx*4]
00B31728 push    eax
00B31729 push    offset word_F641DC
00B3172E push    edi
00B31737 mov     ecx, eax
00B3173E add     ebx, 1
00B31741 cmp     ebx, 4
00B31744 jb      short loc_B31721
00B31746 push    offset unk_EDABE4
00B3174B push    edi
00B31751 mov     eax, [esp+1B44h+var_1B28]
00B31755 sub     eax, [ebp+arg_0]
00B3175B push    offset aByte
00B31760 push    eax
00B31761 push    offset asc_EDAD58
00B31766 push    edi
00B3176F mov     ecx, eax
00B31776 push    eax
00B3177C push    eax
00B3177D call    sub_B03810
00B31785 mov     eax, [esp+1B3Ch+var_1B2C]
00B31789 mov     ecx, [esp+1B3Ch+var_1B20]
00B3178D mov     edx, [esi]
00B3178F mov     edx, [edx+0C8h]
00B31795 push    eax
00B31796 mov     eax, [esp+1B40h+var_1B08]
00B3179A push    ecx
00B3179B mov     ecx, [eax]
00B3179D push    ecx
00B3179E mov     ecx, esi
00B317A0 call    edx
00B317A2 add     dword ptr [esi+9A0h], 1
00B317B0 lea     ecx, [esp+1B3Ch+var_1798]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb31630` | opcode 写入/分发指令 |
| `state` | `0xB31552` | u32 |
| `msma_id` | `0xB31579,0xB3158A` | array<u32,4> |
| `enemy_msma_id` | `0xB315B9,0xB315CA` | array<u32,4> |

## 4. 块内字符串常量（含义取证用）

```
00B3160C
00EDD7D4
00EDC2AC
00EDCB34
00EDABE4
00EDCB24
00EDABE4
```
