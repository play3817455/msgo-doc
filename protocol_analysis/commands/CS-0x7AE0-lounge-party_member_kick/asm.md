# 汇编证据 —— CS-0x7AE0-lounge-party_member_kick

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B924A0 @ `0xb924a0`（`0xb924a0`..`0xb9264d`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_member_kick(` @ `0xeeb1dc`
- opcode 写入：`0xb92514`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb924e6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb924ea  mov     ebp, eax
  0xb924ec  mov     eax, [esi+0Ch]
  0xb924ef  push    eax
  0xb924f0  lea     ecx, [esp+44h+var_2C]
  0xb924f4  call    sub_ABB2F0
  0xb924f9  lea     ecx, [ebp+6]
  0xb924fc  lea     eax, [ebp+2]
  0xb924ff  cmp     eax, ecx
  0xb92501  mov     [esp+40h+var_4], 0
  0xb92509  ja      loc_B92638
  0xb9250f  lea     ebx, [eax+4]
  0xb92512  cmp     ebx, ecx
  0xb92514  mov     word ptr [ebp+0], 7AE0h
  0xb9251a  ja      loc_B92638
  0xb92520  mov     ecx, [esp+40h+arg_0]
  0xb92524  mov     [eax], ecx
  0xb92526  mov     edi, [esi+7CA0h]
  0xb9252c  test    edi, edi
  0xb9252e  jz      loc_B925D9
  0xb92534  lea     edx, [esp+40h+var_28]
  0xb92538  push    edx
  0xb92539  call    sub_CA0CE0
  0xb9253e  add     esp, 4
  0xb92541  mov     ecx, [esi+8]
  0xb92544  push    offset aProtoLoungeCli_582; ")<-_proto_lounge_client::send_party_mem"...
  0xb92549  push    ecx
  0xb9254a  push    offset aId; " (id:"
  0xb9254f  push    eax
  0xb92550  push    edi
  0xb92551  mov     byte ptr [esp+54h+var_4], 1
  0xb92556  call    sub_B03020
  0xb9255b  add     esp, 8
  0xb9255e  push    eax
  0xb9255f  call    sub_41D990
  0xb92564  add     esp, 8
  0xb92567  mov     ecx, eax
  0xb92569  call    sub_ADC810
  0xb9256e  push    eax
  0xb9256f  call    sub_41D990
  0xb92574  add     esp, 8
  0xb92577  lea     ecx, [esp+40h+var_28]
  0xb9257b  mov     byte ptr [esp+40h+var_4], 0
  0xb92580  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9258a  push    offset aPilotId; "pilot_id="
  0xb9259f  push    offset aByte; "]byte"
  0xb925a9  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb925db  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb92514` | u16 |
| `pilot_id` | `0xB92524` | u32 |
