# 汇编证据 —— CS-0xBC92-lounge-msma_msset_del

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B98AA0 @ `0xB98AA0`（`0xB98AA0`..`0xB98C8A`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_msset_del(` @ `0xEEBC4C`
- opcode 写入：`0xB98B14`
- 声明容量：`0x000A`（分配器容量 `push` @ `0xB98AE6`）
- 发送去向：`vt[0x58]` @ `0xB98C18`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b98ae6  push    0Ah
  00b98b14  mov     word ptr [ebp+0], 0BC92h   ; 字段 0 `opcode` => 2
  00b98b2a  mov     [eax], si   ; 字段 1 `deck_type` => 2
  00b98b38  mov     [edx], cx   ; 字段 2 `slot` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE2590  push offset a<name>; "deck_type="
  00EE25EC  push offset a<name>; "slot="
```

## 4. 发送去向切片

```asm
  00b98c18  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB98B14` | u16 / 2 |
| `deck_type` | `0xB98B2A` | u16 / 2 |
| `slot` | `0xB98B38` | u16 / 2 |
