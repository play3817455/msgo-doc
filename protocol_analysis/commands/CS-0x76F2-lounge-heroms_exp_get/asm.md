# 汇编证据 —— CS-0x76F2-lounge-heroms_exp_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA6CC0 @ `0xba6cc0`（`0xba6cc0`..`0xba6efa`）
- 命令名字符串：`)<-_proto_lounge_client::send_heroms_exp_get(` @ `0xeed390`
- opcode 写入：`0xba6d3c`
- 声明容量：`0xE`（分配器容量 `push` @ `0xba6d06`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xba6d0a  mov     ebp, eax
  0xba6d0c  mov     eax, [edi+0Ch]
  0xba6d0f  push    eax
  0xba6d10  lea     ecx, [esp+4Ch+var_34]
  0xba6d14  call    sub_ABB2F0
  0xba6d19  lea     ecx, [ebp+0Eh]
  0xba6d1c  lea     eax, [ebp+2]
  0xba6d1f  cmp     eax, ecx
  0xba6d21  mov     [esp+48h+var_4], 0
  0xba6d29  mov     [esp+48h+var_30], ebp
  0xba6d2d  mov     dword ptr [esp+48h+var_2C], ecx
  0xba6d31  ja      loc_BA6EE5
  0xba6d37  lea     edx, [eax+4]
  0xba6d3a  cmp     edx, ecx
  0xba6d3c  mov     word ptr [ebp+0], 76F2h
  0xba6d42  ja      loc_BA6EE5
  0xba6d48  mov     esi, [esp+48h+arg_0]
  0xba6d4c  mov     [eax], esi
  0xba6d4e  mov     eax, edx
  0xba6d50  lea     edx, [eax+4]
  0xba6d53  cmp     edx, ecx
  0xba6d55  ja      loc_BA6EE5
  0xba6d5b  mov     ecx, [esp+48h+arg_4]
  0xba6d5f  mov     [esp+48h+var_30], edx
  0xba6d63  lea     edx, [esp+48h+var_30]
  0xba6d67  mov     [eax], ecx
  0xba6d69  push    edx
  0xba6d6a  lea     eax, [esp+4Ch+arg_8]
  0xba6d6e  push    eax
  0xba6d6f  call    sub_B02D80
  0xba6d74  add     esp, 8
  0xba6d77  test    al, al
  0xba6d79  jz      loc_BA6EE5
  0xba6d7f  mov     esi, [edi+82B4h]
  0xba6d85  test    esi, esi
  0xba6d87  mov     ebx, [esp+48h+var_30]
  0xba6d8b  jz      loc_BA6E86
  0xba6d91  lea     ecx, [esp+48h+var_28]
  0xba6d95  push    ecx
  0xba6d96  call    sub_CA0CE0
  0xba6d9b  add     esp, 4
  0xba6d9e  mov     edx, [edi+8]
  0xba6da1  push    offset aProtoLoungeCli_587; ")<-_proto_lounge_client::send_heroms_ex"...
  0xba6da6  push    edx
  0xba6da7  push    offset aId; " (id:"
  0xba6dac  push    eax
  0xba6dad  push    esi
  0xba6dae  mov     byte ptr [esp+5Ch+var_4], 1
  0xba6db3  call    sub_B03020
  0xba6db8  add     esp, 8
  0xba6dbb  push    eax
  0xba6dbc  call    sub_41D990
  0xba6dc1  add     esp, 8
  0xba6dc4  mov     ecx, eax
  0xba6dc6  call    sub_ADC810
  0xba6dcb  push    eax
  0xba6dcc  call    sub_41D990
  0xba6dd1  add     esp, 8
  0xba6dd4  lea     ecx, [esp+48h+var_28]
  0xba6dd8  mov     byte ptr [esp+48h+var_4], 0
  0xba6ddd  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xba6dec  push    offset aPilotId; "pilot_id="
  0xba6e14  push    offset aWorldId; "world_id="
  0xba6e37  push    offset aFavmsId; "favms_id="
  0xba6e4c  push    offset aByte; "]byte"
  0xba6e56  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xba6e88  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xba6d3c` | u16 |
| `pilot_id` | `0xBA6D4C` | u32 |
| `world_id` | `0xBA6D67` | u32 |
| `favms_id` | `0xBA6D6F` | u32 |
