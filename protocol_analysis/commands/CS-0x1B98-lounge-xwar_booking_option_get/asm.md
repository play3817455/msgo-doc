# 汇编证据 —— CS-0x1B98-xwar_booking_option_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B91040 @ `0xb91040`（`0xb91040`..`0xb91226`）
- 命令名字符串：`)<-_proto_lounge_client::send_xwar_booking_option_get( ` @ `0xeeafe0`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B91070 jz      loc_B91222
00B91076 mov     ecx, [edi+0Ch]
00B91079 test    ecx, ecx
00B9107B jz      loc_B91222
00B91081 mov     eax, [ecx]
00B91083 mov     edx, [eax+78h]
00B91086 push    0Ah
00B91088 call    edx
00B9108A mov     ebp, eax
00B9108C mov     eax, [edi+0Ch]
00B9108F push    eax
00B91090 lea     ecx, [esp+44h+var_2C]
00B91094 call    sub_ABB2F0
00B91099 lea     ecx, [ebp+0Ah]
00B9109C lea     eax, [ebp+2]
00B9109F cmp     eax, ecx
00B910A9 ja      loc_B91211
00B910AF lea     edx, [eax+4]
00B910B2 cmp     edx, ecx
00B910B4 mov     word ptr [ebp+0], 1B98h
00B910BA ja      loc_B91211
00B910C0 mov     esi, [esp+40h+arg_0]
00B910C4 lea     ebx, [edx+4]
00B910C7 cmp     ebx, ecx
00B910C9 mov     [eax], esi
00B910CB ja      loc_B91211
00B910D1 mov     ecx, [esp+40h+arg_4]
00B910D5 mov     [edx], ecx
00B910D7 mov     esi, [edi+7C3Ch]
00B910DD test    esi, esi
00B910DF jz      loc_B911B2
00B910E5 lea     edx, [esp+40h+var_28]
00B910E9 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B911B2 mov     edx, [edi]
00B911B4 mov     eax, [edx+58h]
00B911B7 sub     ebx, ebp
00B911B9 push    ebx
00B911BA push    ebp
00B911BB mov     ecx, edi
00B911BD call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb910b4` | opcode 写入/分发指令 |
| `matching_type` | `0xB910C9` | u32 |
| `matching_request_flag` | `0xB910D5` | u32 |

## 5. 块内字符串常量（含义取证用）

```
00EEAFE0
00EE4154
00EE413C
```
