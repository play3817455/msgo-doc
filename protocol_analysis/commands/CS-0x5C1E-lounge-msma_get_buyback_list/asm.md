# 汇编证据 —— CS-0x5C1E-lounge-msma_get_buyback_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B92FD0 @ `0xb92fd0`（`0xb92fd0`..`0xb93156`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_get_buyback_list(` @ `0xeeb318`
- opcode 写入：`0xb93029`
- 声明容量：`0x2`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9301a  mov     edi, eax
  0xb9301c  mov     eax, [esi+0Ch]
  0xb9301f  push    eax
  0xb93020  lea     ecx, [esp+44h+var_2C]
  0xb93024  call    sub_ABB2F0
  0xb93029  mov     word ptr [edi], 5C1Eh
  0xb9302e  mov     ebp, [esi+7CECh]
  0xb93034  test    ebp, ebp
  0xb93036  mov     [esp+40h+var_4], 0
  0xb9303e  lea     ebx, [edi+2]
  0xb93041  jz      loc_B930D2
  0xb93047  lea     ecx, [esp+40h+var_28]
  0xb9304b  push    ecx
  0xb9304c  call    sub_CA0CE0
  0xb93051  add     esp, 4
  0xb93054  mov     edx, [esi+8]
  0xb93057  push    offset aProtoLoungeCli_530; ")<-_proto_lounge_client::send_msma_get_"...
  0xb9305c  push    edx
  0xb9305d  push    offset aId; " (id:"
  0xb93062  push    eax
  0xb93063  push    ebp
  0xb93064  mov     byte ptr [esp+54h+var_4], 1
  0xb93069  call    sub_B03020
  0xb9306e  add     esp, 8
  0xb93071  push    eax
  0xb93072  call    sub_41D990
  0xb93077  add     esp, 8
  0xb9307a  mov     ecx, eax
  0xb9307c  call    sub_ADC810
  0xb93081  push    eax
  0xb93082  call    sub_41D990
  0xb93087  add     esp, 8
  0xb9308a  lea     ecx, [esp+40h+var_28]
  0xb9308e  mov     byte ptr [esp+40h+var_4], 0
  0xb93093  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb93098  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb930d4  mov     eax, [edx+58h]
  0xb930d7  sub     ebx, edi
  0xb930d9  push    ebx
  0xb930da  push    edi
  0xb930db  mov     ecx, esi
  0xb930dd  call    eax
  0xb930df  test    al, al
  0xb930e1  jnz     short loc_B9310A
  0xb930e3  lea     ecx, [esp+40h+var_2C]
  0xb930e7  mov     [esp+40h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB93029` | u16 |
