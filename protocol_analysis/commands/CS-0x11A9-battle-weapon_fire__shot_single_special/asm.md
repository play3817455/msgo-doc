# 汇编证据 —— CS-0x11A9-weapon_fire__shot_single_special

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B36C80 @ `0xb36c80`（`0xb36c80`..`0xb36eb7`）
- 命令名字符串：`)<-_proto_battle_client::send_weapon_fire__shot_single_special( ` @ `0xee0cd8`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B36CB0 jz      loc_B36EB3
00B36CB6 mov     ecx, [edi+0Ch]
00B36CB9 test    ecx, ecx
00B36CBB jz      loc_B36EB3
00B36CC1 mov     eax, [ecx]
00B36CC3 mov     edx, [eax+78h]
00B36CC6 push    0Eh
00B36CC8 call    edx
00B36CCA mov     ebp, eax
00B36CCC mov     eax, [edi+0Ch]
00B36CCF push    eax
00B36CD0 lea     ecx, [esp+4Ch+var_34]
00B36CD4 call    sub_ABB2F0
00B36CD9 lea     ecx, [ebp+0Eh]
00B36CDC lea     eax, [ebp+2]
00B36CDF cmp     eax, ecx
00B36CE9 mov     [esp+48h+var_30], ebp
00B36CED mov     dword ptr [esp+48h+var_2C], ecx
00B36CF1 ja      loc_B36EA2
00B36CF7 lea     edx, [eax+4]
00B36CFA cmp     edx, ecx
00B36CFC mov     word ptr [ebp+0], 11A9h
00B36D02 ja      loc_B36EA2
00B36D08 mov     esi, [esp+48h+arg_0]
00B36D0C mov     [eax], esi
00B36D0E mov     eax, edx
00B36D10 lea     edx, [eax+4]
00B36D13 cmp     edx, ecx
00B36D15 ja      loc_B36EA2
00B36D1B mov     ecx, [esp+48h+arg_4]
00B36D1F mov     [esp+48h+var_30], edx
00B36D23 lea     edx, [esp+48h+var_30]
00B36D27 mov     [eax], ecx
00B36D29 push    edx
00B36D2A lea     eax, [esp+4Ch+arg_8]
00B36D2E push    eax
00B36D2F call    sub_B02DA0
00B36D37 test    al, al
00B36D39 jz      loc_B36EA2
00B36D3F mov     esi, [edi+3DD0h]
00B36D45 test    esi, esi
00B36D47 mov     ebx, [esp+48h+var_30]
00B36D4B jz      loc_B36E46
00B36D51 lea     ecx, [esp+48h+var_28]
00B36D55 push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B36E46 mov     edx, [edi]
00B36E48 mov     eax, [edx+58h]
00B36E4B sub     ebx, ebp
00B36E4D push    ebx
00B36E4E push    ebp
00B36E4F mov     ecx, edi
00B36E51 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb36cfc` | opcode 写入/分发指令 |
| `frame_count` | `0xB36D0C` | u32 |
| `itemid` | `0xB36D27` | u32 |
| `AI_ent_id` | `0xB36D2F` | u16 |

## 5. 块内字符串常量（含义取证用）

```
00EE0CD8
00EDC830
00EDBD4C
00EDC870
```
