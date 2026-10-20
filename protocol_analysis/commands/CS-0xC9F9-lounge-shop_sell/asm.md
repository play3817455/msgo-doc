# 汇编证据 —— CS-0xC9F9-lounge-shop_sell

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB9D180`（`0xB9D180`..`0xB9D44A`）
- 命令名字符串：`)<-_proto_lounge_client::send_shop_sell(` @ `0xEEC37C`
- opcode 写入：`0xB9D1FC`
- 声明容量：`0x1A`（分配器容量 `push` @ `0xB9D1C6`）
- 提交（`sub_B02FF0`）：`0xB9D2D6`
- 发送去向：`vt[0x58]` @ `0xB9D3D8`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB9D1C6  push    0x1A            ; 声明容量（不是线长）
  0xB9D1FC  mov     word ptr [buf], C9F9h   ; 字段 0 `opcode` => 2
  00b9d212  mov     [eax+4], esi                       ; 字段 1 `uniqid` => u64 (arg_0/4)
  00b9d224  mov     [edx], cl                          ; 字段 2 `id_type` => u8 (arg_8)
  00b9d234  call    sub_B02DA0                         ; 字段 3 `inv_place` => u16 (arg_C)
  00b9d24e  call    sub_B02D80                         ; 字段 4 `num` => u32 (arg_10)
  00b9d268  call    sub_B02D80                         ; 字段 5 `total_price` => u32 (arg_14)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "uniqid="
  push offset a<Name>; "id_type="
  push offset a<Name>; "inv_place="
  push offset a<Name>; "num="
  push offset a<Name>; "total_price="
```

## 4. 发送去向切片

```asm
  0xB9D3D8  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9D1FC` | u16 / 2 |
| `uniqid` | `0xB9D20C,0xB9D212` | u64 / 8 |
| `id_type` | `0xB9D224` | u8 / 1 |
| `inv_place` | `0xB9D234` | u16 / 2 |
| `num` | `0xB9D24E` | u32 / 4 |
| `total_price` | `0xB9D268` | u32 / 4 |
