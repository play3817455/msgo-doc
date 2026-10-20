# 汇编证据 —— CS-0xC166-battle-eqparts_ready_start

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB3C290`（`0xB3C290`..`0xB3C50E`）
- 命令名字符串：`)<-_proto_battle_client::send_eqparts_ready_start(` @ `0xEE1128`
- opcode 写入：`0xB3C30C`
- 声明容量：`0x12`（分配器容量 `push` @ `0xB3C2D6`）
- 提交（`sub_B02FF0`）：`0xB3C3C7`
- 发送去向：`vt[0x58]` @ `0xB3C49C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB3C2D6  push    0x12            ; 声明容量（不是线长）
  0xB3C30C  mov     word ptr [buf], C166h   ; 字段 0 `opcode` => 2
  00b3c31c  mov     [ecx], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b3c336  mov     [edx], ax                          ; 字段 2 `AI_ent_id` => u16 (arg_4)
  00b3c33f  call    sub_B02DA0                         ; 字段 3 `group_id` => u16 (arg_8)
  00b3c359  call    sub_B061C0                         ; 字段 4 `reason` => u8 (arg_C)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "AI_ent_id="
  push offset a<Name>; "group_id="
  push offset a<Name>; "reason="
```

## 4. 发送去向切片

```asm
  0xB3C49C  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3C30C` | u16 / 2 |
| `frame_count` | `0xB3C31C` | u32 / 4 |
| `AI_ent_id` | `0xB3C336` | u16 / 2 |
| `group_id` | `0xB3C33F` | u16 / 2 |
| `reason` | `0xB3C359` | u8 / 1 |
