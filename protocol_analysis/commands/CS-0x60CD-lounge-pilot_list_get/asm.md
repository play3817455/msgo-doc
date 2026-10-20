# 汇编证据 —— CS-0x60CD-lounge-pilot_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B89F80 @ `0xb89f80`（`0xb89f80`..`0xb8a100`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_list_get(` @ `0xeea310`
- opcode 写入：`0xb89fd6`
- 声明容量：`0x2`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb89fc7  mov     edi, eax
  0xb89fc9  mov     eax, [esi+0Ch]
  0xb89fcc  push    eax
  0xb89fcd  lea     ecx, [esp+44h+var_2C]
  0xb89fd1  call    sub_ABB2F0
  0xb89fd6  mov     word ptr [edi], 60CDh
  0xb89fdb  mov     ebp, [esi+79E4h]
  0xb89fe1  test    ebp, ebp
  0xb89fe3  mov     [esp+40h+var_4], 0
  0xb89feb  lea     ebx, [edi+2]
  0xb89fee  jz      loc_B8A07F
  0xb89ff4  lea     ecx, [esp+40h+var_28]
  0xb89ff8  push    ecx
  0xb89ff9  call    sub_CA0CE0
  0xb89ffe  add     esp, 4
  0xb8a001  mov     edx, [esi+8]
  0xb8a004  push    offset aProtoLoungeCli_389; ")<-_proto_lounge_client::send_pilot_lis"...
  0xb8a009  push    edx
  0xb8a00a  push    offset aId; " (id:"
  0xb8a00f  push    eax
  0xb8a010  push    ebp
  0xb8a011  mov     byte ptr [esp+54h+var_4], 1
  0xb8a016  call    sub_B03020
  0xb8a01b  add     esp, 8
  0xb8a01e  push    eax
  0xb8a01f  call    sub_41D990
  0xb8a024  add     esp, 8
  0xb8a027  mov     ecx, eax
  0xb8a029  call    sub_ADC810
  0xb8a02e  push    eax
  0xb8a02f  call    sub_41D990
  0xb8a034  add     esp, 8
  0xb8a037  lea     ecx, [esp+40h+var_28]
  0xb8a03b  mov     byte ptr [esp+40h+var_4], 0
  0xb8a040  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8a045  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb8a081  mov     eax, [edx+58h]
  0xb8a084  sub     ebx, edi
  0xb8a086  push    ebx
  0xb8a087  push    edi
  0xb8a088  mov     ecx, esi
  0xb8a08a  call    eax
  0xb8a08c  test    al, al
  0xb8a08e  jnz     short loc_B8A0B7
  0xb8a090  lea     ecx, [esp+40h+var_2C]
  0xb8a094  mov     [esp+40h+var_4], 0FFFFFFFFh
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB89FD6` | u16 |
