# 汇编证据 —— CS-0xAD81-lounge-gacha_exec

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9E000 @ `0xB9E000`（`0xB9E000`..`0xB9E23C`）
- 命令名字符串：`)<-_proto_lounge_client::send_gacha_exec(` @ `0xEEC4F8`
- opcode 写入：`0xB9E07C`
- 声明容量：`0x000E`（分配器容量 `push` @ `0xB9E046`）
- 发送去向：`vt[0x58]` @ `0xB9E1CA`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b9e046  push    0Eh
  00b9e07c  mov     word ptr [ebp+0], 0AD81h   ; 字段 0 `opcode` => 2
  00b9e08c  mov     [eax], esi   ; 字段 1 `gacha_id` => 4
  00b9e0a7  mov     [eax], ecx   ; 字段 2 `exec_type` => 4
  00b9e0af  call    sub_B061C0   ; 字段 3 `is_bundle` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE373C  push offset a<name>; "gacha_id="
  00EE3C64  push offset a<name>; "exec_type="
  00EE3C58  push offset a<name>; "is_bundle="
```

## 4. 发送去向切片

```asm
  00b9e1ca  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9E07C` | u16 / 2 |
| `gacha_id` | `0xB9E08C` | u32 / 4 |
| `exec_type` | `0xB9E0A7` | u32 / 4 |
| `is_bundle` | `0xB9E0AF` | u8 / 1 |
