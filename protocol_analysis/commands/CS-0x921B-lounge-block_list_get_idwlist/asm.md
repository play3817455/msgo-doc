# 汇编证据 —— CS-0x921B-lounge-block_list_get_idwlist

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9B170 @ `0xb9b170`（`0xb9b170`..`0xb9b2f6`）
- 命令名字符串：`)<-_proto_lounge_client::send_block_list_get_idwlist(` @ `0xeec0c0`
- opcode 写入：`0xb9b1c9`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb9b1b6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9b1ba  mov     edi, eax
  0xb9b1bc  mov     eax, [esi+0Ch]
  0xb9b1bf  push    eax
  0xb9b1c0  lea     ecx, [esp+44h+var_2C]
  0xb9b1c4  call    sub_ABB2F0
  0xb9b1c9  mov     word ptr [edi], 921Bh
  0xb9b1ce  mov     ebp, [esi+7F28h]
  0xb9b1d4  test    ebp, ebp
  0xb9b1d6  mov     [esp+40h+var_4], 0
  0xb9b1de  lea     ebx, [edi+2]
  0xb9b1e1  jz      loc_B9B272
  0xb9b1e7  lea     ecx, [esp+40h+var_28]
  0xb9b1eb  push    ecx
  0xb9b1ec  call    sub_CA0CE0
  0xb9b1f1  add     esp, 4
  0xb9b1f4  mov     edx, [esi+8]
  0xb9b1f7  push    offset aProtoLoungeCli_366; ")<-_proto_lounge_client::send_block_lis"...
  0xb9b1fc  push    edx
  0xb9b1fd  push    offset aId; " (id:"
  0xb9b202  push    eax
  0xb9b203  push    ebp
  0xb9b204  mov     byte ptr [esp+54h+var_4], 1
  0xb9b209  call    sub_B03020
  0xb9b20e  add     esp, 8
  0xb9b211  push    eax
  0xb9b212  call    sub_41D990
  0xb9b217  add     esp, 8
  0xb9b21a  mov     ecx, eax
  0xb9b21c  call    sub_ADC810
  0xb9b221  push    eax
  0xb9b222  call    sub_41D990
  0xb9b227  add     esp, 8
  0xb9b22a  lea     ecx, [esp+40h+var_28]
  0xb9b22e  mov     byte ptr [esp+40h+var_4], 0
  0xb9b233  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9b238  push    offset aByte; "]byte"
  0xb9b242  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb9b274  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9b1c9` | u16 |
