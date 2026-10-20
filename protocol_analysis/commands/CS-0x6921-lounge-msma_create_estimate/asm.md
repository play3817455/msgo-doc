# 汇编证据 —— CS-0x6921-lounge-msma_create_estimate

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B95C80 @ `0xb95c80`（`0xb95c80`..`0xb95eba`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_create_estimate(` @ `0xeeb7f0`
- opcode 写入：`0xb95cfc`
- 声明容量：`0xE`

## 2. 组包块切片（游标初始化 → 提交）

```asm
  0xb95cca  mov     ebp, eax
  0xb95ccc  mov     eax, [edi+0Ch]
  0xb95ccf  push    eax
  0xb95cd0  lea     ecx, [esp+4Ch+var_34]
  0xb95cd4  call    sub_ABB2F0
  0xb95cd9  lea     ecx, [ebp+0Eh]
  0xb95cdc  lea     eax, [ebp+2]
  0xb95cdf  cmp     eax, ecx
  0xb95ce1  mov     [esp+48h+var_4], 0
  0xb95ce9  mov     [esp+48h+var_30], ebp
  0xb95ced  mov     dword ptr [esp+48h+var_2C], ecx
  0xb95cf1  ja      loc_B95EA5
  0xb95cf7  lea     edx, [eax+4]
  0xb95cfa  cmp     edx, ecx
  0xb95cfc  mov     word ptr [ebp+0], 6921h
  0xb95d02  ja      loc_B95EA5
  0xb95d08  mov     esi, [esp+48h+arg_0]
  0xb95d0c  mov     [eax], esi
  0xb95d0e  mov     eax, edx
  0xb95d10  lea     edx, [eax+4]
  0xb95d13  cmp     edx, ecx
  0xb95d15  ja      loc_B95EA5
  0xb95d1b  mov     ecx, [esp+48h+arg_4]
  0xb95d1f  mov     [esp+48h+var_30], edx
  0xb95d23  lea     edx, [esp+48h+var_30]
  0xb95d27  mov     [eax], ecx
  0xb95d29  push    edx
  0xb95d2a  lea     eax, [esp+4Ch+arg_8]
  0xb95d2e  push    eax
  0xb95d2f  call    sub_B02DA0
  0xb95d34  add     esp, 8
  0xb95d37  test    al, al
  0xb95d39  jz      loc_B95EA5
  0xb95d3f  mov     esi, [edi+7DB0h]
  0xb95d45  test    esi, esi
  0xb95d47  mov     ebx, [esp+48h+var_30]
  0xb95d4b  jz      loc_B95E46
  0xb95d51  lea     ecx, [esp+48h+var_28]
  0xb95d55  push    ecx
  0xb95d56  call    sub_CA0CE0
  0xb95d5b  add     esp, 4
  0xb95d5e  mov     edx, [edi+8]
  0xb95d61  push    offset aProtoLoungeCli_445; ")<-_proto_lounge_client::send_msma_crea"...
  0xb95d66  push    edx
  0xb95d67  push    offset aId; " (id:"
  0xb95d6c  push    eax
  0xb95d6d  push    esi
  0xb95d6e  mov     byte ptr [esp+5Ch+var_4], 1
  0xb95d73  call    sub_B03020
  0xb95d78  add     esp, 8
  0xb95d7b  push    eax
  0xb95d7c  call    sub_41D990
  0xb95d81  add     esp, 8
  0xb95d84  mov     ecx, eax
  0xb95d86  call    sub_ADC810
  0xb95d8b  push    eax
  0xb95d8c  call    sub_41D990
  0xb95d91  add     esp, 8
  0xb95d94  lea     ecx, [esp+48h+var_28]
  0xb95d98  mov     byte ptr [esp+48h+var_4], 0
  0xb95d9d  call    sub_B02FF0   <<<COMMIT
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb95dac  push    offset aMsPlanId; "ms_plan_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb95dd4  push    offset aTicketId; "ticket_id="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb95df7  push    offset aUsenum; "usenum="
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
  0xb95e0c  push    offset aByte; "]byte"
        ; ↑ 日志名；其后的 push/打印调用给出该字段的取值
```

## 4. 发送去向切片

```asm
  0xb95e48  mov     eax, [edx+58h]
  0xb95e4b  sub     ebx, ebp
  0xb95e4d  push    ebx
  0xb95e4e  push    ebp
  0xb95e4f  mov     ecx, edi
  0xb95e51  call    eax
  0xb95e53  test    al, al
  0xb95e55  jz      short loc_B95EA5
  0xb95e57  mov     eax, [edi+79A8h]
  0xb95e5d  test    eax, eax
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。
> 本批 50 条**全部命中同一去向槽 `vt[0x58]`**（与批次-16/17 一致）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB95CFC` | u16 |
| `ms_plan_id` | `0xB95D0C` | u32 |
| `ticket_id` | `0xB95D27` | u32 |
| `usenum` | `0xB95D2F` | u16 |
