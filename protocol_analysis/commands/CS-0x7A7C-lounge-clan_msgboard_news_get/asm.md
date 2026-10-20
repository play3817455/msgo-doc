# 汇编证据 —— CS-0x7A7C-lounge-clan_msgboard_news_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA1C30 @ `0xba1c30`（`0xba1c30`..`0xba1dde`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_msgboard_news_get(` @ `0xeecb14`
- opcode 写入：`0xba1ca4`
- 声明容量：`0x6`（分配器容量 `push` @ `0xba1c76`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba1c7a  mov     edi, eax
  0xba1c7c  mov     eax, [esi+0Ch]
  0xba1c7f  push    eax
  0xba1c80  lea     ecx, [esp+44h+var_2C]
  0xba1c84  call    sub_ABB2F0
  0xba1c89  lea     ecx, [edi+6]
  0xba1c8c  lea     eax, [edi+2]
  0xba1c8f  cmp     eax, ecx
  0xba1c91  mov     [esp+40h+var_4], 0
  0xba1c99  ja      loc_BA1DC9
  0xba1c9f  lea     ebx, [eax+1]
  0xba1ca2  cmp     ebx, ecx
  0xba1ca4  mov     word ptr [edi], 7A7Ch
  0xba1ca9  ja      loc_BA1DC9
  0xba1caf  mov     cl, [esp+40h+arg_0]
  0xba1cb3  mov     [eax], cl
  0xba1cb5  mov     ebp, [esi+80FCh]
  0xba1cbb  test    ebp, ebp
  0xba1cbd  jz      loc_BA1D6A
  0xba1cc3  lea     edx, [esp+40h+var_28]
  0xba1cc7  push    edx
  0xba1cc8  call    sub_CA0CE0
  0xba1ccd  add     esp, 4
  0xba1cd0  mov     ecx, [esi+8]
  0xba1cd3  push    offset aProtoLoungeCli_487; ")<-_proto_lounge_client::send_clan_msgb"...
  0xba1cd8  push    ecx
  0xba1cd9  push    offset aId; " (id:"
  0xba1cde  push    eax
  0xba1cdf  push    ebp
  0xba1ce0  mov     byte ptr [esp+54h+var_4], 1
  0xba1ce5  call    sub_B03020
  0xba1cea  add     esp, 8
  0xba1ced  push    eax
  0xba1cee  call    sub_41D990
  0xba1cf3  add     esp, 8
  0xba1cf6  mov     ecx, eax
  0xba1cf8  call    sub_ADC810
  0xba1cfd  push    eax
  0xba1cfe  call    sub_41D990
  0xba1d03  add     esp, 8
  0xba1d06  lea     ecx, [esp+40h+var_28]
  0xba1d0a  mov     byte ptr [esp+40h+var_4], 0
  0xba1d0f  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba1d19  push    offset aClanKind; "clan_kind="
  0xba1d30  push    offset aByte; "]byte"
  0xba1d3a  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba1d6c  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba1ca4` | u16 |
| `clan_kind` | `0xBA1CB3` | u8 |
