# 汇编证据 —— CS-0x6E89-lounge-gacha_enter

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9D960 @ `0xb9d960`（`0xb9d960`..`0xb9db0d`）
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_enter(` @ `0xeec43c`
- opcode 写入：`0xb9d9d4`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb9d9a6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9d9aa  mov     ebp, eax
  0xb9d9ac  mov     eax, [esi+0Ch]
  0xb9d9af  push    eax
  0xb9d9b0  lea     ecx, [esp+44h+var_2C]
  0xb9d9b4  call    sub_ABB2F0
  0xb9d9b9  lea     ecx, [ebp+6]
  0xb9d9bc  lea     eax, [ebp+2]
  0xb9d9bf  cmp     eax, ecx
  0xb9d9c1  mov     [esp+40h+var_4], 0
  0xb9d9c9  ja      loc_B9DAF8
  0xb9d9cf  lea     ebx, [eax+4]
  0xb9d9d2  cmp     ebx, ecx
  0xb9d9d4  mov     word ptr [ebp+0], 6E89h
  0xb9d9da  ja      loc_B9DAF8
  0xb9d9e0  mov     ecx, [esp+40h+arg_0]
  0xb9d9e4  mov     [eax], ecx
  0xb9d9e6  mov     edi, [esi+7FD0h]
  0xb9d9ec  test    edi, edi
  0xb9d9ee  jz      loc_B9DA99
  0xb9d9f4  lea     edx, [esp+40h+var_28]
  0xb9d9f8  push    edx
  0xb9d9f9  call    sub_CA0CE0
  0xb9d9fe  add     esp, 4
  0xb9da01  mov     ecx, [esi+8]
  0xb9da04  push    offset aProtoLoungeCli_533; ")<-_proto_lounge_client::send_gacha_ent"...
  0xb9da09  push    ecx
  0xb9da0a  push    offset aId; " (id:"
  0xb9da0f  push    eax
  0xb9da10  push    edi
  0xb9da11  mov     byte ptr [esp+54h+var_4], 1
  0xb9da16  call    sub_B03020
  0xb9da1b  add     esp, 8
  0xb9da1e  push    eax
  0xb9da1f  call    sub_41D990
  0xb9da24  add     esp, 8
  0xb9da27  mov     ecx, eax
  0xb9da29  call    sub_ADC810
  0xb9da2e  push    eax
  0xb9da2f  call    sub_41D990
  0xb9da34  add     esp, 8
  0xb9da37  lea     ecx, [esp+40h+var_28]
  0xb9da3b  mov     byte ptr [esp+40h+var_4], 0
  0xb9da40  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9da4a  push    offset aGachaType; "gacha_type="
  0xb9da5f  push    offset aByte; "]byte"
  0xb9da69  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb9da9b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9d9d4` | u16 |
| `gacha_type` | `0xB9D9E4` | u32 |
