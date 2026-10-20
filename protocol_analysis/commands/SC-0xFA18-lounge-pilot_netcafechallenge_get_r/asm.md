# 汇编证据 —— SC-0xFA18-pilot_netcafechallenge_get_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb878db`..`0xb87c6c`
- 命令名字符串：`)->_proto_lounge_client::recv_pilot_netcafechallenge_get_r( ` @ `0xee564c`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B878DB call    sub_B41120
00B878E0 test    al, al
00B878E2 jz      loc_B890FE
00B878E8 mov     ecx, [esi+0Ch]
00B878EB mov     eax, [ecx]
00B878ED mov     edx, [eax+78h]
00B878F0 push    45h
00B878F2 call    edx
00B878F4 mov     [esp+2C5Ch+var_2C2C], eax
00B878F8 mov     eax, [esi+0Ch]
00B878FB push    eax
00B878FC lea     ecx, [esp+2C60h+var_2AF4]
00B87903 call    sub_ABB2F0
00B87908 lea     ecx, [esp+2C5Ch+var_2C2C]
00B8790C push    ecx
00B8790D lea     ecx, [esp+2C60h+var_2C30]
00B8791C call    sub_B06160
00B87921 mov     ebx, [esp+2C5Ch+var_2C30]
00B87925 xor     edi, edi
00B87927 lea     edx, [esp+2C5Ch+var_2C44]
00B8792B push    edx
00B8792C push    ebx
00B8792D call    sub_B07540
00B87935 test    al, al
00B87937 jz      short loc_B87946
00B87939 add     edi, 1
00B8793C add     ebx, 14h
00B8793F cmp     edi, 3
00B87942 jb      short loc_B87927
00B87946 mov     eax, [esi]
00B87948 mov     edx, [eax+64h]
00B8794B push    1
00B8794D push    71h
00B8794F mov     ecx, esi
00B87951 call    edx
00B87953 lea     eax, [esp+2C5Ch+var_2C2C]
00B87957 push    eax
00B87958 lea     ecx, [esp+2C60h+var_2C34]
00B8795C call    sub_B05E30
00B87961 mov     edx, [esp+2C5Ch+var_2C34]
00B87965 lea     ecx, [esp+2C5Ch+var_2C44]
00B87969 push    ecx
00B8796A push    edx
00B8796B call    sub_B06230
00B87973 test    al, al
00B87975 jnz     short loc_B87990
00B87977 mov     eax, [esi]
00B87979 mov     edx, [eax+64h]
00B8797C push    1
00B8797E push    71h
00B87980 mov     ecx, esi
00B87982 call    edx
00B87984 lea     ecx, [esp+2C5Ch+var_2AF4]
00B87990 lea     eax, [esp+2C5Ch+var_2C2C]
00B87994 push    eax
00B87995 lea     ecx, [esp+2C60h+var_2C38]
00B87999 call    sub_B41470
00B8799E mov     edx, [esp+2C5Ch+var_2C38]
00B879A2 lea     ecx, [esp+2C5Ch+var_2C44]
00B879A6 push    ecx
00B879A7 push    edx
00B879A8 call    sub_B02DD0
00B879B0 test    al, al
00B879B2 jz      short loc_B87977
00B879B4 lea     eax, [esp+2C5Ch+var_2C2C]
00B879B8 push    eax
00B879B9 lea     ecx, [esp+2C60h+var_2C48]
00B879BD call    sub_B413B0
00B879C2 mov     edx, [esp+2C5Ch+var_2C48]
00B879C6 lea     ecx, [esp+2C5Ch+var_2C44]
00B879CA push    ecx
00B879CB push    edx
00B879CC call    sub_B02DF0
00B879D4 test    al, al
00B879D6 jz      short loc_B87977
00B879D8 lea     eax, [esp+2C5Ch+var_2C2C]
00B879DC push    eax
00B879DD lea     ecx, [esp+2C60h+var_2C20]
00B879E1 call    sub_B05E30
00B879E6 mov     edx, [esp+2C5Ch+var_2C20]
00B879EA lea     ecx, [esp+2C5Ch+var_2C44]
00B879EE push    ecx
00B879EF push    edx
00B879F0 call    sub_B06230
00B879F8 test    al, al
00B879FA jz      loc_B87977
00B87A00 lea     eax, [esp+2C5Ch+var_2C2C]
00B87A04 push    eax
00B87A05 lea     ecx, [esp+2C60h+var_2C3C]
00B87A09 call    sub_B05E30
00B87A0E mov     edx, [esp+2C5Ch+var_2C3C]
00B87A12 lea     ecx, [esp+2C5Ch+var_2C44]
00B87A16 push    ecx
00B87A17 push    edx
00B87A18 call    sub_B06230
00B87A20 test    al, al
00B87A22 jz      loc_B87977
00B87A28 mov     eax, [esp+2C5Ch+var_2C44]
00B87A2C cmp     eax, [esp+2C5Ch+var_2C40]
00B87A30 mov     ecx, esi
00B87A32 jz      short loc_B87A4B
00B87A34 mov     edx, [esi]
00B87A36 mov     eax, [edx+64h]
00B87A39 push    1
00B87A3B push    71h
00B87A3D call    eax
00B87A3F lea     ecx, [esp+2C5Ch+var_2AF4]
00B87A4B push    71h
00B87A4D call    sub_B41110
00B87A52 mov     edi, eax
00B87A54 test    edi, edi
00B87A56 jz      loc_B87C1A
00B87A5C lea     ecx, [esp+2C5Ch+var_1EC]
00B87A63 push    ecx
00B87A6C mov     edx, [esi+8]
00B87A6F push    offset aProtoLoungeCli_340
00B87A74 push    edx
00B87A75 push    offset aId
00B87A7A push    eax
00B87A7B push    edi
00B87A8C push    eax
00B87A95 mov     ecx, eax
00B87A9C push    eax
00B87AA5 lea     ecx, [esp+2C5Ch+var_1EC]
00B87AB4 call    sub_B02FF0
00B87AB9 push    offset aPdaily
00B87ABE push    edi
00B87AC4 mov     ebx, [esp+2C64h+var_2C30]
00B87AC8 push    ebx
00B87AC9 push    edi
00B87ACA call    sub_B0A1A0
00B87AD2 add     ebx, 14h
00B87AD5 mov     [esp+2C5Ch+var_2C0C], 2
00B87ADD lea     ecx, [ecx+0]
00B87AE0 push    ebx
00B87AE1 push    offset word_F641DC
00B87AE6 push    edi
00B87AEF push    eax
00B87AF0 call    sub_B0A1A0
00B87AF8 add     ebx, 14h
00B87AFB sub     [esp+2C5Ch+var_2C0C], 1
00B87B00 jnz     short loc_B87AE0
00B87B02 push    offset word_F641DC
00B87B07 push    offset unk_EDABE4
00B87B0C push    edi
00B87B15 push    eax
00B87B1B mov     eax, [esp+2C64h+var_2C34]
00B87B22 push    offset word_F641DC
00B87B27 push    eax
00B87B28 push    offset aIsAllClear
00B87B2D push    edi
00B87B36 push    eax
00B87B3F push    eax
00B87B45 mov     ecx, [esp+2C64h+var_2C38]
00B87B49 mov     edx, [ecx]
00B87B4E push    offset word_F641DC
00B87B53 push    edx
00B87B54 push    offset aCntCompleted
00B87B59 push    edi
00B87B62 mov     ecx, eax
00B87B69 push    eax
00B87B6F mov     eax, [esp+2C64h+var_2C48]
00B87B73 movzx   ecx, word ptr [eax]
00B87B79 push    offset word_F641DC
00B87B7E push    ecx
00B87B7F push    offset aYear
00B87B84 push    edi
00B87B8D mov     ecx, eax
00B87B94 push    eax
00B87B9A mov     edx, [esp+2C64h+var_2C20]
00B87BA1 push    offset word_F641DC
00B87BA6 push    edx
00B87BA7 push    offset aMonth
00B87BAC push    edi
00B87BB5 push    eax
00B87BBE push    eax
00B87BC4 mov     eax, [esp+2C64h+var_2C3C]
00B87BCB push    eax
00B87BCC push    offset aDay
00B87BD1 push    edi
00B87BDA push    eax
00B87BE0 mov     eax, [esp+2C64h+var_2C44]
00B87BE4 sub     eax, [ebp+arg_0]
00B87BEA push    offset sub_B03810
00B87BEF push    offset aByte
00B87BF4 push    eax
00B87BF5 push    offset asc_EDAD58
00B87BFA push    edi
00B87C03 mov     ecx, eax
00B87C0A push    eax
00B87C13 mov     ecx, eax
00B87C15 call    sub_B02D30
00B87C1A mov     eax, [esp+2C5Ch+var_2C3C]
00B87C1E movzx   ecx, byte ptr [eax]
00B87C21 mov     eax, [esp+2C5Ch+var_2C20]
00B87C25 mov     edx, [esi]
00B87C27 mov     edx, [edx+168h]
00B87C2D push    ecx
00B87C2E movzx   ecx, byte ptr [eax]
00B87C31 mov     eax, [esp+2C60h+var_2C48]
00B87C35 push    ecx
00B87C36 movzx   ecx, word ptr [eax]
00B87C39 mov     eax, [esp+2C64h+var_2C38]
00B87C3D push    ecx
00B87C3E mov     ecx, [eax]
00B87C40 mov     eax, [esp+2C68h+var_2C34]
00B87C44 push    ecx
00B87C45 movzx   ecx, byte ptr [eax]
00B87C48 mov     eax, [esp+2C6Ch+var_2C30]
00B87C4C push    ecx
00B87C4D push    eax
00B87C4E mov     ecx, esi
00B87C50 call    edx
00B87C52 add     dword ptr [esi+1A88h], 1
00B87C59 lea     ecx, [esp+2C5Ch+var_2AF4]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb87a6f` | opcode 写入/分发指令 |
| `pdaily` | `0xB8792D,0xB8791C` | array<challenge_info,3> |
| `is_all_clear` | `0xB8796B` | u8 |
| `cnt_completed` | `0xB879A8` | u32 |
| `year` | `0xB879CC` | u16 |
| `month` | `0xB879F0` | u8 |
| `day` | `0xB87A18` | u8 |

## 4. 块内字符串常量（含义取证用）

```
00B87A4B
00EE564C
00EE478C
00B87AE0
00EDABE4
00EE477C
00EE476C
00EE4764
00EE475C
00EE4754
00B02D30
```
