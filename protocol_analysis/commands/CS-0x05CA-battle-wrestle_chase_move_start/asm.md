# 汇编证据 —— CS-0x05CA-wrestle_chase_move_start

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B40B50 @ `0xb40b50`（`0xb40b50`..`0xb40f16`）
- 命令名字符串：`)<-_proto_battle_client::send_wrestle_chase_move_start( ` @ `0xee18e0`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B40B80 jz      loc_B40F12
00B40B86 mov     ecx, [edi+0Ch]
00B40B89 test    ecx, ecx
00B40B8B jz      loc_B40F12
00B40B91 mov     eax, [ecx]
00B40B93 mov     edx, [eax+78h]
00B40B96 push    26h
00B40B98 call    edx
00B40B9A mov     ebp, eax
00B40B9C mov     eax, [edi+0Ch]
00B40B9F push    eax
00B40BA0 lea     ecx, [esp+4Ch+var_34]
00B40BA4 call    sub_ABB2F0
00B40BA9 lea     eax, [ebp+26h]
00B40BAC lea     ecx, [ebp+2]
00B40BAF cmp     ecx, eax
00B40BB9 mov     [esp+48h+var_30], ebp
00B40BBD mov     dword ptr [esp+48h+var_2C], eax
00B40BC1 ja      loc_B40F01
00B40BC7 lea     edx, [ecx+4]
00B40BCA cmp     edx, eax
00B40BCC mov     word ptr [ebp+0], 5CAh
00B40BD2 ja      loc_B40F01
00B40BD8 mov     esi, [esp+48h+arg_0]
00B40BDC mov     [ecx], esi
00B40BDE lea     ecx, [edx+2]
00B40BE1 cmp     ecx, eax
00B40BE3 ja      loc_B40F01
00B40BE9 mov     ax, word ptr [esp+48h+arg_4]
00B40BEE mov     [esp+48h+var_30], ecx
00B40BF2 lea     ecx, [esp+48h+var_30]
00B40BF6 mov     [edx], ax
00B40BF9 push    ecx
00B40BFA lea     edx, [esp+4Ch+arg_8]
00B40BFE push    edx
00B40BFF call    sub_B02D80
00B40C07 test    al, al
00B40C09 jz      loc_B40F01
00B40C0F lea     eax, [esp+48h+var_30]
00B40C13 push    eax
00B40C14 lea     ecx, [esp+4Ch+arg_C]
00B40C18 push    ecx
00B40C19 call    sub_B02D80
00B40C21 test    al, al
00B40C23 jz      loc_B40F01
00B40C29 lea     edx, [esp+48h+var_30]
00B40C2D push    edx
00B40C2E lea     eax, [esp+4Ch+arg_10]
00B40C32 push    eax
00B40C33 call    sub_B02DA0
00B40C3B test    al, al
00B40C3D jz      loc_B40F01
00B40C43 lea     ecx, [esp+48h+var_30]
00B40C47 push    ecx
00B40C48 lea     edx, [esp+4Ch+arg_14]
00B40C4C push    edx
00B40C4D call    sub_B02DA0
00B40C55 test    al, al
00B40C57 jz      loc_B40F01
00B40C5D lea     eax, [esp+48h+var_30]
00B40C61 push    eax
00B40C62 lea     ecx, [esp+4Ch+arg_18]
00B40C66 push    ecx
00B40C67 call    sub_B02DA0
00B40C6F test    al, al
00B40C71 jz      loc_B40F01
00B40C77 lea     edx, [esp+48h+var_30]
00B40C7B push    edx
00B40C7C lea     eax, [esp+4Ch+arg_1C]
00B40C80 push    eax
00B40C81 call    sub_B02DA0
00B40C89 test    al, al
00B40C8B jz      loc_B40F01
00B40C91 lea     ecx, [esp+48h+var_30]
00B40C95 push    ecx
00B40C96 lea     edx, [esp+4Ch+arg_20]
00B40C9A push    edx
00B40C9B call    sub_B02DA0
00B40CA3 test    al, al
00B40CA5 jz      loc_B40F01
00B40CAB mov     esi, [edi+40A0h]
00B40CB1 test    esi, esi
00B40CB3 mov     ebx, [esp+48h+var_30]
00B40CB7 jz      loc_B40EA2
00B40CBD lea     eax, [esp+48h+var_28]
00B40CC1 push    eax
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B40EA2 mov     eax, [edi]
00B40EA4 mov     edx, [eax+58h]
00B40EA7 sub     ebx, ebp
00B40EA9 push    ebx
00B40EAA push    ebp
00B40EAB mov     ecx, edi
00B40EAD call    edx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb40bcc` | opcode 写入/分发指令 |
| `frame_count` | `0xB40BDC` | u32 |
| `dir_h` | `0xB40BF6` | u16 |
| `wrestle_id` | `0xB40BFF` | u32 |
| `chase_time_msec` | `0xB40C19` | u32 |
| `target_ent_id` | `0xB40C33` | u16 |
| `target_pos_x` | `0xB40C4D` | u16 |
| `target_pos_y` | `0xB40C67` | u16 |
| `target_pos_z` | `0xB40C81` | u16 |
| `AI_ent_id` | `0xB40C9B` | u16 |

## 5. 块内字符串常量（含义取证用）

```
00EE18E0
00EDC830
00EDC828
00EDC81C
00EDC808
00EDC7F8
00EDC7E8
00EDC7D8
00EDC7C8
00EDC870
```
