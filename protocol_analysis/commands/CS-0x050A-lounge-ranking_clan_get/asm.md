# 汇编证据 —— CS-0x050A-ranking_clan_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA3A30 @ `0xba3a30`（`0xba3a30`..`0xba3c37`）
- 命令名字符串：`)<-_proto_lounge_client::send_ranking_clan_get( ` @ `0xeece60`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA3A60 jz      loc_BA3C33
00BA3A66 mov     ecx, [esi+0Ch]
00BA3A69 test    ecx, ecx
00BA3A6B jz      loc_BA3C33
00BA3A71 mov     eax, [ecx]
00BA3A73 mov     edx, [eax+78h]
00BA3A76 push    12h
00BA3A78 call    edx
00BA3A7A mov     ebp, eax
00BA3A7C mov     eax, [esi+0Ch]
00BA3A7F push    eax
00BA3A80 lea     ecx, [esp+4Ch+var_34]
00BA3A84 call    sub_ABB2F0
00BA3A89 lea     ecx, [ebp+12h]
00BA3A8C lea     eax, [ebp+2]
00BA3A8F cmp     eax, ecx
00BA3A99 mov     [esp+48h+var_30], ebp
00BA3A9D mov     dword ptr [esp+48h+var_2C], ecx
00BA3AA1 ja      loc_BA3C22
00BA3AA7 mov     edx, dword ptr [esp+48h+arg_0]
00BA3AAB lea     ecx, [esp+48h+var_30]
00BA3AAF push    ecx
00BA3AB0 push    edx
00BA3AB1 mov     word ptr [ebp+0], 50Ah
00BA3AB7 mov     [esp+50h+var_30], eax
00BA3ABB call    sub_B42060
00BA3AC0 add     esp, 8
00BA3AC3 test    al, al
00BA3AC5 jz      loc_BA3C22
00BA3ACB mov     eax, [esp+48h+var_30]
00BA3ACF lea     ebx, [eax+1]
00BA3AD2 cmp     ebx, dword ptr [esp+48h+var_2C]
00BA3AD6 ja      loc_BA3C22
00BA3ADC mov     cl, [esp+48h+arg_4]
00BA3AE0 mov     [eax], cl
00BA3AE2 mov     edi, [esi+817Ch]
00BA3AE8 test    edi, edi
00BA3AEA jz      loc_BA3BC1
00BA3AF0 lea     edx, [esp+48h+var_28]
00BA3AF4 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA3BC1 mov     edx, [esi]
00BA3BC3 mov     eax, [edx+58h]
00BA3BC6 mov     edi, ebx
00BA3BC8 sub     edi, ebp
00BA3BCA push    edi
00BA3BCB push    ebp
00BA3BCC mov     ecx, esi
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba3ab1` | opcode 写入/分发指令 |
| `order` | `0xBA3ABB` | struct（复合体 `order`，5×u16=10B；调用点 `call sub_B42060`） |
| `clan_kind` | `0xBA3AE0` | u8 |

## 5. 块内字符串常量（含义取证用）

```
00EECE60
00EE4194
00EE3398
```
