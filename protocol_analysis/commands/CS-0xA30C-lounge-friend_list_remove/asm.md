# 汇编证据 —— CS-0xA30C-lounge-friend_list_remove

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9AC50 @ `0xB9AC50`（`0xB9AC50`..`0xB9ADFD`）
- 命令名字符串：`)<-_proto_lounge_client::send_friend_list_remove(` @ `0xEEC018`
- opcode 写入：`0xB9ACC4`
- 声明容量：`0x0006`（分配器容量 `push` @ `0xB9AC96`）
- 发送去向：`vt[0x58]` @ `0xB9AD8B`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b9ac96  push    6
  00b9acc4  mov     word ptr [ebp+0], 0A30Ch   ; 字段 0 `opcode` => 2
  00b9acd4  mov     [eax], ecx   ; 字段 1 `pilotid` => 4
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3D64  push offset a<name>; "pilotid="
```

## 4. 发送去向切片

```asm
  00b9ad8b  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9ACC4` | u16 / 2 |
| `pilotid` | `0xB9ACD4` | u32 / 4 |
