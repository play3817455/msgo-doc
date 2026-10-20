# 汇编证据 —— CS-0xC59B-lounge-clan_text_notice_set

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xBA0D30`（`0xBA0D30`..`0xBA0F50`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_text_notice_set(` @ `0xEEC9A0`
- opcode 写入：`0xBA0DBC`
- 声明容量：`0x1BA`（分配器容量 `push` @ `0xBA0D76`）
- 提交（`sub_B02FF0`）：`0xBA0E47`
- 发送去向：`vt[0x58]` @ `0xBA0EDC`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xBA0D76  push    0x1BA            ; 声明容量（不是线长）
  0xBA0DBC  mov     word ptr [buf], C59Bh   ; 字段 0 `opcode` => 2
  00ba0dc6  call    sub_B02B40                         ; 字段 1 `body` => bytes (arg_0)
  00ba0deb  mov     [eax], cl                          ; 字段 2 `clan_kind` => u8 (arg_4)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "body="
  push offset a<Name>; "clan_kind="
```

## 4. 发送去向切片

```asm
  0xBA0EDC  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xBA0DBC` | u16 / 2 |
| `body` | `0xBA0DC6` | bytes / 可变 |
| `clan_kind` | `0xBA0DEB` | u8 / 1 |
