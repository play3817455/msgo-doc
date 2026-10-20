# 汇编证据 —— CS-0x7A29-lounge-pilot_tutorial_step_skip

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B8B1A0 @ `0xb8b1a0`（`0xb8b1a0`..`0xb8b380`）
- 命令名字符串：`)<-_proto_lounge_client::send_pilot_tutorial_step_skip(` @ `0xeea4d4`
- opcode 写入：`0xb8b211`
- 声明容量：`0xA`（分配器容量 `push` @ `0xb8b1e3`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb8b1e7  mov     ebp, eax
  0xb8b1e9  mov     eax, [edi+0Ch]
  0xb8b1ec  push    eax
  0xb8b1ed  lea     ecx, [esp+44h+var_2C]
  0xb8b1f1  call    sub_ABB2F0
  0xb8b1f6  lea     ecx, [ebp+0Ah]
  0xb8b1f9  lea     eax, [ebp+2]
  0xb8b1fc  cmp     eax, ecx
  0xb8b1fe  mov     [esp+40h+var_4], 0
  0xb8b206  ja      loc_B8B36B
  0xb8b20c  lea     edx, [eax+4]
  0xb8b20f  cmp     edx, ecx
  0xb8b211  mov     word ptr [ebp+0], 7A29h
  0xb8b217  ja      loc_B8B36B
  0xb8b21d  mov     esi, [esp+40h+arg_0]
  0xb8b221  lea     ebx, [edx+4]
  0xb8b224  cmp     ebx, ecx
  0xb8b226  mov     [eax], esi
  0xb8b228  ja      loc_B8B36B
  0xb8b22e  mov     ecx, [esp+40h+arg_4]
  0xb8b232  mov     [edx], ecx
  0xb8b234  mov     esi, [edi+7A2Ch]
  0xb8b23a  test    esi, esi
  0xb8b23c  jz      loc_B8B30F
  0xb8b242  lea     edx, [esp+40h+var_28]
  0xb8b246  push    edx
  0xb8b247  call    sub_CA0CE0
  0xb8b24c  add     esp, 4
  0xb8b24f  mov     ecx, [edi+8]
  0xb8b252  push    offset aProtoLoungeCli_353; ")<-_proto_lounge_client::send_pilot_tut"...
  0xb8b257  push    ecx
  0xb8b258  push    offset aId; " (id:"
  0xb8b25d  push    eax
  0xb8b25e  push    esi
  0xb8b25f  mov     byte ptr [esp+54h+var_4], 1
  0xb8b264  call    sub_B03020
  0xb8b269  add     esp, 8
  0xb8b26c  push    eax
  0xb8b26d  call    sub_41D990
  0xb8b272  add     esp, 8
  0xb8b275  mov     ecx, eax
  0xb8b277  call    sub_ADC810
  0xb8b27c  push    eax
  0xb8b27d  call    sub_41D990
  0xb8b282  add     esp, 8
  0xb8b285  lea     ecx, [esp+40h+var_28]
  0xb8b289  mov     byte ptr [esp+40h+var_4], 0
  0xb8b28e  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb8b29d  push    offset aTutoStepNow; "tuto_step_now="
  0xb8b2c0  push    offset aTutoStepNext; "tuto_step_next="
  0xb8b2d5  push    offset aByte; "]byte"
  0xb8b2df  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb8b311  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb8b211` | u16 |
| `tuto_step_now` | `0xB8B226` | u32 |
| `tuto_step_next` | `0xB8B232` | u32 |
