# 汇编证据 —— CS-0xB567-lounge-msma_create

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B95A40 @ `0xB95A40`（`0xB95A40`..`0xB95C7A`）
- 命令名字符串：`)<-_proto_lounge_client::send_msma_create(` @ `0xEEB7C4`
- opcode 写入：`0xB95ABC`
- 声明容量：`0x000E`（分配器容量 `push` @ `0xB95A86`）
- 发送去向：`vt[0x58]` @ `0xB95C08`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b95a86  push    0Eh
  00b95abc  mov     word ptr [ebp+0], 0B567h   ; 字段 0 `opcode` => 2
  00b95acc  mov     [eax], esi   ; 字段 1 `ms_plan_id` => 4
  00b95ae7  mov     [eax], ecx   ; 字段 2 `ticket_id` => 4
  00b95aef  call    sub_B02DA0   ; 字段 3 `usenum` => 2
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3E54  push offset a<name>; "ms_plan_id="
  00EE41B0  push offset a<name>; "ticket_id="
  00EE41A8  push offset a<name>; "usenum="
```

## 4. 发送去向切片

```asm
  00b95c08  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB95ABC` | u16 / 2 |
| `ms_plan_id` | `0xB95ACC` | u32 / 4 |
| `ticket_id` | `0xB95AE7` | u32 / 4 |
| `usenum` | `0xB95AEF` | u16 / 2 |
