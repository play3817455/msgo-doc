# 汇编证据 —— CS-0x93EE-lounge-pilot_bot_checkcode_request_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8C610 @ `0xb8c610`（`0xb8c610`..`0xb8c7e6`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_bot_checkcode_request_r(` @ `0xeea74c`
- opcode 写入：`0xb8c693`
- 声明容量：`0x12`（分配器容量 `push` @ `0xb8c656`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8c65a  mov     edi, eax
  0xb8c65c  mov     eax, [esi+0Ch]
  0xb8c65f  push    eax
  0xb8c660  lea     ecx, [esp+4Ch+var_34]
  0xb8c664  call    sub_ABB2F0
  0xb8c669  lea     ecx, [edi+12h]
  0xb8c66c  lea     eax, [edi+2]
  0xb8c66f  cmp     eax, ecx
  0xb8c671  mov     [esp+48h+var_4], 0
  0xb8c679  mov     [esp+48h+var_30], edi
  0xb8c67d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8c681  ja      loc_B8C7D1
  0xb8c687  mov     edx, [esp+48h+arg_0]
  0xb8c68b  push    0Dh
  0xb8c68d  lea     ecx, [esp+4Ch+var_30]
  0xb8c691  push    ecx
  0xb8c692  push    edx
  0xb8c693  mov     word ptr [edi], 93EEh
  0xb8c698  mov     [esp+54h+var_30], eax
  0xb8c69c  call    sub_B02B40
  0xb8c6a1  add     esp, 0Ch
  0xb8c6a4  test    al, al
  0xb8c6a6  jz      loc_B8C7D1
  0xb8c6ac  mov     ebp, [esi+7AA4h]
  0xb8c6b2  test    ebp, ebp
  0xb8c6b4  mov     ebx, [esp+48h+var_30]
  0xb8c6b8  jz      loc_B8C773
  0xb8c6be  lea     eax, [esp+48h+var_28]
  0xb8c6c2  push    eax
  0xb8c6c3  call    sub_CA0CE0
  0xb8c6c8  add     esp, 4
  0xb8c6cb  mov     ecx, [esi+8]
  0xb8c6ce  push    offset aProtoLoungeCli_588; ")<-_proto_lounge_client::send_pilot_bot"...
  0xb8c6d3  push    ecx
  0xb8c6d4  push    offset aId; " (id:"
  0xb8c6d9  push    eax
  0xb8c6da  push    ebp
  0xb8c6db  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8c6e0  call    sub_B03020
  0xb8c6e5  add     esp, 8
  0xb8c6e8  push    eax
  0xb8c6e9  call    sub_41D990
  0xb8c6ee  add     esp, 8
  0xb8c6f1  mov     ecx, eax
  0xb8c6f3  call    sub_ADC810
  0xb8c6f8  push    eax
  0xb8c6f9  call    sub_41D990
  0xb8c6fe  add     esp, 8
  0xb8c701  lea     ecx, [esp+48h+var_28]
  0xb8c705  mov     byte ptr [esp+48h+var_4], 0
  0xb8c70a  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8c713  push    offset asc_EDAD54; "\""
  0xb8c719  push    offset aCode; "code=\""
  0xb8c739  push    offset aByte; "]byte"
  0xb8c743  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8c775  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8c693` | u16 |
| `code` | `0xB8C69C` | bytes |
