# 汇编证据 —— CS-0xA791-lounge-clan_msgboard_msg_delete

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_BA2280 @ `0xBA2280`（`0xBA2280`..`0xBA2474`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_msgboard_msg_delete(` @ `0xEECBC4`
- opcode 写入：`0xBA22F4`
- 声明容量：`0x000E`（分配器容量 `push` @ `0xBA22C6`）
- 发送去向：`vt[0x58]` @ `0xBA2402`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00ba22c6  push    0Eh
  00ba22f4  mov     word ptr [ebp+0], 0A791h   ; 字段 0 `opcode` => 2
  00ba2304  mov     [eax], edi   ; 字段 1 `msg_id` => 8
  00ba230f  mov     [eax+4], edi   ; 字段 1 `msg_id` => 8
  00ba231c  mov     [edx], cl   ; 字段 2 `clan_kind` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE33DC  push offset a<name>; "msg_id="
  00EE3398  push offset a<name>; "clan_kind="
```

## 4. 发送去向切片

```asm
  00ba2402  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA22F4` | u16 / 2 |
| `msg_id` | `0xBA2304, 0xBA230F` | u64 / 8 |
| `clan_kind` | `0xBA231C` | u8 / 1 |
