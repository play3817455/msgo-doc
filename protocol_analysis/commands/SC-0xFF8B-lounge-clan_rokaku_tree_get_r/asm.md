# 汇编证据 —— SC-0xFF8B-clan_rokaku_tree_get_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B51930 @ `0xb51930`　块 `0xb88c9d`..`0xb89116`
- 命令名字符串：`)->_proto_lounge_client::recv_clan_rokaku_tree_get_r( ` @ `0xee5490`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B88C9D push    1E0h
00B88CA2 mov     ecx, esi
00B88CA4 call    sub_B41120
00B88CA9 test    al, al
00B88CAB jz      loc_B890FE
00B88CB1 mov     ecx, [esi+0Ch]
00B88CB4 mov     eax, [ecx]
00B88CB6 mov     edx, [eax+78h]
00B88CB9 push    574h
00B88CBE call    edx
00B88CC0 mov     [esp+2C5Ch+var_2C10], eax
00B88CC4 mov     eax, [esi+0Ch]
00B88CC7 push    eax
00B88CC8 lea     ecx, [esp+2C60h+var_2B80]
00B88CCF call    sub_ABB2F0
00B88CD4 lea     ecx, [esp+2C5Ch+var_2C10]
00B88CD8 push    ecx
00B88CD9 lea     ecx, [esp+2C60h+var_2C38]
00B88CE8 call    sub_B41470
00B88CED mov     eax, [esp+2C5Ch+var_2C38]
00B88CF1 lea     edx, [esp+2C5Ch+var_2C44]
00B88CF5 push    edx
00B88CF6 push    eax
00B88CF7 call    sub_B02DD0
00B88CFF test    al, al
00B88D01 jnz     short loc_B88D18
00B88D03 mov     edx, [esi]
00B88D05 mov     eax, [edx+64h]
00B88D08 push    1
00B88D0A push    1E0h
00B88D0F mov     ecx, esi
00B88D11 call    eax
00B88D18 lea     ecx, [esp+2C5Ch+var_2C44]
00B88D1C push    ecx
00B88D1D lea     edx, [esp+2C60h+var_2C20]
00B88D21 push    edx
00B88D22 call    sub_B02DD0
00B88D2A test    al, al
00B88D2C jnz     short loc_B88D43
00B88D2E mov     eax, [esi]
00B88D30 mov     edx, [eax+64h]
00B88D33 push    1
00B88D35 push    1E0h
00B88D3A mov     ecx, esi
00B88D3C call    edx
00B88D43 mov     ebx, [esp+2C5Ch+var_2C20]
00B88D47 cmp     ebx, 8
00B88D4A ja      short loc_B88D2E
00B88D4C push    ebx
00B88D4D lea     eax, [esp+2C60h+var_2C10]
00B88D51 push    eax
00B88D52 lea     ecx, [esp+2C64h+var_2784]
00B88D59 call    sub_B41850
00B88D5E xor     edi, edi
00B88D60 test    ebx, ebx
00B88D62 jbe     short loc_B88DA4
00B88D64 mov     ecx, dword ptr [esp+2C5Ch+var_2784]
00B88D6B mov     [esp+2C5Ch+var_2C3C], ecx
00B88D6F nop
00B88D70 mov     eax, [esp+2C5Ch+var_2C3C]
00B88D74 lea     edx, [esp+2C5Ch+var_2C44]
00B88D78 push    edx
00B88D79 push    eax
00B88D7A call    sub_B462E0
00B88D82 test    al, al
00B88D84 jz      short loc_B88D94
00B88D86 add     [esp+2C5Ch+var_2C3C], 4
00B88D8B add     edi, 1
00B88D8E cmp     edi, ebx
00B88D90 jb      short loc_B88D70
00B88D94 mov     edx, [esi]
00B88D96 mov     eax, [edx+64h]
00B88D99 push    1
00B88D9B push    1E0h
00B88DA0 mov     ecx, esi
00B88DA2 call    eax
00B88DA4 lea     ecx, [esp+2C5Ch+var_2C44]
00B88DA8 push    ecx
00B88DA9 lea     edx, [esp+2C60h+var_2C2C]
00B88DAD push    edx
00B88DAE call    sub_B02DD0
00B88DB6 test    al, al
00B88DB8 jz      loc_B88D2E
00B88DBE cmp     [esp+2C5Ch+var_2C2C], 15h
00B88DC3 ja      loc_B88D2E
00B88DC9 mov     eax, [esp+2C5Ch+var_2C2C]
00B88DCD push    eax
00B88DCE lea     ecx, [esp+2C60h+var_2C10]
00B88DD2 push    ecx
00B88DD3 lea     ecx, [esp+2C64h+var_2BE8]
00B88DD7 call    sub_B41AC0
00B88DDC xor     edi, edi
00B88DDE cmp     [esp+2C5Ch+var_2C2C], edi
00B88DE2 jbe     short loc_B88E26
00B88DE4 mov     edx, [esp+2C5Ch+var_2BE8]
00B88DE8 mov     [esp+2C5Ch+var_2C3C], edx
00B88DEC lea     esp, [esp+0]
00B88DF0 mov     ecx, [esp+2C5Ch+var_2C3C]
00B88DF4 lea     eax, [esp+2C5Ch+var_2C44]
00B88DF8 push    eax
00B88DF9 push    ecx
00B88DFA call    sub_B46300
00B88E02 test    al, al
00B88E04 jz      short loc_B88E16
00B88E06 add     [esp+2C5Ch+var_2C3C], 40h
00B88E0B add     edi, 1
00B88E0E cmp     edi, [esp+2C5Ch+var_2C2C]
00B88E12 jb      short loc_B88DF0
00B88E16 mov     edx, [esi]
00B88E18 mov     eax, [edx+64h]
00B88E1B push    1
00B88E1D push    1E0h
00B88E22 mov     ecx, esi
00B88E24 call    eax
00B88E26 lea     ecx, [esp+2C5Ch+var_2C10]
00B88E2A push    ecx
00B88E2B lea     ecx, [esp+2C60h+var_2C48]
00B88E2F call    sub_B41470
00B88E34 mov     eax, [esp+2C5Ch+var_2C48]
00B88E38 lea     edx, [esp+2C5Ch+var_2C44]
00B88E3C push    edx
00B88E3D push    eax
00B88E3E call    sub_B02DD0
00B88E46 test    al, al
00B88E48 jz      loc_B88D03
00B88E4E lea     ecx, [esp+2C5Ch+var_2C10]
00B88E52 push    ecx
00B88E53 lea     ecx, [esp+2C60h+var_2C3C]
00B88E57 call    sub_B41470
00B88E5C mov     eax, [esp+2C5Ch+var_2C3C]
00B88E60 lea     edx, [esp+2C5Ch+var_2C44]
00B88E64 push    edx
00B88E65 push    eax
00B88E66 call    sub_B02DD0
00B88E6E test    al, al
00B88E70 jz      loc_B88D03
00B88E76 mov     ecx, [esp+2C5Ch+var_2C44]
00B88E7A cmp     ecx, [esp+2C5Ch+var_2C40]
00B88E7E mov     ecx, esi
00B88E80 jz      short loc_B88E95
00B88E82 mov     edx, [esi]
00B88E84 mov     eax, [edx+64h]
00B88E87 push    1
00B88E89 push    1E0h
00B88E8E call    eax
00B88E95 push    1E0h
00B88E9A call    sub_B41110
00B88E9F mov     edi, eax
00B88EA1 test    edi, edi
00B88EA3 jz      loc_B890A5
00B88EA9 lea     ecx, [esp+2C5Ch+var_2C]
00B88EB0 push    ecx
00B88EB9 mov     edx, [esi+8]
00B88EBC push    offset aProtoLoungeCli_348
00B88EC1 push    edx
00B88EC2 push    offset aId
00B88EC7 push    eax
00B88EC8 push    edi
00B88ED9 push    eax
00B88EE2 mov     ecx, eax
00B88EE9 push    eax
00B88EF2 lea     ecx, [esp+2C5Ch+var_2C]
00B88F01 call    sub_B02FF0
00B88F06 mov     eax, [esp+2C5Ch+var_2C38]
00B88F0A mov     ecx, [eax]
00B88F0C push    offset word_F641DC
00B88F11 push    ecx
00B88F12 push    offset aClanId
00B88F17 push    edi
00B88F20 mov     ecx, eax
00B88F27 push    eax
00B88F2D push    offset aPage
00B88F32 push    edi
00B88F3B test    ebx, ebx
00B88F3D jbe     short loc_B88F50
00B88F3F mov     edx, dword ptr [esp+2C5Ch+var_2784]
00B88F46 push    edx
00B88F47 push    edi
00B88F50 cmp     ebx, 1
00B88F53 jbe     short loc_B88F92
00B88F55 mov     ebx, dword ptr [esp+2C5Ch+var_2784]
00B88F5C mov     eax, [esp+2C5Ch+var_2C20]
00B88F60 add     ebx, 4
00B88F63 add     eax, 0FFFFFFFFh
00B88F66 mov     [esp+2C5Ch+var_2C34], eax
00B88F6A lea     ebx, [ebx+0]
00B88F70 push    ebx
00B88F71 push    offset word_F641DC
00B88F76 push    edi
00B88F7F push    eax
00B88F88 add     ebx, 4
00B88F8B sub     [esp+2C5Ch+var_2C34], 1
00B88F90 jnz     short loc_B88F70
00B88F92 push    offset word_F641DC
00B88F97 push    offset unk_EDABE4
00B88F9C push    edi
00B88FA5 push    eax
00B88FAB push    offset aNode
00B88FB0 push    edi
00B88FB6 mov     ebx, [esp+2C6Ch+var_2C2C]
00B88FBD test    ebx, ebx
00B88FBF jbe     short loc_B88FCF
00B88FC1 mov     ecx, [esp+2C5Ch+var_2BE8]
00B88FC5 push    ecx
00B88FC6 push    edi
00B88FCF cmp     ebx, 1
00B88FD2 jbe     short loc_B89008
00B88FD4 mov     ebx, [esp+2C5Ch+var_2BE8]
00B88FD8 mov     edx, [esp+2C5Ch+var_2C2C]
00B88FDC add     ebx, 40h
00B88FDF add     edx, 0FFFFFFFFh
00B88FE2 mov     [esp+2C5Ch+var_2C34], edx
00B88FE6 push    ebx
00B88FE7 push    offset word_F641DC
00B88FEC push    edi
00B88FF5 push    eax
00B88FFE add     ebx, 40h
00B89001 sub     [esp+2C5Ch+var_2C34], 1
00B89006 jnz     short loc_B88FE6
00B89008 push    offset word_F641DC
00B8900D push    offset unk_EDABE4
00B89012 push    edi
00B8901B push    eax
00B89021 mov     eax, [esp+2C64h+var_2C48]
00B89025 mov     ecx, [eax]
00B8902A push    offset word_F641DC
00B8902F push    ecx
00B89030 push    offset aPointUse
00B89035 push    edi
00B8903E mov     ecx, eax
00B89045 push    eax
00B8904B mov     edx, [esp+2C64h+var_2C3C]
00B8904F mov     eax, [edx]
00B89054 push    eax
00B89055 push    offset aPointPool
00B8905A push    edi
00B89063 mov     ecx, eax
00B8906A mov     eax, [esp+2C5Ch+var_2C44]
00B8906E sub     eax, [ebp+arg_0]
00B89071 push    offset sub_B03810
00B89076 push    offset aByte
00B8907B push    eax
00B8907C push    offset asc_EDAD58
00B89081 push    edi
00B8908A mov     ecx, eax
00B89091 push    eax
00B8909A mov     ecx, eax
00B8909C call    sub_B02D30
00B890A1 mov     ebx, [esp+2C5Ch+var_2C20]
00B890A5 mov     eax, [esp+2C5Ch+var_2C3C]
00B890A9 mov     ecx, [eax]
00B890AB mov     eax, [esp+2C5Ch+var_2C48]
00B890AF mov     edx, [esi]
00B890B1 mov     edx, [edx+484h]
00B890B7 push    ecx
00B890B8 mov     ecx, [eax]
00B890BA mov     eax, [esp+2C60h+var_2C2C]
00B890BE push    ecx
00B890BF mov     ecx, [esp+2C64h+var_2BE8]
00B890C3 push    eax
00B890C4 mov     eax, dword ptr [esp+2C68h+var_2784]
00B890CB push    ecx
00B890CC mov     ecx, [esp+2C6Ch+var_2C38]
00B890D0 push    ebx
00B890D1 push    eax
00B890D2 mov     eax, [ecx]
00B890D4 push    eax
00B890D5 mov     ecx, esi
00B890D7 call    edx
00B890D9 add     dword ptr [esi+5F58h], 1
00B890E7 lea     ecx, [esp+2C5Ch+var_2B80]
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb88ebc` | opcode 写入/分发指令 |
| `clan_id` | `0xB88CF7` | u32 |
| `page_count` | `0xB88D22` | u32 |
| `page` | `0xB88D59,0xB88D70` | array<u32> |
| `node_count` | `0xB88DAE` | u32 |
| `node` | `0xB88DD7,0xB88DFA` | array<elem60> |
| `point_use` | `0xB88E3E` | u32 |
| `point_pool` | `0xB88E66` | u32 |

## 4. 块内字符串常量（含义取证用）

```
00B88E95
00EE5490
00EDB2C8
00EE514C
00B88F92
00B88F70
00EDABE4
00EE39C0
00B89008
00B88FE6
00EDABE4
00EE3CBC
00EE5140
00B02D30
```
