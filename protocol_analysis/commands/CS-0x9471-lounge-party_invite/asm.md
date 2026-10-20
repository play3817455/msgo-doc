# 汇编证据 —— CS-0x9471-lounge-party_invite

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B91D30 @ `0xb91d30`（`0xb91d30`..`0xb91edd`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_invite(` @ `0xeeb120`
- opcode 写入：`0xb91da4`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb91d76`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb91d7a  mov     ebp, eax
  0xb91d7c  mov     eax, [esi+0Ch]
  0xb91d7f  push    eax
  0xb91d80  lea     ecx, [esp+44h+var_2C]
  0xb91d84  call    sub_ABB2F0
  0xb91d89  lea     ecx, [ebp+6]
  0xb91d8c  lea     eax, [ebp+2]
  0xb91d8f  cmp     eax, ecx
  0xb91d91  mov     [esp+40h+var_4], 0
  0xb91d99  ja      loc_B91EC8
  0xb91d9f  lea     ebx, [eax+4]
  0xb91da2  cmp     ebx, ecx
  0xb91da4  mov     word ptr [ebp+0], 9471h
  0xb91daa  ja      loc_B91EC8
  0xb91db0  mov     ecx, [esp+40h+arg_0]
  0xb91db4  mov     [eax], ecx
  0xb91db6  mov     edi, [esi+7C74h]
  0xb91dbc  test    edi, edi
  0xb91dbe  jz      loc_B91E69
  0xb91dc4  lea     edx, [esp+40h+var_28]
  0xb91dc8  push    edx
  0xb91dc9  call    sub_CA0CE0
  0xb91dce  add     esp, 4
  0xb91dd1  mov     ecx, [esi+8]
  0xb91dd4  push    offset aProtoLoungeCli_507; ")<-_proto_lounge_client::send_party_inv"...
  0xb91dd9  push    ecx
  0xb91dda  push    offset aId; " (id:"
  0xb91ddf  push    eax
  0xb91de0  push    edi
  0xb91de1  mov     byte ptr [esp+54h+var_4], 1
  0xb91de6  call    sub_B03020
  0xb91deb  add     esp, 8
  0xb91dee  push    eax
  0xb91def  call    sub_41D990
  0xb91df4  add     esp, 8
  0xb91df7  mov     ecx, eax
  0xb91df9  call    sub_ADC810
  0xb91dfe  push    eax
  0xb91dff  call    sub_41D990
  0xb91e04  add     esp, 8
  0xb91e07  lea     ecx, [esp+40h+var_28]
  0xb91e0b  mov     byte ptr [esp+40h+var_4], 0
  0xb91e10  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb91e1a  push    offset aPilotId; "pilot_id="
  0xb91e2f  push    offset aByte; "]byte"
  0xb91e39  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb91e6b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb91da4` | u16 |
| `pilot_id` | `0xB91DB4` | u32 |
