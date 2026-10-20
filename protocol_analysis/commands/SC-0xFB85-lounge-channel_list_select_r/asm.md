# 汇编证据 —— SC-0xFB85-channel_list_select_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb87e8f`..`0xb88255`
- 命令名字符串：`)->_proto_lounge_client::recv_channel_list_select_r( ` @ `0xee55e8`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B87E8F push    7
00B87E91 mov     ecx, esi
00B87E93 call    sub_B41120
00B87E98 test    al, al
00B87E9A jz      loc_B890FE
00B87EA0 mov     ecx, [esi+0Ch]
00B87EA3 mov     eax, [ecx]
00B87EA5 mov     edx, [eax+78h]
00B87EA8 push    0BEh
00B87EAD call    edx
00B87EAF mov     [esp+2C5Ch+var_2C28], eax
00B87EB3 mov     eax, [esi+0Ch]
00B87EB6 push    eax
00B87EB7 lea     ecx, [esp+2C60h+var_2B60]
00B87EBE call    sub_ABB2F0
00B87EC3 lea     ecx, [esp+2C5Ch+var_2C28]
00B87EC7 push    ecx
00B87EC8 lea     ecx, [esp+2C60h+var_2C34]
00B87ED7 call    sub_B41470
00B87EDC mov     eax, [esp+2C5Ch+var_2C34]
00B87EE0 lea     edx, [esp+2C5Ch+var_2C44]
00B87EE4 push    edx
00B87EE5 push    eax
00B87EE6 call    sub_B02DD0
00B87EEE test    al, al
00B87EF0 jnz     short loc_B87F0B
00B87EF2 mov     edx, [esi]
00B87EF4 mov     eax, [edx+64h]
00B87EF7 push    1
00B87EF9 push    7
00B87EFB mov     ecx, esi
00B87EFD call    eax
00B87EFF lea     ecx, [esp+2C5Ch+var_2B60]
00B87F0B lea     ecx, [esp+2C5Ch+var_2C28]
00B87F0F push    ecx
00B87F10 lea     ecx, [esp+2C60h+var_2C38]
00B87F14 call    sub_B41470
00B87F19 mov     eax, [esp+2C5Ch+var_2C38]
00B87F1D lea     edx, [esp+2C5Ch+var_2C44]
00B87F21 push    edx
00B87F22 push    eax
00B87F23 call    sub_B02DD0
00B87F2B test    al, al
00B87F2D jz      short loc_B87EF2
00B87F2F mov     eax, [esp+2C5Ch+var_2C28]
00B87F33 mov     ecx, eax
00B87F35 push    81h
00B87F3A lea     edx, [esp+2C60h+var_2C44]
00B87F3E push    edx
00B87F3F add     eax, 81h
00B87F44 push    ecx
00B87F45 mov     [esp+2C68h+var_2C30], ecx
00B87F49 mov     [esp+2C68h+var_2C28], eax
00B87F4D call    sub_B02BA0
00B87F55 test    al, al
00B87F57 jnz     short loc_B87F72
00B87F59 mov     eax, [esi]
00B87F5B mov     edx, [eax+64h]
00B87F5E push    1
00B87F60 push    7
00B87F62 mov     ecx, esi
00B87F64 call    edx
00B87F66 lea     ecx, [esp+2C5Ch+var_2B60]
00B87F72 lea     eax, [esp+2C5Ch+var_2C28]
00B87F76 push    eax
00B87F77 lea     ecx, [esp+2C60h+var_2C48]
00B87F7B call    sub_B41470
00B87F80 mov     edx, [esp+2C5Ch+var_2C48]
00B87F84 lea     ecx, [esp+2C5Ch+var_2C44]
00B87F88 push    ecx
00B87F89 push    edx
00B87F8A call    sub_B02DD0
00B87F92 test    al, al
00B87F94 jz      short loc_B87F59
00B87F96 lea     eax, [esp+2C5Ch+var_2C28]
00B87F9A push    eax
00B87F9B lea     ecx, [esp+2C60h+var_2C20]
00B87F9F call    sub_B41470
00B87FA4 mov     edx, [esp+2C5Ch+var_2C20]
00B87FA8 lea     ecx, [esp+2C5Ch+var_2C44]
00B87FAC push    ecx
00B87FAD push    edx
00B87FAE call    sub_B02DD0
00B87FB6 test    al, al
00B87FB8 jz      short loc_B87F59
00B87FBA lea     eax, [esp+2C5Ch+var_2C28]
00B87FBE push    eax
00B87FBF lea     ecx, [esp+2C60h+var_2C3C]
00B87FC3 call    sub_B41470
00B87FC8 mov     edx, [esp+2C5Ch+var_2C3C]
00B87FCC lea     ecx, [esp+2C5Ch+var_2C44]
00B87FD0 push    ecx
00B87FD1 push    edx
00B87FD2 call    sub_B02DD0
00B87FDA test    al, al
00B87FDC jz      loc_B87F59
00B87FE2 mov     ecx, [esp+2C5Ch+var_2C28]
00B87FE6 push    29h
00B87FE8 lea     eax, [esp+2C60h+var_2C44]
00B87FEC push    eax
00B87FED push    ecx
00B87FEE call    sub_B02BA0
00B87FF6 test    al, al
00B87FF8 jz      loc_B87EF2
00B87FFE mov     ebx, [esp+2C5Ch+var_2C44]
00B88002 cmp     ebx, [esp+2C5Ch+var_2C40]
00B88006 mov     ecx, esi
00B88008 jz      short loc_B88021
00B8800A mov     edx, [esi]
00B8800C mov     eax, [edx+64h]
00B8800F push    1
00B88011 push    7
00B88013 call    eax
00B88015 lea     ecx, [esp+2C5Ch+var_2B60]
00B88021 push    7
00B88023 call    sub_B41110
00B88028 mov     edi, eax
00B8802A test    edi, edi
00B8802C jz      loc_B881F6
00B88032 lea     ecx, [esp+2C5Ch+var_17C]
00B88039 push    ecx
00B88042 mov     edx, [esi+8]
00B88045 push    offset aProtoLoungeCli_342
00B8804A push    edx
00B8804B push    offset aId
00B88050 push    eax
00B88051 push    edi
00B88062 push    eax
00B8806B mov     ecx, eax
00B88072 push    eax
00B8807B lea     ecx, [esp+2C5Ch+var_17C]
00B8808A call    sub_B02FF0
00B8808F mov     eax, [esp+2C5Ch+var_2C34]
00B88093 mov     ecx, [eax]
00B88095 push    offset word_F641DC
00B8809A push    ecx
00B8809B push    offset aResult
00B880A0 push    edi
00B880A9 mov     ecx, eax
00B880B0 push    eax
00B880B6 mov     edx, [esp+2C64h+var_2C38]
00B880BA mov     eax, [edx]
00B880BF push    offset word_F641DC
00B880C4 push    eax
00B880C5 push    offset aChannelId
00B880CA push    edi
00B880D3 mov     ecx, eax
00B880DA push    eax
00B880E0 mov     ecx, [esp+2C64h+var_2C30]
00B880E7 push    offset word_F641DC
00B880EC push    offset asc_EDAD54
00B880F1 push    ecx
00B880F2 push    offset aLoungesvHost
00B880F7 push    edi
00B88100 push    eax
00B88109 push    eax
00B88112 push    eax
00B88118 mov     edx, [esp+2C64h+var_2C48]
00B8811C mov     eax, [edx]
00B88121 push    offset word_F641DC
00B88126 push    eax
00B88127 push    offset aLoungesvPort
00B8812C push    edi
00B88135 mov     ecx, eax
00B8813C push    eax
00B88145 mov     ecx, [esp+2C5Ch+var_2C20]
00B88149 mov     edx, [ecx]
00B8814B push    offset word_F641DC
00B88150 push    edx
00B88151 push    offset aUserid
00B88156 push    edi
00B8815F mov     ecx, eax
00B88166 push    eax
00B8816C mov     eax, [esp+2C64h+var_2C3C]
00B88170 mov     ecx, [eax]
00B88175 push    offset word_F641DC
00B8817A push    ecx
00B8817B push    offset aPilotId
00B88180 push    edi
00B88189 mov     ecx, eax
00B88190 push    eax
00B88196 mov     edx, [esp+2C64h+var_2C28]
00B8819D push    offset asc_EDAD54
00B881A2 push    edx
00B881A3 push    offset aOtp
00B881A8 push    edi
00B881B1 push    eax
00B881BA push    eax
00B881C0 sub     ebx, [ebp+arg_0]
00B881C6 push    offset sub_B03810
00B881CB push    offset aByte
00B881D0 push    ebx
00B881D1 push    offset asc_EDAD58
00B881D6 push    edi
00B881DF mov     ecx, eax
00B881E6 push    eax
00B881EF mov     ecx, eax
00B881F1 call    sub_B02D30
00B881F6 mov     ecx, [esp+2C5Ch+var_2C28]
00B881FA mov     edx, [esp+2C5Ch+var_2C3C]
00B881FE mov     eax, [esi]
00B88200 mov     eax, [eax+74h]
00B88203 push    ecx
00B88204 mov     ecx, [edx]
00B88206 mov     edx, [esp+2C60h+var_2C20]
00B8820A push    ecx
00B8820B mov     ecx, [edx]
00B8820D mov     edx, [esp+2C64h+var_2C48]
00B88211 push    ecx
00B88212 mov     ecx, [edx]
00B88214 mov     edx, [esp+2C68h+var_2C30]
00B88218 push    ecx
00B88219 mov     ecx, [esp+2C6Ch+var_2C38]
00B8821D push    edx
00B8821E mov     edx, [ecx]
00B88220 mov     ecx, [esp+2C70h+var_2C34]
00B88224 push    edx
00B88225 mov     edx, [ecx]
00B88227 push    edx
00B88228 mov     ecx, esi
00B8822A call    eax
00B8822C add     dword ptr [esi+6A8h], 1
00B88233 lea     ecx, [esp+2C5Ch+var_2B60]
00B88246 cmp     eax, 0FCD2h
00B8824B jnz     def_B605BD
00B88251 push    3Bh
00B88253 mov     ecx, esi
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb88045` | opcode 写入/分发指令 |
| `result` | `0xB87EE6` | u32 |
| `channel_id` | `0xB87F23` | u32 |
| `loungesv_host` | `0xB87F4D` | str |
| `loungesv_port` | `0xB87F8A` | u32 |
| `userid` | `0xB87FAE` | u32 |
| `pilot_id` | `0xB87FD2` | u32 |
| `otp` | `0xB87FEE` | str |

## 4. 块内字符串常量（含义取证用）

```
00B88021
00EE55E8
00EDAD90
00EE2018
00EDADD0
00EDADC0
00EDADB8
00EDB34C
00EDADB0
00B02D30
00B88C7C
```
