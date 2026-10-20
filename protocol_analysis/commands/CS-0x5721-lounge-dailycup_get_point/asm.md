# 汇编证据 —— CS-0x5721-lounge-dailycup_get_point

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA6700 @ `0xba6700`（`0xba6700`..`0xba6886`）
- 命令名字符串：`)<-_proto_lounge_client::send_dailycup_get_point(` @ `0xeed300`
- opcode 写入：`0xba6759`
- 声明容量：`0x2`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xba674a  mov     edi, eax
  0xba674c  mov     eax, [esi+0Ch]
  0xba674f  push    eax
  0xba6750  lea     ecx, [esp+44h+var_2C]
  0xba6754  call    sub_ABB2F0
  0xba6759  mov     word ptr [edi], 5721h
  0xba675e  mov     ebp, [esi+82A0h]
  0xba6764  test    ebp, ebp
  0xba6766  mov     [esp+40h+var_4], 0
  0xba676e  lea     ebx, [edi+2]
  0xba6771  jz      loc_BA6802
  0xba6777  lea     ecx, [esp+40h+var_28]
  0xba677b  push    ecx
  0xba677c  call    sub_CA0CE0
  0xba6781  add     esp, 4
  0xba6784  mov     edx, [esi+8]
  0xba6787  push    offset aProtoLoungeCli_540; ")<-_proto_lounge_client::send_dailycup_"...
  0xba678c  push    edx
  0xba678d  push    offset aId; " (id:"
  0xba6792  push    eax
  0xba6793  push    ebp
  0xba6794  mov     byte ptr [esp+54h+var_4], 1
  0xba6799  call    sub_B03020
  0xba679e  add     esp, 8
  0xba67a1  push    eax
  0xba67a2  call    sub_41D990
  0xba67a7  add     esp, 8
  0xba67aa  mov     ecx, eax
  0xba67ac  call    sub_ADC810
  0xba67b1  push    eax
  0xba67b2  call    sub_41D990
  0xba67b7  add     esp, 8
  0xba67ba  lea     ecx, [esp+40h+var_28]
  0xba67be  mov     byte ptr [esp+40h+var_4], 0
  0xba67c3  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba67c8  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xba6804  mov     eax, [edx+58h]
  0xba6807  sub     ebx, edi
  0xba6809  push    ebx
  0xba680a  push    edi
  0xba680b  mov     ecx, esi
  0xba680d  call    eax
  0xba680f  test    al, al
  0xba6811  jnz     short loc_BA683A
  0xba6813  lea     ecx, [esp+40h+var_2C]
  0xba6817  mov     [esp+40h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA6759` | u16 |
