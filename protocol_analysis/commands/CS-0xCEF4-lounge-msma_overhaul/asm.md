# 汇编证据 —— CS-0xCEF4-lounge-msma_overhaul

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB982A0`（`0xB982A0`..`0xB984E4`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_overhaul(` @ `0xEEBB80`
- opcode 写入：`0xB9831C`
- 声明容量：`0x12`（分配器容量 `push` @ `0xB982E6`）
- 提交（`sub_B02FF0`）：`0xB983C2`
- 发送去向：`vt[0x58]` @ `0xB98472`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB982E6  push    0x12            ; 声明容量（不是线长）
  0xB9831C  mov     word ptr [buf], CEF4h   ; 字段 0 `opcode` => 2
  00b98332  mov     [eax+4], esi                       ; 字段 1 `uniqid_ms` => u64 (arg_0/4)
  00b98344  mov     [edx], ecx                         ; 字段 2 `ms_plan_id` => u32 (arg_8)
  00b98354  call    sub_B02D80                         ; 字段 3 `ms_plan_num` => u32 (arg_C)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "uniqid_ms="
  push offset a<Name>; "ms_plan_id="
  push offset a<Name>; "ms_plan_num="
```

## 4. 发送去向切片

```asm
  0xB98472  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9831C` | u16 / 2 |
| `uniqid_ms` | `0xB9832C,0xB98332` | u64 / 8 |
| `ms_plan_id` | `0xB98344` | u32 / 4 |
| `ms_plan_num` | `0xB98354` | u32 / 4 |
