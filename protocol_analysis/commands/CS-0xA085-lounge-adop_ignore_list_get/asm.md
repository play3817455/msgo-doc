# 汇编证据 —— CS-0xA085-lounge-adop_ignore_list_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B89E00 @ `0xB89E00`（`0xB89E00`..`0xB89F80`）
- 命令名字符串：`)<-_proto_lounge_client::send_adop_ignore_list_get(` @ `0xEEA2D8`
- opcode 写入：`0xB89E56`
- 声明容量：`0x0002`（分配器容量 `push` @ `0xB89E43`）
- 发送去向：`vt[0x58]` @ `0xB89F01`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b89e43  push    2
  00b89e56  mov     word ptr [edi], 0A085h   ; 字段 0 `opcode` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
```

## 4. 发送去向切片

```asm
  00b89f01  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB89E56` | u16 / 2 |
