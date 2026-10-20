# 汇编证据 —— SC-0xFCD2-pilot_rental_module_remain_info_notice

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb88255`..`0xb884cd`
- 命令名字符串：`)->_proto_lounge_client::recv_pilot_rental_module_remain_info_notice( ` @ `0xee55a0`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B88255 call    sub_B41120
00B8825A test    al, al
00B8825C jz      loc_B890FE
00B88262 mov     ecx, [esi+0Ch]
00B88265 mov     edx, [ecx]
00B88267 mov     eax, [edx+78h]
00B8826A push    600h
00B8826F call    eax
00B88271 mov     ecx, [esi+0Ch]
00B88274 push    ecx
00B88275 lea     ecx, [esp+2C60h+var_2668]
00B8827C mov     [esp+2C60h+var_2C20], eax
00B88280 call    sub_ABB2F0
00B88285 lea     edx, [esp+2C5Ch+var_2C20]
00B88289 push    edx
00B8828A lea     ecx, [esp+2C60h+var_2C3C]
00B88299 call    sub_B412A0
00B8829E mov     ebx, [esp+2C5Ch+var_2C3C]
00B882A2 xor     edi, edi
00B882A4 lea     eax, [esp+2C5Ch+var_2C44]
00B882A8 push    eax
00B882A9 push    ebx
00B882AA call    sub_B434B0
00B882B2 test    al, al
00B882B4 jz      short loc_B882C6
00B882B6 add     edi, 1
00B882B9 add     ebx, 8
00B882BC cmp     edi, 80h
00B882C2 jb      short loc_B882A4
00B882C6 mov     edx, [esi]
00B882C8 mov     eax, [edx+64h]
00B882CB push    1
00B882CD push    3Bh
00B882CF mov     ecx, esi
00B882D1 call    eax
00B882D3 lea     ecx, [esp+2C5Ch+var_2C20]
00B882D7 push    ecx
00B882D8 lea     ecx, [esp+2C60h+var_2C04]
00B882DC call    sub_B412C0
00B882E1 mov     ebx, [esp+2C5Ch+var_2C04]
00B882E5 xor     edi, edi
00B882E7 lea     edx, [esp+2C5Ch+var_2C44]
00B882EB push    edx
00B882EC push    ebx
00B882ED call    sub_B02DD0
00B882F5 test    al, al
00B882F7 jz      short loc_B88309
00B882F9 add     edi, 1
00B882FC add     ebx, 4
00B882FF cmp     edi, 80h
00B88305 jb      short loc_B882E7
00B88309 mov     eax, [esi]
00B8830B mov     edx, [eax+64h]
00B8830E push    1
00B88310 push    3Bh
00B88312 mov     ecx, esi
00B88314 call    edx
00B88316 mov     eax, [esp+2C5Ch+var_2C44]
00B8831A cmp     eax, [esp+2C5Ch+var_2C40]
00B8831E mov     ecx, esi
00B88320 jz      short loc_B88339
00B88322 mov     edx, [esi]
00B88324 mov     eax, [edx+64h]
00B88327 push    1
00B88329 push    3Bh
00B8832B call    eax
00B8832D lea     ecx, [esp+2C5Ch+var_2668]
00B88339 push    3Bh
00B8833B call    sub_B41110
00B88340 mov     edi, eax
00B88342 test    edi, edi
00B88344 jz      loc_B8849D
00B8834A lea     ecx, [esp+2C5Ch+var_144]
00B88351 push    ecx
00B8835A mov     edx, [esi+8]
00B8835D push    offset aProtoLoungeCli_343
00B88362 push    edx
00B88363 push    offset aId
00B88368 push    eax
00B88369 push    edi
00B8837A push    eax
00B88383 mov     ecx, eax
00B8838A push    eax
00B88393 lea     ecx, [esp+2C5Ch+var_144]
00B883A2 call    sub_B02FF0
00B883A7 push    offset aHavRentalModul
00B883AC push    edi
00B883B2 mov     ebx, [esp+2C64h+var_2C3C]
00B883B6 push    ebx
00B883B7 push    edi
00B883B8 call    sub_B47FA0
00B883C0 add     ebx, 8
00B883C3 mov     [esp+2C5Ch+var_2C20], 7Fh
00B883CD align 10h
00B883D0 push    ebx
00B883D1 push    offset word_F641DC
00B883D6 push    edi
00B883DF push    eax
00B883E0 call    sub_B47FA0
00B883E8 add     ebx, 8
00B883EB sub     [esp+2C5Ch+var_2C20], 1
00B883F0 jnz     short loc_B883D0
00B883F2 push    offset word_F641DC
00B883F7 push    offset unk_EDABE4
00B883FC push    edi
00B88405 push    eax
00B8840B push    offset aEmptyRentalMod
00B88410 push    edi
00B88416 mov     eax, [esp+2C6Ch+var_2C04]
00B8841A mov     ecx, [eax]
00B8841F push    ecx
00B88420 mov     ecx, edi
00B88427 mov     ebx, 1
00B8842C lea     esp, [esp+0]
00B88430 mov     edx, [esp+2C5Ch+var_2C04]
00B88434 mov     eax, [edx+ebx*4]
00B88437 push    eax
00B88438 push    offset word_F641DC
00B8843D push    edi
00B88446 mov     ecx, eax
00B8844D add     ebx, 1
00B88450 cmp     ebx, 80h
00B88456 jb      short loc_B88430
00B88458 push    offset unk_EDABE4
00B8845D push    edi
00B88463 mov     eax, [esp+2C64h+var_2C44]
00B88467 sub     eax, [ebp+arg_0]
00B8846D push    offset sub_B03810
00B88472 push    offset aByte
00B88477 push    eax
00B88478 push    offset asc_EDAD58
00B8847D push    edi
00B88486 mov     ecx, eax
00B8848D push    eax
00B88496 mov     ecx, eax
00B88498 call    sub_B02D30
00B8849D mov     eax, [esp+2C5Ch+var_2C04]
00B884A1 mov     ecx, [esp+2C5Ch+var_2C3C]
00B884A5 mov     edx, [esi]
00B884A7 mov     edx, [edx+0ECh]
00B884AD push    eax
00B884AE push    ecx
00B884AF mov     ecx, esi
00B884B1 call    edx
00B884B3 add     dword ptr [esi+1068h], 1
00B884BA lea     ecx, [esp+2C5Ch+var_2668]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb8835d` | opcode 写入/分发指令 |
| `hav_rental_modules` | `0xB88299,0xB882AA` | array<2×u32,128> |
| `empty_rental_modules` | `0xB882ED` | array<u32,128> |

## 4. 块内字符串常量（含义取证用）

```
00B88339
00EE55A0
00EE1DF8
00B883D0
00B883D0
00EDABE4
00EE44D8
00EDABE4
00B02D30
```
