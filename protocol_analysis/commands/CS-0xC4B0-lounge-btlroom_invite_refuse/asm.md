# 汇编证据 —— CS-0xC4B0-lounge-btlroom_invite_refuse

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB90390`（`0xB90390`..`0xB905CA`）
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_invite_refuse(` @ `0xEEAE48`
- opcode 写入：`0xB9040C`
- 声明容量：`0xE`（分配器容量 `push` @ `0xB903D6`）
- 提交（`sub_B02FF0`）：`0xB904AD`
- 发送去向：`vt[0x58]` @ `0xB90558`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB903D6  push    0xE            ; 声明容量（不是线长）
  0xB9040C  mov     word ptr [buf], C4B0h   ; 字段 0 `opcode` => 2
  00b9041c  mov     [eax], esi                         ; 字段 1 `room_id` => u32 (arg_0)
  00b90437  mov     [eax], ecx                         ; 字段 2 `pilot_id` => u32 (arg_4)
  00b9043f  call    sub_B02D80                         ; 字段 3 `reason` => u32 (arg_8)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "room_id="
  push offset a<Name>; "pilot_id="
  push offset a<Name>; "reason="
```

## 4. 发送去向切片

```asm
  0xB90558  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9040C` | u16 / 2 |
| `room_id` | `0xB9041C` | u32 / 4 |
| `pilot_id` | `0xB90437` | u32 / 4 |
| `reason` | `0xB9043F` | u32 / 4 |
