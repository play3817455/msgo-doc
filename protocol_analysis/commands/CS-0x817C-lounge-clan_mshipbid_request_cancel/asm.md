# 汇编证据 —— CS-0x817C-lounge-clan_mshipbid_request_cancel

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9FF00 @ `0xb9ff00`（`0xb9ff00`..`0xba00ae`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_mshipbid_request_cancel(` @ `0xeec824`
- opcode 写入：`0xb9ff74`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb9ff46`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9ff4a  mov     edi, eax
  0xb9ff4c  mov     eax, [esi+0Ch]
  0xb9ff4f  push    eax
  0xb9ff50  lea     ecx, [esp+44h+var_2C]
  0xb9ff54  call    sub_ABB2F0
  0xb9ff59  lea     ecx, [edi+6]
  0xb9ff5c  lea     eax, [edi+2]
  0xb9ff5f  cmp     eax, ecx
  0xb9ff61  mov     [esp+40h+var_4], 0
  0xb9ff69  ja      loc_BA0099
  0xb9ff6f  lea     ebx, [eax+1]
  0xb9ff72  cmp     ebx, ecx
  0xb9ff74  mov     word ptr [edi], 817Ch
  0xb9ff79  ja      loc_BA0099
  0xb9ff7f  mov     cl, [esp+40h+arg_0]
  0xb9ff83  mov     [eax], cl
  0xb9ff85  mov     ebp, [esi+8088h]
  0xb9ff8b  test    ebp, ebp
  0xb9ff8d  jz      loc_BA003A
  0xb9ff93  lea     edx, [esp+40h+var_28]
  0xb9ff97  push    edx
  0xb9ff98  call    sub_CA0CE0
  0xb9ff9d  add     esp, 4
  0xb9ffa0  mov     ecx, [esi+8]
  0xb9ffa3  push    offset aProtoLoungeCli_478; ")<-_proto_lounge_client::send_clan_mshi"...
  0xb9ffa8  push    ecx
  0xb9ffa9  push    offset aId; " (id:"
  0xb9ffae  push    eax
  0xb9ffaf  push    ebp
  0xb9ffb0  mov     byte ptr [esp+54h+var_4], 1
  0xb9ffb5  call    sub_B03020
  0xb9ffba  add     esp, 8
  0xb9ffbd  push    eax
  0xb9ffbe  call    sub_41D990
  0xb9ffc3  add     esp, 8
  0xb9ffc6  mov     ecx, eax
  0xb9ffc8  call    sub_ADC810
  0xb9ffcd  push    eax
  0xb9ffce  call    sub_41D990
  0xb9ffd3  add     esp, 8
  0xb9ffd6  lea     ecx, [esp+40h+var_28]
  0xb9ffda  mov     byte ptr [esp+40h+var_4], 0
  0xb9ffdf  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9ffe9  push    offset aClanKind; "clan_kind="
  0xba0000  push    offset aByte; "]byte"
  0xba000a  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba003c  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9ff74` | u16 |
| `clan_kind` | `0xB9FF83` | u8 |
