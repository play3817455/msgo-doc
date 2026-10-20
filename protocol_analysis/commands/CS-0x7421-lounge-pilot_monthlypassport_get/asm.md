# 汇编证据 —— CS-0x7421-lounge-pilot_monthlypassport_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8F340 @ `0xb8f340`（`0xb8f340`..`0xb8f4c6`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_monthlypassport_get(` @ `0xeeace0`
- opcode 写入：`0xb8f399`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb8f386`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8f38a  mov     edi, eax
  0xb8f38c  mov     eax, [esi+0Ch]
  0xb8f38f  push    eax
  0xb8f390  lea     ecx, [esp+44h+var_2C]
  0xb8f394  call    sub_ABB2F0
  0xb8f399  mov     word ptr [edi], 7421h
  0xb8f39e  mov     ebp, [esi+7BB0h]
  0xb8f3a4  test    ebp, ebp
  0xb8f3a6  mov     [esp+40h+var_4], 0
  0xb8f3ae  lea     ebx, [edi+2]
  0xb8f3b1  jz      loc_B8F442
  0xb8f3b7  lea     ecx, [esp+40h+var_28]
  0xb8f3bb  push    ecx
  0xb8f3bc  call    sub_CA0CE0
  0xb8f3c1  add     esp, 4
  0xb8f3c4  mov     edx, [esi+8]
  0xb8f3c7  push    offset aProtoLoungeCli_560; ")<-_proto_lounge_client::send_pilot_mon"...
  0xb8f3cc  push    edx
  0xb8f3cd  push    offset aId; " (id:"
  0xb8f3d2  push    eax
  0xb8f3d3  push    ebp
  0xb8f3d4  mov     byte ptr [esp+54h+var_4], 1
  0xb8f3d9  call    sub_B03020
  0xb8f3de  add     esp, 8
  0xb8f3e1  push    eax
  0xb8f3e2  call    sub_41D990
  0xb8f3e7  add     esp, 8
  0xb8f3ea  mov     ecx, eax
  0xb8f3ec  call    sub_ADC810
  0xb8f3f1  push    eax
  0xb8f3f2  call    sub_41D990
  0xb8f3f7  add     esp, 8
  0xb8f3fa  lea     ecx, [esp+40h+var_28]
  0xb8f3fe  mov     byte ptr [esp+40h+var_4], 0
  0xb8f403  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8f408  push    offset aByte; "]byte"
  0xb8f412  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8f444  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8f399` | u16 |
