# 汇编证据 —— CS-0x6C57-lounge-get_special_a_info

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA5ED0 @ `0xba5ed0`（`0xba5ed0`..`0xba6056`）
- 命令名字符串：`)<-_proto_lounge_client::send_get_special_a_info(` @ `0xeed1d8`
- opcode 写入：`0xba5f29`
- 声明容量：`0x2`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba5f1a  mov     edi, eax
  0xba5f1c  mov     eax, [esi+0Ch]
  0xba5f1f  push    eax
  0xba5f20  lea     ecx, [esp+44h+var_2C]
  0xba5f24  call    sub_ABB2F0
  0xba5f29  mov     word ptr [edi], 6C57h
  0xba5f2e  mov     ebp, [esi+823Ch]
  0xba5f34  test    ebp, ebp
  0xba5f36  mov     [esp+40h+var_4], 0
  0xba5f3e  lea     ebx, [edi+2]
  0xba5f41  jz      loc_BA5FD2
  0xba5f47  lea     ecx, [esp+40h+var_28]
  0xba5f4b  push    ecx
  0xba5f4c  call    sub_CA0CE0
  0xba5f51  add     esp, 4
  0xba5f54  mov     edx, [esi+8]
  0xba5f57  push    offset aProtoLoungeCli_524; ")<-_proto_lounge_client::send_get_speci"...
  0xba5f5c  push    edx
  0xba5f5d  push    offset aId; " (id:"
  0xba5f62  push    eax
  0xba5f63  push    ebp
  0xba5f64  mov     byte ptr [esp+54h+var_4], 1
  0xba5f69  call    sub_B03020
  0xba5f6e  add     esp, 8
  0xba5f71  push    eax
  0xba5f72  call    sub_41D990
  0xba5f77  add     esp, 8
  0xba5f7a  mov     ecx, eax
  0xba5f7c  call    sub_ADC810
  0xba5f81  push    eax
  0xba5f82  call    sub_41D990
  0xba5f87  add     esp, 8
  0xba5f8a  lea     ecx, [esp+40h+var_28]
  0xba5f8e  mov     byte ptr [esp+40h+var_4], 0
  0xba5f93  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba5f98  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba5fd4  mov     eax, [edx+58h]
  0xba5fd7  sub     ebx, edi
  0xba5fd9  push    ebx
  0xba5fda  push    edi
  0xba5fdb  mov     ecx, esi
  0xba5fdd  call    eax
  0xba5fdf  test    al, al
  0xba5fe1  jnz     short loc_BA600A
  0xba5fe3  lea     ecx, [esp+40h+var_2C]
  0xba5fe7  mov     [esp+40h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA5F29` | u16 |
