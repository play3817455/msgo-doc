# 汇编证据 —— CS-0x20F5-entity_msma_fix

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B0C910 @ `0xb0c910`（`0xb0c910`..`0xb0cc13`）
- 命令名字符串：`)<-_proto_battle::send_entity_msma_fix( ` @ `0xedc160`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B0C940 jz      loc_B0CC0F
00B0C946 mov     ecx, [edi+0Ch]
00B0C949 test    ecx, ecx
00B0C94B jz      loc_B0CC0F
00B0C951 mov     eax, [ecx]
00B0C953 mov     edx, [eax+78h]
00B0C956 push    1Ah
00B0C958 call    edx
00B0C95A mov     ebp, eax
00B0C95C mov     eax, [edi+0Ch]
00B0C95F push    eax
00B0C960 lea     ecx, [esp+4Ch+var_34]
00B0C964 call    sub_ABB2F0
00B0C969 lea     ecx, [ebp+1Ah]
00B0C96C lea     eax, [ebp+2]
00B0C96F cmp     eax, ecx
00B0C979 mov     [esp+48h+var_30], ebp
00B0C97D mov     dword ptr [esp+48h+var_2C], ecx
00B0C981 ja      loc_B0CBFE
00B0C987 lea     edx, [eax+2]
00B0C98A cmp     edx, ecx
00B0C98C mov     word ptr [ebp+0], 20F5h
00B0C992 ja      loc_B0CBFE
00B0C998 mov     si, word ptr [esp+48h+arg_0]
00B0C99D mov     [eax], si
00B0C9A0 mov     eax, edx
00B0C9A2 lea     edx, [eax+2]
00B0C9A5 cmp     edx, ecx
00B0C9A7 ja      loc_B0CBFE
00B0C9AD mov     cx, word ptr [esp+48h+arg_4]
00B0C9B2 mov     [esp+48h+var_30], edx
00B0C9B6 lea     edx, [esp+48h+var_30]
00B0C9BA mov     [eax], cx
00B0C9BD push    edx
00B0C9BE lea     eax, [esp+4Ch+arg_8]
00B0C9C2 push    eax
00B0C9C3 call    sub_B02DA0
00B0C9CB test    al, al
00B0C9CD jz      loc_B0CBFE
00B0C9D3 lea     ecx, [esp+48h+var_30]
00B0C9D7 push    ecx
00B0C9D8 lea     edx, [esp+4Ch+arg_C]
00B0C9DC push    edx
00B0C9DD call    sub_B02DA0
00B0C9E5 test    al, al
00B0C9E7 jz      loc_B0CBFE
00B0C9ED lea     eax, [esp+48h+var_30]
00B0C9F1 push    eax
00B0C9F2 lea     ecx, [esp+4Ch+arg_10]
00B0C9F6 push    ecx
00B0C9F7 call    sub_B02DA0
00B0C9FF test    al, al
00B0CA01 jz      loc_B0CBFE
00B0CA07 lea     edx, [esp+48h+var_30]
00B0CA0B push    edx
00B0CA0C lea     eax, [esp+4Ch+arg_14]
00B0CA10 push    eax
00B0CA11 call    sub_B061C0
00B0CA19 test    al, al
00B0CA1B jz      loc_B0CBFE
00B0CA21 mov     esi, [edi+3D70h]
00B0CA27 test    esi, esi
00B0CA29 mov     ebx, [esp+48h+var_30]
00B0CA2D jz      loc_B0CBA2
00B0CA33 lea     ecx, [esp+48h+var_28]
00B0CA37 push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B0CBA2 mov     edx, [edi]
00B0CBA4 mov     eax, [edx+58h]
00B0CBA7 sub     ebx, ebp
00B0CBA9 push    ebx
00B0CBAA push    ebp
00B0CBAB mov     ecx, edi
00B0CBAD call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb0c98c` | opcode 写入/分发指令 |
| `ent_id` | `0xB0C99D` | u16 |
| `pos_x` | `0xB0C9BA` | u16 |
| `pos_y` | `0xB0C9C3` | u16 |
| `pos_z` | `0xB0C9DD` | u16 |
| `attach_parent_ent_id` | `0xB0C9F7` | u16 |
| `is_using_ss` | `0xB0CA11` | u8 |

## 5. 块内字符串常量（含义取证用）

```
00EDC160
00EDB98C
00EDB984
00EDB97C
00EDB974
00EDC0BC
00EDBD68
```
