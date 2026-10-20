# 汇编证据 —— CS-0xBCA5-battle-dynamic_taskforce_order_change_party

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3F780 @ `0xB3F780`（`0xB3F780`..`0xB3F968`）
- 命令名字符串：`)<-_proto_battle_client::send_dynamic_taskforce_order_change_party(` @ `0xEE1688`
- opcode 写入：`0xB3F7F4`
- 声明容量：`0x000A`（分配器容量 `push` @ `0xB3F7C6`）
- 发送去向：`vt[0x58]` @ `0xB3F8F6`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b3f7c6  push    0Ah
  00b3f7f4  mov     word ptr [ebp+0], 0BCA5h   ; 字段 0 `opcode` => 2
  00b3f809  mov     [ecx], dl   ; 字段 1 `order_kind` => 1
  00b3f815  mov     [edi], eax   ; 字段 2 `order_param` => 4
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDB770  push offset a<name>; "order_kind="
  00EDB760  push offset a<name>; "order_param="
```

## 4. 发送去向切片

```asm
  00b3f8f6  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3F7F4` | u16 / 2 |
| `order_kind` | `0xB3F809` | u8 / 1 |
| `order_param` | `0xB3F815` | u32 / 4 |
