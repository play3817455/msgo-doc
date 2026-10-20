# 汇编证据 —— CS-0x7609-lounge-dailycup_team_info_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA6550 @ `0xba6550`（`0xba6550`..`0xba66fd`）
- 命令名字符串：`)<-_proto_lounge_client::send_dailycup_team_info_get(` @ `0xeed2c8`
- opcode 写入：`0xba65c4`
- 声明容量：`0x6`（分配器容量 `push` @ `0xba6596`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba659a  mov     ebp, eax
  0xba659c  mov     eax, [esi+0Ch]
  0xba659f  push    eax
  0xba65a0  lea     ecx, [esp+44h+var_2C]
  0xba65a4  call    sub_ABB2F0
  0xba65a9  lea     ecx, [ebp+6]
  0xba65ac  lea     eax, [ebp+2]
  0xba65af  cmp     eax, ecx
  0xba65b1  mov     [esp+40h+var_4], 0
  0xba65b9  ja      loc_BA66E8
  0xba65bf  lea     ebx, [eax+4]
  0xba65c2  cmp     ebx, ecx
  0xba65c4  mov     word ptr [ebp+0], 7609h
  0xba65ca  ja      loc_BA66E8
  0xba65d0  mov     ecx, [esp+40h+arg_0]
  0xba65d4  mov     [eax], ecx
  0xba65d6  mov     edi, [esi+8290h]
  0xba65dc  test    edi, edi
  0xba65de  jz      loc_BA6689
  0xba65e4  lea     edx, [esp+40h+var_28]
  0xba65e8  push    edx
  0xba65e9  call    sub_CA0CE0
  0xba65ee  add     esp, 4
  0xba65f1  mov     ecx, [esi+8]
  0xba65f4  push    offset aProtoLoungeCli_541; ")<-_proto_lounge_client::send_dailycup_"...
  0xba65f9  push    ecx
  0xba65fa  push    offset aId; " (id:"
  0xba65ff  push    eax
  0xba6600  push    edi
  0xba6601  mov     byte ptr [esp+54h+var_4], 1
  0xba6606  call    sub_B03020
  0xba660b  add     esp, 8
  0xba660e  push    eax
  0xba660f  call    sub_41D990
  0xba6614  add     esp, 8
  0xba6617  mov     ecx, eax
  0xba6619  call    sub_ADC810
  0xba661e  push    eax
  0xba661f  call    sub_41D990
  0xba6624  add     esp, 8
  0xba6627  lea     ecx, [esp+40h+var_28]
  0xba662b  mov     byte ptr [esp+40h+var_4], 0
  0xba6630  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba663a  push    offset aTeamId; "team_id="
  0xba664f  push    offset aByte; "]byte"
  0xba6659  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba668b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba65c4` | u16 |
| `team_id` | `0xBA65D4` | u32 |
