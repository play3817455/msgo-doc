# 汇编证据 —— CS-0xD9AE-lounge-ranking_pilot_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xBA3650`（`0xBA3650`..`0xBA3819`）
- 命令名字符串：`)<-_proto_lounge_client::send_ranking_pilot_get(` @ `0xEECDF4`
- opcode 写入：`0xBA36D1`
- 声明容量：`0xE`（分配器容量 `push` @ `0xBA3696`）
- 提交（`sub_B02FF0`）：`0xBA3748`
- 发送去向：`vt[0x58]` @ `0xBA37A5`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xBA3696  push    0xE            ; 声明容量（不是线长）
  0xBA36D1  mov     word ptr [buf], D9AEh   ; 字段 0 `opcode` => 2
  00ba36da  call    sub_B42060                         ; 字段 1 `order` => struct (arg_0)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "order="
```

## 4. 发送去向切片

```asm
  0xBA37A5  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA36D1` | u16 / 2 |
| `order` | `0xBA36DA` | struct / 10 |
