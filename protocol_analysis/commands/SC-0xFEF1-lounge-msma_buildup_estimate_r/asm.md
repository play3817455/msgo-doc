# 汇编证据 —— SC-0xFEF1-msma_buildup_estimate_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb88a8e`..`0xb88c9d`
- 命令名字符串：`)->_proto_lounge_client::recv_msma_buildup_estimate_r( ` @ `0xee54c8`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B88A8E push    10Ah
00B88A93 mov     ecx, esi
00B88A95 call    sub_B41120
00B88A9A test    al, al
00B88A9C jz      loc_B890FE
00B88AA2 mov     ecx, [esi+0Ch]
00B88AA5 mov     edx, [ecx]
00B88AA7 mov     eax, [edx+78h]
00B88AAA push    8
00B88AAC call    eax
00B88AAE mov     ecx, [esi+0Ch]
00B88AB1 push    ecx
00B88AB2 lea     ecx, [esp+2C60h+var_282C]
00B88AB9 mov     [esp+2C60h+var_2C48], eax
00B88ABD call    sub_ABB2F0
00B88AC2 lea     edx, [esp+2C5Ch+var_2C48]
00B88AC6 push    edx
00B88AC7 lea     ecx, [esp+2C60h+var_2C20]
00B88AD6 call    sub_B41470
00B88ADB mov     ecx, [esp+2C5Ch+var_2C20]
00B88ADF lea     eax, [esp+2C5Ch+var_2C44]
00B88AE3 push    eax
00B88AE4 push    ecx
00B88AE5 call    sub_B02DD0
00B88AED test    al, al
00B88AEF jnz     short loc_B88B0D
00B88AF1 mov     edx, [esi]
00B88AF3 mov     eax, [edx+64h]
00B88AF6 push    1
00B88AF8 push    10Ah
00B88AFD mov     ecx, esi
00B88AFF call    eax
00B88B01 lea     ecx, [esp+2C5Ch+var_282C]
00B88B0D lea     ecx, [esp+2C5Ch+var_2C48]
00B88B11 push    ecx
00B88B12 lea     ecx, [esp+2C60h+var_2C3C]
00B88B16 call    sub_B41470
00B88B1B mov     eax, [esp+2C5Ch+var_2C3C]
00B88B1F lea     edx, [esp+2C5Ch+var_2C44]
00B88B23 push    edx
00B88B24 push    eax
00B88B25 call    sub_B02DD0
00B88B2D test    al, al
00B88B2F jz      short loc_B88AF1
00B88B31 mov     ebx, [esp+2C5Ch+var_2C44]
00B88B35 cmp     ebx, [esp+2C5Ch+var_2C40]
00B88B39 mov     ecx, esi
00B88B3B jz      short loc_B88B57
00B88B3D mov     edx, [esi]
00B88B3F mov     eax, [edx+64h]
00B88B42 push    1
00B88B44 push    10Ah
00B88B49 call    eax
00B88B4B lea     ecx, [esp+2C5Ch+var_282C]
00B88B57 push    10Ah
00B88B5C call    sub_B41110
00B88B61 mov     edi, eax
00B88B63 test    edi, edi
00B88B65 jz      loc_B88C41
00B88B6B lea     ecx, [esp+2C5Ch+var_64]
00B88B72 push    ecx
00B88B7B mov     edx, [esi+8]
00B88B7E push    offset aProtoLoungeCli_347
00B88B83 push    edx
00B88B84 push    offset aId
00B88B89 push    eax
00B88B8A push    edi
00B88B9B push    eax
00B88BA4 mov     ecx, eax
00B88BAB push    eax
00B88BB4 lea     ecx, [esp+2C5Ch+var_64]
00B88BC3 call    sub_B02FF0
00B88BC8 mov     eax, [esp+2C5Ch+var_2C20]
00B88BCC mov     ecx, [eax]
00B88BCE push    offset word_F641DC
00B88BD3 push    ecx
00B88BD4 push    offset aResult
00B88BD9 push    edi
00B88BE2 mov     ecx, eax
00B88BE9 push    eax
00B88BEF mov     edx, [esp+2C64h+var_2C3C]
00B88BF3 mov     eax, [edx]
00B88BF8 push    eax
00B88BF9 push    offset aPrice
00B88BFE push    edi
00B88C07 mov     ecx, eax
00B88C0E sub     ebx, [ebp+arg_0]
00B88C11 push    offset sub_B03810
00B88C16 push    offset aByte
00B88C1B push    ebx
00B88C1C push    offset asc_EDAD58
00B88C21 push    edi
00B88C2A mov     ecx, eax
00B88C31 push    eax
00B88C3A mov     ecx, eax
00B88C3C call    sub_B02D30
00B88C41 mov     eax, [esp+2C5Ch+var_2C3C]
00B88C45 mov     ecx, [eax]
00B88C47 mov     eax, [esp+2C5Ch+var_2C20]
00B88C4B mov     edx, [esi]
00B88C4D mov     edx, [edx+2BCh]
00B88C53 push    ecx
00B88C54 mov     ecx, [eax]
00B88C56 push    ecx
00B88C57 mov     ecx, esi
00B88C59 call    edx
00B88C5B add     dword ptr [esi+3738h], 1
00B88C62 lea     ecx, [esp+2C5Ch+var_282C]
00B88C75 cmp     eax, 0FF8Bh
00B88C7A jz      short loc_B88C9D
00B88C7C push    ebx
00B88C7D push    edi
00B88C7E mov     ecx, esi
00B88C80 call    sub_B411A0
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb88b7e` | opcode 写入/分发指令 |
| `result` | `0xB88AE5` | u32 |
| `price` | `0xB88B25` | u32 |

## 4. 块内字符串常量（含义取证用）

```
00B88B57
00EE54C8
00EDAD90
00EE3C30
00B02D30
00B88C9D
```
