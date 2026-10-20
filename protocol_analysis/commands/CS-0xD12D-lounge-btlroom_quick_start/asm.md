# 汇编证据 —— CS-0xD12D-lounge-btlroom_quick_start

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB8F830`（`0xB8F830`..`0xB8FABE`）
- 命令名字符串：`)<-_proto_lounge_client::send_btlroom_quick_start(` @ `0xEEAD84`
- opcode 写入：`0xB8F8AC`
- 声明容量：`0x5A`（分配器容量 `push` @ `0xB8F876`）
- 提交（`sub_B02FF0`）：`0xB8F969`
- 发送去向：`vt[0x58]` @ `0xB8FA4C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB8F876  push    0x5A            ; 声明容量（不是线长）
  0xB8F8AC  mov     word ptr [buf], D12Dh   ; 字段 0 `opcode` => 2
  00b8f8bc  mov     [eax], esi                         ; 字段 1 `matching_type` => u32 (arg_0)
  00b8f8d7  mov     [eax], ecx                         ; 字段 2 `is_coop` => u32 (arg_4)
  00b8f8df  call    sub_B02D80                         ; 字段 3 `mission_id` => u32 (arg_8)
  00b8f8fb  call    sub_B02B40                         ; 字段 4 `room_name_new` => bytes (arg_C)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "matching_type="
  push offset a<Name>; "is_coop="
  push offset a<Name>; "mission_id="
  push offset a<Name>; "room_name_new="
```

## 4. 发送去向切片

```asm
  0xB8FA4C  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB8F8AC` | u16 / 2 |
| `matching_type` | `0xB8F8BC` | u32 / 4 |
| `is_coop` | `0xB8F8D7` | u32 / 4 |
| `mission_id` | `0xB8F8DF` | u32 / 4 |
| `room_name_new` | `0xB8F8FB` | bytes / 可变 |
