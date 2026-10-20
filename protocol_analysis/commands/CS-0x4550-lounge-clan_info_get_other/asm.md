# 汇编证据 —— CS-0x4550-lounge-clan_info_get_other

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9F300 @ `0xb9f300`（`0xb9f300`..`0xb9f4e8`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_info_get_other(` @ `0xeec6f8`
- opcode 写入：`0xb9f374`
- 声明容量：`0xA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9f34a  mov     ebp, eax
  0xb9f34c  mov     eax, [esi+0Ch]
  0xb9f34f  push    eax
  0xb9f350  lea     ecx, [esp+44h+var_2C]
  0xb9f354  call    sub_ABB2F0
  0xb9f359  lea     eax, [ebp+0Ah]
  0xb9f35c  lea     ecx, [ebp+2]
  0xb9f35f  cmp     ecx, eax
  0xb9f361  mov     [esp+40h+var_4], 0
  0xb9f369  ja      loc_B9F4D3
  0xb9f36f  lea     edx, [ecx+4]
  0xb9f372  cmp     edx, eax
  0xb9f374  mov     word ptr [ebp+0], 4550h
  0xb9f37a  ja      loc_B9F4D3
  0xb9f380  mov     edi, dword ptr [esp+40h+arg_0]
  0xb9f384  lea     ebx, [edx+1]
  0xb9f387  cmp     ebx, eax
  0xb9f389  mov     [ecx], edi
  0xb9f38b  ja      loc_B9F4D3
  0xb9f391  mov     cl, [esp+40h+arg_4]
  0xb9f395  mov     [edx], cl
  0xb9f397  mov     edi, [esi+8050h]
  0xb9f39d  test    edi, edi
  0xb9f39f  jz      loc_B9F474
  0xb9f3a5  lea     edx, [esp+40h+var_28]
  0xb9f3a9  push    edx
  0xb9f3aa  call    sub_CA0CE0
  0xb9f3af  add     esp, 4
  0xb9f3b2  mov     ecx, [esi+8]
  0xb9f3b5  push    offset aProtoLoungeCli_474; ")<-_proto_lounge_client::send_clan_info"...
  0xb9f3ba  push    ecx
  0xb9f3bb  push    offset aId; " (id:"
  0xb9f3c0  push    eax
  0xb9f3c1  push    edi
  0xb9f3c2  mov     byte ptr [esp+54h+var_4], 1
  0xb9f3c7  call    sub_B03020
  0xb9f3cc  add     esp, 8
  0xb9f3cf  push    eax
  0xb9f3d0  call    sub_41D990
  0xb9f3d5  add     esp, 8
  0xb9f3d8  mov     ecx, eax
  0xb9f3da  call    sub_ADC810
  0xb9f3df  push    eax
  0xb9f3e0  call    sub_41D990
  0xb9f3e5  add     esp, 8
  0xb9f3e8  lea     ecx, [esp+40h+var_28]
  0xb9f3ec  mov     byte ptr [esp+40h+var_4], 0
  0xb9f3f1  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9f400  push    offset aClanId; "clan_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9f423  push    offset aClanKind; "clan_kind="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb9f43a  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb9f476  mov     eax, [edx+58h]
  0xb9f479  sub     ebx, ebp
  0xb9f47b  push    ebx
  0xb9f47c  push    ebp
  0xb9f47d  mov     ecx, esi
  0xb9f47f  call    eax
  0xb9f481  test    al, al
  0xb9f483  jz      short loc_B9F4D3
  0xb9f485  mov     eax, [esi+79A8h]
  0xb9f48b  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9F374` | u16 |
| `clan_id` | `0xB9F389` | u32 |
| `clan_kind` | `0xB9F395` | u8 |
