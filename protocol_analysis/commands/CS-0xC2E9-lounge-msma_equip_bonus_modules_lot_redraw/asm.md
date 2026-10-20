# 汇编证据 —— CS-0xC2E9-lounge-msma_equip_bonus_modules_lot_redraw

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB94030`（`0xB94030`..`0xB94274`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_equip_bonus_modules_lot_redraw(` @ `0xEEB500`
- opcode 写入：`0xB940AC`
- 声明容量：`0x12`（分配器容量 `push` @ `0xB94076`）
- 提交（`sub_B02FF0`）：`0xB94152`
- 发送去向：`vt[0x58]` @ `0xB94202`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB94076  push    0x12            ; 声明容量（不是线长）
  0xB940AC  mov     word ptr [buf], C2E9h   ; 字段 0 `opcode` => 2
  00b940c2  mov     [eax+4], esi                       ; 字段 1 `uniqid_ms` => u64 (arg_0/4)
  00b940d4  mov     [edx], ecx                         ; 字段 2 `item_id` => u32 (arg_8)
  00b940e4  call    sub_B02D80                         ; 字段 3 `status` => u32 (arg_C)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "uniqid_ms="
  push offset a<Name>; "item_id="
  push offset a<Name>; "status="
```

## 4. 发送去向切片

```asm
  0xB94202  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB940AC` | u16 / 2 |
| `uniqid_ms` | `0xB940BC,0xB940C2` | u64 / 8 |
| `item_id` | `0xB940D4` | u32 / 4 |
| `status` | `0xB940E4` | u32 / 4 |
