# 汇编证据 —— CS-0x5F80-lounge-party_leave

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B92310 @ `0xb92310`（`0xb92310`..`0xb92496`）
- 命令名字符串：`)<-_proto_lounge_client::send_party_leave(` @ `0xeeb1b0`
- opcode 写入：`0xb92369`
- 声明容量：`0x2`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb9235a  mov     edi, eax
  0xb9235c  mov     eax, [esi+0Ch]
  0xb9235f  push    eax
  0xb92360  lea     ecx, [esp+44h+var_2C]
  0xb92364  call    sub_ABB2F0
  0xb92369  mov     word ptr [edi], 5F80h
  0xb9236e  mov     ebp, [esi+7C8Ch]
  0xb92374  test    ebp, ebp
  0xb92376  mov     [esp+40h+var_4], 0
  0xb9237e  lea     ebx, [edi+2]
  0xb92381  jz      loc_B92412
  0xb92387  lea     ecx, [esp+40h+var_28]
  0xb9238b  push    ecx
  0xb9238c  call    sub_CA0CE0
  0xb92391  add     esp, 4
  0xb92394  mov     edx, [esi+8]
  0xb92397  push    offset aProtoLoungeCli_510; ")<-_proto_lounge_client::send_party_lea"...
  0xb9239c  push    edx
  0xb9239d  push    offset aId; " (id:"
  0xb923a2  push    eax
  0xb923a3  push    ebp
  0xb923a4  mov     byte ptr [esp+54h+var_4], 1
  0xb923a9  call    sub_B03020
  0xb923ae  add     esp, 8
  0xb923b1  push    eax
  0xb923b2  call    sub_41D990
  0xb923b7  add     esp, 8
  0xb923ba  mov     ecx, eax
  0xb923bc  call    sub_ADC810
  0xb923c1  push    eax
  0xb923c2  call    sub_41D990
  0xb923c7  add     esp, 8
  0xb923ca  lea     ecx, [esp+40h+var_28]
  0xb923ce  mov     byte ptr [esp+40h+var_4], 0
  0xb923d3  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb923d8  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb92414  mov     eax, [edx+58h]
  0xb92417  sub     ebx, edi
  0xb92419  push    ebx
  0xb9241a  push    edi
  0xb9241b  mov     ecx, esi
  0xb9241d  call    eax
  0xb9241f  test    al, al
  0xb92421  jnz     short loc_B9244A
  0xb92423  lea     ecx, [esp+40h+var_2C]
  0xb92427  mov     [esp+40h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB92369` | u16 |
