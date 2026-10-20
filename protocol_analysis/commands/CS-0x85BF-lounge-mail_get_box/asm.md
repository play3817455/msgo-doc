# 汇编证据 —— CS-0x85BF-lounge-mail_get_box

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9BF20 @ `0xb9bf20`（`0xb9bf20`..`0xb9c108`）
- 命令名字符串：`)<-_proto_lounge_client::send_mail_get_box(` @ `0xeec1f4`
- opcode 写入：`0xb9bf94`
- 声明容量：`0xA`（分配器容量 `push` @ `0xb9bf66`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9bf6a  mov     ebp, eax
  0xb9bf6c  mov     eax, [esi+0Ch]
  0xb9bf6f  push    eax
  0xb9bf70  lea     ecx, [esp+44h+var_2C]
  0xb9bf74  call    sub_ABB2F0
  0xb9bf79  lea     eax, [ebp+0Ah]
  0xb9bf7c  lea     ecx, [ebp+2]
  0xb9bf7f  cmp     ecx, eax
  0xb9bf81  mov     [esp+40h+var_4], 0
  0xb9bf89  ja      loc_B9C0F3
  0xb9bf8f  lea     edx, [ecx+4]
  0xb9bf92  cmp     edx, eax
  0xb9bf94  mov     word ptr [ebp+0], 85BFh
  0xb9bf9a  ja      loc_B9C0F3
  0xb9bfa0  mov     edi, dword ptr [esp+40h+arg_0]
  0xb9bfa4  lea     ebx, [edx+1]
  0xb9bfa7  cmp     ebx, eax
  0xb9bfa9  mov     [ecx], edi
  0xb9bfab  ja      loc_B9C0F3
  0xb9bfb1  mov     cl, [esp+40h+arg_4]
  0xb9bfb5  mov     [edx], cl
  0xb9bfb7  mov     edi, [esi+7F58h]
  0xb9bfbd  test    edi, edi
  0xb9bfbf  jz      loc_B9C094
  0xb9bfc5  lea     edx, [esp+40h+var_28]
  0xb9bfc9  push    edx
  0xb9bfca  call    sub_CA0CE0
  0xb9bfcf  add     esp, 4
  0xb9bfd2  mov     ecx, [esi+8]
  0xb9bfd5  push    offset aProtoLoungeCli_503; ")<-_proto_lounge_client::send_mail_get_"...
  0xb9bfda  push    ecx
  0xb9bfdb  push    offset aId; " (id:"
  0xb9bfe0  push    eax
  0xb9bfe1  push    edi
  0xb9bfe2  mov     byte ptr [esp+54h+var_4], 1
  0xb9bfe7  call    sub_B03020
  0xb9bfec  add     esp, 8
  0xb9bfef  push    eax
  0xb9bff0  call    sub_41D990
  0xb9bff5  add     esp, 8
  0xb9bff8  mov     ecx, eax
  0xb9bffa  call    sub_ADC810
  0xb9bfff  push    eax
  0xb9c000  call    sub_41D990
  0xb9c005  add     esp, 8
  0xb9c008  lea     ecx, [esp+40h+var_28]
  0xb9c00c  mov     byte ptr [esp+40h+var_4], 0
  0xb9c011  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9c020  push    offset aBoxType; "box_type="
  0xb9c043  push    offset aForcePresentGe; "force_present_get="
  0xb9c05a  push    offset aByte; "]byte"
  0xb9c064  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb9bfb7  mov     edi, [esi+7F58h]
  0xb9c096  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9bf94` | u16 |
| `box_type` | `0xB9BFA9` | u32 |
| `force_present_get` | `0xB9BFB5` | u8 |
