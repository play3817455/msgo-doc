# 汇编证据 —— CS-0x8288-auth-worldlist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B058B0 @ `0xb058b0`（`0xb058b0`..`0xb05a30`）
- 命令名字符串：`)<-_proto_auth_client::send_worldlist_get(` @ `0xedb0c0`
- opcode 写入：`0xb05906`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb058f3`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb058f7  mov     edi, eax
  0xb058f9  mov     eax, [esi+0Ch]
  0xb058fc  push    eax
  0xb058fd  lea     ecx, [esp+44h+var_2C]
  0xb05901  call    sub_ABB2F0
  0xb05906  mov     word ptr [edi], 8288h
  0xb0590b  mov     ebp, [esi+3B0h]
  0xb05911  test    ebp, ebp
  0xb05913  mov     [esp+40h+var_4], 0
  0xb0591b  lea     ebx, [edi+2]
  0xb0591e  jz      loc_B059AF
  0xb05924  lea     ecx, [esp+40h+var_28]
  0xb05928  push    ecx
  0xb05929  call    sub_CA0CE0
  0xb0592e  add     esp, 4
  0xb05931  mov     edx, [esi+8]
  0xb05934  push    offset aProtoAuthClien_3; ")<-_proto_auth_client::send_worldlist_g"...
  0xb05939  push    edx
  0xb0593a  push    offset aId; " (id:"
  0xb0593f  push    eax
  0xb05940  push    ebp
  0xb05941  mov     byte ptr [esp+54h+var_4], 1
  0xb05946  call    sub_B03020
  0xb0594b  add     esp, 8
  0xb0594e  push    eax
  0xb0594f  call    sub_41D990
  0xb05954  add     esp, 8
  0xb05957  mov     ecx, eax
  0xb05959  call    sub_ADC810
  0xb0595e  push    eax
  0xb0595f  call    sub_41D990
  0xb05964  add     esp, 8
  0xb05967  lea     ecx, [esp+40h+var_28]
  0xb0596b  mov     byte ptr [esp+40h+var_4], 0
  0xb05970  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb05975  push    offset aByte; "]byte"
  0xb0597f  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb059b1  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb05906` | u16 |
