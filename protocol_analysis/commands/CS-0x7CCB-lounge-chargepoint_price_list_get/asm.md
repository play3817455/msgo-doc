# 汇编证据 —— CS-0x7CCB-lounge-chargepoint_price_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8C980 @ `0xb8c980`（`0xb8c980`..`0xb8cb03`）
- 命令名字符串：`)<-_proto_lounge_client::send_chargepoint_price_list_get(` @ `0xeea7bc`
- opcode 写入：`0xb8c9d9`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb8c9c6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8c9ca  mov     edi, eax
  0xb8c9cc  mov     eax, [esi+0Ch]
  0xb8c9cf  push    eax
  0xb8c9d0  lea     ecx, [esp+44h+var_2C]
  0xb8c9d4  call    sub_ABB2F0
  0xb8c9d9  mov     word ptr [edi], 7CCBh
  0xb8c9de  mov     ebp, [esi+7AB4h]
  0xb8c9e4  test    ebp, ebp
  0xb8c9e6  mov     [esp+40h+var_4], 0
  0xb8c9ee  lea     ebx, [edi+2]
  0xb8c9f1  jz      loc_B8CA82
  0xb8c9f7  lea     ecx, [esp+40h+var_28]
  0xb8c9fb  push    ecx
  0xb8c9fc  call    sub_CA0CE0
  0xb8ca01  add     esp, 4
  0xb8ca04  mov     edx, [esi+8]
  0xb8ca07  push    offset aProtoLoungeCli_392; ")<-_proto_lounge_client::send_chargepoi"...
  0xb8ca0c  push    edx
  0xb8ca0d  push    offset aId; " (id:"
  0xb8ca12  push    eax
  0xb8ca13  push    ebp
  0xb8ca14  mov     byte ptr [esp+54h+var_4], 1
  0xb8ca19  call    sub_B03020
  0xb8ca1e  add     esp, 8
  0xb8ca21  push    eax
  0xb8ca22  call    sub_41D990
  0xb8ca27  add     esp, 8
  0xb8ca2a  mov     ecx, eax
  0xb8ca2c  call    sub_ADC810
  0xb8ca31  push    eax
  0xb8ca32  call    sub_41D990
  0xb8ca37  add     esp, 8
  0xb8ca3a  lea     ecx, [esp+40h+var_28]
  0xb8ca3e  mov     byte ptr [esp+40h+var_4], 0
  0xb8ca43  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8ca48  push    offset aByte; "]byte"
  0xb8ca52  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8ca84  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8c9d9` | u16 |
