# 汇编证据 —— CS-0xBB6D-battle-xwar_commander_subcmdr_lot

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B3ECC0 @ `0xB3ECC0`（`0xB3ECC0`..`0xB3EE6E`）
- 命令名字符串：`)<-_proto_battle_client::send_xwar_commander_subcmdr_lot(` @ `0xEE153C`
- opcode 写入：`0xB3ED34`
- 声明容量：`0x0006`（分配器容量 `push` @ `0xB3ED06`）
- 发送去向：`vt[0x58]` @ `0xB3EDFC`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b3ed06  push    6
  00b3ed34  mov     word ptr [edi], 0BB6Dh   ; 字段 0 `opcode` => 2
  00b3ed43  mov     [eax], cl   ; 字段 1 `is_lot` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC2E8  push offset a<name>; "is_lot="
```

## 4. 发送去向切片

```asm
  00b3edfc  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3ED34` | u16 / 2 |
| `is_lot` | `0xB3ED43` | u8 / 1 |
