# 汇编证据 —— CS-0x55D6-lounge-clan_text_offer_set

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA0F50 @ `0xba0f50`（`0xba0f50`..`0xba11f9`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_text_offer_set(` @ `0xeec9d8`
- opcode 写入：`0xba0fcc`
- 声明容量：`0x5E`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba0f9a  mov     ebp, eax
  0xba0f9c  mov     eax, [edi+0Ch]
  0xba0f9f  push    eax
  0xba0fa0  lea     ecx, [esp+4Ch+var_34]
  0xba0fa4  call    sub_ABB2F0
  0xba0fa9  lea     ecx, [ebp+5Eh]
  0xba0fac  lea     eax, [ebp+2]
  0xba0faf  cmp     eax, ecx
  0xba0fb1  mov     [esp+48h+var_4], 0
  0xba0fb9  mov     [esp+48h+var_30], ebp
  0xba0fbd  mov     dword ptr [esp+48h+var_2C], ecx
  0xba0fc1  ja      loc_BA11E4
  0xba0fc7  lea     edx, [eax+4]
  0xba0fca  cmp     edx, ecx
  0xba0fcc  mov     word ptr [ebp+0], 55D6h
  0xba0fd2  ja      loc_BA11E4
  0xba0fd8  mov     ecx, [esp+48h+arg_0]
  0xba0fdc  mov     [esp+48h+var_30], edx
  0xba0fe0  push    31h ; '1'
  0xba0fe2  lea     edx, [esp+4Ch+var_30]
  0xba0fe6  mov     [eax], ecx
  0xba0fe8  mov     eax, [esp+4Ch+arg_4]
  0xba0fec  push    edx
  0xba0fed  push    eax
  0xba0fee  call    sub_B02B40   <<< pushN=49(0x31)
  0xba0ff3  add     esp, 0Ch
  0xba0ff6  test    al, al
  0xba0ff8  jz      loc_BA11E4
  0xba0ffe  mov     edx, dword ptr [esp+48h+arg_8]
  0xba1002  push    1Fh
  0xba1004  lea     ecx, [esp+4Ch+var_30]
  0xba1008  push    ecx
  0xba1009  push    edx
  0xba100a  call    sub_B02B40   <<< pushN=31(0x1F)
  0xba100f  add     esp, 0Ch
  0xba1012  test    al, al
  0xba1014  jz      loc_BA11E4
  0xba101a  lea     eax, [esp+48h+var_30]
  0xba101e  push    eax
  0xba101f  lea     ecx, [esp+4Ch+arg_C]
  0xba1023  push    ecx
  0xba1024  call    sub_B061C0
  0xba1029  add     esp, 8
  0xba102c  test    al, al
  0xba102e  jz      loc_BA11E4
  0xba1034  mov     esi, [edi+80C8h]
  0xba103a  test    esi, esi
  0xba103c  mov     ebx, [esp+48h+var_30]
  0xba1040  jz      loc_BA1185
  0xba1046  lea     edx, [esp+48h+var_28]
  0xba104a  push    edx
  0xba104b  call    sub_CA0CE0
  0xba1050  add     esp, 4
  0xba1053  mov     ecx, [edi+8]
  0xba1056  push    offset aProtoLoungeCli_494; ")<-_proto_lounge_client::send_clan_text"...
  0xba105b  push    ecx
  0xba105c  push    offset aId; " (id:"
  0xba1061  push    eax
  0xba1062  push    esi
  0xba1063  mov     byte ptr [esp+5Ch+var_4], 1
  0xba1068  call    sub_B03020
  0xba106d  add     esp, 8
  0xba1070  push    eax
  0xba1071  call    sub_41D990
  0xba1076  add     esp, 8
  0xba1079  mov     ecx, eax
  0xba107b  call    sub_ADC810
  0xba1080  push    eax
  0xba1081  call    sub_41D990
  0xba1086  add     esp, 8
  0xba1089  lea     ecx, [esp+48h+var_28]
  0xba108d  mov     byte ptr [esp+48h+var_4], 0
  0xba1092  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba10a1  push    offset aIsActive; "is_active="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba10ce  push    offset aSubj; "subj=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba1106  push    offset aBody_0; "body=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba1134  push    offset aClanKind; "clan_kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xba114b  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba1187  mov     eax, [edx+58h]
  0xba118a  sub     ebx, ebp
  0xba118c  push    ebx
  0xba118d  push    ebp
  0xba118e  mov     ecx, edi
  0xba1190  call    eax
  0xba1192  test    al, al
  0xba1194  jz      short loc_BA11E4
  0xba1196  mov     eax, [edi+79A8h]
  0xba119c  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA0FCC` | u16 |
| `is_active` | `0xBA0FE6` | u32 |
| `subj` | `0xBA0FEE` | bytes |
| `body` | `0xBA100A` | bytes |
| `clan_kind` | `0xBA1024` | u8 |
