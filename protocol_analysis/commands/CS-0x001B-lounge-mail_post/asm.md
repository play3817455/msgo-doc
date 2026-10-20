# 汇编证据 —— CS-0x001B-mail_post

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9B9B0 @ `0xb9b9b0`（`0xb9b9b0`..`0xb9bc7c`）
- 命令名字符串：`)<-_proto_lounge_client::send_mail_post( ` @ `0xeec19c`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00B9B9E0 jz      loc_B9BC78
00B9B9E6 mov     ecx, [edi+0Ch]
00B9B9E9 test    ecx, ecx
00B9B9EB jz      loc_B9BC78
00B9B9F1 mov     eax, [ecx]
00B9B9F3 mov     edx, [eax+78h]
00B9B9F6 push    36Eh
00B9B9FB call    edx
00B9B9FD mov     ebp, eax
00B9B9FF mov     eax, [edi+0Ch]
00B9BA02 push    eax
00B9BA03 lea     ecx, [esp+4Ch+var_34]
00B9BA07 call    sub_ABB2F0
00B9BA0C lea     ecx, [ebp+36Eh]
00B9BA12 lea     eax, [ebp+2]
00B9BA15 cmp     eax, ecx
00B9BA1F mov     [esp+48h+var_30], ebp
00B9BA23 mov     dword ptr [esp+48h+var_2C], ecx
00B9BA27 ja      loc_B9BC67
00B9BA2D mov     edx, [esp+48h+arg_0]
00B9BA31 push    19h
00B9BA33 lea     ecx, [esp+4Ch+var_30]
00B9BA37 push    ecx
00B9BA38 push    edx
00B9BA39 mov     word ptr [ebp+0], 1Bh
00B9BA3F mov     [esp+54h+var_30], eax
00B9BA43 call    sub_B02B40
00B9BA4B test    al, al
00B9BA4D jz      loc_B9BC67
00B9BA53 mov     ecx, [esp+48h+var_30]
00B9BA57 lea     eax, [ecx+4]
00B9BA5A cmp     eax, dword ptr [esp+48h+var_2C]
00B9BA5E ja      loc_B9BC67
00B9BA64 mov     edx, [esp+48h+arg_4]
00B9BA68 mov     [esp+48h+var_30], eax
00B9BA6C push    49h
00B9BA6E lea     eax, [esp+4Ch+var_30]
00B9BA72 mov     [ecx], edx
00B9BA74 mov     ecx, [esp+4Ch+arg_8]
00B9BA78 push    eax
00B9BA79 push    ecx
00B9BA7A call    sub_B02B40
00B9BA82 test    al, al
00B9BA84 jz      loc_B9BC67
00B9BA8A mov     eax, [esp+48h+arg_C]
00B9BA8E push    2FEh
00B9BA93 lea     edx, [esp+4Ch+var_30]
00B9BA97 push    edx
00B9BA98 push    eax
00B9BA99 call    sub_B02B40
00B9BAA1 test    al, al
00B9BAA3 jz      loc_B9BC67
00B9BAA9 mov     esi, [edi+7F48h]
00B9BAAF test    esi, esi
00B9BAB1 mov     ebx, [esp+48h+var_30]
00B9BAB5 jz      loc_B9BC08
00B9BABB lea     ecx, [esp+48h+var_28]
00B9BABF push    ecx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00B9BC08 mov     edx, [edi]
00B9BC0A mov     eax, [edx+58h]
00B9BC0D sub     ebx, ebp
00B9BC0F push    ebx
00B9BC10 push    ebp
00B9BC11 mov     ecx, edi
00B9BC13 call    eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xb9ba39` | opcode 写入/分发指令 |
| `to_pilot_name` | `0xB9BA43` | str |
| `kind` | `0xB9BA72` | u32 |
| `subject` | `0xB9BA7A` | str |
| `body` | `0xB9BA99` | str |

## 5. 块内字符串常量（含义取证用）

```
00EEC19C
00EE41E8
00EDD3AC
00EE41DC
00EE41D4
```
