# 汇编证据 —— CS-0xD191-lounge-gacha_effect_stop

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB9E5D0`（`0xB9E5D0`..`0xB9E756`）
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_effect_stop(` @ `0xEEC55C`
- opcode 写入：`0xB9E629`
- 声明容量：`0x2`（分配器容量 `push` @ `0xB9E616`）
- 提交（`sub_B02FF0`）：`0xB9E693`
- 发送去向：`vt[0x58]` @ `0xB9E6D4`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB9E616  push    0x2            ; 声明容量（不是线长）
  0xB9E629  mov     word ptr [buf], D191h   ; 字段 0 `opcode` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  （零负载命令：无字段日志）
```

## 4. 发送去向切片

```asm
  0xB9E6D4  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9E629` | u16 / 2 |
