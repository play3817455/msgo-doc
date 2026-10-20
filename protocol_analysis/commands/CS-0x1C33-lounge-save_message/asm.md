# 汇编证据 —— CS-0x1C33-save_message

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA6890 @ `0xba6890`（`0xba6890`..`0xba6af8`）
- 命令名字符串：`)<-_proto_lounge_client::send_save_message( ` @ `0xeed334`

## 2. 组包块切片（游标初始化 → 提交）

```asm
00BA68C0 jz      loc_BA6AF4
00BA68C6 mov     ecx, [edi+0Ch]
00BA68C9 test    ecx, ecx
00BA68CB jz      loc_BA6AF4
00BA68D1 mov     eax, [ecx]
00BA68D3 mov     edx, [eax+78h]
00BA68D6 push    30Eh
00BA68DB call    edx
00BA68DD mov     ebp, eax
00BA68DF mov     eax, [edi+0Ch]
00BA68E2 push    eax
00BA68E3 lea     ecx, [esp+4Ch+var_34]
00BA68E7 call    sub_ABB2F0
00BA68EC lea     ecx, [ebp+30Eh]
00BA68F2 lea     eax, [ebp+2]
00BA68F5 cmp     eax, ecx
00BA68FF mov     [esp+48h+var_30], ebp
00BA6903 mov     dword ptr [esp+48h+var_2C], ecx
00BA6907 ja      loc_BA6AE3
00BA690D mov     edx, [esp+48h+arg_0]
00BA6911 push    301h
00BA6916 lea     ecx, [esp+4Ch+var_30]
00BA691A push    ecx
00BA691B push    edx
00BA691C mov     word ptr [ebp+0], 1C33h
00BA6922 mov     [esp+54h+var_30], eax
00BA6926 call    sub_B02B40
00BA692E test    al, al
00BA6930 jz      loc_BA6AE3
00BA6936 mov     ecx, [esp+48h+var_30]
00BA693A lea     eax, [ecx+4]
00BA693D cmp     eax, dword ptr [esp+48h+var_2C]
00BA6941 ja      loc_BA6AE3
00BA6947 mov     edx, dword ptr [esp+48h+arg_4]
00BA694B mov     [esp+48h+var_30], eax
00BA694F lea     eax, [esp+48h+var_30]
00BA6953 mov     [ecx], edx
00BA6955 push    eax
00BA6956 lea     ecx, [esp+4Ch+arg_8]
00BA695A push    ecx
00BA695B call    sub_B061C0
00BA6963 test    al, al
00BA6965 jz      loc_BA6AE3
00BA696B mov     esi, [edi+82A8h]
00BA6971 test    esi, esi
00BA6973 mov     ebx, [esp+48h+var_30]
00BA6977 jz      loc_BA6A84
00BA697D lea     edx, [esp+48h+var_28]
00BA6981 push    edx
```

> 说明：本切片由 `ex1.txt` 中的整函数反汇编裁剪而成（仅剔除 SEH 序言、trace 打印块与纯粹寄存器搬运），地址与指令原文未改动。

## 3. 发送去向切片（提交之后的实际发送）

```asm
00BA6A84 mov     eax, [edi]
00BA6A86 mov     edx, [eax+58h]
00BA6A89 sub     ebx, ebp
00BA6A8B push    ebx
00BA6A8C push    ebp
00BA6A8D mov     ecx, edi
00BA6A8F call    edx
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub ebx,ebp` 即「游标 − 缓冲首址」）。

## 4. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| opcode | `0xba691c` | opcode 写入/分发指令 |
| `msg` | `0xBA6926` | str |
| `type` | `0xBA6953` | u32 |
| `is_save_db` | `0xBA695B` | u8 |

## 5. 块内字符串常量（含义取证用）

```
00EED334
00EDC7B8
00EDB364
00EE4164
```
