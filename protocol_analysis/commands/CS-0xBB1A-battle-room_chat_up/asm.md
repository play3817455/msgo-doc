# 汇编证据 —— CS-0xBB1A-battle-room_chat_up

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B32CF0 @ `0xB32CF0`（`0xB32CF0`..`0xB32F0D`）
- 命令名字符串：`)<-_proto_battle_client::send_room_chat_up(` @ `0xEE07A4`
- opcode 写入：`0xB32D7C`
- 声明容量：`0x00BE`（分配器容量 `push` @ `0xB32D36`）
- 发送去向：`vt[0x58]` @ `0xB32E9C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b32d36  push    0BEh
  00b32d7c  mov     word ptr [ebp+0], 0BB1Ah   ; 字段 0 `opcode` => 2
  00b32d86  call    sub_B02B40   ; 字段 1 `msg` => var(≤181)
  00b32dab  mov     [eax], cl   ; 字段 2 `is_party` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDC7B8  push offset a<name>; "msg=""
  00EDC380  push offset a<name>; "is_party="
```

## 4. 发送去向切片

```asm
  00b32e9c  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB32D7C` | u16 / 2 |
| `msg` | `0xB32D86` | str / var(≤181) |
| `is_party` | `0xB32DAB` | u8 / 1 |
