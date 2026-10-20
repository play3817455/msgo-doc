# 汇编证据 —— CS-0x7C80-lounge-beginner_challenge_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA8660 @ `0xba8660`（`0xba8660`..`0xba87e6`）
- 命令名字符串：`)<-_proto_lounge_client::send_beginner_challenge_get(` @ `0xeed6cc`
- opcode 写入：`0xba86b9`
- 声明容量：`0x2`（分配器容量 `push` @ `0xba86a6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba86aa  mov     edi, eax
  0xba86ac  mov     eax, [esi+0Ch]
  0xba86af  push    eax
  0xba86b0  lea     ecx, [esp+44h+var_2C]
  0xba86b4  call    sub_ABB2F0
  0xba86b9  mov     word ptr [edi], 7C80h
  0xba86be  mov     ebp, [esi+835Ch]
  0xba86c4  test    ebp, ebp
  0xba86c6  mov     [esp+40h+var_4], 0
  0xba86ce  lea     ebx, [edi+2]
  0xba86d1  jz      loc_BA8762
  0xba86d7  lea     ecx, [esp+40h+var_28]
  0xba86db  push    ecx
  0xba86dc  call    sub_CA0CE0
  0xba86e1  add     esp, 4
  0xba86e4  mov     edx, [esi+8]
  0xba86e7  push    offset aProtoLoungeCli_515; ")<-_proto_lounge_client::send_beginner_"...
  0xba86ec  push    edx
  0xba86ed  push    offset aId; " (id:"
  0xba86f2  push    eax
  0xba86f3  push    ebp
  0xba86f4  mov     byte ptr [esp+54h+var_4], 1
  0xba86f9  call    sub_B03020
  0xba86fe  add     esp, 8
  0xba8701  push    eax
  0xba8702  call    sub_41D990
  0xba8707  add     esp, 8
  0xba870a  mov     ecx, eax
  0xba870c  call    sub_ADC810
  0xba8711  push    eax
  0xba8712  call    sub_41D990
  0xba8717  add     esp, 8
  0xba871a  lea     ecx, [esp+40h+var_28]
  0xba871e  mov     byte ptr [esp+40h+var_4], 0
  0xba8723  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba8728  push    offset aByte; "]byte"
  0xba8732  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba8764  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba86b9` | u16 |
