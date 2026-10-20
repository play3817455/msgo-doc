# 汇编证据 —— CS-0xB235-lounge-season_rankerbattle_get_entitled_pilot_list

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA7B10 @ `0xBA7B10`（`0xBA7B10`..`0xBA7CD9`）
- 命令名字符串：`)<-_proto_lounge_client::send_season_rankerbattle_get_entitled_pilot_list(` @ `0xEED548`
- opcode 写入：`0xBA7B91`
- 声明容量：`0x000E`（分配器容量 `push` @ `0xBA7B56`）
- 发送去向：`vt[0x58]` @ `0xBA7C65`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00ba7b56  push    0Eh
  00ba7b91  mov     word ptr [edi], 0B235h   ; 字段 0 `opcode` => 2
  00b42073  mov     si, [ecx]   ; 字段 1 `order.kind` => 2
  00b42086  mov     si, [ecx+2]   ; 字段 2 `order.term` => 2
  00b4209a  mov     si, [ecx+4]   ; 字段 3 `order.filter` => 2
  00b420ae  mov     si, [ecx+6]   ; 字段 4 `order.reason` => 2
  00b420bd  call    sub_B02DA0   ; 字段 5 `order.troops` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE4194  push offset a<name>; "order="
```

## 4. 发送去向切片

```asm
  00ba7c65  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA7B91` | u16 / 2 |
| `order.kind` | `0xB42073` | u16 / 2 |
| `order.term` | `0xB42086` | u16 / 2 |
| `order.filter` | `0xB4209A` | u16 / 2 |
| `order.reason` | `0xB420AE` | u16 / 2 |
| `order.troops` | `0xB420BD` | u16 / 2 |
