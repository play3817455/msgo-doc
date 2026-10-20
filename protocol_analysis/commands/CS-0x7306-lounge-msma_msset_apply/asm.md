# 汇编证据 —— CS-0x7306-lounge-msma_msset_apply

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B98C90 @ `0xb98c90`（`0xb98c90`..`0xb98e7a`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_msset_apply(` @ `0xeebc7c`
- opcode 写入：`0xb98d04`
- 声明容量：`0xA`（分配器容量 `push` @ `0xb98cd6`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb98cda  mov     ebp, eax
  0xb98cdc  mov     eax, [edi+0Ch]
  0xb98cdf  push    eax
  0xb98ce0  lea     ecx, [esp+44h+var_2C]
  0xb98ce4  call    sub_ABB2F0
  0xb98ce9  lea     ecx, [ebp+0Ah]
  0xb98cec  lea     eax, [ebp+2]
  0xb98cef  cmp     eax, ecx
  0xb98cf1  mov     [esp+40h+var_4], 0
  0xb98cf9  ja      loc_B98E65
  0xb98cff  lea     edx, [eax+2]
  0xb98d02  cmp     edx, ecx
  0xb98d04  mov     word ptr [ebp+0], 7306h
  0xb98d0a  ja      loc_B98E65
  0xb98d10  mov     si, word ptr [esp+40h+arg_0]
  0xb98d15  lea     ebx, [edx+2]
  0xb98d18  cmp     ebx, ecx
  0xb98d1a  mov     [eax], si
  0xb98d1d  ja      loc_B98E65
  0xb98d23  mov     cx, word ptr [esp+40h+arg_4]
  0xb98d28  mov     [edx], cx
  0xb98d2b  mov     esi, [edi+7E64h]
  0xb98d31  test    esi, esi
  0xb98d33  jz      loc_B98E06
  0xb98d39  lea     edx, [esp+40h+var_28]
  0xb98d3d  push    edx
  0xb98d3e  call    sub_CA0CE0
  0xb98d43  add     esp, 4
  0xb98d46  mov     ecx, [edi+8]
  0xb98d49  push    offset aProtoLoungeCli_443; ")<-_proto_lounge_client::send_msma_msse"...
  0xb98d4e  push    ecx
  0xb98d4f  push    offset aId; " (id:"
  0xb98d54  push    eax
  0xb98d55  push    esi
  0xb98d56  mov     byte ptr [esp+54h+var_4], 1
  0xb98d5b  call    sub_B03020
  0xb98d60  add     esp, 8
  0xb98d63  push    eax
  0xb98d64  call    sub_41D990
  0xb98d69  add     esp, 8
  0xb98d6c  mov     ecx, eax
  0xb98d6e  call    sub_ADC810
  0xb98d73  push    eax
  0xb98d74  call    sub_41D990
  0xb98d79  add     esp, 8
  0xb98d7c  lea     ecx, [esp+40h+var_28]
  0xb98d80  mov     byte ptr [esp+40h+var_4], 0
  0xb98d85  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb98d94  push    offset aDeckType; "deck_type="
  0xb98db7  push    offset aSlot; "slot="
  0xb98dcc  push    offset aByte; "]byte"
  0xb98dd6  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb98e08  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb98d04` | u16 |
| `deck_type` | `0xB98D1A` | u16 |
| `slot` | `0xB98D28` | u16 |
