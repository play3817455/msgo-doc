# 汇编证据 —— CS-0xA5BC-lounge-clan_create

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- sub_B9F830 @ `0xB9F830`（`0xB9F830`..`0xB9FAC7`）
- 命令名字符串：`)<-_proto_lounge_client::send_clan_create(` @ `0xEEC794`
- opcode 写入：`0xB9F8AC`
- 声明容量：`0x002E`（分配器容量 `push` @ `0xB9F876`）
- 发送去向：`vt[0x58]` @ `0xB9FA55`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  00b9f876  push    2Eh ; '.'
  00b9f8ac  mov     word ptr [ebp+0], 0A5BCh   ; 字段 0 `opcode` => 2
  00b9f8c6  mov     [eax], ecx   ; 字段 1 `npc_id` => 4
  00b9f8ce  call    sub_B02B40   ; 字段 2 `clan_name` => var(≤31)
  00b9f8e8  call    sub_B02D80   ; 字段 3 `is_active` => 4
  00b9f902  call    sub_B061C0   ; 字段 4 `clan_kind` => 1
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 /
> `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  00EE3390  push offset a<name>; "npc_id="
  00EDCA98  push offset a<name>; "clan_name=""
  00EE3ED4  push offset a<name>; "is_active="
  00EE3398  push offset a<name>; "clan_kind="
```

## 4. 发送去向切片

```asm
  00b9fa55  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB9F8AC` | u16 / 2 |
| `npc_id` | `0xB9F8C6` | u32 / 4 |
| `clan_name` | `0xB9F8CE` | str / var(≤31) |
| `is_active` | `0xB9F8E8` | u32 / 4 |
| `clan_kind` | `0xB9F902` | u8 / 1 |
