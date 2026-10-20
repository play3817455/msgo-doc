# 汇编证据 —— CS-0x9883-lounge-msma_buildup

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B962C0 @ `0xB962C0`（`0xB962C0`..`0xB96546`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_buildup(` @ `0xEEB890`
- opcode 写入：`0xB9633C`
- 声明容量：`0x0016`（分配器容量 `push` @ `0xB96306`）
- 发送去向：`vt[0x58]` @ `0xB964D4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b96306  push    16h
  00b9633c  mov     word ptr [ebp+0], 9883h   ; 字段 0 `opcode` => 2
  00b9634c  mov     [eax], esi   ; 字段 1 `uniqid_ms` => 8
  00b96352  mov     [eax+4], esi   ; 字段 1 `uniqid_ms` => 8
  00b96364  mov     [edx], ecx   ; 字段 2 `ticket_id` => 4
  00b96374  call    sub_B02DA0   ; 字段 3 `usenum` => 2
  00b9638e  call    sub_B02DA0   ; 字段 4 `param_idx` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE41BC  push offset a<name>; "uniqid_ms="
  00EE41B0  push offset a<name>; "ticket_id="
  00EE41A8  push offset a<name>; "usenum="
  00EE419C  push offset a<name>; "param_idx="
```

## 4. 发送去向切片

```asm
  00b964d4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9633C` | u16 / 2 |
| `uniqid_ms` | `0xB9634C, 0xB96352` | u64 / 8 |
| `ticket_id` | `0xB96364` | u32 / 4 |
| `usenum` | `0xB96374` | u16 / 2 |
| `param_idx` | `0xB9638E` | u16 / 2 |
