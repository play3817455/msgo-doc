# 汇编证据 —— CS-0xCAAE-battle-object_put

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB35D60`（`0xB35D60`..`0xB360A1`）
- 命令名字符串：`)<-_proto_battle_client::send_object_put(` @ `0xEE0BC0`
- opcode 写入：`0xB35DDC`
- 声明容量：`0x1E`（分配器容量 `push` @ `0xB35DA6`）
- 提交（`sub_B02FF0`）：`0xB35EE5`
- 发送去向：`vt[0x58]` @ `0xB36032`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB35DA6  push    0x1E            ; 声明容量（不是线长）
  0xB35DDC  mov     word ptr [buf], CAAEh   ; 字段 0 `opcode` => 2
  00b35dec  mov     [ecx], esi                         ; 字段 1 `frame_count` => u32 (arg_0)
  00b35e06  mov     [edx], ax                          ; 字段 2 `target_x` => u16 (arg_4)
  00b35e0f  call    sub_B02DA0                         ; 字段 3 `target_y` => u16 (arg_8)
  00b35e29  call    sub_B02DA0                         ; 字段 4 `target_z` => u16 (arg_C)
  00b35e43  call    sub_B02DA0                         ; 字段 5 `attach_parent_ent_id` => u16 (arg_10)
  00b35e5d  call    sub_B061C0                         ; 字段 6 `is_initiation` => u8 (arg_14)
  00b35e77  call    sub_B02DA0                         ; 字段 7 `AI_ent_id` => u16 (arg_18)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "frame_count="
  push offset a<Name>; "target_x="
  push offset a<Name>; "target_y="
  push offset a<Name>; "target_z="
  push offset a<Name>; "attach_parent_ent_id="
  push offset a<Name>; "is_initiation="
  push offset a<Name>; "AI_ent_id="
```

## 4. 发送去向切片

```asm
  0xB36032  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB35DDC` | u16 / 2 |
| `frame_count` | `0xB35DEC` | u32 / 4 |
| `target_x` | `0xB35E06` | u16 / 2 |
| `target_y` | `0xB35E0F` | u16 / 2 |
| `target_z` | `0xB35E29` | u16 / 2 |
| `attach_parent_ent_id` | `0xB35E43` | u16 / 2 |
| `is_initiation` | `0xB35E5D` | u8 / 1 |
| `AI_ent_id` | `0xB35E77` | u16 / 2 |
