# 汇编证据 —— CS-0x51EF-lounge-cmdline_exec

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8D9D0 @ `0xb8d9d0`（`0xb8d9d0`..`0xb8dbaf`）
- 命令名字符串：`)<-_proto_lounge_client::send_cmdline_exec(` @ `0xeea980`
- opcode 写入：`0xb8da5c`
- 声明容量：`0xBA`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb8da1d  mov     edi, eax
  0xb8da1f  mov     eax, [esi+0Ch]
  0xb8da22  push    eax
  0xb8da23  lea     ecx, [esp+4Ch+var_34]
  0xb8da27  call    sub_ABB2F0
  0xb8da2c  lea     ecx, [edi+0BAh]
  0xb8da32  lea     eax, [edi+2]
  0xb8da35  cmp     eax, ecx
  0xb8da37  mov     [esp+48h+var_4], 0
  0xb8da3f  mov     [esp+48h+var_30], edi
  0xb8da43  mov     dword ptr [esp+48h+var_2C], ecx
  0xb8da47  ja      loc_B8DB9A
  0xb8da4d  mov     edx, [esp+48h+arg_0]
  0xb8da51  push    0B5h
  0xb8da56  lea     ecx, [esp+4Ch+var_30]
  0xb8da5a  push    ecx
  0xb8da5b  push    edx
  0xb8da5c  mov     word ptr [edi], 51EFh
  0xb8da61  mov     [esp+54h+var_30], eax
  0xb8da65  call    sub_B02B40   <<< pushN=181(0xB5)
  0xb8da6a  add     esp, 0Ch
  0xb8da6d  test    al, al
  0xb8da6f  jz      loc_B8DB9A
  0xb8da75  mov     ebp, [esi+7B14h]
  0xb8da7b  test    ebp, ebp
  0xb8da7d  mov     ebx, [esp+48h+var_30]
  0xb8da81  jz      loc_B8DB3C
  0xb8da87  lea     eax, [esp+48h+var_28]
  0xb8da8b  push    eax
  0xb8da8c  call    sub_CA0CE0
  0xb8da91  add     esp, 4
  0xb8da94  mov     ecx, [esi+8]
  0xb8da97  push    offset aProtoLoungeCli_417; ")<-_proto_lounge_client::send_cmdline_e"...
  0xb8da9c  push    ecx
  0xb8da9d  push    offset aId; " (id:"
  0xb8daa2  push    eax
  0xb8daa3  push    ebp
  0xb8daa4  mov     byte ptr [esp+5Ch+var_4], 1
  0xb8daa9  call    sub_B03020
  0xb8daae  add     esp, 8
  0xb8dab1  push    eax
  0xb8dab2  call    sub_41D990
  0xb8dab7  add     esp, 8
  0xb8daba  mov     ecx, eax
  0xb8dabc  call    sub_ADC810
  0xb8dac1  push    eax
  0xb8dac2  call    sub_41D990
  0xb8dac7  add     esp, 8
  0xb8daca  lea     ecx, [esp+48h+var_28]
  0xb8dace  mov     byte ptr [esp+48h+var_4], 0
  0xb8dad3  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8dae2  push    offset aCmd; "cmd=\""
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb8db02  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8db3e  mov     eax, [edx+58h]
  0xb8db41  mov     ebp, ebx
  0xb8db43  sub     ebp, edi
  0xb8db45  push    ebp
  0xb8db46  push    edi
  0xb8db47  mov     ecx, esi
  0xb8db49  call    eax
  0xb8db4b  test    al, al
  0xb8db4d  jz      short loc_B8DB9A
  0xb8db4f  mov     eax, [esi+79A8h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8DA5C` | u16 |
| `cmd` | `0xB8DA65` | bytes |
