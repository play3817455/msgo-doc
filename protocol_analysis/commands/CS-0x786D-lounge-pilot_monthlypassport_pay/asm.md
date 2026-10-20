# 汇编证据 —— CS-0x786D-lounge-pilot_monthlypassport_pay

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8F4D0 @ `0xb8f4d0`（`0xb8f4d0`..`0xb8f67e`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_monthlypassport_pay(` @ `0xeead1c`
- opcode 写入：`0xb8f544`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb8f516`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8f51a  mov     edi, eax
  0xb8f51c  mov     eax, [esi+0Ch]
  0xb8f51f  push    eax
  0xb8f520  lea     ecx, [esp+44h+var_2C]
  0xb8f524  call    sub_ABB2F0
  0xb8f529  lea     ecx, [edi+6]
  0xb8f52c  lea     eax, [edi+2]
  0xb8f52f  cmp     eax, ecx
  0xb8f531  mov     [esp+40h+var_4], 0
  0xb8f539  ja      loc_B8F669
  0xb8f53f  lea     ebx, [eax+1]
  0xb8f542  cmp     ebx, ecx
  0xb8f544  mov     word ptr [edi], 786Dh
  0xb8f549  ja      loc_B8F669
  0xb8f54f  mov     cl, [esp+40h+arg_0]
  0xb8f553  mov     [eax], cl
  0xb8f555  mov     ebp, [esi+7BB8h]
  0xb8f55b  test    ebp, ebp
  0xb8f55d  jz      loc_B8F60A
  0xb8f563  lea     edx, [esp+40h+var_28]
  0xb8f567  push    edx
  0xb8f568  call    sub_CA0CE0
  0xb8f56d  add     esp, 4
  0xb8f570  mov     ecx, [esi+8]
  0xb8f573  push    offset aProtoLoungeCli_591; ")<-_proto_lounge_client::send_pilot_mon"...
  0xb8f578  push    ecx
  0xb8f579  push    offset aId; " (id:"
  0xb8f57e  push    eax
  0xb8f57f  push    ebp
  0xb8f580  mov     byte ptr [esp+54h+var_4], 1
  0xb8f585  call    sub_B03020
  0xb8f58a  add     esp, 8
  0xb8f58d  push    eax
  0xb8f58e  call    sub_41D990
  0xb8f593  add     esp, 8
  0xb8f596  mov     ecx, eax
  0xb8f598  call    sub_ADC810
  0xb8f59d  push    eax
  0xb8f59e  call    sub_41D990
  0xb8f5a3  add     esp, 8
  0xb8f5a6  lea     ecx, [esp+40h+var_28]
  0xb8f5aa  mov     byte ptr [esp+40h+var_4], 0
  0xb8f5af  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8f5b9  push    offset aPeriodPath; "period_path="
  0xb8f5d0  push    offset aByte; "]byte"
  0xb8f5da  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8f60c  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8f544` | u16 |
| `period_path` | `0xB8F553` | u8 |
