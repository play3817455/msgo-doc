# 汇编证据 —— CS-0x498B-lounge-pilot_rename

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8A310 @ `0xb8a310`（`0xb8a310`..`0xb8a630`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_rename(` @ `0xeea370`
- opcode 写入：`0xb8a389`
- 声明容量：`0x4A`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8a357  mov     ebp, eax
  0xb8a359  mov     eax, [edi+0Ch]
  0xb8a35c  push    eax
  0xb8a35d  lea     ecx, [esp+4Ch+var_34]
  0xb8a361  call    sub_ABB2F0
  0xb8a366  lea     ecx, [ebp+4Ah]
  0xb8a369  lea     eax, [ebp+2]
  0xb8a36c  cmp     eax, ecx
  0xb8a36e  mov     [esp+48h+var_4], 0
  0xb8a376  mov     [esp+48h+var_30], ebp
  0xb8a37a  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8a37e  ja      loc_B8A61B
  0xb8a384  lea     edx, [eax+4]
  0xb8a387  cmp     edx, ecx
  0xb8a389  mov     word ptr [ebp+0], 498Bh
  0xb8a38f  ja      loc_B8A61B
  0xb8a395  mov     esi, [esp+48h+arg_0]
  0xb8a399  mov     [eax], esi
  0xb8a39b  mov     eax, edx
  0xb8a39d  lea     edx, [eax+4]
  0xb8a3a0  cmp     edx, ecx
  0xb8a3a2  ja      loc_B8A61B
  0xb8a3a8  mov     ecx, [esp+48h+arg_4]
  0xb8a3ac  mov     [esp+48h+var_30], edx
  0xb8a3b0  lea     edx, [esp+48h+var_30]
  0xb8a3b4  mov     [eax], ecx
  0xb8a3b6  push    edx
  0xb8a3b7  lea     eax, [esp+4Ch+arg_8]
  0xb8a3bb  push    eax
  0xb8a3bc  call    sub_B02D80
  0xb8a3c1  add     esp, 8
  0xb8a3c4  test    al, al
  0xb8a3c6  jz      loc_B8A61B
  0xb8a3cc  mov     edx, [esp+48h+arg_C]
  0xb8a3d0  push    19h
  0xb8a3d2  lea     ecx, [esp+4Ch+var_30]
  0xb8a3d6  push    ecx
  0xb8a3d7  push    edx
  0xb8a3d8  call    sub_B02B40   <<< pushN=25(0x19)
  0xb8a3dd  add     esp, 0Ch
  0xb8a3e0  test    al, al
  0xb8a3e2  jz      loc_B8A61B
  0xb8a3e8  mov     ecx, dword ptr [esp+48h+arg_10]
  0xb8a3ec  push    19h
  0xb8a3ee  lea     eax, [esp+4Ch+var_30]
  0xb8a3f2  push    eax
  0xb8a3f3  push    ecx
  0xb8a3f4  call    sub_B02B40   <<< pushN=25(0x19)
  0xb8a3f9  add     esp, 0Ch
  0xb8a3fc  test    al, al
  0xb8a3fe  jz      loc_B8A61B
  0xb8a404  lea     edx, [esp+48h+var_30]
  0xb8a408  push    edx
  0xb8a409  lea     eax, [esp+4Ch+arg_14]
  0xb8a40d  push    eax
  0xb8a40e  call    sub_B061C0
  0xb8a413  add     esp, 8
  0xb8a416  test    al, al
  0xb8a418  jz      loc_B8A61B
  0xb8a41e  mov     esi, [edi+79F4h]
  0xb8a424  test    esi, esi
  0xb8a426  mov     ebx, [esp+48h+var_30]
  0xb8a42a  jz      loc_B8A5BF
  0xb8a430  lea     ecx, [esp+48h+var_28]
  0xb8a434  push    ecx
  0xb8a435  call    sub_CA0CE0
  0xb8a43a  add     esp, 4
  0xb8a43d  mov     edx, [edi+8]
  0xb8a440  push    offset aProtoLoungeCli_390; ")<-_proto_lounge_client::send_pilot_ren"...
  0xb8a445  push    edx
  0xb8a446  push    offset aId; " (id:"
  0xb8a44b  push    eax
  0xb8a44c  push    esi
  0xb8a44d  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8a452  call    sub_B03020
  0xb8a457  add     esp, 8
  0xb8a45a  push    eax
  0xb8a45b  call    sub_41D990
  0xb8a460  add     esp, 8
  0xb8a463  mov     ecx, eax
  0xb8a465  call    sub_ADC810
  0xb8a46a  push    eax
  0xb8a46b  call    sub_41D990
  0xb8a470  add     esp, 8
  0xb8a473  lea     ecx, [esp+48h+var_28]
  0xb8a477  mov     byte ptr [esp+48h+var_4], 0
  0xb8a47c  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8a48b  push    offset aTroops; "troops="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a4b3  push    offset aSlot; "slot="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a4db  push    offset aPilotId; "pilot_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a508  push    offset aBefPilotName; "bef_pilot_name=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a540  push    offset aPilotName; "pilot_name=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a56e  push    offset aIsCheckOnly; "is_check_only="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8a585  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8a5c1  mov     eax, [edx+58h]
  0xb8a5c4  sub     ebx, ebp
  0xb8a5c6  push    ebx
  0xb8a5c7  push    ebp
  0xb8a5c8  mov     ecx, edi
  0xb8a5ca  call    eax
  0xb8a5cc  test    al, al
  0xb8a5ce  jz      short loc_B8A61B
  0xb8a5d0  mov     eax, [edi+79A8h]
  0xb8a5d6  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8A389` | u16 |
| `troops` | `0xB8A399` | u32 |
| `slot` | `0xB8A3B4` | u32 |
| `pilot_id` | `0xB8A3BC` | u32 |
| `bef_pilot_name` | `0xB8A3D8` | bytes |
| `pilot_name` | `0xB8A3F4` | bytes |
| `is_check_only` | `0xB8A40E` | u8 |
