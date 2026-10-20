# 汇编证据 —— CS-0xA537-battle-roomlobby_xwar_commander_lot

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B31FD0 @ `0xB31FD0`（`0xB31FD0`..`0xB32178`）
- 命令名字符串：`)<-_proto_battle_client::send_roomlobby_xwar_commander_lot(` @ `0xEE05E4`
- opcode 写入：`0xB32041`
- 声明容量：`0x0006`（分配器容量 `push` @ `0xB32013`）
- 发送去向：`vt[0x58]` @ `0xB32109`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b32013  push    6
  00b32041  mov     word ptr [edi], 0A537h   ; 字段 0 `opcode` => 2
  00b32050  mov     [eax], cl   ; 字段 1 `is_lot` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC2E8  push offset a<name>; "is_lot="
```

## 4. 发送去向切片

```asm
  00b32109  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB32041` | u16 / 2 |
| `is_lot` | `0xB32050` | u8 / 1 |
