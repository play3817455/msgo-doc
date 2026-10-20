# 汇编证据 —— SC-0xFEBB-msma_spawn_warp_start_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B0CC20 @ `0xb0cc20`　块 `0xb31273`..`0xb314fe`
- 命令名字符串：`)->_proto_battle_client::recv_msma_spawn_warp_start_r( ` @ `0xedd810`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B31273 push    4Fh
00B31275 mov     ecx, esi
00B31277 call    sub_B05DA0
00B3127C test    al, al
00B3127E jz      loc_B317C7
00B31284 mov     ecx, [esi+0Ch]
00B31287 mov     eax, [ecx]
00B31289 mov     edx, [eax+78h]
00B3128C push    0Eh
00B3128E call    edx
00B31290 mov     [esp+1B3Ch+var_1B2C], eax
00B31294 mov     eax, [esi+0Ch]
00B31297 push    eax
00B31298 lea     ecx, [esp+1B40h+var_1974]
00B3129F call    sub_ABB2F0
00B312A4 lea     ecx, [esp+1B3Ch+var_1B2C]
00B312A8 push    ecx
00B312A9 lea     ecx, [esp+1B40h+var_1B18]
00B312B8 call    sub_B41470
00B312BD mov     eax, [esp+1B3Ch+var_1B18]
00B312C1 lea     edx, [esp+1B3Ch+var_1B28]
00B312C5 push    edx
00B312C6 push    eax
00B312C7 call    sub_B02DD0
00B312CF test    al, al
00B312D1 jnz     short loc_B312EC
00B312D3 mov     edx, [esi]
00B312D5 mov     eax, [edx+64h]
00B312D8 push    1
00B312DA push    4Fh
00B312DC mov     ecx, esi
00B312DE call    eax
00B312E0 lea     ecx, [esp+1B3Ch+var_1974]
00B312EC lea     ecx, [esp+1B3Ch+var_1B2C]
00B312F0 push    ecx
00B312F1 lea     ecx, [esp+1B40h+var_1B20]
00B312F5 call    sub_B41470
00B312FA mov     eax, [esp+1B3Ch+var_1B20]
00B312FE lea     edx, [esp+1B3Ch+var_1B28]
00B31302 push    edx
00B31303 push    eax
00B31304 call    sub_B02DD0
00B3130C test    al, al
00B3130E jz      short loc_B312D3
00B31310 lea     ecx, [esp+1B3Ch+var_1B2C]
00B31314 push    ecx
00B31315 lea     ecx, [esp+1B40h+var_1B08]
00B31319 call    sub_B413B0
00B3131E mov     eax, [esp+1B3Ch+var_1B08]
00B31322 lea     edx, [esp+1B3Ch+var_1B28]
00B31326 push    edx
00B31327 push    eax
00B31328 call    sub_B02DF0
00B31330 test    al, al
00B31332 jz      short loc_B312D3
00B31334 lea     ecx, [esp+1B3Ch+var_1B2C]
00B31338 push    ecx
00B31339 lea     ecx, [esp+1B40h+var_1B14]
00B3133D call    sub_B41470
00B31342 mov     eax, [esp+1B3Ch+var_1B14]
00B31346 lea     edx, [esp+1B3Ch+var_1B28]
00B3134A push    edx
00B3134B push    eax
00B3134C call    sub_B02DD0
00B31354 test    al, al
00B31356 jz      loc_B312D3
00B3135C mov     ebx, [esp+1B3Ch+var_1B28]
00B31360 cmp     ebx, [esp+1B3Ch+var_1B24]
00B31364 mov     ecx, esi
00B31366 jz      short loc_B3137F
00B31368 mov     edx, [esi]
00B3136A mov     eax, [edx+64h]
00B3136D push    1
00B3136F push    4Fh
00B31371 call    eax
00B31373 lea     ecx, [esp+1B3Ch+var_1974]
00B3137F push    4Fh
00B31381 call    sub_B05D90
00B31386 mov     edi, eax
00B31388 test    edi, edi
00B3138A jz      loc_B314BB
00B31390 lea     ecx, [esp+1B3Ch+var_64]
00B31397 push    ecx
00B313A0 mov     edx, [esi+8]
00B313A3 push    offset aProtoBattleCli_202
00B313A8 push    edx
00B313A9 push    offset aId
00B313AE push    eax
00B313AF push    edi
00B313C0 push    eax
00B313C9 mov     ecx, eax
00B313D0 push    eax
00B313D9 lea     ecx, [esp+1B3Ch+var_64]
00B313E8 call    sub_B02FF0
00B313ED mov     eax, [esp+1B3Ch+var_1B18]
00B313F1 mov     ecx, [eax]
00B313F3 push    offset word_F641DC
00B313F8 push    ecx
00B313F9 push    offset aResult
00B313FE push    edi
00B31407 mov     ecx, eax
00B3140E push    eax
00B31414 mov     edx, [esp+1B44h+var_1B20]
00B31418 mov     eax, [edx]
00B3141D push    offset word_F641DC
00B31422 push    eax
00B31423 push    offset aIsCancel
00B31428 push    edi
00B31431 mov     ecx, eax
00B31438 push    eax
00B3143E mov     ecx, [esp+1B44h+var_1B08]
00B31442 movzx   edx, word ptr [ecx]
00B31448 push    offset word_F641DC
00B3144D push    edx
00B3144E push    offset aEntId
00B31453 push    edi
00B3145C mov     ecx, eax
00B31463 push    eax
00B31469 mov     eax, [esp+1B44h+var_1B14]
00B3146D mov     ecx, [eax]
00B31472 push    ecx
00B31473 push    offset aCountdownMsec
00B31478 push    edi
00B31481 mov     ecx, eax
00B31488 sub     ebx, [ebp+arg_0]
00B3148B push    offset sub_B03810
00B31490 push    offset aByte
00B31495 push    ebx
00B31496 push    offset asc_EDAD58
00B3149B push    edi
00B314A4 mov     ecx, eax
00B314AB push    eax
00B314B4 mov     ecx, eax
00B314B6 call    sub_B02D30
00B314BB mov     eax, [esp+1B3Ch+var_1B14]
00B314BF mov     ecx, [eax]
00B314C1 mov     eax, [esp+1B3Ch+var_1B08]
00B314C5 mov     edx, [esi]
00B314C7 mov     edx, [edx+144h]
00B314CD push    ecx
00B314CE movzx   ecx, word ptr [eax]
00B314D1 mov     eax, [esp+1B40h+var_1B20]
00B314D5 push    ecx
00B314D6 mov     ecx, [eax]
00B314D8 mov     eax, [esp+1B44h+var_1B18]
00B314DC push    ecx
00B314DD mov     ecx, [eax]
00B314DF push    ecx
00B314E0 mov     ecx, esi
00B314E2 call    edx
00B314E4 add     dword ptr [esi+11B0h], 1
00B314EB lea     ecx, [esp+1B3Ch+var_1974]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb313a3` | opcode 写入/分发指令 |
| `result` | `0xB312C7` | u32 |
| `is_cancel` | `0xB31304` | u32 |
| `ent_id` | `0xB31328` | u16 |
| `countdown_msec` | `0xB3134C` | u32 |

## 4. 块内字符串常量（含义取证用）

```
00B3137F
00EDD810
00EDAD90
00EDC47C
00EDB98C
00EDCD88
00B02D30
```
