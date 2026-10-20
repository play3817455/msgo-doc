# 汇编证据 —— CS-0xF20B-lounge-replay_auth_get_downloadkey

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0x00BA4970`（`0x00BA4970`..`0x00BA4AF6`），函数 `sub_BA4970`
- 命令名字符串：`)<-_proto_lounge_client::send_replay_auth_get_downloadkey(` @ `0x00EECFDC`
- opcode 写入：`0x00BA49C9`
- 声明容量：`0x2`（分配器容量 `push` @ `0x00BA49B6`）
- 提交（`sub_B02FF0`）：`0x00BA4A33`
- 发送去向：`vt[0x58]` @ `0x00BA4A74`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00BA49BF  push    eax
  00BA49C0  lea     ecx, [esp+44h+var_2C]
  00BA49C4  call    sub_ABB2F0   ; <<< 初始化 {cur,end}（游标自 buf+2 起）
  00BA49C9  mov     word ptr [edi], 0F20Bh   ; <<< 内联写线（u16）
  00BA49CE  mov     ebp, [esi+81D4h]
  00BA49D4  test    ebp, ebp
  00BA49D6  mov     [esp+40h+var_4], 0
  00BA49DE  lea     ebx, [edi+2]
  00BA49E1  jz      loc_BA4A72
  00BA49E7  lea     ecx, [esp+40h+var_28]
  00BA49EB  push    ecx
  00BA49EC  call    sub_CA0CE0
  00BA49F1  add     esp, 4
  00BA49F4  mov     edx, [esi+8]
  00BA49F7  push    offset aProtoLoungeCli_539
  00BA49FC  push    edx
  00BA49FD  push    offset aId
  00BA4A02  push    eax
  00BA4A03  push    ebp
  00BA4A04  mov     byte ptr [esp+54h+var_4], 1
  00BA4A09  call    sub_B03020
  00BA4A0E  add     esp, 8
  00BA4A11  push    eax
  00BA4A12  call    sub_41D990
  00BA4A17  add     esp, 8
  00BA4A1A  mov     ecx, eax
  00BA4A1C  call    sub_ADC810
  00BA4A21  push    eax
  00BA4A22  call    sub_41D990
  00BA4A27  add     esp, 8
  00BA4A2A  lea     ecx, [esp+40h+var_28]
  00BA4A2E  mov     byte ptr [esp+40h+var_4], 0
  00BA4A33  call    sub_B02FF0   ; <<< 提交（C→S 闭合点）
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00BA4A33  call    sub_B02FF0
  00BA4A38  push    offset aByte
  00BA4A3D  mov     eax, ebx
  00BA4A3F  sub     eax, edi
  00BA4A41  push    eax
  00BA4A42  push    offset asc_EDAD58
  00BA4A47  push    ebp
  00BA4A48  call    sub_41D990
  00BA4A4D  add     esp, 8
  00BA4A50  mov     ecx, eax
  00BA4A52  call    sub_B03580
  00BA4A57  push    eax
  00BA4A58  call    sub_41D990
  00BA4A5D  add     esp, 8
  00BA4A60  mov     ebp, eax
  00BA4A62  push    0Ah
  00BA4A64  mov     ecx, ebp
  00BA4A66  call    sub_B036E0
  00BA4A6B  mov     ecx, ebp
  00BA4A6D  call    sub_40DDF0
  00BA4A72  mov     edx, [esi]
  00BA4A74  mov     eax, [edx+58h]
```

## 4. 发送去向切片

```asm
  00BA4A72  mov     edx, [esi]
  00BA4A74  mov     eax, [edx+58h]
  00BA4A77  sub     ebx, edi
  00BA4A79  push    ebx
  00BA4A7A  push    edi
  00BA4A7B  mov     ecx, esi
  00BA4A7D  call    eax
  00BA4A7F  test    al, al
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `00BA49C9` | u16 / 2 |
