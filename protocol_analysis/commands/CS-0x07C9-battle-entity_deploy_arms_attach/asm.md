# 汇编证据 —— CS-0x07C9-entity_deploy_arms_attach

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B34670 @ `0xb34670`（`0xb34670`..`0xb3492b`）
- 命令名字符串：`)<-_proto_battle_client::send_entity_deploy_arms_attach( ` @ `0xee0a64`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B346A0 jz      loc_B34927
00B346A6 mov     ecx, [edi+0Ch]
00B346A9 test    ecx, ecx
00B346AB jz      loc_B34927
00B346B1 mov     eax, [ecx]
00B346B3 mov     edx, [eax+78h]
00B346B6 push    16h
00B346B8 call    edx
00B346BA mov     ebp, eax
00B346BC mov     eax, [edi+0Ch]
00B346BF push    eax
00B346C0 lea     ecx, [esp+4Ch+var_34]
00B346C4 call    sub_ABB2F0
00B346C9 lea     eax, [ebp+16h]
00B346CC lea     ecx, [ebp+2]
00B346CF cmp     ecx, eax
00B346D9 mov     [esp+48h+var_30], ebp
00B346DD mov     dword ptr [esp+48h+var_2C], eax
00B346E1 ja      loc_B34916
00B346E7 lea     edx, [ecx+4]
00B346EA cmp     edx, eax
00B346EC mov     word ptr [ebp+0], 7C9h
00B346F2 ja      loc_B34916
00B346F8 mov     esi, [esp+48h+arg_0]
00B346FC mov     [ecx], esi
00B346FE lea     ecx, [edx+2]
00B34701 cmp     ecx, eax
00B34703 ja      loc_B34916
00B34709 mov     ax, word ptr [esp+48h+arg_4]
00B3470E mov     [esp+48h+var_30], ecx
00B34712 lea     ecx, [esp+48h+var_30]
00B34716 mov     [edx], ax
00B34719 push    ecx
00B3471A lea     edx, [esp+4Ch+arg_8]
00B3471E push    edx
00B3471F call    sub_B02DA0
00B34727 test    al, al
00B34729 jz      loc_B34916
00B3472F lea     eax, [esp+48h+var_30]
00B34733 push    eax
00B34734 lea     ecx, [esp+4Ch+arg_C]
00B34738 push    ecx
00B34739 call    sub_B02DA0
00B34741 test    al, al
00B34743 jz      loc_B34916
00B34749 lea     edx, [esp+48h+var_30]
00B3474D push    edx
00B3474E lea     eax, [esp+4Ch+arg_10]
00B34752 push    eax
00B34753 call    sub_B02DA0
00B3475B test    al, al
00B3475D jz      loc_B34916
00B34763 mov     esi, [edi+3D50h]
00B34769 test    esi, esi
00B3476B mov     ebx, [esp+48h+var_30]
00B3476F jz      loc_B348BA
00B34775 lea     ecx, [esp+48h+var_28]
00B34779 push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B348BA mov     eax, [edi]
00B348BC mov     edx, [eax+58h]
00B348BF sub     ebx, ebp
00B348C1 push    ebx
00B348C2 push    ebp
00B348C3 mov     ecx, edi
00B348C5 call    edx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb346ec` | opcode 写入/分发指令 |
| `arms_id` | `0xB346FC` | u32 |
| `attach_parent_ent_id` | `0xB34716` | u16 |
| `attach_pos_x` | `0xB3471F` | u16 |
| `attach_pos_y` | `0xB34739` | u16 |
| `attach_pos_z` | `0xB34753` | u16 |

## 5. 块内字符串常量（含义取证用）

```
00EE0A64
00EDBD8C
00EDC0BC
00EDC860
00EDC850
00EDC840
```
