# 汇编证据 —— CS-0x7ABC-lounge-btlroom_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8F680 @ `0xb8f680`（`0xb8f680`..`0xb8f82d`）
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_get(` @ `0xeead58`
- opcode 写入：`0xb8f6f4`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb8f6c6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8f6ca  mov     ebp, eax
  0xb8f6cc  mov     eax, [esi+0Ch]
  0xb8f6cf  push    eax
  0xb8f6d0  lea     ecx, [esp+44h+var_2C]
  0xb8f6d4  call    sub_ABB2F0
  0xb8f6d9  lea     ecx, [ebp+6]
  0xb8f6dc  lea     eax, [ebp+2]
  0xb8f6df  cmp     eax, ecx
  0xb8f6e1  mov     [esp+40h+var_4], 0
  0xb8f6e9  ja      loc_B8F818
  0xb8f6ef  lea     ebx, [eax+4]
  0xb8f6f2  cmp     ebx, ecx
  0xb8f6f4  mov     word ptr [ebp+0], 7ABCh
  0xb8f6fa  ja      loc_B8F818
  0xb8f700  mov     ecx, [esp+40h+arg_0]
  0xb8f704  mov     [eax], ecx
  0xb8f706  mov     edi, [esi+7BC8h]
  0xb8f70c  test    edi, edi
  0xb8f70e  jz      loc_B8F7B9
  0xb8f714  lea     edx, [esp+40h+var_28]
  0xb8f718  push    edx
  0xb8f719  call    sub_CA0CE0
  0xb8f71e  add     esp, 4
  0xb8f721  mov     ecx, [esi+8]
  0xb8f724  push    offset aProtoLoungeCli_562; ")<-_proto_lounge_client::send_btlroom_g"...
  0xb8f729  push    ecx
  0xb8f72a  push    offset aId; " (id:"
  0xb8f72f  push    eax
  0xb8f730  push    edi
  0xb8f731  mov     byte ptr [esp+54h+var_4], 1
  0xb8f736  call    sub_B03020
  0xb8f73b  add     esp, 8
  0xb8f73e  push    eax
  0xb8f73f  call    sub_41D990
  0xb8f744  add     esp, 8
  0xb8f747  mov     ecx, eax
  0xb8f749  call    sub_ADC810
  0xb8f74e  push    eax
  0xb8f74f  call    sub_41D990
  0xb8f754  add     esp, 8
  0xb8f757  lea     ecx, [esp+40h+var_28]
  0xb8f75b  mov     byte ptr [esp+40h+var_4], 0
  0xb8f760  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8f76a  push    offset aRoomType; "room_type="
  0xb8f77f  push    offset aByte; "]byte"
  0xb8f789  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8f7bb  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8f6f4` | u16 |
| `room_type` | `0xB8F704` | u32 |
