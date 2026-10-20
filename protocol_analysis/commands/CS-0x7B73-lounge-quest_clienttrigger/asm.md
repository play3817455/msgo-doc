# 汇编证据 —— CS-0x7B73-lounge-quest_clienttrigger

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9D600 @ `0xb9d600`（`0xb9d600`..`0xb9d7ad`）
- 命令名字符串：`)<-_proto_lounge_client::send_quest_clienttrigger(` @ `0xeec3dc`
- opcode 写入：`0xb9d674`
- 声明容量：`0x6`（分配器容量 `push` @ `0xb9d646`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9d64a  mov     ebp, eax
  0xb9d64c  mov     eax, [esi+0Ch]
  0xb9d64f  push    eax
  0xb9d650  lea     ecx, [esp+44h+var_2C]
  0xb9d654  call    sub_ABB2F0
  0xb9d659  lea     ecx, [ebp+6]
  0xb9d65c  lea     eax, [ebp+2]
  0xb9d65f  cmp     eax, ecx
  0xb9d661  mov     [esp+40h+var_4], 0
  0xb9d669  ja      loc_B9D798
  0xb9d66f  lea     ebx, [eax+4]
  0xb9d672  cmp     ebx, ecx
  0xb9d674  mov     word ptr [ebp+0], 7B73h
  0xb9d67a  ja      loc_B9D798
  0xb9d680  mov     ecx, [esp+40h+arg_0]
  0xb9d684  mov     [eax], ecx
  0xb9d686  mov     edi, [esi+7FC4h]
  0xb9d68c  test    edi, edi
  0xb9d68e  jz      loc_B9D739
  0xb9d694  lea     edx, [esp+40h+var_28]
  0xb9d698  push    edx
  0xb9d699  call    sub_CA0CE0
  0xb9d69e  add     esp, 4
  0xb9d6a1  mov     ecx, [esi+8]
  0xb9d6a4  push    offset aProtoLoungeCli_420; ")<-_proto_lounge_client::send_quest_cli"...
  0xb9d6a9  push    ecx
  0xb9d6aa  push    offset aId; " (id:"
  0xb9d6af  push    eax
  0xb9d6b0  push    edi
  0xb9d6b1  mov     byte ptr [esp+54h+var_4], 1
  0xb9d6b6  call    sub_B03020
  0xb9d6bb  add     esp, 8
  0xb9d6be  push    eax
  0xb9d6bf  call    sub_41D990
  0xb9d6c4  add     esp, 8
  0xb9d6c7  mov     ecx, eax
  0xb9d6c9  call    sub_ADC810
  0xb9d6ce  push    eax
  0xb9d6cf  call    sub_41D990
  0xb9d6d4  add     esp, 8
  0xb9d6d7  lea     ecx, [esp+40h+var_28]
  0xb9d6db  mov     byte ptr [esp+40h+var_4], 0
  0xb9d6e0  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9d6ea  push    offset aTrigger; "trigger="
  0xb9d6ff  push    offset aByte; "]byte"
  0xb9d709  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb9d73b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9d674` | u16 |
| `trigger` | `0xB9D684` | u32 |
