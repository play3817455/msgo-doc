# 汇编证据 —— CS-0xCC9F-lounge-clan_mshipbid_request

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB9FD10`（`0xB9FD10`..`0xB9FEF8`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_mshipbid_request(` @ `0xEEC7EC`
- opcode 写入：`0xB9FD84`
- 声明容量：`0xA`（分配器容量 `push` @ `0xB9FD56`）
- 提交（`sub_B02FF0`）：`0xB9FE01`
- 发送去向：`vt[0x58]` @ `0xB9FE86`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB9FD56  push    0xA            ; 声明容量（不是线长）
  0xB9FD84  mov     word ptr [buf], CC9Fh   ; 字段 0 `opcode` => 2
  00b9fd99  mov     [ecx], edi                         ; 字段 1 `clan_id` => u32 (arg_0)
  00b9fda5  mov     [edx], cl                          ; 字段 2 `clan_kind` => u8 (arg_4)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "clan_id="
  push offset a<Name>; "clan_kind="
```

## 4. 发送去向切片

```asm
  0xB9FE86  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9FD84` | u16 / 2 |
| `clan_id` | `0xB9FD99` | u32 / 4 |
| `clan_kind` | `0xB9FDA5` | u8 / 1 |
