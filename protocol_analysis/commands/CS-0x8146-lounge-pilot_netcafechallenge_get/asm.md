# 汇编证据 —— CS-0x8146-lounge-pilot_netcafechallenge_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8E9E0 @ `0xb8e9e0`（`0xb8e9e0`..`0xb8eb63`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_netcafechallenge_get(` @ `0xeeab74`
- opcode 写入：`0xb8ea39`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb8ea26`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8ea2a  mov     edi, eax
  0xb8ea2c  mov     eax, [esi+0Ch]
  0xb8ea2f  push    eax
  0xb8ea30  lea     ecx, [esp+44h+var_2C]
  0xb8ea34  call    sub_ABB2F0
  0xb8ea39  mov     word ptr [edi], 8146h
  0xb8ea3e  mov     ebp, [esi+7B70h]
  0xb8ea44  test    ebp, ebp
  0xb8ea46  mov     [esp+40h+var_4], 0
  0xb8ea4e  lea     ebx, [edi+2]
  0xb8ea51  jz      loc_B8EAE2
  0xb8ea57  lea     ecx, [esp+40h+var_28]
  0xb8ea5b  push    ecx
  0xb8ea5c  call    sub_CA0CE0
  0xb8ea61  add     esp, 4
  0xb8ea64  mov     edx, [esi+8]
  0xb8ea67  push    offset aProtoLoungeCli_521; ")<-_proto_lounge_client::send_pilot_net"...
  0xb8ea6c  push    edx
  0xb8ea6d  push    offset aId; " (id:"
  0xb8ea72  push    eax
  0xb8ea73  push    ebp
  0xb8ea74  mov     byte ptr [esp+54h+var_4], 1
  0xb8ea79  call    sub_B03020
  0xb8ea7e  add     esp, 8
  0xb8ea81  push    eax
  0xb8ea82  call    sub_41D990
  0xb8ea87  add     esp, 8
  0xb8ea8a  mov     ecx, eax
  0xb8ea8c  call    sub_ADC810
  0xb8ea91  push    eax
  0xb8ea92  call    sub_41D990
  0xb8ea97  add     esp, 8
  0xb8ea9a  lea     ecx, [esp+40h+var_28]
  0xb8ea9e  mov     byte ptr [esp+40h+var_4], 0
  0xb8eaa3  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8eaa8  push    offset aByte; "]byte"
  0xb8eab2  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8eae4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8ea39` | u16 |
