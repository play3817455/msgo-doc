# 汇编证据 —— CS-0xC84F-battle-bullet_supply_r

> 所有地址为完整 VA（`VA = 文件偏移 + 0x400000`，无重定位），可在 IDA 中直接 `G` 跳转。

## 1. 代码位置

- `0xB3D8D0`（`0xB3D8D0`..`0xB3DABA`）
- 命令名字符串：`)<-_proto_battle_client::send_bullet_supply_r(` @ `0xEE1344`
- opcode 写入：`0xB3D944`
- 声明容量：`0xA`（分配器容量 `push` @ `0xB3D916`）
- 提交（`sub_B02FF0`）：`0xB3D9C5`
- 发送去向：`vt[0x58]` @ `0xB3DA48`

## 2. 组包块切片（容量申请 → opcode → 逐字段写线 → 提交）

```asm
  0xB3D916  push    0xA            ; 声明容量（不是线长）
  0xB3D944  mov     word ptr [buf], C84Fh   ; 字段 0 `opcode` => 2
  00b3d95a  mov     [eax], si                          ; 字段 1 `percent_val` => u16 (arg_0)
  00b3d968  mov     [edx], cx                          ; 字段 2 `equip_idx` => u16 (arg_4)
```

> `sub_B02D80`=写 u32 / `sub_B02DA0`=写 u16 / `sub_B061C0`=写 u8 / `sub_B06190`=写 u64 / `sub_B061E0`=写 f32 / `sub_B02B40`=写 NUL 串（**紧邻其前的 `push N`** = 串槽预算）；内联 `mov [reg],src` 宽度看操作数。

## 3. 提交后的 trace 打印块（字段名取证：日志名序 == 线序）

```asm
  push offset a<Name>; "percent_val="
  push offset a<Name>; "equip_idx="
```

## 4. 发送去向切片

```asm
  0xB3DA48  mov     eax, [edx+58h]
```

> `vt[0x58]` = 客户端对象虚表槽；实参 = `(buf, 负载长度)`（`sub <len>, <buf首址>` 即「游标 − 缓冲首址」）。

## 5. 字段证据索引

| 字段 | 证据 VA | 说明 |
|---|---|---|
| `opcode` | `0xB3D944` | u16 / 2 |
| `percent_val` | `0xB3D95A` | u16 / 2 |
| `equip_idx` | `0xB3D968` | u16 / 2 |
