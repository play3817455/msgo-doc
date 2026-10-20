# 汇编证据 —— CS-0x4E94-lounge-pilot_avatar_parts_unlock

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8BAF0 @ `0xb8baf0`（`0xb8baf0`..`0xb8bcd3`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_avatar_parts_unlock(` @ `0xeea5e4`
- opcode 写入：`0xb8bb64`
- 声明容量：`0xA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8bb3a  mov     ebp, eax
  0xb8bb3c  mov     eax, [edi+0Ch]
  0xb8bb3f  push    eax
  0xb8bb40  lea     ecx, [esp+44h+var_2C]
  0xb8bb44  call    sub_ABB2F0
  0xb8bb49  lea     ecx, [ebp+0Ah]
  0xb8bb4c  lea     eax, [ebp+2]
  0xb8bb4f  cmp     eax, ecx
  0xb8bb51  mov     [esp+40h+var_4], 0
  0xb8bb59  ja      loc_B8BCBE
  0xb8bb5f  lea     edx, [eax+4]
  0xb8bb62  cmp     edx, ecx
  0xb8bb64  mov     word ptr [ebp+0], 4E94h
  0xb8bb6a  ja      loc_B8BCBE
  0xb8bb70  mov     esi, [esp+40h+arg_0]
  0xb8bb74  lea     ebx, [edx+4]
  0xb8bb77  cmp     ebx, ecx
  0xb8bb79  mov     [eax], esi
  0xb8bb7b  ja      loc_B8BCBE
  0xb8bb81  mov     ecx, [esp+40h+arg_4]
  0xb8bb85  mov     [edx], ecx
  0xb8bb87  mov     esi, [edi+7A68h]
  0xb8bb8d  test    esi, esi
  0xb8bb8f  jz      loc_B8BC62
  0xb8bb95  lea     edx, [esp+40h+var_28]
  0xb8bb99  push    edx
  0xb8bb9a  call    sub_CA0CE0
  0xb8bb9f  add     esp, 4
  0xb8bba2  mov     ecx, [edi+8]
  0xb8bba5  push    offset aProtoLoungeCli_584; ")<-_proto_lounge_client::send_pilot_ava"...
  0xb8bbaa  push    ecx
  0xb8bbab  push    offset aId; " (id:"
  0xb8bbb0  push    eax
  0xb8bbb1  push    esi
  0xb8bbb2  mov     byte ptr [esp+54h+var_4], 1
  0xb8bbb7  call    sub_B03020
  0xb8bbbc  add     esp, 8
  0xb8bbbf  push    eax
  0xb8bbc0  call    sub_41D990
  0xb8bbc5  add     esp, 8
  0xb8bbc8  mov     ecx, eax
  0xb8bbca  call    sub_ADC810
  0xb8bbcf  push    eax
  0xb8bbd0  call    sub_41D990
  0xb8bbd5  add     esp, 8
  0xb8bbd8  lea     ecx, [esp+40h+var_28]
  0xb8bbdc  mov     byte ptr [esp+40h+var_4], 0
  0xb8bbe1  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8bbf0  push    offset aKind; "kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8bc13  push    offset aCustomId; "custom_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8bc28  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8bc64  mov     eax, [edx+58h]
  0xb8bc67  sub     ebx, ebp
  0xb8bc69  push    ebx
  0xb8bc6a  push    ebp
  0xb8bc6b  mov     ecx, edi
  0xb8bc6d  call    eax
  0xb8bc6f  test    al, al
  0xb8bc71  jz      short loc_B8BCBE
  0xb8bc73  mov     eax, [edi+79A8h]
  0xb8bc79  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8BB64` | u16 |
| `kind` | `0xB8BB79` | u32 |
| `custom_id` | `0xB8BB85` | u32 |
