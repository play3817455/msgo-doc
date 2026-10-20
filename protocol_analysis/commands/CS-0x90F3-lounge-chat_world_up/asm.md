# 汇编证据 —— CS-0x90F3-lounge-chat_world_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8D010 @ `0xb8d010`（`0xb8d010`..`0xb8d1ef`）
- 命令名字符串：`)<-_proto_lounge_client::send_chat_world_up(` @ `0xeea890`
- opcode 写入：`0xb8d09c`
- 声明容量：`0xBA`（分配器容量 `push` @ `0xb8d056`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8d05d  mov     edi, eax
  0xb8d05f  mov     eax, [esi+0Ch]
  0xb8d062  push    eax
  0xb8d063  lea     ecx, [esp+4Ch+var_34]
  0xb8d067  call    sub_ABB2F0
  0xb8d06c  lea     ecx, [edi+0BAh]
  0xb8d072  lea     eax, [edi+2]
  0xb8d075  cmp     eax, ecx
  0xb8d077  mov     [esp+48h+var_4], 0
  0xb8d07f  mov     [esp+48h+var_30], edi
  0xb8d083  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8d087  ja      loc_B8D1DA
  0xb8d08d  mov     edx, [esp+48h+arg_0]
  0xb8d091  push    0B5h
  0xb8d096  lea     ecx, [esp+4Ch+var_30]
  0xb8d09a  push    ecx
  0xb8d09b  push    edx
  0xb8d09c  mov     word ptr [edi], 90F3h
  0xb8d0a1  mov     [esp+54h+var_30], eax
  0xb8d0a5  call    sub_B02B40
  0xb8d0aa  add     esp, 0Ch
  0xb8d0ad  test    al, al
  0xb8d0af  jz      loc_B8D1DA
  0xb8d0b5  mov     ebp, [esi+7ADCh]
  0xb8d0bb  test    ebp, ebp
  0xb8d0bd  mov     ebx, [esp+48h+var_30]
  0xb8d0c1  jz      loc_B8D17C
  0xb8d0c7  lea     eax, [esp+48h+var_28]
  0xb8d0cb  push    eax
  0xb8d0cc  call    sub_CA0CE0
  0xb8d0d1  add     esp, 4
  0xb8d0d4  mov     ecx, [esi+8]
  0xb8d0d7  push    offset aProtoLoungeCli_412; ")<-_proto_lounge_client::send_chat_worl"...
  0xb8d0dc  push    ecx
  0xb8d0dd  push    offset aId; " (id:"
  0xb8d0e2  push    eax
  0xb8d0e3  push    ebp
  0xb8d0e4  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8d0e9  call    sub_B03020
  0xb8d0ee  add     esp, 8
  0xb8d0f1  push    eax
  0xb8d0f2  call    sub_41D990
  0xb8d0f7  add     esp, 8
  0xb8d0fa  mov     ecx, eax
  0xb8d0fc  call    sub_ADC810
  0xb8d101  push    eax
  0xb8d102  call    sub_41D990
  0xb8d107  add     esp, 8
  0xb8d10a  lea     ecx, [esp+48h+var_28]
  0xb8d10e  mov     byte ptr [esp+48h+var_4], 0
  0xb8d113  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8d11c  push    offset asc_EDAD54; "\""
  0xb8d122  push    offset aMsg; "msg=\""
  0xb8d142  push    offset aByte; "]byte"
  0xb8d14c  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8d17e  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8d09c` | u16 |
| `msg` | `0xB8D0A5` | bytes |
