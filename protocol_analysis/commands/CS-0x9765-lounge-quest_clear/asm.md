# 汇编证据 —— CS-0x9765-lounge-quest_clear

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9D7B0 @ `0xB9D7B0`（`0xB9D7B0`..`0xB9D95D`）
- 命令名字符串：`)<-_proto_lounge_client::send_quest_clear(` @ `0xEEC410`
- opcode 写入：`0xB9D824`
- 声明容量：`0x0006`（分配器容量 `push` @ `0xB9D7F6`）
- 发送去向：`vt[0x58]` @ `0xB9D8EB`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b9d7f6  push    6
  00b9d824  mov     word ptr [ebp+0], 9765h   ; 字段 0 `opcode` => 2
  00b9d834  mov     [eax], ecx   ; 字段 1 `quest_id` => 4
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EDB3EC  push offset a<name>; "quest_id="
```

## 4. 发送去向切片

```asm
  00b9d8eb  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9D824` | u16 / 2 |
| `quest_id` | `0xB9D834` | u32 / 4 |
