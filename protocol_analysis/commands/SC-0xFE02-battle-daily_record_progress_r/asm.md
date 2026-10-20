# 汇编证据 —— SC-0xFE02-daily_record_progress_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B0CC20 @ `0xb0cc20`　块 `0xb3106e`..`0xb31273`
- 命令名字符串：`)->_proto_battle_client::recv_daily_record_progress_r( ` @ `0xedd848`

## 2. 读窗口切片（守卫 → 闭合）

```asm
00B3106E push    111h
00B31073 mov     ecx, esi
00B31075 call    sub_B05DA0
00B3107A test    al, al
00B3107C jz      loc_B317C7
00B31082 mov     ecx, [esi+0Ch]
00B31085 mov     eax, [ecx]
00B31087 mov     edx, [eax+78h]
00B3108A push    3Ch
00B3108C call    edx
00B3108E mov     [esp+1B3Ch+var_1B08], eax
00B31092 mov     eax, [esi+0Ch]
00B31095 push    eax
00B31096 lea     ecx, [esp+1B40h+var_175C]
00B3109D call    sub_ABB2F0
00B310A2 lea     ecx, [esp+1B3Ch+var_1B08]
00B310A6 push    ecx
00B310A7 lea     ecx, [esp+1B40h+var_1B14]
00B310B6 call    sub_B06160
00B310BB mov     ebx, [esp+1B3Ch+var_1B14]
00B310BF xor     edi, edi
00B310C1 lea     edx, [esp+1B3Ch+var_1B28]
00B310C5 push    edx
00B310C6 push    ebx
00B310C7 call    sub_B07540
00B310CF test    al, al
00B310D1 jz      short loc_B310E0
00B310D3 add     edi, 1
00B310D6 add     ebx, 14h
00B310D9 cmp     edi, 3
00B310DC jb      short loc_B310C1
00B310E0 mov     eax, [esi]
00B310E2 mov     edx, [eax+64h]
00B310E5 push    1
00B310E7 push    111h
00B310EC mov     ecx, esi
00B310EE call    edx
00B310F0 mov     eax, [esp+1B3Ch+var_1B28]
00B310F4 cmp     eax, [esp+1B3Ch+var_1B24]
00B310F8 mov     ecx, esi
00B310FA jz      short loc_B31116
00B310FC mov     edx, [esi]
00B310FE mov     eax, [edx+64h]
00B31101 push    1
00B31103 push    111h
00B31108 call    eax
00B3110A lea     ecx, [esp+1B3Ch+var_175C]
00B31116 push    111h
00B3111B call    sub_B05D90
00B31120 mov     edi, eax
00B31122 test    edi, edi
00B31124 jz      loc_B31217
00B3112A lea     ecx, [esp+1B3Ch+var_9C]
00B31131 push    ecx
00B3113A mov     edx, [esi+8]
00B3113D push    offset aProtoBattleCli_201
00B31142 push    edx
00B31143 push    offset aId
00B31148 push    eax
00B31149 push    edi
00B3115A push    eax
00B31163 mov     ecx, eax
00B3116A push    eax
00B31173 lea     ecx, [esp+1B3Ch+var_9C]
00B31182 call    sub_B02FF0
00B31187 push    offset aDailyRecordInf
00B3118C push    edi
00B31192 mov     ebx, [esp+1B44h+var_1B14]
00B31196 push    ebx
00B31197 push    edi
00B31198 call    sub_B0A1A0
00B311A0 add     ebx, 14h
00B311A3 mov     [esp+1B3Ch+var_1B08], 2
00B311AD align 10h
00B311B0 push    ebx
00B311B1 push    offset word_F641DC
00B311B6 push    edi
00B311BF push    eax
00B311C0 call    sub_B0A1A0
00B311C8 add     ebx, 14h
00B311CB sub     [esp+1B3Ch+var_1B08], 1
00B311D0 jnz     short loc_B311B0
00B311D2 push    offset unk_EDABE4
00B311D7 push    edi
00B311DD mov     eax, [esp+1B44h+var_1B28]
00B311E1 sub     eax, [ebp+arg_0]
00B311E7 push    offset sub_B03810
00B311EC push    offset aByte
00B311F1 push    eax
00B311F2 push    offset asc_EDAD58
00B311F7 push    edi
00B31200 mov     ecx, eax
00B31207 push    eax
00B31210 mov     ecx, eax
00B31212 call    sub_B02D30
00B31217 mov     ecx, [esp+1B3Ch+var_1B14]
00B3121B mov     eax, [esi]
00B3121D mov     edx, [eax+340h]
00B31223 push    ecx
00B31224 mov     ecx, esi
00B31226 call    edx
00B31228 add     dword ptr [esi+3610h], 1
00B3122F lea     ecx, [esp+1B3Ch+var_175C]
00B31242 sub     eax, 0FE50h
00B31247 jz      loc_B314FE
00B3124D sub     eax, 6Bh
00B31250 jz      short loc_B31273
00B31252 push    ebx
00B31253 push    edi
00B31254 mov     ecx, esi
00B31256 call    sub_B0C210
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb3113d` | opcode 写入/分发指令 |
| `daily_record_info` | `0xB310B6,0xB310C7` | array<challenge_info,3> |

## 4. 块内字符串常量（含义取证用）

```
00B31116
00EDD848
00EDD6C4
00B311B0
00B311B0
00EDABE4
00B02D30
00B314FE
00B31273
00B0C210
```
