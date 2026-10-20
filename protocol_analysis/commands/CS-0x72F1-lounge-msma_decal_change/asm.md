# 汇编证据 —— CS-0x72F1-lounge-msma_decal_change

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B94A10 @ `0xb94a10`（`0xb94a10`..`0xb94c59`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_decal_change(` @ `0xeeb620`
- opcode 写入：`0xb94a8c`
- 声明容量：`0x16`（分配器容量 `push` @ `0xb94a56`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb94a5a  mov     ebp, eax
  0xb94a5c  mov     eax, [edi+0Ch]
  0xb94a5f  push    eax
  0xb94a60  lea     ecx, [esp+4Ch+var_34]
  0xb94a64  call    sub_ABB2F0
  0xb94a69  lea     ecx, [ebp+16h]
  0xb94a6c  lea     eax, [ebp+2]
  0xb94a6f  cmp     eax, ecx
  0xb94a71  mov     [esp+48h+var_4], 0
  0xb94a79  mov     [esp+48h+var_30], ebp
  0xb94a7d  mov     dword ptr [esp+48h+var_2C], ecx
  0xb94a81  ja      loc_B94C44
  0xb94a87  lea     edx, [eax+8]
  0xb94a8a  cmp     edx, ecx
  0xb94a8c  mov     word ptr [ebp+0], 72F1h
  0xb94a92  ja      loc_B94C44
  0xb94a98  mov     esi, [esp+48h+arg_0]
  0xb94a9c  mov     [eax], esi
  0xb94a9e  mov     esi, [esp+48h+arg_4]
  0xb94aa2  mov     [eax+4], esi
  0xb94aa5  lea     eax, [edx+4]
  0xb94aa8  cmp     eax, ecx
  0xb94aaa  ja      loc_B94C44
  0xb94ab0  mov     ecx, [esp+48h+arg_8]
  0xb94ab4  mov     [edx], ecx
  0xb94ab6  lea     edx, [esp+48h+var_30]
  0xb94aba  mov     [esp+48h+var_30], eax
  0xb94abe  push    edx
  0xb94abf  lea     eax, [esp+4Ch+arg_C]
  0xb94ac3  push    eax
  0xb94ac4  call    sub_B06190
  0xb94ac9  add     esp, 8
  0xb94acc  test    al, al
  0xb94ace  jz      loc_B94C44
  0xb94ad4  mov     esi, [edi+7D6Ch]
  0xb94ada  test    esi, esi
  0xb94adc  mov     ebx, [esp+48h+var_30]
  0xb94ae0  jz      loc_B94BE5
  0xb94ae6  lea     ecx, [esp+48h+var_28]
  0xb94aea  push    ecx
  0xb94aeb  call    sub_CA0CE0
  0xb94af0  add     esp, 4
  0xb94af3  mov     edx, [edi+8]
  0xb94af6  push    offset aProtoLoungeCli_460; ")<-_proto_lounge_client::send_msma_deca"...
  0xb94afb  push    edx
  0xb94afc  push    offset aId; " (id:"
  0xb94b01  push    eax
  0xb94b02  push    esi
  0xb94b03  mov     byte ptr [esp+5Ch+var_4], 1
  0xb94b08  call    sub_B03020
  0xb94b0d  add     esp, 8
  0xb94b10  push    eax
  0xb94b11  call    sub_41D990
  0xb94b16  add     esp, 8
  0xb94b19  mov     ecx, eax
  0xb94b1b  call    sub_ADC810
  0xb94b20  push    eax
  0xb94b21  call    sub_41D990
  0xb94b26  add     esp, 8
  0xb94b29  lea     ecx, [esp+48h+var_28]
  0xb94b2d  mov     byte ptr [esp+48h+var_4], 0
  0xb94b32  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb94b46  push    offset aUniqidMs; "uniqid_ms="
  0xb94b6e  push    offset aDecal; "decal="
  0xb94b96  push    offset aUniqidDecal; "uniqid_decal="
  0xb94bab  push    offset aByte; "]byte"
  0xb94bb5  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb94be7  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb94a8c` | u16 |
| `uniqid_ms` | `0xB94A9C, 0xB94AA2` | u64 |
| `decal` | `0xB94AB4` | u32 |
| `uniqid_decal` | `0xB94AC4` | u64 |
