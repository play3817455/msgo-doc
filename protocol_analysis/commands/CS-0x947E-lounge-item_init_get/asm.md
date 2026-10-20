# 汇编证据 —— CS-0x947E-lounge-item_init_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B99DE0 @ `0xb99de0`（`0xb99de0`..`0xb99f66`）
- 命令名字符串：`)<-_proto_lounge_client::send_item_init_get(` @ `0xeebe60`
- opcode 写入：`0xb99e39`
- 声明容量：`0x2`（分配器容量 `push` @ `0xb99e26`）

## 2. 组包块切片（游标初始化 → 逐字段写线 → 提交）

```asm
  0xb99e2a  mov     edi, eax
  0xb99e2c  mov     eax, [esi+0Ch]
  0xb99e2f  push    eax
  0xb99e30  lea     ecx, [esp+44h+var_2C]
  0xb99e34  call    sub_ABB2F0
  0xb99e39  mov     word ptr [edi], 947Eh
  0xb99e3e  mov     ebp, [esi+7EACh]
  0xb99e44  test    ebp, ebp
  0xb99e46  mov     [esp+40h+var_4], 0
  0xb99e4e  lea     ebx, [edi+2]
  0xb99e51  jz      loc_B99EE2
  0xb99e57  lea     ecx, [esp+40h+var_28]
  0xb99e5b  push    ecx
  0xb99e5c  call    sub_CA0CE0
  0xb99e61  add     esp, 4
  0xb99e64  mov     edx, [esi+8]
  0xb99e67  push    offset aProtoLoungeCli_396; ")<-_proto_lounge_client::send_item_init"...
  0xb99e6c  push    edx
  0xb99e6d  push    offset aId; " (id:"
  0xb99e72  push    eax
  0xb99e73  push    ebp
  0xb99e74  mov     byte ptr [esp+54h+var_4], 1
  0xb99e79  call    sub_B03020
  0xb99e7e  add     esp, 8
  0xb99e81  push    eax
  0xb99e82  call    sub_41D990
  0xb99e87  add     esp, 8
  0xb99e8a  mov     ecx, eax
  0xb99e8c  call    sub_ADC810
  0xb99e91  push    eax
  0xb99e92  call    sub_41D990
  0xb99e97  add     esp, 8
  0xb99e9a  lea     ecx, [esp+40h+var_28]
  0xb99e9e  mov     byte ptr [esp+40h+var_4], 0
  0xb99ea3  call    sub_B02FF0
```

> `sub_ABB2F0` = 用传输层缓冲初始化 `{cur,end}`；`sub_B02FF0` = 提交（组包结束标志）。
> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B02B40`=写 NUL 串（其**紧邻之前的 `push N`** = 串槽预算）。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  0xb99ea8  push    offset aByte; "]byte"
  0xb99eb2  push    offset asc_EDAD58; " ) ["
```

## 4. 发送去向切片

```asm
  0xb99ee4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xb99e39` | u16 |
