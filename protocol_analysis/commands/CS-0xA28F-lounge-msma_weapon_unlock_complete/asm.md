# 汇编证据 —— CS-0xA28F-lounge-msma_weapon_unlock_complete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B97DC0 @ `0xB97DC0`（`0xB97DC0`..`0xB98046`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_weapon_unlock_complete(` @ `0xEEBB10`
- opcode 写入：`0xB97E3C`
- 声明容量：`0x0016`（分配器容量 `push` @ `0xB97E06`）
- 发送去向：`vt[0x58]` @ `0xB97FD4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b97e06  push    16h
  00b97e3c  mov     word ptr [ebp+0], 0A28Fh   ; 字段 0 `opcode` => 2
  00b97e4c  mov     [eax], esi   ; 字段 1 `uniqid_ms` => 8
  00b97e52  mov     [eax+4], esi   ; 字段 1 `uniqid_ms` => 8
  00b97e64  mov     [edx], ecx   ; 字段 2 `item_id` => 4
  00b97e74  call    sub_B02D80   ; 字段 3 `use_gp` => 4
  00b97e8e  call    sub_B02D80   ; 字段 4 `use_bc` => 4
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE41BC  push offset a<name>; "uniqid_ms="
  00EDB448  push offset a<name>; "item_id="
  00EE407C  push offset a<name>; "use_gp="
  00EE3FE4  push offset a<name>; "use_bc="
```

## 4. 发送去向切片

```asm
  00b97fd4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB97E3C` | u16 / 2 |
| `uniqid_ms` | `0xB97E4C, 0xB97E52` | u64 / 8 |
| `item_id` | `0xB97E64` | u32 / 4 |
| `use_gp` | `0xB97E74` | u32 / 4 |
| `use_bc` | `0xB97E8E` | u32 / 4 |
