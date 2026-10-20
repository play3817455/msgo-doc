# 汇编证据 —— SC-0xFCE9-btlroom_invite_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb88852`..`0xb88a8e`
- 命令名字符串：`)->_proto_lounge_client::recv_btlroom_invite_r( ` @ `0xee5500`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B88852 push    91h
00B88857 mov     ecx, esi
00B88859 call    sub_B41120
00B8885E test    al, al
00B88860 jz      loc_B890FE
00B88866 mov     ecx, [esi+0Ch]
00B88869 mov     eax, [ecx]
00B8886B mov     edx, [eax+78h]
00B8886E push    0Ch
00B88870 call    edx
00B88872 mov     [esp+2C5Ch+var_2C3C], eax
00B88876 mov     eax, [esi+0Ch]
00B88879 push    eax
00B8887A lea     ecx, [esp+2C60h+var_29CC]
00B88881 call    sub_ABB2F0
00B88886 lea     ecx, [esp+2C5Ch+var_2C3C]
00B8888A push    ecx
00B8888B lea     ecx, [esp+2C60h+var_2C38]
00B8889A call    sub_B41470
00B8889F mov     eax, [esp+2C5Ch+var_2C38]
00B888A3 lea     edx, [esp+2C5Ch+var_2C44]
00B888A7 push    edx
00B888A8 push    eax
00B888A9 call    sub_B02DD0
00B888B1 test    al, al
00B888B3 jnz     short loc_B888D1
00B888B5 mov     edx, [esi]
00B888B7 mov     eax, [edx+64h]
00B888BA push    1
00B888BC push    91h
00B888C1 mov     ecx, esi
00B888C3 call    eax
00B888C5 lea     ecx, [esp+2C5Ch+var_29CC]
00B888D1 lea     ecx, [esp+2C5Ch+var_2C3C]
00B888D5 push    ecx
00B888D6 lea     ecx, [esp+2C60h+var_2C48]
00B888DA call    sub_B41470
00B888DF mov     eax, [esp+2C5Ch+var_2C48]
00B888E3 lea     edx, [esp+2C5Ch+var_2C44]
00B888E7 push    edx
00B888E8 push    eax
00B888E9 call    sub_B02DD0
00B888F1 test    al, al
00B888F3 jz      short loc_B888B5
00B888F5 lea     ecx, [esp+2C5Ch+var_2C3C]
00B888F9 push    ecx
00B888FA lea     ecx, [esp+2C60h+var_2C20]
00B888FE call    sub_B41470
00B88903 mov     eax, [esp+2C5Ch+var_2C20]
00B88907 lea     edx, [esp+2C5Ch+var_2C44]
00B8890B push    edx
00B8890C push    eax
00B8890D call    sub_B02DD0
00B88915 test    al, al
00B88917 jz      short loc_B888B5
00B88919 mov     ebx, [esp+2C5Ch+var_2C44]
00B8891D cmp     ebx, [esp+2C5Ch+var_2C40]
00B88921 mov     ecx, esi
00B88923 jz      short loc_B8893F
00B88925 mov     edx, [esi]
00B88927 mov     eax, [edx+64h]
00B8892A push    1
00B8892C push    91h
00B88931 call    eax
00B88933 lea     ecx, [esp+2C5Ch+var_29CC]
00B8893F push    91h
00B88944 call    sub_B41110
00B88949 mov     edi, eax
00B8894B test    edi, edi
00B8894D jz      loc_B88A53
00B88953 lea     ecx, [esp+2C5Ch+var_9C]
00B8895A push    ecx
00B88963 mov     edx, [esi+8]
00B88966 push    offset aProtoLoungeCli_346
00B8896B push    edx
00B8896C push    offset aId
00B88971 push    eax
00B88972 push    edi
00B88983 push    eax
00B8898C mov     ecx, eax
00B88993 push    eax
00B8899C lea     ecx, [esp+2C5Ch+var_9C]
00B889AB call    sub_B02FF0
00B889B0 mov     eax, [esp+2C5Ch+var_2C38]
00B889B4 mov     ecx, [eax]
00B889B6 push    offset word_F641DC
00B889BB push    ecx
00B889BC push    offset aResult
00B889C1 push    edi
00B889CA mov     ecx, eax
00B889D1 push    eax
00B889D7 mov     edx, [esp+2C64h+var_2C48]
00B889DB mov     eax, [edx]
00B889E0 push    offset word_F641DC
00B889E5 push    eax
00B889E6 push    offset aRefusePilotId
00B889EB push    edi
00B889F4 mov     ecx, eax
00B889FB push    eax
00B88A01 mov     ecx, [esp+2C64h+var_2C20]
00B88A05 mov     edx, [ecx]
00B88A0A push    edx
00B88A0B push    offset aReason
00B88A10 push    edi
00B88A19 mov     ecx, eax
00B88A20 sub     ebx, [ebp+arg_0]
00B88A23 push    offset sub_B03810
00B88A28 push    offset aByte
00B88A2D push    ebx
00B88A2E push    offset asc_EDAD58
00B88A33 push    edi
00B88A3C mov     ecx, eax
00B88A43 push    eax
00B88A4C mov     ecx, eax
00B88A4E call    sub_B02D30
00B88A53 mov     ecx, [esp+2C5Ch+var_2C20]
00B88A57 mov     edx, [ecx]
00B88A59 mov     ecx, [esp+2C5Ch+var_2C48]
00B88A5D mov     eax, [esi]
00B88A5F mov     eax, [eax+1B4h]
00B88A65 push    edx
00B88A66 mov     edx, [ecx]
00B88A68 mov     ecx, [esp+2C60h+var_2C38]
00B88A6C push    edx
00B88A6D mov     edx, [ecx]
00B88A6F push    edx
00B88A70 mov     ecx, esi
00B88A72 call    eax
00B88A74 add     dword ptr [esi+2088h], 1
00B88A7B lea     ecx, [esp+2C5Ch+var_29CC]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb88966` | opcode 写入/分发指令 |
| `result` | `0xB888A9` | u32 |
| `refuse_pilot_id` | `0xB888E9` | u32 |
| `reason` | `0xB8890D` | u32 |

## 4. 块内字符串常量（含义取证用）

```
00B8893F
00EE5500
00EDAD90
00EE4914
00EDC2E0
00B02D30
```
