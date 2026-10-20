# 汇编证据 —— CS-0xC6E3-lounge-clan_memberlist_get

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB9F4F0`（`0xB9F4F0`..`0xB9F69E`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_memberlist_get(` @ `0xEEC72C`
- opcode 写入：`0xB9F564`
- 声明容量：`0x6`（分配器容量 `push` @ `0xB9F536`）
- 提交（`sub_B02FF0`）：`0xB9F5CF`
- 发送去向：`vt[0x58]` @ `0xB9F62C`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB9F536  push    0x6            ; 声明容量（不是线长）
  0xB9F564  mov     word ptr [buf], C6E3h   ; 字段 0 `opcode` => 2
  00b9f573  mov     [eax], cl                          ; 字段 1 `clan_kind` => u8 (arg_0)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "clan_kind="
```

## 4. 发送去向切片

```asm
  0xB9F62C  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9F564` | u16 / 2 |
| `clan_kind` | `0xB9F573` | u8 / 1 |
