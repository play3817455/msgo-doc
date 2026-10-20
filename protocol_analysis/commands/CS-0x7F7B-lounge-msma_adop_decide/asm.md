# 汇编证据 —— CS-0x7F7B-lounge-msma_adop_decide

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA7090 @ `0xba7090`（`0xba7090`..`0xba723d`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_adop_decide(` @ `0xeed3f4`
- opcode 写入：`0xba7104`
- 声明容量：`0x6`（分配器容量 `push` @ `0xba70d6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba70da  mov     ebp, eax
  0xba70dc  mov     eax, [esi+0Ch]
  0xba70df  push    eax
  0xba70e0  lea     ecx, [esp+44h+var_2C]
  0xba70e4  call    sub_ABB2F0
  0xba70e9  lea     ecx, [ebp+6]
  0xba70ec  lea     eax, [ebp+2]
  0xba70ef  cmp     eax, ecx
  0xba70f1  mov     [esp+40h+var_4], 0
  0xba70f9  ja      loc_BA7228
  0xba70ff  lea     ebx, [eax+4]
  0xba7102  cmp     ebx, ecx
  0xba7104  mov     word ptr [ebp+0], 7F7Bh
  0xba710a  ja      loc_BA7228
  0xba7110  mov     ecx, [esp+40h+arg_0]
  0xba7114  mov     [eax], ecx
  0xba7116  mov     edi, [esi+82C4h]
  0xba711c  test    edi, edi
  0xba711e  jz      loc_BA71C9
  0xba7124  lea     edx, [esp+40h+var_28]
  0xba7128  push    edx
  0xba7129  call    sub_CA0CE0
  0xba712e  add     esp, 4
  0xba7131  mov     ecx, [esi+8]
  0xba7134  push    offset aProtoLoungeCli_590; ")<-_proto_lounge_client::send_msma_adop"...
  0xba7139  push    ecx
  0xba713a  push    offset aId; " (id:"
  0xba713f  push    eax
  0xba7140  push    edi
  0xba7141  mov     byte ptr [esp+54h+var_4], 1
  0xba7146  call    sub_B03020
  0xba714b  add     esp, 8
  0xba714e  push    eax
  0xba714f  call    sub_41D990
  0xba7154  add     esp, 8
  0xba7157  mov     ecx, eax
  0xba7159  call    sub_ADC810
  0xba715e  push    eax
  0xba715f  call    sub_41D990
  0xba7164  add     esp, 8
  0xba7167  lea     ecx, [esp+40h+var_28]
  0xba716b  mov     byte ptr [esp+40h+var_4], 0
  0xba7170  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba717a  push    offset aDeleteWid; "delete_wid="
  0xba718f  push    offset aByte; "]byte"
  0xba7199  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba71cb  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba7104` | u16 |
| `delete_wid` | `0xBA7114` | u32 |
