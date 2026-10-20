# 汇编证据 —— CS-0xC6E2-lounge-msma_buyback

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB99A20`（`0xB99A20`..`0xB99C12`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_buyback(` @ `0xEEBDFC`
- opcode 写入：`0xB99A94`
- 声明容量：`0xE`（分配器容量 `push` @ `0xB99A66`）
- 提交（`sub_B02FF0`）：`0xB99B18`
- 发送去向：`vt[0x58]` @ `0xB99BA0`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB99A66  push    0xE            ; 声明容量（不是线长）
  0xB99A94  mov     word ptr [buf], C6E2h   ; 字段 0 `opcode` => 2
  00b99aaf  mov     [eax+4], esi                       ; 字段 1 `uniqid_ms` => u64 (arg_0/4)
  00b99abc  mov     [edx], ecx                         ; 字段 2 `price` => u32 (arg_8)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "uniqid_ms="
  push offset a<Name>; "price="
```

## 4. 发送去向切片

```asm
  0xB99BA0  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB99A94` | u16 / 2 |
| `uniqid_ms` | `0xB99AA4,0xB99AAF` | u64 / 8 |
| `price` | `0xB99ABC` | u32 / 4 |
