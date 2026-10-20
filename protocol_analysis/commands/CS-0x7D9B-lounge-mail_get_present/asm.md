# 汇编证据 —— CS-0x7D9B-lounge-mail_get_present

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9C530 @ `0xb9c530`（`0xb9c530`..`0xb9c774`）
- 命令名字符串：`)<-_proto_lounge_client::send_mail_get_present(` @ `0xeec28c`
- opcode 写入：`0xb9c5ac`
- 声明容量：`0x12`（分配器容量 `push` @ `0xb9c576`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb9c57a  mov     ebp, eax
  0xb9c57c  mov     eax, [edi+0Ch]
  0xb9c57f  push    eax
  0xb9c580  lea     ecx, [esp+4Ch+var_34]
  0xb9c584  call    sub_ABB2F0
  0xb9c589  lea     ecx, [ebp+12h]
  0xb9c58c  lea     eax, [ebp+2]
  0xb9c58f  cmp     eax, ecx
  0xb9c591  mov     [esp+48h+var_4], 0
  0xb9c599  mov     [esp+48h+var_30], ebp
  0xb9c59d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb9c5a1  ja      loc_B9C75F
  0xb9c5a7  lea     edx, [eax+8]
  0xb9c5aa  cmp     edx, ecx
  0xb9c5ac  mov     word ptr [ebp+0], 7D9Bh
  0xb9c5b2  ja      loc_B9C75F
  0xb9c5b8  mov     esi, [esp+48h+arg_0]
  0xb9c5bc  mov     [eax], esi
  0xb9c5be  mov     esi, [esp+48h+arg_4]
  0xb9c5c2  mov     [eax+4], esi
  0xb9c5c5  lea     eax, [edx+4]
  0xb9c5c8  cmp     eax, ecx
  0xb9c5ca  ja      loc_B9C75F
  0xb9c5d0  mov     ecx, [esp+48h+arg_8]
  0xb9c5d4  mov     [edx], ecx
  0xb9c5d6  lea     edx, [esp+48h+var_30]
  0xb9c5da  mov     [esp+48h+var_30], eax
  0xb9c5de  push    edx
  0xb9c5df  lea     eax, [esp+4Ch+arg_C]
  0xb9c5e3  push    eax
  0xb9c5e4  call    sub_B02D80
  0xb9c5e9  add     esp, 8
  0xb9c5ec  test    al, al
  0xb9c5ee  jz      loc_B9C75F
  0xb9c5f4  mov     esi, [edi+7F70h]
  0xb9c5fa  test    esi, esi
  0xb9c5fc  mov     ebx, [esp+48h+var_30]
  0xb9c600  jz      loc_B9C700
  0xb9c606  lea     ecx, [esp+48h+var_28]
  0xb9c60a  push    ecx
  0xb9c60b  call    sub_CA0CE0
  0xb9c610  add     esp, 4
  0xb9c613  mov     edx, [edi+8]
  0xb9c616  push    offset aProtoLoungeCli_506; ")<-_proto_lounge_client::send_mail_get_"...
  0xb9c61b  push    edx
  0xb9c61c  push    offset aId; " (id:"
  0xb9c621  push    eax
  0xb9c622  push    esi
  0xb9c623  mov     byte ptr [esp+5Ch+var_4], 1
  0xb9c628  call    sub_B03020
  0xb9c62d  add     esp, 8
  0xb9c630  push    eax
  0xb9c631  call    sub_41D990
  0xb9c636  add     esp, 8
  0xb9c639  mov     ecx, eax
  0xb9c63b  call    sub_ADC810
  0xb9c640  push    eax
  0xb9c641  call    sub_41D990
  0xb9c646  add     esp, 8
  0xb9c649  lea     ecx, [esp+48h+var_28]
  0xb9c64d  mov     byte ptr [esp+48h+var_4], 0
  0xb9c652  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb9c666  push    offset aMailid; "mailid="
  0xb9c68e  push    offset aAttachType; "attach_type="
  0xb9c6b1  push    offset aAttachId; "attach_id="
  0xb9c6c6  push    offset aByte; "]byte"
  0xb9c6d0  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb9c702  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb9c5ac` | u16 |
| `mailid` | `0xB9C5BC, 0xB9C5C2` | u64 |
| `attach_type` | `0xB9C5D4` | u32 |
| `attach_id` | `0xB9C5E4` | u32 |
