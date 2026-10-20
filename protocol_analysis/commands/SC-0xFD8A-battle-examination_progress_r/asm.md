# 汇编证据 —— SC-0xFD8A-examination_progress_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B0CC20 @ `0xb0cc20`　块 `0xb30c68`..`0xb30ef6`
- 命令名字符串：`)->_proto_battle_client::recv_examination_progress_r( ` @ `0xedd8c4`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B30C68 call    sub_B05DA0
00B30C6D test    al, al
00B30C6F jz      loc_B317C7
00B30C75 mov     ecx, [esi+0Ch]
00B30C78 mov     eax, [ecx]
00B30C7A mov     edx, [eax+78h]
00B30C7D push    58h
00B30C7F call    edx
00B30C81 mov     [esp+1B3Ch+var_1B14], eax
00B30C85 mov     eax, [esi+0Ch]
00B30C88 push    eax
00B30C89 lea     ecx, [esp+1B40h+var_1850]
00B30C90 call    sub_ABB2F0
00B30C95 lea     ecx, [esp+1B3Ch+var_1B14]
00B30C99 push    ecx
00B30C9A lea     ecx, [esp+1B40h+var_1B20]
00B30CA9 call    sub_B419B0
00B30CAE mov     ebx, [esp+1B3Ch+var_1B20]
00B30CB2 xor     edi, edi
00B30CB4 lea     edx, [esp+1B3Ch+var_1B28]
00B30CB8 push    edx
00B30CB9 push    ebx
00B30CBA call    sub_B06BA0
00B30CC2 test    al, al
00B30CC4 jz      short loc_B30CD3
00B30CC6 add     edi, 1
00B30CC9 add     ebx, 10h
00B30CCC cmp     edi, 5
00B30CCF jb      short loc_B30CB4
00B30CD3 mov     eax, [esi]
00B30CD5 mov     edx, [eax+64h]
00B30CD8 push    1
00B30CDA push    10Fh
00B30CDF mov     ecx, esi
00B30CE1 call    edx
00B30CE3 lea     eax, [esp+1B3Ch+var_1B14]
00B30CE7 push    eax
00B30CE8 lea     ecx, [esp+1B40h+var_1B2C]
00B30CEC call    sub_B41470
00B30CF1 mov     edx, [esp+1B3Ch+var_1B2C]
00B30CF5 lea     ecx, [esp+1B3Ch+var_1B28]
00B30CF9 push    ecx
00B30CFA push    edx
00B30CFB call    sub_B02DD0
00B30D03 test    al, al
00B30D05 jnz     short loc_B30D23
00B30D07 mov     eax, [esi]
00B30D09 mov     edx, [eax+64h]
00B30D0C push    1
00B30D0E push    10Fh
00B30D13 mov     ecx, esi
00B30D15 call    edx
00B30D17 lea     ecx, [esp+1B3Ch+var_1850]
00B30D23 lea     eax, [esp+1B3Ch+var_1B14]
00B30D27 push    eax
00B30D28 lea     ecx, [esp+1B40h+var_1B08]
00B30D2C call    sub_B41470
00B30D31 mov     edx, [esp+1B3Ch+var_1B08]
00B30D35 lea     ecx, [esp+1B3Ch+var_1B28]
00B30D39 push    ecx
00B30D3A push    edx
00B30D3B call    sub_B02DD0
00B30D43 test    al, al
00B30D45 jz      short loc_B30D07
00B30D47 mov     eax, [esp+1B3Ch+var_1B28]
00B30D4B cmp     eax, [esp+1B3Ch+var_1B24]
00B30D4F mov     ecx, esi
00B30D51 jz      short loc_B30D6D
00B30D53 mov     edx, [esi]
00B30D55 mov     eax, [edx+64h]
00B30D58 push    1
00B30D5A push    10Fh
00B30D5F call    eax
00B30D61 lea     ecx, [esp+1B3Ch+var_1850]
00B30D6D push    10Fh
00B30D72 call    sub_B05D90
00B30D77 mov     edi, eax
00B30D79 test    edi, edi
00B30D7B jz      loc_B30EBD
00B30D81 lea     ecx, [esp+1B3Ch+var_10C]
00B30D88 push    ecx
00B30D91 mov     edx, [esi+8]
00B30D94 push    offset aProtoBattleCli_199
00B30D99 push    edx
00B30D9A push    offset aId
00B30D9F push    eax
00B30DA0 push    edi
00B30DB1 push    eax
00B30DBA mov     ecx, eax
00B30DC1 push    eax
00B30DCA lea     ecx, [esp+1B3Ch+var_10C]
00B30DD9 call    sub_B02FF0
00B30DDE push    offset aExaminationInf
00B30DE3 push    edi
00B30DE9 mov     ebx, [esp+1B44h+var_1B20]
00B30DED push    ebx
00B30DEE push    edi
00B30DF7 add     ebx, 10h
00B30DFA mov     [esp+1B3Ch+var_1B14], 4
00B30E02 push    ebx
00B30E03 push    offset word_F641DC
00B30E08 push    edi
00B30E11 push    eax
00B30E1A add     ebx, 10h
00B30E1D sub     [esp+1B3Ch+var_1B14], 1
00B30E22 jnz     short loc_B30E02
00B30E24 push    offset word_F641DC
00B30E29 push    offset unk_EDABE4
00B30E2E push    edi
00B30E37 push    eax
00B30E3D mov     eax, [esp+1B44h+var_1B2C]
00B30E41 mov     ecx, [eax]
00B30E46 push    offset word_F641DC
00B30E4B push    ecx
00B30E4C push    offset aExaminationPla
00B30E51 push    edi
00B30E5A mov     ecx, eax
00B30E61 push    eax
00B30E67 mov     edx, [esp+1B44h+var_1B08]
00B30E6B mov     eax, [edx]
00B30E70 push    eax
00B30E71 push    offset aExaminationPla_0
00B30E76 push    edi
00B30E7F mov     ecx, eax
00B30E86 mov     eax, [esp+1B3Ch+var_1B28]
00B30E8A sub     eax, [ebp+arg_0]
00B30E8D push    offset sub_B03810
00B30E92 push    offset aByte
00B30E97 push    eax
00B30E98 push    offset asc_EDAD58
00B30E9D push    edi
00B30EA6 mov     ecx, eax
00B30EAD push    eax
00B30EB6 mov     ecx, eax
00B30EB8 call    sub_B02D30
00B30EBD mov     eax, [esp+1B3Ch+var_1B08]
00B30EC1 mov     ecx, [eax]
00B30EC3 mov     eax, [esp+1B3Ch+var_1B2C]
00B30EC7 mov     edx, [esi]
00B30EC9 mov     edx, [edx+33Ch]
00B30ECF push    ecx
00B30ED0 mov     ecx, [eax]
00B30ED2 mov     eax, [esp+1B40h+var_1B20]
00B30ED6 push    ecx
00B30ED7 push    eax
00B30ED8 mov     ecx, esi
00B30EDA call    edx
00B30EDC add     dword ptr [esi+35B0h], 1
00B30EE3 lea     ecx, [esp+1B3Ch+var_1850]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb30d94` | opcode 写入/分发指令 |
| `examination_info` | `0xB30CA9,0xB30CBA` | array<4×u32,5> |
| `examination_playscore` | `0xB30CFB` | u32 |
| `examination_playsec_remain_msec` | `0xB30D3B` | u32 |

## 4. 块内字符串常量（含义取证用）

```
00B30D6D
00EDD8C4
00EDD6B0
00B30E02
00EDABE4
00EDD698
00EDD674
00B02D30
```
