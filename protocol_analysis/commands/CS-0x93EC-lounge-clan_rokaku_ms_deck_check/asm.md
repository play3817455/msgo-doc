# 汇编证据 —— CS-0x93EC-lounge-clan_rokaku_ms_deck_check

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA2F40 @ `0xba2f40`（`0xba2f40`..`0xba30c6`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_rokaku_ms_deck_check(` @ `0xeecd20`
- opcode 写入：`0xba2f99`
- 声明容量：`0x2`（分配器容量 `push` @ `0xba2f86`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba2f8a  mov     edi, eax
  0xba2f8c  mov     eax, [esi+0Ch]
  0xba2f8f  push    eax
  0xba2f90  lea     ecx, [esp+44h+var_2C]
  0xba2f94  call    sub_ABB2F0
  0xba2f99  mov     word ptr [edi], 93ECh
  0xba2f9e  mov     ebp, [esi+814Ch]
  0xba2fa4  test    ebp, ebp
  0xba2fa6  mov     [esp+40h+var_4], 0
  0xba2fae  lea     ebx, [edi+2]
  0xba2fb1  jz      loc_BA3042
  0xba2fb7  lea     ecx, [esp+40h+var_28]
  0xba2fbb  push    ecx
  0xba2fbc  call    sub_CA0CE0
  0xba2fc1  add     esp, 4
  0xba2fc4  mov     edx, [esi+8]
  0xba2fc7  push    offset aProtoLoungeCli_496; ")<-_proto_lounge_client::send_clan_roka"...
  0xba2fcc  push    edx
  0xba2fcd  push    offset aId; " (id:"
  0xba2fd2  push    eax
  0xba2fd3  push    ebp
  0xba2fd4  mov     byte ptr [esp+54h+var_4], 1
  0xba2fd9  call    sub_B03020
  0xba2fde  add     esp, 8
  0xba2fe1  push    eax
  0xba2fe2  call    sub_41D990
  0xba2fe7  add     esp, 8
  0xba2fea  mov     ecx, eax
  0xba2fec  call    sub_ADC810
  0xba2ff1  push    eax
  0xba2ff2  call    sub_41D990
  0xba2ff7  add     esp, 8
  0xba2ffa  lea     ecx, [esp+40h+var_28]
  0xba2ffe  mov     byte ptr [esp+40h+var_4], 0
  0xba3003  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba3008  push    offset aByte; "]byte"
  0xba3012  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba3044  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba2f99` | u16 |
