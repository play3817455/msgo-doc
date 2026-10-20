# 汇编证据 —— CS-0xBA4E-lounge-friend_list_mail_accept

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9AA50 @ `0xB9AA50`（`0xB9AA50`..`0xB9AC42`）
- 命令名字符串：`)<-_proto_lounge_client::send_friend_list_mail_accept(` @ `0xEEBFE0`
- opcode 写入：`0xB9AAC4`
- 声明容量：`0x000E`（分配器容量 `push` @ `0xB9AA96`）
- 发送去向：`vt[0x58]` @ `0xB9ABD0`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b9aa96  push    0Eh
  00b9aac4  mov     word ptr [ebp+0], 0BA4Eh   ; 字段 0 `opcode` => 2
  00b9aad4  mov     [eax], esi   ; 字段 1 `mailid` => 8
  00b9aadf  mov     [eax+4], esi   ; 字段 1 `mailid` => 8
  00b9aaec  mov     [edx], ecx   ; 字段 2 `pilotid` => 4
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3254  push offset a<name>; "mailid="
  00EE3D64  push offset a<name>; "pilotid="
```

## 4. 发送去向切片

```asm
  00b9abd0  mov     edx, [eax+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9AAC4` | u16 / 2 |
| `mailid` | `0xB9AAD4, 0xB9AADF` | u64 / 8 |
| `pilotid` | `0xB9AAEC` | u32 / 4 |
